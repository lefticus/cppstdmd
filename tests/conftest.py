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
