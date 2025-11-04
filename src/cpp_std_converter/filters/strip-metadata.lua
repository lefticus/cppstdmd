-- strip-metadata.lua
-- Remove all metadata from the document output
--
-- This filter strips YAML front matter from the final markdown output.
-- Metadata is still available to all previous filters in the pipeline
-- (e.g., for cross-file linking), but is removed before writing the output.
--
-- Usage: Add this as the LAST filter in the pipeline

function Meta(meta)
  -- Return empty metadata block to strip all YAML front matter
  return {}
end
