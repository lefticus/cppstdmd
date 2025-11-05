--[[
cpp-notes-examples.lua

Pandoc Lua filter to convert C++ standard note and example environments.

Handles:
- \begin{note}...\end{note} → [*Note N*: ... — *end note*]
- \begin{example}...\end{example} → [*Example N*: ... — *end example*]

Both can contain nested elements like code blocks, cross-refs, and footnotes.
Counters reset when encountering new sections.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local trim = common.trim
local expand_cpp_version_macros = common.expand_cpp_version_macros
local expand_concept_macros = common.expand_concept_macros
local convert_cross_references_in_code = common.convert_cross_references_in_code
local expand_library_spec_macros = common.expand_library_spec_macros
local extract_braced_content = common.extract_braced_content
local expand_nested_macros_recursive = common.expand_nested_macros_recursive

-- Track note and example counters
local note_counter = 0
local example_counter = 0

-- Helper function to clean up LaTeX escapes in code
-- (copied from cpp-code-blocks.lua to handle nested codeblocks)
local function clean_code(code)
  -- Remove @ escape delimiters and expand common macros

  -- \commentellip represents "..."
  code = code:gsub("@\\commentellip@", "...")

  -- Special case: preserve newlines after \textbackslash in @\tcode{}@ blocks
  -- This must be handled BEFORE the general macro expansion
  code = code:gsub("@\\tcode{([^@]-)\\textbackslash}@\n", function(content)
    return content .. "\\\n"
  end)

  -- Expand macros in multiple passes to handle nesting (e.g., \tcode{\keyword{x}})
  -- Use helper function for cleaner recursive expansion
  local macro_patterns = {
    -- \tcode{x} represents inline code (just extract the content)
    -- Handle both @\tcode{x}@ and bare \tcode{x} (in comments)
    -- Use pattern that matches up to }@ specifically
    {pattern = "@\\tcode{([^@]-)}@", replacement = "%1"},
    {pattern = "\\tcode{([^}]*)}", replacement = "%1"},

    -- \placeholder{x} represents a placeholder (keep as-is or use angle brackets)
    {pattern = "@\\placeholder{([^}]*)}@", replacement = "%1"},
    {pattern = "\\placeholder{([^}]*)}", replacement = "%1"},

    -- \placeholdernc{x} represents a placeholder (non-code variant)
    {pattern = "@\\placeholdernc{([^}]*)}@", replacement = "%1"},
    {pattern = "\\placeholdernc{([^}]*)}", replacement = "%1"},

    -- \exposid{x} represents exposition-only identifier
    {pattern = "@\\exposid{([^}]*)}@", replacement = "%1"},
    {pattern = "\\exposid{([^}]*)}", replacement = "%1"},

    -- \keyword{x} in code comments
    {pattern = "\\keyword{([^}]*)}", replacement = "%1"},

    -- \texttt{x} in code comments (font switch, just extract content)
    {pattern = "\\texttt{([^}]*)}", replacement = "%1"},

    -- \grammarterm{x} in code comments
    {pattern = "\\grammarterm{([^}]*)}", replacement = "%1"},

    -- \term{x} in code comments
    {pattern = "\\term{([^}]*)}", replacement = "%1"}
  }

  code = expand_nested_macros_recursive(code, macro_patterns, 5)

  -- Concept macros (library, exposition-only, and old-style concepts)
  code = expand_concept_macros(code, true)

  -- Handle escaped special characters
  code = code:gsub("\\#", "#")
  code = code:gsub("\\%%", "%")
  code = code:gsub("\\&", "&")
  code = code:gsub("\\$", "$")

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

  -- \colcol{} represents ::
  code = code:gsub("\\colcol{}", "::")

  -- Strip \brk{} line break hints
  code = code:gsub("\\brk{}", "")

  -- Math formatting in code comments
  code = code:gsub("\\mathit{([^}]*)}", "%1")
  code = code:gsub("\\mathrm{([^}]*)}", "%1")

  -- Text formatting in code comments - strip the commands but keep content
  -- Handle @\textrm{}@ and @\textit{}@ with nested braces
  while true do
    local changed = false
    local new_code = code:gsub("@\\textrm{([^{}@]*)}@", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    new_code = code:gsub("@\\textit{([^{}@]*)}@", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    -- Also handle bare versions (not in @ delimiters)
    new_code = code:gsub("\\textrm{([^{}]*)}", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    new_code = code:gsub("\\textit{([^{}]*)}", "%1")
    if new_code ~= code then changed = true end
    code = new_code
    if not changed then break end
  end

  -- \ref{x} cross-references
  code = code:gsub("\\ref{([^}]*)}", "[%1]")

  -- \textbackslash represents a backslash (for line continuations, etc.)
  code = code:gsub("\\textbackslash", "\\")

  -- Remove any remaining @ delimiters
  code = code:gsub("@([^@]*)@", "%1")

  -- Clean up extra whitespace but preserve indentation
  -- Remove trailing whitespace from each line
  code = code:gsub("[ \t]+\n", "\n")

  return code
end

-- Helper function to convert codeblock Div to CodeBlock or replace placeholders
local function process_codeblock_div(block, codeblocks)
  -- Check for placeholder in Para blocks
  if block.t == "Para" and codeblocks then
    local text = pandoc.utils.stringify(block)
    -- Only replace if the Para contains ONLY the placeholder (possibly with whitespace)
    local trimmed = trim(text)
    local placeholder = trimmed:match("^__CODEBLOCK_(%d+)__$")
    if placeholder then
      local idx = tonumber(placeholder)
      if codeblocks[idx] then
        return pandoc.CodeBlock(codeblocks[idx], {class = "cpp"})
      end
    end
  end

  -- Check for codeblock Div (fallback for cases without placeholders)
  if block.t == "Div" and block.classes and block.classes[1] == "codeblock" then
    -- Extract text content from all Para blocks inside the div
    local code_text = ""
    for _, div_block in ipairs(block.content) do
      if div_block.t == "Para" then
        -- Convert Para content to plain text
        local text = pandoc.utils.stringify(div_block)
        if #code_text > 0 then
          code_text = code_text .. "\n"
        end
        code_text = code_text .. text
      elseif div_block.t == "CodeBlock" then
        -- Already a code block, use its text
        if #code_text > 0 then
          code_text = code_text .. "\n"
        end
        code_text = code_text .. div_block.text
      end
    end

    -- Create a proper CodeBlock with class "cpp"
    if #code_text > 0 then
      return pandoc.CodeBlock(code_text, {class = "cpp"})
    end
  end

  return block
end

-- Optimized codeblock extraction using position tracking instead of repeated scanning
-- Handles all code block types: codeblock, codeblocktu, codeblockdigitsep, outputblock
-- Uses pattern matching with balanced brace extraction for codeblocktu titles
local function extract_codeblocks(content)
  local codeblocks = {}
  local modified_content = content
  local counter = 0

  -- Process each type with its own pattern, finding earliest match each iteration
  local pos = 1
  while pos <= #modified_content do
    local earliest_start, earliest_end, earliest_code, earliest_type = nil, nil, nil, nil

    -- Try each pattern and find which one matches earliest
    local patterns = {
      {name = "codeblock", start_pat = "\\begin{codeblock}",  end_pat = "\\end{codeblock}"},
      {name = "codeblockdigitsep", start_pat = "\\begin{codeblockdigitsep}", end_pat = "\\end{codeblockdigitsep}"},
      {name = "outputblock", start_pat = "\\begin{outputblock}", end_pat = "\\end{outputblock}"},
    }

    for _, p in ipairs(patterns) do
      local start_pos = modified_content:find(p.start_pat, pos, true)
      if start_pos and (not earliest_start or start_pos < earliest_start) then
        local end_pos = modified_content:find(p.end_pat, start_pos, true)
        if end_pos then
          local code_start = start_pos + #p.start_pat
          local code = modified_content:sub(code_start, end_pos - 1)
          earliest_start = start_pos
          earliest_end = end_pos + #p.end_pat - 1
          earliest_code = code
          earliest_type = p.name
        end
      end
    end

    -- Handle codeblocktu separately due to title parameter with nested braces
    local cbtu_start = modified_content:find("\\begin{codeblocktu}{", pos, true)
    local cbtu_title = nil
    if cbtu_start and (not earliest_start or cbtu_start < earliest_start) then
      -- Use brace-balanced extraction for the title
      local title_brace_start = cbtu_start + 20  -- After \begin{codeblocktu}{
      local title, title_end = extract_braced_content(modified_content, title_brace_start - 1, 0)
      if title and title_end then
        local cbtu_end = modified_content:find("\\end{codeblocktu}", title_end, true)
        if cbtu_end then
          local code = modified_content:sub(title_end + 1, cbtu_end - 1)
          earliest_start = cbtu_start
          earliest_end = cbtu_end + 17 - 1  -- \end{codeblocktu} is 17 chars
          earliest_code = code
          earliest_type = "codeblocktu"
          cbtu_title = title  -- Store the raw title for processing
        end
      end
    end

    if earliest_start and earliest_code then
      -- Clean and store the code
      local code = earliest_code:gsub("^%s*\n", ""):gsub("\n%s*$", "")
      code = clean_code(code)

      -- For codeblocktu, prepend the formatted title
      if earliest_type == "codeblocktu" and cbtu_title then
        -- Process title: expand \tcode{} and clean up
        local formatted_title = cbtu_title
        formatted_title = formatted_title:gsub("\\tcode{([^}]*)}", "`%1`")
        formatted_title = formatted_title:gsub("\\#", "#")
        code = "**" .. formatted_title .. "**\n\n" .. code
      end

      counter = counter + 1
      codeblocks[counter] = code

      -- Replace with placeholder
      local placeholder = "\n\n__CODEBLOCK_" .. counter .. "__\n\n"
      modified_content = modified_content:sub(1, earliest_start - 1) .. placeholder .. modified_content:sub(earliest_end + 1)

      -- Continue from after the placeholder
      pos = earliest_start + #placeholder
    else
      break
    end
  end

  return modified_content, codeblocks, counter
end

-- Macro expansion lookup table for better performance
local macro_expansions = {
  ["\\Cpp{}"] = "C++",
  ["\\IsoC{}"] = "ISO/IEC 9899:2018 (C)",
}

-- Optimized macro expansion using single pass
local function expand_macros(content)
  -- Expand table-based macros first
  for pattern, replacement in pairs(macro_expansions) do
    content = content:gsub(pattern:gsub("%p", "%%%1"), replacement)  -- Escape pattern chars
  end

  -- Expand context-sensitive macros (those with optional whitespace/delimiters)
  content = content:gsub("\\Cpp%s", "C++ ")
  content = content:gsub("\\Cpp([^%w])", "C++%1")

  -- Expand \term{} and \defn{} to \emph{}
  content = content:gsub("\\term{([^}]*)}", "\\emph{%1}")
  content = content:gsub("\\defn{([^}]*)}", "\\emph{%1}")

  return content
end

-- Unified function to process note or example environments
-- env_type: "note" or "example"
-- counter_val: current counter value
-- Returns: result blocks, updated counter value
local function process_environment(content, env_type, counter_val)
  counter_val = counter_val + 1

  -- Trim leading/trailing whitespace
  content = trim(content)

  -- Expand macros efficiently
  content = expand_macros(content)

  -- Extract codeblocks before parsing (optimized)
  local modified_content, codeblocks, codeblock_count = extract_codeblocks(content)

  -- Parse the LaTeX content to get Pandoc AST elements
  local parsed = pandoc.read(modified_content, "latex+raw_tex")
  local has_blocks = false

  -- Check if content has non-Para blocks
  for _, parsed_block in ipairs(parsed.blocks) do
    if parsed_block.t ~= "Para" then
      has_blocks = true
      break
    end
  end
  if codeblock_count > 0 then
    has_blocks = true  -- Force complex case if we have codeblocks
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
    -- Complex case: has code blocks or other non-Para blocks
    local opening = {
      pandoc.Str("["),
      pandoc.Emph({pandoc.Str(label .. " " .. counter_val)}),
      pandoc.Str(":")
    }
    table.insert(result, pandoc.Para(opening))

    -- Output all blocks from parsed content
    for _, parsed_block in ipairs(parsed.blocks) do
      table.insert(result, process_codeblock_div(parsed_block, codeblocks))
    end

    local closing = {
      pandoc.Str("— "),
      pandoc.Emph({pandoc.Str("end " .. env_type)}),
      pandoc.Str("]")
    }
    table.insert(result, pandoc.Para(closing))
  end

  return result, counter_val
end

-- Process blocks to find and convert note/example environments
function Blocks(blocks)
  local result = {}

  for i, block in ipairs(blocks) do
    -- Reset counters when we encounter a new section (any header level 1-4)
    if block.t == "Header" and block.level <= 4 then
      note_counter = 0
      example_counter = 0
      table.insert(result, block)
      goto continue
    end

    -- Handle note environments in RawBlock
    if block.t == "RawBlock" and block.format == "latex" then
      local text = block.text

      -- Skip blocks that contain description lists - let cpp-macros.lua handle those
      -- (they may contain nested notes/examples which will be processed after parsing)
      if text:match("\\begin{description}") then
        table.insert(result, block)
        goto continue
      end

      -- Check for note environment
      local note_content = text:match("\\begin{note}([%s%S]-)\\end{note}")
      if note_content then
        local blocks_to_insert
        blocks_to_insert, note_counter = process_environment(note_content, "note", note_counter)
        for _, b in ipairs(blocks_to_insert) do
          table.insert(result, b)
        end
        goto continue
      end

      -- Check for example environment
      local example_content = text:match("\\begin{example}([%s%S]-)\\end{example}")
      if example_content then
        local blocks_to_insert
        blocks_to_insert, example_counter = process_environment(example_content, "example", example_counter)
        for _, b in ipairs(blocks_to_insert) do
          table.insert(result, b)
        end
        goto continue
      end
    end

    -- Handle note/example environments in CodeBlock with class "latex"
    -- These are rare edge cases where content is preserved as raw LaTeX
    if block.t == "CodeBlock" and block.classes and block.classes[1] == "latex" then
      local text = block.text

      -- Check for note environment
      local note_content = text:match("\\begin{note}([%s%S]-)\\end{note}")
      if note_content then
        note_counter = note_counter + 1
        note_content = trim(note_content)
        table.insert(result, pandoc.Para({
          pandoc.Str("["),
          pandoc.Emph({pandoc.Str("Note " .. note_counter)}),
          pandoc.Str(": "),
          pandoc.RawInline('latex', note_content),
          pandoc.Str(" — "),
          pandoc.Emph({pandoc.Str("end note")}),
          pandoc.Str("]")
        }))
        goto continue
      end

      -- Check for example environment
      local example_content = text:match("\\begin{example}([%s%S]-)\\end{example}")
      if example_content then
        example_counter = example_counter + 1
        example_content = trim(example_content)
        table.insert(result, pandoc.Para({
          pandoc.Str("["),
          pandoc.Emph({pandoc.Str("Example " .. example_counter)}),
          pandoc.Str(": "),
          pandoc.RawInline('latex', example_content),
          pandoc.Str(" — "),
          pandoc.Emph({pandoc.Str("end example")}),
          pandoc.Str("]")
        }))
        goto continue
      end
    end

    -- Handle Div elements that Pandoc created from LaTeX environments
    -- These are environments that Pandoc's LaTeX reader converts to Div instead of RawBlock
    if block.t == "Div" and block.classes then
      -- Handle <div class="note">
      if block.classes[1] == "note" then
        note_counter = note_counter + 1

        local note_inlines = {}
        local has_blocks = false

        -- Check if content has non-Para blocks
        for _, div_block in ipairs(block.content) do
          if div_block.t ~= "Para" then
            has_blocks = true
            break
          end
        end

        if not has_blocks then
          -- Simple case: only paragraphs, combine into single inline sequence
          for _, div_block in ipairs(block.content) do
            if div_block.t == "Para" and div_block.content then
              if #note_inlines > 0 then
                table.insert(note_inlines, pandoc.Space())
              end
              for _, inline in ipairs(div_block.content) do
                table.insert(note_inlines, inline)
              end
            end
          end

          local note_para = {
            pandoc.Str("["),
            pandoc.Emph({pandoc.Str("Note " .. note_counter)}),
            pandoc.Str(": ")
          }
          for _, inline in ipairs(note_inlines) do
            table.insert(note_para, inline)
          end
          table.insert(note_para, pandoc.Str(" — "))
          table.insert(note_para, pandoc.Emph({pandoc.Str("end note")}))
          table.insert(note_para, pandoc.Str("]"))

          table.insert(result, pandoc.Para(note_para))
        else
          -- Complex case: has code blocks or other non-Para blocks
          local opening = {
            pandoc.Str("["),
            pandoc.Emph({pandoc.Str("Note " .. note_counter)}),
            pandoc.Str(":")
          }
          table.insert(result, pandoc.Para(opening))

          -- Output all blocks from div content
          for _, div_block in ipairs(block.content) do
            table.insert(result, process_codeblock_div(div_block))
          end

          local closing = {
            pandoc.Str("— "),
            pandoc.Emph({pandoc.Str("end note")}),
            pandoc.Str("]")
          }
          table.insert(result, pandoc.Para(closing))
        end

        goto continue
      end

      -- Handle <div class="example">
      if block.classes[1] == "example" then
        example_counter = example_counter + 1

        local example_inlines = {}
        local has_blocks = false

        -- Check if content has non-Para blocks
        for _, div_block in ipairs(block.content) do
          if div_block.t ~= "Para" then
            has_blocks = true
            break
          end
        end

        if not has_blocks then
          -- Simple case: only paragraphs, combine into single inline sequence
          for _, div_block in ipairs(block.content) do
            if div_block.t == "Para" and div_block.content then
              if #example_inlines > 0 then
                table.insert(example_inlines, pandoc.Space())
              end
              for _, inline in ipairs(div_block.content) do
                table.insert(example_inlines, inline)
              end
            end
          end

          local example_para = {
            pandoc.Str("["),
            pandoc.Emph({pandoc.Str("Example " .. example_counter)}),
            pandoc.Str(": ")
          }
          for _, inline in ipairs(example_inlines) do
            table.insert(example_para, inline)
          end
          table.insert(example_para, pandoc.Str(" — "))
          table.insert(example_para, pandoc.Emph({pandoc.Str("end example")}))
          table.insert(example_para, pandoc.Str("]"))

          table.insert(result, pandoc.Para(example_para))
        else
          -- Complex case: has code blocks or other non-Para blocks
          local opening = {
            pandoc.Str("["),
            pandoc.Emph({pandoc.Str("Example " .. example_counter)}),
            pandoc.Str(":")
          }
          table.insert(result, pandoc.Para(opening))

          -- Output all blocks from div content
          for _, div_block in ipairs(block.content) do
            table.insert(result, process_codeblock_div(div_block))
          end

          local closing = {
            pandoc.Str("— "),
            pandoc.Emph({pandoc.Str("end example")}),
            pandoc.Str("]")
          }
          table.insert(result, pandoc.Para(closing))
        end

        goto continue
      end

      -- Handle <div class="footnote"> - just unwrap the div, keep content
      if block.classes[1] == "footnote" then
        -- Footnotes are just unwrapped - no special formatting needed
        -- Just output the content blocks directly
        for _, div_block in ipairs(block.content) do
          table.insert(result, div_block)
        end
        goto continue
      end

      -- Handle <div class="codeblock"> - convert to proper code block
      if block.classes[1] == "codeblock" then
        -- Extract text content from all Para blocks inside the div
        local code_text = ""
        for _, div_block in ipairs(block.content) do
          if div_block.t == "Para" then
            -- Convert Para content to plain text
            local text = pandoc.utils.stringify(div_block)
            if #code_text > 0 then
              code_text = code_text .. "\n"
            end
            code_text = code_text .. text
          elseif div_block.t == "CodeBlock" then
            -- Already a code block, use its text
            if #code_text > 0 then
              code_text = code_text .. "\n"
            end
            code_text = code_text .. div_block.text
          end
        end

        -- Create a proper CodeBlock with class "cpp"
        if #code_text > 0 then
          table.insert(result, pandoc.CodeBlock(code_text, {class = "cpp"}))
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

-- Return single filter
return {
  { Blocks = Blocks }
}
