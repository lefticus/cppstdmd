"""Tests for cpp-grammar.lua filter"""
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
    assert "[encoding]" in output  # \opt{} should become [...]

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
    # \bnfindent should be converted to spaces
    assert "  [parameter-list]" in output or "[parameter-list]" in output

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
    assert "[brace-or-equal-initializer]" in output
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
