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
cpp-common.lua

Shared utility functions and data tables used across multiple C++ standard Lua filters.

This module provides common functionality to avoid code duplication across filters:
- subscripts: Unicode subscript mappings for converting math subscripts
- convert_special_chars: Converts LaTeX special character macros to Unicode/ASCII
- extract_braced_content: Extracts brace-balanced content from LaTeX macros

Usage in other filters:
  local common = require("cpp-common")
  local text = common.convert_special_chars(text)
  local subscript = common.subscripts["i"]
  local content, end_pos = common.extract_braced_content(text, start_pos, macro_len)
]]

-- Subscript mappings (Unicode subscript characters)
-- Used by cpp-code-blocks.lua, cpp-macros.lua, cpp-math.lua
-- This is the most complete version from cpp-math.lua
local subscripts = {
  ["0"] = "₀",
  ["1"] = "₁",
  ["2"] = "₂",
  ["3"] = "₃",
  ["4"] = "₄",
  ["5"] = "₅",
  ["6"] = "₆",
  ["7"] = "₇",
  ["8"] = "₈",
  ["9"] = "₉",
  ["a"] = "ₐ",
  ["e"] = "ₑ",
  ["o"] = "ₒ",
  ["x"] = "ₓ",
  ["h"] = "ₕ",
  ["k"] = "ₖ",
  ["l"] = "ₗ",
  ["m"] = "ₘ",
  ["n"] = "ₙ",
  ["p"] = "ₚ",
  ["r"] = "ᵣ",
  ["s"] = "ₛ",
  ["t"] = "ₜ",
  ["u"] = "ᵤ",
  ["v"] = "ᵥ",
  ["i"] = "ᵢ",
  ["j"] = "ⱼ",
  ["+"] = "₊",  -- Subscript plus sign for arithmetic like x_{i+1}
  ["-"] = "₋",  -- Subscript minus sign for arithmetic like x_{n-1}
}

-- Helper function to trim leading and trailing whitespace
-- Used by many filters (13+ occurrences across 6 files)
-- Removes all leading and trailing whitespace from a string
local function trim(text)
  return text:match("^%s*(.-)%s*$")
end

-- Comprehensive mapping of all special characters used in LaTeX to C++ standard conversion
-- Two types:
--   "escaped" for simple \X patterns (like \{)
--   "macro" for \name{} patterns (like \caret{})
-- preserve_space: whether \macro<space> should keep the space in output
local special_chars = {
  -- LaTeX escaped characters (simple backslash + char)
  {pattern = "\\{", replacement = "{", type = "escaped"},
  {pattern = "\\}", replacement = "}", type = "escaped"},
  {pattern = "\\#", replacement = "#", type = "escaped"},
  {pattern = "\\&", replacement = "&", type = "escaped"},
  {pattern = "\\%%", replacement = "%%", type = "escaped"},
  {pattern = "\\%$", replacement = "$", type = "escaped"},
  {pattern = "\\_", replacement = "_", type = "escaped"},

  -- Special character macros (with optional {} and space variants)
  {pattern = "\\textbackslash", replacement = "\\", type = "macro", preserve_space = false},
  {pattern = "\\caret", replacement = "^", type = "macro", preserve_space = true},
  {pattern = "\\textasciitilde", replacement = "~", type = "macro", preserve_space = true},
  {pattern = "\\atsign", replacement = "@", type = "macro", preserve_space = true},
  {pattern = "\\unun", replacement = "__", type = "macro", preserve_space = true},
  -- \~ is a tilde accent macro that becomes plain tilde in code (issue #8)
  -- Must handle \~{identifier} → ~identifier (remove braces) for destructor syntax
  {pattern = "\\~", replacement = "~", type = "macro", preserve_space = false},
}

-- Helper function to unescape LaTeX escaped characters
-- Converts LaTeX escaped characters to their actual characters
-- Used by process_code_macro and other code processing functions
local function unescape_latex_chars(text)
  for _, char in ipairs(special_chars) do
    if char.type == "escaped" then
      text = text:gsub(char.pattern, char.replacement)
    end
  end
  return text
end

-- Helper function to convert special character macros
-- Used by cpp-macros.lua, cpp-tables.lua
-- Converts LaTeX special character commands to their Unicode/ASCII equivalents
local function convert_special_chars(text)
  for _, char in ipairs(special_chars) do
    if char.type == "macro" then
      -- Handle all three variants: \macro{}, \macro<space>, \macro
      text = text:gsub(char.pattern .. "{}", char.replacement)
      if char.preserve_space then
        text = text:gsub(char.pattern .. "%s", char.replacement .. " ")
      else
        text = text:gsub(char.pattern .. "%s", char.replacement)
      end
      text = text:gsub(char.pattern, char.replacement)
    end
  end
  return text
end

-- Helper function to extract brace-balanced content from LaTeX macros
-- Used by cpp-macros.lua, cpp-itemdecl.lua
--
-- Extracts content within balanced braces {} after a macro.
-- For example, given "\foo{bar{baz}qux}" starting at position of \foo,
-- this returns "bar{baz}qux" and the position after the closing brace.
--
-- Parameters:
--   text: The full text string
--   start_pos: Position of the start of the macro (e.g., position of \)
--   macro_len: Length of the macro name (e.g., 4 for "\foo")
--
-- Returns:
--   content: The extracted content (without outer braces), or nil on failure
--   end_pos: Position immediately after the closing brace, or nil on failure
local function extract_braced_content(text, start_pos, macro_len)
  local pos = start_pos + macro_len
  if pos > #text or text:sub(pos, pos) ~= "{" then
    return nil, nil
  end
  pos = pos + 1
  local depth = 1
  local content_start = pos
  while pos <= #text and depth > 0 do
    local c = text:sub(pos, pos)

    -- If we encounter a backslash, we need to skip escape sequences and special macros
    if c == "\\" and pos < #text then
      -- Check for \textbackslash macro (needs special handling in BNF contexts)
      -- This must be checked BEFORE single-character escapes
      if text:sub(pos, pos + 13) == "\\textbackslash" then
        pos = pos + 14  -- Skip entire \textbackslash macro
      else
        -- Check for single-character LaTeX escapes: { } \ # $ % & _
        local next_char = text:sub(pos + 1, pos + 1)
        if next_char == "{" or next_char == "}" or next_char == "\\" or
           next_char == "#" or next_char == "$" or next_char == "%" or
           next_char == "&" or next_char == "_" then
          pos = pos + 2  -- Skip backslash and escaped char
        else
          -- It's some other macro, just move forward
          pos = pos + 1
        end
      end
    else
      -- Normal brace counting
      if c == "{" then depth = depth + 1
      elseif c == "}" then depth = depth - 1 end
      if depth > 0 then pos = pos + 1 else break end
    end
  end
  if depth == 0 then
    return text:sub(content_start, pos - 1), pos + 1
  end
  return nil, nil
end

-- Helper function to remove font switch commands
-- Used by cpp-code-blocks.lua, cpp-itemdecl.lua, cpp-macros.lua
-- Removes LaTeX font formatting commands from code blocks
local function remove_font_switches(text)
  text = text:gsub("\\normalfont%s*", "")
  text = text:gsub("\\itshape%s*", "")
  text = text:gsub("\\rmfamily%s*", "")
  text = text:gsub("\\bfseries%s*", "")
  return text
end

-- Helper function to extract balanced braces with escaped character support
-- Used by process_code_macro() for table processing
-- Differs from extract_braced_content by:
-- - Skipping leading whitespace
-- - Handling escaped characters (backslash followed by any char)
-- - Returning position after closing brace instead of content end
--
-- Parameters:
--   text: The full text string
--   start_pos: Position to start looking for opening brace
--
-- Returns:
--   content: The extracted content (without outer braces), or nil on failure
--   end_pos: Position immediately after the closing brace, or start_pos on failure
local function extract_braced(text, start_pos)
  -- Skip whitespace to find the opening brace
  local pos = start_pos
  while pos <= #text and text:sub(pos, pos):match("%s") do
    pos = pos + 1
  end

  if pos > #text or text:sub(pos, pos) ~= "{" then
    return nil, start_pos
  end

  local depth = 1
  local brace_start = pos
  pos = pos + 1
  while pos <= #text and depth > 0 do
    local c = text:sub(pos, pos)
    if c == "\\" then
      pos = pos + 2 -- Skip escaped character
    elseif c == "{" then
      depth = depth + 1
      pos = pos + 1
    elseif c == "}" then
      depth = depth - 1
      pos = pos + 1
    else
      pos = pos + 1
    end
  end

  if depth == 0 then
    return text:sub(brace_start + 1, pos - 2), pos
  else
    return nil, start_pos
  end
end

-- Helper function to expand a command with balanced braces
-- Iteratively processes nested commands until no more are found
-- Used by process_code_macro() to strip nested \texttt{} and \tcode{}
--
-- Parameters:
--   text: The text to process
--   cmd: The command name (without backslash)
--   replacement_func: Function that takes content and returns replacement
--
-- Returns:
--   The processed text with all instances of \cmd{content} replaced
local function expand_balanced_command(text, cmd, replacement_func)
  local result = text
  local changed = true

  -- Keep processing until no more changes (handles nested commands)
  while changed do
    changed = false
    local new_result = result:gsub("\\" .. cmd .. "{([^{}]*)}", function(content)
      changed = true
      return replacement_func(content)
    end)
    result = new_result
  end

  return result
end

-- Helper function to replace code macros with single escaped special characters
-- Handles cases like \tcode{\{} → `{` before the balanced brace processor
-- This must run before process_code_macro() since extract_braced doesn't handle escaped braces
-- Used by cpp-tables.lua
--
-- Parameters:
--   text: The text to process
--   macro_name: The macro name (e.g., "tcode", "texttt")
--
-- Returns:
--   Text with simple escaped char macros converted to backtick-wrapped chars
local function replace_code_macro_special_chars(text, macro_name)
  for _, char in ipairs(special_chars) do
    if char.type == "escaped" then
      -- \tcode{\{} → `{`
      text = text:gsub("\\" .. macro_name .. "{" .. char.pattern .. "}",
                       "`" .. char.replacement .. "`")
    elseif char.type == "macro" then
      -- \tcode{\caret} → `^`
      text = text:gsub("\\" .. macro_name .. "{" .. char.pattern .. "}",
                       "`" .. char.replacement .. "`")
    end
  end
  return text
end

-- Helper function to process code macros with balanced braces
-- Converts \macro{content} → `content` with proper special char handling
-- Supports nested braces and escaped characters
-- Used by cpp-tables.lua and can be used by other filters
--
-- Parameters:
--   text: The text to process
--   macro_name: The macro name (e.g., "tcode", "texttt")
--
-- Returns:
--   Text with \macro{content} converted to `content` with special chars processed
local function process_code_macro(text, macro_name)
  local macro_pattern = "\\" .. macro_name .. "{"
  local macro_len = #macro_name + 1  -- +1 for backslash

  while true do
    local macro_start = text:find(macro_pattern, 1, true)
    if not macro_start then break end

    local content, end_pos = extract_braced(text, macro_start + macro_len)
    if not content then break end

    -- Handle special characters inside code
    content = unescape_latex_chars(content)  -- Handles \{, \}, \#, \&, \%, \$, \_
    -- Handles \caret, \textasciitilde, \textbackslash, \unun, \atsign
    content = convert_special_chars(content)
    content = content:gsub("`", "")  -- Strip any backticks from nested processing

    -- Strip any nested \texttt{} and \tcode{} from content (handles cpp-macros.lua conversions)
    -- This prevents nested backticks when \tcode{\keyword{signed} \keyword{char}}
    -- becomes \texttt{\texttt{signed} \texttt{char}} after cpp-macros.lua
    content = expand_balanced_command(content, "texttt", function(c) return c end)
    content = expand_balanced_command(content, "tcode", function(c) return c end)

    -- Replace \macro{content} with `content`
    text = text:sub(1, macro_start - 1) .. "`" .. content .. "`" .. text:sub(end_pos)
  end

  return text
end

-- Helper function to process a macro with a custom replacement function
-- Uses extract_braced_content for proper nested brace handling
-- Parameters:
--   text: The text to process
--   macro_name: The macro name without backslash (e.g., "tcode")
--   replacement_func: Function that takes content and returns replacement
-- Returns:
--   Modified text with all instances of \macro{content} replaced
local function process_macro_with_replacement(text, macro_name, replacement_func)
  local macro_pattern = "\\" .. macro_name .. "{"
  local macro_len = #macro_name + 1  -- +1 for backslash

  while true do
    local macro_start = text:find(macro_pattern, 1, true)
    if not macro_start then break end

    local content, end_pos = extract_braced_content(text, macro_start, macro_len)
    if not content then break end

    local replacement = replacement_func(content)
    text = text:sub(1, macro_start - 1) .. replacement .. text:sub(end_pos)
  end

  return text
end

-- Helper function to extract and clean description from \impdefx macro
-- Used by cpp-macros.lua and expand_impdefx_in_text()
-- Extracts the description argument, handling nested braces properly
-- Parameters:
--   text: The full text string
--   start_pos: Position where \impdefx pattern starts
--   prefix_len: Length of the prefix (e.g., 9 for "\impdefx{", 10 for "@\impdefx{")
--   suffix_char: Optional character that must follow closing brace (e.g., "@")
-- Returns:
--   description: Cleaned description text, or nil on failure
--   end_pos: Position after closing brace (and suffix if present), or nil on failure
local function extract_impdefx_description(text, start_pos, prefix_len, suffix_char)
  local pos = start_pos + prefix_len
  local depth = 1
  local desc_start = pos

  -- Find matching closing brace with nested brace support
  while pos <= #text and depth > 0 do
    local c = text:sub(pos, pos)
    if c == "{" then
      depth = depth + 1
    elseif c == "}" then
      depth = depth - 1
    end
    if depth > 0 then
      pos = pos + 1
    end
  end

  -- Check for unbalanced braces
  if depth ~= 0 then
    return nil, nil
  end

  -- Check for required suffix character if specified
  if suffix_char then
    if text:sub(pos + 1, pos + 1) ~= suffix_char then
      return nil, nil
    end
  end

  -- Extract description
  local description = text:sub(desc_start, pos - 1)

  -- Clean nested macros using process_macro_with_replacement for proper brace-balancing
  -- (fixes ([^}]*) anti-pattern)
  description = process_macro_with_replacement(description, "tcode", function(content)
    return content
  end)
  description = process_macro_with_replacement(description, "placeholder", function(content)
    return content
  end)

  -- Calculate end position (after brace and optional suffix)
  local end_pos = suffix_char and (pos + 2) or (pos + 1)

  return description, end_pos
end

-- Helper function to expand all \impdefx macros in text
-- Used by cpp-macros.lua and cpp-common.lua
-- Processes all occurrences of \impdefx{description} → "implementation-defined  // description"
-- Parameters:
--   text: The text to process
--   pattern: The pattern to search for (e.g., "\\impdefx{" or "@\\impdefx{")
--   prefix_len: Length of the pattern plus opening brace
--   suffix_char: Optional character that must follow closing brace (e.g., "@" for @-delimited)
-- Returns:
--   Modified text with all \impdefx macros expanded
local function expand_impdefx_in_text(text, pattern, prefix_len, suffix_char)
  while true do
    local start_pos = text:find(pattern, 1, true)
    if not start_pos then break end

    local description, end_pos = extract_impdefx_description(text, start_pos,
                                                              prefix_len, suffix_char)

    if description then
      local replacement = "implementation-defined  // " .. description
      text = text:sub(1, start_pos - 1) .. replacement .. text:sub(end_pos)
    else
      break
    end
  end

  return text
end

-- Helper function to parse \impdefx description into Pandoc inline elements
-- Used by cpp-macros.lua RawInline() handler
-- Handles nested \tcode{} macros by creating alternating Str elements
-- Parameters:
--   description: The description text (already extracted and partially cleaned)
-- Returns:
--   Table of Pandoc inline elements
local function parse_impdefx_description_to_inlines(description)
  local inlines = {pandoc.Str("implementation-defined  // ")}
  local pos = 1

  while pos <= #description do
    -- Look for \tcode{...}
    local tcode_start, tcode_end = description:find("\\tcode{", pos, true)

    if tcode_start then
      -- Add text before \tcode
      if tcode_start > pos then
        local text_before = description:sub(pos, tcode_start - 1)
        text_before = text_before:gsub("\\#", "#"):gsub("\\&", "&")
        table.insert(inlines, pandoc.Str(text_before))
      end

      -- Extract \tcode content
      -- "\tcode" is 6 chars
      local tcode_content, next_pos = extract_braced_content(description, tcode_start, 6)

      if tcode_content then
        tcode_content = tcode_content:gsub("\\#", "#"):gsub("\\&", "&")
        table.insert(inlines, pandoc.Str(tcode_content))
        pos = next_pos
      else
        -- Malformed \tcode, skip it
        pos = tcode_end + 1
      end
    else
      -- No more \tcode, add remaining text
      local remaining = description:sub(pos)
      remaining = remaining:gsub("\\#", "#"):gsub("\\&", "&")
      table.insert(inlines, pandoc.Str(remaining))
      break
    end
  end

  return inlines
end

-- Helper function to expand C++ version macros
-- Used by cpp-code-blocks.lua, cpp-notes-examples.lua, cpp-itemdecl.lua
-- Converts \CppXX{} macros to their readable versions (e.g., \CppXVII{} → C++17)
local function expand_cpp_version_macros(text)
  text = text:gsub("\\CppIII{}", "C++03")
  text = text:gsub("\\CppXI{}", "C++11")
  text = text:gsub("\\CppXIV{}", "C++14")
  text = text:gsub("\\CppXVII{}", "C++17")
  text = text:gsub("\\CppXX{}", "C++20")
  text = text:gsub("\\CppXXIII{}", "C++23")
  text = text:gsub("\\CppXXVI{}", "C++26")
  return text
end

-- Helper function to expand concept macros
-- Used by cpp-code-blocks.lua, cpp-notes-examples.lua, cpp-itemdecl.lua
-- Converts concept macros (\libconcept, \exposconcept, \oldconcept) to their names
-- Parameters:
--   text: The text to process
--   has_at_delimiters: Whether to handle @...@ delimited versions (used in code blocks)
local function expand_concept_macros(text, has_at_delimiters)
  -- Note: @...@ delimited versions are kept as simple patterns since @ delimiters
  -- prevent brace nesting in the C++ standard's usage. Only non-@ versions need
  -- proper brace-balancing via process_macro_with_replacement.
  if has_at_delimiters then
    text = text:gsub("@\\libconcept{([^}]*)}@", "%1")
    text = text:gsub("@\\exposconcept{([^}]*)}@", "%1")
    text = text:gsub("@\\oldconcept{([^}]*)}@", "Cpp17%1")
  end
  -- Use process_macro_with_replacement for non-@ versions (fixes ([^}]*) anti-pattern)
  text = process_macro_with_replacement(text, "libconcept", function(content)
    return content
  end)
  text = process_macro_with_replacement(text, "exposconcept", function(content)
    return content
  end)
  text = process_macro_with_replacement(text, "oldconcept", function(content)
    return "Cpp17" .. content
  end)
  return text
end

-- Helper function to convert cross-references in code
-- Used by cpp-code-blocks.lua, cpp-notes-examples.lua, cpp-itemdecl.lua
-- Converts \iref{} and \ref{} to [label] format
-- Parameters:
--   text: The text to process
--   has_at_delimiters: Whether to handle @...@ delimited versions (used in code blocks)
local function convert_cross_references_in_code(text, has_at_delimiters)
  -- Note: @...@ delimited versions are kept as simple patterns since @ delimiters
  -- prevent brace nesting in the C++ standard's usage. Only non-@ versions need
  -- proper brace-balancing via process_macro_with_replacement.
  if has_at_delimiters then
    text = text:gsub("@\\iref{([^}]*)}@", "[%1]")
    text = text:gsub("@\\ref{([^}]*)}@", "[%1]")
  end
  -- Use process_macro_with_replacement for non-@ versions (fixes ([^}]*) anti-pattern)
  text = process_macro_with_replacement(text, "iref", function(content)
    return "[" .. content .. "]"
  end)
  text = process_macro_with_replacement(text, "ref", function(content)
    return "[" .. content .. "]"
  end)
  return text
end

-- Helper function to expand library specification macros
-- Used by cpp-code-blocks.lua, cpp-notes-examples.lua, cpp-itemdecl.lua
-- Converts library-specific macros to their text equivalents
-- Parameters:
--   text: The text to process
--   has_at_delimiters: Whether to handle @...@ delimited versions (used in code blocks)
local function expand_library_spec_macros(text, has_at_delimiters)
  if has_at_delimiters then
    text = text:gsub("@\\seebelow@", "see below")
    text = text:gsub("@\\unspec@", "unspecified")
    text = text:gsub("@\\unspecnc@", "unspecified")
    -- Match @\expos@ first (complete pattern), then partial matches
    -- This avoids matching @\exposid@ or @\exposidnc@
    text = text:gsub("@\\expos@", "exposition only")
    text = text:gsub("@\\expos([^i@])", "exposition only%1")

    -- Handle @\impdefx{description}@ with nested braces (extract description)
    -- Process this BEFORE @\impdef@ to avoid prefix matching
    text = expand_impdefx_in_text(text, "@\\impdefx{", 10, "@")

    -- Handle remaining @\impdef@ patterns (without 'x' or 'nc' suffixes)
    text = text:gsub("@\\impdefnc@", "implementation-defined")
    text = text:gsub("@\\impdef@", "implementation-defined")
  end

  -- Non-delimited versions (for prose text)
  -- Process specific patterns BEFORE general ones to avoid prefix matching
  text = text:gsub("\\seebelow", "see below")
  text = text:gsub("\\unspec", "unspecified")
  text = text:gsub("\\unspecnc", "unspecified")
  -- Use pattern that requires \expos to NOT be followed by 'i'
  -- to avoid matching \exposid or \exposidnc
  text = text:gsub("\\expos([^i])", "exposition only%1")
  text = text:gsub("\\expos$", "exposition only")

  -- Process \impdefx{...} with nested braces (fallback for any missed by cpp-macros.lua)
  text = expand_impdefx_in_text(text, "\\impdefx{", 9, nil)

  -- Process remaining \impdef variants
  -- Use pattern that requires \impdefnc and \impdef to be followed by
  -- non-letter to avoid partial matches
  text = text:gsub("\\impdefnc([^%w])", "implementation-defined%1")
  text = text:gsub("\\impdefnc$", "implementation-defined")
  text = text:gsub("\\impdef([^%w])", "implementation-defined%1")
  text = text:gsub("\\impdef$", "implementation-defined")

  text = text:gsub("\\notdef", "not defined")
  return text
end

-- Helper function to extract multiple brace-balanced arguments from LaTeX macros
-- Used to simplify extraction of multi-argument macros like \unicode{codepoint}{description}
-- Generalizes the pattern of calling extract_braced_content multiple times
--
-- Parameters:
--   text: The full text string
--   start_pos: Position of the start of the macro (e.g., position of \)
--   macro_len: Length of the macro name (e.g., 9 for "\unicode")
--   num_args: Number of brace-balanced arguments to extract
--
-- Returns:
--   args: Table of extracted arguments {arg1, arg2, ..., argN}, or nil on failure
--   end_pos: Position immediately after the last closing brace, or nil on failure
local function extract_multi_arg_macro(text, start_pos, macro_len, num_args)
  local args = {}
  local pos = start_pos + macro_len

  for i = 1, num_args do
    -- Skip whitespace before argument
    while pos <= #text and text:sub(pos, pos):match("%s") do
      pos = pos + 1
    end

    -- Extract this argument
    if pos > #text or text:sub(pos, pos) ~= "{" then
      return nil, nil
    end

    -- pos-1 to include the brace, macro_len=1 for just "{"
    local content, next_pos = extract_braced_content(text, pos - 1, 1)
    if not content then
      return nil, nil
    end

    args[i] = content
    pos = next_pos
  end

  return args, pos
end

-- Helper function to process all instances of a macro with a replacement function
-- Generalizes the pattern of finding a macro, extracting content, and replacing it
-- Used to eliminate repetitive macro processing loops across filters
--
-- Parameters:
--   text: The text to process
--   macro_name: The macro name (without backslash, e.g., "defn", "term", "impldef")
--   replacement_func: Function(content) that returns replacement text
--
-- Returns:
--   The processed text with all \macro_name{content} replaced
-- Helper function to expand nested macros recursively with multiple passes
-- Generalizes the multi-pass expansion pattern used in clean_code() functions
-- Handles cases like \tcode{\keyword{noexcept}(\keyword{true})}
--
-- Parameters:
--   text: The text to process
--   macro_patterns: Table of {pattern=string, replacement=string or function} entries
--                   If replacement is a function, it receives the matched content
--   max_passes: Maximum number of expansion passes (default 5)
--
-- Returns:
--   The text with nested macros expanded
local function expand_nested_macros_recursive(text, macro_patterns, max_passes)
  max_passes = max_passes or 5

  for pass = 1, max_passes do
    local changed = false
    local new_text = text

    for _, pattern_info in ipairs(macro_patterns) do
      local pattern = pattern_info.pattern
      local replacement = pattern_info.replacement

      if type(replacement) == "function" then
        -- Pattern with capture group, call function with captured content
        new_text = new_text:gsub(pattern, function(captured)
          changed = true
          return replacement(captured)
        end)
      else
        -- Simple string replacement
        local old_text = new_text
        new_text = new_text:gsub(pattern, replacement)
        if new_text ~= old_text then
          changed = true
        end
      end
    end

    text = new_text

    -- If nothing changed in this pass, we're done
    if not changed then
      break
    end
  end

  return text
end

-- Helper function to remove all instances of a macro
-- Generalizes the pattern of removing LaTeX commands while preserving content
-- Used by cpp-macros.lua and other filters to clean up markup
--
-- Parameters:
--   text: The text to process
--   macro_name: The macro name (without backslash, e.g., "textrm", "emph")
--   keep_content: If true, keeps the content; if false, removes macro and content (default: true)
--
-- Returns:
--   The text with \macro_name{content} removed (keeping content if keep_content=true)
local function remove_macro(text, macro_name, keep_content)
  if keep_content == nil then keep_content = true end

  local macro_pattern = "\\" .. macro_name .. "{"
  local macro_len = #macro_name + 1  -- +1 for backslash

  while true do
    local macro_start = text:find(macro_pattern, 1, true)
    if not macro_start then break end

    local content, end_pos = extract_braced_content(text, macro_start, macro_len)
    if not content then break end

    local replacement = keep_content and content or ""
    text = text:sub(1, macro_start - 1) .. replacement .. text:sub(end_pos)
  end

  return text
end

-- Shared code block macro patterns for nested expansion
-- Used by cpp-code-blocks.lua and cpp-notes-examples.lua
--
-- NOTE: These patterns use ([^}]*) for simplicity and historical reasons.
-- The @...@ delimited versions are safe because @ delimiters prevent nesting
-- in the C++ standard's actual usage. The bare versions are used in a multi-pass
-- expansion loop (expand_nested_macros_recursive) which handles simple nesting.
-- For truly complex nested braces, use process_macro_with_replacement instead.
local code_block_macro_patterns = {
  -- \tcode{x} represents inline code (just extract the content)
  -- Handle both @\tcode{x}@ and bare \tcode{x} (in comments)
  {pattern = "@\\tcode{([^}]*)}@", replacement = "%1"},
  {pattern = "\\tcode{([^}]*)}", replacement = "%1"},

  -- \placeholder{x}{} or \placeholder{x} represents a placeholder
  -- Handle with empty braces first (order matters!)
  {pattern = "@\\placeholder{([^}]*)}{}@", replacement = "%1"},
  {pattern = "@\\placeholder{([^}]*)}@", replacement = "%1"},
  {pattern = "\\placeholder{([^}]*)}{}",  replacement = "%1"},
  {pattern = "\\placeholder{([^}]*)}", replacement = "%1"},

  -- \placeholdernc{x}{} or \placeholdernc{x} represents a placeholder (non-code variant)
  -- Handle with empty braces first (order matters!)
  {pattern = "@\\placeholdernc{([^}]*)}{}@", replacement = "%1"},
  {pattern = "@\\placeholdernc{([^}]*)}@", replacement = "%1"},
  {pattern = "\\placeholdernc{([^}]*)}{}",  replacement = "%1"},
  {pattern = "\\placeholdernc{([^}]*)}", replacement = "%1"},

  -- \exposid{x} represents exposition-only identifier
  {pattern = "@\\exposid{([^}]*)}@", replacement = "%1"},
  {pattern = "\\exposid{([^}]*)}", replacement = "%1"},

  -- \exposidnc{x} represents exposition-only identifier (no italic correction)
  {pattern = "@\\exposidnc{([^}]*)}@", replacement = "%1"},
  {pattern = "\\exposidnc{([^}]*)}", replacement = "%1"},

  -- \libglobal{x} represents a library-level global name (Issue #24)
  {pattern = "@\\libglobal{([^}]*)}@", replacement = "%1"},
  {pattern = "\\libglobal{([^}]*)}", replacement = "%1"},

  -- \libmember{member}{class} represents a library class member name (Issue #24)
  -- Takes 2 parameters but only outputs the first (member name)
  {pattern = "@\\libmember{([^}]*)}{([^}]*)}@", replacement = "%1"},
  {pattern = "\\libmember{([^}]*)}{([^}]*)}", replacement = "%1"},

  -- \keyword{x} in code comments
  {pattern = "\\keyword{([^}]*)}", replacement = "%1"},

  -- \texttt{x} in code comments (font switch, just extract content)
  {pattern = "\\texttt{([^}]*)}", replacement = "%1"},

  -- \grammarterm{x} in code comments
  {pattern = "\\grammarterm{([^}]*)}", replacement = "%1"},

  -- \term{x} in code comments
  {pattern = "\\term{([^}]*)}", replacement = "%1"}
}

-- Helper function to handle layout overlap commands
-- Used by clean_code_common() for code block cleaning
local function handle_overlap_commands(text)
  text = text:gsub("\\rlap{([^}]+)}", "%1")
  text = text:gsub("\\llap{([^}]+)}", "%1")
  text = text:gsub("\\clap{([^}]+)}", "%1")
  return text
end

-- ============================================================================
-- Comprehensive Math-to-Unicode Conversion
-- Shared by: cpp-math.lua, cpp-grammar.lua, convert_math_in_code()
-- Strategy: All-or-nothing - only convert if 100% successful, else preserve $...$
-- ============================================================================

-- Unicode conversion tables
local math_operators = {
  ["\\leq"] = "≤",
  ["\\geq"] = "≥",
  ["\\neq"] = "≠",
  ["\\times"] = "×",
  ["\\cdot"] = "⋅",
  ["\\cdots"] = "⋯",
  ["\\ldots"] = "…",   -- Horizontal ellipsis
  ["\\vdots"] = "⋮",   -- Vertical ellipsis
  ["\\dotsc"] = "…",   -- Dots for series/commas
  ["\\dotsb"] = "…",   -- Dots for binary operators
  ["\\land"] = "∧",
  ["\\lor"] = "∨",
  ["\\le"] = "≤",      -- Short form of \leq
  ["\\ge"] = "≥",      -- Short form of \geq
  ["\\to"] = "→",      -- Short form of \rightarrow
  -- Bitwise/set operators
  ["\\oplus"] = "⊕",   -- XOR / exclusive or
  ["\\ll"] = "<<",     -- Much less than / left shift
  ["\\gg"] = ">>",     -- Much greater than / right shift
  ["\\wedge"] = "∧",   -- AND (synonym for \land)
  ["\\vee"] = "∨",     -- OR (synonym for \lor)
  ["\\mid"] = "|",     -- Divides / bitwise OR
  ["\\sim"] = "~",     -- Similar to / tilde operator (ASCII)
  ["\\backslash"] = "\\", -- Backslash character (ASCII)
  -- Additional math operators
  ["\\infty"] = "∞",   -- Infinity
  ["\\equiv"] = "≡",   -- Equivalence
  ["\\approx"] = "≈",  -- Approximately equal
  ["\\pm"] = "±",      -- Plus-minus
  ["\\mp"] = "∓",      -- Minus-plus
  -- Set theory operators
  ["\\cap"] = "∩",     -- Intersection
  ["\\cup"] = "∪",     -- Union
  ["\\in"] = "∈",      -- Element of
  ["\\notin"] = "∉",   -- Not element of
  ["\\subset"] = "⊂",  -- Subset
  ["\\supset"] = "⊃",  -- Superset
  ["\\subseteq"] = "⊆", -- Subset or equal
  ["\\supseteq"] = "⊇", -- Superset or equal
  ["\\emptyset"] = "∅", -- Empty set
  -- Logic operators
  ["\\exists"] = "∃",  -- There exists
  ["\\forall"] = "∀",  -- For all
  ["<"] = "<",
  [">"] = ">",
  ["="] = "=",
  ["+"] = "+",
  ["-"] = "-",
  ["*"] = "*",
  ["/"] = "/",
}

local greek_letters = {
  ["\\alpha"] = "α",
  ["\\beta"] = "β",
  ["\\gamma"] = "γ",
  ["\\delta"] = "δ",
  ["\\epsilon"] = "ε",
  ["\\zeta"] = "ζ",
  ["\\lambda"] = "λ",
  ["\\mu"] = "μ",
  ["\\pi"] = "π",
  ["\\rho"] = "ρ",
  ["\\sigma"] = "σ",
  ["\\theta"] = "θ",
  ["\\phi"] = "φ",
  ["\\ell"] = "ℓ",
}

local arrows = {
  ["\\rightarrow"] = "→",
  ["\\leftarrow"] = "←",
  ["\\Rightarrow"] = "⇒",
  ["\\Leftarrow"] = "⇐",
  ["\\mapsto"] = "↦",
}

-- Floor and ceiling delimiters
local delimiters = {
  ["\\lfloor"] = "⌊",
  ["\\rfloor"] = "⌋",
  ["\\lceil"] = "⌈",
  ["\\rceil"] = "⌉",
}

-- Math functions (convert to plain text)
local math_functions = {
  ["\\min"] = "min",
  ["\\max"] = "max",
  ["\\log"] = "log",
  ["\\bmod"] = " mod ",
  ["\\exp"] = "exp",
}

-- Superscript mappings (limited Unicode support)
local superscripts = {
  -- Digits
  ["0"] = "⁰",
  ["1"] = "¹",
  ["2"] = "²",
  ["3"] = "³",
  ["4"] = "⁴",
  ["5"] = "⁵",
  ["6"] = "⁶",
  ["7"] = "⁷",
  ["8"] = "⁸",
  ["9"] = "⁹",
  -- Lowercase letters
  ["a"] = "ᵃ",
  ["b"] = "ᵇ",
  ["c"] = "ᶜ",
  ["d"] = "ᵈ",
  ["e"] = "ᵉ",
  ["f"] = "ᶠ",
  ["g"] = "ᵍ",
  ["h"] = "ʰ",
  ["i"] = "ⁱ",
  ["j"] = "ʲ",
  ["k"] = "ᵏ",
  ["l"] = "ˡ",
  ["m"] = "ᵐ",
  ["n"] = "ⁿ",
  ["o"] = "ᵒ",
  ["p"] = "ᵖ",
  ["r"] = "ʳ",
  ["s"] = "ˢ",
  ["t"] = "ᵗ",
  ["u"] = "ᵘ",
  ["v"] = "ᵛ",
  ["w"] = "ʷ",
  ["x"] = "ˣ",
  ["y"] = "ʸ",
  ["z"] = "ᶻ",
  -- Uppercase letters (limited Unicode support)
  ["N"] = "ᴺ",
  -- Operators
  ["+"] = "⁺",
  ["-"] = "⁻",
  ["="] = "⁼",
  ["("] = "⁽",
  [")"] = "⁾",
}

-- Plain string replacement (not pattern-based)
local function plain_replace(text, find_str, replace_str)
  local start_pos = 1
  while true do
    local find_start, find_end = text:find(find_str, start_pos, true)  -- true = plain text search
    if not find_start then
      break
    end
    text = text:sub(1, find_start - 1) .. replace_str .. text:sub(find_end + 1)
    start_pos = find_start + #replace_str
  end
  return text
end

-- Check if a string contains complex LaTeX that can't be converted
local function is_complex_math(text)
  -- Patterns that indicate complex math
  local complex_patterns = {
    "\\frac",      -- fractions
    "\\int",       -- integrals
    "\\sum",       -- summations
    "\\prod",      -- products
    "\\lim",       -- limits
    "\\sqrt",      -- square roots
    "\\binom",     -- binomial coefficients
    "\\left",      -- large delimiters
    "\\right",
    "\\begin",     -- environments
    "\\operatorname",
    "\\mathcal",   -- special fonts we can't represent
    "\\mathbb",
    "\\mathfrak",
    "\\hat",       -- accents
    "\\bar",
    "\\tilde",
    "\\dot",
  }

  for _, pattern in ipairs(complex_patterns) do
    if text:find(pattern, 1, true) then
      return true
    end
  end

  -- Check for complex subscripts/superscripts (more than one character in braces)
  -- Pattern: _{...} or ^{...} where ... has length > 1
  -- UPDATED: Now allow multi-character subscripts/superscripts if they can be converted
  for subscript in text:gmatch("_(%b{})") do
    local content = subscript:sub(2, -2)  -- Remove braces
    -- Skip if contains backslash (LaTeX commands)
    if content:match("\\") then
      return true
    end
    -- Check if it's simple arithmetic: single char, +/-, single char
    local is_simple_arithmetic = content:match("^%w[-+]%w$")
    -- Check if it's all word characters (could be multi-char like "max")
    local is_word_chars_only = content:match("^%w+$")
    -- Complex if:
    --   - Has multiple chars AND
    --   - Is NOT simple arithmetic AND
    --   - Is NOT all word characters (which convert_subscript_string can handle)
    if content:match("%S.*%S") and not is_simple_arithmetic and not is_word_chars_only then
      return true
    end
  end

  for superscript in text:gmatch("%^(%b{})") do
    local content = superscript:sub(2, -2)  -- Remove braces
    -- Skip if contains backslash (LaTeX commands)
    if content:match("\\") then
      return true
    end
    -- Check if it's simple arithmetic: single char, +/-, single char
    local is_simple_arithmetic = content:match("^%w[-+]%w$")
    -- Check if it's all word characters (could be multi-char like "max")
    local is_word_chars_only = content:match("^%w+$")
    -- Complex if:
    --   - Has multiple chars AND
    --   - Is NOT simple arithmetic AND
    --   - Is NOT all word characters (which convert_superscript_string can handle)
    if content:match("%S.*%S") and not is_simple_arithmetic and not is_word_chars_only then
      return true
    end
  end

  return false
end

-- Convert simple subscript
local function convert_subscript_char(char)
  return subscripts[char] or nil
end

-- Convert simple superscript
local function convert_superscript_char(char)
  return superscripts[char] or nil
end

-- Convert multi-character string to subscript (each char individually)
local function convert_subscript_string(str)
  local result = ""
  for i = 1, #str do
    local char = str:sub(i, i)
    local unicode_char = subscripts[char]
    if not unicode_char then
      return nil  -- Can't convert this character
    end
    result = result .. unicode_char
  end
  return result
end

-- Convert multi-character string to superscript (each char individually)
local function convert_superscript_string(str)
  local result = ""
  for i = 1, #str do
    local char = str:sub(i, i)
    local unicode_char = superscripts[char]
    if not unicode_char then
      return nil  -- Can't convert this character
    end
    result = result .. unicode_char
  end
  return result
end

-- Try to convert math to Unicode (all-or-nothing strategy)
-- Returns: converted text if 100% successful, nil otherwise
local function try_unicode_conversion(text)
  -- Trim whitespace
  text = text:gsub("^%s+", ""):gsub("%s+$", "")

  -- STEP 1: Extract backtick pairs to protect them from subscript/superscript conversions
  -- We preserve operators BETWEEN backticks (e.g., `a` ≤ `b`)
  -- but prevent conversions INSIDE backticks (e.g., `numeric_limits` should stay as-is)
  -- Use hyphen instead of underscore to avoid subscript conversion on the placeholder itself
  local backtick_regions = {}
  local backtick_count = 0

  text = text:gsub("`([^`]*)`", function(content)
    backtick_count = backtick_count + 1
    local placeholder = "@@BACKTICK-" .. backtick_count .. "@@"
    backtick_regions[placeholder] = content
    return placeholder
  end)

  -- Start conversion
  local result = text

  -- Convert \mathtt{X} -> X (already monospace in markdown code)
  result = process_macro_with_replacement(result, "mathtt", function(content)
    return content
  end)

  -- Convert \mathrm{text} -> text
  result = process_macro_with_replacement(result, "mathrm", function(content)
    return content
  end)

  -- Convert \mathit{text} -> text (we'll use plain text)
  result = process_macro_with_replacement(result, "mathit", function(content)
    return content
  end)

  -- Convert \mathsf{text} -> text (sans-serif font)
  result = process_macro_with_replacement(result, "mathsf", function(content)
    return content
  end)

  -- Strip typesetting hint macros (they don't affect semantic meaning)
  -- \mathrel{...} -> ... (relational operator spacing)
  result = process_macro_with_replacement(result, "mathrel", function(content)
    return content
  end)

  -- \mathbin{...} -> ... (binary operator spacing)
  result = process_macro_with_replacement(result, "mathbin", function(content)
    return content
  end)

  -- Convert \cv{} (cv-qualifiers) to plain text
  result = result:gsub("\\cv{}", "cv")

  -- Strip outer grouping braces before ordinal superscripts
  -- This handles patterns like {k_i}^\text{th} -> k_i^\text{th}
  -- allowing the subscript conversion to work properly
  result = result:gsub("{([^}]+)}%^\\text{th}", "%1^\\text{th}")
  result = result:gsub("{([^}]+)}%^\\text{st}", "%1^\\text{st}")
  result = result:gsub("{([^}]+)}%^\\text{nd}", "%1^\\text{nd}")
  result = result:gsub("{([^}]+)}%^\\text{rd}", "%1^\\text{rd}")

  -- Also handle non-\text{} variants: {k_i}^{th} -> k_i^{th}
  result = result:gsub("{([^}]+)}%^{th}", "%1^{th}")
  result = result:gsub("{([^}]+)}%^{st}", "%1^{st}")
  result = result:gsub("{([^}]+)}%^{nd}", "%1^{nd}")
  result = result:gsub("{([^}]+)}%^{rd}", "%1^{rd}")

  -- Convert ordinal superscripts BEFORE \text{} conversion
  -- Patterns like $i^\text{th}$ -> iᵗʰ, $1^\text{st}$ -> 1ˢᵗ
  result = result:gsub("%^\\text{th}", "ᵗʰ")
  result = result:gsub("%^\\text{st}", "ˢᵗ")
  result = result:gsub("%^\\text{nd}", "ⁿᵈ")
  result = result:gsub("%^\\text{rd}", "ʳᵈ")

  -- Also handle ordinals without \text{} wrapper: $i^{th}$ -> iᵗʰ
  result = result:gsub("(%w)%^{th}", "%1ᵗʰ")
  result = result:gsub("(%w)%^{st}", "%1ˢᵗ")
  result = result:gsub("(%w)%^{nd}", "%1ⁿᵈ")
  result = result:gsub("(%w)%^{rd}", "%1ʳᵈ")

  -- Convert \text{text} -> text (text mode in math)
  result = process_macro_with_replacement(result, "text", function(content)
    return content
  end)

  -- Handle \textit{...} and \exposid{...} with special underscore protection
  -- If underscore appears INSIDE these macros, it's part of an identifier name, not a subscript
  -- Pattern: \textit{identifier_name} or \exposid{current_}
  -- We replace underscores inside with a placeholder to protect them from subscript conversion
  result = process_macro_with_replacement(result, "textit", function(content)
    -- Replace underscores with placeholder inside identifier names
    local protected_content = content:gsub("_", "@@UNDERSCORE@@")
    return protected_content
  end)

  result = process_macro_with_replacement(result, "exposid", function(content)
    -- Replace underscores with placeholder inside identifier names
    local protected_content = content:gsub("_", "@@UNDERSCORE@@")
    return protected_content
  end)

  -- Strip sizing commands (they don't affect the output, just LaTeX presentation)
  result = result:gsub("\\bigl%s*", "")
  result = result:gsub("\\bigr%s*", "")
  result = result:gsub("\\Bigl%s*", "")
  result = result:gsub("\\Bigr%s*", "")
  result = result:gsub("\\big%s*", "")
  result = result:gsub("\\Big%s*", "")

  -- Convert spacing commands to spaces
  result = result:gsub("\\quad", "  ")    -- quad = wider space
  result = result:gsub("\\qquad", "    ") -- qquad = even wider space
  result = result:gsub("\\,", " ")         -- thin space
  result = result:gsub("\\;", " ")         -- medium space
  result = result:gsub("\\!", "")          -- negative thin space (just remove)
  result = result:gsub("\\ ", " ")         -- control space (backslash-space)

  -- Convert known simple patterns FIRST (before checking for complex math)
  -- This prevents false positives like \rightarrow being flagged as complex due to \right

  -- Convert arrows using plain replacement
  for latex, unicode in pairs(arrows) do
    result = plain_replace(result, latex, unicode)
  end

  -- Convert floor/ceil delimiters using plain replacement
  for latex, unicode in pairs(delimiters) do
    result = plain_replace(result, latex, unicode)
  end

  -- Convert Greek letters using plain replacement
  for latex, unicode in pairs(greek_letters) do
    result = plain_replace(result, latex, unicode)
  end

  -- Convert ellipsis operators EARLY (before complexity check)
  -- This prevents them from being flagged as complex math
  result = plain_replace(result, "\\dotsc", "…")   -- Dots for series/commas
  result = plain_replace(result, "\\dotsb", "…")   -- Dots for binary operators
  result = plain_replace(result, "\\dotsm", "…")   -- Dots for multiplication
  result = plain_replace(result, "\\dotsi", "…")   -- Dots for integrals
  result = plain_replace(result, "\\dotso", "…")   -- Dots for other purposes
  result = plain_replace(result, "\\ldots", "…")   -- Generic dots
  result = plain_replace(result, "\\cdots", "⋯")   -- Centered dots
  result = plain_replace(result, "\\cdot", "⋅")    -- Centered dot (single)

  -- EARLY check for complex math BEFORE other operator conversions
  -- This prevents partial matches like \in matching prefix of \int
  if is_complex_math(result) then
    return nil
  end

  -- Convert remaining operators using plain replacement
  -- IMPORTANT: Sort by length (longest first) to avoid partial matches
  -- Ellipsis operators already converted above
  local ellipsis_ops = {
    ["\\dotsc"] = true, ["\\dotsb"] = true, ["\\dotsm"] = true,
    ["\\dotsi"] = true, ["\\dotso"] = true, ["\\ldots"] = true,
    ["\\cdots"] = true, ["\\cdot"] = true
  }

  local sorted_operators = {}
  for latex, unicode in pairs(math_operators) do
    if not ellipsis_ops[latex] then
      table.insert(sorted_operators, {latex = latex, unicode = unicode})
    end
  end
  table.sort(sorted_operators, function(a, b) return #a.latex > #b.latex end)

  for _, op in ipairs(sorted_operators) do
    result = plain_replace(result, op.latex, op.unicode)
  end

  -- Convert math functions using plain replacement
  for latex, text_replacement in pairs(math_functions) do
    result = plain_replace(result, latex, text_replacement)
  end

  -- Strip empty braces (used for spacing in LaTeX, e.g., cv{}_i)
  -- Do this AFTER all macro conversions but BEFORE complexity check
  -- so empty braces don't cause unnecessary conversion failures
  result = result:gsub("{}", "")

  -- NOW check if this is complex math that shouldn't be converted
  -- (after simple conversions, so we don't have false positives)
  if is_complex_math(result) then
    return nil
  end

  -- Convert simple superscripts: x^2 or x^{n}
  -- First pass: check if all superscripts are convertible
  local has_unconvertible_super = false
  result:gsub("(%w)%^(%w)", function(base, exp)
    if not convert_superscript_char(exp) then
      has_unconvertible_super = true
    end
  end)
  result:gsub("(%w)%^{(%w)}", function(base, exp)
    if not convert_superscript_char(exp) then
      has_unconvertible_super = true
    end
  end)

  -- Check bare superscripts: ^n, ^{n} (without base identifier)
  result:gsub("^%^(%w)$", function(exp)
    if not convert_superscript_char(exp) then
      has_unconvertible_super = true
    end
  end)
  result:gsub("^%^{(%w)}$", function(exp)
    if not convert_superscript_char(exp) then
      has_unconvertible_super = true
    end
  end)

  -- Check arithmetic superscripts: x^{N-1}, 2^{i+1}
  result:gsub("(%w)%^{(%w)([-+])(%w)}", function(base, super1, op, super2)
    if not convert_superscript_char(super1) or not convert_superscript_char(op) or not convert_superscript_char(super2) then
      has_unconvertible_super = true
    end
  end)

  if has_unconvertible_super then
    return nil  -- Abort conversion if any superscript can't be converted
  end

  -- IMPORTANT: Handle bare subscript + superscript combinations FIRST (before individual conversions)
  -- Pattern: _i^n → ᵢⁿ, _{i}^{n} → ᵢⁿ
  -- This must run before individual superscript conversion to avoid `_i^n` → `_iⁿ`
  result = result:gsub("_(%w)%^(%w)", function(sub, super)
    local unicode_sub = convert_subscript_char(sub)
    local unicode_super = convert_superscript_char(super)
    return unicode_sub .. unicode_super
  end)
  result = result:gsub("_{(%w)}%^{(%w)}", function(sub, super)
    local unicode_sub = convert_subscript_char(sub)
    local unicode_super = convert_superscript_char(super)
    return unicode_sub .. unicode_super
  end)
  result = result:gsub("_(%w)%^{(%w)}", function(sub, super)
    local unicode_sub = convert_subscript_char(sub)
    local unicode_super = convert_superscript_char(super)
    return unicode_sub .. unicode_super
  end)
  result = result:gsub("_{(%w)}%^(%w)", function(sub, super)
    local unicode_sub = convert_subscript_char(sub)
    local unicode_super = convert_superscript_char(super)
    return unicode_sub .. unicode_super
  end)

  -- Second pass: actually convert
  result = result:gsub("(%w)%^(%w)", function(base, exp)
    local unicode_exp = convert_superscript_char(exp)
    return base .. unicode_exp
  end)

  result = result:gsub("(%w)%^{(%w)}", function(base, exp)
    local unicode_exp = convert_superscript_char(exp)
    return base .. unicode_exp
  end)

  -- Convert bare superscripts: ^n → ⁿ, ^{n} → ⁿ (without base identifier)
  result = result:gsub("^%^(%w)$", function(exp)
    local unicode_exp = convert_superscript_char(exp)
    return unicode_exp or ("^" .. exp)
  end)

  result = result:gsub("^%^{(%w)}$", function(exp)
    local unicode_exp = convert_superscript_char(exp)
    return unicode_exp or ("^{" .. exp .. "}")
  end)

  -- Convert arithmetic superscripts: x^{N-1} → xᴺ⁻¹, 2^{i+1} → 2ⁱ⁺¹
  -- Pattern: x^{N-1}, 2^{i+1}
  result = result:gsub("(%w)%^{(%w)([-+])(%w)}", function(base, super1, op, super2)
    local unicode_super1 = convert_superscript_char(super1)
    local unicode_op = convert_superscript_char(op)
    local unicode_super2 = convert_superscript_char(super2)
    return base .. unicode_super1 .. unicode_op .. unicode_super2
  end)

  -- Convert simple subscripts: x_i or x_{0}
  -- First pass: check if all subscripts are convertible
  local has_unconvertible_sub = false
  result:gsub("(%w)_(%w)", function(base, sub)
    if not convert_subscript_char(sub) then
      has_unconvertible_sub = true
    end
  end)
  result:gsub("(%w)_{(%w)}", function(base, sub)
    if not convert_subscript_char(sub) then
      has_unconvertible_sub = true
    end
  end)

  -- Check bare subscripts: _n, _{n} (without base identifier)
  result:gsub("^_(%w)$", function(sub)
    if not convert_subscript_char(sub) then
      has_unconvertible_sub = true
    end
  end)
  result:gsub("^_{(%w)}$", function(sub)
    if not convert_subscript_char(sub) then
      has_unconvertible_sub = true
    end
  end)

  -- Check arithmetic subscripts: x_{n-1}, x_{i+1}
  result:gsub("(%w)_{(%w)([-+])(%w)}", function(base, sub1, op, sub2)
    if not convert_subscript_char(sub1) or not convert_subscript_char(op) or not convert_subscript_char(sub2) then
      has_unconvertible_sub = true
    end
  end)

  if has_unconvertible_sub then
    return nil  -- Abort conversion if any subscript can't be converted
  end

  -- Second pass: actually convert arithmetic subscripts first (before simple ones)
  -- Pattern: x_{n-1} → xₙ₋₁, p_{i+1} → pᵢ₊₁
  result = result:gsub("(%w)_{(%w)([-+])(%w)}", function(base, sub1, op, sub2)
    local unicode_sub1 = convert_subscript_char(sub1)
    local unicode_op = convert_subscript_char(op)
    local unicode_sub2 = convert_subscript_char(sub2)
    return base .. unicode_sub1 .. unicode_op .. unicode_sub2
  end)

  -- Iterate subscript conversion until no more changes occur
  -- This handles consecutive subscripts like c_1c_2...c_k → c₁c₂...cₖ
  local max_iterations = 10
  local iteration = 0
  local prev_result

  repeat
    prev_result = result
    iteration = iteration + 1

    -- Then convert simple subscripts (but leave subscripts that are part of sub+super combinations like _i^n)
    -- Handle subscripts NOT followed by superscript
    result = result:gsub("(%w)_(%w)([^%^])", function(base, sub, after)
      local unicode_sub = convert_subscript_char(sub)
      return base .. unicode_sub .. after
    end)
    result = result:gsub("(%w)_(%w)$", function(base, sub)
      local unicode_sub = convert_subscript_char(sub)
      return base .. unicode_sub
    end)

    result = result:gsub("(%w)_{(%w)}([^%^])", function(base, sub, after)
      local unicode_sub = convert_subscript_char(sub)
      return base .. unicode_sub .. after
    end)
    result = result:gsub("(%w)_{(%w)}$", function(base, sub)
      local unicode_sub = convert_subscript_char(sub)
      return base .. unicode_sub
    end)

    -- Convert bare subscripts: _n → ₙ, _{n} → ₙ (without base identifier)
    result = result:gsub("^_(%w)$", function(sub)
      local unicode_sub = convert_subscript_char(sub)
      return unicode_sub or ("_" .. sub)
    end)

    result = result:gsub("^_{(%w)}$", function(sub)
      local unicode_sub = convert_subscript_char(sub)
      return unicode_sub or ("_{" .. sub .. "}")
    end)

    -- Handle subscripts after Unicode superscripts (e.g., xⁱ_j → xⁱⱼ, cvʲ_i → cvʲᵢ)
    -- This needs to run AFTER superscript conversion
    -- Match any Unicode superscript character followed by _char or _{char}
    local superscript_chars = "[⁰¹²³⁴⁵⁶⁷⁸⁹ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻᴺ⁺⁻⁼⁽⁾]"

    result = result:gsub("(" .. superscript_chars .. ")_(%w)", function(super_char, sub_char)
      local unicode_sub = convert_subscript_char(sub_char)
      if unicode_sub then
        return super_char .. unicode_sub
      else
        return super_char .. "_" .. sub_char  -- Keep original if conversion fails
      end
    end)

    result = result:gsub("(" .. superscript_chars .. ")_{(%w)}", function(super_char, sub_char)
      local unicode_sub = convert_subscript_char(sub_char)
      if unicode_sub then
        return super_char .. unicode_sub
      else
        return super_char .. "_{" .. sub_char .. "}"  -- Keep original if conversion fails
      end
    end)

    -- Handle subscripts after Unicode subscripts (e.g., c₁_2 → c₁₂, x₀_n → x₀ₙ)
    -- This fixes consecutive subscripts like c_1c_2...c_k → c₁c₂...cₖ
    -- Match any Unicode subscript character followed by _char or _{char}
    local subscript_chars = "[₀₁₂₃₄₅₆₇₈₉ₐₑₒᵣₓₕₖₗₘₙₚₛₜᵤᵥᵢⱼ₊₋₌₍₎]"

    result = result:gsub("(" .. subscript_chars .. ")_(%w)", function(sub_char, next_sub)
      local unicode_sub = convert_subscript_char(next_sub)
      if unicode_sub then
        return sub_char .. unicode_sub
      else
        return sub_char .. "_" .. next_sub  -- Keep original if conversion fails
      end
    end)

    result = result:gsub("(" .. subscript_chars .. ")_{(%w)}", function(sub_char, next_sub)
      local unicode_sub = convert_subscript_char(next_sub)
      if unicode_sub then
        return sub_char .. unicode_sub
      else
        return sub_char .. "_{" .. next_sub .. "}"  -- Keep original if conversion fails
      end
    end)

  until result == prev_result or iteration >= max_iterations

  -- Handle multi-character subscripts: _{max} → ₘₐₓ, x_{max} → xₘₐₓ
  -- Pattern: _{word+} where each character is converted individually
  -- First pass: check if all characters are convertible
  local has_unconvertible_multi_sub = false
  result:gsub("(%w?)_{(%w%w+)}", function(base, sub_str)
    if not convert_subscript_string(sub_str) then
      has_unconvertible_multi_sub = true
    end
  end)

  if has_unconvertible_multi_sub then
    return nil  -- Abort conversion if any multi-char subscript can't be converted
  end

  -- Second pass: actually convert multi-character subscripts
  result = result:gsub("(%w?)_{(%w%w+)}", function(base, sub_str)
    local unicode_sub = convert_subscript_string(sub_str)
    return base .. unicode_sub
  end)

  -- Handle multi-character superscripts: ^{max} → ᵐᵃˣ, x^{max} → xᵐᵃˣ
  -- First pass: check if all characters are convertible
  local has_unconvertible_multi_super = false
  result:gsub("(%w?)%^{(%w%w+)}", function(base, super_str)
    if not convert_superscript_string(super_str) then
      has_unconvertible_multi_super = true
    end
  end)

  if has_unconvertible_multi_super then
    return nil  -- Abort conversion if any multi-char superscript can't be converted
  end

  -- Second pass: actually convert multi-character superscripts
  result = result:gsub("(%w?)%^{(%w%w+)}", function(base, super_str)
    local unicode_super = convert_superscript_string(super_str)
    return base .. unicode_super
  end)

  -- If we still have LaTeX commands, we can't fully convert
  if result:match("\\[a-zA-Z]") then
    return nil
  end

  -- If we still have ^{ or _{ patterns, we couldn't convert them
  if result:match("[%^_]{") then
    return nil
  end

  -- FINAL STEP: Restore backtick regions (preserve original content inside backticks)
  -- Use literal string replacement (not pattern-based) to avoid issues with special characters
  -- Unescape \_ to _ inside backticks (LaTeX escaped underscores should be literal in code)
  for placeholder, content in pairs(backtick_regions) do
    local start_pos = result:find(placeholder, 1, true)  -- true = plain text search
    if start_pos then
      local end_pos = start_pos + #placeholder - 1
      -- Unescape LaTeX escaped characters inside code
      local unescaped_content = content:gsub("\\_", "_")
      result = result:sub(1, start_pos - 1) .. "`" .. unescaped_content .. "`" .. result:sub(end_pos + 1)
    end
  end

  -- Restore protected underscores from \textit{} and \exposid{} identifiers
  result = result:gsub("@@UNDERSCORE@@", "_")

  return result
end

-- Helper function to convert math patterns in code
-- Used by clean_code_common() for code block cleaning
local function convert_math_in_code(text)
  -- Process @$...$@ patterns (math mode in code blocks)
  -- These contain subscripts, placeholders, and math symbols
  text = text:gsub("@%$(.-)%$@", function(math_content)
    -- Convert all ellipsis operators to Unicode for consistency
    math_content = math_content:gsub("\\dotsc", "…")
    math_content = math_content:gsub("\\dotsb", "…")
    math_content = math_content:gsub("\\dotsm", "…")
    math_content = math_content:gsub("\\dotsi", "…")
    math_content = math_content:gsub("\\dotso", "…")
    math_content = math_content:gsub("\\ldots", "…")
    math_content = math_content:gsub("\\cdots", "⋯")

    -- Convert subscripts: \tcode{\placeholder{X}}_{n} → Xₙ
    -- Or: \tcode{\placeholder{X}_{n}} → Xₙ
    -- NOTE: Using ([^}]*) here is acceptable because this is within @$...$@ context
    -- where the @ delimiters prevent complex nesting in actual C++ standard usage
    math_content = math_content:gsub(
      "\\tcode{\\placeholder{([^}]*)}}_{{?([%w]+)}?}",
      function(name, sub)
      if subscripts[sub] then
        return name .. subscripts[sub]
      else
        return name .. "_" .. sub
      end
    end)

    -- Convert subscripts in simpler form: \tcode{\placeholder{X}}_{n} without nested braces
    -- NOTE: Using ([^}]*) here is acceptable - same reason as above
    math_content = math_content:gsub("\\tcode{([^}]*)}_{{?([%w]+)}?}", function(name, sub)
      -- Remove \placeholder{} wrapper if present
      -- NOTE: Using ([^}]*) here is acceptable - same reason as above
      name = name:gsub("\\placeholder{([^}]*)}", "%1")
      if subscripts[sub] then
        return name .. subscripts[sub]
      else
        return name .. "_" .. sub
      end
    end)

    -- Convert standalone subscripts: X_{n} → Xₙ or X_n → Xₙ
    -- Fixed pattern: _{?...}? to properly handle both X_n and X_{n}
    math_content = math_content:gsub("([%w]+)_{?([%w]+)}?", function(name, sub)
      if subscripts[sub] then
        return name .. subscripts[sub]
      else
        return name .. "_" .. sub
      end
    end)

    -- Remove remaining \tcode{} and \placeholder{} wrappers
    -- NOTE: Using ([^}]*) here is acceptable - same reason as above
    math_content = math_content:gsub("\\tcode{([^}]*)}", "%1")
    math_content = math_content:gsub("\\placeholder{([^}]*)}", "%1")

    return math_content
  end)

  -- Also process plain $...$ patterns (inline math in code comments without @ delimiters)
  -- Use comprehensive math-to-Unicode conversion (all-or-nothing strategy)
  text = text:gsub("%$([^$]+)%$", function(math_content)
    -- Try comprehensive Unicode conversion
    local converted = try_unicode_conversion(math_content)
    if converted then
      return converted
    else
      -- Conversion failed or incomplete, preserve original $...$ delimiters
      return "$" .. math_content .. "$"
    end
  end)

  -- Convert standalone @\vdots@ to Unicode vertical ellipsis
  text = text:gsub("@\\vdots@", "⋮")
  text = text:gsub("\\vdots", "⋮")

  -- Convert standalone @\ldots@ to Unicode ellipsis
  text = text:gsub("@\\ldots@", "…")
  text = text:gsub("\\ldots", "…")

  return text
end

-- Unified function to clean up LaTeX escapes in code blocks
-- Used by cpp-code-blocks.lua and cpp-notes-examples.lua
-- Merges ALL logic from both filters for consistent code handling
--
-- Parameters:
--   code: The code text to clean
--   handle_textbackslash: If true, special handling for \textbackslash in @\tcode{}@ blocks
--
-- Returns:
--   Cleaned code text
local function clean_code_common(code, handle_textbackslash)
  -- Remove @ escape delimiters and expand common macros

  -- First, convert math patterns (@$...$@) before processing other escapes
  code = convert_math_in_code(code)

  -- \commentellip represents "..."
  code = code:gsub("@\\commentellip@", "...")

  -- Special case for cpp-notes-examples.lua: preserve newlines after
  -- \textbackslash in @\tcode{}@ blocks. Must be handled BEFORE general expansion
  if handle_textbackslash then
    code = code:gsub("@\\tcode{([^@]-)\\textbackslash}@\n", function(content)
      return content .. "\\\n"
    end)
  end

  -- Expand macros in multiple passes to handle nesting (e.g., \tcode{\keyword{x}})
  -- Use shared macro patterns from code_block_macro_patterns
  -- For cpp-notes-examples.lua with textbackslash handling, override @\tcode pattern
  local macro_patterns
  if handle_textbackslash then
    macro_patterns = {}
    for i, v in ipairs(code_block_macro_patterns) do
      macro_patterns[i] = v
    end
    -- Override the first @\tcode pattern to use ([^@]-) for special textbackslash handling
    macro_patterns[1] = {pattern = "@\\tcode{([^@]-)}@", replacement = "%1"}
    code = expand_nested_macros_recursive(code, macro_patterns, 5)
  else
    code = expand_nested_macros_recursive(code, code_block_macro_patterns, 5)
  end

  -- Concept macros (library, exposition-only, and old-style concepts)
  code = expand_concept_macros(code, true)

  -- Handle escaped special characters
  code = code:gsub("\\#", "#")
  code = code:gsub("\\%%", "%")
  code = code:gsub("\\&", "&")
  code = code:gsub("\\$", "$")
  code = code:gsub("\\{", "{")
  code = code:gsub("\\}", "}")
  -- Tilde (issue #8) - \~ is LaTeX tilde accent, convert to plain tilde
  code = code:gsub("\\~{([^}]*)}", "~%1")  -- \~{identifier} → ~identifier (remove braces)
  code = code:gsub("\\~", "~")  -- any remaining \~ → ~

  -- Remove LaTeX spacing commands that should not appear in code
  code = code:gsub("\\;", "")  -- \; is a medium space in LaTeX
  code = code:gsub("\\:", "")  -- \: is a medium space in LaTeX
  code = code:gsub("\\,", "")  -- \, is a thin space in LaTeX
  code = code:gsub("\\!", "")  -- \! is a negative thin space in LaTeX

  -- Cross-references - convert to [label]
  code = convert_cross_references_in_code(code, true)

  -- \defn{x} definition terms
  -- NOTE: Both @...@ and bare versions use simple ([^}]*) pattern because:
  -- 1) @ delimiters prevent nesting in actual C++ standard usage
  -- 2) Definition terms in code are typically simple text without nested braces
  code = code:gsub("@\\defn{([^}]*)}@", "%1")
  code = code:gsub("\\defn{([^}]*)}", "%1")

  -- \defexposconcept{x} exposition-only concept definition
  -- NOTE: Same reasoning as \defn - simple patterns are acceptable here
  code = code:gsub("@\\defexposconcept{([^}]*)}@", "%1")
  code = code:gsub("\\defexposconcept{([^}]*)}", "%1")

  -- \cv represents "cv"
  code = code:gsub("@\\cv{}@", "cv")
  code = code:gsub("\\cv{}", "cv")
  code = code:gsub("\\cv%s", "cv ")

  -- C++ version macros
  code = expand_cpp_version_macros(code)

  -- Library specification macros
  code = expand_library_spec_macros(code, true)

  -- \defnlibxname{X} represents __X (used for feature test macro names like __cpp_lib_*)
  -- This expands to \xname{X} in the LaTeX, which should become __X
  -- NOTE: Both @...@ and bare versions use simple ([^}]*) pattern because:
  -- 1) @ delimiters prevent nesting in actual C++ standard usage
  -- 2) Macro names are simple identifiers without nested braces
  code = code:gsub("@\\defnlibxname{([^}]*)}@", "__%1")
  code = code:gsub("\\defnlibxname{([^}]*)}", "__%1")

  -- \xname{X} represents __X (special identifiers with underscore prefix)
  -- NOTE: Same reasoning - simple patterns acceptable
  code = code:gsub("@\\xname{([^}]*)}@", "__%1")
  code = code:gsub("\\xname{([^}]*)}", "__%1")

  -- \mname{X} represents __X__ (preprocessor macro names with underscore wrapper)
  -- NOTE: Same reasoning - simple patterns acceptable
  code = code:gsub("@\\mname{([^}]*)}@", "__%1__")
  code = code:gsub("\\mname{([^}]*)}", "__%1__")

  -- \libheader{X} represents <X> in code blocks (without backticks, plain angle brackets)
  -- NOTE: Same reasoning - header names are simple
  code = code:gsub("@\\libheader{([^}]*)}@", "<%1>")
  code = code:gsub("\\libheader{([^}]*)}", "<%1>")

  -- \ucode{XXXX} represents Unicode code point U+XXXX (process before \textrm to handle nesting)
  -- NOTE: Same reasoning - code points are simple hex values
  code = code:gsub("@\\ucode{([^}]*)}@", "U+%1")
  code = code:gsub("\\ucode{([^}]*)}", "U+%1")

  -- \colcol{} represents ::
  code = code:gsub("\\colcol{}", "::")

  -- Strip \brk{} line break hints
  code = code:gsub("\\brk{}", "")

  -- Math formatting in code comments
  -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
  code = process_macro_with_replacement(code, "mathit", function(content)
    return content
  end)
  code = process_macro_with_replacement(code, "mathrm", function(content)
    return content
  end)

  -- Text formatting in code comments - strip the commands but keep content
  -- Handle @\textrm{}@, @\textit{}@, and @\texttt{}@ with nested braces
  while true do
    local changed = false
    local new_code = code:gsub("@\\textrm{([^{}@]*)}@", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    new_code = code:gsub("@\\textit{([^{}@]*)}@", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    new_code = code:gsub("@\\texttt{([^{}@]*)}@", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    -- Also handle bare versions (not in @ delimiters)
    new_code = code:gsub("\\textrm{([^{}]*)}", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    new_code = code:gsub("\\textit{([^{}]*)}", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    new_code = code:gsub("\\texttt{([^{}]*)}", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    if not changed then break end
  end

  -- \ref{x} cross-references
  -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
  code = process_macro_with_replacement(code, "ref", function(content)
    return "[" .. content .. "]"
  end)

  -- \tref{x} table cross-references (also use [label] format)
  -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
  code = process_macro_with_replacement(code, "tref", function(content)
    return "[" .. content .. "]"
  end)

  -- \range{first}{last} macro for half-open ranges
  -- Use extract_braced_content twice for 2-argument macro (fixes ([^}]*) anti-pattern)
  local range_pattern = "\\range{"
  local range_len = 6  -- length of "\range"
  while true do
    local range_start = code:find(range_pattern, 1, true)
    if not range_start then break end

    local first, pos1 = extract_braced_content(code, range_start, range_len)
    if not first then break end

    local second, pos2 = extract_braced_content(code, pos1 - 1, 1)  -- pos1-1 to include the brace
    if not second then break end

    code = code:sub(1, range_start - 1) .. "[" .. first .. ", " .. second .. ")" .. code:sub(pos2)
  end

  -- Strip indexing commands (these should not appear in code blocks but handle defensively)
  code = code:gsub("\\indexlibrary[^{]*{[^}]*}", "")
  code = code:gsub("\\indexlibraryglobal{[^}]*}", "")

  -- \impldef{description} -> "implementation-defined" (used in @\UNSP{\impldef{}}@)
  -- Handle this before \UNSP{} so nested macros get expanded
  -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
  code = process_macro_with_replacement(code, "impldef", function(content)
    return "implementation-defined"
  end)

  -- \UNSP{x} represents unspecified value (italic monospace in LaTeX)
  -- In code blocks, just extract the content (may contain nested macros)
  -- Must handle nested braces iteratively
  while true do
    local new_code = code:gsub("@\\UNSP{([^{}@]*)}@", "%1")
    if new_code == code then break end
    code = new_code
  end
  -- Also handle bare \UNSP{} (without @ delimiters)
  while true do
    local new_code = code:gsub("\\UNSP{([^{}]*)}", "%1")
    if new_code == code then break end
    code = new_code
  end

  -- Handle \textbackslash for cpp-notes-examples.lua
  if handle_textbackslash then
    code = code:gsub("\\textbackslash", "\\")
  end

  -- Remove any @ delimiters first (escape markers from listings package)
  code = code:gsub("@([^@]*)@", "%1")

  -- Remove unnecessary LaTeX grouping braces
  -- Pattern: {'<content>} where content is punctuation/short text
  -- Example: M{'s} → M's (possessive after \tcode{M})
  code = code:gsub("{('[ %w]+)}", "%1")  -- {' followed by letters/spaces

  -- Remove font switch commands (bare commands without arguments)
  -- Process these BEFORE overlap commands since they may appear inside
  code = remove_font_switches(code)

  -- Handle layout overlap commands: \rlap{}, \llap{}, \clap{}
  -- These create overlapping text in LaTeX - just extract the content
  -- After removing font switches above, the content should be simpler
  code = handle_overlap_commands(code)

  -- Clean up extra whitespace but preserve indentation
  -- Remove trailing whitespace from each line
  code = code:gsub("[ \t]+\n", "\n")

  return code
end

-- Helper function to split comma-separated references and create individual links
-- E.g., "a,b,c" -> "[[a]], [[b]], [[c]]"
-- Parameters:
--   refs_str: Comma-separated reference string
--   references_table: Optional table to track references (ref -> true)
-- Returns:
--   Text string with formatted references
local function split_refs_text(refs_str, references_table)
  local parts = {}
  for ref in refs_str:gmatch("([^,]+)") do
    ref = trim(ref)  -- trim whitespace
    if references_table then
      references_table[ref] = true
    end
    table.insert(parts, "[[" .. ref .. "]]")
  end
  return table.concat(parts, ", ")
end

-- Helper function to convert LaTeX spacing commands to regular spaces
-- Used by expand_macros_common() and cpp-macros.lua
-- Converts various LaTeX spacing commands to regular spaces
local function convert_latex_spacing(text)
  text = text:gsub("\\enspace", " ")
  -- Handle \quad and \qquad with following space FIRST to avoid double spacing
  text = text:gsub("\\quad ", " ")    -- Wide space (with following space)
  text = text:gsub("\\quad", " ")     -- Wide space (standalone)
  text = text:gsub("\\qquad ", " ")   -- Very wide space (with following space)
  text = text:gsub("\\qquad", " ")    -- Very wide space (standalone)
  text = text:gsub("\\;", " ")        -- Medium space
  text = text:gsub("\\,", " ")        -- Thin space
  text = text:gsub("\\!", " ")        -- Negative thin space (convert to regular space)
  -- NOTE: Bare ~ (non-breaking space) is NOT converted here because it can
  -- interfere with escaped sequences like \~ (tilde) after backslash processing
  return text
end

-- Helper function to convert \mname{} macro
-- Used by expand_macros_common() and individual filters
-- \mname{X} renders as __X__ (preprocessor macro names with underscore wrapper)
-- Handles special cases: VA_ARGS, VA_OPT
local function convert_mname(text)
  -- Handle specific cases first
  text = text:gsub("\\mname{VA_ARGS}", "__VA_ARGS__")
  text = text:gsub("\\mname{VA_OPT}", "__VA_OPT__")
  -- Then handle generic case
  -- NOTE: Using ([^}]*) is acceptable - macro names are simple identifiers without nested braces
  text = text:gsub("\\mname{([^}]*)}", "__%1__")
  return text
end

-- Consolidated macro expansion function for use across multiple filters
-- Handles common macro expansion patterns with context-specific options
--
-- Parameters:
--   text: The text to process
--   options: Table of options controlling behavior:
--     .skip_special_chars: Skip special character conversion (for BNF blocks)
--     .spec_labels: Convert specification labels (expects, requires, etc.) to \textit{}
--     .ref_format: "wikilink" for [[ref]], "placeholder" for @@REF:ref@@,
--                  or function(refs) for custom
--     .escape_at_macros: Handle @ escaped macros for code blocks
--     .convert_to_latex: Use \textit{} and \texttt{} instead of markdown *x* and `x`
--     .minimal: Only expand minimal set (for notes/examples context)
--     .strip_indexlibrary: Strip \indexlibrary{} macros
--
-- Returns:
--   Text with macros expanded according to options
local function expand_macros_common(text, options)
  if not text then return text end
  options = options or {}

  -- Tier 1: Critical preprocessing (always done unless minimal mode)
  if not options.minimal then
    -- Strip discretionary hyphen \- used for line breaking (BEFORE processing \tcode)
    text = text:gsub("\\%-", "")

    -- Strip \itcorr[...] italic correction markers (PDF spacing corrections)
    text = text:gsub("\\itcorr%[%-?%d*%]", "")

    -- Convert LaTeX spacing commands to regular spaces (BEFORE processing \tcode)
    -- Skip when convert_to_latex=true: Pandoc will handle \, correctly in math vs text
    if not options.convert_to_latex then
      text = convert_latex_spacing(text)
    end

    -- \impdefx{description} renders as "implementation-defined  // description"
    -- MUST be processed BEFORE \tcode{} conversion to handle nested \tcode{}
    text = expand_impdefx_in_text(text, "\\impdefx{", 9, nil)

    -- Strip indexlibrary if requested (itemdecl context)
    if options.strip_indexlibrary then
      text = remove_macro(text, "indexlibrary", false)
    end
  end

  -- Tier 2: Specification labels (itemdecl context only)
  if options.spec_labels then
    local spec_label_macros = {
      {pattern = "\\expects", replacement = "\\textit{Preconditions:}"},
      {pattern = "\\requires", replacement = "\\textit{Requires:}"},
      {pattern = "\\constraints", replacement = "\\textit{Constraints:}"},
      {pattern = "\\effects", replacement = "\\textit{Effects:}"},
      {pattern = "\\ensures", replacement = "\\textit{Ensures:}"},
      {pattern = "\\returns", replacement = "\\textit{Returns:}"},
      {pattern = "\\result", replacement = "\\textit{Result:}"},
      {pattern = "\\postconditions", replacement = "\\textit{Postconditions:}"},
      {pattern = "\\complexity", replacement = "\\textit{Complexity:}"},
      {pattern = "\\remarks", replacement = "\\textit{Remarks:}"},
      {pattern = "\\throws", replacement = "\\textit{Throws:}"},
      {pattern = "\\errors", replacement = "\\textit{Error conditions:}"},
      {pattern = "\\mandates", replacement = "\\textit{Mandates:}"},
      {pattern = "\\recommended", replacement = "\\textit{Recommended practice:}"},
      {pattern = "\\required", replacement = "\\textit{Required behavior:}"},
      {pattern = "\\default", replacement = "\\textit{Default behavior:}"},
      {pattern = "\\sync", replacement = "\\textit{Synchronization:}"},
      {pattern = "\\replaceable", replacement = "\\textit{Replaceable:}"},
      {pattern = "\\returntype", replacement = "\\textit{Return type:}"},
      {pattern = "\\ctype", replacement = "\\textit{Type:}"},
      {pattern = "\\templalias", replacement = "\\textit{Alias template:}"},
      {pattern = "\\implimits", replacement = "\\textit{Implementation limits:}"},
    }

    for _, macro in ipairs(spec_label_macros) do
      -- Handle both \macro\n and \macro<space> patterns
      text = text:gsub(macro.pattern .. "%s*\n", macro.replacement .. " ")
      text = text:gsub(macro.pattern .. "%s+", macro.replacement .. " ")
    end
  end

  -- Tier 3: @ escaped macros (itemdecl code blocks context)
  if options.escape_at_macros then
    -- These convert @ delimited macros to plain text for code blocks
    text = text:gsub("@\\placeholdernc{([^}]*)}@", "%1")
    text = text:gsub("@\\placeholder{([^}]*)}@", "%1")
    text = text:gsub("@\\tcode{([^}]*)}@", "%1")
    text = text:gsub("@\\exposid{([^}]*)}@", "%1")
    text = text:gsub("@\\libconcept{([^}]*)}@", "%1")
    text = text:gsub("@\\exposconcept{([^}]*)}@", "%1")
    text = text:gsub("@\\defexposconcept{([^}]*)}@", "%1")
    text = text:gsub("@\\commentellip@", "...")
    text = text:gsub("@", "")
  end

  -- Tier 4: Code formatting macros
  if options.convert_to_latex then
    -- Convert to LaTeX commands that Pandoc will process
    text = text:gsub("\\keyword{", "\\texttt{")
    text = text:gsub("\\ctype{", "\\texttt{")
    text = text:gsub("\\tcode{", "\\texttt{")
    text = text:gsub("\\libconcept{", "\\texttt{")
    text = text:gsub("\\exposconcept{", "\\texttt{")
  elseif not options.minimal then
    -- Convert to \texttt for Pandoc (standard behavior for cpp-macros.lua)
    text = text:gsub("\\keyword{", "\\texttt{")
    text = text:gsub("\\ctype{", "\\texttt{")
    text = text:gsub("\\tcode{", "\\texttt{")
  end

  -- Tier 5: Grammar and special identifiers
  if not options.minimal then
    if options.convert_to_latex then
      -- Use \textit{} for Pandoc to process
      text = text:gsub("\\grammarterm{", "\\textit{")
      text = text:gsub("\\placeholder{", "\\textit{")
      text = text:gsub("\\placeholdernc{", "\\textit{")
      text = text:gsub("\\exposid{", "\\textit{")
      -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
      text = process_macro_with_replacement(text, "oldconcept", function(content)
        return "\\textit{Cpp17" .. content .. "}"
      end)
    else
      -- Use *italic* markdown (cpp-macros.lua behavior)
      -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
      text = process_macro_with_replacement(text, "grammarterm", function(content)
        return "*" .. content .. "*"
      end)
      text = process_macro_with_replacement(text, "placeholder", function(content)
        return "*" .. content .. "*"
      end)
      text = process_macro_with_replacement(text, "placeholdernc", function(content)
        return "*" .. content .. "*"
      end)
    end
  end

  -- Tier 6: C++ and library version macros
  if options.minimal then
    -- Minimal mode: just expand \Cpp variants
    text = text:gsub("\\Cpp{}", "C++")
    text = text:gsub("\\Cpp%s", "C++ ")
    text = text:gsub("\\Cpp([^%w])", "C++%1")
    text = text:gsub("\\IsoC{}", "ISO/IEC 9899:2018 (C)")
  else
    -- Full mode: expand all C++ versions
    text = expand_cpp_version_macros(text)

    -- Library chapter references (if FIRSTLIB and LASTLIB are set)
    -- Note: These globals are set in Meta() by cpp-macros.lua
    if _G.FIRSTLIB then
      text = text:gsub("\\firstlibchapter{}", _G.FIRSTLIB)
      text = text:gsub("\\firstlibchapter", _G.FIRSTLIB)
    end
    if _G.LASTLIB then
      text = text:gsub("\\lastlibchapter{}", _G.LASTLIB)
      text = text:gsub("\\lastlibchapter", _G.LASTLIB)
    end

    -- \stage{N} -> Stage N: (skip when convert_to_latex=true to preserve for Pandoc)
    if not options.convert_to_latex then
      -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
      text = process_macro_with_replacement(text, "stage", function(content)
        return "Stage " .. content .. ":"
      end)
    end
  end

  -- Tier 7: Term/definition macros
  if options.minimal or options.convert_to_latex then
    text = text:gsub("\\term{", "\\emph{")
    text = text:gsub("\\defn{", "\\emph{")
  end

  -- Tier 8: Special characters (skip for BNF context and LaTeX output mode)
  if not options.skip_special_chars and not options.minimal then
    -- IMPORTANT: When convert_to_latex=true, we're preparing text for Pandoc's LaTeX reader
    -- Pandoc will handle \textbackslash → \ conversion itself
    -- Converting too early breaks Pandoc's parsing (e.g., '\n' becomes '``')
    if not options.convert_to_latex then
      text = convert_special_chars(text)
    end
  end

  -- Tier 9: Preprocessor and special macros
  if not options.minimal then
    -- \caret, \unun - special characters that Pandoc macro preprocessing can't handle
    text = text:gsub("\\caret{}", "^")
    text = text:gsub("\\caret%s", "^ ")
    text = text:gsub("\\caret([^a-zA-Z])", "^%1")
    text = text:gsub("\\unun{}", "__")
    text = text:gsub("\\unun%s", "__ ")
    text = text:gsub("\\unun([^a-zA-Z])", "__%1")

    -- \mname{X} -> __X__ (preprocessor macro names)
    text = convert_mname(text)

    -- \xname{X} -> __X (special identifiers with underscore prefix)
    -- NOTE: Using ([^}]*) is acceptable - identifiers are simple without nested braces
    text = text:gsub("\\xname{([^}]*)}", "__%1")

    -- \NTS{text} -> UPPERCASE
    -- NOTE: Using ([^}]*) is acceptable - text content is simple
    text = text:gsub("\\NTS{([^}]*)}", function(s) return s:upper() end)

    -- \ucode{XXXX} -> `U+XXXX`
    -- NOTE: Using ([^}]*) is acceptable - code points are simple hex values
    text = text:gsub("\\ucode{([^}]*)}", "`U+%1`")

    -- \colcol{} -> ::
    text = text:gsub("\\colcol{}", "::")

    -- \ntbs{} and \ntmbs{} - null-terminated string abbreviations
    text = text:gsub("\\ntbs{}", "NTBS")
    text = text:gsub("\\ntmbs{}", "NTMBS")
  end

  -- Tier 10: Math formatting
  if not options.minimal then
    -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
    text = process_macro_with_replacement(text, "mathit", function(content)
      return "*" .. content .. "*"
    end)
    text = process_macro_with_replacement(text, "mathrm", function(content)
      return content
    end)

    -- \bigoh{x} -> 𝑂(x) (only for itemdecl context)
    -- Use process_macro_with_replacement for proper brace-balancing
    if options.convert_to_latex then
      text = process_macro_with_replacement(text, "bigoh", function(content)
        content = content:gsub("\\log", "log")
        content = content:gsub("\\min", "min")
        content = content:gsub("\\max", "max")
        content = content:gsub("\\sqrt", "sqrt")
        return "𝑂(" .. content .. ")"
      end)
    end
  end

  -- Tier 11: Range macros (itemdecl context only)
  -- Use extract_multi_arg_macro for 2-argument macros (fixes ([^}]*) anti-pattern)
  if options.convert_to_latex then
    local range_macros = {
      {name = "range", template = function(a, b) return "[\\texttt{" .. a .. "}, \\texttt{" .. b .. "})" end},
      {name = "crange", template = function(a, b) return "[\\texttt{" .. a .. "}, \\texttt{" .. b .. "}]" end},
      {name = "countedrange", template = function(a, b) return "\\texttt{" .. a .. "}+[0, \\texttt{" .. b .. "})" end},
      {name = "brange", template = function(a, b) return "(\\texttt{" .. a .. "}, \\texttt{" .. b .. "})" end},
      {name = "orange", template = function(a, b) return "(\\texttt{" .. a .. "}, \\texttt{" .. b .. "})" end},
    }

    for _, macro in ipairs(range_macros) do
      local pattern = "\\" .. macro.name .. "{"
      local macro_len = #macro.name + 1  -- +1 for backslash
      while true do
        local start_pos = text:find(pattern, 1, true)
        if not start_pos then break end

        local args, end_pos = extract_multi_arg_macro(text, start_pos, macro_len, 2)
        if not args then break end

        local replacement = macro.template(args[1], args[2])
        text = text:sub(1, start_pos - 1) .. replacement .. text:sub(end_pos)
      end
    end
  end

  -- Tier 12: \impldef handling (itemdecl context)
  if options.convert_to_latex then
    text = process_macro_with_replacement(text, "impldef", function(content)
      return "\\textit{implementation-defined}"
    end)
  end

  -- Tier 13: \phantom{} spacing (itemdecl context)
  if options.convert_to_latex then
    -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
    text = process_macro_with_replacement(text, "phantom", function(content)
      return content
    end)
  end

  -- Tier 14: Cross-references
  if type(options.ref_format) == "function" then
    -- Custom reference formatting function provided
    local function process_refs(refs_str)
      return options.ref_format(refs_str)
    end

    -- Process \ref, \iref, \tref with space handling
    -- Three patterns for each: preceded by non-space (add space),
    -- preceded by space (keep space), at start
    text = text:gsub("([^%s])\\ref{([^}]*)}", function(before, refs)
      return before .. " " .. process_refs(refs)
    end)
    text = text:gsub("(%s)\\ref{([^}]*)}", function(space, refs)
      return space .. process_refs(refs)
    end)
    text = text:gsub("^\\ref{([^}]*)}", function(refs)
      return process_refs(refs)
    end)

    text = text:gsub("([^%s])\\iref{([^}]*)}", function(before, refs)
      return before .. " " .. process_refs(refs)
    end)
    text = text:gsub("(%s)\\iref{([^}]*)}", function(space, refs)
      return space .. process_refs(refs)
    end)
    text = text:gsub("^\\iref{([^}]*)}", function(refs)
      return process_refs(refs)
    end)

    text = text:gsub("([^%s])\\tref{([^}]*)}", function(before, refs)
      return before .. " " .. process_refs(refs)
    end)
    text = text:gsub("(%s)\\tref{([^}]*)}", function(space, refs)
      return space .. process_refs(refs)
    end)
    text = text:gsub("^\\tref{([^}]*)}", function(refs)
      return process_refs(refs)
    end)
  elseif options.ref_format == "placeholder" then
    -- Use @@REF:label@@ placeholders (itemdecl context)
    text = text:gsub("\\ref{([^}]*)}", "@@REF:%1@@")
    text = text:gsub("\\iref{([^}]*)}", "@@REF:%1@@")
    text = text:gsub("\\tref{([^}]*)}", "@@REF:%1@@")
  -- Note: wikilink format is handled by the custom ref_format function path above
  -- No additional processing needed for this format here
  end

  -- Tier 15: Empty braces cleanup (cpp-macros context only)
  if not options.minimal and not options.convert_to_latex then
    -- Strip empty braces {} that appear after C++ version identifiers
    -- BUT preserve = {} (default initializers in function signatures)
    text = text:gsub("(%S){}%s", "%1 ")
    text = text:gsub("(%S){}$", "%1")
  end

  return text
end

-- Export public API
return {
  subscripts = subscripts,
  unescape_latex_chars = unescape_latex_chars,
  convert_special_chars = convert_special_chars,
  extract_braced_content = extract_braced_content,
  trim = trim,
  remove_font_switches = remove_font_switches,
  extract_braced = extract_braced,
  expand_balanced_command = expand_balanced_command,
  replace_code_macro_special_chars = replace_code_macro_special_chars,
  process_code_macro = process_code_macro,
  extract_impdefx_description = extract_impdefx_description,
  expand_impdefx_in_text = expand_impdefx_in_text,
  parse_impdefx_description_to_inlines = parse_impdefx_description_to_inlines,
  expand_cpp_version_macros = expand_cpp_version_macros,
  expand_concept_macros = expand_concept_macros,
  convert_cross_references_in_code = convert_cross_references_in_code,
  expand_library_spec_macros = expand_library_spec_macros,
  extract_multi_arg_macro = extract_multi_arg_macro,
  process_macro_with_replacement = process_macro_with_replacement,
  expand_nested_macros_recursive = expand_nested_macros_recursive,
  remove_macro = remove_macro,
  handle_overlap_commands = handle_overlap_commands,
  convert_math_in_code = convert_math_in_code,
  clean_code_common = clean_code_common,
  code_block_macro_patterns = code_block_macro_patterns,
  split_refs_text = split_refs_text,
  convert_latex_spacing = convert_latex_spacing,
  convert_mname = convert_mname,
  expand_macros_common = expand_macros_common,
  try_unicode_conversion = try_unicode_conversion,
}
