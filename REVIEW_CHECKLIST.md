# n4950 Quality Review Checklist

## Purpose

Systematically review all converted markdown files for quality issues by comparing them against the source .tex files. Work through files from smallest to largest, one at a time.

## Workflow (for each file)

### 1. Compare Source and Output
- Read the .tex source file from `cplusplus-draft/source/`
- Read the .md output file from `n4950/`
- Look at structure, content, and formatting

### 2. Identify Issues
Look for:
- **Missing content** - sections, paragraphs, examples not converted
- **Unconverted LaTeX** - `\command{}` syntax still present
- **Broken code blocks** - malformed ``` blocks, incorrect language tags
- **Incorrect heading levels** - `#` count doesn't match structure
- **Missing cross-references** - `[label]` links broken or missing
- **Formatting problems** - lists, tables, notes, examples not rendering correctly
- **Math/symbols** - Unicode conversion issues

### 3. Categorize Issues
- **Filter bugs** - Problems in Lua filters that need code fixes
- **Systematic issues** - Patterns affecting multiple files (address once globally)
- **One-off quirks** - Edge cases specific to this file (document for later)

### 4. Discuss Findings
- Report findings to user
- User reviews all proposed changes
- **No commits without user approval**

### 5. Fix (if approved)
- For filter bugs: Update Lua filters, test, regenerate
- For one-offs: Document or make targeted fixes
- Re-run tests after any filter changes

### 6. Mark Complete
- Check off the file in the list below
- Document any patterns in "Issues Found" section

## Files to Review (37 total, smallest first)

- [x] `back.md` (1.0K) - ✅ FIXED: \doccite{} with nested \Cpp{} macro
- [x] `grammar.md` (1.5K) - ✅ Perfect, no issues
- [x] `uax31.md` (4.5K) - ✅ FIXED: \UAX{} and \unicode{}{} macros not being processed
- [x] `limits.md` (5.8K) - ✅ FIXED: \grammarterm{}{} with plural suffix dropping the suffix
- [ ] `module.md` (24K)
- [ ] `stmt.md` (32K)
- [ ] `except.md` (33K)
- [ ] `intro.md` (33K)
- [ ] `concepts.md` (41K)
- [ ] `cpp.md` (52K)
- [ ] `diagnostics.md` (54K)
- [ ] `lex.md` (57K)
- [ ] `meta.md` (58K)
- [ ] `future.md` (67K)
- [ ] `compatibility.md` (89K)
- [ ] `re.md` (95K)
- [ ] `library.md` (101K)
- [ ] `front.md` (114K)
- [ ] `over.md` (119K)
- [ ] `localization.md` (127K)
- [ ] `strings.md` (141K)
- [ ] `support.md` (160K)
- [ ] `class.md` (177K)
- [ ] `mem.md` (180K)
- [ ] `iterators.md` (191K)
- [ ] `basic.md` (219K)
- [ ] `numerics.md` (230K)
- [ ] `expr.md` (251K)
- [ ] `temp.md` (254K)
- [ ] `time.md` (257K)
- [ ] `dcl.md` (264K)
- [ ] `thread.md` (308K)
- [ ] `algorithms.md` (405K)
- [ ] `input.md` (413K)
- [ ] `utilities.md` (414K)
- [ ] `ranges.md` (415K)
- [ ] `containers.md` (543K)

## Issues Found

### Patterns Discovered

**Nested Macro Issue** - Macros that can contain other macros (like `\doccite{\Cpp{}}`) need brace-balanced parsing instead of simple `[^}]*` regex patterns.

**Multi-Argument Macros** - Some macros take optional second arguments for suffixes (like `\grammarterm{term}{s}` for plurals). These need special handling to extract both arguments and append the suffix after the emphasized term.

### Filter Improvements Needed

- [x] **FIXED**: `\doccite{}` and `\Fundescx{}` now use brace-balanced parsing (cpp-macros.lua lines 610-630)
- [x] **TEST ADDED**: `test_doccite_with_nested_cpp_macro` verifies the fix
- [x] **FIXED**: `\UAX{}` and `\unicode{}{}`macros now processed in RawInline handler (cpp-macros.lua lines 823-857)
- [x] **TEST ADDED**: `test_uax_macro` and `test_unicode_macro_with_description` verify the fix
- [x] **FIXED**: `\grammarterm{term}{suffix}` now handles optional suffix argument (cpp-macros.lua lines 641-660)
- [x] **TEST ADDED**: `test_grammarterm_with_suffix` verifies the fix
- [x] **IMPACT**: Affects 314 instances across the entire codebase

### Known Edge Cases

**Pandoc-Recognized LaTeX Commands** - Some LaTeX macros (like `\unicode`) are recognized by Pandoc's LaTeX reader and preserved as `RawInline` elements instead of `Str` elements. These need explicit handling in the `RawInline` function, not just in `expand_macros`.
