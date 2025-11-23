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
cpp-grammar.lua

Pandoc Lua filter to handle C++ standard grammar blocks.

The C++ standard uses special environments for BNF grammar:
- ncbnf: Non-concept BNF grammar
- ncsimplebnf: Simple BNF grammar
- ncrebnf: Regular expression BNF grammar

These environments are not recognized by Pandoc and may be dropped or
poorly formatted. This filter converts them to code blocks with appropriate
formatting.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local convert_special_chars = common.convert_special_chars
local trim = common.trim
local process_macro_with_replacement = common.process_macro_with_replacement
local subscripts = common.subscripts
local try_unicode_conversion = common.try_unicode_conversion
local extract_multi_arg_macro = common.extract_multi_arg_macro


-- Helper function to clean up grammar content
local function clean_grammar(grammar)
  if not grammar then return grammar end

  -- Replace \br (line break in grammar) with actual newlines
  -- Handle \br\n as a unit to avoid double newlines
  grammar = grammar:gsub("\\br\n", "\n")
  -- Handle remaining \br without following newline
  grammar = grammar:gsub("\\br", "\n")

  -- Replace \bnfindent with indentation (2 spaces)
  grammar = grammar:gsub("\\bnfindent", "  ")

  -- Replace \nontermdef{x} with "x:" (non-terminal definition)
  grammar = grammar:gsub("\\nontermdef{([^}]*)}", "%1:")

  -- Replace \grammarterm{x} with x (grammar terms are just italicized normally)
  grammar = grammar:gsub("\\grammarterm{([^}]*)}", "%1")

  -- Replace \keyword{x} with x (keywords - macros filter may have already handled this)
  grammar = grammar:gsub("\\keyword{([^}]*)}", "%1")

  -- Replace \textnormal{x} with x (normal text) - use brace-balanced extraction
  -- This handles nested macros like \tref{} inside \textnormal{}
  grammar = process_macro_with_replacement(grammar, "textnormal", function(content)
    return content  -- Just strip the wrapper, preserve nested content
  end)

  -- Replace \textbf{x} with x (bold text in BNF blocks)
  -- Inside code blocks, we just unwrap since markdown bold doesn't render well
  grammar = process_macro_with_replacement(grammar, "textbf", function(content)
    return content  -- Just strip the wrapper, preserve nested content
  end)

  -- Replace \terminal{x} with 'x' (terminal symbols)
  -- Use brace-balanced extraction to handle escaped braces properly
  grammar = process_macro_with_replacement(grammar, "terminal", function(content)
    -- Unescape common LaTeX special characters
    content = content:gsub("\\#", "#")
    content = content:gsub("\\%$", "$")
    content = content:gsub("\\%%", "%%")
    content = content:gsub("\\&", "&")
    content = content:gsub("\\_", "_")
    content = content:gsub("\\{", "{")
    content = content:gsub("\\}", "}")
    -- Handle \textbackslash macro (may appear in terminal symbols)
    -- Note: Pandoc adds a space after macro names, so handle both variants
    content = content:gsub("\\textbackslash%s", "\\")  -- with trailing space
    content = content:gsub("\\textbackslash", "\\")
    return "'" .. content .. "'"
  end)

  -- Replace \tcode{x} with x (code - macros filter may have already handled this)
  grammar = grammar:gsub("\\tcode{([^}]*)}", "%1")

  -- Replace \texttt{x} with x (Pandoc may convert \keyword{} to \texttt{} in BNF blocks)
  grammar = grammar:gsub("\\texttt{([^}]*)}", "%1")

  -- Replace \unicode{XXXX}{description} with U+XXXX (description)
  -- This macro takes two brace-balanced arguments
  while true do
    local start_pos = grammar:find("\\unicode{", 1, true)
    if not start_pos then break end

    -- Try to extract 2 args first (the standard form used in actual LaTeX)
    local args, end_pos = extract_multi_arg_macro(grammar, start_pos, 8, 2)
    if args then
      -- Replace \unicode{XXXX}{desc} with U+XXXX (desc)
      local replacement = "U+" .. args[1] .. " (" .. args[2] .. ")"
      grammar = grammar:sub(1, start_pos - 1) .. replacement .. grammar:sub(end_pos)
    else
      -- Fallback: handle single-argument form \unicode{XXXX} (for backwards compatibility)
      -- This form doesn't appear in actual C++ standard sources but may exist in tests
      break  -- Exit loop and let gsub handle single-arg forms below
    end
  end

  -- Fallback: Replace \unicode{XXXX} with actual Unicode character (single-arg form)
  grammar = grammar:gsub("\\unicode{([0-9A-Fa-f]+)}", function(hex)
    local codepoint = tonumber(hex, 16)
    if codepoint then
      return utf8.char(codepoint)
    else
      return "U+" .. hex
    end
  end)

  -- Replace special character macros (\caret{}, \textasciitilde{}, etc.)
  grammar = convert_special_chars(grammar)

  -- Remove \indexgrammar and other index commands
  grammar = grammar:gsub("\\indexgrammar[^\n]*\n?", "")
  grammar = grammar:gsub("\\indextext{[^}]*}", "")
  grammar = grammar:gsub("\\idxcode{[^}]*}", "")

  -- Remove \microtypesetup{...}
  grammar = grammar:gsub("\\microtypesetup{[^}]*}", "")

  -- Remove \obeyspaces directives (LaTeX command for preserving spaces)
  grammar = grammar:gsub("\\obeyspaces\n?", "")

  -- Remove }% LaTeX artifacts (closing brace + comment marker)
  grammar = grammar:gsub("}%%\n?", "")

  -- \xname{X} renders as __X (special identifiers with underscore prefix)
  grammar = grammar:gsub("\\xname{([^}]*)}", "__%1")

  -- \descr{X} renders as X (description text, just remove wrapper)
  grammar = grammar:gsub("\\descr{([^}]*)}", "%1")

  -- Exposition-only identifiers and concepts - strip in grammar/BNF contexts
  grammar = grammar:gsub("\\exposid{([^}]*)}", "%1")
  grammar = grammar:gsub("\\exposidnc{([^}]*)}", "%1")
  grammar = grammar:gsub("\\exposconceptnc{([^}]*)}", "%1")

  -- Process cross-reference macros that may appear in BNF blocks
  -- \tref{label} -> [[label]] (table reference)
  -- \iref{label} -> [[label]] (indexed reference)
  -- Must be converted here since cpp-macros doesn't process BNF RawBlocks
  grammar = grammar:gsub("\\tref{([^}]*)}", "[[%1]]")
  grammar = grammar:gsub("\\iref{([^}]*)}", "[[%1]]")

  -- Convert inline math to Unicode (comprehensive conversion)
  -- Processes all $...$ patterns with full math-to-Unicode conversion
  -- Handles subscripts, superscripts, Greek letters, operators, arrows, etc.
  grammar = grammar:gsub("%$([^$]+)%$", function(math_content)
    local converted = try_unicode_conversion(math_content)
    if converted then
      return converted
    else
      -- Conversion failed or incomplete, preserve original $...$ delimiters
      return "$" .. math_content .. "$"
    end
  end)

  -- Clean up extra whitespace
  grammar = trim(grammar)

  return grammar
end

-- Helper function to extract and process BNF environments
-- Consolidates duplicate pattern: match environment, clean grammar, return CodeBlock
-- Parameters:
--   text: LaTeX source text to search
--   env_name: BNF environment name (e.g., "ncbnf", "ncsimplebnf")
--   has_param: If true, expects {param} after \begin{env_name}
-- Returns:
--   CodeBlock if environment matched, nil otherwise
local function process_bnf_environment(text, env_name, has_param)
  local grammar, param

  if has_param then
    -- Match \begin{env}{param}...\end{env}
    param, grammar = text:match("\\begin{" .. env_name .. "}{([^}]*)}(.-)\\end{" .. env_name .. "}")
  else
    -- Match \begin{env}...\end{env}
    grammar = text:match("\\begin{" .. env_name .. "}(.-)\\end{" .. env_name .. "}")
  end

  if grammar then
    grammar = clean_grammar(grammar)

    -- Add parameter as comment if present (for bnfbase)
    if param and #param > 0 then
      grammar = "// " .. param .. "\n" .. grammar
    end

    return pandoc.CodeBlock(grammar, {class = "bnf"})
  end

  return nil
end

-- Main filter function for raw blocks
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Try each BNF environment type using the helper function
  -- Order matters: check most specific environments first
  local result

  -- Non-concept BNF environments
  result = process_bnf_environment(text, "ncbnf", false)
  if result then return result end

  result = process_bnf_environment(text, "ncsimplebnf", false)
  if result then return result end

  result = process_bnf_environment(text, "ncrebnf", false)
  if result then return result end

  -- Base BNF with name parameter
  result = process_bnf_environment(text, "bnfbase", true)
  if result then return result end

  -- Regular BNF
  result = process_bnf_environment(text, "bnf", false)
  if result then return result end

  -- No match, return unchanged
  return elem
end
