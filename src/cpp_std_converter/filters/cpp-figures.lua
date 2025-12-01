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

--[=[
cpp-figures.lua

Pandoc Lua filter to handle importgraphic figure markers in the C++ standard.

simplified_macros.tex converts:
  \begin{importgraphic}{CAPTION}{TAG}{FILE}\end{importgraphic}
to:
  @@FIGURE:TAG:FILE:CAPTION@@

This filter finds those markers and converts them to markdown figures:
  <a id="fig:TAG"></a>

  ![CAPTION [fig:TAG]](images/FILE.svg)

The marker is processed at the Para level because:
1. Multi-line captions get split across multiple Str elements
2. We need to return Block elements for proper paragraph separation
]=]

-- Check if content contains a figure marker
-- Uses two-step pattern to handle tags with colons (n3337 uses "fig:dag", n4950 uses "class.dag")
local function extract_figure_marker(text)
  -- Trim whitespace (multi-line markers have trailing space from SoftBreak)
  text = text:gsub("^%s+", ""):gsub("%s+$", "")

  -- Step 1: Split at .pdf: boundary to separate (tag:filename) from caption
  local before_caption, caption = text:match("^@@FIGURE:(.*%.pdf):(.+)@@$")
  if not before_caption then
    return nil
  end

  -- Step 2: Split tag from filename (filename is the last segment ending in .pdf)
  local tag, filename = before_caption:match("^(.+):([^:]+%.pdf)$")
  if not tag then
    return nil
  end

  return tag, filename, caption
end

-- Create figure blocks from marker data
local function create_figure(tag, filename, caption)
  -- Convert filename from .pdf to .svg
  local svg_filename = filename:gsub("%.pdf$", ".svg")

  -- Build the figure label, handling legacy tags that already have "fig:" prefix
  -- n3337 uses: {fig:dag}, n4950 uses: {class.dag}
  local fig_label
  if tag:match("^fig:") then
    fig_label = tag  -- Tag already has "fig:" prefix (n3337 style)
  else
    fig_label = "fig:" .. tag  -- Add "fig:" prefix (n4950 style)
  end

  -- Return list of blocks: anchor paragraph + figure paragraph
  return {
    pandoc.RawBlock('html', '<a id="' .. fig_label .. '"></a>'),
    pandoc.Para({
      pandoc.Image({pandoc.Str(caption .. ' [' .. fig_label .. ']')}, 'images/' .. svg_filename)
    })
  }
end

-- Process Para elements to find and extract figure markers
function Para(elem)
  -- Look for Spans containing figure markers
  local has_figure = false
  local before_content = {}
  local after_content = {}
  local figure_blocks = nil
  local found_figure = false

  for _, inline in ipairs(elem.content) do
    if inline.t == 'Span' and not found_figure then
      local text = pandoc.utils.stringify(inline)
      local tag, filename, caption = extract_figure_marker(text)
      if tag then
        found_figure = true
        figure_blocks = create_figure(tag, filename, caption)
        has_figure = true
      else
        table.insert(before_content, inline)
      end
    elseif found_figure then
      table.insert(after_content, inline)
    else
      table.insert(before_content, inline)
    end
  end

  if not has_figure then
    return elem
  end

  -- Build result: [before paragraph] + figure blocks + [after paragraph]
  local result = {}

  -- Add paragraph with content before figure (if any)
  if #before_content > 0 then
    -- Trim trailing whitespace from before content
    while #before_content > 0 and
          (before_content[#before_content].t == 'Space' or
           before_content[#before_content].t == 'SoftBreak') do
      table.remove(before_content)
    end
    if #before_content > 0 then
      table.insert(result, pandoc.Para(before_content))
    end
  end

  -- Add figure blocks
  for _, block in ipairs(figure_blocks) do
    table.insert(result, block)
  end

  -- Add paragraph with content after figure (if any)
  if #after_content > 0 then
    -- Trim leading whitespace from after content
    while #after_content > 0 and
          (after_content[1].t == 'Space' or
           after_content[1].t == 'SoftBreak') do
      table.remove(after_content, 1)
    end
    if #after_content > 0 then
      table.insert(result, pandoc.Para(after_content))
    end
  end

  return result
end

return {
  { Para = Para }
}
