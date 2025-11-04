"""Tests for description list handling in cpp-macros.lua filter"""
import subprocess
from pathlib import Path

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-macros.lua")

def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with macro filter"""
    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        f"--lua-filter={FILTER_PATH}",
    ]
    result = subprocess.run(
        cmd,
        input=latex_content,
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
