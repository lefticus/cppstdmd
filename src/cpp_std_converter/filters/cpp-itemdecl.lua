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
cpp-itemdecl.lua

Pandoc Lua filter to handle C++ standard itemdecl and itemdescr environments.

The C++ standard uses:
- \begin{itemdecl}...\end{itemdecl} for function/class declarations
- \begin{itemdescr}...\end{itemdescr} for descriptions with \pnum, \expects, \effects, etc.

Pandoc doesn't recognize these custom environments and drops all their content,
resulting in massive documentation loss. This filter converts them to proper
Markdown structure.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local extract_braced_content = common.extract_braced_content
local trim = common.trim
local remove_font_switches = common.remove_font_switches
local expand_cpp_version_macros = common.expand_cpp_version_macros
local expand_concept_macros = common.expand_concept_macros
local convert_cross_references_in_code = common.convert_cross_references_in_code
local expand_library_spec_macros = common.expand_library_spec_macros
local remove_macro = common.remove_macro
local process_macro_with_replacement = common.process_macro_with_replacement
local clean_code_common = common.clean_code_common
local expand_macros_common = common.expand_macros_common

-- Track note and example counters across itemdescr processing
local itemdescr_note_counter = 0
local itemdescr_example_counter = 0

-- Reset counters when encountering headers (same logic as cpp-notes-examples.lua)
function Header(elem)
  if elem.level <= 4 then
    itemdescr_note_counter = 0
    itemdescr_example_counter = 0
  end
  return elem
end

-- extract_braced_content is now imported from cpp-common

-- Helper function to upgrade code blocks to fenced format for consistency
-- Pandoc converts \begin{verbatim} to indented code blocks (no language class)
-- We want all code blocks to use ``` cpp fences like cpp-code-blocks.lua produces
-- This function recursively processes nested structures (Div, BlockQuote, lists)
local function upgrade_code_blocks(blocks)
  local result = {}

  for _, block in ipairs(blocks) do
    if block.t == "CodeBlock" then
      -- Check if this is an indented code block (no classes)
      -- or already has a language class
      if not block.classes or #block.classes == 0 then
        -- Upgrade to fenced code block with cpp class
        block.classes = {"cpp"}
      end
      table.insert(result, block)
    elseif block.t == "Div" and block.content then
      -- Recursively process content inside Div blocks (notes/examples)
      block.content = upgrade_code_blocks(block.content)
      table.insert(result, block)
    elseif block.t == "BlockQuote" and block.content then
      -- Recursively process content inside BlockQuote
      block.content = upgrade_code_blocks(block.content)
      table.insert(result, block)
    elseif (block.t == "BulletList" or block.t == "OrderedList") and block.content then
      -- Recursively process list items
      for i, item in ipairs(block.content) do
        block.content[i] = upgrade_code_blocks(item)
      end
      table.insert(result, block)
    else
      table.insert(result, block)
    end
  end

  return result
end

-- Helper function to convert @@REF:label@@ placeholders to [[label]] markdown links
-- This is called after Pandoc processes the content to convert our temporary placeholders
local function convert_ref_placeholders(inlines)
  local result = {}
  for _, inline in ipairs(inlines) do
    if inline.t == "Str" then
      -- Check if this string contains our reference placeholder
      local text = inline.text
      -- Split on @@REF: markers and process each part
      local parts = {}
      local pos = 1
      while pos <= #text do
        local start_marker = text:find("@@REF:", pos, true)
        if start_marker then
          -- Add text before the marker
          local prefix = ""
          if start_marker > pos then
            local before_text = text:sub(pos, start_marker - 1)
            table.insert(parts, pandoc.Str(before_text))
            -- Check if we need a space before the reference for readability
            -- Add space if the text doesn't already end with whitespace
            if not before_text:match("%s$") then
              prefix = " "
            end
          elseif #parts > 0 and parts[#parts].t == "Str" then
            -- No text in current segment, check previous part
            local prev_text = parts[#parts].text
            if not prev_text:match("%s$") then
              prefix = " "
            end
          end
          -- Find end marker
          local end_marker = text:find("@@", start_marker + 6, true)
          if end_marker then
            -- Extract label
            local label = text:sub(start_marker + 6, end_marker - 1)
            -- Insert as RawInline markdown reference with space for readability
            table.insert(parts, pandoc.RawInline('markdown', prefix .. '[[' .. label .. ']]'))
            pos = end_marker + 2
          else
            -- No end marker, just add the rest
            table.insert(parts, pandoc.Str(text:sub(start_marker)))
            break
          end
        else
          -- No more markers, add the rest
          table.insert(parts, pandoc.Str(text:sub(pos)))
          break
        end
      end
      -- Add all parts to result
      for _, part in ipairs(parts) do
        table.insert(result, part)
      end
    else
      -- Not a string, keep as-is
      table.insert(result, inline)
    end
  end
  return result
end

-- Recursive helper to convert @@REF:label@@ placeholders in all block types
-- This handles nested structures like BulletList, OrderedList, etc.
local function convert_ref_placeholders_in_blocks(blocks)
  local result = {}
  for _, block in ipairs(blocks) do
    if block.t == "Para" and block.content then
      -- Convert placeholders in paragraph inline content
      block.content = convert_ref_placeholders(block.content)
      table.insert(result, block)
    elseif block.t == "Plain" and block.content then
      -- Convert placeholders in plain inline content
      block.content = convert_ref_placeholders(block.content)
      table.insert(result, block)
    elseif block.t == "BulletList" and block.content then
      -- Recursively process each list item
      for i, item in ipairs(block.content) do
        block.content[i] = convert_ref_placeholders_in_blocks(item)
      end
      table.insert(result, block)
    elseif block.t == "OrderedList" and block.content then
      -- Recursively process each list item
      for i, item in ipairs(block.content) do
        block.content[i] = convert_ref_placeholders_in_blocks(item)
      end
      table.insert(result, block)
    elseif block.t == "DefinitionList" and block.content then
      -- Recursively process definition list items
      for i, item in ipairs(block.content) do
        -- item is a pair: [term, definitions]
        -- term is a list of inlines
        item[1] = convert_ref_placeholders(item[1])
        -- definitions is a list of block lists
        for j, def_blocks in ipairs(item[2]) do
          item[2][j] = convert_ref_placeholders_in_blocks(def_blocks)
        end
        block.content[i] = item
      end
      table.insert(result, block)
    elseif block.t == "BlockQuote" and block.content then
      -- Recursively process blockquote content
      block.content = convert_ref_placeholders_in_blocks(block.content)
      table.insert(result, block)
    elseif block.t == "Div" and block.content then
      -- Recursively process div content
      block.content = convert_ref_placeholders_in_blocks(block.content)
      table.insert(result, block)
    else
      -- Other block types (CodeBlock, RawBlock, etc.) - keep as-is
      table.insert(result, block)
    end
  end
  return result
end

-- Forward declaration (defined later, after all helper functions)
local expand_itemdescr_macros

-- Unified function to process note or example environments in itemdescr
-- env_type: "note" or "example"
-- counter_ref: table with counter value (pass by reference)
-- already_expanded: (optional) if true, skip macro expansion (content already processed)
-- Returns: result blocks
local function process_itemdescr_environment(content, env_type, counter_ref, already_expanded)
  counter_ref[1] = counter_ref[1] + 1
  local counter_val = counter_ref[1]

  -- Trim leading/trailing whitespace
  content = trim(content)

  -- Expand macros before Pandoc processing to preserve cross-references
  -- Skip if content was already expanded (e.g., from RawBlock processing with +raw_tex)
  if not already_expanded then
    content = expand_itemdescr_macros(content)
  end

  -- Parse the LaTeX content to get Pandoc AST elements
  -- Use +raw_tex to ensure nested custom environments (like libtab2) are passed as RawBlocks
  local parsed = pandoc.read(content, "latex+raw_tex")
  local has_blocks = false

  -- Check if content has non-Para blocks (like code blocks, itemize)
  for _, parsed_block in ipairs(parsed.blocks) do
    if parsed_block.t ~= "Para" then
      has_blocks = true
      break
    end
  end

  local label = env_type:sub(1,1):upper() .. env_type:sub(2)  -- Capitalize first letter
  local result = {}

  if not has_blocks then
    -- Simple case: only paragraphs, combine into single inline sequence
    local inlines = {}
    for _, parsed_block in ipairs(parsed.blocks) do
      if parsed_block.t == "Para" and parsed_block.content then
        if #inlines > 0 then
          table.insert(inlines, pandoc.Space())
        end
        for _, inline in ipairs(parsed_block.content) do
          table.insert(inlines, inline)
        end
      end
    end

    -- Convert @@REF:label@@ placeholders to [[label]] markdown links
    inlines = convert_ref_placeholders(inlines)

    local para = {
      pandoc.Str("["),
      pandoc.Emph({pandoc.Str(label .. " " .. counter_val)}),
      pandoc.Str(": ")
    }
    for _, inline in ipairs(inlines) do
      table.insert(para, inline)
    end
    table.insert(para, pandoc.Str(" — "))
    table.insert(para, pandoc.Emph({pandoc.Str("end " .. env_type)}))
    table.insert(para, pandoc.Str("]"))

    table.insert(result, pandoc.Para(para))
  else
    -- Complex case: has code blocks or other non-Para blocks (like itemize)
    local opening = {
      pandoc.Str("["),
      pandoc.Emph({pandoc.Str(label .. " " .. counter_val)}),
      pandoc.Str(":")
    }
    table.insert(result, pandoc.Para(opening))

    -- Output all blocks from parsed content, converting ref placeholders in Para blocks
    for _, parsed_block in ipairs(parsed.blocks) do
      if parsed_block.t == "Para" and parsed_block.content then
        parsed_block.content = convert_ref_placeholders(parsed_block.content)
      end
      table.insert(result, parsed_block)
    end

    local closing = {
      pandoc.Str("— "),
      pandoc.Emph({pandoc.Str("end " .. env_type)}),
      pandoc.Str("]")
    }
    table.insert(result, pandoc.Para(closing))
  end

  return result
end

-- Helper function to process note/example blocks after pandoc.read()
-- This mirrors the logic from cpp-notes-examples.lua
local function process_notes_examples_blocks(blocks)
  local result = {}

  for _, block in ipairs(blocks) do
    -- Handle note/example Div blocks that Pandoc creates from \begin{note}/\begin{example}
    -- These were already parsed by Pandoc, so we just need to convert ref placeholders
    if block.t == "Div" and block.classes then
      local is_note = false
      local is_example = false
      for _, class in ipairs(block.classes) do
        if class == "note" then is_note = true end
        if class == "example" then is_example = true end
      end

      if is_note or is_example then
        -- Convert @@REF:label@@ placeholders in all Para blocks within this Div
        for i, div_block in ipairs(block.content) do
          if div_block.t == "Para" and div_block.content then
            div_block.content = convert_ref_placeholders(div_block.content)
            block.content[i] = div_block
          end
        end
        table.insert(result, block)
        goto continue
      end
    end

    -- Handle note environments in RawBlock
    if block.t == "RawBlock" and block.format == "latex" then
      local text = block.text

      -- Check for note environment
      local note_content = text:match("\\begin{note}([%s%S]-)\\end{note}")
      if note_content then
        local note_counter_ref = {itemdescr_note_counter}
        -- Pass true for already_expanded since content comes from RawBlock
        -- after macro expansion
        local blocks_to_insert = process_itemdescr_environment(
          note_content, "note", note_counter_ref, true)
        itemdescr_note_counter = note_counter_ref[1]
        for _, b in ipairs(blocks_to_insert) do
          table.insert(result, b)
        end
        goto continue
      end

      -- Check for example environment
      local example_content = text:match("\\begin{example}([%s%S]-)\\end{example}")
      if example_content then
        local example_counter_ref = {itemdescr_example_counter}
        -- Pass true for already_expanded since content comes from RawBlock
        -- after macro expansion
        local blocks_to_insert = process_itemdescr_environment(
          example_content, "example", example_counter_ref, true)
        itemdescr_example_counter = example_counter_ref[1]
        for _, b in ipairs(blocks_to_insert) do
          table.insert(result, b)
        end
        goto continue
      end
    end

    -- Keep other blocks as-is
    table.insert(result, block)

    ::continue::
  end

  return result
end

-- Helper function to expand macros in itemdescr text before Pandoc processing
-- (Forward declared earlier, defined here)
-- Uses hybrid approach: specialized logic FIRST,
-- then expand_macros_common for standard processing
expand_itemdescr_macros = function(text)
  -- PHASE 1: Itemdecl-specific specialized logic that must run BEFORE
  -- expand_macros_common. Transformations need to see the raw LaTeX before
  -- other macros are expanded

  -- COMPLEXITY #1: Handle \tcode{\placeholdernc{...}...} special case
  -- with proper brace balancing
  -- When \tcode wraps \placeholdernc, the placeholder dominates and we want
  -- italic, not code. This pattern can contain nested \tcode{} inside, like:
  -- \tcode{\placeholdernc{FUN}($\tcode{T}_j$)}
  -- We need to strip ALL \tcode{} wrappers while converting
  -- \placeholdernc{} -> \textit{}
  while true do
    local start_pos = text:find("\\tcode{\\placeholdernc{", 1, true)
    if not start_pos then break end

    -- Extract the full \tcode{...} content using brace-balancing
    -- "\tcode" is 6 chars
    local tcode_content, end_pos = extract_braced_content(text, start_pos, 6)
    if tcode_content then
      -- Remove nested \tcode{} wrappers while preserving content
      -- Example: \placeholdernc{FUN}($\tcode{T}_j$) -> \placeholdernc{FUN}($T_j$)
      -- Use helper function to recursively remove all \tcode{} macros
      local cleaned = remove_macro(tcode_content, "tcode", true)

      -- Now apply placeholder conversion
      cleaned = cleaned:gsub("\\placeholdernc{", "\\textit{")
      text = text:sub(1, start_pos - 1) .. cleaned .. text:sub(end_pos)
    else
      -- Couldn't extract, skip this occurrence
      break
    end
  end

  -- COMPLEXITY #2: Process \tcode{} blocks to strip nested \texttt{} from
  -- simplified_macros.tex preprocessing. This prevents nested backticks like
  -- `const_cast``<X ``const``&>` in the final markdown
  -- Example: \tcode{\texttt{const_cast}<X \texttt{const}\&>}
  --       -> \texttt{const_cast<X const\&>}
  -- When simplified_macros.tex converts \keyword{} to \texttt{}, we need to
  -- strip those inner \texttt{} wrappers before pandoc.read() sees them
  -- (to avoid double conversion)
  while true do
    local start_pos = text:find("\\tcode{", 1, true)
    if not start_pos then break end

    -- Extract the full \tcode{...} content using brace-balancing
    -- "\tcode" is 6 chars
    local tcode_content, end_pos = extract_braced_content(text, start_pos, 6)
    if tcode_content then
      -- Strip all \texttt{} wrappers that came from simplified_macros.tex
      -- (\keyword{}, \libconcept{}, etc.)
      -- Use remove_macro to recursively remove all \texttt{} macros
      local cleaned = remove_macro(tcode_content, "texttt", true)

      -- Replace \tcode{...} with \texttt{cleaned}
      text = text:sub(1, start_pos - 1) .. "\\texttt{" .. cleaned .. "}" .. text:sub(end_pos)
    else
      -- Couldn't extract, skip this occurrence
      break
    end
  end

  -- PHASE 2: Use shared expand_macros_common for standard macro processing
  -- This handles: spec labels, @ escaped macros, range macros, bigoh, impldef, phantom, references
  -- NOTE: We run this AFTER specialized logic so \placeholdernc is already converted to \textit
  text = expand_macros_common(text, {
    spec_labels = true,            -- Convert \expects, \returns, etc. to \textit{Labels:}
    escape_at_macros = true,       -- Handle @\tcode{}@ patterns in code blocks
    convert_to_latex = true,       -- Use \textit{} and \texttt{} for Pandoc
    strip_indexlibrary = true,     -- Remove \indexlibrary{} index generation
    ref_format = "placeholder",    -- Use @@REF:label@@ format for cross-refs
  })

  -- COMPLEXITY #3: Convert \begin{codeblock}...\end{codeblock} to LaTeX verbatim
  -- Pandoc doesn't recognize the custom codeblock environment and strips it
  -- We need to convert it to \begin{verbatim}...\end{verbatim} before pandoc.read()
  text = text:gsub("\\begin{codeblock}(.-)\\end{codeblock}", function(code)
    -- Clean up the code using shared function from cpp-common
    code = clean_code_common(code, false)

    -- Trim leading/trailing whitespace
    code = code:gsub("^%s+", "")
    code = code:gsub("%s+$", "")

    -- Return as LaTeX verbatim that pandoc.read() will convert to code block
    -- Use \n to ensure proper spacing around the code block
    return "\n\n\\begin{verbatim}\n" .. code .. "\n\\end{verbatim}\n\n"
  end)

  return text
end

-- Main filter function for raw blocks
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Match \begin{itemdecl}...\end{itemdecl}
  local content = text:match("\\begin{itemdecl}(.-)\\end{itemdecl}")

  if content then
    -- Clean up the code using shared function from cpp-common
    content = clean_code_common(content, false)

    -- Trim leading/trailing whitespace
    content = content:gsub("^%s+", "")
    content = content:gsub("%s+$", "")

    -- Return as a code block with cpp language
    return pandoc.CodeBlock(content, {class = "cpp"})
  end

  -- Match \begin{itemdescr}...\end{itemdescr}
  -- This environment contains descriptive text with special commands
  content = text:match("\\begin{itemdescr}(.-)\\end{itemdescr}")

  if content then
    -- First expand macros before Pandoc processes the content
    -- This prevents \tcode{}, \range{}, etc. from being stripped
    content = expand_itemdescr_macros(content)

    -- Now process with Pandoc to convert LaTeX to Markdown
    -- Use +raw_tex to ensure nested custom environments (like libtab2) are passed as RawBlocks
    local blocks = pandoc.read(content, "latex+raw_tex").blocks

    -- Process any note/example blocks in the result
    -- This handles nested environments like \begin{itemize} properly
    blocks = process_notes_examples_blocks(blocks)

    -- Upgrade indented code blocks to fenced blocks for consistency
    -- This ensures all code blocks use ``` cpp format like cpp-code-blocks.lua
    blocks = upgrade_code_blocks(blocks)

    -- Convert @@REF:label@@ placeholders to [[label]] in all block types
    -- This handles references in Para, Plain, BulletList, OrderedList, etc.
    blocks = convert_ref_placeholders_in_blocks(blocks)

    -- Return blocks without blockquote wrapper for better readability
    return blocks
  end

  -- If no match, return unchanged
  return elem
end
