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

"""Tests for description list handling in cpp-macros.lua filter"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-macros.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with macro filter"""
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


def test_simple_description_list():
    """Test basic description list with two items"""
    latex = r"""
\begin{description}
\item TERM_ONE\\
Description for term one.

\item TERM_TWO\\
Description for term two.
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Terms with underscores get code formatting
    assert "**`TERM_ONE`**" in output
    assert "**`TERM_TWO`**" in output
    assert "Description for term one" in output
    assert "Description for term two" in output


def test_description_with_mname():
    r"""Test description list with \mname{} macro"""
    latex = r"""
\begin{description}
\item \mname{DATE}\\
The date of translation of the source file.

\item \mname{FILE}\\
The presumed name of the current source file.
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "**`__DATE__`**" in output
    assert "**`__FILE__`**" in output
    assert "date of translation" in output
    assert "presumed name" in output


def test_description_with_xname():
    r"""Test description list with \xname{} macro"""
    latex = r"""
\begin{description}
\item \xname{cplusplus}\\
The integer literal value.
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "**`__cplusplus`**" in output
    assert "integer literal" in output


def test_description_with_index_commands():
    """Test that index commands are stripped from terms"""
    latex = r"""
\begin{description}
\item
\indextext{\idxxname{cplusplus}}%
\xname{cplusplus}\\
The integer literal value.

\item
\indextext{__date__@\mname{DATE}}%
\mname{DATE}\\
The date of translation.
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have clean terms without index commands
    assert "**`__cplusplus`**" in output
    assert "**`__DATE__`**" in output
    # Should NOT have LaTeX artifacts
    assert "\\indextext" not in output
    assert "\\idxxname" not in output
    assert "integer literal" in output
    assert "date of translation" in output


def test_description_with_tcode():
    r"""Test description list with \tcode{} in description text"""
    latex = r"""
\begin{description}
\item \mname{VA_ARGS}\\
Replaced by the preprocessing tokens of the corresponding argument.
Use \tcode{__VA_ARGS__} in macros.
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "**`__VA_ARGS__`**" in output
    assert "`__VA_ARGS__`" in output
    assert "preprocessing tokens" in output


def test_nested_description_note():
    r"""Test description list containing a note environment"""
    latex = r"""
\begin{description}
\item \mname{STDC}\\
Whether \tcode{__STDC__} is predefined.
\begin{note}
This macro is not predefined in \Cpp{}.
\end{note}
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "**`__STDC__`**" in output
    assert "`__STDC__`" in output
    # Note: The note environment would be processed by cpp-notes-examples.lua filter
    # This test just ensures description list parsing doesn't break on nested environments


def test_multiple_description_lists():
    """Test multiple separate description lists in one document"""
    latex = r"""
\begin{description}
\item \mname{DATE}\\
The date.
\end{description}

Some text between lists.

\begin{description}
\item \mname{FILE}\\
The file name.
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "**`__DATE__`**" in output
    assert "**`__FILE__`**" in output
    assert "Some text between lists" in output


def test_description_with_stage():
    r"""Test description list with \stage{} macro"""
    latex = r"""\begin{description}
\stage{1}
The function initializes local variables.

\stage{2}
The function performs conversion.
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "Stage 1:" in output
    assert "Stage 2:" in output
    assert "initializes local variables" in output
    assert "performs conversion" in output
