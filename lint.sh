#!/bin/bash
# lint.sh - Run all linters on the codebase

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Track failures
FAILURES=0

echo "========================================="
info "Running Python linters and formatters"
echo "========================================="
echo ""

# 1. Black - Python formatter (check mode)
info "Running Black (Python formatter)..."
if ./venv/bin/black --check --diff src/ tests/ *.py 2>/dev/null; then
    success "Black: All files properly formatted"
else
    error "Black: Some files need formatting"
    warn "Run './venv/bin/black src/ tests/ *.py' to auto-format"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# 2. Ruff - Python linter
info "Running Ruff (Python linter)..."
if ./venv/bin/ruff check src/ tests/ *.py; then
    success "Ruff: No issues found"
else
    error "Ruff: Issues found"
    warn "Run './venv/bin/ruff check --fix src/ tests/ *.py' to auto-fix"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# 3. MyPy - Python type checker (optional, can be slow)
if [ "${SKIP_MYPY}" != "1" ]; then
    info "Running MyPy (Python type checker)..."
    if ./venv/bin/mypy src/ 2>/dev/null; then
        success "MyPy: No type errors found"
    else
        warn "MyPy: Type errors found (optional check)"
        # Don't count as failure since type hints are optional
    fi
    echo ""
else
    warn "Skipping MyPy (set SKIP_MYPY=0 to enable)"
    echo ""
fi

# 4. Pytest - Run tests
info "Running Pytest (test suite)..."
if ./venv/bin/pytest tests/ -q --tb=line; then
    success "Pytest: All tests passed"
else
    error "Pytest: Some tests failed"
    FAILURES=$((FAILURES + 1))
fi
echo ""

# 5. Luacheck - Lua linter (if available)
if command -v luacheck &> /dev/null; then
    info "Running Luacheck (Lua linter)..."
    if luacheck src/cpp_std_converter/filters/*.lua; then
        success "Luacheck: No issues found"
    else
        error "Luacheck: Issues found in Lua files"
        FAILURES=$((FAILURES + 1))
    fi
    echo ""
else
    warn "Luacheck not installed (install with: sudo apt install luacheck or luarocks install luacheck)"
    warn "Skipping Lua linting"
    echo ""
fi

# Summary
echo "========================================="
if [ $FAILURES -eq 0 ]; then
    success "All linters passed!"
    echo "========================================="
    exit 0
else
    error "$FAILURES linter(s) failed"
    echo "========================================="
    exit 1
fi
