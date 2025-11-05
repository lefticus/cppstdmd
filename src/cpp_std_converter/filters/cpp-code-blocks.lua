--[[
cpp-code-blocks.lua

Pandoc Lua filter to handle C++ standard codeblock environments.

The C++ standard uses \begin{codeblock}...\end{codeblock} which is defined
via \lstnewenvironment from the listings package. Pandoc doesn't recognize
this and drops all code blocks, resulting in massive content loss.

This filter intercepts raw LaTeX blocks, detects codeblock environments,
extracts the code, and converts them to proper Markdown code blocks.
]]

-- Add current directory to Lua search path for local modules
local script_dir = debug.getinfo(1, "S").source:match("@?(.*/)") or "./"
package.path = package.path .. ";" .. script_dir .. "?.lua"

-- Import shared utilities
local common = require("cpp-common")
local subscripts = common.subscripts
local remove_font_switches = common.remove_font_switches
local trim = common.trim
local expand_cpp_version_macros = common.expand_cpp_version_macros
local expand_concept_macros = common.expand_concept_macros
local convert_cross_references_in_code = common.convert_cross_references_in_code
local expand_library_spec_macros = common.expand_library_spec_macros

-- Helper function to handle layout overlap commands
local function handle_overlap_commands(text)
  text = text:gsub("\\rlap{([^}]+)}", "%1")
  text = text:gsub("\\llap{([^}]+)}", "%1")
  text = text:gsub("\\clap{([^}]+)}", "%1")
  return text
end

-- trim is now imported from cpp-common
-- Note: trim_code used to use gsub with %s+ instead of %s*,
-- but trim() from common uses the more standard pattern

-- Helper function to convert math patterns in code
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

    -- Convert standalone subscripts: X_{n} → Xₙ
    math_content = math_content:gsub("([%w]+)_{{?([%w]+)}?}", function(name, sub)
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

  -- Convert standalone @\vdots@ to Unicode vertical ellipsis
  text = text:gsub("@\\vdots@", "⋮")
  text = text:gsub("\\vdots", "⋮")

  -- Convert standalone @\ldots@ to Unicode ellipsis
  text = text:gsub("@\\ldots@", "…")
  text = text:gsub("\\ldots", "…")

  return text
end

-- Helper function to clean up LaTeX escapes in code
local function clean_code(code)
  -- Remove @ escape delimiters and expand common macros

  -- First, convert math patterns (@$...$@) before processing other escapes
  code = convert_math_in_code(code)

  -- \commentellip represents "..."
  code = code:gsub("@\\commentellip@", "...")

  -- Expand macros in multiple passes to handle nesting (e.g., \tcode{\keyword{x}})
  -- Run until no more changes occur (max 5 passes to prevent infinite loops)
  local max_passes = 5
  for pass = 1, max_passes do
    local old_code = code

    -- \tcode{x} represents inline code (just extract the content)
    -- Handle both @\tcode{x}@ and bare \tcode{x} (in comments)
    code = code:gsub("@\\tcode{([^}]*)}@", "%1")
    code = code:gsub("\\tcode{([^}]*)}", "%1")

    -- \placeholder{x}{} or \placeholder{x} represents a placeholder
    -- Handle with empty braces first (order matters!)
    code = code:gsub("@\\placeholder{([^}]*)}{}@", "%1")
    code = code:gsub("@\\placeholder{([^}]*)}@", "%1")
    code = code:gsub("\\placeholder{([^}]*)}{}",  "%1")
    code = code:gsub("\\placeholder{([^}]*)}", "%1")

    -- \placeholdernc{x}{} or \placeholdernc{x} represents a placeholder (non-code variant)
    -- Handle with empty braces first (order matters!)
    code = code:gsub("@\\placeholdernc{([^}]*)}{}@", "%1")
    code = code:gsub("@\\placeholdernc{([^}]*)}@", "%1")
    code = code:gsub("\\placeholdernc{([^}]*)}{}",  "%1")
    code = code:gsub("\\placeholdernc{([^}]*)}", "%1")

    -- \exposid{x} represents exposition-only identifier
    code = code:gsub("@\\exposid{([^}]*)}@", "%1")
    code = code:gsub("\\exposid{([^}]*)}", "%1")

    -- \keyword{x} in code comments
    code = code:gsub("\\keyword{([^}]*)}", "%1")

    -- \texttt{x} in code comments (font switch, just extract content)
    code = code:gsub("\\texttt{([^}]*)}", "%1")

    -- \grammarterm{x} in code comments
    code = code:gsub("\\grammarterm{([^}]*)}", "%1")

    -- \term{x} in code comments
    code = code:gsub("\\term{([^}]*)}", "%1")

    -- If nothing changed, we're done
    if code == old_code then
      break
    end
  end

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

  -- Remove any @ delimiters first (escape markers from listings package)
  code = code:gsub("@([^@]*)@", "%1")

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

-- Main filter function for raw blocks
function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Only process blocks that are STANDALONE code blocks (codeblock, outputblock, etc.)
  -- If the block contains other LaTeX environments (description, note, example, etc.),
  -- let other filters handle it. Check if block is primarily a code block by verifying
  -- it starts with \begin{codeblock*} or \begin{outputblock} (after whitespace).
  local trimmed = text:match("^%s*(.-)%s*$")
  if not (trimmed:match("^\\begin{codeblock") or
          trimmed:match("^\\begin{outputblock") or
          trimmed:match("^\\begin{codeblocktu}") or
          trimmed:match("^\\begin{codeblockdigitsep}")) then
    -- Not a standalone code block, skip it
    return elem
  end

  -- Match \begin{codeblock}...\end{codeblock}
  -- Using .* to match any content (non-greedy)
  local code = text:match("\\begin{codeblock}(.-)\\end{codeblock}")

  if code then
    -- Clean up the code
    code = clean_code(code)
    code = trim(code)

    -- Return as a code block with cpp language
    return pandoc.CodeBlock(code, {class = "cpp"})
  end

  -- Match \begin{codeblocktu}...\end{codeblocktu}
  -- (codeblock with title - translation unit)
  code = text:match("\\begin{codeblocktu}{[^}]*}(.-)\\end{codeblocktu}")

  if code then
    code = clean_code(code)
    code = trim(code)
    return pandoc.CodeBlock(code, {class = "cpp"})
  end

  -- Match \begin{outputblock}...\end{outputblock}
  -- (program output, not C++ code)
  code = text:match("\\begin{outputblock}(.-)\\end{outputblock}")

  if code then
    code = clean_code(code)
    code = trim(code)
    return pandoc.CodeBlock(code, {class = "text"})  -- Use "text" class for output
  end

  -- Match \begin{codeblockdigitsep}...\end{codeblockdigitsep}
  -- (code block with digit separators)
  code = text:match("\\begin{codeblockdigitsep}(.-)\\end{codeblockdigitsep}")

  if code then
    code = clean_code(code)
    code = trim(code)
    return pandoc.CodeBlock(code, {class = "cpp"})
  end

  -- If no match, return unchanged
  return elem
end

-- Handler for CodeBlock elements that may contain LaTeX commands
-- This catches code blocks that were converted by Pandoc or earlier filters
-- but still have LaTeX formatting commands in them
function CodeBlock(elem)
  local code = elem.text

  -- Check if this code block has LaTeX commands that need cleaning
  if code:match("\\rlap") or code:match("\\llap") or code:match("\\clap") or
     code:match("\\normalfont") or code:match("\\itshape") or code:match("\\rmfamily") or code:match("\\bfseries") then

    -- Remove font switch commands
    code = remove_font_switches(code)

    -- Handle layout overlap commands
    code = handle_overlap_commands(code)

    -- Return updated code block
    return pandoc.CodeBlock(code, elem.attr)
  end

  return elem
end

-- Note: We don't handle inline \tcode{} here because cpp-macros.lua
-- handles it with proper nested macro expansion. This filter only
-- handles code blocks (codeblock, codeblocktu, codeblockdigitsep, outputblock).
