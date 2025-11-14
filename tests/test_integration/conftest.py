"""Shared fixtures for integration tests

This conftest provides session-scoped fixtures to prevent race conditions
when running tests in parallel with pytest-xdist.

Key design decisions:
- draft_repo: session scope ensures only ONE git checkout for all integration tests
- converter: session scope for efficiency (stateless, can be reused)

Race condition fix: Previously, each test module had its own module-scoped
draft_repo fixture, causing concurrent git checkouts on the same repository
when running with -n auto. Session scope ensures sequential setup.
"""

from pathlib import Path

import pytest

from cpp_std_converter.converter import Converter
from cpp_std_converter.repo_manager import DraftRepoManager


@pytest.fixture(scope="session")
def draft_repo():
    """
    Session-scoped fixture to ensure draft repository exists and is on n4950.

    Session scope prevents race conditions when running tests in parallel:
    - Only ONE checkout happens for all integration tests
    - All workers share the same repository state
    - No concurrent git operations
    """
    # Look for cplusplus-draft in project directory first (from setup-and-build.sh)
    project_root = Path(__file__).parent.parent.parent
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
