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
cpp-tables.lua

Pandoc Lua filter to convert C++ standard table environments to GFM tables.

Handles:
- \begin{floattable}{caption}{label}{colspec}...\end{floattable}
- \begin{libsumtab}{caption}{label}...\end{libsumtab}
- \begin{LongTable}{caption}{label}{colspec}...\end{LongTable}
- \begin{concepttable}{caption}{label}{colspec}...\end{concepttable}
- \begin{simpletypetable}{caption}{label}{colspec}...\end{simpletypetable}
- \begin{oldconcepttable}{name}{extra}{label}{colspec}...\end{oldconcepttable}

All convert to pipe-delimited GFM tables.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local convert_special_chars = common.convert_special_chars
local trim = common.trim
local extract_braced = common.extract_braced
local expand_balanced_command = common.expand_balanced_command
local replace_code_macro_special_chars = common.replace_code_macro_special_chars
local process_code_macro = common.process_code_macro
local extract_multi_arg_macro = common.extract_multi_arg_macro
local split_refs_text = common.split_refs_text

-- Initialize references table if not already created by cpp-macros.lua
-- This allows cpp-tables.lua to work standalone or as part of filter chain
if not references then
  references = {}
end

-- Environment length constants (for caption offset calculations)
local ENV_BEGIN_LEN = {
  floattable = 18,      -- \begin{floattable}
  libsumtab = 17,       -- \begin{libsumtab}
  lib2dtab2 = 17,       -- \begin{lib2dtab2}
  libtab2 = 15,         -- \begin{libtab2}
  libefftab = 17,       -- \begin{libefftab}
  longlibefftab = 21,   -- \begin{longlibefftab}
  longliberrtab = 21,   -- \begin{longliberrtab}
  LongTable = 17,       -- \begin{LongTable}
  concepttable = 20,    -- \begin{concepttable}
  simpletypetable = 23, -- \begin{simpletypetable}
  oldconcepttable = 23, -- \begin{oldconcepttable}
}

-- Helper function to expand common macros in table cells
local function expand_table_macros(text)
  if not text then return text end

  -- \keyword{X} → X (strip keyword markup, keep content)
  -- Process this first and repeatedly until all nested keywords are removed
  text = expand_balanced_command(text, "keyword", function(content) return content end)

  -- \hdstyle{X} → X (strip header style markup, keep content)
  -- Used in table headers to make text bold
  text = expand_balanced_command(text, "hdstyle", function(content) return content end)

  -- \uname{X} → X (Unicode character names - strip small caps formatting)
  text = expand_balanced_command(text, "uname", function(content) return content end)

  -- \textbf{X} → **X** (bold text in markdown)
  text = expand_balanced_command(text, "textbf",
                                  function(content) return "**" .. content .. "**" end)

  -- \textit{X} → X (strip italic wrapper - tailnotes are already italicized)
  text = expand_balanced_command(text, "textit",
                                  function(content) return content end)

  -- \libglobal{X} → `X` (library global identifiers)
  text = expand_balanced_command(text, "libglobal",
                                  function(content) return "`" .. content .. "`" end)

  -- Special characters
  text = convert_special_chars(text)

  -- \notdef → *not defined* (exposition-only marker)
  text = text:gsub("\\notdef{}", "*not defined*")
  text = text:gsub("\\notdef%s", "*not defined* ")
  text = text:gsub("\\notdef", "*not defined*")

  -- Strip italic corrections (PDF-only spacing)
  text = text:gsub("\\itcorr%[%-?%d*%]", "")
  text = text:gsub("\\itcorr{}", "")
  text = text:gsub("\\itcorr%s", "")

  -- Handle bare \texttt{} and \tcode{} with escaped special chars FIRST
  -- (before process_code_macro which uses extract_braced that doesn't handle escaped braces)
  text = replace_code_macro_special_chars(text, "tcode")
  text = replace_code_macro_special_chars(text, "texttt")

  -- \tcode{X} → `X` and \texttt{X} → `X`
  -- Use balanced brace extraction to handle nested braces like \tcode{T u\{\};}
  text = process_code_macro(text, "tcode")
  text = process_code_macro(text, "texttt")

  -- \xname{X} → __X
  text = text:gsub("\\xname{([^}]*)}", "__%1")

  -- \defnxname{X} → `__X` (for feature-test macros, uses \xname which only adds prefix)
  -- Wrapped in backticks to render as code, not markdown bold
  text = text:gsub("\\defnxname{([^}]*)}", "`__%1`")

  -- \defnlibxname{X} → `__X` (for library feature-test macros, uses \xname which only adds prefix)
  -- Wrapped in backticks to render as code, not markdown bold
  text = text:gsub("\\defnlibxname{([^}]*)}", "`__%1`")

  -- \mname{X} → __X__
  text = text:gsub("\\mname{([^}]*)}", "__%1__")


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

  -- \multicolumn{N}{alignment}{content} → content
  -- Markdown doesn't support column spans, so just extract the content
  -- This macro takes three brace-balanced arguments
  while true do
    local start_pos = text:find("\\multicolumn{", 1, true)
    if not start_pos then break end

    -- Extract first argument (number of columns to span)
    -- "\\multicolumn{" is 12 chars total, so first { after it is at start_pos + 12
    local num_cols, pos1 = extract_braced(text, start_pos + 12)
    if not num_cols then
      -- Debug: extraction failed, add marker and break
      text = text:gsub("\\multicolumn{", "[MULTICOLUMN-EXTRACT-FAILED]{", 1)
      break
    end

    -- Extract second argument (alignment spec like |p{5.3in}|)
    local alignment, pos2 = extract_braced(text, pos1)
    if not alignment then break end

    -- Extract third argument (cell content)
    local content, pos3 = extract_braced(text, pos2)
    if not content then break end

    -- Recursively process content (may contain nested macros)
    content = expand_table_macros(content)

    -- Replace \multicolumn{...}{...}{content} with just content
    -- Prefix with note about column span for clarity
    local replacement = "*[spans " .. num_cols .. " columns]* " .. content
    text = text:sub(1, start_pos - 1) .. replacement .. text:sub(pos3)
  end

  -- \begin{itemize} ... \end{itemize} → semicolon-separated list
  -- Convert itemized lists to readable inline format
  while true do
    local itemize_start = text:find("\\begin{itemize}", 1, true)
    if not itemize_start then break end

    local itemize_end = text:find("\\end{itemize}", itemize_start, true)
    if not itemize_end then break end

    local list_content = text:sub(itemize_start + 15, itemize_end - 1)  -- +15 for "\begin{itemize}"

    -- Split on \item and collect items
    local items = {}
    for item in list_content:gmatch("\\item%s*([^\\]*)") do
      item = trim(item)  -- trim whitespace
      if item ~= "" then
        -- Recursively expand any macros in the item
        item = expand_table_macros(item)
        table.insert(items, item)
      end
    end

    -- Join with semicolons for readability
    local replacement = table.concat(items, "; ")
    -- +14 for "\end{itemize}"
    text = text:sub(1, itemize_start - 1) .. replacement ..
           text:sub(itemize_end + 14)
  end

  -- \begin{tailnote} ... \end{tailnote} → italic text
  -- Tailnotes are footnotes/clarifications, render as emphasized text
  while true do
    local note_start = text:find("\\begin{tailnote}", 1, true)
    if not note_start then break end

    local note_end = text:find("\\end{tailnote}", note_start, true)
    if not note_end then break end

    -- +16 for "\begin{tailnote}"
    local note_content = text:sub(note_start + 16, note_end - 1)

    -- Recursively expand any macros in the note
    note_content = expand_table_macros(note_content)
    note_content = trim(note_content)  -- trim whitespace

    -- Wrap in italic markers
    local replacement = "*" .. note_content .. "*"
    -- +15 for "\end{tailnote}"
    text = text:sub(1, note_start - 1) .. replacement .. text:sub(note_end + 15)
  end

  -- \br → <br> (line break within table cell)
  text = text:gsub("\\br{}", "<br>")
  text = text:gsub("\\br%s", "<br> ")
  text = text:gsub("\\br", "<br>")

  -- \oldconcept{X} → Cpp17X
  text = expand_balanced_command(text, "oldconcept", function(content)
    return "Cpp17" .. content
  end)

  -- Strip LaTeX table formatting commands that may leak into cells
  -- These can appear after \\ at end of rows: \\ \hline, \\ \cline{...}
  text = text:gsub("\\\\%s*\\hline[^a-zA-Z]*", "")  -- Remove \\ \hline
  text = text:gsub("\\\\%s*\\cline{[^}]*}", "")  -- Remove \\ \cline{...}
  text = text:gsub("\\\\%s*\\rowsep[^a-zA-Z]*", "")  -- Remove \\ \rowsep
  text = text:gsub("\\\\%s*", "")  -- Remove remaining bare \\

  -- Cross-reference macros - use shared function from cpp-common
  -- Track references and handle comma-separated refs: {a,b,c} → [[a]], [[b]], [[c]]
  local function process_refs(refs)
    return split_refs_text(refs, references)
  end

  text = text:gsub("\\ref{([^}]*)}", process_refs)
  text = text:gsub("\\iref{([^}]*)}", process_refs)
  text = text:gsub("\\tref{([^}]*)}", process_refs)

  return text
end

-- Helper function to extract table headers from table content
-- Tries multiple header styles in order: \hdstyle{}, then \lhdr{}/\chdr{}/\rhdr{}
-- Returns array of header strings with macros expanded
local function extract_table_headers(table_content)
  local headers = {}

  -- Try to find all headers in row using \hdstyle{} pattern
  local header_line = table_content:match("\\hdstyle{.-}.-\\\\ *\\capsep")
  if header_line then
    for hdr in header_line:gmatch("\\hdstyle{([^}]*)}") do
      table.insert(headers, expand_table_macros(hdr))
    end
  end

  -- If no \hdstyle, try \lhdr, \chdr, \rhdr combination
  if #headers == 0 then
    local lhdr_line = table_content:match("\\lhdr{.-}.-\\\\ *\\capsep")
    if lhdr_line then
      for hdr in lhdr_line:gmatch("\\lhdr{([^}]*)}") do
        table.insert(headers, expand_table_macros(hdr))
      end
      for hdr in lhdr_line:gmatch("\\chdr{([^}]*)}") do
        table.insert(headers, expand_table_macros(hdr))
      end
      for hdr in lhdr_line:gmatch("\\rhdr{([^}]*)}") do
        table.insert(headers, expand_table_macros(hdr))
      end
    end
  end

  return headers
end

-- Helper function to parse a table row (split by &)
local function parse_row(row_text)
  local cells = {}
  local current_cell = ""
  local depth = 0

  for i = 1, #row_text do
    local c = row_text:sub(i, i)

    if c == "{" then
      depth = depth + 1
      current_cell = current_cell .. c
    elseif c == "}" then
      depth = depth - 1
      current_cell = current_cell .. c
    elseif c == "&" and depth == 0 then
      -- End of cell
      table.insert(cells, trim(current_cell))
      current_cell = ""
    else
      current_cell = current_cell .. c
    end
  end

  -- Add last cell (even if empty - important for trailing empty columns)
  table.insert(cells, trim(current_cell))

  -- Expand macros in each cell
  for i, cell in ipairs(cells) do
    cells[i] = expand_table_macros(cell)
  end

  return cells
end

-- Helper function to normalize table row endings
-- Converts LaTeX row endings (\\ with various suffixes) to standard @@ROWEND@@
-- CRITICAL: Must be called BEFORE removing formatting commands like \rowsep
local function normalize_table_rows(text)
  -- Process patterns in order - more specific patterns first
  -- \\ \rowsep with newline
  local normalized = text:gsub("\\\\%s*\\rowsep%s*\n", "@@ROWEND@@\n")
  -- \\ \rowsep without immediate newline
  normalized = normalized:gsub("\\\\%s*\\rowsep", "@@ROWEND@@")
  normalized = normalized:gsub("\\\\%s*\\hline", "@@ROWEND@@")
  normalized = normalized:gsub("\\\\%s*\\cline{[^}]*}", "@@ROWEND@@")
  normalized = normalized:gsub("\\\\%s*\n", "@@ROWEND@@\n")  -- \\ with newline
  normalized = normalized:gsub("\\\\%s*$", "@@ROWEND@@")  -- bare \\ at end of text

  -- NOW remove any remaining formatting commands
  -- Note: Must also remove \topline and \capsep that may appear in the data section
  local cleaned = normalized:gsub("\\topline[^\n]*\n?", "")
  cleaned = cleaned:gsub("\\capsep[^\n]*\n?", "")
  cleaned = cleaned:gsub("\\rowsep[^\n]*\n?", "")
  return cleaned
end

-- Helper function to parse table rows from normalized text
-- Takes text with @@ROWEND@@ markers and returns array of row arrays
-- Filters out LaTeX formatting commands that may have leaked through
local function parse_table_rows(normalized_text)
  local rows = {}
  local row_num = 0
  for row_content in normalized_text:gmatch("([^@]+)@@ROWEND@@") do
    row_num = row_num + 1
    -- DEBUG: Add marker to see what rows were found
    -- io.stderr:write("[DEBUG] Row " .. row_num .. ": " .. row_content:sub(1, 50) .. "\n")

    -- Normalize whitespace (replace newlines with spaces)
    row_content = trim(row_content:gsub("%s+", " "))
    -- Safety net: skip rows with LaTeX formatting commands that slipped through
    if row_content ~= "" and
       not row_content:match("\\hline") and
       not row_content:match("\\cline") and
       not row_content:match("\\topline") and
       not row_content:match("\\capsep") and
       not row_content:match("\\lhdr") and
       not row_content:match("\\rhdr") and
       not row_content:match("\\hdstyle") and
       not row_content:match("\\continuedcaption") then
      local cells = parse_row(row_content)
      if #cells > 0 then
        table.insert(rows, cells)
      end
    end
  end
  return rows
end

-- Helper function to extract data section from table content
-- Tries multiple patterns to find where data rows start (after headers)
local function extract_data_section(table_content)
  -- Try after \endhead FIRST (used in LongTable - must come before \capsep check)
  local data_section = table_content:match("\\endhead[^\n]*\n(.*)")

  if not data_section then
    -- Try after \endfirsthead (used in LongTable)
    data_section = table_content:match("\\endfirsthead[^\n]*\n(.*)")
  end

  if not data_section then
    -- Try to find data after \capsep (common in most table types)
    data_section = table_content:match("\\capsep[^\n]*\n(.*)")
  end

  if not data_section then
    -- Try after \rhdr (floattable with no \capsep)
    data_section = table_content:match("\\rhdr{[^}]*}[^\n]*\\\\ *\\rowsep[^\n]*\n(.*)")
    if not data_section then
      data_section = table_content:match("\\rhdr{[^}]*}[^\n]*\\\\[^\n]*\n(.*)")
    end
  end

  if not data_section then
    -- Try after \topline (tables with no headers)
    data_section = table_content:match("\\topline[^\n]*\n(.*)")
  end

  if not data_section then
    -- Final fallback: take everything
    data_section = table_content
  end

  return data_section
end

-- Memoization cache for string width calculations (20-30% performance gain)
local width_cache = {}

-- Calculate raw string width for markdown source alignment
-- Counts all characters including markdown syntax (backticks, brackets, etc.)
-- For pretty-printing markdown source, we want alignment based on what you see in a text editor
local function string_width(str)
  if not str or str == "" then
    return 0
  end

  -- Check cache first
  local cached = width_cache[str]
  if cached then
    return cached
  end

  -- Count UTF-8 characters (not bytes), including all markdown syntax
  -- This pattern matches UTF-8 character boundaries
  local count = 0
  for _ in str:gmatch("[%z\1-\127\194-\244][\128-\191]*") do
    count = count + 1
  end

  -- Cache the result
  width_cache[str] = count
  return count
end

-- Calculate maximum width for each column
local function calculate_column_widths(headers, rows)
  local widths = {}
  local num_cols = #headers

  -- Initialize with header widths
  for i, header in ipairs(headers) do
    widths[i] = string_width(header)
  end

  -- Update with row data widths
  -- Skip malformed rows that don't have the expected number of columns
  for _, row in ipairs(rows) do
    if #row == num_cols then  -- Only process rows with correct column count
      for i, cell in ipairs(row) do
        local width = string_width(cell)
        if not widths[i] or width > widths[i] then
          widths[i] = width
        end
      end
    end
  end

  return widths
end

-- Pad a cell to the specified width with trailing spaces
local function pad_cell(cell, width)
  if not cell then
    cell = ""
  end

  local current_width = string_width(cell)
  local padding_needed = width - current_width

  if padding_needed > 0 then
    return cell .. string.rep(" ", padding_needed)
  end

  return cell
end

-- Helper function to build markdown table from structured data
-- This is the single source of truth for table formatting (DRY principle)
local function build_markdown_table(caption, headers, rows)
  local md_lines = {}

  -- Add caption as heading
  table.insert(md_lines, "**Table: " .. caption .. "**\n")

  -- If no headers provided but we have rows, generate empty headers based on column count
  -- This ensures valid markdown table structure
  if #headers == 0 and #rows > 0 and #rows[1] > 0 then
    for i = 1, #rows[1] do
      table.insert(headers, "")
    end
  end

  -- Calculate column widths for alignment
  local col_widths = calculate_column_widths(headers, rows)

  -- Enforce minimum width of 3 for all columns (markdown requires at least --- in separator)
  for i = 1, #col_widths do
    col_widths[i] = math.max(col_widths[i], 3)
  end

  -- Add header row and separator (required for valid markdown tables)
  if #headers > 0 then
    -- Build padded header row
    local padded_headers = {}
    for i, header in ipairs(headers) do
      table.insert(padded_headers, pad_cell(header, col_widths[i]))
    end
    table.insert(md_lines, "| " .. table.concat(padded_headers, " | ") .. " |")

    -- Add separator row with dashes matching column widths
    local sep = {}
    for i = 1, #headers do
      table.insert(sep, string.rep("-", col_widths[i]))
    end
    table.insert(md_lines, "| " .. table.concat(sep, " | ") .. " |")
  end

  -- Add data rows with padding
  for _, row in ipairs(rows) do
    local padded_row = {}
    for i, cell in ipairs(row) do
      table.insert(padded_row, pad_cell(cell, col_widths[i] or 3))
    end
    table.insert(md_lines, "| " .. table.concat(padded_row, " | ") .. " |")
  end

  -- Add trailing blank line to separate table from following content
  return table.concat(md_lines, "\n") .. "\n\n"
end

-- Generic handler for "libeff family" table types
-- These table types share a common structure: {caption}{label}[optional args]
-- with implicit or partially implicit headers (first column is always "Element")
--
-- Parameters:
--   text: Raw LaTeX text containing the table environment
--   env_name: Name of the environment (e.g., "libefftabmean", "LibEffTab")
--   header_config: Array of header strings. Use nil to extract from arguments.
--                  Examples: {"Element", "Meaning"} - both fixed
--                           {"Element", nil} - second extracted from arg 3
--   skip_args: Number of additional arguments to skip after headers (e.g., width specs)
--
-- Returns: pandoc.RawBlock with markdown table, or nil if parsing fails
local function handle_libeff_family_table(text, env_name, header_config, skip_args)
  skip_args = skip_args or 0  -- default to 0 if not provided

  local begin_tag = "\\begin{" .. env_name .. "}"
  local end_tag = "\\end{" .. env_name .. "}"

  local env_start = text:find(begin_tag, 1, true)
  if not env_start then
    return nil
  end

  -- Extract caption (first braced argument)
  local caption_start = env_start + #begin_tag
  local caption, pos1 = extract_braced(text, caption_start)

  -- Extract label (second braced argument)
  local label, pos2 = extract_braced(text, pos1)

  if not caption or not label then
    return nil
  end

  -- Extract additional arguments if needed (for headers with nil placeholders)
  local extracted_headers = {}
  local current_pos = pos2
  for _, hdr in ipairs(header_config) do
    if hdr == nil then
      -- Extract this header from next argument
      local extracted, next_pos = extract_braced(text, current_pos)
      if not extracted then
        return nil
      end
      table.insert(extracted_headers, expand_table_macros(extracted))
      current_pos = next_pos
    else
      -- Use fixed header
      table.insert(extracted_headers, hdr)
    end
  end

  -- Skip additional arguments (e.g., width specifications)
  for i = 1, skip_args do
    local _, next_pos = extract_braced(text, current_pos)
    if not next_pos then
      return nil
    end
    current_pos = next_pos
  end

  -- Find the end of environment
  local env_end = text:find(end_tag, current_pos, true)
  if not env_end then
    return nil
  end

  -- Extract table content
  local table_content = text:sub(current_pos + 1, env_end - 1)

  -- Parse caption (may contain macros)
  caption = expand_table_macros(caption)

  -- Extract data rows (handle multi-line rows)
  local normalized = normalize_table_rows(table_content)
  local rows = parse_table_rows(normalized)

  -- Generate markdown table using shared helper
  local markdown = build_markdown_table(caption, extracted_headers, rows)
  return pandoc.RawBlock('markdown', markdown)
end

-- Main filter function for raw blocks
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Handle floattable environment
  local float_start = text:find("\\begin{floattable}", 1, true)
  if float_start then
    -- Extract caption (first braced argument)
    local caption_start = float_start + ENV_BEGIN_LEN.floattable
    local caption, pos = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, end_pos = extract_braced(text, pos)

    if caption and label then
      -- Find the end of floattable
      local float_end = text:find("\\end{floattable}", end_pos, true)
      if float_end then
        local table_content = text:sub(end_pos + 1, float_end - 1)

        -- Parse caption (may contain macros)
        caption = expand_table_macros(caption)

        -- Extract header row (supports multiple columns and column-spanning headers)
        local headers = {}

        -- Try to find header line (ends with \\ and followed by \capsep)
        -- Must handle multiline headers where \lhdr{Name} & \rhdr{Meaning} spans lines
        local header_line = table_content:match("(.-\\\\)%s*\\capsep")

        if header_line then
          -- Parse headers by scanning for \lhdrx, \lhdr, \chdr, \rhdr, \hdstyle macros
          -- \lhdrx{N}{text} creates N columns with text in first
          -- Other macros create single columns

          local header_pos = 1
          while header_pos <= #header_line do
            -- Check for \lhdrx{N}{text} - column-spanning header
            local lhdrx_start = header_line:find("\\lhdrx{", header_pos, true)
            if lhdrx_start and lhdrx_start == header_pos then
              -- Extract span count - point to the '{' character
              -- "\lhdrx" is 6 chars, so '{' is at lhdrx_start + 6
              local span_count, pos1 = extract_braced(header_line, lhdrx_start + 6)
              if span_count and pos1 then
                -- Extract header text - pos1 points after first '}', look for next '{'
                local header_text, pos2 = extract_braced(header_line, pos1)
                if header_text then
                  header_text = expand_table_macros(header_text)
                  -- Add first column with text, remaining columns empty
                  table.insert(headers, header_text)
                  for i = 2, tonumber(span_count) or 1 do
                    table.insert(headers, "")
                  end
                  header_pos = pos2
                  goto continue
                end
              end
            end

            -- Check for \lhdr{text}
            local lhdr_start = header_line:find("\\lhdr{", header_pos, true)
            if lhdr_start and lhdr_start == header_pos then
              -- "\lhdr" is 5 chars, so '{' is at lhdr_start + 5
              local lhdr_match, lhdr_end_pos = extract_braced(header_line, lhdr_start + 5)
              if lhdr_match then
                table.insert(headers, expand_table_macros(lhdr_match))
                header_pos = lhdr_end_pos
                goto continue
              end
            end

            -- Check for \chdr{text}
            local chdr_start = header_line:find("\\chdr{", header_pos, true)
            if chdr_start and chdr_start == header_pos then
              -- "\chdr" is 5 chars, so '{' is at chdr_start + 5
              local chdr_match, chdr_end_pos = extract_braced(header_line, chdr_start + 5)
              if chdr_match then
                table.insert(headers, expand_table_macros(chdr_match))
                header_pos = chdr_end_pos
                goto continue
              end
            end

            -- Check for \rhdr{text}
            local rhdr_start = header_line:find("\\rhdr{", header_pos, true)
            if rhdr_start and rhdr_start == header_pos then
              -- "\rhdr" is 5 chars, so '{' is at rhdr_start + 5
              local rhdr_match, rhdr_end_pos = extract_braced(header_line, rhdr_start + 5)
              if rhdr_match then
                table.insert(headers, expand_table_macros(rhdr_match))
                header_pos = rhdr_end_pos
                goto continue
              end
            end

            -- Check for \hdstyle{text}
            local hdstyle_start = header_line:find("\\hdstyle{", header_pos, true)
            if hdstyle_start and hdstyle_start == header_pos then
              -- "\hdstyle" is 8 chars, so '{' is at hdstyle_start + 8
              local hdstyle_match, hdstyle_end_pos = extract_braced(header_line, hdstyle_start + 8)
              if hdstyle_match then
                table.insert(headers, expand_table_macros(hdstyle_match))
                header_pos = hdstyle_end_pos
                goto continue
              end
            end

            -- Skip other characters (whitespace, &, etc.)
            header_pos = header_pos + 1
            ::continue::
          end
        end

        -- Fallback: if no headers found, try old 2-column pattern
        if #headers == 0 then
          local h1, h2 = table_content:match("\\hdstyle{([^}]*)}%s*&%s*\\hdstyle{([^}]*)}")
          if h1 and h2 then
            headers = {expand_table_macros(h1), expand_table_macros(h2)}
          else
            h1, h2 = table_content:match(
              "\\lhdr{([^}]*)}%s*&%s*\\rhdr{([^}]*)}")
            if h1 and h2 then
              headers = {expand_table_macros(h1),
                         expand_table_macros(h2)}
            end
          end
        end

        -- Final fallback: handle multi-row headers with \multicolumn and
        -- plain \tcode{} content. Example: "File open modes" table
        -- Row 1: \multicolumn{6}{|c}{\tcode{ios_base} flag combination} &
        --        \tcode{stdio} equivalent \\
        -- Row 2: \tcode{binary} & \tcode{in} & \tcode{out} & \tcode{trunc} &
        --        \tcode{app} & \tcode{noreplace} \\ \capsep
        if #headers == 0 and header_line and
           header_line:find("\\multicolumn{", 1, true) then
          -- Extract the header from the row after \multicolumn
          -- Get part after \multicolumn{...}{...}{...} from first row
          -- (may have extra column header)
          local remaining_first_row =
            header_line:match("\\multicolumn{.-}{.-}{.-}%s*&%s*(.-)%s*\\\\")

          -- Get the second row before \\ \capsep (actual column headers)
          local second_row = header_line:match("\n([^\n]*)\\\\%s*$")

          if second_row and second_row ~= "" then
            -- Parse second row to get main column headers
            headers = parse_row(second_row)

            -- If there's a remaining header from first row, append it
            if remaining_first_row and remaining_first_row ~= "" then
              local extra_header = expand_table_macros(remaining_first_row)
              table.insert(headers, extra_header)
            end
          end
        end

        -- Extract data rows (handle multi-line rows)
        local data_section = extract_data_section(table_content)
        local normalized = normalize_table_rows(data_section)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table using shared helper (DRY)
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle libsumtab environment (library summary tables)
  local libsum_start = text:find("\\begin{libsumtab}", 1, true)
  if libsum_start then
    -- Extract caption (first braced argument)
    local caption_start = libsum_start + ENV_BEGIN_LEN.libsumtab
    local caption, pos = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, end_pos = extract_braced(text, pos)

    if caption and label then
      -- Find the end of libsumtab
      local libsum_end = text:find("\\end{libsumtab}", end_pos, true)
      if libsum_end then
        local table_content = text:sub(end_pos + 1, libsum_end - 1)

        -- Parse caption (may contain macros)
        caption = expand_table_macros(caption)

        -- libsumtab has implicit headers: Subclause | (Description) | Header
        local headers = {"Subclause", "", "Header"}

        -- Extract data rows (handle multi-line rows)
        -- Note: libsumtab doesn't use extract_data_section() - it processes the whole content
        local normalized = normalize_table_rows(table_content)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table using shared helper
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle lib2dtab2 environment (2D comparison tables with row headers)
  local lib2dtab2_start = text:find("\\begin{lib2dtab2}", 1, true)
  if lib2dtab2_start then
    -- Extract caption (first braced argument)
    local caption_start = lib2dtab2_start + ENV_BEGIN_LEN.lib2dtab2
    local caption, pos1 = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, pos2 = extract_braced(text, pos1)

    -- Extract column 1 header (third braced argument)
    local col1_header, pos3 = extract_braced(text, pos2)

    -- Extract column 2 header (fourth braced argument)
    local col2_header, end_pos = extract_braced(text, pos3)

    if caption and label and col1_header and col2_header then
      -- Find the end of lib2dtab2
      local lib2dtab2_end = text:find("\\end{lib2dtab2}", end_pos, true)
      if lib2dtab2_end then
        local table_content = text:sub(end_pos + 1, lib2dtab2_end - 1)

        -- Parse caption and headers (may contain macros)
        caption = expand_table_macros(caption)
        col1_header = expand_table_macros(col1_header)
        col2_header = expand_table_macros(col2_header)

        -- Headers: row header column + 2 data columns
        local headers = {"", col1_header, col2_header}

        -- Parse rows - lib2dtab2 uses \rowhdr{} for row headers and \rowsep for separators
        local rows = {}

        -- Normalize line breaks (converts \\ to @@ROWEND@@ and removes \rowsep)
        local normalized = normalize_table_rows(table_content)

        -- Parse each row (split on @@ROWEND@@ markers)
        for row_content in normalized:gmatch("([^@]+)@@ROWEND@@") do
          -- Normalize whitespace (replace newlines with spaces)
          row_content = row_content:gsub("%s+", " ")
          local trimmed = row_content:match("^%s*(.-)%s*$")

          if trimmed and #trimmed > 0 then
            -- Check if this row starts with \rowhdr{}
            local rowhdr_start = trimmed:find("\\rowhdr{", 1, true)
            if rowhdr_start == 1 then
              -- Use extract_braced to handle nested braces correctly
              -- +7 for "\rowhdr"
              local row_header, row_end_pos = extract_braced(trimmed, rowhdr_start + 7)
              if row_header then
                row_header = expand_table_macros(row_header)

                -- Extract the remaining cells (after \rowhdr{...})
                -- Skip leading whitespace and the first & separator
                local rest = trimmed:sub(row_end_pos + 1)
                rest = rest:match("^%s*&?%s*(.*)$") or rest

                -- Parse the remaining cells using parse_row helper (handles & separators)
                local cells = parse_row(rest)

                -- Build row: row header + cells
                local row = {row_header}
                for _, cell in ipairs(cells) do
                  table.insert(row, cell)
                end

                table.insert(rows, row)
              end
            end
          end
        end

        -- Generate markdown table using shared helper
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle libtab2 environment (simple 2-column tables)
  local libtab2_start = text:find("\\begin{libtab2}", 1, true)
  if libtab2_start then
    -- Extract caption (first braced argument)
    local caption_start = libtab2_start + ENV_BEGIN_LEN.libtab2
    local caption, pos1 = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, pos2 = extract_braced(text, pos1)

    -- Extract column spec (third braced argument) - we don't use this, just skip it
    local colspec, pos3 = extract_braced(text, pos2)

    -- Extract header 1 (fourth braced argument)
    local header1, pos4 = extract_braced(text, pos3)

    -- Extract header 2 (fifth braced argument)
    local header2, end_pos = extract_braced(text, pos4)

    if caption and label and header1 and header2 then
      -- Find the end of libtab2
      local libtab2_end = text:find("\\end{libtab2}", end_pos, true)
      if libtab2_end then
        local table_content = text:sub(end_pos + 1, libtab2_end - 1)

        -- Parse caption and headers (may contain macros)
        caption = expand_table_macros(caption)
        header1 = expand_table_macros(header1)
        header2 = expand_table_macros(header2)

        -- Headers
        local headers = {header1, header2}

        -- Extract data rows (simple 2-column format)
        local normalized = normalize_table_rows(table_content)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table using shared helper
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle libefftab environment (enum/bitmask effects tables)
  local libefftab_start = text:find("\\begin{libefftab}", 1, true)
  if libefftab_start then
    -- Extract caption (first braced argument)
    local caption_start = libefftab_start + ENV_BEGIN_LEN.libefftab
    local caption, pos1 = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, end_pos = extract_braced(text, pos1)

    if caption and label then
      -- Find the end of libefftab
      local libefftab_end = text:find("\\end{libefftab}", end_pos, true)
      if libefftab_end then
        local table_content = text:sub(end_pos + 1, libefftab_end - 1)

        -- Parse caption (may contain macros)
        caption = expand_table_macros(caption)

        -- Implicit headers for effects tables
        local headers = {"Element", "Effect(s) if set"}

        -- Extract data rows (handle multi-line rows)
        local normalized = normalize_table_rows(table_content)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table using shared helper
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle longlibefftab environment (long enum/bitmask effects tables)
  local longlibefftab_start = text:find("\\begin{longlibefftab}", 1, true)
  if longlibefftab_start then
    -- Extract caption (first braced argument)
    local caption_start = longlibefftab_start + ENV_BEGIN_LEN.longlibefftab
    local caption, pos1 = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, end_pos = extract_braced(text, pos1)

    if caption and label then
      -- Find the end of longlibefftab
      local longlibefftab_end = text:find("\\end{longlibefftab}", end_pos, true)
      if longlibefftab_end then
        local table_content = text:sub(end_pos + 1, longlibefftab_end - 1)

        -- Parse caption (may contain macros)
        caption = expand_table_macros(caption)

        -- Implicit headers for effects tables
        local headers = {"Element", "Effect(s) if set"}

        -- Extract data rows (handle multi-line rows)
        local normalized = normalize_table_rows(table_content)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table using shared helper
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle longliberrtab environment (error value tables)
  local longliberrtab_start = text:find("\\begin{longliberrtab}", 1, true)
  if longliberrtab_start then
    -- Extract caption (first braced argument)
    local caption_start = longliberrtab_start + ENV_BEGIN_LEN.longliberrtab
    local caption, pos1 = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, end_pos = extract_braced(text, pos1)

    if caption and label then
      -- Find the end of longliberrtab
      local longliberrtab_end = text:find("\\end{longliberrtab}", end_pos, true)
      if longliberrtab_end then
        local table_content = text:sub(end_pos + 1, longliberrtab_end - 1)

        -- Parse caption (may contain macros)
        caption = expand_table_macros(caption)

        -- Implicit headers for error tables
        local headers = {"Value", "Error condition"}

        -- Extract data rows (handle multi-line rows)
        local normalized = normalize_table_rows(table_content)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table using shared helper
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle libefftabmean environment (enum/bitmask "meaning" tables)
  -- Arguments: {caption}{label}
  -- Uses generic handler with fixed headers
  local result = handle_libeff_family_table(text, "libefftabmean", {"Element", "Meaning"})
  if result then return result end

  -- Handle libefftabvalue environment (enum/bitmask "value" tables)
  -- Arguments: {caption}{label}
  -- Uses generic handler with fixed headers
  result = handle_libeff_family_table(text, "libefftabvalue", {"Element", "Value"})
  if result then return result end

  -- Handle LibEffTab environment (generic effects table with custom second header)
  -- Arguments: {caption}{label}{header2}{width2}
  -- Headers: Element (fixed) + header2 (extracted from arg 3)
  -- Skip: width2 (arg 4)
  result = handle_libeff_family_table(text, "LibEffTab", {"Element", nil}, 1)
  if result then return result end

  -- Handle longlibefftabvalue environment (long enum/bitmask "value" tables)
  -- Arguments: {caption}{label}
  -- Uses generic handler with fixed headers
  result = handle_libeff_family_table(text, "longlibefftabvalue", {"Element", "Value"})
  if result then return result end

  -- Handle longLibEffTab environment (long generic effects table with custom second header)
  -- Arguments: {caption}{label}{header2}{width2}
  -- Headers: Element (fixed) + header2 (extracted from arg 3)
  -- Skip: width2 (arg 4)
  result = handle_libeff_family_table(text, "longLibEffTab", {"Element", nil}, 1)
  if result then return result end

  -- Handle LongTable environment
  local long_start = text:find("\\begin{LongTable}", 1, true)
  if long_start then
    -- Extract caption (first braced argument)
    local caption_start = long_start + ENV_BEGIN_LEN.LongTable
    local caption, pos1 = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, pos2 = extract_braced(text, pos1)

    -- Extract colspec (third braced argument)
    local colspec, end_pos = extract_braced(text, pos2)

    if caption and label and colspec then
      -- Find the end of LongTable
      local long_end = text:find("\\end{LongTable}", end_pos, true)
      if long_end then
        local table_content = text:sub(end_pos + 1, long_end - 1)

        -- Parse caption (may contain macros)
        caption = expand_table_macros(caption)

        -- Extract header from first head section (between \topline and \endfirsthead)
        local first_head = table_content:match("\\topline(.-)\\endfirsthead")
        local headers = {}
        if first_head then
          local h1, h2 = first_head:match("\\lhdr{([^}]*)}%s*&%s*\\rhdr{([^}]*)}")
          if h1 and h2 then
            headers = {expand_table_macros(h1), expand_table_macros(h2)}
          end
        end

        -- Extract data rows (after \endhead) - handle multi-line rows
        local data_section = extract_data_section(table_content)
        local normalized = normalize_table_rows(data_section)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table using shared helper (DRY)
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle concepttable environment (C++20 concept requirements tables)
  local concept_start = text:find("\\begin{concepttable}", 1, true)
  if concept_start then
    -- Extract caption (first braced argument)
    local caption_start = concept_start + ENV_BEGIN_LEN.concepttable
    local caption, pos1 = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, pos2 = extract_braced(text, pos1)

    -- Extract colspec (third braced argument)
    local colspec, end_pos = extract_braced(text, pos2)

    if caption and label and colspec then
      -- Find the end of concepttable
      local concept_end = text:find("\\end{concepttable}", end_pos, true)
      if concept_end then
        local table_content = text:sub(end_pos + 1, concept_end - 1)

        -- Parse caption (may contain macros)
        caption = expand_table_macros(caption)

        -- Extract header row using shared helper
        local headers = extract_table_headers(table_content)

        -- Extract data rows (after \capsep)
        local data_section = extract_data_section(table_content)
        local normalized = normalize_table_rows(data_section)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle simpletypetable environment
  local simple_start = text:find("\\begin{simpletypetable}", 1, true)
  if simple_start then
    -- Extract caption (first braced argument)
    local caption_start = simple_start + ENV_BEGIN_LEN.simpletypetable
    local caption, pos1 = extract_braced(text, caption_start)

    -- Extract label (second braced argument)
    local label, pos2 = extract_braced(text, pos1)

    -- Extract colspec (third braced argument)
    local colspec, end_pos = extract_braced(text, pos2)

    if caption and label and colspec then
      -- Find the end of simpletypetable
      local simple_end = text:find("\\end{simpletypetable}", end_pos, true)
      if simple_end then
        local table_content = text:sub(end_pos + 1, simple_end - 1)

        -- Parse caption (may contain macros)
        caption = expand_table_macros(caption)

        -- Extract header row using shared helper
        local headers = extract_table_headers(table_content)

        -- Extract data rows (after \capsep)
        local data_section = extract_data_section(table_content)
        local normalized = normalize_table_rows(data_section)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  -- Handle oldconcepttable environment (Cpp17* requirements tables)
  local oldconcept_start = text:find("\\begin{oldconcepttable}", 1, true)
  if oldconcept_start then
    -- Extract name (first braced argument) - e.g., "EqualityComparable"
    local name_start = oldconcept_start + ENV_BEGIN_LEN.oldconcepttable
    local name, pos1 = extract_braced(text, name_start)

    -- Extract extra (second braced argument) - e.g., "" or " (in addition to ...)"
    local extra, pos2 = extract_braced(text, pos1)

    -- Extract label (third braced argument) - e.g., "cpp17.equalitycomparable"
    local label, pos3 = extract_braced(text, pos2)

    -- Extract colspec (fourth braced argument) - e.g., "x{1in}x{1in}p{3in}"
    local colspec, end_pos = extract_braced(text, pos3)

    if name and extra and label and colspec then
      -- Find the end of oldconcepttable
      local oldconcept_end = text:find("\\end{oldconcepttable}", end_pos, true)
      if oldconcept_end then
        local table_content = text:sub(end_pos + 1, oldconcept_end - 1)

        -- Generate caption: "Cpp17{NAME} requirements{EXTRA}"
        local caption = "Cpp17" .. name .. " requirements" .. extra

        -- Parse caption to expand any macros in EXTRA (like \oldconcept{...})
        caption = expand_table_macros(caption)

        -- Extract header row using shared helper
        local headers = extract_table_headers(table_content)

        -- Extract data rows (after \capsep)
        local data_section = extract_data_section(table_content)
        local normalized = normalize_table_rows(data_section)
        local rows = parse_table_rows(normalized)

        -- Generate markdown table using shared helper (DRY)
        local markdown = build_markdown_table(caption, headers, rows)
        return pandoc.RawBlock('markdown', markdown)
      end
    end
  end

  return elem
end

-- Add link reference definitions at end of document
-- This function runs after all RawBlock processing is complete
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

    -- Add each link definition
    for _, ref in ipairs(refs) do
      local link_def = pandoc.RawBlock('markdown', '[' .. ref .. ']: #' .. ref)
      table.insert(doc.blocks, link_def)
    end
  end

  return doc
end
