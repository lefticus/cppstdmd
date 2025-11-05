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
local convert_special_chars = common.convert_special_chars
local extract_braced_content = common.extract_braced_content
local trim = common.trim
local extract_impdefx_description = common.extract_impdefx_description
local expand_impdefx_in_text = common.expand_impdefx_in_text
local parse_impdefx_description_to_inlines = common.parse_impdefx_description_to_inlines
local extract_multi_arg_macro = common.extract_multi_arg_macro
local process_macro_with_replacement = common.process_macro_with_replacement
local remove_macro = common.remove_macro

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

-- Helper function to convert inline math with subscripts in code
-- Converts $X_i$ to Xᵢ (Unicode subscript)
local function convert_math_subscripts(text)
  -- Process $...$  patterns (inline math in code)
  text = text:gsub("%$([^$]+)%$", function(math_content)
    -- Convert subscripts with braces: X_{i} → Xᵢ
    math_content = math_content:gsub("([%w]+)_{([%w]+)}", function(name, sub)
      if subscripts[sub] then
        return name .. subscripts[sub]
      else
        return name .. "_" .. sub
      end
    end)
    -- Convert subscripts without braces: X_i → Xᵢ
    math_content = math_content:gsub("([%w]+)_([%w])", function(name, sub)
      if subscripts[sub] then
        return name .. subscripts[sub]
      else
        return name .. "_" .. sub
      end
    end)
    -- Return the content without $ delimiters
    return math_content
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
    io.stderr:write("Warning: Could not load label index from " .. file_path .. ": " .. tostring(err) .. "\n")
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

-- extract_braced_content is now imported from cpp-common

-- Helper function to convert LaTeX spacing commands to regular spaces
-- Used in code processing to normalize LaTeX spacing to plain spaces
local function convert_latex_spacing(text)
  text = text:gsub("\\;", " ")        -- Medium space
  text = text:gsub("\\,", " ")        -- Thin space
  text = text:gsub("\\quad ", " ")    -- Wide space (with following space)
  text = text:gsub("\\quad", " ")     -- Wide space (standalone)
  text = text:gsub("\\qquad ", " ")   -- Very wide space (with following space)
  text = text:gsub("\\qquad", " ")    -- Very wide space (standalone)
  text = text:gsub("\\! ", " ")       -- Negative space (convert to regular space)
  text = text:gsub("\\!", " ")        -- Negative space (standalone)
  return text
end

-- convert_special_chars is now imported from cpp-common

-- Helper function to convert \mname{} macros
-- Handles special cases like VA_ARGS and VA_OPT first, then generic pattern
local function convert_mname(text)
  text = text:gsub("\\mname{VA_ARGS}", "__VA_ARGS__")
  text = text:gsub("\\mname{VA_OPT}", "__VA_OPT__")
  text = text:gsub("\\mname{([^}]*)}", "__%1__")
  return text
end

-- Helper function to expand macros in text
local function expand_macros(text, skip_special_chars)
  if not text then return text end

  -- Tier 1: Most Critical Macros
  -- \Cpp renders as C++
  text = text:gsub("\\Cpp{}", "C++")
  text = text:gsub("\\Cpp%s", "C++ ")
  text = text:gsub("\\Cpp([^%w])", "C++%1")

  -- \cppver renders as the C++ version literal (from config.tex)
  text = text:gsub("\\cppver{}", "202302L")
  text = text:gsub("\\cppver%s", "202302L ")
  text = text:gsub("\\cppver", "202302L")

  -- Strip discretionary hyphen \- used for line breaking (BEFORE processing \tcode)
  text = text:gsub("\\%-", "")

  -- Strip \itcorr[...] italic correction markers (PDF spacing corrections)
  text = text:gsub("\\itcorr%[%-?%d*%]", "")

  -- Convert LaTeX spacing commands to regular spaces (BEFORE processing \tcode)
  -- These need to be processed before \tcode{} → \texttt{} conversion
  text = convert_latex_spacing(text)
  -- NOTE: Control space (\<space>) is NOT converted here because it would
  -- conflict with table row breaks (\\) when followed by space

  -- \impdefx{description} renders as "implementation-defined  // description"
  -- MUST be processed BEFORE \tcode{} conversion to handle nested \tcode{}
  text = expand_impdefx_in_text(text, "\\impdefx{", 9, nil)

  -- \tcode{x} and \keyword{x} - convert to \texttt{x} for Pandoc to handle
  -- Pandoc's LaTeX reader will convert \texttt{} to Code elements properly
  text = text:gsub("\\tcode{", "\\texttt{")
  text = text:gsub("\\keyword{", "\\texttt{")

  -- \deflibconcept{x} - marks concept definition, just keep the name
  text = text:gsub("\\deflibconcept{([^}]*)}", "%1")

  -- Tier 2: Grammar and Special Identifiers
  -- \grammarterm{x} renders as *x* (italics)
  text = text:gsub("\\grammarterm{([^}]*)}", "*%1*")

  -- \exposid{x} renders as exposition-only identifier
  text = text:gsub("\\exposid{([^}]*)}", "*%1*")

  -- \exposidnc{x} renders as exposition-only identifier without italic correction
  text = text:gsub("\\exposidnc{([^}]*)}", "*%1*")

  -- \exposconcept{x} renders as exposition-only concept reference
  text = text:gsub("\\exposconcept{([^}]*)}", "`%1`")

  -- \placeholder{x} renders as placeholder
  text = text:gsub("\\placeholder{([^}]*)}", "*%1*")

  -- \placeholdernc{x} renders as placeholder (non-code variant)
  text = text:gsub("\\placeholdernc{([^}]*)}", "*%1*")

  -- \libheader{x} renders as <x>
  text = text:gsub("\\libheader{([^}]*)}", "`<%1>`")

  -- \libheaderdef{x} renders as <x>
  text = text:gsub("\\libheaderdef{([^}]*)}", "`<%1>`")

  -- \libheaderref{x} renders as <x> (reference to header, same as libheader)
  text = text:gsub("\\libheaderref{([^}]*)}", "`<%1>`")

  -- \libheaderrefx{header}{section} renders as <header> (ignores section label)
  text = text:gsub("\\libheaderrefx{([^}]*)}{[^}]*}", "`<%1>`")

  -- Tier 3: C++ Version Macros and General C++ Macro
  text = text:gsub("\\Cpp{}", "C++")
  text = text:gsub("\\Cpp{%*%.", "C++")  -- Handle broken case like \Cpp{*.
  text = text:gsub("\\Cpp%s+", "C++ ")

  text = text:gsub("\\CppIII{}", "C++03")
  text = text:gsub("\\CppXI{}", "C++11")
  text = text:gsub("\\CppXIV{}", "C++14")
  text = text:gsub("\\CppXVII{}", "C++17")
  text = text:gsub("\\CppXX{}", "C++20")
  text = text:gsub("\\CppXXIII{}", "C++23")

  -- Library chapter reference macros (dynamic, loaded from config.tex in Meta())
  -- Handle with braces first (more specific pattern)
  text = text:gsub("\\firstlibchapter{}", FIRSTLIB)
  text = text:gsub("\\lastlibchapter{}", LASTLIB)
  -- Then without braces
  text = text:gsub("\\firstlibchapter", FIRSTLIB)
  text = text:gsub("\\lastlibchapter", LASTLIB)
  text = text:gsub("\\CppXXVI{}", "C++26")

  -- Tier 4: Reference Standards
  text = text:gsub("\\IsoC{}", "ISO/IEC 9899:2018 (C)")
  text = text:gsub("\\IsoPosix{}", "IEEE 1003.1-2017 (POSIX)")
  text = text:gsub("\\IsoFloatUndated{}", "ISO/IEC 60559")

  -- Tier 5: Common Formatting
  -- \cv renders as "cv"
  text = text:gsub("\\cv{}", "cv")
  text = text:gsub("\\cv%s", "cv ")
  text = text:gsub("\\cv([^%w])", "cv%1")

  -- Tier 6: Library specification macros
  -- \seebelow renders as "*see below*"
  text = text:gsub("\\seebelow{}", "*see below*")
  text = text:gsub("\\seebelow%s", "*see below* ")
  text = text:gsub("\\seebelow", "*see below*")

  -- \unspec renders as "*unspecified*"
  text = text:gsub("\\unspec{}", "*unspecified*")
  text = text:gsub("\\unspec%s", "*unspecified* ")
  text = text:gsub("\\unspec", "*unspecified*")

  -- \unspecnc renders as "*unspecified*" (non-code variant)
  text = text:gsub("\\unspecnc{}", "*unspecified*")
  text = text:gsub("\\unspecnc%s", "*unspecified* ")
  text = text:gsub("\\unspecnc", "*unspecified*")

  -- \expos renders as "*exposition only*"
  text = text:gsub("\\expos{}", "*exposition only*")
  text = text:gsub("\\expos%s", "*exposition only* ")
  text = text:gsub("\\expos", "*exposition only*")

  -- \fmtgrammarterm{x} renders as *x* (format grammar term - gray sans-serif italic -> italic)
  text = text:gsub("\\fmtgrammarterm{([^}]*)}", "*%1*")

  -- \libglobal{x} renders as `x` (library global function/type)
  text = text:gsub("\\libglobal{([^}]*)}", "`%1`")

  -- \impldef{description} renders as "*implementation-defined*"
  -- The description text is informational only and doesn't appear in output
  text = process_macro_with_replacement(text, "impldef", function(content)
    return "*implementation-defined*"
  end)

  -- \cvqual renders as "cv-qualifier"
  text = text:gsub("\\cvqual{}", "cv-qualifier")
  text = text:gsub("\\cvqual%s", "cv-qualifier ")
  text = text:gsub("\\cvqual([^%w])", "cv-qualifier%1")

  -- \ctype{x} renders as C type
  text = text:gsub("\\ctype{([^}]*)}", "`%1`")

  -- \stage{N} renders as "Stage N:" (used in description lists)
  text = text:gsub("\\stage{([^}]*)}", "Stage %1:")

  -- Tier 7: Special characters and preprocessor macros
  -- Skip for BNF blocks (cpp-grammar.lua handles \textbackslash specially)
  if not skip_special_chars then
    text = convert_special_chars(text)
  end

  -- \mname{X} renders as __X__ (preprocessor macro names with underscore wrapper)
  -- \xname{X} renders as __X (special identifiers with underscore prefix)
  -- Note: \defnxname and \defnlibxname are handled in RawInline filter with proper emphasis
  -- (can't use literal asterisks here as they get escaped by Pandoc)
  text = convert_mname(text)
  text = text:gsub("\\xname{([^}]*)}", "__%1")

  -- \descr{X} renders as X (description text, just remove wrapper)
  text = text:gsub("\\descr{([^}]*)}", "%1")

  -- \defn{x} renders as definition term
  text = process_macro_with_replacement(text, "defn", function(content)
    return "*" .. content .. "*"
  end)

  -- Note: \defnx, \defnadj, \defexposconcept are now handled in RawInline
  -- with proper emphasis using pandoc.Emph() instead of literal asterisks

  -- Change description macros - these are section headers in change history
  -- \change -> **Change:**
  text = text:gsub("\\change%s*\n", "**Change:** ")
  text = text:gsub("\\change%s+", "**Change:** ")
  text = text:gsub("\\change([^%w])", "**Change:**%1")

  -- \rationale -> **Rationale:**
  text = text:gsub("\\rationale%s*\n", "**Rationale:** ")
  text = text:gsub("\\rationale%s+", "**Rationale:** ")
  text = text:gsub("\\rationale([^%w])", "**Rationale:**%1")

  -- \effect -> **Effect on original feature:**
  text = text:gsub("\\effect%s*\n", "**Effect on original feature:** ")
  text = text:gsub("\\effect%s+", "**Effect on original feature:** ")
  text = text:gsub("\\effect([^%w])", "**Effect on original feature:**%1")

  -- \term{x} renders as term
  text = process_macro_with_replacement(text, "term", function(content)
    return "*" .. content .. "*"
  end)

  -- \doccite{x} renders as italic (document citation)
  text = text:gsub("\\doccite{([^}]*)}", "*%1*")

  -- \opt{x} renders as x_opt (optional grammar element with subscript marker)
  -- Use simple pattern - don't recursively expand since expand_macros processes left-to-right
  -- Special case \opt{\grammarterm{...}} is handled in RawInline for emphasis preservation
  text = text:gsub("\\opt{([^}]*)}", "%1_opt")

  -- \ucode{XXXX} renders Unicode code point as U+XXXX
  -- The LaTeX macro does complex text scaling, but for Markdown we simplify to standard format
  text = text:gsub("\\ucode{([^}]*)}", "`U+%1`")

  -- \ntbs{} and \ntmbs{} - null-terminated byte/multibyte string abbreviations
  -- These expand to \NTS{ntbs} -> \textsc{ntbs} which should render as uppercase
  text = text:gsub("\\ntbs{}", "NTBS")
  text = text:gsub("\\ntmbs{}", "NTMBS")
  -- Also handle \NTS{text} directly (converts \textsc{text} to uppercase)
  text = text:gsub("\\NTS{([^}]*)}", function(s) return s:upper() end)

  -- Special characters that may appear in inline text (already handled above by convert_special_chars)
  -- Left here for documentation but no longer needed as duplicates

  -- \uname{X} → X (Unicode character names - strip small caps formatting)
  text = text:gsub("\\uname{([^}]*)}", "%1")

  -- \notdef → *not defined* (exposition-only marker)
  text = text:gsub("\\notdef{}", "*not defined*")
  text = text:gsub("\\notdef%s", "*not defined* ")
  text = text:gsub("\\notdef", "*not defined*")

  -- \colcol{} renders as ::
  text = text:gsub("\\colcol{}", "::")

  -- Math formatting
  text = text:gsub("\\mathit{([^}]*)}", "*%1*")
  text = text:gsub("\\mathrm{([^}]*)}", "%1")

  -- Helper function to split comma-separated references and create individual links
  -- E.g., "a,b,c" -> "[[a]], [[b]], [[c]]"
  local function split_refs(refs_str)
    local parts = {}
    for ref in refs_str:gmatch("([^,]+)") do
      ref = trim(ref)  -- trim whitespace
      references[ref] = true
      table.insert(parts, "[[" .. ref .. "]]")
    end
    return table.concat(parts, ", ")
  end

  -- Cross-references - convert to reference-style links for consistency
  -- with C++ standard's stable name convention [section.name]
  -- Add space before reference for readability if not already present
  -- Handles comma-separated refs: \ref{a,b,c} -> [a], [b], [c]
  text = text:gsub("([^%s])\\ref{([^}]*)}", function(before, refs)
    return before .. " " .. split_refs(refs)
  end)
  text = text:gsub("^\\ref{([^}]*)}", function(refs)
    return split_refs(refs)
  end)

  -- \iref is "inline ref" - also should use [section.name] format
  -- Add space before reference for readability if not already present
  -- Handles comma-separated refs: \iref{a,b,c} -> [a], [b], [c]
  text = text:gsub("([^%s])\\iref{([^}]*)}", function(before, refs)
    return before .. " " .. split_refs(refs)
  end)
  text = text:gsub("^\\iref{([^}]*)}", function(refs)
    return split_refs(refs)
  end)

  -- \tref is "table ref" - also should use [section.name] format
  -- Add space before reference for readability if not already present
  -- Handles comma-separated refs: \tref{a,b,c} -> [a], [b], [c]
  text = text:gsub("([^%s])\\tref{([^}]*)}", function(before, refs)
    return before .. " " .. split_refs(refs)
  end)
  text = text:gsub("^\\tref{([^}]*)}", function(refs)
    return split_refs(refs)
  end)

  return text
end

-- Apply to all string elements
function Str(elem)
  elem.text = expand_macros(elem.text)
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
  if text:match("^\\indextext{") or text:match("^\\index{") then
    return {}  -- Return empty list to remove element
  end

  -- \impldef{description} - handle BEFORE \tcode to avoid greedy matching issues
  if text:match("^\\impldef{") then
    return pandoc.Emph({pandoc.Str("implementation-defined")})
  end

  -- \impdefx{description} - handle BEFORE \tcode to extract description with nested macros
  if text:match("^\\impdefx{") then
    local description, _ = extract_impdefx_description(text, 1, 9, nil)  -- "\impdefx{" is 9 chars
    if description then
      return parse_impdefx_description_to_inlines(description)
    end
  end

  -- \term{} - use brace-balanced extraction to handle nested \tcode{}
  -- Handle BEFORE \tcode to avoid greedy matching issues
  if text:match("^\\term{") then
    local content, _ = extract_braced_content(text, 1, 5)  -- "\term" is 5 chars
    if content then
      -- Parse content into a list of inline elements
      local inlines = {}
      local pos = 1
      while pos <= #content do
        -- Look for \tcode{...}
        local tcode_start, tcode_end = content:find("\\tcode{", pos, true)
        if tcode_start then
          -- Add text before \tcode
          if tcode_start > pos then
            local text_before = content:sub(pos, tcode_start - 1)
            text_before = text_before:gsub("\\#", "#"):gsub("\\&", "&")
            table.insert(inlines, pandoc.Str(text_before))
          end
          -- Extract \tcode content
          local tcode_content, next_pos = extract_braced_content(content, tcode_start, 6)  -- "\tcode" is 6 chars
          if tcode_content then
            tcode_content = tcode_content:gsub("\\#", "#"):gsub("\\&", "&")
            -- Convert inline math with subscripts to Unicode
            tcode_content = convert_math_subscripts(tcode_content)
            -- Convert LaTeX spacing commands to regular spaces
            tcode_content = convert_latex_spacing(tcode_content)
            table.insert(inlines, pandoc.Code(tcode_content))
            pos = next_pos
          else
            -- Malformed \tcode, skip it
            pos = tcode_end + 1
          end
        else
          -- No more \tcode, add remaining text
          local remaining = content:sub(pos)
          remaining = remaining:gsub("\\#", "#"):gsub("\\&", "&")
          table.insert(inlines, pandoc.Str(remaining))
          break
        end
      end
      return pandoc.Emph(inlines)
    end
  end

  -- Inline code macros - return Code elements
  -- Need to expand nested macros first
  local code

  code = text:match("\\tcode{(.*)}")
  if code then
    -- Strip \brk{} line break hints and \- discretionary hyphens first
    code = code:gsub("\\brk{}", "")
    code = code:gsub("\\%-", "")
    -- Convert inline math with subscripts to Unicode (BEFORE other processing)
    code = convert_math_subscripts(code)
    -- Convert LaTeX spacing commands to regular spaces
    code = convert_latex_spacing(code)
    -- Handle escaped special characters
    code = code:gsub("\\([~!@#$%%^&*])", "%1")
    -- Clean up ~{} from LaTeX \~{} (tilde with spacing braces)
    code = code:gsub("~{}", "~")
    -- Expand nested macros in code content
    code = code:gsub("\\keyword{([^}]*)}", "%1")
    code = code:gsub("\\ctype{([^}]*)}", "%1")
    code = code:gsub("\\term{([^}]*)}", "%1")
    code = code:gsub("\\grammarterm{([^}]*)}", "%1")
    code = code:gsub("\\libconcept{([^}]*)}", "%1")
    code = code:gsub("\\exposconcept{([^}]*)}", "%1")
    code = code:gsub("\\placeholder{([^}]*)}", "%1")
    code = code:gsub("\\placeholdernc{([^}]*)}", "%1")
    code = code:gsub("\\exposid{([^}]*)}", "%1")
    code = code:gsub("\\mathit{([^}]*)}", "%1")
    code = code:gsub("\\mathrm{([^}]*)}", "%1")
    code = code:gsub("\\colcol{}", "::")
    -- Handle special characters
    code = convert_special_chars(code)
    -- Handle \mname macros
    code = convert_mname(code)
    return pandoc.Code(code)
  end

  code = text:match("\\keyword{([^}]*)}")
  if code then return pandoc.Code(code) end

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
    local content, _ = extract_braced_content(text, doccite_start, 8)  -- "\doccite" is 8 chars
    if content then
      -- Expand macros in content before wrapping in emphasis
      content = expand_macros(content)
      return pandoc.Emph({pandoc.Str(content)})
    end
  end

  -- Function description cross-reference - use brace-balanced parsing
  local fundescx_start = text:find("\\Fundescx{", 1, true)
  if fundescx_start then
    local content, _ = extract_braced_content(text, fundescx_start, 9)  -- "\Fundescx" is 9 chars
    if content then
      -- Expand macros in content before wrapping in emphasis
      content = expand_macros(content)
      return pandoc.Emph({pandoc.Str(content)})
    end
  end

  -- Other emphasis macros - return Emph elements
  local emph

  -- \oldconcept{x} - C++17-era named requirements (prepend Cpp17 prefix)
  emph = text:match("\\oldconcept{([^}]*)}")
  if emph then return pandoc.Emph({pandoc.Str("Cpp17" .. emph)}) end

  -- Emphasis macros - return Emph elements

  -- \opt{\grammarterm{...}} - optional grammar term (special case before general grammarterm handling)
  local opt_start = text:find("\\opt{", 1, true)
  if opt_start and opt_start == 1 then
    local opt_content, opt_end = extract_braced_content(text, opt_start, 4)  -- \opt is 4 chars
    if opt_content and opt_end and opt_end - 1 == #text then
      -- Check if content is \grammarterm{...}
      if opt_content:match("^\\grammarterm{") then
        local term, _ = extract_braced_content(opt_content, 1, 12)  -- \grammarterm is 12 chars
        if term then
          -- Return Emph followed by _opt suffix
          return {pandoc.Emph({pandoc.Str(term)}), pandoc.Str("_opt")}
        end
      end
    end
  end

  -- \grammarterm{term}{suffix} - with optional suffix (e.g., {s} for plurals)
  -- Returns Emph + Str if suffix present, otherwise just Emph
  local grammarterm_start = text:find("\\grammarterm{", 1, true)
  if grammarterm_start and grammarterm_start == 1 then  -- Must be at start
    local term, pos_after_term = extract_braced_content(text, grammarterm_start, 12)  -- \grammarterm is 12 chars
    if term then
      -- Check if there's a second argument (suffix)
      if pos_after_term and pos_after_term <= #text and text:sub(pos_after_term, pos_after_term) == "{" then
        local suffix, pos_after_suffix = extract_braced_content(text, pos_after_term, 0)
        if suffix and pos_after_suffix and pos_after_suffix - 1 == #text then  -- Suffix must end the string
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
    local content, _ = extract_braced_content(text, defn_start, 5)  -- "\defn" is 5 chars
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
      -- Expand macros in plural form before wrapping in emphasis
      plural = expand_macros(plural)
      return pandoc.Emph({pandoc.Str(plural)})
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

  -- \fmtgrammarterm{x} - format grammar term (italic)
  emph = text:match("\\fmtgrammarterm{([^}]*)}")
  if emph then return pandoc.Emph({pandoc.Str(emph)}) end

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

  -- \descr{X} - description text, just unwrap
  local descr = text:match("\\descr{([^}]*)}")
  if descr then
    return pandoc.Str(descr)
  end

  -- \range{first}{last} - half-open range [first, last)
  local first, last = text:match("\\range{([^}]*)}{([^}]*)}")
  if first and last then
    return pandoc.RawInline('markdown', '[`' .. first .. '`, `' .. last .. '`)')
  end

  -- Handle bare \Cpp (without braces)
  if text == "\\Cpp" then
    return pandoc.Str("C++")
  end

  -- Handle bare \cv (without braces)
  if text == "\\cv" then
    return pandoc.Str("cv")
  end

  -- Library specification macros - return as Emph
  if text:match("^\\seebelow") then
    return pandoc.Emph({pandoc.Str("see below")})
  end

  if text:match("^\\unspec") then
    return pandoc.Emph({pandoc.Str("unspecified")})
  end

  if text:match("^\\unspecnc") then
    return pandoc.Emph({pandoc.Str("unspecified")})
  end

  if text:match("^\\expos") then
    return pandoc.Emph({pandoc.Str("exposition only")})
  end

  -- \UAX{number} - Unicode Annex reference (e.g., \UAX{31} -> UAX #31)
  local uax_num = text:match("^\\UAX{([^}]*)}")
  if uax_num then
    return pandoc.Str("UAX #" .. uax_num)
  end

  -- \unicode{code}{description} - Unicode character with description
  -- This needs special handling because Pandoc recognizes \unicode as a known LaTeX command
  local unicode_match = text:match("^\\unicode{")
  if unicode_match then
    -- Extract both brace-balanced arguments
    local args, _ = extract_multi_arg_macro(text, 1, 8, 2)  -- \unicode is 8 chars, 2 args
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
  text = text:gsub("\\uname{([^}]*)}", "%1")

  -- \notdef → *not defined* (exposition-only marker)
  text = text:gsub("\\notdef{}", "*not defined*")
  text = text:gsub("\\notdef%s", "*not defined* ")
  text = text:gsub("\\notdef", "*not defined*")

  -- \unicode{XXXX}{description} → U+XXXX (description)
  -- This macro takes two brace-balanced arguments
  while true do
    local start_pos = text:find("\\unicode{", 1, true)
    if not start_pos then break end

    local args, end_pos = extract_multi_arg_macro(text, start_pos, 8, 2)  -- \unicode is 8 chars, 2 args
    if not args then break end

    -- Replace \unicode{XXXX}{desc} with U+XXXX (desc)
    text = text:sub(1, start_pos - 1) .. "U+" .. args[1] .. " (" .. args[2] .. ")" .. text:sub(end_pos)
  end

  -- Handle \mname{} macros
  text = convert_mname(text)

  -- \deflibconcept{x} - marks concept definition, just keep the name
  text = text:gsub("\\deflibconcept{([^}]*)}", "%1")

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
    local plural, next_pos = extract_braced_content(text, 1, 6)  -- "\defnx" is 6 chars
    if plural then
      -- Parse plural content into a list of inline elements
      local inlines = {}
      local pos = 1
      while pos <= #plural do
        -- Look for \tcode{...}
        local tcode_start, tcode_end = plural:find("\\tcode{", pos, true)
        if tcode_start then
          -- Add text before \tcode
          if tcode_start > pos then
            local text_before = plural:sub(pos, tcode_start - 1)
            text_before = text_before:gsub("\\#", "#"):gsub("\\&", "&")
            table.insert(inlines, pandoc.Str(text_before))
          end
          -- Extract \tcode content
          local tcode_content, tcode_next_pos = extract_braced_content(plural, tcode_start, 6)  -- "\tcode" is 6 chars
          if tcode_content then
            tcode_content = tcode_content:gsub("\\#", "#"):gsub("\\&", "&")
            table.insert(inlines, pandoc.Code(tcode_content))
            pos = tcode_next_pos
          else
            -- Malformed \tcode, skip it
            pos = tcode_end + 1
          end
        else
          -- No more \tcode, add remaining text
          local remaining = plural:sub(pos)
          remaining = remaining:gsub("\\#", "#"):gsub("\\&", "&")
          table.insert(inlines, pandoc.Str(remaining))
          break
        end
      end
      return pandoc.Para({pandoc.Emph(inlines)})
    end
  end

  -- Handle description lists (used for predefined macros, etc.)
  -- Find balanced begin/end description pairs
  local desc_start = text:find("\\begin{description}")
  if desc_start then
    -- Find the matching \end{description} accounting for nesting
    local pos = desc_start + 19 -- length of "\begin{description}"
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

    -- Split content by \item or \stage{N}
    local pos = 1
    while true do
      -- Look for either \item or \stage{...}
      local item_start, item_end = desc_content:find("\\item%s*", pos)
      local stage_start, stage_end = desc_content:find("\\stage{[^}]*}", pos)

      -- Use whichever comes first
      local start_pos, end_pos, is_stage
      if item_start and (not stage_start or item_start < stage_start) then
        start_pos, end_pos = item_start, item_end
        is_stage = false
      elseif stage_start then
        start_pos, end_pos = stage_start, stage_end
        is_stage = true
      else
        break -- No more items
      end

      -- Get text until next \item/\stage or end
      local next_item = desc_content:find("\\item%s*", end_pos + 1)
      local next_stage = desc_content:find("\\stage{[^}]*}", end_pos + 1)
      local next_start
      if next_item and (not next_stage or next_item < next_stage) then
        next_start = next_item
      else
        next_start = next_stage
      end

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

      pos = end_pos + 1
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
        local parsed = pandoc.read(rest, "latex")
        for _, block in ipairs(parsed.blocks) do
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
        io.stderr:write("cpp-macros.lua: Loaded lastlibchapter = " .. LASTLIB .. "\n")
      end
    else
      io.stderr:write("cpp-macros.lua: Warning - could not open " .. config_path .. ", using defaults\n")
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

function Pandoc(doc)
  -- Collect all references and sort them
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
