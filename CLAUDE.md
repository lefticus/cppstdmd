# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Pandoc-first tool for converting C++ draft standard LaTeX sources from the [cplusplus/draft](https://github.com/cplusplus/draft) repository to high-quality GitHub Flavored Markdown. The tool is production-ready with 163/163 tests passing and 99.4% code coverage.

## Quick Start

**ALWAYS run this script at the start of every development session:**

```bash
./setup-and-build.sh
```

This is the **standard entry point** for all development work. The script:
1. Creates/activates local `venv` if needed
2. Installs/updates Python dependencies (smart timestamp checking - skips if up-to-date)
3. Verifies Pandoc 3.0+ is available
4. Clones/updates `cplusplus-draft` repository into project directory
5. Runs full test suite in parallel (**aborts on any test failure**)
6. Converts n4950 (C++23) to markdown in `n4950/` directory

**Why use this script:**
- ✅ Idempotent - safe to run repeatedly (skips unnecessary work)
- ✅ Fast when already set up (checks timestamps, only updates what changed)
- ✅ Works offline (if cplusplus-draft already exists)
- ✅ Guarantees tests pass before proceeding
- ✅ Ensures consistent environment across all development sessions

**Do not skip this step.** Even if you think everything is set up, run it to verify the environment is correct.

## Development Setup (Manual)

If you need manual control instead of using `setup-and-build.sh`:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install dependencies
pip install -r requirements.txt

# Clone cplusplus/draft repository (into project directory)
git clone https://github.com/cplusplus/draft.git cplusplus-draft
```

## Testing

**Note:** `./setup-and-build.sh` runs the full test suite automatically. Use these commands for manual testing during development:

```bash
# Run all tests
./venv/bin/pytest tests/ -v

# Run specific test module
./venv/bin/pytest tests/test_filters/test_code_blocks.py -v
./venv/bin/pytest tests/test_filters/test_macros.py -v
./venv/bin/pytest tests/test_integration/test_chapters.py -v

# Run with coverage report
./venv/bin/pytest tests/ --cov=src/cpp_std_converter --cov-report=html

# Run tests in parallel (faster for full suite)
./venv/bin/pytest tests/ -v -n auto
```

**Test Structure:**
- `tests/test_filters/` - Unit tests for individual Lua filters (143 tests)
- `tests/test_integration/` - Integration tests using actual C++ standard files (20 tests)
- Integration tests use **n4950 (C++23)** as the stable baseline
- Tests look for `cplusplus-draft/` in the project directory (or fall back to `/tmp/cplusplus-draft/`)

## CLI Usage

**Note:** After running `./setup-and-build.sh`, the `cpp-std-convert` command will be available in your venv.

The primary command is `cpp-std-convert` (entry point: `src/cpp_std_converter/converter.py:main`):

```bash
# Convert single file to stdout
cpp-std-convert intro.tex

# Convert single file to output file
cpp-std-convert intro.tex -o intro.md

# Convert directory of .tex files
cpp-std-convert cplusplus-draft/source -o ./output

# Build full standard (all chapters concatenated)
cpp-std-convert --build-full --draft-repo cplusplus-draft -o full_standard.md --git-ref n4950

# Build separate markdown files with cross-file linking
cpp-std-convert --build-separate --draft-repo cplusplus-draft -o output_dir/ --git-ref n4950

# Use custom draft repository location
cpp-std-convert --build-full --draft-repo /path/to/draft -o output.md --git-ref n4950

# Convert specific C++ standard version
cpp-std-convert intro.tex --git-ref n4950 -o intro_cpp23.md

# List available version tags
cpp-std-convert --list-tags

# Verbose output for debugging
cpp-std-convert intro.tex -o intro.md -v
```

## Architecture

### Three-Stage Pipeline

1. **Minimal Preprocessing** (Python) - Repository management and file discovery
2. **Conversion** (Pandoc + Lua Filters) - **Heavy lifting** happens here: LaTeX parsing, AST transformations, Markdown generation
3. **Minimal Post-processing** (Python) - Output format generation and metadata

### Core Components

- `src/cpp_std_converter/converter.py` - Main conversion logic + CLI (entry point)
- `src/cpp_std_converter/repo_manager.py` - Git operations for cplusplus/draft repo
- `src/cpp_std_converter/standard_builder.py` - Builds full/separate standard documents
- `src/cpp_std_converter/stable_name.py` - Extracts stable names from `\rSec0` tags
- `src/cpp_std_converter/label_indexer.py` - Cross-reference link management
- `src/cpp_std_converter/filters/*.lua` - Pandoc Lua filters for LaTeX transformations

### Lua Filter Pipeline

Filters are applied in a specific order (defined in `converter.py:44-57`):

1. `cpp-sections.lua` - Section heading conversion (`\rSec0` through `\rSec3`)
2. `cpp-itemdecl.lua` - Item declarations and descriptions
3. `cpp-code-blocks.lua` - Code blocks (`\begin{codeblock}`, `\begin{outputblock}`)
4. `cpp-definitions.lua` - Definition blocks
5. `cpp-notes-examples.lua` - Notes and examples
6. `cpp-lists.lua` - List merging (runs early before macro/grammar processing)
7. `cpp-macros.lua` - 50+ custom C++ standard macros (`\tcode{}`, `\Cpp`, etc.)
8. `cpp-math.lua` - Unicode math conversion
9. `cpp-grammar.lua` - Grammar notation (BNF variants)
10. `cpp-tables.lua` - Table processing

**Order matters** - do not reorder filters without understanding dependencies.

### Stable Names

The tool automatically extracts "stable names" from `\rSec0` tags to generate consistent file names:
- `expressions.tex` → `expr.md`
- `statements.tex` → `stmt.md`
- `preprocessor.tex` → `cpp.md`

This enables stable cross-file linking when using `--build-separate` mode.

## Code Style

- Formatting: Black (configured in requirements.txt)
- Linting: Ruff (configured in requirements.txt)
- Python version: 3.10+

## External Dependencies

**Required system packages:**
- Pandoc 3.0+ (LaTeX → Markdown conversion)
- Lua 5.3 or 5.4 (for Pandoc filters)
- Git (for cplusplus/draft repo management)

**Python packages:** See `requirements.txt`

## Common Development Workflows

**Start every workflow by running `./setup-and-build.sh` first.**

### Making Changes and Committing

**CRITICAL:** Always follow this workflow before committing any changes to filters or code that affects output:

1. Make your code changes
2. Add unit tests for your changes in `tests/test_filters/`
3. Run `./venv/bin/pytest tests/test_filters/your_test.py -v` to test iteratively
4. **Run `./setup-and-build.sh` to test and regenerate with correct settings**
5. Review git diffs carefully to ensure:
   - Only expected files changed
   - No regressions in other files
   - Generated output looks correct
6. Stage changes: `git add <files>`
7. Commit only if everything looks good

**Why this matters:** The script runs the full test suite AND regenerates the n4950 output with your preferred settings. Skipping this step risks committing broken output or missing regressions.

### Adding a New Filter

1. Run `./setup-and-build.sh` to ensure environment is ready
2. Create the filter in `src/cpp_std_converter/filters/`
3. Add it to the filter list in `converter.py` in the correct order
4. Add unit tests in `tests/test_filters/`
5. Run `./venv/bin/pytest tests/test_filters/your_test.py -v` to test iteratively
6. **Run `./setup-and-build.sh` before committing** (see "Making Changes and Committing" above)

### Debugging Conversion Issues

1. Run `./setup-and-build.sh` first to ensure environment is correct
2. Use `-v` flag for verbose output: `cpp-std-convert intro.tex -o intro.md -v`
3. Test with small LaTeX snippets in unit tests first
4. Check filter order - later filters don't see earlier transformations
5. Integration tests use n4950 as the stable baseline
6. After fixes, **run `./setup-and-build.sh` before committing** (see "Making Changes and Committing" above)

### Working with Git Refs

The `--git-ref` parameter accepts:
- Tags: `n4950`, `n4971`, etc.
- Branches: `main`, `feature-branch`
- SHAs: `abc123def`

Use `--list-tags` to see available C++ standard versions.
