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
  ["s"] = "ₛ",
  ["t"] = "ₜ",
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
      text = text:gsub("\\" .. macro_name .. "{" .. char.pattern .. "}", "`" .. char.replacement .. "`")
    elseif char.type == "macro" then
      -- \tcode{\caret} → `^`
      text = text:gsub("\\" .. macro_name .. "{" .. char.pattern .. "}", "`" .. char.replacement .. "`")
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
    content = convert_special_chars(content)  -- Handles \caret, \textasciitilde, \textbackslash, \unun, \atsign
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

  -- Clean nested macros (simple pattern replacement for non-nested cases)
  description = description:gsub("\\tcode{([^}]*)}", "%1")
  description = description:gsub("\\placeholder{([^}]*)}", "%1")

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

    local description, end_pos = extract_impdefx_description(text, start_pos, prefix_len, suffix_char)

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
      local tcode_content, next_pos = extract_braced_content(description, tcode_start, 6)  -- "\tcode" is 6 chars

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
  if has_at_delimiters then
    text = text:gsub("@\\libconcept{([^}]*)}@", "%1")
    text = text:gsub("@\\exposconcept{([^}]*)}@", "%1")
    text = text:gsub("@\\oldconcept{([^}]*)}@", "Cpp17%1")
  end
  text = text:gsub("\\libconcept{([^}]*)}", "%1")
  text = text:gsub("\\exposconcept{([^}]*)}", "%1")
  text = text:gsub("\\oldconcept{([^}]*)}", "Cpp17%1")
  return text
end

-- Helper function to convert cross-references in code
-- Used by cpp-code-blocks.lua, cpp-notes-examples.lua, cpp-itemdecl.lua
-- Converts \iref{} and \ref{} to [label] format
-- Parameters:
--   text: The text to process
--   has_at_delimiters: Whether to handle @...@ delimited versions (used in code blocks)
local function convert_cross_references_in_code(text, has_at_delimiters)
  if has_at_delimiters then
    text = text:gsub("@\\iref{([^}]*)}@", "[%1]")
    text = text:gsub("@\\ref{([^}]*)}@", "[%1]")
  end
  text = text:gsub("\\iref{([^}]*)}", "[%1]")
  text = text:gsub("\\ref{([^}]*)}", "[%1]")
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
  -- Use pattern that requires \expos to NOT be followed by 'i' to avoid matching \exposid or \exposidnc
  text = text:gsub("\\expos([^i])", "exposition only%1")
  text = text:gsub("\\expos$", "exposition only")

  -- Process \impdefx{...} with nested braces (fallback for any missed by cpp-macros.lua)
  text = expand_impdefx_in_text(text, "\\impdefx{", 9, nil)

  -- Process remaining \impdef variants
  -- Use pattern that requires \impdefnc and \impdef to be followed by non-letter to avoid partial matches
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

    local content, next_pos = extract_braced_content(text, pos - 1, 1)  -- pos-1 to include the brace, macro_len=1 for just "{"
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

-- Helper function to convert math patterns in code
-- Used by clean_code_common() for code block cleaning
local function convert_math_in_code(text)
  -- Process @$...$@ patterns (math mode in code blocks)
  -- These contain subscripts, placeholders, and math symbols
  text = text:gsub("@%$(.-)%$@", function(math_content)
    -- Convert \ldots to Unicode ellipsis
    math_content = math_content:gsub("\\ldots", "…")

    -- Convert subscripts: \tcode{\placeholder{X}}_{n} → Xₙ
    -- Or: \tcode{\placeholder{X}_{n}} → Xₙ
    math_content = math_content:gsub("\\tcode{\\placeholder{([^}]*)}}_{{?([%w]+)}?}", function(name, sub)
      if subscripts[sub] then
        return name .. subscripts[sub]
      else
        return name .. "_" .. sub
      end
    end)

    -- Convert subscripts in simpler form: \tcode{\placeholder{X}}_{n} without nested braces
    math_content = math_content:gsub("\\tcode{([^}]*)}_{{?([%w]+)}?}", function(name, sub)
      -- Remove \placeholder{} wrapper if present
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
    math_content = math_content:gsub("\\tcode{([^}]*)}", "%1")
    math_content = math_content:gsub("\\placeholder{([^}]*)}", "%1")

    return math_content
  end)

  -- Also process plain $...$ patterns (inline math in code comments without @ delimiters)
  -- Only convert if they contain LaTeX commands like \mathtt, \mathrm, \rightarrow
  text = text:gsub("%$([^$]+)%$", function(math_content)
    -- Only process if it contains LaTeX commands
    if math_content:match("\\math") or math_content:match("\\rightarrow") or
       math_content:match("\\leftarrow") or math_content:match("\\ldots") then

      -- Convert \mathtt{...} to plain text
      math_content = math_content:gsub("\\mathtt{([^}]*)}", "%1")
      math_content = math_content:gsub("\\mathrm{([^}]*)}", "%1")
      math_content = math_content:gsub("\\mathit{([^}]*)}", "%1")

      -- Convert arrows to Unicode
      math_content = math_content:gsub("\\rightarrow", "→")
      math_content = math_content:gsub("\\leftarrow", "←")
      math_content = math_content:gsub("\\Rightarrow", "⇒")
      math_content = math_content:gsub("\\Leftarrow", "⇐")

      -- Convert \ldots to Unicode ellipsis
      math_content = math_content:gsub("\\ldots", "…")

      return math_content
    else
      -- Not LaTeX math, return unchanged with $ delimiters
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

  -- Special case for cpp-notes-examples.lua: preserve newlines after \textbackslash in @\tcode{}@ blocks
  -- This must be handled BEFORE the general macro expansion
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

  -- Remove LaTeX spacing commands that should not appear in code
  code = code:gsub("\\;", "")  -- \; is a medium space in LaTeX
  code = code:gsub("\\:", "")  -- \: is a medium space in LaTeX
  code = code:gsub("\\,", "")  -- \, is a thin space in LaTeX
  code = code:gsub("\\!", "")  -- \! is a negative thin space in LaTeX

  -- Cross-references - convert to [label]
  code = convert_cross_references_in_code(code, true)

  -- \defn{x} definition terms
  code = code:gsub("@\\defn{([^}]*)}@", "%1")
  code = code:gsub("\\defn{([^}]*)}", "%1")

  -- \defexposconcept{x} exposition-only concept definition
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
  code = code:gsub("@\\defnlibxname{([^}]*)}@", "__%1")
  code = code:gsub("\\defnlibxname{([^}]*)}", "__%1")

  -- \xname{X} represents __X (special identifiers with underscore prefix)
  code = code:gsub("@\\xname{([^}]*)}@", "__%1")
  code = code:gsub("\\xname{([^}]*)}", "__%1")

  -- \mname{X} represents __X__ (preprocessor macro names with underscore wrapper)
  code = code:gsub("@\\mname{([^}]*)}@", "__%1__")
  code = code:gsub("\\mname{([^}]*)}", "__%1__")

  -- \libheader{X} represents <X> in code blocks (without backticks, plain angle brackets)
  code = code:gsub("@\\libheader{([^}]*)}@", "<%1>")
  code = code:gsub("\\libheader{([^}]*)}", "<%1>")

  -- \ucode{XXXX} represents Unicode code point U+XXXX (process before \textrm to handle nesting)
  code = code:gsub("@\\ucode{([^}]*)}@", "U+%1")
  code = code:gsub("\\ucode{([^}]*)}", "U+%1")

  -- \colcol{} represents ::
  code = code:gsub("\\colcol{}", "::")

  -- Strip \brk{} line break hints
  code = code:gsub("\\brk{}", "")

  -- Math formatting in code comments
  code = code:gsub("\\mathit{([^}]*)}", "%1")
  code = code:gsub("\\mathrm{([^}]*)}", "%1")

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
  code = code:gsub("\\ref{([^}]*)}", "[%1]")

  -- \tref{x} table cross-references (also use [label] format)
  code = code:gsub("\\tref{([^}]*)}", "[%1]")

  -- \range{first}{last} macro for half-open ranges
  code = code:gsub("\\range{([^}]*)}{([^}]*)}", "[%1, %2)")

  -- Strip indexing commands (these should not appear in code blocks but handle defensively)
  code = code:gsub("\\indexlibrary[^{]*{[^}]*}", "")
  code = code:gsub("\\indexlibraryglobal{[^}]*}", "")

  -- \impldef{description} -> "implementation-defined" (used in @\UNSP{\impldef{}}@)
  -- Handle this before \UNSP{} so nested macros get expanded
  code = code:gsub("\\impldef{([^}]*)}", "implementation-defined")

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
}
