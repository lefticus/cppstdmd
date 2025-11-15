#!/bin/bash
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <https://unlicense.org>

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
