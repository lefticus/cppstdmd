"""Pytest configuration and shared fixtures"""

from pathlib import Path

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def filter_dir():
    """Path to filters directory"""
    return PROJECT_ROOT / "src" / "cpp_std_converter" / "filters"


@pytest.fixture
def simplified_macros():
    """Load simplified macro definitions for Pandoc preprocessing"""
    macros_file = PROJECT_ROOT / "src" / "cpp_std_converter" / "filters" / "simplified_macros.tex"
    if macros_file.exists():
        return macros_file.read_text(encoding="utf-8")
    return ""


def inject_macros(latex_content, macros=None):
    """Inject simplified macro definitions into LaTeX content

    This mimics the preprocessing done by converter.py to ensure tests
    run with the same macro expansion behavior as production.
    """
    if macros is None:
        macros_file = (
            PROJECT_ROOT / "src" / "cpp_std_converter" / "filters" / "simplified_macros.tex"
        )
        if macros_file.exists():
            macros = macros_file.read_text(encoding="utf-8")
        else:
            macros = ""

    if macros:
        return macros + "\n\n" + latex_content
    return latex_content


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
