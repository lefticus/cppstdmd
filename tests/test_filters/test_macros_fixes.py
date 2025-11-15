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

"""Tests for macro filter improvements (impldef, tcode with special chars)"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-macros.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with macros filter"""
    # Inject simplified_macros.tex preprocessing
    latex_with_macros = inject_macros(latex_content)

    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        f"--lua-filter={FILTER_PATH}",
    ]
    result = subprocess.run(
        cmd,
        input=latex_with_macros,
        capture_output=True,
        text=True,
    )
    return result.stdout, result.returncode


def test_impldef_simple():
    """Test \\impldef macro conversion"""
    latex = r"The value is \impldef{description text}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*implementation-defined*" in output
    # The description should not appear
    assert "description text" not in output


def test_impldef_with_nested_tcode():
    """Test \\impldef with nested \\tcode macro"""
    latex = r"The value is \impldef{search locations for \tcode{<>} header}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*implementation-defined*" in output
    # Neither the description nor the nested tcode should appear
    assert "search locations" not in output
    assert "<>" not in output


def test_tcode_with_hash():
    """Test \\tcode{\\#} conversion"""
    latex = r"It does not begin with a \tcode{\#} at the start."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`#`" in output
    assert "does not begin with a" in output


def test_tcode_with_double_hash():
    """Test \\tcode{\\#\\#} conversion"""
    latex = r"The \tcode{\#\#} operator is used for concatenation."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`##`" in output
    assert "operator" in output


def test_tcode_in_sentence():
    """Test \\tcode with various special characters"""
    latex = r"The macro \tcode{EMPTY} is defined."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`EMPTY`" in output
    assert "macro" in output
    assert "defined" in output
