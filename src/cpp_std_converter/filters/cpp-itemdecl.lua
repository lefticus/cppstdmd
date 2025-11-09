--[[
cpp-itemdecl.lua

Pandoc Lua filter to handle C++ standard itemdecl and itemdescr environments.

The C++ standard uses:
- \begin{itemdecl}...\end{itemdecl} for function/class declarations
- \begin{itemdescr}...\end{itemdescr} for descriptions with \pnum, \expects, \effects, etc.

Pandoc doesn't recognize these custom environments and drops all their content,
resulting in massive documentation loss. This filter converts them to proper
Markdown structure.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local extract_braced_content = common.extract_braced_content
local trim = common.trim
local remove_font_switches = common.remove_font_switches
local expand_cpp_version_macros = common.expand_cpp_version_macros
local expand_concept_macros = common.expand_concept_macros
local convert_cross_references_in_code = common.convert_cross_references_in_code
local expand_library_spec_macros = common.expand_library_spec_macros
local remove_macro = common.remove_macro
local process_macro_with_replacement = common.process_macro_with_replacement

-- Track note and example counters across itemdescr processing
local itemdescr_note_counter = 0
local itemdescr_example_counter = 0

-- Reset counters when encountering headers (same logic as cpp-notes-examples.lua)
function Header(elem)
  if elem.level <= 4 then
    itemdescr_note_counter = 0
    itemdescr_example_counter = 0
  end
  return elem
end

-- extract_braced_content is now imported from cpp-common

-- Helper function to upgrade code blocks to fenced format for consistency
-- Pandoc converts \begin{verbatim} to indented code blocks (no language class)
-- We want all code blocks to use ``` cpp fences like cpp-code-blocks.lua produces
-- This function recursively processes nested structures (Div, BlockQuote, lists)
local function upgrade_code_blocks(blocks)
  local result = {}

  for _, block in ipairs(blocks) do
    if block.t == "CodeBlock" then
      -- Check if this is an indented code block (no classes)
      -- or already has a language class
      if not block.classes or #block.classes == 0 then
        -- Upgrade to fenced code block with cpp class
        block.classes = {"cpp"}
      end
      table.insert(result, block)
    elseif block.t == "Div" and block.content then
      -- Recursively process content inside Div blocks (notes/examples)
      block.content = upgrade_code_blocks(block.content)
      table.insert(result, block)
    elseif block.t == "BlockQuote" and block.content then
      -- Recursively process content inside BlockQuote
      block.content = upgrade_code_blocks(block.content)
      table.insert(result, block)
    elseif (block.t == "BulletList" or block.t == "OrderedList") and block.content then
      -- Recursively process list items
      for i, item in ipairs(block.content) do
        block.content[i] = upgrade_code_blocks(item)
      end
      table.insert(result, block)
    else
      table.insert(result, block)
    end
  end

  return result
end

-- Helper function to convert @@REF:label@@ placeholders to [[label]] markdown links
-- This is called after Pandoc processes the content to convert our temporary placeholders
local function convert_ref_placeholders(inlines)
  local result = {}
  for _, inline in ipairs(inlines) do
    if inline.t == "Str" then
      -- Check if this string contains our reference placeholder
      local text = inline.text
      -- Split on @@REF: markers and process each part
      local parts = {}
      local pos = 1
      while pos <= #text do
        local start_marker = text:find("@@REF:", pos, true)
        if start_marker then
          -- Add text before the marker
          local prefix = ""
          if start_marker > pos then
            local before_text = text:sub(pos, start_marker - 1)
            table.insert(parts, pandoc.Str(before_text))
            -- Check if we need a space before the reference for readability
            -- Add space if the text doesn't already end with whitespace
            if not before_text:match("%s$") then
              prefix = " "
            end
          elseif #parts > 0 and parts[#parts].t == "Str" then
            -- No text in current segment, check previous part
            local prev_text = parts[#parts].text
            if not prev_text:match("%s$") then
              prefix = " "
            end
          end
          -- Find end marker
          local end_marker = text:find("@@", start_marker + 6, true)
          if end_marker then
            -- Extract label
            local label = text:sub(start_marker + 6, end_marker - 1)
            -- Insert as RawInline markdown reference with space for readability
            table.insert(parts, pandoc.RawInline('markdown', prefix .. '[[' .. label .. ']]'))
            pos = end_marker + 2
          else
            -- No end marker, just add the rest
            table.insert(parts, pandoc.Str(text:sub(start_marker)))
            break
          end
        else
          -- No more markers, add the rest
          table.insert(parts, pandoc.Str(text:sub(pos)))
          break
        end
      end
      -- Add all parts to result
      for _, part in ipairs(parts) do
        table.insert(result, part)
      end
    else
      -- Not a string, keep as-is
      table.insert(result, inline)
    end
  end
  return result
end

-- Recursive helper to convert @@REF:label@@ placeholders in all block types
-- This handles nested structures like BulletList, OrderedList, etc.
local function convert_ref_placeholders_in_blocks(blocks)
  local result = {}
  for _, block in ipairs(blocks) do
    if block.t == "Para" and block.content then
      -- Convert placeholders in paragraph inline content
      block.content = convert_ref_placeholders(block.content)
      table.insert(result, block)
    elseif block.t == "Plain" and block.content then
      -- Convert placeholders in plain inline content
      block.content = convert_ref_placeholders(block.content)
      table.insert(result, block)
    elseif block.t == "BulletList" and block.content then
      -- Recursively process each list item
      for i, item in ipairs(block.content) do
        block.content[i] = convert_ref_placeholders_in_blocks(item)
      end
      table.insert(result, block)
    elseif block.t == "OrderedList" and block.content then
      -- Recursively process each list item
      for i, item in ipairs(block.content) do
        block.content[i] = convert_ref_placeholders_in_blocks(item)
      end
      table.insert(result, block)
    elseif block.t == "DefinitionList" and block.content then
      -- Recursively process definition list items
      for i, item in ipairs(block.content) do
        -- item is a pair: [term, definitions]
        -- term is a list of inlines
        item[1] = convert_ref_placeholders(item[1])
        -- definitions is a list of block lists
        for j, def_blocks in ipairs(item[2]) do
          item[2][j] = convert_ref_placeholders_in_blocks(def_blocks)
        end
        block.content[i] = item
      end
      table.insert(result, block)
    elseif block.t == "BlockQuote" and block.content then
      -- Recursively process blockquote content
      block.content = convert_ref_placeholders_in_blocks(block.content)
      table.insert(result, block)
    elseif block.t == "Div" and block.content then
      -- Recursively process div content
      block.content = convert_ref_placeholders_in_blocks(block.content)
      table.insert(result, block)
    else
      -- Other block types (CodeBlock, RawBlock, etc.) - keep as-is
      table.insert(result, block)
    end
  end
  return result
end

-- Unified function to process note or example environments in itemdescr
-- env_type: "note" or "example"
-- counter_ref: table with counter value (pass by reference)
-- Returns: result blocks
local function process_itemdescr_environment(content, env_type, counter_ref)
  counter_ref[1] = counter_ref[1] + 1
  local counter_val = counter_ref[1]

  -- Trim leading/trailing whitespace
  content = trim(content)

  -- Expand macros before Pandoc processing to preserve cross-references
  content = expand_itemdescr_macros(content)

  -- Parse the LaTeX content to get Pandoc AST elements
  local parsed = pandoc.read(content, "latex")
  local has_blocks = false

  -- Check if content has non-Para blocks (like code blocks, itemize)
  for _, parsed_block in ipairs(parsed.blocks) do
    if parsed_block.t ~= "Para" then
      has_blocks = true
      break
    end
  end

  local label = env_type:sub(1,1):upper() .. env_type:sub(2)  -- Capitalize first letter
  local result = {}

  if not has_blocks then
    -- Simple case: only paragraphs, combine into single inline sequence
    local inlines = {}
    for _, parsed_block in ipairs(parsed.blocks) do
      if parsed_block.t == "Para" and parsed_block.content then
        if #inlines > 0 then
          table.insert(inlines, pandoc.Space())
        end
        for _, inline in ipairs(parsed_block.content) do
          table.insert(inlines, inline)
        end
      end
    end

    -- Convert @@REF:label@@ placeholders to [[label]] markdown links
    inlines = convert_ref_placeholders(inlines)

    local para = {
      pandoc.Str("["),
      pandoc.Emph({pandoc.Str(label .. " " .. counter_val)}),
      pandoc.Str(": ")
    }
    for _, inline in ipairs(inlines) do
      table.insert(para, inline)
    end
    table.insert(para, pandoc.Str(" — "))
    table.insert(para, pandoc.Emph({pandoc.Str("end " .. env_type)}))
    table.insert(para, pandoc.Str("]"))

    table.insert(result, pandoc.Para(para))
  else
    -- Complex case: has code blocks or other non-Para blocks (like itemize)
    local opening = {
      pandoc.Str("["),
      pandoc.Emph({pandoc.Str(label .. " " .. counter_val)}),
      pandoc.Str(":")
    }
    table.insert(result, pandoc.Para(opening))

    -- Output all blocks from parsed content, converting ref placeholders in Para blocks
    for _, parsed_block in ipairs(parsed.blocks) do
      if parsed_block.t == "Para" and parsed_block.content then
        parsed_block.content = convert_ref_placeholders(parsed_block.content)
      end
      table.insert(result, parsed_block)
    end

    local closing = {
      pandoc.Str("— "),
      pandoc.Emph({pandoc.Str("end " .. env_type)}),
      pandoc.Str("]")
    }
    table.insert(result, pandoc.Para(closing))
  end

  return result
end

-- Helper function to process note/example blocks after pandoc.read()
-- This mirrors the logic from cpp-notes-examples.lua
local function process_notes_examples_blocks(blocks)
  local result = {}

  for _, block in ipairs(blocks) do
    -- Handle note/example Div blocks that Pandoc creates from \begin{note}/\begin{example}
    -- These were already parsed by Pandoc, so we just need to convert ref placeholders
    if block.t == "Div" and block.classes then
      local is_note = false
      local is_example = false
      for _, class in ipairs(block.classes) do
        if class == "note" then is_note = true end
        if class == "example" then is_example = true end
      end

      if is_note or is_example then
        -- Convert @@REF:label@@ placeholders in all Para blocks within this Div
        for i, div_block in ipairs(block.content) do
          if div_block.t == "Para" and div_block.content then
            div_block.content = convert_ref_placeholders(div_block.content)
            block.content[i] = div_block
          end
        end
        table.insert(result, block)
        goto continue
      end
    end

    -- Handle note environments in RawBlock
    if block.t == "RawBlock" and block.format == "latex" then
      local text = block.text

      -- Check for note environment
      local note_content = text:match("\\begin{note}([%s%S]-)\\end{note}")
      if note_content then
        local note_counter_ref = {itemdescr_note_counter}
        local blocks_to_insert = process_itemdescr_environment(note_content, "note", note_counter_ref)
        itemdescr_note_counter = note_counter_ref[1]
        for _, b in ipairs(blocks_to_insert) do
          table.insert(result, b)
        end
        goto continue
      end

      -- Check for example environment
      local example_content = text:match("\\begin{example}([%s%S]-)\\end{example}")
      if example_content then
        local example_counter_ref = {itemdescr_example_counter}
        local blocks_to_insert = process_itemdescr_environment(example_content, "example", example_counter_ref)
        itemdescr_example_counter = example_counter_ref[1]
        for _, b in ipairs(blocks_to_insert) do
          table.insert(result, b)
        end
        goto continue
      end
    end

    -- Keep other blocks as-is
    table.insert(result, block)

    ::continue::
  end

  return result
end

-- Helper function to expand macros in itemdescr text before Pandoc processing
local function expand_itemdescr_macros(text)
  -- Expand custom macros to standard LaTeX that Pandoc understands
  -- We use \texttt{} for code and \textit{} for emphasis

  -- Strip \indexlibrary{} macro (used for index generation, not content)
  -- Must handle nested braces like \indexlibrary{\idxcode{terminate}}
  text = remove_macro(text, "indexlibrary", false)

  -- Specification section labels - convert to italic with colon using LaTeX commands
  -- Use \textit{...}: for italic that Pandoc will convert properly
  -- \expects -> \textit{Preconditions:}
  text = text:gsub("\\expects%s*\n", "\\textit{Preconditions:} ")
  text = text:gsub("\\expects%s+", "\\textit{Preconditions:} ")

  -- \requires -> \textit{Requires:}
  text = text:gsub("\\requires%s*\n", "\\textit{Requires:} ")
  text = text:gsub("\\requires%s+", "\\textit{Requires:} ")

  -- \constraints -> \textit{Constraints:}
  text = text:gsub("\\constraints%s*\n", "\\textit{Constraints:} ")
  text = text:gsub("\\constraints%s+", "\\textit{Constraints:} ")

  -- \effects -> \textit{Effects:}
  text = text:gsub("\\effects%s*\n", "\\textit{Effects:} ")
  text = text:gsub("\\effects%s+", "\\textit{Effects:} ")

  -- \ensures -> \textit{Ensures:}
  text = text:gsub("\\ensures%s*\n", "\\textit{Ensures:} ")
  text = text:gsub("\\ensures%s+", "\\textit{Ensures:} ")

  -- \returns -> \textit{Returns:}
  text = text:gsub("\\returns%s*\n", "\\textit{Returns:} ")
  text = text:gsub("\\returns%s+", "\\textit{Returns:} ")

  -- \result -> \textit{Result:}
  text = text:gsub("\\result%s*\n", "\\textit{Result:} ")
  text = text:gsub("\\result%s+", "\\textit{Result:} ")

  -- \postconditions -> \textit{Postconditions:}
  text = text:gsub("\\postconditions%s*\n", "\\textit{Postconditions:} ")
  text = text:gsub("\\postconditions%s+", "\\textit{Postconditions:} ")

  -- \complexity -> \textit{Complexity:}
  text = text:gsub("\\complexity%s*\n", "\\textit{Complexity:} ")
  text = text:gsub("\\complexity%s+", "\\textit{Complexity:} ")

  -- \remarks -> \textit{Remarks:}
  text = text:gsub("\\remarks%s*\n", "\\textit{Remarks:} ")
  text = text:gsub("\\remarks%s+", "\\textit{Remarks:} ")

  -- \throws -> \textit{Throws:}
  text = text:gsub("\\throws%s*\n", "\\textit{Throws:} ")
  text = text:gsub("\\throws%s+", "\\textit{Throws:} ")

  -- \errors -> \textit{Error conditions:}
  text = text:gsub("\\errors%s*\n", "\\textit{Error conditions:} ")
  text = text:gsub("\\errors%s+", "\\textit{Error conditions:} ")

  -- \mandates -> \textit{Mandates:}
  text = text:gsub("\\mandates%s*\n", "\\textit{Mandates:} ")
  text = text:gsub("\\mandates%s+", "\\textit{Mandates:} ")

  -- \recommended -> \textit{Recommended practice:}
  text = text:gsub("\\recommended%s*\n", "\\textit{Recommended practice:} ")
  text = text:gsub("\\recommended%s+", "\\textit{Recommended practice:} ")

  -- \required -> \textit{Required behavior:}
  text = text:gsub("\\required%s*\n", "\\textit{Required behavior:} ")
  text = text:gsub("\\required%s+", "\\textit{Required behavior:} ")

  -- \default -> \textit{Default behavior:}
  text = text:gsub("\\default%s*\n", "\\textit{Default behavior:} ")
  text = text:gsub("\\default%s+", "\\textit{Default behavior:} ")

  -- \sync -> \textit{Synchronization:}
  text = text:gsub("\\sync%s*\n", "\\textit{Synchronization:} ")
  text = text:gsub("\\sync%s+", "\\textit{Synchronization:} ")

  -- \replaceable -> \textit{Replaceable:}
  text = text:gsub("\\replaceable%s*\n", "\\textit{Replaceable:} ")
  text = text:gsub("\\replaceable%s+", "\\textit{Replaceable:} ")

  -- \returntype -> \textit{Return type:}
  text = text:gsub("\\returntype%s*\n", "\\textit{Return type:} ")
  text = text:gsub("\\returntype%s+", "\\textit{Return type:} ")

  -- \ctype -> \textit{Type:} (Fundesc label variant)
  text = text:gsub("\\ctype%s*\n", "\\textit{Type:} ")
  text = text:gsub("\\ctype%s+", "\\textit{Type:} ")

  -- \templalias -> \textit{Alias template:}
  text = text:gsub("\\templalias%s*\n", "\\textit{Alias template:} ")
  text = text:gsub("\\templalias%s+", "\\textit{Alias template:} ")

  -- \implimits -> \textit{Implementation limits:}
  text = text:gsub("\\implimits%s*\n", "\\textit{Implementation limits:} ")
  text = text:gsub("\\implimits%s+", "\\textit{Implementation limits:} ")

  -- Handle @ escaped macros FIRST (before regular conversions)
  -- The @ delimiters mark where LaTeX macros appear in code blocks
  -- These should be converted to PLAIN TEXT since they're in code blocks
  -- NOT to \textit{} or \texttt{} which will leak into the output

  -- @\placeholdernc{x}@ -> x (plain text)
  text = text:gsub("@\\placeholdernc{([^}]*)}@", "%1")

  -- @\placeholder{x}@ -> x (plain text)
  text = text:gsub("@\\placeholder{([^}]*)}@", "%1")

  -- @\tcode{x}@ -> x (plain text, not \texttt)
  text = text:gsub("@\\tcode{([^}]*)}@", "%1")

  -- @\exposid{x}@ -> x (plain text)
  text = text:gsub("@\\exposid{([^}]*)}@", "%1")

  -- @\libconcept{x}@ -> x (plain text)
  text = text:gsub("@\\libconcept{([^}]*)}@", "%1")

  -- @\exposconcept{x}@ -> x (plain text)
  text = text:gsub("@\\exposconcept{([^}]*)}@", "%1")

  -- @\defexposconcept{x}@ -> x (plain text)
  text = text:gsub("@\\defexposconcept{([^}]*)}@", "%1")

  -- @\commentellip@ -> ... (plain text)
  text = text:gsub("@\\commentellip@", "...")

  -- Remove any remaining @ delimiters
  text = text:gsub("@", "")

  -- \bigoh{x} -> 𝑂(x) using Unicode Mathematical Italic Capital O (U+1D442)
  -- Must be done BEFORE \tcode conversion to handle nested macros
  -- Pandoc strips \bigoh when outside math mode, so we expand it
  -- Also expand common math commands inside bigoh to plain text
  text = text:gsub("\\bigoh{([^}]*)}", function(content)
    -- Expand math commands to plain text
    content = content:gsub("\\log", "log")
    content = content:gsub("\\min", "min")
    content = content:gsub("\\max", "max")
    content = content:gsub("\\sqrt", "sqrt")
    return "𝑂(" .. content .. ")"
  end)

  -- Handle \tcode{\placeholdernc{...}...} special case with proper brace balancing
  -- When \tcode wraps \placeholdernc, the placeholder dominates and we want italic, not code
  -- This pattern can contain nested \tcode{} inside, like: \tcode{\placeholdernc{FUN}($\tcode{T}_j$)}
  -- We need to strip ALL \tcode{} wrappers while converting \placeholdernc{} -> \textit{}
  while true do
    local start_pos = text:find("\\tcode{\\placeholdernc{", 1, true)
    if not start_pos then break end

    -- Extract the full \tcode{...} content using brace-balancing
    local tcode_content, end_pos = extract_braced_content(text, start_pos, 6)  -- "\tcode" is 6 chars
    if tcode_content then
      -- Remove nested \tcode{} wrappers while preserving content
      -- Example: \placeholdernc{FUN}($\tcode{T}_j$) -> \placeholdernc{FUN}($T_j$)
      -- Use helper function to recursively remove all \tcode{} macros
      local cleaned = remove_macro(tcode_content, "tcode", true)

      -- Now apply placeholder conversion
      cleaned = cleaned:gsub("\\placeholdernc{", "\\textit{")
      text = text:sub(1, start_pos - 1) .. cleaned .. text:sub(end_pos)
    else
      -- Couldn't extract, skip this occurrence
      break
    end
  end

  -- \placeholdernc{x} -> \textit{x}
  -- Must be done BEFORE \tcode conversion to avoid nested macros getting trapped
  -- in code blocks (e.g., \tcode{\placeholdernc{X}} should become italic, not code)
  text = text:gsub("\\placeholdernc{", "\\textit{")

  -- Process \tcode{} blocks to strip nested \texttt{} from simplified_macros.tex preprocessing
  -- This prevents nested backticks like `const_cast``<X ``const``&>` in the final markdown
  -- Example: \tcode{\texttt{const_cast}<X \texttt{const}\&>} -> \texttt{const_cast<X const\&>}
  -- When simplified_macros.tex converts \keyword{} to \texttt{}, we need to strip those
  -- inner \texttt{} wrappers before pandoc.read() sees them (to avoid double conversion)
  while true do
    local start_pos = text:find("\\tcode{", 1, true)
    if not start_pos then break end

    -- Extract the full \tcode{...} content using brace-balancing
    local tcode_content, end_pos = extract_braced_content(text, start_pos, 6)  -- "\tcode" is 6 chars
    if tcode_content then
      -- Strip all \texttt{} wrappers that came from simplified_macros.tex (\keyword{}, \libconcept{}, etc.)
      -- Use remove_macro to recursively remove all \texttt{} macros
      local cleaned = remove_macro(tcode_content, "texttt", true)

      -- Replace \tcode{...} with \texttt{cleaned}
      text = text:sub(1, start_pos - 1) .. "\\texttt{" .. cleaned .. "}" .. text:sub(end_pos)
    else
      -- Couldn't extract, skip this occurrence
      break
    end
  end

  -- Range macros
  -- \range{first}{last} -> [first, last) (half-open range)
  text = text:gsub("\\range{([^}]*)}{([^}]*)}", "[\\texttt{%1}, \\texttt{%2})")

  -- \crange{first}{last} -> [first, last] (closed range - both inclusive)
  text = text:gsub("\\crange{([^}]*)}{([^}]*)}", "[\\texttt{%1}, \\texttt{%2}]")

  -- \countedrange{first}{n} -> first+[0, n) (counted range)
  text = text:gsub("\\countedrange{([^}]*)}{([^}]*)}", "\\texttt{%1}+[0, \\texttt{%2})")

  -- \brange{first}{last} -> (first, last) (both exclusive)
  text = text:gsub("\\brange{([^}]*)}{([^}]*)}", "(\\texttt{%1}, \\texttt{%2})")

  -- \orange{first}{last} -> (first, last) (open range - both exclusive, alias for \brange)
  text = text:gsub("\\orange{([^}]*)}{([^}]*)}", "(\\texttt{%1}, \\texttt{%2})")

  -- \libconcept{x} -> \texttt{x}
  text = text:gsub("\\libconcept{", "\\texttt{")

  -- \exposconcept{x} -> \texttt{x}
  text = text:gsub("\\exposconcept{", "\\texttt{")

  -- \oldconcept{x} -> \textit{Cpp17x} (prepend Cpp17 prefix)
  text = text:gsub("\\oldconcept{([^}]*)}", "\\textit{Cpp17%1}")

  -- \grammarterm{x} -> \textit{x} (grammar terms)
  text = text:gsub("\\grammarterm{", "\\textit{")

  -- \impldef{description} -> \textit{implementation-defined}
  -- The description is for implementers, we just show "implementation-defined"
  -- Use brace-balanced extraction because description may contain nested \tcode{}
  text = process_macro_with_replacement(text, "impldef", function(content)
    return "\\textit{implementation-defined}"
  end)

  -- \mname{X} -> __X__ (preprocessor macro names with underscore wrapper)
  -- Handle specific cases first
  text = text:gsub("\\mname{VA_ARGS}", "__VA_ARGS__")
  text = text:gsub("\\mname{VA_OPT}", "__VA_OPT__")
  -- Then handle generic case
  text = text:gsub("\\mname{([^}]*)}", "__%1__")

  -- \ntbs{} and \ntmbs{} - null-terminated string abbreviations
  text = text:gsub("\\ntbs{}", "NTBS")
  text = text:gsub("\\ntmbs{}", "NTMBS")
  text = text:gsub("\\NTS{([^}]*)}", function(s) return s:upper() end)

  -- \placeholder{x} -> \textit{x}
  text = text:gsub("\\placeholder{", "\\textit{")

  -- \exposid{x} -> \textit{x}
  text = text:gsub("\\exposid{", "\\textit{")

  -- Cross-references - Pandoc strips these, so we need to preserve them
  -- Use a temporary placeholder that Pandoc will accept as LaTeX
  -- We'll convert these to markdown links after Pandoc processes the content
  -- Using @@REF: prefix as a marker that we can find and replace later
  text = text:gsub("\\ref{([^}]*)}", "@@REF:%1@@")
  text = text:gsub("\\iref{([^}]*)}", "@@REF:%1@@")
  text = text:gsub("\\tref{([^}]*)}", "@@REF:%1@@")

  -- \phantom{x} -> x (extract content for spacing)
  -- LaTeX spacing command, just extract the content
  text = text:gsub("\\phantom{([^}]*)}", "%1")

  -- Convert \begin{codeblock}...\end{codeblock} to LaTeX verbatim
  -- Pandoc doesn't recognize the custom codeblock environment and strips it
  -- We need to convert it to \begin{verbatim}...\end{verbatim} before pandoc.read()
  text = text:gsub("\\begin{codeblock}(.-)\\end{codeblock}", function(code)
    -- Clean up the code inline (can't call clean_itemdecl_code - it's defined later)
    -- Just do the essential cleaning: remove @ delimiters and common macros

    -- Remove @ escape delimiters
    code = code:gsub("@\\commentellip@", "...")
    code = code:gsub("@\\tcode{([^}]*)}@", "%1")
    code = code:gsub("@\\placeholder{([^}]*)}@", "%1")
    code = code:gsub("@\\placeholdernc{([^}]*)}@", "%1")
    code = code:gsub("@\\exposid{([^}]*)}@", "%1")
    code = code:gsub("@\\exposidnc{([^}]*)}@", "%1")
    code = code:gsub("@\\libglobal{([^}]*)}@", "%1")
    code = code:gsub("@\\libmember{([^}]*)}{([^}]*)}@", "%1")
    code = code:gsub("@\\libconcept{([^}]*)}@", "%1")
    code = code:gsub("@\\exposconcept{([^}]*)}@", "%1")
    code = code:gsub("@", "")

    -- Expand macros
    code = code:gsub("\\tcode{([^}]*)}", "%1")
    code = code:gsub("\\placeholder{([^}]*)}", "%1")
    code = code:gsub("\\placeholdernc{([^}]*)}", "%1")
    code = code:gsub("\\exposid{([^}]*)}", "%1")
    code = code:gsub("\\exposidnc{([^}]*)}", "%1")
    code = code:gsub("\\libglobal{([^}]*)}", "%1")
    code = code:gsub("\\libmember{([^}]*)}{([^}]*)}", "%1")
    code = code:gsub("\\libconcept{([^}]*)}", "%1")
    code = code:gsub("\\exposconcept{([^}]*)}", "%1")
    code = code:gsub("\\oldconcept{([^}]*)}", "%1")
    code = code:gsub("\\iref{([^}]*)}", "[%1]")
    code = code:gsub("\\tref{([^}]*)}", "[%1]")
    code = code:gsub("\\ref{([^}]*)}", "[%1]")
    code = code:gsub("\\range{([^}]*)}{([^}]*)}", "[%1, %2)")
    code = code:gsub("\\brk{}", "")
    code = code:gsub("\\cv{}", "cv")
    code = code:gsub("\\seebelow", "see below")
    code = code:gsub("\\unspec", "unspecified")
    -- Use pattern that requires \expos to NOT be followed by 'i' to avoid matching \exposid or \exposidnc
    code = code:gsub("\\expos([^i])", "exposition only%1")
    code = code:gsub("\\expos$", "exposition only")

    -- Remove font switch commands (bare commands without arguments)
    code = remove_font_switches(code)

    -- Handle layout overlap commands: \rlap{}, \llap{}, \clap{}
    code = code:gsub("\\rlap{([^}]+)}", "%1")
    code = code:gsub("\\llap{([^}]+)}", "%1")
    code = code:gsub("\\clap{([^}]+)}", "%1")

    -- Trim leading/trailing whitespace
    code = code:gsub("^%s+", "")
    code = code:gsub("%s+$", "")

    -- Return as LaTeX verbatim that pandoc.read() will convert to code block
    -- Use \n to ensure proper spacing around the code block
    return "\n\n\\begin{verbatim}\n" .. code .. "\n\\end{verbatim}\n\n"
  end)

  return text
end

-- Helper function to clean up code in itemdecl
local function clean_itemdecl_code(code)
  -- These are similar to code blocks, use same cleaning approach

  -- Remove @ escape delimiters and expand common macros
  code = code:gsub("@\\commentellip@", "...")

  -- \tcode{x} represents inline code (just extract the content)
  code = code:gsub("@\\tcode{([^}]*)}@", "%1")
  code = code:gsub("\\tcode{([^}]*)}", "%1")

  -- \placeholder{x} represents a placeholder
  code = code:gsub("@\\placeholder{([^}]*)}@", "%1")
  code = code:gsub("\\placeholder{([^}]*)}", "%1")

  -- \placeholdernc{x} represents a placeholder (non-code variant)
  code = code:gsub("@\\placeholdernc{([^}]*)}@", "%1")
  code = code:gsub("\\placeholdernc{([^}]*)}", "%1")

  -- \exposid{x} represents exposition-only identifier
  code = code:gsub("@\\exposid{([^}]*)}@", "%1")
  code = code:gsub("\\exposid{([^}]*)}", "%1")

  -- \libglobal{x} represents a library-level global name (Issue #24)
  code = code:gsub("@\\libglobal{([^}]*)}@", "%1")
  code = code:gsub("\\libglobal{([^}]*)}", "%1")

  -- \libmember{member}{class} represents a library class member name (Issue #24)
  -- Takes 2 parameters but only outputs the first (member name)
  code = code:gsub("@\\libmember{([^}]*)}{([^}]*)}@", "%1")
  code = code:gsub("\\libmember{([^}]*)}{([^}]*)}", "%1")

  -- Concept macros (library, exposition-only, and old-style concepts)
  code = expand_concept_macros(code, true)

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

  -- Library specification macros
  code = expand_library_spec_macros(code, true)

  -- Additional cross-references not in shared function
  code = code:gsub("\\tref{([^}]*)}", "[%1]")

  -- \range{first}{last} macro
  code = code:gsub("\\range{([^}]*)}{([^}]*)}", "[%1, %2)")

  -- Strip \brk{} line break hints
  code = code:gsub("\\brk{}", "")

  -- Strip indexing commands
  code = code:gsub("\\indexlibrary[^{]*{[^}]*}", "")
  code = code:gsub("\\indexlibraryglobal{[^}]*}", "")

  -- Remove any remaining @ delimiters
  code = code:gsub("@", "")

  -- Clean up extra whitespace but preserve indentation
  code = code:gsub("[ \\t]+\\n", "\\n")

  return code
end

-- Main filter function for raw blocks
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Match \begin{itemdecl}...\end{itemdecl}
  local content = text:match("\\begin{itemdecl}(.-)\\end{itemdecl}")

  if content then
    -- Clean up the code
    content = clean_itemdecl_code(content)

    -- Trim leading/trailing whitespace
    content = content:gsub("^%s+", "")
    content = content:gsub("%s+$", "")

    -- Return as a code block with cpp language
    return pandoc.CodeBlock(content, {class = "cpp"})
  end

  -- Match \begin{itemdescr}...\end{itemdescr}
  -- This environment contains descriptive text with special commands
  content = text:match("\\begin{itemdescr}(.-)\\end{itemdescr}")

  if content then
    -- First expand macros before Pandoc processes the content
    -- This prevents \tcode{}, \range{}, etc. from being stripped
    content = expand_itemdescr_macros(content)

    -- Now process with Pandoc to convert LaTeX to Markdown
    local blocks = pandoc.read(content, "latex").blocks

    -- Process any note/example blocks in the result
    -- This handles nested environments like \begin{itemize} properly
    blocks = process_notes_examples_blocks(blocks)

    -- Upgrade indented code blocks to fenced blocks for consistency
    -- This ensures all code blocks use ``` cpp format like cpp-code-blocks.lua
    blocks = upgrade_code_blocks(blocks)

    -- Convert @@REF:label@@ placeholders to [[label]] in all block types
    -- This handles references in Para, Plain, BulletList, OrderedList, etc.
    blocks = convert_ref_placeholders_in_blocks(blocks)

    -- Return blocks without blockquote wrapper for better readability
    return blocks
  end

  -- If no match, return unchanged
  return elem
end
