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

  -- Replace \textnormal{x} with x (normal text)
  grammar = grammar:gsub("\\textnormal{([^}]*)}", "%1")

  -- Replace \terminal{x} with 'x' (terminal symbols)
  -- Also unescape LaTeX special characters within terminals
  grammar = grammar:gsub("\\terminal{([^}]*)}", function(content)
    -- Unescape common LaTeX special characters
    content = content:gsub("\\#", "#")
    content = content:gsub("\\$", "$")
    content = content:gsub("\\%%", "%%")
    content = content:gsub("\\&", "&")
    content = content:gsub("\\_", "_")
    content = content:gsub("\\{", "{")
    content = content:gsub("\\}", "}")
    return "'" .. content .. "'"
  end)

  -- Replace \opt{x} with [x] (optional elements)
  grammar = grammar:gsub("\\opt{([^}]*)}", "[%1]")

  -- Replace \tcode{x} with x (code - macros filter may have already handled this)
  grammar = grammar:gsub("\\tcode{([^}]*)}", "%1")

  -- Replace \unicode{XXXX} with actual Unicode character
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

  -- Clean up extra whitespace
  grammar = trim(grammar)

  return grammar
end

-- Main filter function for raw blocks
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Match \begin{ncbnf}...\end{ncbnf}
  local grammar = text:match("\\begin{ncbnf}(.-)\\end{ncbnf}")

  if grammar then
    grammar = clean_grammar(grammar)
    -- Return as code block with bnf class
    return pandoc.CodeBlock(grammar, {class = "bnf"})
  end

  -- Match \begin{ncsimplebnf}...\end{ncsimplebnf}
  grammar = text:match("\\begin{ncsimplebnf}(.-)\\end{ncsimplebnf}")

  if grammar then
    grammar = clean_grammar(grammar)
    return pandoc.CodeBlock(grammar, {class = "bnf"})
  end

  -- Match \begin{ncrebnf}...\end{ncrebnf}
  grammar = text:match("\\begin{ncrebnf}(.-)\\end{ncrebnf}")

  if grammar then
    grammar = clean_grammar(grammar)
    return pandoc.CodeBlock(grammar, {class = "bnf"})
  end

  -- Match \begin{bnfbase}{name}...\end{bnfbase}
  -- (base BNF with a name parameter)
  local bnf_name
  bnf_name, grammar = text:match("\\begin{bnfbase}{([^}]*)}(.-)\\end{bnfbase}")

  if grammar then
    grammar = clean_grammar(grammar)
    -- Include the name as a comment in the grammar
    if bnf_name and #bnf_name > 0 then
      grammar = "// " .. bnf_name .. "\n" .. grammar
    end
    return pandoc.CodeBlock(grammar, {class = "bnf"})
  end

  -- Match regular \begin{bnf}...\end{bnf}
  grammar = text:match("\\begin{bnf}(.-)\\end{bnf}")

  if grammar then
    grammar = clean_grammar(grammar)
    return pandoc.CodeBlock(grammar, {class = "bnf"})
  end

  -- No match, return unchanged
  return elem
end
