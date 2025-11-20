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
cpp-macros.lua

Pandoc Lua filter to expand C++ standard custom macros.

The C++ standard uses many custom macros that Pandoc doesn't recognize,
resulting in empty content. This filter expands common macros to their
intended text representation.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local subscripts = common.subscripts
local unescape_latex_chars = common.unescape_latex_chars
local convert_special_chars = common.convert_special_chars
local extract_braced_content = common.extract_braced_content
local trim = common.trim
local extract_impdefx_description = common.extract_impdefx_description
local expand_impdefx_in_text = common.expand_impdefx_in_text
local try_unicode_conversion = common.try_unicode_conversion
local parse_content_with_tcode = common.parse_content_with_tcode
local parse_impdefx_description_to_inlines = common.parse_impdefx_description_to_inlines
local extract_multi_arg_macro = common.extract_multi_arg_macro
local process_macro_with_replacement = common.process_macro_with_replacement
local remove_macro = common.remove_macro
local split_refs_text = common.split_refs_text
local convert_latex_spacing = common.convert_latex_spacing
local convert_mname = common.convert_mname
local expand_macros_common = common.expand_macros_common

-- Table to collect all references for link definitions
-- Made global so cpp-tables.lua can also track references
references = {}

-- Metadata for cross-file reference support
local current_file = nil
local label_index = {}

-- Library chapter references (defaults for C++23/N4950)
-- Can be overridden by reading config.tex if source_dir metadata is provided
local FIRSTLIB = "support"
local LASTLIB = "thread"

-- Macro length constants (prevents off-by-one errors, improves maintainability)
local MACRO_LEN = {
  term = 5,           -- \term
  mbox = 5,           -- \mbox
  defn = 5,           -- \defn
  tcode = 6,          -- \tcode
  range = 6,          -- \range
  defnx = 6,          -- \defnx
  bigoh = 6,          -- \bigoh
  doccite = 8,        -- \doccite
  unicode = 8,        -- \unicode
  impdefx = 9,        -- \impdefx
  Fundescx = 9,       -- \Fundescx
  grammarterm = 12,   -- \grammarterm
  description = 19,   -- \begin{description}
}

-- Common pattern constants (DRY principle, improves maintainability)
local PATTERN = {
  inline_math = "%$([^$]+)%$",
  subscript_braced = "([%w]+)_{([%w]+)}",
  subscript_simple = "([%w]+)_([%w])",
  simple_macro = "\\([^}]*){}",
  braced_macro = "\\([^{]*)%{([^}]*)%}",
}

-- Helper function to convert inline math in code (subscripts and operators)
-- Converts $X_i$ to Xᵢ (Unicode subscript)
-- Converts $A \land B$ to A ∧ B (logical operators) - Issue #52
-- Delegates to try_unicode_conversion from cpp-common for unified behavior
local function convert_math_in_code(text)
  -- Process $...$  patterns (inline math in code)
  text = text:gsub(PATTERN.inline_math, function(math_content)
    -- Unescape double backslashes from Pandoc's LaTeX parsing
    -- Pandoc escapes inner \tcode to \\tcode when parsing nested macros
    -- Pattern: $\\tcode{T}_i$ → $\tcode{T}_i$
    math_content = math_content:gsub("\\\\", "\\")

    -- Strip nested \tcode{} since we're already in code context from outer \tcode{}
    -- Inner \tcode{T} → T (no backticks needed, outer \tcode{} provides them)
    -- This prevents nested backticks like `` `T` `` and allows subscripts to convert
    -- Pattern: \tcode{decay_t<$\tcode{T}_i$>} → decay_t<Tᵢ> (wrapped by outer backticks)
    math_content = process_macro_with_replacement(math_content, "tcode", function(content)
      return content  -- Just strip wrapper, don't add backticks
    end)

    -- Now convert math to Unicode (subscripts, operators, etc.)
    local converted = try_unicode_conversion(math_content)
    return converted or math_content  -- Fallback to original if conversion fails
  end)
  return text
end

-- Load label index from Lua table file
local function load_label_index(file_path)
  if not file_path then
    return {}
  end

  local chunk, err = loadfile(file_path)
  if not chunk then
    io.stderr:write("Warning: Could not load label index from " .. file_path ..
                    ": " .. tostring(err) .. "\n")
    return {}
  end

  local success, result = pcall(chunk)
  if not success then
    io.stderr:write("Warning: Error executing label index file: " .. tostring(result) .. "\n")
    return {}
  end

  return result or {}
end

-- Generate link target for a reference
-- Returns "#ref" for same-file references, "file.md#ref" for cross-file references
local function generate_link_target(ref)
  -- Check if we have label index information
  if not current_file or not label_index or not label_index[ref] then
    -- No index info - use default same-file link
    return "#" .. ref
  end

  local target_file = label_index[ref]

  -- Check if reference is in the same file
  if target_file == current_file then
    -- Same file - use simple anchor
    return "#" .. ref
  else
    -- Different file - use relative link
    return target_file .. ".md#" .. ref
  end
end

-- Helper function to expand macros in text using shared implementation
-- Wrapper around expand_macros_common with cpp-macros context
local function expand_macros(text, skip_special_chars)
  if not text then return text end

  -- Use shared function from cpp-common to split comma-separated references
  -- E.g., "a,b,c" -> "[[a]], [[b]], [[c]]"
  local function split_refs(refs_str)
    return split_refs_text(refs_str, references)
  end

  -- Set global FIRSTLIB and LASTLIB for expand_macros_common to use
  _G.FIRSTLIB = FIRSTLIB
  _G.LASTLIB = LASTLIB

  -- Call consolidated function with cpp-macros context options
  return expand_macros_common(text, {
    skip_special_chars = skip_special_chars,
    ref_format = split_refs,  -- Custom function that tracks references
  })
end

-- Apply to all string elements
function Str(elem)
  elem.text = expand_macros(elem.text)

  -- Strip TeX dimension remnants that appear after \kern removal (Issue #58)
  -- Pattern: -1.2pta → a, 1ptd → d, 0.6ptti → ti
  -- These appear when \kern precedes text and Pandoc parses dimensions as part of next word
  elem.text = elem.text:gsub("^%-?%d+%.?%d*pt", "")   -- pt units (points)
  elem.text = elem.text:gsub("^%-?%d+%.?%d*em", "")   -- em units
  elem.text = elem.text:gsub("^%-?%d+%.?%d*ex", "")   -- ex units (x-height)

  return elem
end

-- Apply to raw inline LaTeX and markdown
function RawInline(elem)
  -- Handle markdown RawInline elements from other filters (like cpp-itemdecl.lua)
  -- Extract [[label]] patterns to track them in the references table
  if elem.format == "markdown" and elem.text then
    for label in elem.text:gmatch("%[%[([^%]]+)%]%]") do
      references[label] = true
    end
    return elem  -- Return unchanged, just tracking
  end

  -- Handle LaTeX RawInline elements
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Strip index generation commands - these are PDF-only and should never appear in output
  if text:match("^\\indextext{") or text:match("^\\index{") or text:match("^\\indexlibrary{") then
    return {}  -- Return empty list to remove element
  end

  -- Strip TeX box/spacing primitives - PDF typesetting artifacts (Issue #58)
  -- These commands have no semantic meaning in Markdown output

  -- \kern<dimension> - horizontal spacing (dimensions will be stripped from next Str element)
  if text:match("^\\kern$") then
    return {}  -- Remove element entirely
  end

  -- \hspace{<dimension>} - explicit horizontal space
  if text:match("^\\hspace{.*}$") then
    return {}  -- Remove element entirely
  end

  -- \vspace{<dimension>} - vertical spacing
  if text:match("^\\vspace{.*}$") then
    return {}  -- Remove element entirely
  end

  -- \raise<dimension> - vertical positioning (will be followed by \hbox{})
  if text:match("^\\raise$") then
    return {}  -- Remove element entirely
  end

  -- \hbox{<content>} - extract content, discard box wrapper
  local hbox_content = text:match("^\\hbox{(.*)}$")
  if hbox_content then
    return pandoc.Str(hbox_content)
  end


  -- \impdefx{description} - handle BEFORE \tcode to extract description with nested macros
  if text:match("^\\impdefx{") then
    local description, _ = extract_impdefx_description(text, 1, MACRO_LEN.impdefx, nil)  -- "\impdefx{" is 9 chars
    if description then
      return parse_impdefx_description_to_inlines(description)
    end
  end

  -- \term{} - use brace-balanced extraction to handle nested \tcode{}
  -- Handle BEFORE \tcode to avoid greedy matching issues
  if text:match("^\\term{") then
    local content, _ = extract_braced_content(text, 1, MACRO_LEN.term)  -- \term is 5 chars
    if content then
      -- Parse content with nested \tcode{} support
      -- Custom tcode processor: unescape + convert math + convert spacing
      local inlines = parse_content_with_tcode(content, {
        tcode_processor = function(code)
          code = unescape_latex_chars(code)
          code = convert_math_in_code(code)
          return convert_latex_spacing(code)
        end
      })
      return pandoc.Emph(inlines)
    end
  end

  -- \bigoh{} - Big-O complexity notation (Issue #38)
  -- Converts \bigoh{x} → 𝑂(x) with support for nested \tcode{} and math commands
  -- Handle BEFORE \tcode to process nested macros properly
  if text:match("^\\bigoh{") then
    local content, _ = extract_braced_content(text, 1, MACRO_LEN.bigoh)  -- \bigoh is 6 chars
    if content then
      -- Convert LaTeX math commands to text equivalents (same as cpp-common.lua)
      content = content:gsub("\\log", "log")
      content = content:gsub("\\min", "min")
      content = content:gsub("\\max", "max")
      content = content:gsub("\\sqrt", "sqrt")

      -- Parse content with nested \tcode{} support
      -- Custom tcode processor: unescape + convert math + convert spacing
      local inlines = parse_content_with_tcode(content, {
        tcode_processor = function(code)
          code = unescape_latex_chars(code)
          code = convert_math_in_code(code)
          return convert_latex_spacing(code)
        end
      })

      -- Return as: 𝑂(content) using Mathematical Italic O (matches cpp-common.lua)
      local result = {pandoc.Str("𝑂(")}
      for _, inline in ipairs(inlines) do
        table.insert(result, inline)
      end
      table.insert(result, pandoc.Str(")"))
      return result
    end
  end

  -- \mbox{...} - process nested macros within the box
  local mbox_start = text:find("\\mbox{", 1, true)
  if mbox_start and mbox_start == 1 then
    local content, _ = extract_braced_content(text, mbox_start, MACRO_LEN.mbox)  -- \mbox is 5 chars
    if content then
      -- Parse content into inline elements, processing nested macros
      local inlines = {}
      local pos = 1

      while pos <= #content do
        -- Look for known macros in order
        local next_macro_pos = nil
        local next_macro_name = nil

        -- Check for each macro type
        for _, macro_info in ipairs({
          {"\\placeholder{", 12, "placeholder"},     -- \placeholder = 12 chars
          {"\\placeholdernc{", 14, "placeholdernc"}, -- \placeholdernc = 14 chars
          {"\\tcode{", 6, "tcode"},                   -- \tcode = 6 chars
          {"\\grammarterm{", 12, "grammarterm"},     -- \grammarterm = 12 chars
          -- \keyword{} now handled in simplified_macros.tex (Issue #63)
          {"\\term{", 5, "term"},                     -- \term = 5 chars
        }) do
          local macro_pattern = macro_info[1]
          local macro_len = macro_info[2]
          local macro_type = macro_info[3]

          local found_pos = content:find(macro_pattern, pos, true)
          if found_pos and (not next_macro_pos or found_pos < next_macro_pos) then
            next_macro_pos = found_pos
            next_macro_name = {macro_pattern, macro_len, macro_type}
          end
        end

        if next_macro_pos then
          -- Add text before macro
          if next_macro_pos > pos then
            local text_before = content:sub(pos, next_macro_pos - 1)
            text_before = expand_macros(text_before)
            text_before = unescape_latex_chars(text_before)
            if #text_before > 0 then
              table.insert(inlines, pandoc.Str(text_before))
            end
          end

          -- Extract macro content
          local macro_content, macro_next_pos =
            extract_braced_content(content, next_macro_pos, next_macro_name[2])
          if macro_content then
            macro_content = unescape_latex_chars(macro_content)

            -- Process based on macro type
            if next_macro_name[3] == "tcode" or next_macro_name[3] == "keyword" then
              table.insert(inlines, pandoc.Code(macro_content))
            elseif next_macro_name[3] == "grammarterm" then
              table.insert(inlines, pandoc.Emph({pandoc.Str(macro_content)}))
            elseif next_macro_name[3] == "placeholder" or next_macro_name[3] == "placeholdernc" then
              table.insert(inlines, pandoc.Emph({pandoc.Str(macro_content)}))
            elseif next_macro_name[3] == "term" then
              table.insert(inlines, pandoc.Emph({pandoc.Str(macro_content)}))
            end
            pos = macro_next_pos
          else
            -- Malformed macro, skip it
            pos = next_macro_pos + next_macro_name[2]
          end
        else
          -- No more macros, add remaining text
          local remaining = content:sub(pos)
          remaining = expand_macros(remaining)
          remaining = unescape_latex_chars(remaining)
          if #remaining > 0 then
            table.insert(inlines, pandoc.Str(remaining))
          end
          break
        end
      end

      return inlines
    end
  end

  -- Inline code macros - return Code elements
  -- Need to expand nested macros first
  local code

  -- Use brace-balanced extraction instead of greedy matching for \tcode{}
  local tcode_start = text:find("\\tcode{", 1, true)
  local end_pos
  if tcode_start and tcode_start == 1 then  -- Must be at start
    code, end_pos = extract_braced_content(text, tcode_start, MACRO_LEN.tcode)  -- \tcode is 6 chars
  end
  if code then
    -- Strip \brk{} line break hints and \- discretionary hyphens first
    code = code:gsub("\\brk{}", "")
    code = code:gsub("\\%-", "")
    -- Handle LaTeX spacing braces: { } (with space) should become regular space
    -- Do this BEFORE unescaping so we don't affect C++ code
    code = code:gsub("{ }", " ")
    -- Unescape LaTeX escaped characters (\{ → {, \} → }, etc.)
    code = unescape_latex_chars(code)
    -- Convert inline math (subscripts and operators) to Unicode (BEFORE other processing)
    code = convert_math_in_code(code)
    -- Convert LaTeX spacing commands to regular spaces
    code = convert_latex_spacing(code)
    -- Handle escaped special characters
    code = code:gsub("\\([~!@#$%%^&*])", "%1")
    -- Clean up ~{} from LaTeX \~{} (tilde with spacing braces)
    code = code:gsub("~{}", "~")
    -- Expand nested macros in code content
    -- Strip \texttt{} from \keyword{} preprocessing
    code = code:gsub("\\texttt{([^}]*)}", "%1")
    code = code:gsub("\\ctype{([^}]*)}", "%1")
    code = code:gsub("\\term{([^}]*)}", "%1")
    code = code:gsub("\\grammarterm{([^}]*)}", "%1")
    code = code:gsub("\\libconcept{([^}]*)}", "%1")
    code = code:gsub("\\exposconcept{([^}]*)}", "%1")
    code = code:gsub("\\placeholder{([^}]*)}", "%1")
    code = code:gsub("\\placeholdernc{([^}]*)}", "%1")
    -- Library indexing macros (issue #46)
    code = code:gsub("\\libmember{([^}]*)}{([^}]*)}", "%1")  -- Extract member name, discard class
    code = code:gsub("\\libglobal{([^}]*)}", "%1")  -- Extract global name (issue #24)
    code = code:gsub("\\exposid{([^}]*)}", "%1")
    code = code:gsub("\\mathit{([^}]*)}", "%1")
    -- Different meaning in math mode
    code = code:gsub("\\mathrm{([^}]*)}", "%1")
    -- Strip \textit{} from simplified_macros.tex preprocessing
    code = code:gsub("\\textit{([^}]*)}", "%1")
    code = code:gsub("\\colcol{}", "::")  -- Context-dependent
    -- Convert cv{} to cv (cv-qualifiers: const/volatile)
    -- simplified_macros.tex expands \cv to cv, leaving cv{} in output
    code = code:gsub("cv%{%}", "cv")
    -- Handle special characters
    code = convert_special_chars(code)
    -- Handle \mname macros
    code = convert_mname(code)

    -- Check if there's a suffix like {s} after the \tcode{} for plurals
    -- Pattern: \tcode{...}{s} should become `code`s
    if end_pos and end_pos <= #text and text:sub(end_pos, end_pos) == "{" then
      local suffix, pos_after_suffix = extract_braced_content(text, end_pos, 0)
      if suffix and pos_after_suffix and pos_after_suffix - 1 == #text then
        -- Suffix must end the string - return Code + Str
        return {pandoc.Code(code), pandoc.Str(suffix)}
      end
    end

    return pandoc.Code(code)
  end

  -- NOTE: \keyword{} now handled in simplified_macros.tex (Issue #63)

  code = text:match("\\ctype{([^}]*)}")
  if code then return pandoc.Code(code) end

  -- Library header macros - return Code with angle brackets
  code = text:match("\\libheader{([^}]*)}")
  if code then return pandoc.Code("<" .. code .. ">") end

  code = text:match("\\libheaderdef{([^}]*)}")
  if code then return pandoc.Code("<" .. code .. ">") end

  code = text:match("\\libheaderref{([^}]*)}")
  if code then return pandoc.Code("<" .. code .. ">") end

  -- \libheaderrefx{header}{section} - extract just the header name
  code = text:match("\\libheaderrefx{([^}]*)}{[^}]*}")
  if code then return pandoc.Code("<" .. code .. ">") end

  -- Library concept - return Code element
  code = text:match("\\libconcept{([^}]*)}")
  if code then return pandoc.Code(code) end

  -- \libglobal{x} - library global function/type - return Code element
  code = text:match("\\libglobal{([^}]*)}")
  if code then return pandoc.Code(code) end

  -- Exposition-only concept - return Code element
  code = text:match("\\exposconcept{([^}]*)}")
  if code then return pandoc.Code(code) end

  -- \ucode{XXXX} - Unicode code point - return Code element
  code = text:match("\\ucode{([^}]*)}")
  if code then return pandoc.Code("U+" .. code) end

  -- Document citations - use brace-balanced parsing to handle nested macros like \Cpp{}
  local doccite_start = text:find("\\doccite{", 1, true)
  if doccite_start then
    local content, _ = extract_braced_content(text, doccite_start, MACRO_LEN.doccite)  -- \doccite is 8 chars
    if content then
      -- Expand macros in content before wrapping in emphasis
      content = expand_macros(content)
      return pandoc.Emph({pandoc.Str(content)})
    end
  end

  -- Function description cross-reference - use brace-balanced parsing
  local fundescx_start = text:find("\\Fundescx{", 1, true)
  if fundescx_start then
    local content, _ = extract_braced_content(text, fundescx_start, MACRO_LEN.Fundescx)  -- \Fundescx is 9 chars
    if content then
      -- Expand macros in content before wrapping in emphasis
      content = expand_macros(content)
      return pandoc.Emph({pandoc.Str(content)})
    end
  end


  -- Emphasis macros - return Emph elements

  -- \grammarterm{term}{suffix} - with optional suffix (e.g., {s} for plurals)
  -- Returns Emph + Str if suffix present, otherwise just Emph
  -- Special case: \grammarterm{}{word} has empty first arg (LaTeX source bug in n3337/n4140)
  local grammarterm_start = text:find("\\grammarterm{", 1, true)
  if grammarterm_start and grammarterm_start == 1 then  -- Must be at start
    -- \grammarterm is 12 chars
    local term, pos_after_term = extract_braced_content(text, grammarterm_start, 12)
    if term then
      -- Check if there's a second argument (suffix or actual term if first is empty)
      if pos_after_term and pos_after_term <= #text and
         text:sub(pos_after_term, pos_after_term) == "{" then
        local suffix, pos_after_suffix = extract_braced_content(text, pos_after_term, 0)

        -- Handle empty first argument (LaTeX source bug in n3337/n4140)
        if term == "" and suffix then
          -- Pattern: \grammarterm{}{statement} -> term="", suffix="statement"
          -- Should render as: *statement* (use suffix as term)
          if pos_after_suffix - 1 == #text then
            return pandoc.Emph({pandoc.Str(suffix)})
          end

          -- Pattern: \grammarterm{}{statement}{s} -> should render as: *statement*s
          -- Check for third argument (plural suffix)
          if pos_after_suffix and pos_after_suffix <= #text and
             text:sub(pos_after_suffix, pos_after_suffix) == "{" then
            local plural, pos_after_plural = extract_braced_content(text, pos_after_suffix, 0)
            if plural and pos_after_plural - 1 == #text then
              -- Render suffix (actual term) in italics, plural outside (for consistency)
              return {pandoc.Emph({pandoc.Str(suffix)}), pandoc.Str(plural)}
            end
          end
        end

        -- Normal case: \grammarterm{term}{suffix}
        -- Suffix must end the string
        if suffix and pos_after_suffix and pos_after_suffix - 1 == #text then
          -- Return list of Inlines: Emph + Str for the suffix
          -- Pandoc will splice these into the document
          return {pandoc.Emph({pandoc.Str(term)}), pandoc.Str(suffix)}
        end
      end
      -- No suffix or not at end - check if it ends here
      if pos_after_term and pos_after_term - 1 == #text then
        return pandoc.Emph({pandoc.Str(term)})
      end
    end
  end

  emph = text:match("\\exposid{([^}]*)}")
  if emph then return pandoc.Emph({pandoc.Str(emph)}) end

  emph = text:match("\\exposidnc{([^}]*)}")
  if emph then return pandoc.Emph({pandoc.Str(emph)}) end

  emph = text:match("\\placeholder{([^}]*)}")
  if emph then return pandoc.Emph({pandoc.Str(emph)}) end

  emph = text:match("\\placeholdernc{([^}]*)}")
  if emph then return pandoc.Emph({pandoc.Str(emph)}) end

  -- \defn{x} - use brace-balanced parsing to handle nested macros like \Cpp{}
  local defn_start = text:find("\\defn{", 1, true)
  if defn_start then
    local content, _ = extract_braced_content(text, defn_start, MACRO_LEN.defn)  -- \defn is 5 chars
    if content then
      -- Expand macros in content before wrapping in emphasis
      content = expand_macros(content)
      return pandoc.Emph({pandoc.Str(content)})
    end
  end

  -- \defexposconcept{x} - use brace-balanced parsing
  local defexpos_start = text:find("\\defexposconcept{", 1, true)
  if defexpos_start then
    local content, _ = extract_braced_content(text, defexpos_start, 16)
    if content then
      -- Expand macros in content before wrapping in emphasis
      content = expand_macros(content)
      return pandoc.Emph({pandoc.Str(content)})
    end
  end

  -- \defnx{plural}{singular} - use plural form with brace-balanced parsing
  local defnx_start = text:find("\\defnx{", 1, true)
  if defnx_start then
    local plural, next_pos = extract_braced_content(text, defnx_start, 6)
    if plural then
      -- Parse plural content with nested \tcode{} support
      -- Custom text processor: expand macros (like \Cpp{}) then unescape
      local inlines = parse_content_with_tcode(plural, {
        text_processor = function(t) return unescape_latex_chars(expand_macros(t)) end
      })
      return pandoc.Emph(inlines)
    end
  end

  -- \defnadj{adjective}{noun} - use brace-balanced parsing
  local defnadj_start = text:find("\\defnadj{", 1, true)
  if defnadj_start then
    local adj, next_pos = extract_braced_content(text, defnadj_start, 8)
    if adj and next_pos then
      -- next_pos is after the first }, so we're at the { of the second argument
      local noun, _ = extract_braced_content(text, next_pos, 0)
      if noun then
        -- Expand macros in both parts before concatenating
        adj = expand_macros(adj)
        noun = expand_macros(noun)
        return pandoc.Emph({pandoc.Str(adj .. " " .. noun)})
      end
    end
  end

  -- \defnxname{x} - define identifier with __ prefix (italic)
  local defnxname = text:match("\\defnxname{([^}]*)}")
  if defnxname then
    return pandoc.Emph({pandoc.Str("__" .. defnxname)})
  end

  -- \defnlibxname{x} - define library identifier with __ prefix (italic)
  local defnlibxname = text:match("\\defnlibxname{([^}]*)}")
  if defnlibxname then
    return pandoc.Emph({pandoc.Str("__" .. defnlibxname)})
  end

  -- Helper function to split comma-separated refs and build inline elements
  -- E.g., "a,b,c" -> Space, "[a], [b], [c]"
  local function split_refs_inline(refs_str)
    local parts = {}
    for ref in refs_str:gmatch("([^,]+)") do
      ref = trim(ref)  -- trim whitespace
      -- Expand macros in reference (e.g., \firstlibchapter -> support)
      ref = expand_macros(ref)
      references[ref] = true
      if #parts > 0 then
        table.insert(parts, pandoc.Str(", "))
      end
      table.insert(parts, pandoc.RawInline('markdown', '[[' .. ref .. ']]'))
    end
    -- Add leading space before the first reference
    table.insert(parts, 1, pandoc.Space())
    return parts
  end

  -- Cross-reference macros - return as reference-style link [ref]
  -- These will need link definitions added at end of document
  -- Return with leading space for readability
  -- Handles comma-separated refs: \ref{a,b,c} -> [a], [b], [c]
  local refs = text:match("\\ref{([^}]*)}")
  if refs then
    return split_refs_inline(refs)
  end

  -- \iref is "inline ref" - also use [ref] format
  -- Track this reference for link definitions
  -- Return with leading space for readability
  -- Handles comma-separated refs: \iref{a,b,c} -> [a], [b], [c]
  refs = text:match("\\iref{([^}]*)}")
  if refs then
    return split_refs_inline(refs)
  end

  -- \tref is "table ref" - also use [ref] format
  -- Track this reference for link definitions
  -- Return with leading space for readability
  -- Handles comma-separated refs: \tref{a,b,c} -> [a], [b], [c]
  refs = text:match("\\tref{([^}]*)}")
  if refs then
    return split_refs_inline(refs)
  end

  -- Strip \brk{} line break hints - not needed in markdown
  if text:match("^\\brk{}$") then
    return {}  -- Return empty list to remove element
  end

  -- \xname{X} - special identifier with underscore prefix
  local xname = text:match("\\xname{([^}]*)}")
  if xname then
    return pandoc.Code("__" .. xname)
  end

  -- \mname{X} - preprocessor macro name with underscore wrapper
  local mname = text:match("\\mname{([^}]*)}")
  if mname then
    return pandoc.Code("__" .. mname .. "__")
  end

  -- \range{first}{last} - half-open range [first, last)
  -- Use brace-balanced extraction to handle nested braces
  local range_start = text:find("\\range{", 1, true)
  if range_start and range_start == 1 then
    -- \range is 6 chars, 2 args
    local args, range_end_pos = extract_multi_arg_macro(text, range_start, 6, 2)
    if args and range_end_pos and range_end_pos - 1 == #text then
      local first = expand_macros(args[1])
      local last = expand_macros(args[2])
      return pandoc.RawInline('markdown', '[`' .. first .. '`, `' .. last .. '`)')
    end
  end

  -- \unicode{code}{description} - Unicode character with description
  -- This needs special handling because Pandoc recognizes \unicode as a known LaTeX command
  local unicode_match = text:match("^\\unicode{")
  if unicode_match then
    -- Extract both brace-balanced arguments
    local args, _ = extract_multi_arg_macro(text, 1, MACRO_LEN.unicode, 2)  -- \unicode, 2 args
    if args then
      return pandoc.Str("U+" .. args[1] .. " (" .. args[2] .. ")")
    end
  end

  -- Plain text macros - expand and return as Str
  local expanded = expand_macros(text)
  if expanded ~= text then
    return pandoc.Str(expanded)
  end

  return elem
end

-- Apply to code elements (for inline code)
function Code(elem)
  -- Don't expand macros inside inline code, but handle special cases
  -- like discretionary hyphens that shouldn't appear in code
  elem.text = elem.text:gsub("\\%-", "")

  -- Strip \textit{} from simplified_macros.tex preprocessing
  elem.text = elem.text:gsub("\\textit{([^}]*)}", "%1")

  -- LaTeX spacing commands should be converted to regular spaces
  elem.text = convert_latex_spacing(elem.text)

  return elem
end

-- Apply to code blocks to clean up LaTeX artifacts
function CodeBlock(elem)
  -- Expand macros that might appear in code blocks
  local text = elem.text

  -- Special characters that appear in code
  text = convert_special_chars(text)

  -- Escaped braces in code
  text = text:gsub("\\{", "{")
  text = text:gsub("\\%}", "}")

  -- Remove font switch commands (bare commands without arguments)
  text = text:gsub("\\normalfont%s*", "")
  text = text:gsub("\\itshape%s*", "")
  text = text:gsub("\\rmfamily%s*", "")
  text = text:gsub("\\bfseries%s*", "")

  -- Handle layout overlap commands: \rlap{}, \llap{}, \clap{}
  -- These create overlapping text in LaTeX - just extract the content
  text = text:gsub("\\rlap{([^}]+)}", "%1")
  text = text:gsub("\\llap{([^}]+)}", "%1")
  text = text:gsub("\\clap{([^}]+)}", "%1")

  -- \uname{X} → X (Unicode character names - strip formatting)


  -- \unicode{XXXX}{description} → U+XXXX (description)
  -- This macro takes two brace-balanced arguments
  while true do
    local start_pos = text:find("\\unicode{", 1, true)
    if not start_pos then break end

    -- \unicode is 8 chars, 2 args
    local args, end_pos = extract_multi_arg_macro(text, start_pos, 8, 2)
    if not args then break end

    -- Replace \unicode{XXXX}{desc} with U+XXXX (desc)
    text = text:sub(1, start_pos - 1) .. "U+" .. args[1] .. " (" .. args[2] ..
           ")" .. text:sub(end_pos)
  end

  -- Handle \mname{} macros
  text = convert_mname(text)

  -- Strip discretionary hyphen \- used for line breaking
  text = text:gsub("\\%-", "")

  -- Remove \obeyspaces commands and LaTeX artifacts that shouldn't appear in output
  text = text:gsub("\\obeyspaces\n", "")
  text = text:gsub("\\obeyspaces", "")
  -- Remove LaTeX brace/comment markers that leak into BNF blocks
  text = text:gsub("}%%\n", "")
  text = text:gsub("}%%", "")

  elem.text = text
  return elem
end

-- Helper function to remove a LaTeX command with balanced braces (discard content)
local function remove_latex_command(text, command)
  return remove_macro(text, command, false)  -- false = discard content
end

-- Apply to raw blocks as well
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Handle simple \tcode{} blocks (common in bullet list items)
  -- When a bullet item contains only \tcode{...}, Pandoc creates a RawBlock
  if text:match("^\\tcode{.*}$") then
    local code = text:match("^\\tcode{(.*)}$")
    if code then
      -- Unescape LaTeX escaped characters first
      code = unescape_latex_chars(code)
      -- Convert inline math (subscripts and operators) to Unicode
      code = convert_math_in_code(code)
      -- Convert cv{} to cv (cv-qualifiers: const/volatile)
      -- simplified_macros.tex expands \cv to cv, leaving cv{} in output
      code = code:gsub("cv%{%}", "cv")
      -- Handle escaped special characters
      code = code:gsub("\\#", "#")
      code = code:gsub("\\&", "&")
      code = code:gsub("\\textbackslash{}", "\\")
      code = code:gsub("\\textbackslash%s", "\\")  -- Match whitespace but don't output it
      code = code:gsub("\\textbackslash", "\\")
      -- Handle angle brackets
      code = code:gsub("<", "<")
      code = code:gsub(">", ">")
      return pandoc.Plain({pandoc.Code(code)})
    end
  end

  -- \defnx{plural}{singular} - renders plural form with nested \tcode{} support
  if text:match("^\\defnx{") then
    local plural, next_pos = extract_braced_content(text, 1, MACRO_LEN.defnx)  -- \defnx is 6 chars
    if plural then
      -- Parse plural content with nested \tcode{} support (uses defaults)
      local inlines = parse_content_with_tcode(plural)
      return pandoc.Para({pandoc.Emph(inlines)})
    end
  end

  -- Handle description lists (used for predefined macros, etc.)
  -- Find balanced begin/end description pairs
  local desc_start = text:find("\\begin{description}")
  if desc_start then
    -- Find the matching \end{description} accounting for nesting
    local pos = desc_start + MACRO_LEN.description
    local depth = 1
    local desc_end = nil

    while pos <= #text and depth > 0 do
      local next_begin = text:find("\\begin{description}", pos, true)
      local next_end = text:find("\\end{description}", pos, true)

      if next_end and (not next_begin or next_end < next_begin) then
        depth = depth - 1
        if depth == 0 then
          desc_end = next_end - 1
        else
          pos = next_end + 17
        end
      elseif next_begin then
        depth = depth + 1
        pos = next_begin + 19
      else
        break
      end
    end

    if desc_end then
      local desc_content = text:sub(desc_start + 19, desc_end)
    -- Parse individual items by splitting on \item or \stage{}
    local blocks = {}
    local items = {}

    -- Helper function to find next \item or \stage that's not inside a nested environment
    local function find_next_item_or_stage(content, start_pos)
      local search_pos = start_pos
      while search_pos <= #content do
        local item_pos = content:find("\\item%s*", search_pos)
        local stage_pos = content:find("\\stage{[^}]*}", search_pos)

        -- Find which comes first
        local candidate_pos, candidate_end, is_stage
        if item_pos and (not stage_pos or item_pos < stage_pos) then
          candidate_pos = item_pos
          candidate_end = content:find("%s*", item_pos + 5) or item_pos + 5
          is_stage = false
        elseif stage_pos then
          candidate_pos = stage_pos
          _, candidate_end = content:find("\\stage{[^}]*}", stage_pos)
          is_stage = true
        else
          return nil, nil, nil -- No more candidates
        end

        -- Check if this candidate is inside an itemize/enumerate environment
        -- by scanning backwards from candidate_pos to start_pos
        local nested_depth = 0
        local check_pos = start_pos
        while check_pos < candidate_pos do
          local begin_item = content:find("\\begin{itemize}", check_pos, true)
          local begin_enum = content:find("\\begin{enumerate}", check_pos, true)
          local end_item = content:find("\\end{itemize}", check_pos, true)
          local end_enum = content:find("\\end{enumerate}", check_pos, true)

          -- Find earliest event
          local next_event = math.huge
          local event_type = nil
          if begin_item and begin_item < candidate_pos and begin_item < next_event then
            next_event = begin_item
            event_type = "begin"
          end
          if begin_enum and begin_enum < candidate_pos and begin_enum < next_event then
            next_event = begin_enum
            event_type = "begin"
          end
          if end_item and end_item < candidate_pos and end_item < next_event then
            next_event = end_item
            event_type = "end"
          end
          if end_enum and end_enum < candidate_pos and end_enum < next_event then
            next_event = end_enum
            event_type = "end"
          end

          if event_type == "begin" then
            nested_depth = nested_depth + 1
            check_pos = next_event + 15
          elseif event_type == "end" then
            nested_depth = nested_depth - 1
            check_pos = next_event + 13
          else
            break
          end
        end

        -- If we're at depth 0, this is a valid item/stage boundary
        if nested_depth == 0 then
          return candidate_pos, candidate_end, is_stage
        end

        -- Otherwise, skip this one and keep searching
        search_pos = candidate_end + 1
      end

      return nil, nil, nil
    end

    -- Split content by \item or \stage{N}
    local item_pos = 1
    while true do
      -- Look for either \item or \stage{...} that's not inside nested environments
      local start_pos, end_pos, is_stage = find_next_item_or_stage(desc_content, item_pos)

      if not start_pos then
        break -- No more items
      end

      -- Get text until next \item/\stage or end
      local next_start, _, _ = find_next_item_or_stage(desc_content, end_pos + 1)

      local item_content
      if is_stage then
        -- For \stage{}, include the \stage{N} as the term followed by \\
        local stage_text = desc_content:sub(start_pos, end_pos)
        local rest_text
        if next_start then
          rest_text = desc_content:sub(end_pos + 1, next_start - 1)
        else
          rest_text = desc_content:sub(end_pos + 1)
        end
        item_content = stage_text .. "\\\\" .. rest_text
      else
        -- For \item, just take content after it
        if next_start then
          item_content = desc_content:sub(end_pos + 1, next_start - 1)
        else
          item_content = desc_content:sub(end_pos + 1)
        end
      end

      if item_content and #item_content > 0 then
        table.insert(items, item_content)
      end

      item_pos = end_pos + 1
      if not next_start then break end
    end

    for _, item_text in ipairs(items) do
      -- Extract term (text before first \\)
      local term, rest = item_text:match("^(.-)\\\\(.*)$")
      if not term then
        -- No \\ found, whole thing is term
        term = item_text
        rest = ""
      end

      -- Strip index commands from term (handle nested braces)
      term = remove_latex_command(term, "indextext")
      term = remove_latex_command(term, "index")
      term = remove_latex_command(term, "idxxname")
      term = term:gsub("%%[^\n]*", "") -- Remove comments

      -- Expand macros in term and clean up
      term = expand_macros(term:gsub("^%s+", ""):gsub("%s+$", ""))

      -- Create bullet with bold term
      -- Use Code for terms containing underscores to avoid GFM escaping
      local term_elem
      if term:match("_") then
        term_elem = pandoc.Code(term)
      else
        term_elem = pandoc.Str(term)
      end
      table.insert(blocks, pandoc.Para({
        pandoc.Str("- "),
        pandoc.Strong({term_elem})
      }))

      -- Parse and add description content
      if rest and #rest > 0 then
        rest = expand_macros(rest)
        -- Convert @@REF:label@@ placeholders to [[label]] (from itemdescr processing)
        rest = rest:gsub("@@REF:([^@]+)@@", "[[%1]]")
        -- Use +raw_tex to ensure nested custom environments (like tables) are passed as RawBlocks
        local success, parsed = pcall(pandoc.read, rest, "latex+raw_tex")
        if not success then
          io.stderr:write("ERROR: Failed to parse description item content:\n")
          io.stderr:write("Term: " .. (term or "nil") .. "\n")
          io.stderr:write("Rest (first 500 chars): " .. rest:sub(1, 500) .. "\n")
          io.stderr:write("Error: " .. tostring(parsed) .. "\n")
          error("Failed to parse description item: " .. tostring(parsed))
        end
        for _, block in ipairs(parsed.blocks) do
          -- Process RawBlocks that contain code blocks (since cpp-code-blocks.lua already ran)
          if block.tag == "RawBlock" and block.format == "latex" then
            local block_text = block.text
            -- Check if this is a codeblock environment
            local code = block_text:match("\\begin{codeblock}(.-)\\end{codeblock}")
            if code then
              -- Clean up code: remove leading/trailing whitespace
              code = code:gsub("^%s+", ""):gsub("%s+$", "")
              block = pandoc.CodeBlock(code, {class = "cpp"})
            end
            -- Check for outputblock
            if not code then
              code = block_text:match("\\begin{outputblock}(.-)\\end{outputblock}")
              if code then
                code = code:gsub("^%s+", ""):gsub("%s+$", "")
                block = pandoc.CodeBlock(code, {class = "text"})
              end
            end
            -- Check for codeblocktu
            if not code then
              code = block_text:match("\\begin{codeblocktu}{[^}]*}(.-)\\end{codeblocktu}")
              if code then
                code = code:gsub("^%s+", ""):gsub("%s+$", "")
                block = pandoc.CodeBlock(code, {class = "cpp"})
              end
            end
          end
          -- Upgrade indented code blocks to fenced (add cpp class if missing)
          if block.tag == "CodeBlock" and not block.attr.classes[1] then
            block.attr = pandoc.Attr("", {"cpp"}, {})
          end
          table.insert(blocks, block)
        end
      end

      -- Blank line between items
      table.insert(blocks, pandoc.Para({}))
    end

    if #blocks > 0 then
      return blocks
    end
    end
  end

  -- For BNF blocks: expand macros but skip special char conversion
  -- (cpp-grammar.lua handles \textbackslash specially in terminals)
  local is_bnf = text:match("\\begin{bnf}") or text:match("\\begin{ncbnf}") or
                 text:match("\\begin{ncsimplebnf}") or text:match("\\begin{ncrebnf}") or
                 text:match("\\begin{bnfbase}")

  -- Fallback: expand macros in text (skip special chars for BNF)
  elem.text = expand_macros(text, is_bnf)
  return elem
end

-- Add link reference definitions at the end of the document
-- Meta handler to receive metadata from Pandoc
function Meta(meta)
  -- Try to load library chapter names from config.tex if source directory provided
  if meta.source_dir then
    local source_dir = pandoc.utils.stringify(meta.source_dir)
    local config_path = source_dir .. "/config.tex"

    local f = io.open(config_path, "r")
    if f then
      local content = f:read("*all")
      f:close()

      -- Extract library chapter names using simple pattern matching
      local firstlib = content:match("\\newcommand{\\firstlibchapter}{([^}]*)}")
      local lastlib = content:match("\\newcommand{\\lastlibchapter}{([^}]*)}")

      if firstlib then
        FIRSTLIB = firstlib
        io.stderr:write("cpp-macros.lua: Loaded firstlibchapter = " .. FIRSTLIB .. "\n")
      end
      if lastlib then
        LASTLIB = lastlib
        io.stderr:write("cpp-macros.lua: Loaded lastlibchapter = " .. LASTLIB ..
                        "\n")
      end
    else
      io.stderr:write("cpp-macros.lua: Warning - could not open " ..
                      config_path .. ", using defaults\n")
    end
  end

  -- Get current file stem for cross-file reference detection
  if meta.current_file then
    current_file = pandoc.utils.stringify(meta.current_file)
  end

  -- Load label index if provided
  if meta.label_index_file then
    local index_path = pandoc.utils.stringify(meta.label_index_file)
    label_index = load_label_index(index_path)
  end

  return meta
end

-- Handle Code elements (inline code) to process remaining \libmember{} macros
-- This catches cases where \tcode{} was converted to Code by Pandoc's table handler
-- before our \tcode{} processing ran (issue #46)
function Code(elem)
  local text = elem.text

  -- Process \libmember{member}{class} - extract member name only
  text = text:gsub("\\libmember{([^}]*)}{([^}]*)}", "%1")

  -- Process \libglobal{name} - extract name
  text = text:gsub("\\libglobal{([^}]*)}", "%1")

  -- Convert escaped tilde to plain tilde (issue #8)
  text = text:gsub("\\~{([^}]*)}", "~%1")  -- \~{identifier} → ~identifier (remove braces)
  text = text:gsub("\\~", "~")  -- any remaining \~ → ~

  if text ~= elem.text then
    return pandoc.Code(text, elem.attr)
  end

  return elem
end

function Pandoc(doc)
  -- Merge section_labels from cpp-sections.lua with our references
  -- This ensures all section labels get link definitions, preventing duplicates (issue #2)
  if doc.meta['section_labels'] then
    for _, label in ipairs(doc.meta['section_labels']) do
      -- Convert MetaInlines to string if needed
      if type(label) == 'table' and label.t == 'MetaInlines' then
        label = pandoc.utils.stringify(label)
      end
      references[label] = true
    end
  end

  -- Collect all references (both from wikilinks and section labels) and sort them
  local refs = {}
  for ref, _ in pairs(references) do
    table.insert(refs, ref)
  end
  table.sort(refs)

  -- Create link reference definitions
  if #refs > 0 then
    -- Add a separator comment
    local separator = pandoc.RawBlock('markdown', '\n<!-- Link reference definitions -->')
    table.insert(doc.blocks, separator)

    -- Add each link definition with smart cross-file linking
    for _, ref in ipairs(refs) do
      local target = generate_link_target(ref)
      local link_def = pandoc.RawBlock('markdown', '[' .. ref .. ']: ' .. target)
      table.insert(doc.blocks, link_def)
    end
  end

  return doc
end
