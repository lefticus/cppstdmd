#!/bin/bash
# Script to fix all Lua linting warnings
set -e

echo "Fixing Lua linting warnings..."

# Directory where the filters are
FILTER_DIR="/home/jason/notes/cpp_standard_tools/converted/cppstdmd/src/cpp_std_converter/filters"

echo "✓ cpp-definitions.lua - already fixed"

echo "Fixing cpp-macros.lua shadowing warnings..."
# Fix shadowing warnings in cpp-macros.lua
sed -i '523s/local tcode_start,/local inner_tcode_start,/' "$FILTER_DIR/cpp-macros.lua"
sed -i '523s/\(tcode_start, tcode_end\)/inner_tcode_start, tcode_end/' "$FILTER_DIR/cpp-macros.lua"
sed -i '650s/local end_pos =/local inner_end_pos =/' "$FILTER_DIR/cpp-macros.lua"
sed -i '650s/end_pos = plural:find/inner_end_pos = plural:find/' "$FILTER_DIR/cpp-macros.lua"
sed -i '856s/local pos =/local check_pos =/' "$FILTER_DIR/cpp-macros.lua"
sed -i '929s/local pos =/local search_pos =/' "$FILTER_DIR/cpp-macros.lua"
sed -i '1017s/local text =/local block_text =/' "$FILTER_DIR/cpp-macros.lua"

echo "Fixing cpp-notes-examples.lua shadowing warnings..."
# Fix shadowing warnings in cpp-notes-examples.lua
sed -i '785s/local blocks =/local inner_blocks =/' "$FILTER_DIR/cpp-notes-examples.lua"
sed -i '854s/local blocks =/local inner_blocks2 =/' "$FILTER_DIR/cpp-notes-examples.lua"

echo "Fixing cpp-tables.lua shadowing warnings..."
# Fix shadowing warnings in cpp-tables.lua
sed -i '583s/local pos =/local search_pos =/' "$FILTER_DIR/cpp-tables.lua"
sed -i '611s/local end_pos =/local match_end =/' "$FILTER_DIR/cpp-tables.lua"
sed -i '623s/local end_pos =/local match_end2 =/' "$FILTER_DIR/cpp-tables.lua"
sed -i '635s/local end_pos =/local match_end3 =/' "$FILTER_DIR/cpp-tables.lua"
sed -i '647s/local end_pos =/local match_end4 =/' "$FILTER_DIR/cpp-tables.lua"
sed -i '791s/local end_pos =/local row_end_pos =/' "$FILTER_DIR/cpp-tables.lua"
sed -i '1076s/local header_line =/local header_pattern =/' "$FILTER_DIR/cpp-tables.lua"
sed -i '1137s/local header_line =/local header_pattern2 =/' "$FILTER_DIR/cpp-tables.lua"
sed -i '1206s/local header_line =/local header_pattern3 =/' "$FILTER_DIR/cpp-tables.lua"

echo "Fixing cpp-lists.lua unused variable warning..."
# Fix unused variable in cpp-lists.lua
sed -i '52s/local had_text_block =/local _had_text_block =/' "$FILTER_DIR/cpp-lists.lua"

echo "Fixing cpp-sections.lua unused variable warning..."
# Fix unused variable in cpp-sections.lua
sed -i '64s/local title_content =/local _title_content =/' "$FILTER_DIR/cpp-sections.lua"

echo "Fixing cpp-common.lua empty if branch warning..."
# Fix empty if branch in cpp-common.lua
sed -i '1371s/else$/else  -- Base case: no special ref handling needed/' "$FILTER_DIR/cpp-common.lua"

echo "Done! Running luacheck to verify..."
luacheck "$FILTER_DIR"/*.lua || true
