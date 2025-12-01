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

"""Tests for importgraphic handling in cpp-figures.lua filter"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-figures.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with figures filter"""
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


def test_importgraphic_basic():
    """Test basic importgraphic environment conversion"""
    latex = r"""
\begin{importgraphic}
{Directed acyclic graph}
{class.dag}
{figdag.pdf}
\end{importgraphic}
"""
    output, exitcode = run_pandoc_with_filter(latex)
    assert exitcode == 0

    # Should have anchor for cross-referencing
    assert '<a id="fig:class.dag"></a>' in output

    # Should have image with caption and reference (brackets may be escaped in GFM)
    assert "![Directed acyclic graph" in output
    assert "fig:class.dag" in output
    assert "images/figdag.svg" in output


def test_importgraphic_single_line():
    """Test importgraphic with arguments on single line"""
    latex = r"\begin{importgraphic}{Name lookup}{class.lookup}{figname.pdf}\end{importgraphic}"
    output, exitcode = run_pandoc_with_filter(latex)
    assert exitcode == 0

    assert '<a id="fig:class.lookup"></a>' in output
    # Check image with caption (brackets may be escaped in GFM)
    assert "![Name lookup" in output
    assert "fig:class.lookup" in output
    assert "images/figname.svg" in output


def test_importgraphic_valuecategories():
    """Test the expression category taxonomy diagram"""
    latex = r"""
\begin{importgraphic}
{Expression category taxonomy}
{basic.lval}
{valuecategories.pdf}
\end{importgraphic}
"""
    output, exitcode = run_pandoc_with_filter(latex)
    assert exitcode == 0

    assert '<a id="fig:basic.lval"></a>' in output
    # Check image with caption (brackets may be escaped in GFM)
    assert "![Expression category taxonomy" in output
    assert "fig:basic.lval" in output
    assert "images/valuecategories.svg" in output


def test_importgraphic_with_surrounding_text():
    """Test importgraphic with surrounding text"""
    latex = r"""
Some text before.

\begin{importgraphic}
{Virtual base}
{class.virt}
{figvirt.pdf}
\end{importgraphic}

Some text after.
"""
    output, exitcode = run_pandoc_with_filter(latex)
    assert exitcode == 0

    # Should preserve surrounding text
    assert "Some text before" in output
    assert "Some text after" in output

    # Should have the figure
    assert '<a id="fig:class.virt"></a>' in output
    # Check image with caption (brackets may be escaped in GFM)
    assert "![Virtual base" in output
    assert "fig:class.virt" in output
    assert "images/figvirt.svg" in output


def test_non_importgraphic_unchanged():
    """Test that plain text without importgraphic passes through unchanged"""
    latex = r"""
This is some plain text without any importgraphic environment.

It should pass through the filter unchanged.
"""
    output, exitcode = run_pandoc_with_filter(latex)
    assert exitcode == 0

    # Plain text should pass through unchanged
    assert "plain text" in output
    assert "importgraphic" in output
    assert "unchanged" in output
