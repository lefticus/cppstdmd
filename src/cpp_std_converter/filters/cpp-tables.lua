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
local trim = common.trim
local extract_braced = common.extract_braced
local extract_multi_arg_macro = common.extract_multi_arg_macro
local split_refs_text = common.split_refs_text
local expand_text_macros = common.expand_text_macros

-- Initialize references table if not already created by cpp-macros.lua
-- This allows cpp-tables.lua to work standalone or as part of filter chain
if not references then
  references = {}
end

-- Table type configuration registry (data-driven dispatch)
-- Key: environment name
-- Values:
--   num_args: Number of braced arguments after \begin{envname}
--   headers: Fixed headers array, OR "parse" to extract from content, OR indices into args
--   header_parser: Optional custom header parser function name (string)
--   data_section: "extract" (use extract_data_section) or "full" (use entire content)
--   caption_builder: Optional function to build caption from args
--   row_parser: Optional special row parser name (string)
--   label_arg: Which arg contains the label (default: 2)
local TABLE_CONFIGS = {
  -- Simple 2-arg tables with fixed headers
  libsumtab = {
    num_args = 2,
    headers = {"Subclause", "", "Header"},
    data_section = "full",
  },
  libefftab = {
    num_args = 2,
    headers = {"Element", "Effect(s) if set"},
    data_section = "full",
  },
  longlibefftab = {
    num_args = 2,
    headers = {"Element", "Effect(s) if set"},
    data_section = "full",
  },
  longliberrtab = {
    num_args = 2,
    headers = {"Value", "Error condition"},
    data_section = "full",
  },
  libefftabmean = {
    num_args = 2,
    headers = {"Element", "Meaning"},
    data_section = "full",
  },
  libefftabvalue = {
    num_args = 2,
    headers = {"Element", "Value"},
    data_section = "full",
  },
  longlibefftabvalue = {
    num_args = 2,
    headers = {"Element", "Value"},
    data_section = "full",
  },

  -- 3-arg tables with parsed headers
  floattable = {
    num_args = 3,
    headers = "parse",
    header_parser = "parse_floattable_headers",
    data_section = "extract",
  },
  LongTable = {
    num_args = 3,
    headers = "parse_longtable",
    data_section = "extract",
  },
  concepttable = {
    num_args = 3,
    headers = "parse",
    data_section = "extract",
  },
  simpletypetable = {
    num_args = 3,
    headers = "parse",
    data_section = "extract",
  },

  -- 4-arg tables with headers from args
  lib2dtab2 = {
    num_args = 4,
    headers = {"", 3, 4},  -- "" = empty, 3/4 = arg indices
    row_parser = "lib2dtab2",
    data_section = "full",
  },
  LibEffTab = {
    num_args = 4,
    headers = {"Element", 3},  -- "Element" fixed, arg 3 for second header
    data_section = "full",
  },
  longLibEffTab = {
    num_args = 4,
    headers = {"Element", 3},
    data_section = "full",
  },

  -- 5-arg tables
  libtab2 = {
    num_args = 5,
    headers = {4, 5},  -- Headers from args 4 and 5
    data_section = "full",
  },

  -- Special: oldconcepttable has custom caption builder
  oldconcepttable = {
    num_args = 4,
    caption_builder = function(args)
      return "Cpp17" .. args[1] .. " requirements" .. args[2]
    end,
    headers = "parse",
    data_section = "extract",
    label_arg = 3,  -- Label is 3rd arg for oldconcepttable
  },
}

-- Helper function to expand common macros in table cells
-- Uses shared expand_text_macros() for common macros, then handles table-specific ones
local function expand_table_macros(text)
  if not text then return text end

  -- Use shared function for common macros (keyword, textbf, tcode, xname, etc.)
  text = expand_text_macros(text, {references_table = references})

  -- === TABLE-SPECIFIC HANDLING BELOW ===

  -- \multicolumn{N}{alignment}{content} → content
  -- Markdown doesn't support column spans, so just extract the content
  while true do
    local start_pos = text:find("\\multicolumn{", 1, true)
    if not start_pos then break end

    -- Extract first argument (number of columns to span)
    -- "\\multicolumn{" is 12 chars total, so first { after it is at start_pos + 12
    local num_cols, pos1 = extract_braced(text, start_pos + 12)
    if not num_cols then
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
    local replacement = "*[spans " .. num_cols .. " columns]* " .. content
    text = text:sub(1, start_pos - 1) .. replacement .. text:sub(pos3)
  end

  -- \begin{itemize} ... \end{itemize} → semicolon-separated list
  while true do
    local itemize_start = text:find("\\begin{itemize}", 1, true)
    if not itemize_start then break end

    local itemize_end = text:find("\\end{itemize}", itemize_start, true)
    if not itemize_end then break end

    local list_content = text:sub(itemize_start + 15, itemize_end - 1)

    -- Split on \item and collect items
    local items = {}
    for item in list_content:gmatch("\\item%s*([^\\]*)") do
      item = trim(item)
      if item ~= "" then
        item = expand_table_macros(item)
        table.insert(items, item)
      end
    end

    local replacement = table.concat(items, "; ")
    text = text:sub(1, itemize_start - 1) .. replacement .. text:sub(itemize_end + 14)
  end

  -- \begin{tailnote} ... \end{tailnote} → italic text
  while true do
    local note_start = text:find("\\begin{tailnote}", 1, true)
    if not note_start then break end

    local note_end = text:find("\\end{tailnote}", note_start, true)
    if not note_end then break end

    local note_content = text:sub(note_start + 16, note_end - 1)
    note_content = expand_table_macros(note_content)
    note_content = trim(note_content)

    local replacement = "*" .. note_content .. "*"
    text = text:sub(1, note_start - 1) .. replacement .. text:sub(note_end + 15)
  end

  -- Strip LaTeX table formatting commands that may leak into cells
  text = text:gsub("\\\\%s*\\hline[^a-zA-Z]*", "")
  text = text:gsub("\\\\%s*\\cline{[^}]*}", "")
  text = text:gsub("\\\\%s*\\rowsep[^a-zA-Z]*", "")
  text = text:gsub("\\\\%s*", "")

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

-- Memoization cache for string width calculations
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

-- Split string on & respecting brace depth
-- Used for parsing table header lines into columns
local function split_on_ampersand(text)
  local parts = {}
  local current = ""
  local depth = 0

  for i = 1, #text do
    local c = text:sub(i, i)
    if c == "{" then
      depth = depth + 1
      current = current .. c
    elseif c == "}" then
      depth = depth - 1
      current = current .. c
    elseif c == "&" and depth == 0 then
      table.insert(parts, current)
      current = ""
    else
      current = current .. c
    end
  end

  if current ~= "" then
    table.insert(parts, current)
  end

  return parts
end

-- Extract header text from a column that may contain header macros
-- Returns the header content, with macros stripped/expanded
-- Uses extract_braced for proper nested brace handling (e.g., \chdr{\tcode{float16_t}})
local function extract_header_from_column(col)
  col = trim(col)
  -- Strip trailing \\ if present
  col = col:gsub("\\\\%s*$", "")
  col = trim(col)

  -- Check for \lhdrx{N}{text} - column-spanning header
  -- This is special: returns the text AND the span count
  local lhdrx_pos = col:find("\\lhdrx{", 1, true)
  if lhdrx_pos then
    -- Extract span count from first braced argument
    -- \lhdrx is 6 chars, { is at position 7, so offset is +6
    local span_str, pos_after_span = extract_braced(col, lhdrx_pos + 6)
    if span_str then
      local span_count = tonumber(span_str)
      -- Extract header text from second braced argument
      local header_text, _ = extract_braced(col, pos_after_span)
      if header_text and span_count then
        return header_text, span_count
      end
    end
  end

  -- Check for \lhdr{text}, \chdr{text}, \rhdr{text}, \hdstyle{text}
  -- Using extract_braced for proper nested brace handling
  -- len is position offset to the opening brace (without the '{' itself)
  local header_macros = {
    { pattern = "\\lhdr{", len = 5 },   -- \lhdr is 5 chars, { is at +6
    { pattern = "\\chdr{", len = 5 },   -- \chdr is 5 chars, { is at +6
    { pattern = "\\rhdr{", len = 5 },   -- \rhdr is 5 chars, { is at +6
    { pattern = "\\hdstyle{", len = 8 }, -- \hdstyle is 8 chars, { is at +9
  }

  for _, macro in ipairs(header_macros) do
    local macro_pos = col:find(macro.pattern, 1, true)
    if macro_pos then
      local header_text, _ = extract_braced(col, macro_pos + macro.len)
      if header_text then
        return header_text, 1
      end
    end
  end

  -- Fallback: use column content as-is (handles plain text headers)
  return col, 1
end

-- Check if a row contains actual column headers (not just group headers)
-- Returns true if the row has \lhdr, \chdr, \rhdr, or \hdstyle
-- Returns false if row only has \ohdrx (spanning group header)
local function row_has_column_headers(row)
  return row:find("\\lhdr", 1, true) or
         row:find("\\chdr", 1, true) or
         row:find("\\rhdr", 1, true) or
         row:find("\\hdstyle", 1, true)
end

-- Parse multi-row headers (e.g., stacked headers with sub-labels)
-- Merges text from multiple header rows vertically by column position
-- Example:
--   \lhdr{Name} & \chdr{Value} & \chdr{POSIX} & \rhdr{Definition} \\
--               & \chdr{(octal)} & \chdr{macro} &                  \\ \capsep
-- Produces: ["Name", "Value (octal)", "POSIX macro", "Definition"]
--
-- Note: Rows containing only \ohdrx (group headers) are skipped - these are
-- spanning rows used for grouping, not column headers.
local function parse_multirow_headers(header_block)
  -- Split on \\ to get individual rows
  -- Pattern matches content before each \\
  local rows = {}
  local pos = 1
  while pos <= #header_block do
    -- Find next \\ (which is \\\\ in Lua pattern)
    local row_end = header_block:find("\\\\", pos, true)
    if row_end then
      local row = header_block:sub(pos, row_end - 1)
      row = trim(row)
      if row ~= "" then
        table.insert(rows, row)
      end
      pos = row_end + 2  -- Skip past \\
    else
      -- No more \\, take the rest
      local row = header_block:sub(pos)
      row = trim(row)
      if row ~= "" then
        table.insert(rows, row)
      end
      break
    end
  end

  if #rows == 0 then return {} end

  -- Filter out rows that only contain \ohdrx (group headers, not column headers)
  -- These are spanning rows like "\ohdrx{2}{Option group...}" used for grouping
  local column_header_rows = {}
  for _, row in ipairs(rows) do
    if row_has_column_headers(row) then
      table.insert(column_header_rows, row)
    end
  end

  -- If after filtering we have no column header rows, fall back to using all rows
  if #column_header_rows == 0 then
    column_header_rows = rows
  end

  -- Parse each row into columns
  local row_columns = {}
  local max_cols = 0
  for _, row in ipairs(column_header_rows) do
    local cols = split_on_ampersand(row)
    table.insert(row_columns, cols)
    max_cols = math.max(max_cols, #cols)
  end

  -- Merge columns vertically
  local headers = {}
  for col_idx = 1, max_cols do
    local merged = {}
    for _, cols in ipairs(row_columns) do
      local cell = cols[col_idx] or ""
      local text, _ = extract_header_from_column(cell)
      text = expand_table_macros(text)
      text = trim(text)
      if text ~= "" then
        table.insert(merged, text)
      end
    end
    table.insert(headers, table.concat(merged, " "))
  end

  return headers
end

-- Parse floattable headers from table content
-- Splits header line on & and extracts content from each column
-- Handles: \lhdrx, \lhdr, \chdr, \rhdr, \hdstyle, plain text, and multi-row headers
local function parse_floattable_headers(table_content)
  local headers = {}

  -- Find the entire header block (everything before \capsep or \rowsep)
  local header_block = table_content:match("(.-)\\capsep")
  if not header_block then
    header_block = table_content:match("(.-)\\rowsep")
  end

  -- Verify the block actually contains header markers
  if header_block and not (
      header_block:find("\\lhdr", 1, true) or
      header_block:find("\\lhdrx", 1, true) or
      header_block:find("\\chdr", 1, true) or
      header_block:find("\\rhdr", 1, true) or
      header_block:find("\\hdstyle", 1, true) or
      header_block:find("\\multicolumn", 1, true)
  ) then
    header_block = nil
  end

  if header_block then
    -- Check for \multicolumn FIRST (special case with spanning headers)
    -- This must be checked before multi-row merge to avoid incorrect merging
    if header_block:find("\\multicolumn{", 1, true) then
      -- Multi-row header: Row 1 has \multicolumn, Row 2 has actual column headers
      -- Example: "File open modes" table
      local remaining_first_row =
        header_block:match("\\multicolumn{.-}{.-}{.-}%s*&%s*(.-)%s*\\\\")

      -- Get the second row before \\ (actual column headers)
      local second_row = header_block:match("\n([^\n]*)\\\\%s*$")

      if second_row and second_row ~= "" then
        -- Parse second row to get main column headers
        headers = parse_row(second_row)

        -- If there's a remaining header from first row, append it
        if remaining_first_row and remaining_first_row ~= "" then
          local extra_header = expand_table_macros(remaining_first_row)
          table.insert(headers, extra_header)
        end
        return headers
      end
    end

    -- Check for multi-row headers (multiple \\ without \multicolumn)
    -- These are stacked headers with sub-labels that should be merged
    local row_sep_count = 0
    local pos = 1
    while true do
      local found = header_block:find("\\\\", pos, true)
      if found then
        row_sep_count = row_sep_count + 1
        pos = found + 2
      else
        break
      end
    end

    -- Multi-row headers (2+ row separators): use the merge function
    if row_sep_count >= 2 then
      return parse_multirow_headers(header_block)
    end

    -- Single-row headers: split on & and process each column
    local columns = split_on_ampersand(header_block)

    for _, col in ipairs(columns) do
      local header_text, span_count = extract_header_from_column(col)
      header_text = expand_table_macros(header_text)

      -- Add header (and empty columns for spanning headers)
      table.insert(headers, header_text)
      for _ = 2, span_count do
        table.insert(headers, "")
      end
    end
  end

  return headers
end

-- Helper function to build markdown table from structured data
-- Single source of truth for table formatting
local function build_markdown_table(caption, headers, rows, label)
  local md_lines = {}

  -- Add caption as heading with optional anchor for cross-references
  if label and label ~= "" then
    table.insert(md_lines, "**Table: " .. caption .. "** <a id=\"" .. label .. "\">[" .. label .. "]</a>\n")
  else
    table.insert(md_lines, "**Table: " .. caption .. "**\n")
  end

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

-- Special row parser for lib2dtab2 (handles \rowhdr{})
local function parse_lib2dtab2_rows(table_content)
  local rows = {}
  local normalized = normalize_table_rows(table_content)

  for row_content in normalized:gmatch("([^@]+)@@ROWEND@@") do
    row_content = row_content:gsub("%s+", " "):match("^%s*(.-)%s*$")
    if row_content and #row_content > 0 then
      local rowhdr_start = row_content:find("\\rowhdr{", 1, true)
      if rowhdr_start == 1 then
        local row_header, row_end_pos = extract_braced(row_content, rowhdr_start + 7)
        if row_header then
          row_header = expand_table_macros(row_header)
          local rest = row_content:sub(row_end_pos + 1):match("^%s*&?%s*(.*)$") or ""
          local cells = parse_row(rest)
          local row = {row_header}
          for _, cell in ipairs(cells) do
            table.insert(row, cell)
          end
          table.insert(rows, row)
        end
      end
    end
  end
  return rows
end

-- Header parser registry (maps parser names to functions)
-- parse_floattable_headers is defined earlier in the file (line ~492)
local HEADER_PARSERS = {
  parse_floattable_headers = parse_floattable_headers,
}

-- Generic table handler using configuration from TABLE_CONFIGS
-- @param text: Raw LaTeX containing the table
-- @param env_name: Environment name (key in TABLE_CONFIGS)
-- @return: pandoc.RawBlock with markdown, or nil
local function handle_table_generic(text, env_name)
  local config = TABLE_CONFIGS[env_name]
  if not config then return nil end

  local begin_tag = "\\begin{" .. env_name .. "}"
  local end_tag = "\\end{" .. env_name .. "}"

  local env_start = text:find(begin_tag, 1, true)
  if not env_start then return nil end

  -- Extract arguments using shared utility (KEY DRY IMPROVEMENT)
  local args, content_start = extract_multi_arg_macro(text, env_start, #begin_tag, config.num_args)
  if not args then return nil end

  -- Find environment end
  local env_end = text:find(end_tag, content_start, true)
  if not env_end then return nil end

  -- Extract table content
  local table_content = text:sub(content_start, env_end - 1)

  -- Build caption
  local caption
  if config.caption_builder then
    caption = config.caption_builder(args)
  else
    caption = args[1]  -- Default: first arg is caption
  end
  caption = expand_table_macros(caption)

  -- Get label (usually arg 2, but can be overridden)
  local label_idx = config.label_arg or 2
  local label = args[label_idx]

  -- Build headers
  local headers = {}
  if type(config.headers) == "table" then
    -- Array of fixed strings or arg indices
    for _, h in ipairs(config.headers) do
      if type(h) == "number" then
        table.insert(headers, expand_table_macros(args[h]))
      else
        table.insert(headers, h)
      end
    end
  elseif config.headers == "parse" then
    -- Use standard header extraction
    if config.header_parser and HEADER_PARSERS[config.header_parser] then
      headers = HEADER_PARSERS[config.header_parser](table_content)
    else
      headers = extract_table_headers(table_content)
    end
  elseif config.headers == "parse_longtable" then
    -- Special LongTable header parsing
    local first_head = table_content:match("\\topline(.-)\\endfirsthead")
    if first_head then
      local h1, h2 = first_head:match("\\lhdr{([^}]*)}%s*&%s*\\rhdr{([^}]*)}")
      if h1 and h2 then
        headers = {expand_table_macros(h1), expand_table_macros(h2)}
      end
    end
  end

  -- Extract data section
  local data_section
  if config.data_section == "extract" then
    data_section = extract_data_section(table_content)
  else
    data_section = table_content
  end

  -- Parse rows
  local rows
  if config.row_parser == "lib2dtab2" then
    rows = parse_lib2dtab2_rows(data_section)
  else
    local normalized = normalize_table_rows(data_section)
    rows = parse_table_rows(normalized)
  end

  -- Build markdown
  return pandoc.RawBlock('markdown', build_markdown_table(caption, headers, rows, label))
end

-- Main filter function for raw blocks
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Try generic handler first for all configured table types
  for env_name, _ in pairs(TABLE_CONFIGS) do
    if text:find("\\begin{" .. env_name .. "}", 1, true) then
      local result = handle_table_generic(text, env_name)
      if result then return result end
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
