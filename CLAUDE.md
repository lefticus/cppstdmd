# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CRITICAL INFORMATION FOR CLAUDE

**YOU WROTE THIS ENTIRE CODEBASE (100%)** - The user (lefticus) has only provided guidance and direction. You are responsible for all code, tests, documentation, and GitHub issue management. Remember this between sessions.

**ALWAYS TAKE RESPONSIBILITY FOR FAILING TESTS** - All tests pass at the start of every session unless the user explicitly states otherwise. If tests fail during your work, it is YOUR bug to fix. Do not try to make problems "not your problem."

## Repository Overview

This is a Pandoc-first tool for converting C++ draft standard LaTeX sources from the [cplusplus/draft](https://github.com/cplusplus/draft) repository to high-quality GitHub Flavored Markdown. The tool is production-ready with comprehensive test coverage.

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

# Install dependencies
pip install -r requirements.txt

# Clone cplusplus/draft repository (into project directory)
git clone https://github.com/cplusplus/draft.git cplusplus-draft
```

**Note:** The package is **not installed** - all scripts and tests run directly from the source directory. This eliminates confusion between installed and source files.

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
- `tests/test_filters/` - Unit tests for individual Lua filters
- `tests/test_integration/` - Integration tests using actual C++ standard files
- Other tests - Converter, repo manager, stable names, utils, etc.
- Integration tests use **n4950 (C++23)** as the stable baseline
- Tests look for `cplusplus-draft/` in the project directory (or fall back to `/tmp/cplusplus-draft/`)

## CLI Usage

All tools run directly from the repository root without installation. The `./setup-and-build.sh` script
sets up dependencies and runs the full conversion pipeline automatically.

**Main tools:**
- `./convert.py` - Convert C++ draft LaTeX to Markdown (wrapper for `src/cpp_std_converter/converter.py:main`)
- `./generate_diffs.py` - Generate diffs between C++ standard versions
- `./generate_html_site.py` - Generate HTML site from diffs

```bash
# Convert LaTeX to Markdown
./convert.py intro.tex -o intro.md
./convert.py --build-separate -o n4950/ --git-ref n4950
./convert.py --build-full -o full.md --git-ref n4950
./convert.py --list-tags

# Generate diffs between versions
./generate_diffs.py n3337 n4950
./generate_diffs.py --list

# Generate HTML site from diffs
./generate_html_site.py --output build/site/
./generate_html_site.py --test
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

Filters are applied in a specific order (see `self.filters` list in `converter.py`):

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

### Problem-Solving Approach: Check simplified_macros.tex First

**IMPORTANT:** When fixing LaTeX parsing issues, ALWAYS check if `src/cpp_std_converter/filters/simplified_macros.tex` can solve it first.

**Use simplified_macros.tex for:**
- LaTeX typesetting commands with no semantic meaning (`\@`, `\-`, `\linebreak`)
- Simple string replacements (`\Cpp` → `C++`)
- Macros that should be removed entirely

**Advantages:** One-line fix, happens before Pandoc parsing, cleaner than Lua filters or Python preprocessing.

**Recent example (Issue #77):** Fixed malformed table rows with `\renewcommand{\@}{}` instead of complex Python preprocessing.

### Stable Names

The tool automatically extracts "stable names" from `\rSec0` tags to generate consistent file names:
- `expressions.tex` → `expr.md`
- `statements.tex` → `stmt.md`
- `preprocessor.tex` → `cpp.md`

This enables stable cross-file linking when using `--build-separate` mode.

## Code Quality and Style

This project uses automated linting and formatting. See [LINTING.md](LINTING.md) for complete documentation.

**Quick commands:**
```bash
./format.sh  # Auto-format all code (Black + Ruff)
./lint.sh    # Run all linters (Black, Ruff, MyPy, Pytest)
make format  # Same as ./format.sh
make lint    # Same as ./lint.sh
```

**Tools configured:**
- **Black** - Python code formatter (line length: 100)
- **Ruff** - Fast Python linter (replaces flake8, isort, pyupgrade)
- **MyPy** - Static type checker (optional)
- **Luacheck** - Lua linter for Pandoc filters
- **Pre-commit hooks** - Automatic linting on git commit

**Configuration files:**
- `pyproject.toml` - Black, Ruff, MyPy, Pytest settings
- `.luacheckrc` - Luacheck settings for Lua filters
- `.pre-commit-config.yaml` - Pre-commit hooks

**Python version:** 3.10+

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
2. **Run `./format.sh` to auto-format code**
3. Add unit tests for your changes in `tests/test_filters/`
4. Run `./venv/bin/pytest tests/test_filters/your_test.py -v` to test iteratively
5. **Run `./lint.sh` to verify code quality**
6. **Run `./setup-and-build.sh` to test and regenerate with correct settings**
7. Review git diffs carefully to ensure:
   - Only expected files changed
   - No regressions in other files
   - Generated output looks correct
8. Stage changes: `git add <files>`
9. Commit (pre-commit hooks will run automatically if installed)

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
2. Use `-v` flag for verbose output: `./convert.py intro.tex -o intro.md -v`
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

## Generating Diffs Between Standard Versions

The `generate_diffs.py` script creates comprehensive diffs between C++ standard versions, useful for understanding language evolution.

### Quick Start

```bash
# Generate all default version pairs
./generate_diffs.py

# Generate specific version pair
./generate_diffs.py n3337 n4950     # C++11 → C++23

# List available versions
./generate_diffs.py --list
```

### What Gets Generated

For each version pair (e.g., `n3337_to_n4950/`):
- **README.md** - Summary with statistics and links to chapter diffs
- **Per-chapter diffs** (e.g., `class.diff`, `expr.diff`) - Render well on GitHub (<512 KB)
- **full_standard.diff** - Complete diff of all chapters (for local viewing, ~9 MB)

### Output Structure

```
diffs/
  n3337_to_n4140/        # C++11 → C++14
    README.md            # Summary with new/removed chapters, statistics
    class.diff           # Individual chapter diffs
    expr.diff
    ...
    full_standard.diff   # Complete standard diff
  n4950_to_trunk/        # C++23 → C++26 (latest)
    README.md
    ...
```

### Default Version Pairs

The script generates diffs for these pairs by default:
- `n3337 → n4140` - C++11 → C++14
- `n4140 → n4659` - C++14 → C++17
- `n4659 → n4861` - C++17 → C++20
- `n4861 → n4950` - C++20 → C++23
- `n4950 → trunk` - C++23 → C++26 (working draft)
- `n3337 → n4950` - C++11 → C++23 (major evolution)
- `n3337 → trunk` - C++11 → C++26 (complete evolution)

### Viewing Diffs

**On GitHub:**
```bash
# Per-chapter diffs render well (under 512 KB)
cat diffs/n3337_to_n4950/class.diff
```

**Locally:**
```bash
# View specific chapter diff with pager
less diffs/n3337_to_n4950/class.diff

# View with side-by-side comparison
diff -y n3337/class.md n4950/class.md | less

# View full standard diff (warning: large file)
less diffs/n3337_to_n4950/full_standard.diff

# Use git diff for better formatting
git diff --no-index --word-diff n3337/class.md n4950/class.md
```

### Summary File Format

Each `README.md` contains:
- **New Chapters** - Features added in the new version (e.g., concepts, ranges)
- **Removed Chapters** - Sections merged or restructured
- **Modified Chapters Table** - Size/line count changes with percentages
- **Links** - Direct links to individual chapter diffs

Example output:
```markdown
| Chapter | Old Size | New Size | Change | Old Lines | New Lines | Change |
|---------|----------|----------|--------|-----------|-----------|--------|
| class   | 95.1 KB  | 183.8 KB | +88.6 KB (+93.2%) | 2,744 | 5,775 | +3,031 (+110.5%) |
| containers | 215.0 KB | 543.7 KB | +328.7 KB (+152.9%) | 5,681 | 15,358 | +9,677 (+170.3%) |
```

### Requirements

Diffs require both separate chapter files AND full standard files:
- **Separate files**: Built by `./setup-and-build.sh` into `n3337/`, `n4950/`, etc.
- **Full files**: Built by `./setup-and-build.sh` (Step 12) into `full/n3337.md`, etc.

Both are generated automatically when you run `./setup-and-build.sh`.
