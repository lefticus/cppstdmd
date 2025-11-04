"""Pytest configuration and shared fixtures"""
import pytest
from pathlib import Path
import subprocess

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent

@pytest.fixture
def filter_dir():
    """Path to filters directory"""
    return PROJECT_ROOT / "src" / "cpp_std_converter" / "filters"

@pytest.fixture
def cpp_draft_source():
    """Path to C++ draft source if available"""
    # Look in project directory first, then fall back to /tmp
    project_draft = PROJECT_ROOT / "cplusplus-draft" / "source"
    if project_draft.exists():
        return project_draft

    # Fall back to legacy location for backwards compatibility
    tmp_draft = Path("/tmp/cplusplus-draft/source")
    if tmp_draft.exists():
        return tmp_draft

    return None

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests requiring cplusplus-draft"
    )
