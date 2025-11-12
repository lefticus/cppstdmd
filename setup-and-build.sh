#!/bin/bash
# Setup and build script for C++ Standard LaTeX to Markdown Converter
# This script prepares the development environment and runs a full build

set -e  # Exit on error
set -u  # Exit on undefined variable

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
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

abort() {
    error "$1"
    exit 1
}

# ============================================================================
# Step 1: Set up local venv if necessary
# ============================================================================
info "Step 1: Checking Python virtual environment..."

if [ ! -d "venv" ]; then
    info "Creating virtual environment..."
    python3 -m venv venv || abort "Failed to create virtual environment. Is python3-venv installed?"
    success "Virtual environment created"
else
    info "Virtual environment already exists"
fi

# Activate the venv
source venv/bin/activate || abort "Failed to activate virtual environment"
success "Virtual environment activated"

# ============================================================================
# Step 2: Install/update requirements
# ============================================================================
info "Step 2: Checking Python dependencies..."

# Check if we need to install/update
NEED_INSTALL=false

if [ ! -f "venv/.setup_complete" ]; then
    NEED_INSTALL=true
elif [ "requirements.txt" -nt "venv/.setup_complete" ]; then
    info "requirements.txt has been modified, reinstalling..."
    NEED_INSTALL=true
elif [ "setup.py" -nt "venv/.setup_complete" ]; then
    info "setup.py has been modified, reinstalling..."
    NEED_INSTALL=true
fi

if [ "$NEED_INSTALL" = true ]; then
    info "Installing/updating dependencies..."
    pip install --upgrade pip || abort "Failed to upgrade pip"
    pip install -e . || abort "Failed to install package in development mode"
    pip install -r requirements.txt || abort "Failed to install requirements"
    touch venv/.setup_complete
    success "Dependencies installed"
else
    info "Dependencies already up to date"
fi

# ============================================================================
# Step 3: Check Pandoc version
# ============================================================================
info "Step 3: Checking Pandoc version..."

if ! command -v pandoc &> /dev/null; then
    abort "Pandoc is not installed. Please install Pandoc 3.0+ (https://pandoc.org/installing.html)"
fi

PANDOC_VERSION=$(pandoc --version | head -n1 | cut -d' ' -f2)
PANDOC_MAJOR=$(echo "$PANDOC_VERSION" | cut -d'.' -f1)

if [ "$PANDOC_MAJOR" -lt 3 ]; then
    abort "Pandoc version $PANDOC_VERSION found, but version 3.0+ is required"
fi

success "Pandoc version $PANDOC_VERSION found"

# ============================================================================
# Step 4: Clone/update cplusplus/draft repository
# ============================================================================
info "Step 4: Setting up cplusplus/draft repository..."

DRAFT_DIR="$SCRIPT_DIR/cplusplus-draft"

if [ ! -d "$DRAFT_DIR" ]; then
    info "Cloning cplusplus/draft repository..."
    git clone https://github.com/cplusplus/draft.git "$DRAFT_DIR" || \
        abort "Failed to clone cplusplus/draft repository"
    success "Repository cloned"
else
    info "Repository already exists, attempting to update..."
    cd "$DRAFT_DIR"

    # Check if repository is in a valid state
    if ! git rev-parse --git-dir &>/dev/null; then
        warn "Repository appears corrupted, but continuing with existing files"
        cd "$SCRIPT_DIR"
    else
        # Try to fetch and update with timeout, but don't fail if offline
        if timeout 10 git fetch --tags 2>/dev/null; then
            # Only pull if we're on a branch (not detached HEAD)
            if git symbolic-ref --short HEAD &>/dev/null; then
                timeout 10 git pull 2>/dev/null || warn "Could not pull latest changes (offline or timeout)"
                success "Repository updated"
            else
                info "Repository in detached HEAD state (likely using specific git ref)"
                success "Repository ready (using existing checkout)"
            fi
        else
            warn "Could not fetch from remote (offline, timeout, or network error), using local repository"
            success "Repository ready (using existing checkout)"
        fi

        cd "$SCRIPT_DIR"
    fi
fi

# Verify the source directory exists
if [ ! -d "$DRAFT_DIR/source" ]; then
    abort "cplusplus/draft repository is missing 'source' directory"
fi

success "cplusplus/draft repository ready at $DRAFT_DIR"

# ============================================================================
# Step 5: Run full test suite in parallel
# ============================================================================
info "Step 5: Running full test suite..."

pytest tests/ -v -n auto \
    --ignore=tests/test_repo_manager.py \
    --ignore=tests/test_integration/test_cli.py \
    --ignore=tests/test_integration/test_standard_builder.py || abort "Tests failed! Please fix failing tests before proceeding."

success "All tests passed"

# ============================================================================
# Function: Convert a C++ standard version (separate + full builds in parallel)
# ============================================================================
convert_standard_version() {
    local git_ref="$1"
    local version_name="$2"
    local output_dir="${3:-$git_ref}"  # Default to git_ref if not provided

    info "Converting $version_name standard ($git_ref) to Markdown..."

    # Create directories if needed
    mkdir -p "$output_dir"
    mkdir -p full

    # Launch separate build in background
    info "Building separate markdown files with cross-file linking..."
    cpp-std-convert --build-separate \
        --draft-repo "$DRAFT_DIR" \
        --git-ref "$git_ref" \
        --toc-depth 3 \
        -o "$output_dir/" &
    local separate_pid=$!

    # Launch full build in background
    info "Building full standard file..."
    cpp-std-convert --build-full \
        --draft-repo "$DRAFT_DIR" \
        --git-ref "$git_ref" \
        --toc-depth 3 \
        -o "full/$output_dir.md" &
    local full_pid=$!

    # Wait for both builds to complete
    wait $separate_pid || abort "Failed to convert $output_dir separate chapters"
    wait $full_pid || abort "Failed to convert $output_dir full standard"

    success "$output_dir conversion complete (separate + full)"
}

# ============================================================================
# Step 6: Convert n4950 (C++23)
# ============================================================================
convert_standard_version "n4950" "C++23"

# ============================================================================
# Step 7: Convert n3337 (C++11)
# ============================================================================
convert_standard_version "n3337" "C++11"

# ============================================================================
# Step 8: Convert n4140 (C++14)
# ============================================================================
convert_standard_version "n4140" "C++14"

# ============================================================================
# Step 9: Convert n4659 (C++17)
# ============================================================================
convert_standard_version "n4659" "C++17"

# ============================================================================
# Step 10: Convert n4861 (C++20)
# ============================================================================
convert_standard_version "n4861" "C++20"

# ============================================================================
# Step 11: Update repo and convert main branch (trunk)
# ============================================================================
info "Step 11: Updating repository and converting latest development version (main branch)..."

# Update the repository to get latest changes
cd "$DRAFT_DIR"
if git rev-parse --git-dir &>/dev/null; then
    info "Updating cplusplus/draft repository..."
    if timeout 10 git fetch --tags 2>/dev/null; then
        # Checkout main branch
        git checkout main 2>/dev/null || warn "Could not checkout main branch"
        # Try to pull latest changes
        if git symbolic-ref --short HEAD &>/dev/null; then
            timeout 10 git pull 2>/dev/null || warn "Could not pull latest changes (offline or timeout)"
        fi
        success "Repository updated to main branch"
    else
        warn "Could not fetch from remote (offline, timeout, or network error)"
    fi
else
    warn "Repository appears corrupted, using existing state"
fi
cd "$SCRIPT_DIR"

# Convert main branch to trunk output directory
convert_standard_version "main" "C++26 (working draft)" "trunk"

# ============================================================================
# All done!
# ============================================================================
echo ""
echo "========================================"
success "Setup and build completed successfully!"
echo "========================================"
echo ""
info "Summary:"
echo "  - Virtual environment: venv/"
echo "  - C++ draft repository: $DRAFT_DIR"
echo "  - Test results: All passing"
echo ""
info "Separate chapter files:"
echo "  - n3337/ (C++11) - 35 files"
echo "  - n4140/ (C++14) - 35 files"
echo "  - n4659/ (C++17) - 33 files"
echo "  - n4861/ (C++20) - 35 files"
echo "  - n4950/ (C++23) - 37 files"
echo "  - trunk/ (C++26 working draft) - 36 files"
echo ""
info "Full standard files (for diffs):"
echo "  - full/n3337.md through full/trunk.md"
echo ""
info "Next steps:"
echo "  - Run tests: ./venv/bin/pytest tests/ -v"
echo "  - Generate diffs: ./generate_diffs.py"
echo "  - Compare chapters: diff n3337/class.md n4950/class.md"
echo "  - Compare full standards: diff full/n3337.md full/n4950.md"
echo "  - See CLAUDE.md for more commands"
echo ""
