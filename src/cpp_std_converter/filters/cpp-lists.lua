-- cpp-lists.lua
-- Convert loose lists to tight lists by transforming Para blocks to Plain blocks
-- This removes blank lines between list items for better readability

-- Helper function to clean up leading whitespace after RawInline elements
local function clean_leading_whitespace(inlines)
  -- Remove leading SoftBreak/Space elements that follow RawInline elements that will be stripped
  -- This handles cases like \indextext{...}\n content which becomes RawInline, SoftBreak, content
  -- Only strip whitespace after macros that are known to be stripped (indextext, index, etc.)
  local i = 1
  while i <= #inlines do
    if inlines[i].t == "RawInline" then
      -- Get the LaTeX command text - Pandoc Lua API uses .text field
      local raw_text = inlines[i].text or ""
      -- Check if this is a macro that gets stripped (starts with \indextext or \index)
      local is_stripped_macro = raw_text:match("^\\index") ~= nil

      -- Skip over RawInline
      i = i + 1
      -- If this macro will be stripped and next element is SoftBreak or Space, remove it
      if is_stripped_macro and i <= #inlines and (inlines[i].t == "SoftBreak" or inlines[i].t == "Space") then
        table.remove(inlines, i)
        -- Don't increment i since we just removed an element
      end
    else
      -- Hit non-RawInline element, stop processing
      break
    end
  end
  return inlines
end

-- Helper function to merge multiple blocks in a list item into a single Plain block
local function merge_item_blocks(item)
  -- If item has only one block that's Para or Plain, just return it as Plain
  if #item == 1 then
    if item[1].t == "Para" then
      local content = clean_leading_whitespace(item[1].content)
      return {pandoc.Plain(content)}
    elseif item[1].t == "Plain" then
      local content = clean_leading_whitespace(item[1].content)
      return {pandoc.Plain(content)}
    else
      -- Single non-Para/Plain block (CodeBlock, BulletList, etc.) - preserve it
      return item
    end
  end

  -- Item has multiple blocks - try to merge them into one Plain block
  local merged_content = {}
  local has_non_mergeable = false
  local had_text_block = false  -- Track if we've seen Para/Plain blocks

  for j, block in ipairs(item) do
    if block.t == "Para" or block.t == "Plain" then
      -- Add a space before this block's content if we have any previous content
      if #merged_content > 0 then
        table.insert(merged_content, pandoc.Space())
      end
      -- Add content from Para/Plain blocks
      for _, inline in ipairs(block.content) do
        table.insert(merged_content, inline)
      end
      had_text_block = true
    elseif block.t == "RawBlock" and block.format == "latex" then
      -- Check if this is a footnote or other block-level environment
      -- These should not be merged into the list item content
      local raw_text = block.text or ""
      if raw_text:match("^\\begin{footnote}") or raw_text:match("^\\begin{note}") then
        -- Footnotes and notes should remain as separate blocks
        has_non_mergeable = true
        break
      end
      -- Convert LaTeX RawBlock to RawInline for later filter processing
      table.insert(merged_content, pandoc.RawInline("latex", raw_text))
    else
      -- Non-mergeable block type (CodeBlock, BulletList, etc.)
      has_non_mergeable = true
      break
    end
  end

  if has_non_mergeable then
    -- Can't merge - convert Para to Plain but preserve structure
    local new_item = {}
    for j, block in ipairs(item) do
      if block.t == "Para" then
        local content = clean_leading_whitespace(block.content)
        table.insert(new_item, pandoc.Plain(content))
      else
        table.insert(new_item, block)
      end
    end
    return new_item
  else
    -- Successfully merged into single block
    -- Clean up whitespace after index macros that will be stripped
    merged_content = clean_leading_whitespace(merged_content)
    return {pandoc.Plain(merged_content)}
  end
end

-- Process bullet lists
function BulletList(elem)
  local new_content = {}

  for i, item in ipairs(elem.content) do
    table.insert(new_content, merge_item_blocks(item))
  end

  elem.content = new_content
  return elem
end

-- Process ordered lists
function OrderedList(elem)
  local new_content = {}

  for i, item in ipairs(elem.content) do
    table.insert(new_content, merge_item_blocks(item))
  end

  elem.content = new_content
  return elem
end
