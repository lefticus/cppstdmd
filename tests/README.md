# Test Suite

## Running Tests

### Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Run All Tests

```bash
./venv/bin/pytest tests/ -v
```

### Run Specific Test Module

```bash
./venv/bin/pytest tests/test_filters/test_code_blocks.py -v
./venv/bin/pytest tests/test_filters/test_macros.py -v
./venv/bin/pytest tests/test_filters/test_grammar.py -v
```

### Run with Coverage

```bash
./venv/bin/pytest tests/ --cov=src/cpp_std_converter --cov-report=html
```

## Test Results

**Current Status**: 44/44 tests passing (100%) ✅

### Unit Tests: 27/27 passing ✅

#### test_code_blocks.py: 5/5 passing
- ✅ test_basic_codeblock
- ✅ test_codeblock_with_commentellip
- ✅ test_codeblock_with_tcode
- ✅ test_codeblocktu
- ✅ test_outputblock

#### test_grammar.py: 5/5 passing
- ✅ test_ncbnf_basic
- ✅ test_ncbnf_with_terminal
- ✅ test_ncbnf_with_opt
- ✅ test_ncsimplebnf
- ✅ test_ncrebnf

#### test_macros.py: 10/10 passing
- ✅ test_cpp_macro
- ✅ test_tcode_macro
- ✅ test_keyword_macro
- ✅ test_grammarterm_macro
- ✅ test_cpp_version_macros
- ✅ test_isoc_macro
- ✅ test_libheader_macro
- ✅ test_ref_macro
- ✅ test_defnx_macro
- ✅ test_defnadj_macro

#### test_sections.py: 7/7 passing
- ✅ test_rsec0_basic
- ✅ test_rsec1_nested
- ✅ test_rsec2_nested
- ✅ test_rsec3_deeply_nested
- ✅ test_multiple_sections
- ✅ test_section_with_complex_title
- ✅ test_section_in_context

### Integration Tests: 17/17 passing ✅

All integration tests use **n4950 (C++23)** as the stable baseline.

#### test_chapters.py: 7/7 passing
- ✅ test_intro_chapter
- ✅ test_basic_chapter
- ✅ test_expressions_chapter (90 code blocks)
- ✅ test_classes_chapter (137 code blocks)
- ✅ test_grammar_chapter (6 BNF blocks)
- ✅ test_no_empty_output
- ✅ test_macro_expansion

#### test_cli.py: 10/10 passing
- ✅ test_help_command
- ✅ test_single_file_to_stdout
- ✅ test_single_file_to_file
- ✅ test_verbose_mode
- ✅ test_list_tags
- ✅ test_git_ref_conversion
- ✅ test_directory_conversion
- ✅ test_missing_input_file
- ✅ test_directory_without_output
- ✅ test_invalid_git_ref

## Integration Testing

The filters have been tested on actual C++ standard chapters:
- intro.tex: ✅ Working
- lex.tex: ✅ Working
- basic.tex: ✅ Working
- expressions.tex: ✅ Working (106 code blocks recovered)
- grammar.tex: ✅ Working (6 grammar blocks recovered)
