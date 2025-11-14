--[[
cpp-sections.lua

Pandoc Lua filter to convert C++ standard section headings to Markdown.

The C++ standard uses custom sectioning commands like \rSec0, \rSec1, etc.
which Pandoc doesn't recognize. Pandoc converts them to paragraphs with
the pattern: Para [ Str "[label]", ... "Title" ]

This filter detects this pattern and converts to proper headers:
  \rSec0[label]{Title} → # Title {#label}
  \rSec1[label]{Title} → ## Title {#label}
  etc.
]]

-- Global table to track all section labels for link definition generation
local section_labels = {}

-- Helper function to extract title text from paragraph content
local function extract_title(content)
  local title_parts = {}
  for i, elem in ipairs(content) do
    if elem.t == "Str" then
      table.insert(title_parts, elem.text)
    elseif elem.t == "Space" then
      table.insert(title_parts, " ")
    elseif elem.t == "Span" and elem.content then
      -- Extract from Span
      for _, inner in ipairs(elem.content) do
        if inner.t == "Str" then
          table.insert(title_parts, inner.text)
        end
      end
    end
  end
  return table.concat(title_parts)
end

-- Main filter for paragraphs that might be sections
function Para(elem)
  local content = elem.content
  local headers = {}
  local i = 1

  -- Pattern 1: Pandoc parses \rSec0[label]{Title} as:
  --   Para [RawInline("\rSec0"), Str("[label]"), Span([Str("Title")]), SoftBreak, ...]
  -- When multiple sections appear consecutively, they're in the SAME Para element
  -- We need to extract ALL of them
  while i <= #content do
    -- Check if current position starts a \rSecN pattern
    if content[i].t == "RawInline" and content[i].format == "latex" then
      local raw_text = content[i].text
      local level = raw_text:match("^\\rSec(%d)$")

      if level and i + 1 <= #content and content[i + 1].t == "Str" then
        -- Extract label from [label] string
        local label = content[i + 1].text:match("^%[([^%]]+)%]$")

        if label and i + 2 <= #content then
          -- Track this section label for link definition generation
          section_labels[label] = true

          -- Extract title content from the Span or remaining elements
          local title_content

          if content[i + 2].t == "Span" and content[i + 2].content then
            title_content = content[i + 2].content
          else
            -- If not a Span, this pattern didn't match, advance and continue
            i = i + 1
            goto continue
          end

          if #title_content > 0 then
            local heading_level = tonumber(level) + 1  -- rSec0 → H1, rSec1 → H2, etc.

            -- Append visible anchor with stable name to heading
            table.insert(title_content, pandoc.Space())
            table.insert(title_content,
                         pandoc.RawInline('html', '<a id="' .. label .. '">[[' ..
                                          label .. ']]</a>'))

            -- Create the heading with embedded anchor
            local header = pandoc.Header(heading_level, title_content)
            table.insert(headers, header)

            -- Advance past the processed elements: RawInline + Str + Span
            i = i + 3

            -- Skip SoftBreak if present (separates sections in the same Para)
            if i <= #content and content[i].t == "SoftBreak" then
              i = i + 1
            end

            goto continue
          end
        end
      end
    end

    -- Pattern 2: Fallback for "[label]Title" format (older approach)
    -- Only check this if we haven't found any \rSec patterns yet
    if #headers == 0 and i == 1 and content[i].t == "Str" then
      local first_str = content[i].text

      -- Match [label] pattern and extract label
      local label = first_str:match("^%[([^%]]+)%]$")

      if label then
        -- Determine heading level based on label structure
        -- Heuristic: count dots in label
        -- intro.scope (1 dot) → likely H1 (rSec0)
        -- intro.compliance.general (2 dots) → H2 (rSec1)
        -- etc.
        local _, dot_count = label:gsub("%.", "")
        local heading_level = math.min(dot_count + 1, 6)

        -- If we can't determine, default to H2
        if heading_level == 0 then
          heading_level = 2
        end

        -- Extract title from remaining content
        local title_content = {}
        for j = 2, #content do
          table.insert(title_content, content[j])
        end

        -- If we got content, convert to header
        if #title_content > 0 then
          return pandoc.Header(heading_level, title_content, {id = label})
        end
      end
    end

    i = i + 1
    ::continue::
  end

  -- If we extracted any headers, return them; otherwise keep original Para
  if #headers > 0 then
    return headers
  end

  return elem
end

-- Also handle raw LaTeX blocks/inlines for any that slip through
function RawInline(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text
  -- Pattern: \rSecN[label]{title}
  -- NOTE: Using ([^}]*) here is acceptable because section titles in the C++ standard
  -- are simple text without nested braces. The main Para() handler above processes
  -- the majority of sections; this is just a fallback for edge cases.
  local level, label, title = text:match("\\rSec(%d)%[([^%]]*)%]%{([^}]*)%}")

  if level and label and title then
    -- Track this section label for link definition generation
    section_labels[label] = true
    local heading_level = tonumber(level) + 1
    return pandoc.Header(heading_level, pandoc.Str(title), {id = label})
  end

  return elem
end

function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text
  -- Pattern: \rSecN[label]{title}
  -- NOTE: Using ([^}]*) here is acceptable - same reason as RawInline() above
  local level, label, title = text:match("\\rSec(%d)%[([^%]]*)%]%{([^}]*)%}")

  if level and label and title then
    -- Track this section label for link definition generation
    section_labels[label] = true
    local heading_level = tonumber(level) + 1
    return pandoc.Header(heading_level, pandoc.Str(title), {id = label})
  end

  return elem
end

-- Generate link definitions for all section labels
function Pandoc(doc)
  -- Convert section_labels table to sorted list
  local labels = {}
  for label, _ in pairs(section_labels) do
    table.insert(labels, label)
  end
  table.sort(labels)

  -- Only add definitions if we have sections
  if #labels > 0 then
    -- Add a separator comment
    local separator = pandoc.RawBlock('markdown', '\n<!-- Section link definitions -->')
    table.insert(doc.blocks, separator)

    -- Add each link definition
    for _, label in ipairs(labels) do
      local link_def = pandoc.RawBlock('markdown', '[' .. label .. ']: #' .. label)
      table.insert(doc.blocks, link_def)
    end
  end

  return doc
end
