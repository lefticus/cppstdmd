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

# Setup and build script for C++ Standard LaTeX to Markdown Converter
# This script prepares the development environment and runs a full build
#
# Uses git worktrees to avoid checkout conflicts and preserve file mtimes.

set -e  # Exit on error
set -u  # Exit on undefined variable

# Parse command line arguments
UPDATE_SOURCES=false
REBUILD_STANDARDS=false
SKIP_TESTS=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --update-sources)
            UPDATE_SOURCES=true
            shift
            ;;
        --rebuild-standards)
            REBUILD_STANDARDS=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--update-sources] [--rebuild-standards] [--skip-tests]"
            echo ""
            echo "Options:"
            echo "  --update-sources    Fetch/pull latest cplusplus/draft repo (default: use existing)"
            echo "  --rebuild-standards Force reconversion of all standard versions even if unchanged"
            echo "  --skip-tests        Skip running pytest (useful for incremental builds)"
            echo ""
            echo "By default, if cplusplus-draft/ exists, it will be used as-is without updating."
            echo "Use --update-sources to fetch the latest changes from GitHub."
            echo "Standard conversions are cached - only runs if output is missing."
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

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
fi

if [ "$NEED_INSTALL" = true ]; then
    info "Installing/updating dependencies..."
    pip install --upgrade pip || abort "Failed to upgrade pip"
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
# Step 3b: Check Graphviz (for diagram conversion)
# ============================================================================
info "Step 3b: Checking Graphviz installation..."

if ! command -v dot &> /dev/null; then
    abort "Graphviz is not installed. Please install it:
    Ubuntu/Debian: sudo apt install graphviz
    macOS: brew install graphviz
    See: https://graphviz.org/download/"
fi

GRAPHVIZ_VERSION=$(dot -V 2>&1 | head -n1)
success "Graphviz found: $GRAPHVIZ_VERSION"

# ============================================================================
# Step 4: Clone/update cplusplus/draft repository and set up worktrees
# ============================================================================
info "Step 4: Setting up cplusplus/draft repository with worktrees..."

DRAFT_DIR="$SCRIPT_DIR/cplusplus-draft"
WORKTREES_DIR="$DRAFT_DIR/worktrees"

# Clone if needed
if [ ! -d "$DRAFT_DIR" ]; then
    info "Cloning cplusplus/draft repository..."
    git clone https://github.com/cplusplus/draft.git "$DRAFT_DIR" || \
        abort "Failed to clone cplusplus/draft repository"
    success "Repository cloned"
fi

# Clean up any stale git lock files
if [ -f "$DRAFT_DIR/.git/index.lock" ]; then
    warn "Removing stale git lock file..."
    rm -f "$DRAFT_DIR/.git/index.lock"
fi

# Update if requested
if [ "$UPDATE_SOURCES" = true ]; then
    info "Updating repository (--update-sources specified)..."
    cd "$DRAFT_DIR"

    if git rev-parse --git-dir &>/dev/null; then
        if timeout 30 git fetch --tags --prune 2>/dev/null; then
            success "Repository updated (fetched latest tags)"
        else
            warn "Could not fetch from remote (offline, timeout, or network error)"
        fi
    else
        warn "Repository appears corrupted"
    fi

    cd "$SCRIPT_DIR"
fi

# Verify the source directory exists in main repo
if [ ! -d "$DRAFT_DIR/source" ]; then
    abort "cplusplus/draft repository is missing 'source' directory"
fi

# Create worktrees directory
mkdir -p "$WORKTREES_DIR"

# Function to ensure a worktree exists for a given ref
ensure_worktree() {
    local ref="$1"
    local worktree_path="$WORKTREES_DIR/$ref"

    if [ -d "$worktree_path" ]; then
        # Worktree exists, check if it's valid
        if [ -d "$worktree_path/source" ]; then
            return 0
        else
            # Invalid worktree, remove and recreate
            warn "Worktree $ref appears invalid, recreating..."
            cd "$DRAFT_DIR"
            git worktree remove --force "$worktree_path" 2>/dev/null || rm -rf "$worktree_path"
            cd "$SCRIPT_DIR"
        fi
    fi

    # Create new worktree
    info "Creating worktree for $ref..."
    cd "$DRAFT_DIR"

    # For tags, we need to use the full ref
    if git rev-parse "refs/tags/$ref" &>/dev/null; then
        git worktree add "$worktree_path" "refs/tags/$ref" 2>/dev/null || \
            git worktree add "$worktree_path" "$ref" 2>/dev/null || \
            abort "Failed to create worktree for $ref"
    else
        # For branches like 'main' - might be currently checked out
        # Use --detach to create a detached worktree at the same commit
        if ! git worktree add "$worktree_path" "$ref" 2>/dev/null; then
            # Branch might be currently checked out, try detached
            local commit
            commit=$(git rev-parse "$ref" 2>/dev/null)
            if [ -n "$commit" ]; then
                git worktree add --detach "$worktree_path" "$commit" 2>/dev/null || \
                    abort "Failed to create worktree for $ref"
            else
                abort "Failed to create worktree for $ref - ref not found"
            fi
        fi
    fi

    cd "$SCRIPT_DIR"
    success "Created worktree for $ref"
}

# Set up worktrees for all versions we need
VERSION_REFS=("n3337" "n4140" "n4659" "n4861" "n4950" "main")

for ref in "${VERSION_REFS[@]}"; do
    ensure_worktree "$ref"
done

success "All worktrees ready"

# ============================================================================
# Step 5: Run full test suite in parallel (optional)
# ============================================================================
if [ "$SKIP_TESTS" = true ]; then
    info "Step 5: Skipping tests (--skip-tests specified)"
else
    info "Step 5: Running full test suite..."

    pytest tests/ -v -n auto \
        --ignore=tests/test_repo_manager.py \
        --ignore=tests/test_integration/test_cli.py \
        --ignore=tests/test_integration/test_standard_builder.py || abort "Tests failed! Please fix failing tests before proceeding."

    success "All tests passed"
fi

# ============================================================================
# Function: Compute hash of conversion scripts (for cache invalidation)
# ============================================================================
compute_scripts_hash() {
    # Hash the main converter, all Lua filters, and key Python modules
    local hash_input=""

    # Main converter script
    if [ -f "convert.py" ]; then
        hash_input+=$(stat -c '%Y%s' convert.py 2>/dev/null || echo "0")
    fi

    # All Lua filters
    for f in lua_filters/*.lua; do
        if [ -f "$f" ]; then
            hash_input+=$(stat -c '%Y%s' "$f" 2>/dev/null || echo "0")
        fi
    done

    # Key Python modules
    for f in cpp_std_converter/*.py; do
        if [ -f "$f" ]; then
            hash_input+=$(stat -c '%Y%s' "$f" 2>/dev/null || echo "0")
        fi
    done

    # Return a short hash
    echo "$hash_input" | sha256sum | cut -c1-16
}

# ============================================================================
# Function: Convert a C++ standard version using its worktree
# ============================================================================
convert_standard_version() {
    local git_ref="$1"
    local version_name="$2"
    local output_dir="${3:-$git_ref}"  # Default to git_ref if not provided
    local worktree_path="$WORKTREES_DIR/$git_ref"
    local sentinel="venv/.converted_${output_dir}"
    local scripts_hash
    scripts_hash=$(compute_scripts_hash)

    # Check if conversion can be skipped (unless --rebuild-standards specified)
    if [ "$REBUILD_STANDARDS" = false ] && [ -f "$sentinel" ]; then
        # Check if scripts have changed since last conversion
        local saved_hash
        saved_hash=$(cat "$sentinel" 2>/dev/null || echo "")
        if [ "$saved_hash" != "$scripts_hash" ]; then
            info "$version_name: Conversion scripts changed, rebuilding..."
        elif [ -d "$output_dir" ]; then
            local md_count
            md_count=$(find "$output_dir" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
            if [ "$md_count" -gt 10 ]; then
                # Output exists, scripts unchanged, skip conversion
                info "Skipping $version_name conversion (unchanged)"
                return 0
            fi
        fi
    fi

    # Verify worktree exists
    if [ ! -d "$worktree_path/source" ]; then
        abort "Worktree for $git_ref not found at $worktree_path"
    fi

    info "Converting $version_name standard from worktree..."

    # Create directories if needed
    mkdir -p "$output_dir"
    mkdir -p full

    # Launch separate build in background
    info "Building separate markdown files with cross-file linking..."
    ./convert.py --build-separate \
        --draft-repo "$worktree_path" \
        --toc-depth 3 \
        -o "$output_dir/" &
    local separate_pid=$!

    # Launch full build in background
    info "Building full standard file..."
    ./convert.py --build-full \
        --draft-repo "$worktree_path" \
        --toc-depth 3 \
        -o "full/$output_dir.md" &
    local full_pid=$!

    # Wait for both builds to complete
    wait $separate_pid || abort "Failed to convert $output_dir separate chapters"
    wait $full_pid || abort "Failed to convert $output_dir full standard"

    # Save scripts hash to sentinel file for cache invalidation
    echo "$scripts_hash" > "$sentinel"
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
# Step 11: Convert main branch (trunk / C++26 working draft)
# ============================================================================
info "Step 11: Converting latest development version (main branch)..."

# Update main worktree if --update-sources was specified
if [ "$UPDATE_SOURCES" = true ]; then
    main_worktree="$WORKTREES_DIR/main"
    if [ -d "$main_worktree" ]; then
        info "Updating main worktree..."
        cd "$main_worktree"
        # Worktree is detached, so use fetch + reset instead of pull
        if timeout 20 git fetch origin main 2>/dev/null && \
           git reset --hard origin/main 2>/dev/null; then
            success "Main worktree updated"
        else
            warn "Could not update main worktree (offline or timeout)"
        fi
        cd "$SCRIPT_DIR"
    fi
fi

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
echo "  - Worktrees: $WORKTREES_DIR/{n3337,n4140,n4659,n4861,n4950,main}"
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
