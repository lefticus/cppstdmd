-- .luacheckrc - Configuration for luacheck (Lua linter)

-- Lua version
std = "lua53+lua54"

-- Global options
max_line_length = 100
max_code_line_length = 100
max_string_line_length = 100
max_comment_line_length = 100

-- Pandoc globals that are available in filters
globals = {
    "pandoc",
    "PANDOC_VERSION",
    "PANDOC_API_VERSION",
    "PANDOC_SCRIPT_FILE",
    "PANDOC_STATE",
    "FORMAT",
    "PANDOC_WRITER_OPTIONS",
    -- Pandoc filter functions (element handlers - these are assigned by filters)
    "Str",
    "RawBlock",
    "RawInline",
    "CodeBlock",
    "Header",
    "Para",
    "Blocks",
    "BulletList",
    "OrderedList",
    "Pandoc",
    "Meta",
    "Math",
    "Code",
    "emph",
    "_",  -- Lodash-style utility or placeholder variable
    -- Custom globals used across filters
    "references",  -- Cross-reference tracking table (shared across filter files)
    "process_single_block",  -- Shared function across filters
}

-- Read-only pandoc globals (don't allow modification)
read_globals = {
    "pandoc",
    "PANDOC_VERSION",
    "PANDOC_API_VERSION",
    "PANDOC_SCRIPT_FILE",
    "PANDOC_STATE",
    "FORMAT",
    "PANDOC_WRITER_OPTIONS",
}

-- Files and directories to exclude
exclude_files = {
    "cplusplus-draft/",
    "n3337/",
    "n4140/",
    "n4659/",
    "n4861/",
    "n4950/",
    "trunk/",
    "full/",
    "diffs/",
    "build/",
    "venv/",
}

-- Warnings to ignore
ignore = {
    "211", -- Unused local variable (common in Pandoc filters)
    "212", -- Unused argument (common in filter functions)
    "213", -- Unused loop variable
}

-- Files to check
files = {
    "src/cpp_std_converter/filters/*.lua",
}
