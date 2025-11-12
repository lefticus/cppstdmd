-- cpp-math.lua
-- Convert simple LaTeX math to Unicode characters
-- Complex math is left as LaTeX for MathJax/KaTeX rendering

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local subscripts = common.subscripts

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
  ["i"] = "ⁱ",
  ["n"] = "ⁿ",
}

-- subscripts is now imported from cpp-common

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
  -- BUT: Allow simple arithmetic like _{n-1} or _{i+1} (single char + operator + single char)
  for subscript in text:gmatch("_(%b{})") do
    local content = subscript:sub(2, -2)  -- Remove braces
    -- Check if it's simple arithmetic: single char, +/-, single char
    local is_simple_arithmetic = content:match("^%w[-+]%w$")
    -- If content has more than one character (excluding whitespace) or contains backslash, it's complex
    -- UNLESS it's simple arithmetic which we can convert
    if not is_simple_arithmetic and (content:match("%S.*%S") or content:match("\\")) then
      return true
    end
  end

  for superscript in text:gmatch("%^(%b{})") do
    local content = superscript:sub(2, -2)  -- Remove braces
    if content:match("%S.*%S") or content:match("\\") then
      return true
    end
  end

  return false
end

-- Convert simple subscript
local function convert_subscript(char)
  return subscripts[char] or nil
end

-- Convert simple superscript
local function convert_superscript(char)
  return superscripts[char] or nil
end

-- Helper function to extract content from \tcode{} and \texttt{} with nested braces
local function extract_code_macro(text, macro_name)
  local results = {}
  local i = 1
  while i <= #text do
    local start_pos = text:find("\\" .. macro_name .. "{", i, true)
    if not start_pos then
      break
    end

    -- Find the matching closing brace
    local brace_count = 0
    local content_start = start_pos + #macro_name + 2  -- Skip \macro_name{
    local j = content_start
    local content_end = nil

    while j <= #text do
      if text:sub(j, j) == "{" then
        brace_count = brace_count + 1
      elseif text:sub(j, j) == "}" then
        if brace_count == 0 then
          content_end = j - 1
          break
        end
        brace_count = brace_count - 1
      end
      j = j + 1
    end

    if content_end then
      local content = text:sub(content_start, content_end)
      local macro_end = j  -- Position of closing brace

      -- Check for subscript after the macro: _{n} or _n
      local subscript = nil
      local full_end = macro_end

      if text:sub(macro_end + 1, macro_end + 1) == "_" then
        if text:sub(macro_end + 2, macro_end + 2) == "{" then
          -- Pattern: _{n}
          local sub_end = text:find("}", macro_end + 2, true)
          if sub_end then
            subscript = text:sub(macro_end + 3, sub_end - 1)
            full_end = sub_end
          end
        else
          -- Pattern: _n
          local sub_match = text:match("^([%w]+)", macro_end + 2)
          if sub_match then
            subscript = sub_match
            full_end = macro_end + 1 + #sub_match
          end
        end
      end

      table.insert(results, {
        content = content,
        subscript = subscript,
        start_pos = start_pos,
        end_pos = full_end
      })

      i = full_end + 1
    else
      i = start_pos + 1
    end
  end

  return results
end

-- Check if text is fully converted to Unicode (no LaTeX remaining)
-- Returns true if 100% Unicode, false if any LaTeX patterns detected
local function is_fully_converted(text)
  -- Check for backslash commands (indicates unconverted LaTeX)
  if text:match("\\") then
    return false
  end

  -- Check for complex superscripts (^{...})
  if text:match("%^{") then
    return false
  end

  -- Check for complex subscripts (_{...})
  if text:match("_{") then
    return false
  end

  -- Check for remaining braces (usually indicates LaTeX structures)
  if text:match("[{}]") then
    return false
  end

  -- Text is fully converted
  return true
end

-- Try to convert math to Unicode
local function try_unicode_conversion(text)
  -- Trim whitespace
  text = text:gsub("^%s+", ""):gsub("%s+$", "")

  -- Start conversion
  local result = text

  -- Convert \mathtt{X} -> X (already monospace in markdown code)
  result = result:gsub("\\mathtt{([^}]*)}", "%1")

  -- Convert \mathrm{text} -> text
  result = result:gsub("\\mathrm{([^}]*)}", "%1")

  -- Convert \mathit{text} -> text (we'll use plain text)
  result = result:gsub("\\mathit{([^}]*)}", "%1")

  -- Convert \mathsf{text} -> text (sans-serif font)
  result = result:gsub("\\mathsf{([^}]*)}", "%1")

  -- Convert ordinal superscripts BEFORE \text{} conversion
  -- Patterns like $i^\text{th}$ -> iᵗʰ, $1^\text{st}$ -> 1ˢᵗ
  result = result:gsub("%^\\text{th}", "ᵗʰ")
  result = result:gsub("%^\\text{st}", "ˢᵗ")
  result = result:gsub("%^\\text{nd}", "ⁿᵈ")
  result = result:gsub("%^\\text{rd}", "ʳᵈ")

  -- Convert \text{text} -> text (text mode in math)
  result = result:gsub("\\text{([^}]*)}", "%1")

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

  -- Convert operators using plain replacement for special characters
  -- IMPORTANT: Sort by length (longest first) to avoid partial matches
  -- For example, \cdots must be replaced before \cdot to prevent leaving 's' behind
  -- This bug was discovered when \cdots → ⋯ was being converted as \cdot → ⋅ + 's'
  local sorted_operators = {}
  for latex, unicode in pairs(math_operators) do
    table.insert(sorted_operators, {latex = latex, unicode = unicode})
  end
  table.sort(sorted_operators, function(a, b) return #a.latex > #b.latex end)

  for _, op in ipairs(sorted_operators) do
    result = plain_replace(result, op.latex, op.unicode)
  end

  -- Convert math functions using plain replacement
  for latex, text_replacement in pairs(math_functions) do
    result = plain_replace(result, latex, text_replacement)
  end

  -- NOW check if this is complex math that shouldn't be converted
  -- (after simple conversions, so we don't have false positives)
  if is_complex_math(result) then
    return nil
  end

  -- Convert simple superscripts: x^2 or x^{n}
  -- First pass: check if all superscripts are convertible
  local has_unconvertible_super = false
  result:gsub("(%w)%^(%w)", function(base, exp)
    if not convert_superscript(exp) then
      has_unconvertible_super = true
    end
  end)
  result:gsub("(%w)%^{(%w)}", function(base, exp)
    if not convert_superscript(exp) then
      has_unconvertible_super = true
    end
  end)

  if has_unconvertible_super then
    return nil  -- Abort conversion if any superscript can't be converted
  end

  -- Second pass: actually convert
  result = result:gsub("(%w)%^(%w)", function(base, exp)
    local unicode_exp = convert_superscript(exp)
    return base .. unicode_exp
  end)

  result = result:gsub("(%w)%^{(%w)}", function(base, exp)
    local unicode_exp = convert_superscript(exp)
    return base .. unicode_exp
  end)

  -- Convert simple subscripts: x_i or x_{0}
  -- First pass: check if all subscripts are convertible
  local has_unconvertible_sub = false
  result:gsub("(%w)_(%w)", function(base, sub)
    if not convert_subscript(sub) then
      has_unconvertible_sub = true
    end
  end)
  result:gsub("(%w)_{(%w)}", function(base, sub)
    if not convert_subscript(sub) then
      has_unconvertible_sub = true
    end
  end)

  -- Check arithmetic subscripts: x_{n-1}, x_{i+1}
  result:gsub("(%w)_{(%w)([-+])(%w)}", function(base, sub1, op, sub2)
    if not convert_subscript(sub1) or not convert_subscript(op) or not convert_subscript(sub2) then
      has_unconvertible_sub = true
    end
  end)

  if has_unconvertible_sub then
    return nil  -- Abort conversion if any subscript can't be converted
  end

  -- Second pass: actually convert arithmetic subscripts first (before simple ones)
  -- Pattern: x_{n-1} → xₙ₋₁, p_{i+1} → pᵢ₊₁
  result = result:gsub("(%w)_{(%w)([-+])(%w)}", function(base, sub1, op, sub2)
    local unicode_sub1 = convert_subscript(sub1)
    local unicode_op = convert_subscript(op)
    local unicode_sub2 = convert_subscript(sub2)
    return base .. unicode_sub1 .. unicode_op .. unicode_sub2
  end)

  -- Then convert simple subscripts
  result = result:gsub("(%w)_(%w)", function(base, sub)
    local unicode_sub = convert_subscript(sub)
    return base .. unicode_sub
  end)

  result = result:gsub("(%w)_{(%w)}", function(base, sub)
    local unicode_sub = convert_subscript(sub)
    return base .. unicode_sub
  end)

  -- If we still have LaTeX commands, we can't fully convert
  if result:match("\\[a-zA-Z]") then
    return nil
  end

  -- If we still have ^{ or _{ patterns, we couldn't convert them
  if result:match("[%^_]{") then
    return nil
  end

  return result
end

-- Main filter function
function Math(elem)
  -- Only process inline math
  if elem.mathtype == "InlineMath" then
    local text = elem.text
    local original_text = text  -- Save original for potential revert

    -- Special case: Math containing \tcode{} or \texttt{} (code with subscripts/operators)
    -- Examples: $\tcode{\placeholder{C}}_0$, $\texttt{count} \geq \texttt{n}$
    -- Convert to inline code with Unicode subscripts/operators
    if text:match("\\tcode{") or text:match("\\texttt{") then
      -- Extract all \tcode{} and \texttt{} macros with their subscripts
      local tcode_parts = extract_code_macro(text, "tcode")
      local texttt_parts = extract_code_macro(text, "texttt")

      -- Combine all parts and track positions for processing
      local all_parts = {}
      for _, part in ipairs(tcode_parts) do
        part.macro_type = "tcode"
        table.insert(all_parts, part)
      end
      for _, part in ipairs(texttt_parts) do
        part.macro_type = "texttt"
        table.insert(all_parts, part)
      end

      -- Sort by position
      table.sort(all_parts, function(a, b) return a.start_pos < b.start_pos end)

      -- Build result by replacing macros and converting subscripts/operators
      if #all_parts > 0 then
        local result = ""
        local last_pos = 1

        for _, part in ipairs(all_parts) do
          -- Add text before this macro
          if part.start_pos > last_pos then
            result = result .. text:sub(last_pos, part.start_pos - 1)
          end

          -- Process the macro content
          local content = part.content
          if part.macro_type == "tcode" then
            -- Remove \placeholder{} wrappers
            content = content:gsub("\\placeholder{([^}]*)}", "%1")
          end

          -- Add subscript if present
          if part.subscript then
            local unicode_sub = subscripts[part.subscript]
            if unicode_sub then
              content = content .. unicode_sub
            else
              content = content .. "_" .. part.subscript
            end
          end

          -- Wrap in backticks
          result = result .. "`" .. content .. "`"

          last_pos = part.end_pos + 1
        end

        -- Add remaining text after last macro
        if last_pos <= #text then
          result = result .. text:sub(last_pos)
        end

        -- Convert operators to Unicode
        result = result:gsub("\\geq", "≥")
        result = result:gsub("\\leq", "≤")
        result = result:gsub("\\neq", "≠")

        return pandoc.RawInline('markdown', result)
      end
    end

    -- Regular math conversion
    local converted = try_unicode_conversion(text)

    if converted then
      -- All-or-nothing approach: Check if 100% converted to Unicode
      -- If ANY LaTeX remains, revert to original $...$ form
      if is_fully_converted(converted) then
        -- 100% converted - use Unicode version
        return pandoc.RawInline('markdown', converted)
      else
        -- Partial conversion detected - revert to original LaTeX
        -- This ensures consistency: either fully readable or fully LaTeX for MathJax
        return pandoc.RawInline('markdown', "$" .. original_text .. "$")
      end
    end
  end

  -- Return unchanged (display math or unconvertible inline math)
  return elem
end

return {
  {Math = Math}
}
