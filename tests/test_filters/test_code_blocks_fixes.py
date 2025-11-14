"""Tests for code block filter improvements (textrm, textit)"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-code-blocks.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with code-blocks filter"""
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


def test_textrm_in_code_comment():
    """Test \\textrm in code block comment"""
    latex = r"""\begin{codeblock}
#include "file.h"      @\textrm{(after macro replacement)}@
\end{codeblock}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "(after macro replacement)" in output
    # Should NOT contain LaTeX commands
    assert "\\textrm" not in output
    assert "@" not in output or "@" in "#include"  # @ only in code, not as delimiter


def test_textit_in_code_comment():
    """Test \\textit in code block comment"""
    latex = r"""\begin{codeblock}
int x = 42;      @\textit{(initialization)}@
\end{codeblock}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "(initialization)" in output
    # Should NOT contain LaTeX commands
    assert "\\textit" not in output


def test_nested_textrm_textit():
    """Test nested \\textrm and \\textit"""
    latex = r"""\begin{codeblock}
#include "vers2.h"      @\textrm{(\textit{after macro replacement, before file access})}@
\end{codeblock}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "(after macro replacement, before file access)" in output
    # Should NOT contain LaTeX commands
    assert "\\textrm" not in output
    assert "\\textit" not in output
    # Check basic structure is preserved
    assert '#include "vers2.h"' in output


def test_code_without_formatting():
    """Test code block without special formatting (regression test)"""
    latex = r"""\begin{codeblock}
int main() {
    return 0;
}
\end{codeblock}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "int main()" in output
    assert "return 0" in output
