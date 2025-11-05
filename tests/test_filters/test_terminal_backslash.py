"""Test for \terminal{\textbackslash} conversion in BNF grammar"""
import subprocess
from pathlib import Path

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-grammar.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with grammar filter"""
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
        check=True,
    )
    return result.stdout


def test_terminal_with_textbackslash():
    """Test that \\terminal{\\textbackslash} converts to '\\' in BNF grammar."""
    input_latex = r"""\begin{bnf}
\nontermdef{simple-escape-sequence}\br
    \terminal{\textbackslash} simple-escape-sequence-char
\end{bnf}"""

    # Expected output: \terminal{\textbackslash} should convert to '\'
    expected = """``` bnf
simple-escape-sequence:
    '\\' simple-escape-sequence-char
```"""

    actual = run_pandoc_with_filter(input_latex)
    assert expected.strip() in actual.strip(), f"Expected:\n{expected}\n\nGot:\n{actual}"
