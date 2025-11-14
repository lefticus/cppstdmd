#!/bin/bash
# format.sh - Auto-format all code in the repository

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "========================================="
info "Auto-formatting Python code"
echo "========================================="
echo ""

# 1. Black - Python formatter
info "Running Black (Python formatter)..."
./venv/bin/black src/ tests/ *.py
success "Black formatting complete"
echo ""

# 2. Ruff - Python linter with auto-fix
info "Running Ruff (Python linter with auto-fix)..."
./venv/bin/ruff check --fix src/ tests/ *.py || true
success "Ruff auto-fix complete"
echo ""

# 3. isort - Import sorting
info "Running isort (import sorter)..."
./venv/bin/python -m isort --profile black --line-length 100 src/ tests/ *.py 2>/dev/null || {
    # isort might not be installed, that's okay
    info "isort not available, skipping import sorting"
}
echo ""

echo "========================================="
success "Auto-formatting complete!"
info "Run './lint.sh' to verify code quality"
echo "========================================="
