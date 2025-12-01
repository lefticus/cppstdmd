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

  -- Pattern 1: Pandoc parses \rSec0[label]{Title} or \rSec{0}[label]{Title} as:
  --   Para [RawInline("\rSec0") or RawInline("\rSec{0}"), Str("[label]"), Span([Str("Title")]), SoftBreak, ...]
  -- Annexes have an @@ANNEX@@ marker before the \rSec{0}:
  --   Para [Str("@@ANNEX@@"), RawInline("\rSec{0}"), Str("[label]"), Span([Str("Title")])]
  -- When multiple sections appear consecutively, they're in the SAME Para element
  -- We need to extract ALL of them
  while i <= #content do
    -- Check for annex marker (@@ANNEX:informative@@ or @@ANNEX:normative@@)
    local annex_type = nil
    if content[i].t == "Str" and content[i].text:match("^@@ANNEX:(.+)@@$") then
      annex_type = content[i].text:match("^@@ANNEX:(.+)@@$")
      i = i + 1  -- Skip past marker
    end

    -- Check if current position starts a \rSecN or \rSec{N} pattern
    if content[i].t == "RawInline" and content[i].format == "latex" then
      local raw_text = content[i].text
      -- Match either \rSec0 or \rSec{0}
      local level = raw_text:match("^\\rSec(%d)$") or raw_text:match("^\\rSec%{(%d)%}$")

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

            -- For annexes, add the type designation to the title
            if annex_type then
              table.insert(title_content, pandoc.Space())
              table.insert(title_content, pandoc.Str("(" .. annex_type .. ")"))
            end

            -- Append visible anchor with stable name to heading
            -- Mark annexes with data-annex attribute for TOC generation
            table.insert(title_content, pandoc.Space())
            if annex_type then
              table.insert(title_content,
                           pandoc.RawInline('html', '<a id="' .. label .. '" data-annex="true" data-annex-type="' .. annex_type .. '">[[' ..
                                            label .. ']]</a>'))
            else
              table.insert(title_content,
                           pandoc.RawInline('html', '<a id="' .. label .. '">[[' ..
                                            label .. ']]</a>'))
            end

            -- Create the heading with embedded anchor
            local header = pandoc.Header(heading_level, title_content)
            table.insert(headers, header)

            -- Advance past the processed elements: RawInline + Str + Span
            i = i + 3

            -- Skip SoftBreak if present (separates sections in the same Para)
            if i <= #content and content[i].t == "SoftBreak" then
              i = i + 1
            end

            -- Check if next element is another section or if we should stop
            -- If it's not a section marker (@@ANNEX or \rSec), break to preserve remaining content
            if i <= #content then
              local next_elem = content[i]
              local is_section_start = false
              if next_elem.t == "Str" and next_elem.text:match("^@@ANNEX:") then
                is_section_start = true
              elseif next_elem.t == "RawInline" and next_elem.format == "latex" then
                local next_text = next_elem.text
                if next_text:match("^\\rSec%d$") or next_text:match("^\\rSec%{%d%}$") then
                  is_section_start = true
                end
              end
              if not is_section_start then
                break  -- Stop processing, remaining content is not a section
              end
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
        -- Track this section label for link definition generation
        section_labels[label] = true

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

        -- If we got content, convert to header with embedded anchor
        if #title_content > 0 then
          table.insert(title_content, pandoc.Space())
          table.insert(title_content,
                       pandoc.RawInline('html', '<a id="' .. label .. '">[[' ..
                                        label .. ']]</a>'))
          return pandoc.Header(heading_level, title_content)
        end
      end
    end

    i = i + 1
    ::continue::
  end

  -- If we extracted any headers, return them along with any remaining content
  if #headers > 0 then
    -- Check if there's remaining content after the extracted headers
    -- This handles cases like: \rSec2[label]{Title}\pnum Paragraph text...
    -- where the paragraph text should be preserved as a separate paragraph
    local remaining = {}
    while i <= #content do
      -- Skip leading whitespace and \pnum markers
      if content[i].t == "SoftBreak" or content[i].t == "Space" then
        i = i + 1
      elseif content[i].t == "RawInline" and content[i].format == "latex" and
             content[i].text == "\\pnum" then
        i = i + 1
      else
        break
      end
    end

    -- Collect remaining content
    while i <= #content do
      table.insert(remaining, content[i])
      i = i + 1
    end

    -- If there's remaining content, add it as a paragraph after the headers
    if #remaining > 0 then
      table.insert(headers, pandoc.Para(remaining))
    end

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

  -- Pattern 1: \rSecN[label]{title}
  local level, label, title = text:match("\\rSec(%d)%[([^%]]*)%]%{([^}]*)%}")
  if level and label and title then
    -- Track this section label for link definition generation
    section_labels[label] = true
    local heading_level = tonumber(level) + 1
    -- Create heading with embedded anchor
    local content = {
      pandoc.Str(title),
      pandoc.Space(),
      pandoc.RawInline('html', '<a id="' .. label .. '">[[' .. label .. ']]</a>')
    }
    return pandoc.Header(heading_level, content)
  end

  -- Pattern 2: \infannex{label}{title} or \normannex{label}{title}
  -- These are appendix-level sections (H1)
  local inf_label, inf_title = text:match("\\infannex%{([^}]*)%}%{([^}]*)%}")
  if inf_label and inf_title then
    -- Track this section label for link definition generation
    section_labels[inf_label] = true
    -- Create H1 heading with embedded anchor marked as informative annex
    local content = {
      pandoc.Str(inf_title),
      pandoc.Space(),
      pandoc.Str("(informative)"),
      pandoc.Space(),
      pandoc.RawInline('html', '<a id="' .. inf_label .. '" data-annex="true" data-annex-type="informative">[[' .. inf_label .. ']]</a>')
    }
    return pandoc.Header(1, content)
  end

  local norm_label, norm_title = text:match("\\normannex%{([^}]*)%}%{([^}]*)%}")
  if norm_label and norm_title then
    -- Track this section label for link definition generation
    section_labels[norm_label] = true
    -- Create H1 heading with embedded anchor marked as normative annex
    local content = {
      pandoc.Str(norm_title),
      pandoc.Space(),
      pandoc.Str("(normative)"),
      pandoc.Space(),
      pandoc.RawInline('html', '<a id="' .. norm_label .. '" data-annex="true" data-annex-type="normative">[[' .. norm_label .. ']]</a>')
    }
    return pandoc.Header(1, content)
  end

  return elem
end

function RawBlock(elem)
  if elem.format ~= 'latex' then
    return elem
  end

  local text = elem.text

  -- Pattern 1: \rSecN[label]{title}
  local level, label, title = text:match("\\rSec(%d)%[([^%]]*)%]%{([^}]*)%}")
  if level and label and title then
    -- Track this section label for link definition generation
    section_labels[label] = true
    local heading_level = tonumber(level) + 1
    -- Create heading with embedded anchor
    local content = {
      pandoc.Str(title),
      pandoc.Space(),
      pandoc.RawInline('html', '<a id="' .. label .. '">[[' .. label .. ']]</a>')
    }
    return pandoc.Header(heading_level, content)
  end

  -- Pattern 2: \infannex{label}{title} or \normannex{label}{title}
  -- These are appendix-level sections (H1)
  local inf_label, inf_title = text:match("\\infannex%{([^}]*)%}%{([^}]*)%}")
  if inf_label and inf_title then
    -- Track this section label for link definition generation
    section_labels[inf_label] = true
    -- Create H1 heading with embedded anchor marked as informative annex
    local content = {
      pandoc.Str(inf_title),
      pandoc.Space(),
      pandoc.Str("(informative)"),
      pandoc.Space(),
      pandoc.RawInline('html', '<a id="' .. inf_label .. '" data-annex="true" data-annex-type="informative">[[' .. inf_label .. ']]</a>')
    }
    return pandoc.Header(1, content)
  end

  local norm_label, norm_title = text:match("\\normannex%{([^}]*)%}%{([^}]*)%}")
  if norm_label and norm_title then
    -- Track this section label for link definition generation
    section_labels[norm_label] = true
    -- Create H1 heading with embedded anchor marked as normative annex
    local content = {
      pandoc.Str(norm_title),
      pandoc.Space(),
      pandoc.Str("(normative)"),
      pandoc.Space(),
      pandoc.RawInline('html', '<a id="' .. norm_label .. '" data-annex="true" data-annex-type="normative">[[' .. norm_label .. ']]</a>')
    }
    return pandoc.Header(1, content)
  end

  return elem
end

-- Export section_labels to metadata for use by cpp-macros.lua
-- This prevents duplicate link definitions
function Pandoc(doc)
  -- Convert section_labels table to a list and store in metadata
  local labels_list = {}
  for label, _ in pairs(section_labels) do
    table.insert(labels_list, label)
  end

  -- Store in document metadata so cpp-macros.lua can access it
  doc.meta['section_labels'] = labels_list

  return doc
end
