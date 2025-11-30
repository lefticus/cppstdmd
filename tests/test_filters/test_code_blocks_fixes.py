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


def test_nested_textit_textrm_in_code():
    r"""Test deeply nested \textit{\textrm{}} gets fully stripped from code comments"""
    latex = r"""\begin{codeblock}
/* size of the struct in @\textit{\textrm{C++}}@ */
int size = sizeof(MyStruct);
\end{codeblock}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have C++ in the comment
    assert "C++" in output
    # Should NOT have unconverted LaTeX
    assert "\\textit" not in output
    assert "\\textrm" not in output
    # Should be a code block
    assert "```" in output


def test_textnormal_in_code_block():
    r"""Test \textnormal{} in code blocks (BNF-style grammars)"""
    latex = r"""\begin{codeblock}
\d @\textnormal{and}@ [[:digit:]]
\s @\textnormal{and}@ [[:space:]]
\end{codeblock}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have plain "and" text
    assert "and" in output
    # Should NOT contain LaTeX commands
    assert "\\textnormal" not in output
    # Should be a code block
    assert "```" in output
    # Verify BNF-style content is preserved
    assert "\\d" in output or "d" in output
    assert "[[:digit:]]" in output
