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

"""Test tilde with spacing braces cleanup in inline code."""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros


def run_pandoc_with_filter(latex_content, filter_name="cpp-macros.lua"):
    """Helper to run Pandoc with a filter on LaTeX content"""
    # Inject simplified_macros.tex preprocessing
    latex_with_macros = inject_macros(latex_content)

    cmd = [
        "pandoc",
        "-f",
        "latex+raw_tex",
        "-t",
        "gfm",
        "--lua-filter",
        f"src/cpp_std_converter/filters/{filter_name}",
    ]
    result = subprocess.run(cmd, input=latex_with_macros, capture_output=True, text=True)
    return result.stdout, result.returncode


def test_tilde_in_destructor():
    r"""Test \tcode{A::\~{}A()} renders correctly (except.md bug)."""
    latex = r"""Furthermore, if \tcode{A::\~{}A()} were virtual, the program would be
ill-formed since a function that overrides a virtual function from a base class shall
not have a potentially-throwing exception specification."""

    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have destructor with plain tilde
    assert "`A::~A()`" in output
    # Should NOT have tilde with braces
    assert "~{}" not in output


def test_tilde_operator():
    r"""Test \tcode{\~{}} (bitwise complement operator) renders correctly."""
    latex = r"The operand of the \tcode{\~{}} operator shall have integral type."

    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have plain tilde
    assert "`~`" in output
    # Should NOT have tilde with braces
    assert "~{}" not in output


def test_tilde_in_class_description():
    r"""Test tilde in destructor references (class.md patterns)."""
    latex = r"In an explicit destructor call, the destructor is specified by a \tcode{\~{}} followed by a type name."

    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have plain tilde
    assert "`~`" in output
    # Should NOT have tilde with braces
    assert "~{}" not in output
