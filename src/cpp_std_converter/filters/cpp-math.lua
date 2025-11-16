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

-- REMOVED DUPLICATION: All math conversion tables and functions now in cpp-common.lua
-- Imported: try_unicode_conversion (the main conversion function with all-or-nothing logic)
local try_unicode_conversion = common.try_unicode_conversion

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
  -- Check for LaTeX commands (backslash followed by letter)
  -- Allow bare backslashes (from \backslash conversion) and >> << (ASCII operators)
  if text:match("\\[a-zA-Z]") then
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
            -- Use process_macro_with_replacement for proper brace-balancing (fixes ([^}]*) anti-pattern)
            content = common.process_macro_with_replacement(content, "placeholder", function(c)
              return c
            end)
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
