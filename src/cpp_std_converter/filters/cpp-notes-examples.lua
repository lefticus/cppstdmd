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
cpp-notes-examples.lua

Pandoc Lua filter to convert C++ standard note and example environments.

Handles:
- \begin{note}...\end{note} → [*Note N*: ... — *end note*]
- \begin{example}...\end{example} → [*Example N*: ... — *end example*]

Both can contain nested elements like code blocks, cross-refs, and footnotes.
Counters reset when encountering new sections.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local trim = common.trim
local clean_code_common = common.clean_code_common
local extract_braced_content = common.extract_braced_content
local expand_macros_common = common.expand_macros_common
local extract_code_from_div = common.extract_code_from_div

-- Track note and example counters
local note_counter = 0
local example_counter = 0

-- Helper function to clean up LaTeX escapes in code
-- Now uses unified clean_code_common() from cpp-common.lua with special textbackslash handling
local function clean_code(code)
  return clean_code_common(code, true)  -- true = special textbackslash handling for notes/examples
end

-- Helper function to convert codeblock Div to CodeBlock or replace placeholders
-- Returns a list of blocks (to support title + code for codeblocktu)
local function process_codeblock_div(block, codeblocks, titles)
  -- Check for placeholder in Para blocks
  if block.t == "Para" and codeblocks then
    local text = pandoc.utils.stringify(block)
    -- Only replace if the Para contains ONLY the placeholder (possibly with whitespace)
    local trimmed = trim(text)
    local placeholder = trimmed:match("^__CODEBLOCK_(%d+)__$")
    if placeholder then
      local idx = tonumber(placeholder)
      if codeblocks[idx] then
        local result = {}
        -- If this codeblock has a title, add it as a paragraph first
        if titles and titles[idx] then
          table.insert(result, pandoc.Para({pandoc.Str(titles[idx])}))
        end
        -- Add the code block
        table.insert(result, pandoc.CodeBlock(codeblocks[idx], {class = "cpp"}))
        return result
      end
    end
  end

  -- Check for codeblock Div (fallback for cases without placeholders)
  if block.t == "Div" and block.classes and block.classes[1] == "codeblock" then
    local code_block = extract_code_from_div(block, "cpp")
    if code_block then
      return {code_block}
    end
  end

  -- Handle BulletList and OrderedList blocks - recursively process items
  -- for placeholders (Issue #18)
  if (block.t == "BulletList" or block.t == "OrderedList") and codeblocks then
    local modified = false
    local new_items = {}

    for _, item in ipairs(block.content) do
      local new_item_blocks = {}
      for _, item_block in ipairs(item) do
        -- Recursively process each block in the list item
        local processed = process_codeblock_div(item_block, codeblocks, titles)
        for _, b in ipairs(processed) do
          table.insert(new_item_blocks, b)
        end
        -- Check if we made a modification
        if #processed ~= 1 or processed[1] ~= item_block then
          modified = true
        end
      end
      table.insert(new_items, new_item_blocks)
    end

    if modified then
      -- Return modified list
      if block.t == "BulletList" then
        return {pandoc.BulletList(new_items)}
      else
        return {pandoc.OrderedList(new_items, block.listAttributes)}
      end
    end
  end

  -- Return block as single-item list for consistency
  return {block}
end

-- Optimized codeblock extraction using position tracking instead of repeated scanning
-- Handles all code block types: codeblock, codeblocktu, codeblockdigitsep, outputblock
-- Uses pattern matching with balanced brace extraction for codeblocktu titles
-- Returns: modified_content, codeblocks, titles, counter
local function extract_codeblocks(content)
  local codeblocks = {}
  local titles = {}  -- Store titles for codeblocktu (indexed by codeblock number)
  local modified_content = content
  local counter = 0

  -- Process each type with its own pattern, finding earliest match each iteration
  local pos = 1
  while pos <= #modified_content do
    local earliest_start, earliest_end, earliest_code, earliest_type = nil, nil, nil, nil

    -- Try each pattern and find which one matches earliest
    local patterns = {
      {name = "codeblock", start_pat = "\\begin{codeblock}",
       end_pat = "\\end{codeblock}"},
      {name = "codeblockdigitsep", start_pat = "\\begin{codeblockdigitsep}",
       end_pat = "\\end{codeblockdigitsep}"},
      {name = "outputblock", start_pat = "\\begin{outputblock}",
       end_pat = "\\end{outputblock}"},
    }

    for _, p in ipairs(patterns) do
      local start_pos = modified_content:find(p.start_pat, pos, true)
      if start_pos and (not earliest_start or start_pos < earliest_start) then
        local end_pos = modified_content:find(p.end_pat, start_pos, true)
        if end_pos then
          local code_start = start_pos + #p.start_pat
          local code = modified_content:sub(code_start, end_pos - 1)
          earliest_start = start_pos
          earliest_end = end_pos + #p.end_pat - 1
          earliest_code = code
          earliest_type = p.name
        end
      end
    end

    -- Handle codeblocktu separately due to title parameter with nested braces
    local cbtu_start = modified_content:find("\\begin{codeblocktu}{", pos, true)
    local cbtu_title = nil
    if cbtu_start and (not earliest_start or cbtu_start < earliest_start) then
      -- Use brace-balanced extraction for the title
      local title_brace_start = cbtu_start + 20  -- After \begin{codeblocktu}{
      local title, title_end = extract_braced_content(modified_content, title_brace_start - 1, 0)
      if title and title_end then
        local cbtu_end = modified_content:find("\\end{codeblocktu}", title_end, true)
        if cbtu_end then
          local code = modified_content:sub(title_end + 1, cbtu_end - 1)
          earliest_start = cbtu_start
          earliest_end = cbtu_end + 17 - 1  -- \end{codeblocktu} is 17 chars
          earliest_code = code
          earliest_type = "codeblocktu"
          cbtu_title = title  -- Store the raw title for processing
        end
      end
    end

    if earliest_start and earliest_code then
      -- Clean and store the code
      local code = earliest_code:gsub("^%s*\n", ""):gsub("\n%s*$", "")
      code = clean_code(code)

      counter = counter + 1
      codeblocks[counter] = code

      -- For codeblocktu, store the title separately
      if earliest_type == "codeblocktu" and cbtu_title then
        -- Process title: expand \tcode{} and clean up
        local formatted_title = cbtu_title
        formatted_title = formatted_title:gsub("\\tcode{([^}]*)}", "`%1`")
        formatted_title = formatted_title:gsub("\\#", "#")
        titles[counter] = formatted_title
      end

      -- Replace with placeholder
      local placeholder = "\n\n__CODEBLOCK_" .. counter .. "__\n\n"
      modified_content = modified_content:sub(1, earliest_start - 1) ..
                         placeholder .. modified_content:sub(earliest_end + 1)

      -- Continue from after the placeholder
      pos = earliest_start + #placeholder
    else
      break
    end
  end

  return modified_content, codeblocks, titles, counter
end

-- Optimized macro expansion using shared function from cpp-common
local function expand_macros(content)
  -- Use shared expand_macros_common with minimal mode for notes/examples context
  return expand_macros_common(content, {minimal = true})
end

-- Forward declarations for recursive processing
local process_div_block
local process_environment

-- Helper function to process Div blocks (examples, notes, footnotes)
-- Takes codeblocks and titles for placeholder replacement
-- Returns a list of blocks
function process_div_block(block, codeblocks, titles)
  if not block.classes then
    return {block}
  end

  -- Handle <div class="note">
  if block.classes[1] == "note" then
    note_counter = note_counter + 1

    local note_inlines = {}
    local has_blocks = false

    -- Check if content has non-Para blocks
    for _, div_block in ipairs(block.content) do
      if div_block.t ~= "Para" then
        has_blocks = true
        break
      end
    end

    if not has_blocks then
      -- Simple case: only paragraphs, combine into single inline sequence
      for _, div_block in ipairs(block.content) do
        if div_block.t == "Para" and div_block.content then
          if #note_inlines > 0 then
            table.insert(note_inlines, pandoc.Space())
          end
          for _, inline in ipairs(div_block.content) do
            table.insert(note_inlines, inline)
          end
        end
      end

      local note_para = {
        pandoc.Str("["),
        pandoc.Emph({pandoc.Str("Note " .. note_counter)}),
        pandoc.Str(": ")
      }
      for _, inline in ipairs(note_inlines) do
        table.insert(note_para, inline)
      end
      table.insert(note_para, pandoc.Str(" — "))
      table.insert(note_para, pandoc.Emph({pandoc.Str("end note")}))
      table.insert(note_para, pandoc.Str("]"))

      return {pandoc.Para(note_para)}
    else
      -- Complex case: has code blocks or other non-Para blocks
      local result = {}
      local opening = {
        pandoc.Str("["),
        pandoc.Emph({pandoc.Str("Note " .. note_counter)}),
        pandoc.Str(":")
      }
      table.insert(result, pandoc.Para(opening))

      -- Recursively process nested div content, passing codeblocks/titles
      for _, div_block in ipairs(block.content) do
        local blocks = process_single_block(div_block, codeblocks, titles)
        for _, b in ipairs(blocks) do
          table.insert(result, b)
        end
      end

      local closing = {
        pandoc.Str("— "),
        pandoc.Emph({pandoc.Str("end note")}),
        pandoc.Str("]")
      }
      table.insert(result, pandoc.Para(closing))
      return result
    end
  end

  -- Handle <div class="example">
  if block.classes[1] == "example" then
    example_counter = example_counter + 1

    local example_inlines = {}
    local has_blocks = false

    -- Check if content has non-Para blocks
    for _, div_block in ipairs(block.content) do
      if div_block.t ~= "Para" then
        has_blocks = true
        break
      end
    end

    if not has_blocks then
      -- Simple case: only paragraphs, combine into single inline sequence
      for _, div_block in ipairs(block.content) do
        if div_block.t == "Para" and div_block.content then
          if #example_inlines > 0 then
            table.insert(example_inlines, pandoc.Space())
          end
          for _, inline in ipairs(div_block.content) do
            table.insert(example_inlines, inline)
          end
        end
      end

      local example_para = {
        pandoc.Str("["),
        pandoc.Emph({pandoc.Str("Example " .. example_counter)}),
        pandoc.Str(": ")
      }
      for _, inline in ipairs(example_inlines) do
        table.insert(example_para, inline)
      end
      table.insert(example_para, pandoc.Str(" — "))
      table.insert(example_para, pandoc.Emph({pandoc.Str("end example")}))
      table.insert(example_para, pandoc.Str("]"))

      return {pandoc.Para(example_para)}
    else
      -- Complex case: has code blocks or other non-Para blocks
      local result = {}
      local opening = {
        pandoc.Str("["),
        pandoc.Emph({pandoc.Str("Example " .. example_counter)}),
        pandoc.Str(":")
      }
      table.insert(result, pandoc.Para(opening))

      -- Recursively process nested div content, passing codeblocks/titles
      for _, div_block in ipairs(block.content) do
        local blocks = process_single_block(div_block, codeblocks, titles)
        for _, b in ipairs(blocks) do
          table.insert(result, b)
        end
      end

      local closing = {
        pandoc.Str("— "),
        pandoc.Emph({pandoc.Str("end example")}),
        pandoc.Str("]")
      }
      table.insert(result, pandoc.Para(closing))
      return result
    end
  end

  -- Handle <div class="footnote"> - just unwrap the div, keep content
  if block.classes[1] == "footnote" then
    local result = {}
    for _, div_block in ipairs(block.content) do
      table.insert(result, div_block)
    end
    return result
  end

  -- Handle <div class="codeblock"> - convert to proper code block
  if block.classes[1] == "codeblock" then
    local code_block = extract_code_from_div(block, "cpp")
    if code_block then
      return {code_block}
    end
  end

  -- Return block as-is if not recognized
  return {block}
end

-- Helper function to recursively process a single block, handling nested Divs and RawBlocks
local function process_single_block(block, codeblocks, titles)
  -- Handle Div blocks that might contain nested examples/notes/footnotes
  if block.t == "Div" and block.classes then
    return process_div_block(block, codeblocks, titles)
  end

  -- Handle RawBlock that might contain nested examples/notes
  -- Note: At this point, codeblocks have already been extracted and replaced with placeholders
  -- by the parent's extract_codeblocks() call. We need to parse the content and process it
  -- using the existing codeblocks dict rather than calling process_environment() which would
  -- try to extract codeblocks again.
  if block.t == "RawBlock" and block.format == "latex" then
    local text = block.text

    -- Check for nested note
    local note_start, note_end = text:find("\\begin{note}")
    if note_start then
      local note_content_end = text:find("\\end{note}", note_start)
      if note_content_end then
        note_counter = note_counter + 1
        -- 12 = length of "\begin{note}"
        local note_content = text:sub(note_start + 12, note_content_end - 1)
        note_content = trim(note_content)
        note_content = expand_macros(note_content)

        -- Parse the content (which already has codeblock placeholders)
        local parsed = pandoc.read(note_content, "latex+raw_tex")

        local result = {}
        local label = "Note"
        -- Opening
        table.insert(result, pandoc.Para({
          pandoc.Str("["),
          pandoc.Emph({pandoc.Str(label .. " " .. note_counter)}),
          pandoc.Str(":")
        }))

        -- Process all blocks recursively with the existing codeblocks dict
        for _, parsed_block in ipairs(parsed.blocks) do
          local blocks = process_single_block(parsed_block, codeblocks, titles)
          for _, b in ipairs(blocks) do
            table.insert(result, b)
          end
        end

        -- Closing
        table.insert(result, pandoc.Para({
          pandoc.Str("— "),
          pandoc.Emph({pandoc.Str("end note")}),
          pandoc.Str("]")
        }))

        return result
      end
    end

    -- Check for nested example
    local example_start, example_end = text:find("\\begin{example}")
    if example_start then
      local example_content_end = text:find("\\end{example}", example_start)
      if example_content_end then
        example_counter = example_counter + 1
        -- 15 = length of "\begin{example}"
        local example_content = text:sub(example_start + 15, example_content_end - 1)
        example_content = trim(example_content)
        example_content = expand_macros(example_content)

        -- Parse the content (which already has codeblock placeholders)
        local parsed = pandoc.read(example_content, "latex+raw_tex")

        local result = {}
        local label = "Example"
        -- Opening
        table.insert(result, pandoc.Para({
          pandoc.Str("["),
          pandoc.Emph({pandoc.Str(label .. " " .. example_counter)}),
          pandoc.Str(":")
        }))

        -- Process all blocks recursively with the existing codeblocks dict
        for _, parsed_block in ipairs(parsed.blocks) do
          local blocks = process_single_block(parsed_block, codeblocks, titles)
          for _, b in ipairs(blocks) do
            table.insert(result, b)
          end
        end

        -- Closing
        table.insert(result, pandoc.Para({
          pandoc.Str("— "),
          pandoc.Emph({pandoc.Str("end example")}),
          pandoc.Str("]")
        }))

        return result
      end
    end

    -- Check for nested footnote
    local footnote_start, footnote_end = text:find("\\begin{footnote}")
    if footnote_start then
      local footnote_content_end = text:find("\\end{footnote}", footnote_start)
      if footnote_content_end then
        -- 16 = length of "\begin{footnote}"
        local footnote_content = text:sub(footnote_start + 16, footnote_content_end - 1)
        footnote_content = trim(footnote_content)
        footnote_content = expand_macros(footnote_content)

        -- Create a native Pandoc footnote (Note inline element)
        local parsed = pandoc.read(footnote_content, "latex+raw_tex")

        -- Create Note with parsed blocks as content
        local note = pandoc.Note(parsed.blocks)

        -- Return as Para containing the Note inline element
        return {pandoc.Para({note})}
      end
    end
  end

  -- Handle codeblock replacement
  return process_codeblock_div(block, codeblocks, titles)
end

-- Unified function to process note or example environments
-- env_type: "note" or "example"
-- counter_val: current counter value
-- Returns: result blocks, updated counter value
function process_environment(content, env_type, counter_val)
  counter_val = counter_val + 1

  -- Trim leading/trailing whitespace
  content = trim(content)

  -- Expand macros efficiently
  content = expand_macros(content)

  -- Extract codeblocks before parsing (optimized)
  local modified_content, codeblocks, titles, codeblock_count = extract_codeblocks(content)

  -- Parse the LaTeX content to get Pandoc AST elements
  local parsed = pandoc.read(modified_content, "latex+raw_tex")
  local has_blocks = false

  -- Check if content has non-Para blocks
  for _, parsed_block in ipairs(parsed.blocks) do
    if parsed_block.t ~= "Para" then
      has_blocks = true
      break
    end
  end
  if codeblock_count > 0 then
    has_blocks = true  -- Force complex case if we have codeblocks
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
    -- Complex case: has code blocks or other non-Para blocks
    local opening = {
      pandoc.Str("["),
      pandoc.Emph({pandoc.Str(label .. " " .. counter_val)}),
      pandoc.Str(":")
    }
    table.insert(result, pandoc.Para(opening))

    -- Output all blocks from parsed content, recursively processing Divs
    for _, parsed_block in ipairs(parsed.blocks) do
      local blocks = process_single_block(parsed_block, codeblocks, titles)
      -- Insert all blocks from the list (handles both single block and title+code)
      for _, block in ipairs(blocks) do
        table.insert(result, block)
      end
    end

    local closing = {
      pandoc.Str("— "),
      pandoc.Emph({pandoc.Str("end " .. env_type)}),
      pandoc.Str("]")
    }
    table.insert(result, pandoc.Para(closing))
  end

  return result, counter_val
end

-- Process blocks to find and convert note/example environments
function Blocks(blocks)
  local result = {}

  for i, block in ipairs(blocks) do
    -- Reset counters when we encounter a new section (any header level 1-4)
    if block.t == "Header" and block.level <= 4 then
      note_counter = 0
      example_counter = 0
      table.insert(result, block)
      goto continue
    end

    -- Handle note environments in RawBlock
    if block.t == "RawBlock" and block.format == "latex" then
      local text = block.text

      -- Skip blocks that contain description lists - let cpp-macros.lua handle those
      -- (they may contain nested notes/examples which will be processed after parsing)
      if text:match("\\begin{description}") then
        table.insert(result, block)
        goto continue
      end

      -- Check for note environment
      local note_content = text:match("\\begin{note}([%s%S]-)\\end{note}")
      if note_content then
        local blocks_to_insert
        blocks_to_insert, note_counter = process_environment(note_content, "note", note_counter)
        for _, b in ipairs(blocks_to_insert) do
          table.insert(result, b)
        end
        goto continue
      end

      -- Check for example environment
      local example_content = text:match("\\begin{example}([%s%S]-)\\end{example}")
      if example_content then
        local blocks_to_insert
        blocks_to_insert, example_counter =
          process_environment(example_content, "example", example_counter)
        for _, b in ipairs(blocks_to_insert) do
          table.insert(result, b)
        end
        goto continue
      end

      -- Check for footnote environment
      local footnote_content = text:match("\\begin{footnote}([%s%S]-)\\end{footnote}")
      if footnote_content then
        -- Create a native Pandoc footnote (Note inline element)
        footnote_content = trim(footnote_content)
        footnote_content = expand_macros(footnote_content)
        local parsed = pandoc.read(footnote_content, "latex+raw_tex")

        -- Create Note with parsed blocks as content
        local note = pandoc.Note(parsed.blocks)

        -- Find the last Para block in result to attach the footnote to
        local last_para_idx = nil
        for idx = #result, 1, -1 do
          if result[idx].t == "Para" then
            last_para_idx = idx
            break
          end
        end

        if last_para_idx then
          -- Append footnote to the end of the paragraph's inline content
          table.insert(result[last_para_idx].content, note)
        else
          -- No preceding paragraph found; create new Para with just the footnote
          table.insert(result, pandoc.Para({note}))
        end
        goto continue
      end
    end

    -- Handle note/example environments in CodeBlock with class "latex"
    -- These are rare edge cases where content is preserved as raw LaTeX
    if block.t == "CodeBlock" and block.classes and block.classes[1] == "latex" then
      local text = block.text

      -- Check for note environment
      local note_content = text:match("\\begin{note}([%s%S]-)\\end{note}")
      if note_content then
        note_counter = note_counter + 1
        note_content = trim(note_content)
        table.insert(result, pandoc.Para({
          pandoc.Str("["),
          pandoc.Emph({pandoc.Str("Note " .. note_counter)}),
          pandoc.Str(": "),
          pandoc.RawInline('latex', note_content),
          pandoc.Str(" — "),
          pandoc.Emph({pandoc.Str("end note")}),
          pandoc.Str("]")
        }))
        goto continue
      end

      -- Check for example environment
      local example_content = text:match("\\begin{example}([%s%S]-)\\end{example}")
      if example_content then
        example_counter = example_counter + 1
        example_content = trim(example_content)
        table.insert(result, pandoc.Para({
          pandoc.Str("["),
          pandoc.Emph({pandoc.Str("Example " .. example_counter)}),
          pandoc.Str(": "),
          pandoc.RawInline('latex', example_content),
          pandoc.Str(" — "),
          pandoc.Emph({pandoc.Str("end example")}),
          pandoc.Str("]")
        }))
        goto continue
      end
    end

    -- Handle Div elements that Pandoc created from LaTeX environments
    -- These are environments that Pandoc's LaTeX reader converts to Div instead of RawBlock
    if block.t == "Div" and block.classes then
      -- Handle <div class="note">
      if block.classes[1] == "note" then
        note_counter = note_counter + 1

        local note_inlines = {}
        local has_blocks = false

        -- Check if content has non-Para blocks
        for _, div_block in ipairs(block.content) do
          if div_block.t ~= "Para" then
            has_blocks = true
            break
          end
        end

        if not has_blocks then
          -- Simple case: only paragraphs, combine into single inline sequence
          for _, div_block in ipairs(block.content) do
            if div_block.t == "Para" and div_block.content then
              if #note_inlines > 0 then
                table.insert(note_inlines, pandoc.Space())
              end
              for _, inline in ipairs(div_block.content) do
                table.insert(note_inlines, inline)
              end
            end
          end

          local note_para = {
            pandoc.Str("["),
            pandoc.Emph({pandoc.Str("Note " .. note_counter)}),
            pandoc.Str(": ")
          }
          for _, inline in ipairs(note_inlines) do
            table.insert(note_para, inline)
          end
          table.insert(note_para, pandoc.Str(" — "))
          table.insert(note_para, pandoc.Emph({pandoc.Str("end note")}))
          table.insert(note_para, pandoc.Str("]"))

          table.insert(result, pandoc.Para(note_para))
        else
          -- Complex case: has code blocks or other non-Para blocks
          local opening = {
            pandoc.Str("["),
            pandoc.Emph({pandoc.Str("Note " .. note_counter)}),
            pandoc.Str(":")
          }
          table.insert(result, pandoc.Para(opening))

          -- Output all blocks from div content
          for _, div_block in ipairs(block.content) do
            local processed_blocks = process_codeblock_div(div_block, nil, nil)
            for _, b in ipairs(processed_blocks) do
              table.insert(result, b)
            end
          end

          local closing = {
            pandoc.Str("— "),
            pandoc.Emph({pandoc.Str("end note")}),
            pandoc.Str("]")
          }
          table.insert(result, pandoc.Para(closing))
        end

        goto continue
      end

      -- Handle <div class="example">
      if block.classes[1] == "example" then
        example_counter = example_counter + 1

        local example_inlines = {}
        local has_blocks = false

        -- Check if content has non-Para blocks
        for _, div_block in ipairs(block.content) do
          if div_block.t ~= "Para" then
            has_blocks = true
            break
          end
        end

        if not has_blocks then
          -- Simple case: only paragraphs, combine into single inline sequence
          for _, div_block in ipairs(block.content) do
            if div_block.t == "Para" and div_block.content then
              if #example_inlines > 0 then
                table.insert(example_inlines, pandoc.Space())
              end
              for _, inline in ipairs(div_block.content) do
                table.insert(example_inlines, inline)
              end
            end
          end

          local example_para = {
            pandoc.Str("["),
            pandoc.Emph({pandoc.Str("Example " .. example_counter)}),
            pandoc.Str(": ")
          }
          for _, inline in ipairs(example_inlines) do
            table.insert(example_para, inline)
          end
          table.insert(example_para, pandoc.Str(" — "))
          table.insert(example_para, pandoc.Emph({pandoc.Str("end example")}))
          table.insert(example_para, pandoc.Str("]"))

          table.insert(result, pandoc.Para(example_para))
        else
          -- Complex case: has code blocks or other non-Para blocks
          local opening = {
            pandoc.Str("["),
            pandoc.Emph({pandoc.Str("Example " .. example_counter)}),
            pandoc.Str(":")
          }
          table.insert(result, pandoc.Para(opening))

          -- Output all blocks from div content
          for _, div_block in ipairs(block.content) do
            local processed_blocks2 = process_codeblock_div(div_block, nil, nil)
            for _, b in ipairs(processed_blocks2) do
              table.insert(result, b)
            end
          end

          local closing = {
            pandoc.Str("— "),
            pandoc.Emph({pandoc.Str("end example")}),
            pandoc.Str("]")
          }
          table.insert(result, pandoc.Para(closing))
        end

        goto continue
      end

      -- Handle <div class="footnote"> - just unwrap the div, keep content
      if block.classes[1] == "footnote" then
        -- Footnotes are just unwrapped - no special formatting needed
        -- Just output the content blocks directly
        for _, div_block in ipairs(block.content) do
          table.insert(result, div_block)
        end
        goto continue
      end

      -- Handle <div class="codeblock"> - convert to proper code block
      if block.classes[1] == "codeblock" then
        local code_block = extract_code_from_div(block, "cpp")
        if code_block then
          table.insert(result, code_block)
        end
        goto continue
      end

      -- Handle other div classes (like "indented", "center", "ncbnf")
      -- unwrap by outputting content as blockquote. This preserves content
      -- from LaTeX environments like \begin{indented} that would be lost
      if block.classes[1] then
        -- Skip table-related Div blocks - let cpp-tables.lua handle them
        if block.classes[1] == "libtab2" or
           block.classes[1] == "lib2dtab2" or
           block.classes[1] == "libtab3" or
           block.classes[1] == "lib2dtab3" then
          table.insert(result, block)
          goto continue
        end

        -- Convert to blockquote to preserve indentation/centering visually
        table.insert(result, pandoc.BlockQuote(block.content))
        goto continue
      end
    end

    -- Keep other blocks as-is
    table.insert(result, block)

    ::continue::
  end

  return result
end

-- Return single filter
return {
  { Blocks = Blocks }
}
