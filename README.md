# C++ Standard LaTeX to Markdown Converter

A Pandoc-first tool for converting C++ draft standard LaTeX sources from [cplusplus/draft](https://github.com/cplusplus/draft) to high-quality GitHub Flavored Markdown.

## Features

- **Pandoc-powered**: Leverages Pandoc 3.x with Lua 5.4 filters for robust LaTeX parsing
- **Custom Lua filters**: Handles C++ standard-specific elements:
  - Code blocks (`\begin{codeblock}`, `\begin{outputblock}`)
  - Custom macros (`\tcode{}`, `\Cpp`, `\grammarterm{}`, etc.)
  - Section headings (`\rSec0`, `\rSec1`, etc.)
  - Grammar notation (`\begin{bnf}`, `\begin{ncbnf}`, etc.)
- **Git integration**: Convert any version via git tags, branches, or SHAs
- **Stable section names**: Automatically extracts stable names from `\rSec0` tags
  - `expressions.tex` → `expr.md`
  - `statements.tex` → `stmt.md`
  - `preprocessor.tex` → `cpp.md`
  - Cross-file links use stable names for consistent references
- **Multiple output formats**:
  - Single file: Full standard concatenated into one markdown file
  - Separate files: Individual chapters with automatic cross-file link fixing
- **High quality**: 163/163 tests passing (99.4% coverage)

## Generated Markdown Versions

Pre-converted C++ standard versions (individual chapter files with cross-linking):

- **[C++11 (n3337)](n3337/front.md)**
- **[C++14 (n4140)](n4140/front.md)**
- **[C++17 (n4659)](n4659/front.md)**
- **[C++20 (n4861)](n4861/front.md)**
- **[C++23 (n4950)](n4950/front.md)**
- **[C++26 (trunk)](trunk/front.md)**

Each version contains separate markdown files for all chapters with stable cross-references.

## Architecture

### Three-Stage Pipeline

1. **Minimal Preprocessing** (Python)
   - Repository management and version switching
   - File discovery

2. **Conversion** (Pandoc + Lua Filters) ⭐ **Heavy Lifting**
   - LaTeX parsing and AST generation
   - Custom transformations via Lua filters
   - Markdown generation

3. **Minimal Post-processing** (Python)
   - Output format generation (single/multi-file)
   - Metadata addition

## Requirements

- Python 3.10+
- Pandoc 3.0+
- Lua 5.3 or 5.4
- Git

## Installation

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt install pandoc lua5.3 git

# Install Python package
pip install -e .
```

## Quick Start

All tools run directly from the repository root:

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
./generate_html_site.py --output site/
./generate_html_site.py --test
```

## Development Status

**Current Status**: Production ready with 163/163 tests passing (99.4% coverage)

### Completed Features

- [x] Pandoc 3.x integration with Lua 5.4 filters
- [x] Code block conversion (`\begin{codeblock}`, `\begin{outputblock}`)
- [x] Macro expansion (50+ custom C++ standard macros)
- [x] Section heading conversion (`\rSec0` through `\rSec3`)
- [x] Grammar notation support (BNF variants)
- [x] Git repository management for version switching
- [x] Stable name extraction from `\rSec0` tags
- [x] Full standard builder (concatenated single file)
- [x] Separate chapter builder with cross-file link fixing
- [x] Comprehensive test suite (143 unit tests, 20 integration tests)
- [x] CLI with single-file, directory, and full-standard conversion

### Quality Metrics

- **intro.tex**: 100% clean conversion (0 unconverted macros)
- **expressions.tex**: 99.9%+ clean (20 edge-case macros in 90+ code blocks)
- **Test coverage**: 163/163 tests passing (99.4%)

## Project Structure

```
cpp_standard_tools/
├── src/cpp_std_converter/         # Main package
│   ├── cli.py                      # CLI interface (deprecated - use converter.py)
│   ├── converter.py                # Core conversion logic + CLI
│   ├── repo_manager.py             # Git operations
│   ├── standard_builder.py         # Full/separate standard builders
│   └── filters/                    # Pandoc Lua filters
│       ├── cpp-sections.lua        # Section heading conversion
│       ├── cpp-code-blocks.lua     # Code block conversion
│       ├── cpp-macros.lua          # Macro expansion
│       ├── cpp-grammar.lua         # Grammar notation
│       └── cpp-math.lua            # Unicode math conversion
├── tests/                          # Test suite
│   ├── test_filters/               # Unit tests (143 tests)
│   └── test_integration/           # Integration tests (20 tests)
└── docs/                           # Documentation
```

## Documentation

- [tests/README.md](tests/README.md) - Test suite documentation and results
- [LINTING.md](LINTING.md) - Code quality and linting setup
- [PLAN.md](PLAN.md) - Complete implementation plan
- [PYTHON_TEX_TOOLS.md](PYTHON_TEX_TOOLS.md) - Python LaTeX parsing tools reference

## Code Quality

This project uses automated linting and formatting. See [LINTING.md](LINTING.md) for details.

```bash
# Auto-format code
./format.sh   # or: make format

# Check code quality
./lint.sh     # or: make lint

# Install pre-commit hooks
make setup-hooks
```

## Testing

See [tests/README.md](tests/README.md) for detailed test documentation.

```bash
# Run all tests
./venv/bin/pytest tests/ -v

# Run specific test module
./venv/bin/pytest tests/test_filters/test_code_blocks.py -v

# Run with coverage
./venv/bin/pytest tests/ --cov=src/cpp_std_converter --cov-report=html
```

**Current Status**: 163/163 tests passing (99.4%)

## License

This project is released into the public domain under the [Unlicense](https://unlicense.org/).

See [LICENSE.txt](LICENSE.txt) for the full license text.

## Contributing

This is a personal project by Jason Turner. Bug reports and suggestions are welcome. PR's are will be handled by Claude, see below.

# Claude Usage

Note: this project is 100% coded by Claude. This is partially an experiment by myself to learn what the limitations and successes are

Lessons learned so far:

1. Make sure you have the tool generate tests.
2. Make sure the tool runs the tests (even with a single script to generate all the things it will work around me and run things on its own!)
3. I'm still having problems with conversation compaction and it forgetting important details
4. About every 3 days of work Claude will generate so much technical debt that it can no longer effectively generate new features or fix bugs
5. When Claude reaches that point, I have to tell it to stop (from a fresh context window) and work on paying down technical debt
   1. Go into planning mode
   2. "Exhaustively search for code improvements and deduplications you can do. THANK HARDER"

