# Linting and Code Quality

This project uses automated linting and formatting tools to maintain code quality.

## Quick Start

```bash
# Auto-format all code
./format.sh

# Check code quality
./lint.sh

# Or use Makefile shortcuts
make format
make lint
```

## Tools Used

### Python Tools

1. **Black** - Code formatter
   - Automatically formats Python code to a consistent style
   - Line length: 100 characters
   - Enforces double quotes, consistent indentation

2. **Ruff** - Fast Python linter
   - Checks for code quality issues
   - Enforces best practices (pycodestyle, pyflakes, isort)
   - Auto-fixes many issues with `--fix` flag

3. **MyPy** - Static type checker (optional)
   - Checks type hints for correctness
   - Helps catch type-related bugs early
   - Skipped in CI by default (set `SKIP_MYPY=0` to enable)

4. **isort** - Import sorter
   - Organizes imports into sections
   - Configured to work with Black

### Lua Tools

1. **Luacheck** - Lua linter
   - Lints all Pandoc Lua filters in `src/cpp_std_converter/filters/`
   - Configured for Pandoc globals in `.luacheckrc`
   - Install: `sudo apt install luacheck` or `luarocks install luacheck`

## Configuration Files

- `pyproject.toml` - Black, Ruff, MyPy, and Pytest configuration
- `.luacheckrc` - Luacheck configuration for Lua filters
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `Makefile` - Convenient command shortcuts

## Manual Linting

### Python

```bash
# Check formatting (without changing files)
./venv/bin/black --check src/ tests/ *.py

# Auto-format Python code
./venv/bin/black src/ tests/ *.py

# Run Ruff linter
./venv/bin/ruff check src/ tests/ *.py

# Auto-fix Ruff issues
./venv/bin/ruff check --fix src/ tests/ *.py

# Run type checker
./venv/bin/mypy src/

# Sort imports
./venv/bin/isort --profile black --line-length 100 src/ tests/ *.py
```

### Lua

```bash
# Lint all Lua filters
luacheck src/cpp_std_converter/filters/*.lua

# Lint specific filter
luacheck src/cpp_std_converter/filters/cpp-macros.lua
```

## Pre-commit Hooks

Pre-commit hooks automatically run linters before each commit.

### Installation

```bash
# Install hooks
make setup-hooks

# Or manually
./venv/bin/pre-commit install
```

### Usage

Once installed, hooks run automatically on `git commit`. To run manually:

```bash
# Run on all files
./venv/bin/pre-commit run --all-files

# Run on staged files only
./venv/bin/pre-commit run

# Run specific hook
./venv/bin/pre-commit run black
```

### Bypass Hooks (Emergency Only)

```bash
# Skip hooks for a single commit (not recommended)
git commit --no-verify -m "Emergency fix"
```

## IDE Integration

### VS Code

Install extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Black Formatter (ms-python.black-formatter)
- Ruff (charliermarsh.ruff)

Add to `.vscode/settings.json`:
```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### Neovim

Use null-ls or conform.nvim with Black and Ruff:
```lua
require("conform").setup({
  formatters_by_ft = {
    python = { "black", "isort" },
  },
})
```

## CI/CD Integration

The linting scripts are designed to work in CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Lint code
  run: |
    pip install -r requirements.txt
    ./lint.sh
```

## Troubleshooting

### "Black would reformat files"

Run `./format.sh` to auto-format all code.

### "Ruff found issues"

Most issues can be auto-fixed:
```bash
./venv/bin/ruff check --fix src/ tests/ *.py
```

### "MyPy type errors"

Type checking is optional. To skip:
```bash
SKIP_MYPY=1 ./lint.sh
```

### "Luacheck not found"

Luacheck is optional for Lua linting. Install with:
```bash
# Ubuntu/Debian
sudo apt install luacheck

# Using LuaRocks
luarocks install luacheck
```

## Code Quality Standards

### Python

- **Line length**: 100 characters
- **Quotes**: Double quotes for strings
- **Imports**: Sorted by isort, grouped into stdlib, third-party, first-party
- **Type hints**: Encouraged but not required
- **Docstrings**: Required for public functions and classes

### Lua

- **Line length**: 100 characters
- **Globals**: Only Pandoc-provided globals allowed
- **Unused variables**: Underscore-prefix for intentionally unused vars

## Excluded Directories

The following directories are excluded from linting:
- Generated markdown: `n3337/`, `n4140/`, `n4659/`, `n4861/`, `n4950/`, `trunk/`
- Build outputs: `diffs/`, `site/`, `full/`
- External repos: `cplusplus-draft/`
- Virtual env: `venv/`
