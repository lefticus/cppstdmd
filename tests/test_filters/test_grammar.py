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

"""Tests for cpp-grammar.lua filter"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-grammar.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with grammar filter"""
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


def test_ncbnf_basic():
    """Test basic ncbnf grammar block"""
    latex = r"""
\begin{ncbnf}
typedef-name:\br
    identifier
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "``` bnf" in output
    assert "typedef-name:" in output
    assert "identifier" in output


def test_ncbnf_with_terminal():
    r"""Test \terminal{} in grammar"""
    latex = r"""
\begin{ncbnf}
string-literal:\br
    \terminal{R} raw-string
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "'R'" in output  # \terminal{R} should become 'R'


def test_ncbnf_with_opt():
    r"""Test \opt{} in grammar"""
    latex = r"""
\begin{ncbnf}
string:\br
    \opt{encoding} \terminal{"} text \terminal{"}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "encodingₒₚₜ" in output  # \opt{} should become contentₒₚₜ


def test_ncsimplebnf():
    """Test ncsimplebnf environment"""
    latex = r"""
\begin{ncsimplebnf}
expression:\br
    literal
\end{ncsimplebnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "``` bnf" in output
    assert "expression:" in output


def test_ncrebnf():
    """Test ncrebnf environment"""
    latex = r"""
\begin{ncrebnf}
pattern:\br
    regex
\end{ncrebnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "``` bnf" in output
    assert "pattern:" in output


def test_nontermdef():
    r"""Test \nontermdef{} command"""
    latex = r"""
\begin{ncbnf}
\nontermdef{class-name}\br
    identifier\br
    simple-template-id
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "class-name:" in output
    assert "identifier" in output
    assert "simple-template-id" in output


def test_keyword():
    r"""Test \keyword{} command"""
    latex = r"""
\begin{ncbnf}
\nontermdef{class-key}\br
    \keyword{class}\br
    \keyword{struct}\br
    \keyword{union}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "class-key:" in output
    # Keywords should be converted to backticks (from earlier filter) or plain text
    assert "class" in output
    assert "struct" in output
    assert "union" in output


def test_bnfindent():
    r"""Test \bnfindent indentation"""
    latex = r"""
\begin{ncbnf}
\nontermdef{function-ptr}\br
    \terminal{void} \terminal{(} \terminal{*} identifier \terminal{)}\br
    \bnfindent\opt{parameter-list}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "function-ptr:" in output
    assert "'void'" in output
    # \bnfindent should be converted to spaces, \opt{} to Unicode subscript
    assert "  parameter-listₒₚₜ" in output or "parameter-listₒₚₜ" in output


def test_grammarterm():
    r"""Test \grammarterm{} command"""
    latex = r"""
\begin{ncbnf}
\nontermdef{expr}\br
    \grammarterm{id-expression}\br
    \grammarterm{literal}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "expr:" in output
    assert "id-expression" in output
    assert "literal" in output


def test_textnormal():
    r"""Test \textnormal{} command"""
    latex = r"""
\begin{ncbnf}
\nontermdef{hex-digit}\br
    \textnormal{one of}\br
    \terminal{0} \terminal{1} \terminal{2}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "hex-digit:" in output
    assert "one of" in output
    assert "'0'" in output


def test_unicode():
    r"""Test \unicode{} command"""
    latex = r"""
\begin{ncbnf}
\nontermdef{special}\br
    \unicode{2026}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "special:" in output
    # \unicode{2026} is horizontal ellipsis …
    assert "…" in output


def test_unicode_with_description():
    r"""Test \unicode{}{} with two arguments (code and description) - Issue #21"""
    latex = r"""
\begin{ncbnf}
\nontermdef{n-char} \textnormal{one of}\br
     \textnormal{any member except the \unicode{007d}{right curly bracket}}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "U+007d (right curly bracket)" in output
    # Ensure malformed output is not present
    assert "}{right curly bracket}" not in output


def test_tcode_in_bnf():
    r"""Test \tcode{} in BNF blocks"""
    latex = r"""
\begin{ncbnf}
\nontermdef{type-spec}\br
    \tcode{int}\br
    \tcode{char}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "type-spec:" in output
    assert "int" in output
    assert "char" in output


def test_texttt_in_bnf():
    r"""Test \texttt{} in BNF blocks (module.md bug - Pandoc converts \keyword{} to \texttt{})"""
    latex = r"""
\begin{bnf}
\nontermdef{export-declaration}\br
    \texttt{export} name-declaration\br
    \texttt{export} \terminal{\{} \opt{declaration-seq} \terminal{\}}
\end{bnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "export-declaration:" in output
    assert "export" in output
    assert "\\texttt" not in output
    assert "'{'" in output


def test_caret():
    r"""Test \caret{} command"""
    latex = r"""
\begin{ncbnf}
\nontermdef{xor-expr}\br
    expr \caret{} expr
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "xor-expr:" in output
    assert "^" in output


def test_complex_bnf():
    """Test complex BNF with multiple commands"""
    latex = r"""
\begin{ncbnf}
\nontermdef{member-declarator}\br
    \grammarterm{declarator} \opt{\grammarterm{brace-or-equal-initializer}}\br
    \bnfindent\opt{\grammarterm{attribute-specifier-seq}}\br
    \grammarterm{identifier} \opt{\grammarterm{attribute-specifier-seq}} \terminal{:} \grammarterm{constant-expression}\br
    \bnfindent\opt{\grammarterm{brace-or-equal-initializer}}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "member-declarator:" in output
    assert "declarator" in output
    assert "brace-or-equal-initializerₒₚₜ" in output  # \opt{} uses Unicode subscript
    assert "':'" in output


def test_terminal_with_escaped_chars():
    r"""Test that \terminal{} properly unescapes LaTeX special characters"""
    latex = r"""
\begin{ncbnf}
\nontermdef{pp-token}\br
    \terminal{\#}\br
    \terminal{\%}\br
    \terminal{\_}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "pp-token:" in output
    # Escaped characters should be unescaped in output
    assert "'#'" in output
    assert "'%'" in output
    assert "'_'" in output
    # Should NOT have backslash escapes
    assert r"'\#'" not in output
    assert r"'\%'" not in output
    assert r"'\_'" not in output


def test_textnormal_with_nested_tref():
    r"""Test \textnormal{} with nested \tref{} (Issue #22 - lex.md bug)"""
    latex = r"""
\begin{bnf}
\nontermdef{keyword}\br
    \textnormal{any identifier listed in \tref{lex.key}}\br
\end{bnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "keyword:" in output
    # The \textnormal{} wrapper should be stripped, preserving nested content
    assert "any identifier listed in" in output
    # CRITICAL: \tref{lex.key} should be converted to [[lex.key]]
    assert "[[lex.key]]" in output
    # Verify the entire phrase is correct (no truncation/mangling)
    assert "any identifier listed in [[lex.key]]" in output
    # Should NOT have unconverted \tref
    assert r"\tref" not in output


def test_math_subscripts_in_bnf():
    r"""Test that $_1$ subscripts in BNF are converted to Unicode (Issue #3)"""
    latex = r"""
\begin{ncbnf}
\nontermdef{selection-statement}\br
    \keyword{if} \keyword{consteval} compound-statement$_1$ \keyword{else} statement$_2$
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "``` bnf" in output
    # $_1$ should become ₁ and $_2$ should become ₂
    assert "compound-statement₁" in output
    assert "statement₂" in output
    # Should NOT have raw LaTeX math
    assert "$_1$" not in output
    assert "$_2$" not in output


def test_math_subscripts_with_braces():
    r"""Test that $_{n}$ subscripts in BNF are converted to Unicode (Issue #3)"""
    latex = r"""
\begin{ncbnf}
\nontermdef{test-expr}\br
    expr$_{0}$ \terminal{+} expr$_{1}$
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "``` bnf" in output
    # $_{0}$ should become ₀ and $_{1}$ should become ₁
    assert "expr₀" in output
    assert "expr₁" in output
    # Should NOT have raw LaTeX math
    assert "$_{0}$" not in output
    assert "$_{1}$" not in output


def test_math_superscripts_in_bnf():
    r"""Test superscripts in BNF grammar"""
    latex = r"""
\begin{ncbnf}
\nontermdef{pattern}\br
    expr$^n$\br
    value$^{2}$
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Superscripts should be converted to Unicode
    assert "exprⁿ" in output
    assert "value²" in output
    # Should NOT have raw LaTeX math
    assert "$^n$" not in output
    assert "$^{2}$" not in output


def test_math_operators_in_bnf():
    r"""Test math operators like \times, \le in BNF"""
    latex = r"""
\begin{ncbnf}
\nontermdef{complexity}\br
    $n \times m$ operations\br
    $i \le n$
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Operators should be converted to Unicode
    assert "n × m operations" in output
    assert "i ≤ n" in output
    # Should NOT have raw LaTeX
    assert r"\times" not in output
    assert r"\le" not in output


def test_greek_letters_in_bnf():
    r"""Test Greek letters in BNF grammar"""
    latex = r"""
\begin{ncbnf}
\nontermdef{theorem}\br
    $\alpha$ production\br
    $\beta$ reduction
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Greek letters should be converted to Unicode
    assert "α production" in output
    assert "β reduction" in output
    # Should NOT have raw LaTeX
    assert r"\alpha" not in output
    assert r"\beta" not in output


def test_arrows_in_bnf():
    r"""Test arrows in BNF grammar"""
    latex = r"""
\begin{ncbnf}
\nontermdef{transition}\br
    state$_1$ $\rightarrow$ state$_2$\br
    $A \Rightarrow B$
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Arrows and subscripts should be converted
    assert "state₁ → state₂" in output
    assert "A ⇒ B" in output
    # Should NOT have raw LaTeX
    assert r"\rightarrow" not in output
    assert r"\Rightarrow" not in output


def test_combined_math_in_bnf():
    r"""Test combined math expressions in BNF"""
    latex = r"""
\begin{ncbnf}
\nontermdef{complex-rule}\br
    expr$_i^n$ $\le$ bound$_{max}$\br
    $\alpha \cdot \beta \to \gamma$
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Combined subscript/superscript
    assert "exprᵢⁿ ≤ boundₘₐₓ" in output
    # Greek letters with operators and arrow
    assert "α ⋅ β → γ" in output
    # Should NOT have raw LaTeX
    assert "$_i^n$" not in output
    assert r"\alpha" not in output


def test_unconvertible_math_preserved():
    r"""Test that complex/unconvertible math is preserved as LaTeX"""
    latex = r"""
\begin{ncbnf}
\nontermdef{complex}\br
    pattern with $\frac{a}{b}$ fraction
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Fractions can't be converted, should preserve $...$ delimiters
    assert r"$\frac{a}{b}$" in output or "$" in output


def test_bnfnontermshape_stripped():
    r"""Test that \locnontermdef produces clean output without braces (Issue #74)"""
    latex = r"""
\begin{ncbnf}
\locnontermdef{intval}\br
    sign units
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # BnfNontermshape and itcorr should be stripped
    assert "BnfNontermshape" not in output
    assert "itcorr" not in output
    # Should have clean output WITHOUT braces
    assert "intval:" in output
    assert "{intval}" not in output  # No braces!
    assert "sign units" in output


def test_itcorr_stripped_with_optional_arg():
    r"""Test that \itcorr[N] italic correction is stripped"""
    latex = r"Text with\itcorr[-1] spacing correction and\itcorr[2] another one."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # itcorr commands should be stripped
    assert "itcorr" not in output
    assert "Text with spacing correction and another one." in output


def test_itcorr_stripped_no_arg():
    r"""Test that \itcorr without argument is stripped"""
    latex = r"Text with \itcorr spacing here."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # itcorr command should be stripped
    assert "itcorr" not in output
    assert "Text with spacing here." in output


def test_renontermdef_in_bnf():
    r"""Test \renontermdef{} regex grammar macro conversion (Issue #70)"""
    latex = r"""
\begin{ncrebnf}
\renontermdef{ClassAtom}\br
  \terminal{-}\br
  ClassAtomNoDash
\end{ncrebnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should output term with :: suffix
    assert "ClassAtom::" in output
    # Should NOT have \textit or other LaTeX commands
    assert "\\textit" not in output
    assert "renontermdef" not in output
    # Should be in a BNF code block
    assert "``` bnf" in output or "```bnf" in output


def test_textbf_and_textnormal_in_bnf():
    r"""Test \textbf{} and \textnormal{} unwrapping in BNF blocks (Issue #69)"""
    latex = r"""
\begin{ncrebnf}
\renontermdef{IdentityEscape}\br
  SourceCharacter \textnormal{\textbf{but not}} \terminal{c}
\end{ncrebnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have clean output without LaTeX commands
    assert "but not" in output
    # Should NOT have raw LaTeX commands
    assert "\\textbf" not in output
    assert "\\textnormal" not in output
    # Should be in a BNF code block
    assert "``` bnf" in output or "```bnf" in output


def test_fmtnontermdef_no_textit():
    r"""Test \fmtnontermdef{} doesn't leave \textit{} in BNF output"""
    latex = r"""
\begin{ncbnf}
\fmtnontermdef{replacement-field}\br
    \terminal{\{} arg-idₒₚₜ format-specifierₒₚₜ \terminal{\}}
\end{ncbnf}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have the nonterminal name in output
    assert "replacement-field" in output
    # Should NOT have unconverted \textit{} LaTeX
    assert "\\textit" not in output
    # Should be in a BNF code block
    assert "``` bnf" in output or "```bnf" in output
