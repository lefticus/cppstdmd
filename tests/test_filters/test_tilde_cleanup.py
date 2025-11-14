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
