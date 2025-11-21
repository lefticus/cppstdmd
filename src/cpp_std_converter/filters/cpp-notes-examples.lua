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
local has_complex_blocks = common.has_complex_blocks
local build_environment_opening = common.build_environment_opening
local build_environment_closing = common.build_environment_closing

-- Track note and example counters
local note_counter = 0
local example_counter = 0

-- Helper: Capitalize first letter of string
local function capitalize(str)
  return str:sub(1,1):upper() .. str:sub(2)
end

-- Helper: Get counter value for environment type
local function get_counter_for_env(env_type)
  return env_type == "note" and note_counter or example_counter
end

-- Helper: Set counter value for environment type
local function set_counter_for_env(env_type, value)
  if env_type == "note" then
    note_counter = value
  else
    example_counter = value
  end
end

-- Helper: Prepare environment by incrementing counter and getting label
local function prepare_environment(env_type, counter_val)
  return counter_val + 1, capitalize(env_type)
end

-- Optimized macro expansion using shared function from cpp-common
local function expand_macros(content)
  -- Use shared expand_macros_common with minimal mode for notes/examples context
  return expand_macros_common(content, {minimal = true})
end

-- Helper: Prepare content by trimming and expanding macros
local function prepare_content(content)
  return expand_macros(trim(content))
end

-- Forward declarations for functions used before they're defined
local process_list_recursive
local convert_environment_from_blocks
local convert_environment_from_nested_string
local convert_environment_from_string
local convert_environment_from_codeblock
local process_block_recursive

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
    return process_list_recursive(block, process_codeblock_div, codeblocks, titles)
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
      local cbtu_prefix = "\\begin{codeblocktu}{"
      local title_brace_start = cbtu_start + #cbtu_prefix
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
      code = clean_code_common(code, true)

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

-- Helper: Extract environment content from text string
-- Returns: content string (or nil if not found)
local function extract_environment_content(text, env_type)
  local pattern = "\\begin{" .. env_type .. "}([%s%S]-)\\end{" .. env_type .. "}"
  return text:match(pattern)
end

-- Helper: Process list items recursively
-- Consolidates duplicate list processing logic from
-- process_codeblock_div and process_block_recursive
-- block: BulletList or OrderedList block to process
-- processor_fn: function(item_block, ...) that returns list of blocks
-- ...: additional args to pass to processor_fn (e.g., codeblocks, titles)
-- Returns: list containing modified list block (if changed) or original block (if unchanged)
function process_list_recursive(block, processor_fn, ...)
  if block.t ~= "BulletList" and block.t ~= "OrderedList" then
    return {block}
  end

  local modified = false
  local new_items = {}

  for _, item in ipairs(block.content) do
    local new_item_blocks = {}
    for _, item_block in ipairs(item) do
      -- Recursively process each block in the list item
      local processed = processor_fn(item_block, ...)
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

  return {block}
end

-- Helper: Build environment output (simple or complex mode)
-- Consolidates the shared rendering logic from all environment converters
-- label: capitalized environment type (e.g., "Note", "Example")
-- counter_val: counter value for this environment
-- blocks: array of blocks to render
-- env_type: "note" or "example" (lowercase)
-- codeblocks: optional dict for placeholder replacement
-- titles: optional dict for codeblocktu titles
-- is_simple: if true, render as inline; if false, render with opening/closing blocks
-- Returns: result blocks
local function build_environment_output(
  label, counter_val, blocks, env_type, codeblocks, titles, is_simple
)
  local result = {}

  if is_simple then
    -- Simple case: only paragraphs, combine into single inline sequence
    local inlines = {}
    for _, block in ipairs(blocks) do
      if block.t == "Para" and block.content then
        if #inlines > 0 then
          table.insert(inlines, pandoc.Space())
        end
        for _, inline in ipairs(block.content) do
          table.insert(inlines, inline)
        end
      end
    end

    local para = build_environment_opening(label, counter_val, false)
    table.insert(para, pandoc.Str(" "))  -- space after colon
    for _, inline in ipairs(inlines) do
      table.insert(para, inline)
    end
    table.insert(para, pandoc.Str(" "))  -- space before closing
    local closing = build_environment_closing(env_type, false)
    for _, inline in ipairs(closing) do
      table.insert(para, inline)
    end

    table.insert(result, pandoc.Para(para))
  else
    -- Complex case: has code blocks or other non-Para blocks
    table.insert(result, build_environment_opening(label, counter_val, true))

    -- Recursively process blocks
    for _, block in ipairs(blocks) do
      local processed = process_block_recursive(block, codeblocks, titles)
      for _, b in ipairs(processed) do
        table.insert(result, b)
      end
    end

    table.insert(result, build_environment_closing(env_type, true))
  end

  return result
end

-- Generic function to convert note or example from Div blocks
-- env_type: "note" or "example"
-- block_content: array of blocks from Div
-- codeblocks: optional dict for placeholder replacement
-- titles: optional dict for codeblocktu titles
-- counter_val: current counter value
-- Returns: result_blocks, updated_counter
function convert_environment_from_blocks(
  env_type, block_content, codeblocks, titles, counter_val
)
  local label
  counter_val, label = prepare_environment(env_type, counter_val)
  local is_simple = not has_complex_blocks(block_content)
  local result = build_environment_output(
    label, counter_val, block_content, env_type, codeblocks, titles, is_simple
  )
  return result, counter_val
end

-- Generic function to convert note or example from nested RawBlock string
-- Used when codeblocks have already been extracted by parent
-- env_type: "note" or "example"
-- content: string content (already has codeblock placeholders)
-- codeblocks: dict for placeholder replacement
-- titles: dict for codeblocktu titles
-- counter_val: current counter value
-- Returns: result_blocks, updated_counter
function convert_environment_from_nested_string(
  env_type, content, codeblocks, titles, counter_val
)
  local label
  counter_val, label = prepare_environment(env_type, counter_val)

  content = prepare_content(content)

  -- Parse the content (which already has codeblock placeholders)
  local parsed = pandoc.read(content, "latex+raw_tex")

  -- Always use complex mode since codeblocks were already extracted
  local result = build_environment_output(
    label, counter_val, parsed.blocks, env_type, codeblocks, titles, false
  )

  return result, counter_val
end

-- Generic function to convert note or example from CodeBlock with "latex" class
-- This is a rare edge case where content is preserved as raw LaTeX
-- env_type: "note" or "example"
-- content: raw LaTeX string content
-- counter_val: current counter value
-- Returns: result_blocks (single Para with RawInline), updated_counter
function convert_environment_from_codeblock(env_type, content, counter_val)
  local label
  counter_val, label = prepare_environment(env_type, counter_val)

  content = trim(content)

  local inlines = build_environment_opening(label, counter_val, false)
  table.insert(inlines, pandoc.Str(" "))
  table.insert(inlines, pandoc.RawInline('latex', content))
  table.insert(inlines, pandoc.Str(" "))
  local closing = build_environment_closing(env_type, false)
  for _, inline in ipairs(closing) do
    table.insert(inlines, inline)
  end

  return {pandoc.Para(inlines)}, counter_val
end

-- Unified recursive block processor
-- Handles all block types: RawBlock, Div, CodeBlock, lists, placeholders
-- This is the single entry point for recursive processing
-- Increments module-level counters (note_counter, example_counter)
-- codeblocks: optional dict for placeholder replacement
-- titles: optional dict for codeblocktu titles
-- Returns: list of blocks
function process_block_recursive(block, codeblocks, titles)
  -- Handle Div blocks that might contain notes/examples/footnotes/codeblocks
  if block.t == "Div" and block.classes then
    local class = block.classes[1]

    if class == "note" or class == "example" then
      local counter = get_counter_for_env(class)
      local result
      result, counter = convert_environment_from_blocks(
        class, block.content, codeblocks, titles, counter
      )
      set_counter_for_env(class, counter)
      return result
    elseif class == "footnote" then
      -- Just unwrap the div, keep content
      return block.content
    elseif class == "codeblock" then
      local code_block = extract_code_from_div(block, "cpp")
      if code_block then
        return {code_block}
      end
    end
    -- If not recognized, return as-is
    return {block}
  end

  -- Handle RawBlock that might contain nested notes/examples/footnotes
  if block.t == "RawBlock" and block.format == "latex" then
    local text = block.text

    -- Check for note or example environments
    for _, env_type in ipairs({"note", "example"}) do
      local content = extract_environment_content(text, env_type)
      if content then
        local counter = get_counter_for_env(env_type)
        local result
        -- Use nested string converter if we have codeblocks (already extracted)
        -- Otherwise use regular string converter (will extract codeblocks)
        if codeblocks then
          result, counter = convert_environment_from_nested_string(
            env_type, content, codeblocks, titles, counter
          )
        else
          result, counter = convert_environment_from_string(
            content, env_type, counter
          )
        end
        set_counter_for_env(env_type, counter)
        return result
      end
    end
    -- Note: Footnote handling is done at top-level in Blocks() function
    -- Footnotes inside notes/examples are handled by the environment converters
  end

  -- Handle CodeBlock with "latex" class (rare edge case)
  if block.t == "CodeBlock" and block.classes and block.classes[1] == "latex" then
    local text = block.text

    -- Check for note or example environments
    for _, env_type in ipairs({"note", "example"}) do
      local content = extract_environment_content(text, env_type)
      if content then
        local counter = get_counter_for_env(env_type)
        local result
        result, counter = convert_environment_from_codeblock(
          env_type, content, counter
        )
        set_counter_for_env(env_type, counter)
        return result
      end
    end
  end

  -- Handle BulletList and OrderedList blocks - recursively process items (FIXES ISSUE #5!)
  if block.t == "BulletList" or block.t == "OrderedList" then
    return process_list_recursive(block, process_block_recursive, codeblocks, titles)
  end

  -- Handle codeblock placeholder replacement and codeblock Divs
  return process_codeblock_div(block, codeblocks, titles)
end

-- Generic function to convert note or example from top-level RawBlock string
-- Handles codeblock extraction, macro expansion, and parsing
-- env_type: "note" or "example"
-- content: raw LaTeX string
-- counter_val: current counter value
-- Returns: result blocks, updated counter value
function convert_environment_from_string(content, env_type, counter_val)
  local label
  counter_val, label = prepare_environment(env_type, counter_val)

  content = prepare_content(content)

  -- Extract codeblocks before parsing (optimized)
  local modified_content, codeblocks, titles, codeblock_count = extract_codeblocks(content)

  -- Parse the LaTeX content to get Pandoc AST elements
  local parsed = pandoc.read(modified_content, "latex+raw_tex")
  local has_blocks = has_complex_blocks(parsed.blocks) or (codeblock_count > 0)

  local is_simple = not has_blocks
  local result = build_environment_output(
    label, counter_val, parsed.blocks, env_type, codeblocks, titles, is_simple
  )

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

      -- If RawBlock contains note/example, delegate to process_block_recursive()
      -- (it will handle any footnotes inside them correctly)
      if text:match("\\begin{note}") or text:match("\\begin{example}") then
        local processed = process_block_recursive(block, nil, nil)
        for _, b in ipairs(processed) do
          table.insert(result, b)
        end
        goto continue
      end

      -- Check for footnote environment (special case - attaches to previous Para)
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

      -- For all other RawBlock content, use the unified processor
      -- This handles note/example environments
      local processed = process_block_recursive(block, nil, nil)
      for _, b in ipairs(processed) do
        table.insert(result, b)
      end
      goto continue
    end

    -- Handle Div elements that Pandoc created from LaTeX environments
    if block.t == "Div" and block.classes and block.classes[1] then
      local class = block.classes[1]

      -- Skip table-related Div blocks - let cpp-tables.lua handle them
      if class == "libtab2" or class == "lib2dtab2" or
         class == "libtab3" or class == "lib2dtab3" then
        table.insert(result, block)
        goto continue
      end

      -- For known classes, use unified processor
      if class == "note" or class == "example" or class == "footnote" or class == "codeblock" then
        local processed = process_block_recursive(block, nil, nil)
        for _, b in ipairs(processed) do
          table.insert(result, b)
        end
        goto continue
      end

      -- Handle other unknown div classes (like "indented", "center", "ncbnf")
      -- Convert to blockquote to preserve indentation/centering visually
      table.insert(result, pandoc.BlockQuote(block.content))
      goto continue
    end

    -- For all other block types (including CodeBlock), use unified processor
    local processed = process_block_recursive(block, nil, nil)
    for _, b in ipairs(processed) do
      table.insert(result, b)
    end

    ::continue::
  end

  return result
end

-- Return single filter with topdown traversal to ensure correct processing order
-- This prevents Pandoc from calling Blocks() in bottom-up order (which would
-- process notes inside lists before top-level notes, breaking counter sequence)
return {
  {
    Blocks = Blocks,
    traverse = 'topdown'
  }
}
