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
cpp-code-blocks.lua

Pandoc Lua filter to handle C++ standard codeblock environments.

The C++ standard uses \begin{codeblock}...\end{codeblock} which is defined
via \lstnewenvironment from the listings package. Pandoc doesn't recognize
this and drops all code blocks, resulting in massive content loss.

This filter intercepts raw LaTeX blocks, detects codeblock environments,
extracts the code, and converts them to proper Markdown code blocks.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local trim = common.trim
local clean_code_common = common.clean_code_common
local remove_font_switches = common.remove_font_switches
local handle_overlap_commands = common.handle_overlap_commands
local extract_footnotes_from_code = common.extract_footnotes_from_code

-- Main filter function for raw blocks
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Only process blocks that are STANDALONE code blocks (codeblock, outputblock, etc.)
  -- If the block contains other LaTeX environments (description, note, example, etc.),
  -- let other filters handle it. Check if block is primarily a code block by verifying
  -- it starts with \begin{codeblock*} or \begin{outputblock} (after whitespace).
  local trimmed = text:match("^%s*(.-)%s*$")
  if not (trimmed:match("^\\begin{codeblock") or
          trimmed:match("^\\begin{outputblock") or
          trimmed:match("^\\begin{codeblocktu}") or
          trimmed:match("^\\begin{codeblockdigitsep}")) then
    -- Not a standalone code block, skip it
    return elem
  end

  -- Match \begin{codeblock}...\end{codeblock}
  -- Using .* to match any content (non-greedy)
  local code = text:match("\\begin{codeblock}(.-)\\end{codeblock}")

  if code then
    -- Extract footnotes from code content before processing
    -- Footnotes appear as \begin{footnote}...\end{footnote} and must be converted
    -- to GFM footnote syntax instead of being left as literal LaTeX in code blocks
    local footnote_blocks
    code, footnote_blocks = extract_footnotes_from_code(code)

    -- Clean up the code
    code = clean_code_common(code, false)
    code = trim(code)

    -- Build result blocks: code block followed by footnote paragraphs
    local blocks = {pandoc.CodeBlock(code, {class = "cpp"})}
    for _, fn_block in ipairs(footnote_blocks) do
      table.insert(blocks, fn_block)
    end

    -- Return all blocks (code + footnotes)
    return blocks
  end

  -- Match \begin{codeblocktu}...\end{codeblocktu}
  -- (codeblock with title - translation unit)
  code = text:match("\\begin{codeblocktu}{[^}]*}(.-)\\end{codeblocktu}")

  if code then
    -- Extract footnotes from code content
    local footnote_blocks
    code, footnote_blocks = extract_footnotes_from_code(code)

    code = clean_code_common(code, false)
    code = trim(code)

    local blocks = {pandoc.CodeBlock(code, {class = "cpp"})}
    for _, fn_block in ipairs(footnote_blocks) do
      table.insert(blocks, fn_block)
    end
    return blocks
  end

  -- Match \begin{outputblock}...\end{outputblock}
  -- (program output, not C++ code)
  code = text:match("\\begin{outputblock}(.-)\\end{outputblock}")

  if code then
    -- Extract footnotes from code content
    local footnote_blocks
    code, footnote_blocks = extract_footnotes_from_code(code)

    code = clean_code_common(code, false)
    code = trim(code)

    local blocks = {pandoc.CodeBlock(code, {class = "text"})}  -- Use "text" class for output
    for _, fn_block in ipairs(footnote_blocks) do
      table.insert(blocks, fn_block)
    end
    return blocks
  end

  -- Match \begin{codeblockdigitsep}...\end{codeblockdigitsep}
  -- (code block with digit separators)
  code = text:match("\\begin{codeblockdigitsep}(.-)\\end{codeblockdigitsep}")

  if code then
    -- Extract footnotes from code content
    local footnote_blocks
    code, footnote_blocks = extract_footnotes_from_code(code)

    code = clean_code_common(code, false)
    code = trim(code)

    local blocks = {pandoc.CodeBlock(code, {class = "cpp"})}
    for _, fn_block in ipairs(footnote_blocks) do
      table.insert(blocks, fn_block)
    end
    return blocks
  end

  -- If no match, return unchanged
  return elem
end

-- Handler for CodeBlock elements that may contain LaTeX commands
-- This catches code blocks that were converted by Pandoc or earlier filters
-- but still have LaTeX formatting commands in them
function CodeBlock(elem)
  local code = elem.text

  -- Check if this code block has LaTeX commands that need cleaning
  if code:match("\\rlap") or code:match("\\llap") or code:match("\\clap") or
     code:match("\\normalfont") or code:match("\\itshape") or
     code:match("\\rmfamily") or code:match("\\bfseries") or
     code:match("\\texttt{") or code:match("\\textit{") or code:match("\\textrm{") then

    -- Remove font switch commands
    code = remove_font_switches(code)

    -- Handle layout overlap commands
    code = handle_overlap_commands(code)

    -- Strip \texttt{}, \textit{}, and \textrm{} from simplified_macros.tex preprocessing
    -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
    -- Process in multiple passes to handle nesting like \textit{\textrm{C++}}
    code = common.process_macro_with_replacement(code, "texttt", function(content)
      return content
    end)
    code = common.process_macro_with_replacement(code, "textrm", function(content)
      return content
    end)
    code = common.process_macro_with_replacement(code, "textit", function(content)
      return content
    end)

    -- Return updated code block
    return pandoc.CodeBlock(code, elem.attr)
  end

  return elem
end

-- Note: We don't handle inline \tcode{} here because cpp-macros.lua
-- handles it with proper nested macro expansion. This filter only
-- handles code blocks (codeblock, codeblocktu, codeblockdigitsep, outputblock).
