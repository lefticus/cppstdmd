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

-- Helper function to clean up LaTeX escapes in code
-- Now uses unified clean_code_common() from cpp-common.lua
local function clean_code(code)
  return clean_code_common(code, false)  -- false = no special textbackslash handling
end

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
    -- Clean up the code
    code = clean_code(code)
    code = trim(code)

    -- Return as a code block with cpp language
    return pandoc.CodeBlock(code, {class = "cpp"})
  end

  -- Match \begin{codeblocktu}...\end{codeblocktu}
  -- (codeblock with title - translation unit)
  code = text:match("\\begin{codeblocktu}{[^}]*}(.-)\\end{codeblocktu}")

  if code then
    code = clean_code(code)
    code = trim(code)
    return pandoc.CodeBlock(code, {class = "cpp"})
  end

  -- Match \begin{outputblock}...\end{outputblock}
  -- (program output, not C++ code)
  code = text:match("\\begin{outputblock}(.-)\\end{outputblock}")

  if code then
    code = clean_code(code)
    code = trim(code)
    return pandoc.CodeBlock(code, {class = "text"})  -- Use "text" class for output
  end

  -- Match \begin{codeblockdigitsep}...\end{codeblockdigitsep}
  -- (code block with digit separators)
  code = text:match("\\begin{codeblockdigitsep}(.-)\\end{codeblockdigitsep}")

  if code then
    code = clean_code(code)
    code = trim(code)
    return pandoc.CodeBlock(code, {class = "cpp"})
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
     code:match("\\texttt{") or code:match("\\textit{") then

    -- Remove font switch commands
    code = remove_font_switches(code)

    -- Handle layout overlap commands
    code = handle_overlap_commands(code)

    -- Strip \texttt{} and \textit{} from simplified_macros.tex preprocessing
    code = code:gsub("\\texttt{([^}]*)}", "%1")
    code = code:gsub("\\textit{([^}]*)}", "%1")

    -- Return updated code block
    return pandoc.CodeBlock(code, elem.attr)
  end

  return elem
end

-- Note: We don't handle inline \tcode{} here because cpp-macros.lua
-- handles it with proper nested macro expansion. This filter only
-- handles code blocks (codeblock, codeblocktu, codeblockdigitsep, outputblock).
