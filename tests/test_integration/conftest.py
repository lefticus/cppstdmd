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

"""Shared fixtures for integration tests

This conftest provides session-scoped fixtures to prevent race conditions
when running tests in parallel with pytest-xdist.

Key design decisions:
- draft_repo: Uses git worktrees to avoid checkout conflicts
- converter: session scope for efficiency (stateless, can be reused)

Uses worktrees created by setup-and-build.sh to avoid:
- Race conditions from concurrent git checkouts
- Index lock conflicts
- Mtime changes that break incremental builds
"""

from pathlib import Path

import pytest

from cpp_std_converter.converter import Converter
from cpp_std_converter.repo_manager import DraftRepoManager


@pytest.fixture(scope="session")
def draft_repo():
    """
    Session-scoped fixture to get draft repository path for n4950.

    Uses the n4950 worktree created by setup-and-build.sh to avoid
    any git checkout operations during tests.
    """
    project_root = Path(__file__).parent.parent.parent

    # First, try to use the worktree (preferred - no checkout needed)
    worktree_path = project_root / "cplusplus-draft" / "worktrees" / "n4950"
    if worktree_path.exists() and (worktree_path / "source").exists():
        # Return a repo manager pointing at the worktree
        repo_manager = DraftRepoManager(repo_dir=worktree_path)
        return repo_manager

    # Fall back to main repo with checkout (legacy behavior)
    project_draft = project_root / "cplusplus-draft"
    if project_draft.exists() and (project_draft / ".git").exists():
        repo_manager = DraftRepoManager(repo_dir=project_draft)
    else:
        # Fall back to default ~/cplusplus-draft
        repo_manager = DraftRepoManager()

    # Ensure repo exists
    if not repo_manager.exists():
        try:
            repo_manager.clone(shallow=False)
        except Exception as e:
            pytest.skip(f"Could not clone draft repository: {e}")

    # Checkout n4950 (C++23) for consistent, stable test state
    try:
        repo_manager.checkout("n4950")
    except Exception as e:
        pytest.skip(f"Could not checkout n4950: {e}")

    return repo_manager


@pytest.fixture(scope="session")
def converter():
    """
    Session-scoped converter instance.

    Converter is stateless, so session scope is safe and more efficient
    than creating a new instance per module or test.
    """
    return Converter()
