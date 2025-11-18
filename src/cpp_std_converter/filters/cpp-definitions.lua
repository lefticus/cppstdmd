--[[
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
]]

--[[
cpp-definitions.lua

Pandoc Lua filter to convert C++ standard definition entries.

Handles the intro.defs section which uses special definition macros:
- \definition{term}{label} → H4 heading with anchor
- \defncontext{context} → ⟨context⟩
- \begin{defnote}...\end{defnote} → [Note N to entry: ... — end note]

The tricky part: \definition, \defncontext, and the definition text
all appear as RawInline elements WITHIN THE SAME Para!
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local trim = common.trim
local build_defnote = common.build_defnote

-- Track definition and note counters
local definition_counter = 0
local note_counter = 0

-- Process blocks to split Paras containing definitions
function Blocks(blocks)
  local result = {}
  local pending_definition = nil
  local pending_context = nil

  for i, block in ipairs(blocks) do
    -- Check for \definition and \defncontext in RawBlock (separate from Para)
    if block.t == "RawBlock" and block.format == "latex" then
      local text = block.text
      -- Pattern: \definition{term}{label}
      -- NOTE: Using simple ([^}]*) is acceptable because definition terms and labels
      -- in the intro.defs section are simple text without nested braces.
      local term, label = text:match("\\definition%s*{([^}]*)}%s*{([^}]*)}")
      if term and label then
        pending_definition = {term = term, label = label}
        -- Don't add to result, will be added as header before next Para
        goto continue
      end

      -- Check for \definition{term} without label (label on next line)
      -- NOTE: Same reasoning - simple patterns acceptable
      local term_only = text:match("\\definition%s*{([^}]*)}")
      if term_only and not term then  -- Only if we didn't already extract term above
        pending_definition = {term = term_only, label = nil}
        -- Don't add to result, will be added as header before next Para
        goto continue
      end

      -- Pattern: \defncontext{context}
      -- NOTE: Same reasoning - simple patterns acceptable
      local ctx = text:match("\\defncontext%s*{([^}]*)}")
      if ctx then
        pending_context = ctx
        -- Don't add to result, will prepend to next Para
        goto continue
      end

      -- Check for defnote
      local note_content = text:match("\\begin{defnote}([%s%S]-)\\end{defnote}")
      if note_content then
        note_counter = note_counter + 1
        table.insert(result, build_defnote(note_content, note_counter, true))
        goto continue
      end
    end

    if block.t == "Para" then
      -- Check if this Para contains a \definition
      local has_definition = false
      local def_term = nil
      local def_label = nil
      local context = nil
      local new_content = {}
      local skip_first_span = false

      -- Check if we have a pending definition without label and first element is Span
      if pending_definition and not pending_definition.label and
         #block.content > 0 and block.content[1].t == "Span" then
        -- Extract label from Span content
        local span_text = pandoc.utils.stringify(block.content[1])
        def_label = span_text
        def_term = pending_definition.term
        has_definition = true
        pending_definition = nil
        skip_first_span = true
      end

      for item_idx, inline in ipairs(block.content) do
        -- Skip the first Span if we extracted label from it
        if skip_first_span and item_idx == 1 and inline.t == "Span" then
          goto skip_inline
        end
        if inline.t == "RawInline" and inline.format == "latex" then
          local text = inline.text

          -- Check for \definition{term}{label}
          local term, label = text:match("\\definition%s*{([^}]*)}%s*{([^}]*)}")
          if term and label then
            has_definition = true
            def_term = term
            def_label = label
            -- Don't add to new_content (remove it)
          -- Check for \defncontext{context}
          elseif text:match("\\defncontext%s*{([^}]*)}") then
            context = text:match("\\defncontext%s*{([^}]*)}")
            -- Don't add to new_content (remove it)
          -- Check for \indexdefn (remove it - combined with above to avoid empty branch)
          elseif not text:match("\\indexdefn") then
            -- Keep inline if it's not an indexdefn command
            table.insert(new_content, inline)
          end
        elseif inline.t ~= "SoftBreak" or #new_content > 0 then
          -- Keep other inlines, but skip leading SoftBreaks
          table.insert(new_content, inline)
        end

        ::skip_inline::
      end

      -- Check if there's a pending definition from previous RawBlock
      if pending_definition and not has_definition then
        has_definition = true
        def_term = pending_definition.term
        def_label = pending_definition.label
        pending_definition = nil
      end

      -- Check if there's a pending context from previous RawBlock
      if pending_context and not context then
        context = pending_context
        pending_context = nil
      end

      -- If we found a definition, create header and modified para
      if has_definition and def_term and def_label then
        definition_counter = definition_counter + 1
        note_counter = 0  -- Reset note counter for new definition
        local def_num = tostring(definition_counter)

        -- Create header
        local heading_text = def_num .. " " .. def_term
        local anchor = '<a id="' .. def_label .. '">[' .. def_label .. ']</a>'
        local header = pandoc.Header(4, {
          pandoc.Str(heading_text),
          pandoc.Space(),
          pandoc.RawInline('html', anchor)
        })
        table.insert(result, header)

        -- Prepend context if present
        if context then
          local context_content = {
            pandoc.Str("⟨" .. context .. "⟩"),
            pandoc.Space()
          }
          for _, item in ipairs(new_content) do
            table.insert(context_content, item)
          end
          new_content = context_content
        end

        -- Create modified para with remaining content
        if #new_content > 0 then
          table.insert(result, pandoc.Para(new_content))
        end
      else
        -- No definition, keep para as-is
        table.insert(result, block)
      end

    elseif block.t == "CodeBlock" and block.classes and block.classes[1] == "latex" then
      -- Handle defnote as CodeBlock
      local text = block.text
      -- Use [%s%S] to match any character including newlines
      local note_content = text:match("\\begin{defnote}([%s%S]-)\\end{defnote}")
      if note_content then
        note_counter = note_counter + 1
        table.insert(result, build_defnote(note_content, note_counter, false))
      else
        table.insert(result, block)
      end

    elseif block.t == "RawBlock" and block.format == "latex" then
      -- Handle defnote as RawBlock
      local text = block.text
      -- Use [%s%S] to match any character including newlines
      local note_content = text:match("\\begin{defnote}([%s%S]-)\\end{defnote}")
      if note_content then
        note_counter = note_counter + 1
        table.insert(result, build_defnote(note_content, note_counter, false))
      else
        table.insert(result, block)
      end

    else
      -- Keep other blocks as-is
      table.insert(result, block)
    end

    ::continue::
  end

  return result
end

-- Return single filter
return {
  { Blocks = Blocks }
}
