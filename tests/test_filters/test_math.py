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

"""Tests for cpp-math.lua filter"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-math.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with math filter"""
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


# Superscript tests
def test_superscript_digits():
    """Test superscript digit conversion"""
    latex = r"Value is $x^2$ and $10^9$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "x²" in output
    assert "10⁹" in output
    # Should not have LaTeX math delimiters
    assert "$" not in output


def test_superscript_with_braces():
    """Test superscript with braces $x^{n}$"""
    latex = r"Result is $2^{n}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "2ⁿ" in output
    assert "$" not in output


def test_superscript_letters():
    """Test available superscript letters (i, n)"""
    latex = r"Values $x^i$ and $y^n$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "xⁱ" in output
    assert "yⁿ" in output


def test_superscript_unavailable_letter():
    """Test superscript with unavailable letter stays as LaTeX"""
    latex = r"Result $x^q$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should keep as LaTeX since 'q' superscript not available
    assert "$x^q$" in output


def test_complex_superscript_unchanged():
    """Test multi-char superscripts convert when possible"""
    latex = r"Value $x^{text}$ and $2^{i+1}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Multi-char word-only superscripts now convert
    assert "xᵗᵉˣᵗ" in output
    # But complex expressions with operators remain as LaTeX
    assert "$2^{i+1}$" in output


# Subscript tests
def test_subscript_digits():
    """Test subscript digit conversion"""
    latex = r"Variables $x_0$, $B_1$, and $a_9$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "x₀" in output
    assert "B₁" in output
    assert "a₉" in output
    assert "$" not in output


def test_subscript_with_braces():
    """Test subscript with braces"""
    latex = r"Index $a_{10}$ works."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Multi-digit subscripts now convert with multi-char support
    assert "a₁₀" in output


def test_consecutive_subscripts():
    """Test consecutive subscripts convert properly"""
    latex = r"Sequence $c_1c_2...c_k$ works."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # All three subscripts should convert
    assert "c₁c₂...cₖ" in output
    # Should NOT have any unconverted subscripts
    assert "c_2" not in output


def test_subscript_letters():
    """Test available subscript letters"""
    latex = r"Values $x_i$, $x_n$, and $T_k$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "xᵢ" in output
    assert "xₙ" in output
    assert "Tₖ" in output


def test_subscript_more_letters():
    """Test more available subscript letters (a, e, o, x, h, l, m, p, s, t)"""
    latex = r"$x_a$, $y_e$, $z_o$, $a_h$, $b_m$, $c_p$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "xₐ" in output
    assert "yₑ" in output
    assert "zₒ" in output
    assert "aₕ" in output
    assert "bₘ" in output
    assert "cₚ" in output


def test_subscript_unavailable_letters():
    """Test subscripts with unavailable letters stay as LaTeX"""
    latex = r"Value $x_q$ and $x_y$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # q and y subscripts not available
    assert "$x_q$" in output
    assert "$x_y$" in output


def test_complex_subscript_unchanged():
    """Test multi-char subscripts convert when possible"""
    latex = r"Values $x_{tail}$, $x_{i+1}$, $x_{\mathrm{max}}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Multi-char word-only subscripts now convert
    assert "xₜₐᵢₗ" in output
    # Arithmetic subscripts convert
    assert "xᵢ₊₁" in output
    # \mathrm{} is stripped and multi-char converts
    assert "xₘₐₓ" in output


def test_mixed_sub_and_super():
    """Test mixed subscript and superscript"""
    latex = r"Value $x_i^2$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should convert both if both are simple
    assert "xᵢ²" in output
    assert "$" not in output


# Comparison operator tests
def test_comparison_operators():
    """Test comparison operator conversion"""
    latex = r"$x \leq y$ and $a \geq b$ but $x \neq y$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "x ≤ y" in output
    assert "a ≥ b" in output
    assert "x ≠ y" in output
    assert "$" not in output


def test_standard_comparison():
    """Test standard comparison operators"""
    latex = r"$a < b$ and $x = y$ and $c > d$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "a < b" in output
    assert "x = y" in output
    assert "c > d" in output


# Greek letter tests
def test_greek_letters_basic():
    """Test basic Greek letter conversion"""
    latex = r"$\alpha + \beta = \gamma$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "α + β = γ" in output
    assert "$" not in output


def test_greek_letters_complete():
    """Test all supported Greek letters"""
    latex = r"$\alpha$, $\beta$, $\gamma$, $\delta$, $\epsilon$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "α" in output
    assert "β" in output
    assert "γ" in output
    assert "δ" in output
    assert "ε" in output


def test_greek_letters_more():
    """Test additional Greek letters"""
    latex = r"$\lambda$, $\mu$, $\sigma$, $\pi$, $\theta$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "λ" in output
    assert "μ" in output
    assert "σ" in output
    assert "π" in output
    assert "θ" in output


# Arrow tests
def test_arrows():
    """Test arrow conversion"""
    latex = r"$A \rightarrow B$ and $C \leftarrow D$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "A → B" in output
    assert "C ← D" in output


def test_double_arrows():
    """Test double arrow conversion"""
    latex = r"$A \Rightarrow B$ and $C \Leftarrow D$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "A ⇒ B" in output
    assert "C ⇐ D" in output


def test_mapsto_arrow():
    """Test mapsto arrow"""
    latex = r"$f \mapsto g$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "f ↦ g" in output


# Math operator tests
def test_math_operators():
    """Test multiplication and dot operators"""
    latex = r"$a \times b$ and $x \cdot y$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "a × b" in output
    assert "x ⋅ y" in output


def test_ellipsis():
    """Test cdots ellipsis"""
    latex = r"$a_1, \cdots, a_n$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "a₁, ⋯, aₙ" in output


def test_logical_operators():
    """Test land and lor operators"""
    latex = r"$A \land B$ or $C \lor D$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "A ∧ B" in output
    assert "C ∨ D" in output


# Mixed expression tests
def test_mixed_simple_expression():
    """Test mixed expression like in GENERALIZED_SUM"""
    latex = r"$1 < \mathtt{K}+1 = \mathtt{M} \leq \mathtt{N}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "1 < K+1 = M ≤ N" in output
    assert "$" not in output


def test_inequality_chain():
    """Test inequality chain"""
    latex = r"$0 \leq i < n$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "0 ≤ i < n" in output


# Complex math that should remain unchanged
def test_fractions_unchanged():
    """Test fractions remain as LaTeX"""
    latex = r"$\frac{a}{b}$ and $\frac{1}{2}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert r"$\frac{a}{b}$" in output
    assert r"$\frac{1}{2}$" in output


def test_integrals_unchanged():
    """Test integrals remain as LaTeX"""
    latex = r"$\int_0^1 f(x)dx$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert r"$\int_0^1 f(x)dx$" in output


def test_summations_unchanged():
    """Test summations remain as LaTeX"""
    latex = r"$\sum_{i=1}^n x_i$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert r"$\sum_{i=1}^n x_i$" in output


def test_square_root_unchanged():
    """Test square roots remain as LaTeX"""
    latex = r"$\sqrt{x}$ and $\sqrt{2}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert r"$\sqrt{x}$" in output
    assert r"$\sqrt{2}$" in output


def test_limits_unchanged():
    """Test limits remain as LaTeX"""
    latex = r"$\lim_{x \rightarrow 0} f(x)$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert r"$\lim_{x \rightarrow 0} f(x)$" in output


# Math font tests
def test_mathtt_conversion():
    """Test mathtt conversion"""
    latex = r"$\mathtt{X} = 5$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "X = 5" in output
    assert "mathtt" not in output


def test_mathrm_conversion():
    """Test mathrm conversion with multi-char subscript"""
    latex = r"$x_{\mathrm{max}}$ converts."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # \mathrm{} is stripped, then multi-char subscript converts
    assert "xₘₐₓ" in output


def test_mathit_conversion():
    """Test mathit conversion in simple context"""
    latex = r"$\mathit{text}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "text" in output


# Edge cases
def test_empty_math():
    """Test empty math expression"""
    latex = r"Text $$ text."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Empty math should either be removed or stay minimal


def test_whitespace_handling():
    """Test whitespace in math is handled correctly"""
    latex = r"$ x \leq y $."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "x ≤ y" in output


def test_display_math_unchanged():
    """Test display math (block equations) remain unchanged"""
    latex = r"""
Text before.
$$x^2 + y^2 = z^2$$
Text after.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Display math should remain (Pandoc converts $$ to display math)
    # May appear as ``` math block or similar


def test_nested_superscript_unchanged():
    """Test nested superscripts remain as LaTeX"""
    latex = r"$x^{y^z}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert r"$x^{y^z}$" in output


def test_nested_subscript_unchanged():
    """Test nested subscripts remain as LaTeX"""
    latex = r"$a_{b_{c}}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert r"$a_{b_{c}}$" in output


def test_ldots_to_unicode():
    """Test \\ldots converts to Unicode horizontal ellipsis"""
    latex = r"$V_{0}$, $V_{1}$, $V_{2}$, $\ldots$"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have Unicode subscripts and ellipsis
    assert "V₀" in output or "V_0" in output  # Accept either format
    assert "…" in output or "..." in output  # Unicode or ASCII ellipsis


def test_vdots_to_unicode():
    """Test \\vdots converts to Unicode vertical ellipsis"""
    latex = r"\vdots"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "⋮" in output


def test_simple_subscripts_to_unicode():
    """Test simple subscripts like $V_{0}$, $C_i$ convert to Unicode"""
    latex = r"enum { $V_{0}$, $V_{1}$, $V_{2}$, $V_{3}$ }"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have Unicode subscripts
    assert "V₀" in output
    assert "V₁" in output
    assert "V₂" in output
    assert "V₃" in output


def test_control_space_in_math():
    """Test backslash-space (control space) in math mode converts properly"""
    latex = r"$\min(x, \ y)$ and $a\ b\ c$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Control space should be converted to regular space (not preserved as \\ )
    assert r"\ " not in output
    # Content should be present
    assert "min" in output
    assert "x" in output
    assert "y" in output


def test_to_arrow_alias():
    """Test \\to converts to Unicode arrow (alias for \\rightarrow)"""
    latex = r"$f: A \to B$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "f: A → B" in output
    assert "$" not in output


def test_le_ge_aliases():
    """Test \\le and \\ge convert to Unicode (aliases for \\leq and \\geq)"""
    latex = r"$x \le y$ and $a \ge b$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "x ≤ y" in output
    assert "a ≥ b" in output
    assert "$" not in output


def test_dotsc_ellipsis():
    """Test \\dotsc converts to Unicode ellipsis (dots for series/commas)"""
    latex = r"$a_1, a_2, \dotsc, a_n$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "a₁, a₂, …, aₙ" in output
    assert "$" not in output


def test_dotsb_ellipsis():
    """Test \\dotsb converts to Unicode ellipsis (dots for binary operators)"""
    latex = r"$x_1 + x_2 + \dotsb + x_n$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "x₁ + x₂ + … + xₙ" in output
    assert "$" not in output


def test_additional_greek_letters():
    """Test additional Greek letters (rho, phi, ell, zeta)"""
    latex = r"$\rho$, $\phi$, $\ell$, $\zeta$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "ρ" in output
    assert "φ" in output
    assert "ℓ" in output
    assert "ζ" in output
    assert "$" not in output


# Arithmetic subscript tests
def test_arithmetic_subscript_minus():
    """Test arithmetic subscripts with minus: x_{n-1} → xₙ₋₁"""
    latex = r"$x_{n-1}$ and $p_{i-1}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "xₙ₋₁" in output
    assert "pᵢ₋₁" in output
    assert "$" not in output


def test_arithmetic_subscript_plus():
    """Test arithmetic subscripts with plus: x_{i+1} → xᵢ₊₁"""
    latex = r"$x_{i+1}$ and $a_{k+1}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "xᵢ₊₁" in output
    assert "aₖ₊₁" in output
    assert "$" not in output


def test_arithmetic_subscript_with_digits():
    """Test arithmetic subscripts with digits: a_{0-1}, b_{1+1}"""
    latex = r"$a_{0-1}$ and $b_{1+2}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "a₀₋₁" in output
    assert "b₁₊₂" in output
    assert "$" not in output


def test_arithmetic_subscript_unconvertible():
    """Test that unconvertible arithmetic subscripts stay as LaTeX"""
    # Capital letters don't have subscript equivalents
    latex = r"$X_{N-1}$ and $E_{M+1}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should stay as LaTeX since N, M have no subscript form
    assert "$X_{N-1}$" in output
    assert "$E_{M+1}$" in output


def test_mixed_simple_and_arithmetic_subscripts():
    """Test mixed simple and arithmetic subscripts in same expression"""
    latex = r"$x_i$ and $x_{i-1}$ and $x_{i+1}$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "xᵢ" in output
    assert "xᵢ₋₁" in output
    assert "xᵢ₊₁" in output
    assert "$" not in output


# Ordinal superscript tests
def test_ordinal_superscript_th():
    """Test ordinal superscripts with 'th': i^\text{th} → iᵗʰ"""
    latex = r"$i^\text{th}$ element and $n^\text{th}$ item."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "iᵗʰ" in output
    assert "nᵗʰ" in output
    assert "$" not in output


def test_ordinal_superscript_st_nd_rd():
    """Test ordinal superscripts with st/nd/rd: 1^\text{st}, 2^\text{nd}, 3^\text{rd}"""
    latex = r"$1^\text{st}$, $2^\text{nd}$, and $3^\text{rd}$ elements."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "1ˢᵗ" in output
    assert "2ⁿᵈ" in output
    assert "3ʳᵈ" in output
    assert "$" not in output


# Absolute value tests
def test_absolute_value_with_comparison():
    """Test absolute value with comparison operators: |k| ≤ 1"""
    latex = r"$|k| \le 1$ and $|x| \ge 0$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "|k| ≤ 1" in output
    assert "|x| ≥ 0" in output
    assert "$" not in output


def test_absolute_value_simple():
    """Test simple absolute value expressions"""
    latex = r"$|a + b| = |c|$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "|a + b| = |c|" in output
    assert "$" not in output


# Tests for improved Unicode conversions (empty braces, new superscripts, bitwise ops)
def test_empty_braces_stripped():
    """Test empty braces {} are stripped from math expressions"""
    latex = r"Value $x{}^2$ and $a_1, \dotsc{}, a_n$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "x²" in output
    assert "a₁, …, aₙ" in output
    assert "$" not in output


def test_cv_macro_conversion():
    """Test \\cv{} macro converts to plain text 'cv'"""
    latex = r"Type is $\cv{}_i$ where i is the index."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cvᵢ" in output
    assert "$" not in output


def test_cv_macro_with_multiple_subscripts():
    """Test \\cv{} with multiple subscript patterns"""
    latex = r"Qualifiers $\cv{}_1$ and $\cv{}_2$ are related."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cv₁" in output
    assert "cv₂" in output
    assert "$" not in output


def test_expanded_superscript_letters():
    """Test expanded superscript character set (29 new letters)"""
    latex = r"Values $x^a$, $y^b$, $z^c$, $n^d$, $f^e$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "xᵃ" in output
    assert "yᵇ" in output
    assert "zᶜ" in output
    assert "nᵈ" in output
    assert "fᵉ" in output
    assert "$" not in output


def test_superscript_letters_extended():
    """Test additional superscript letters"""
    latex = r"More letters: $g^h$, $i^j$, $k^l$, $m^o$, $p^r$, $s^t$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "gʰ" in output
    assert "iʲ" in output
    assert "kˡ" in output
    assert "mᵒ" in output
    assert "pʳ" in output
    assert "sᵗ" in output
    assert "$" not in output


def test_superscript_uppercase_N():
    """Test superscript uppercase N"""
    latex = r"Modulo $2^N$ where N is width."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "2ᴺ" in output
    assert "$" not in output


def test_bitwise_xor_operator():
    """Test \\oplus (XOR) bitwise operator"""
    latex = r"Result is $a \oplus b$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "a ⊕ b" in output
    assert "$" not in output


def test_bitwise_shift_operators():
    """Test \\ll and \\gg shift operators convert to ASCII << and >>"""
    latex = r"Shifts: $x \ll 2$ and $y \gg 3$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "x << 2" in output
    assert "y >> 3" in output
    assert "$" not in output


def test_bitwise_logical_synonyms():
    """Test \\wedge and \\vee (synonyms for \\land and \\lor)"""
    latex = r"Logical: $p \wedge q$ and $r \vee s$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "p ∧ q" in output
    assert "r ∨ s" in output
    assert "$" not in output


def test_bitwise_mid_operator():
    """Test \\mid (divides) operator"""
    latex = r"Relation $n \mid m$ means n divides m."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "n | m" in output
    assert "$" not in output


def test_superscript_and_subscript_combined():
    """Test superscript followed by subscript (e.g., cvʲᵢ)"""
    latex = r"Pattern $cv{}^j_i$ converts fully."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cvʲᵢ" in output
    assert "$" not in output


def test_superscript_subscript_multiple():
    """Test multiple superscript+subscript combinations"""
    latex = r"Components $cv{}^1_i$, $cv{}^2_i$, and $cv{}^3_i$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cv¹ᵢ" in output
    assert "cv²ᵢ" in output
    assert "cv³ᵢ" in output
    assert "$" not in output


def test_combined_improvements():
    """Test all improvements working together"""
    latex = r"Expression $\cv{}_i \oplus x^a + 2^N$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cvᵢ ⊕ xᵃ + 2ᴺ" in output
    assert "$" not in output


# Tests for additional operators (sim, backslash) and ordinals without \text{}
def test_sim_operator():
    """Test \\sim (similar to) operator converts to ~ (ASCII tilde)"""
    latex = r"Type $T_1 \sim T_2$ means similar."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "T₁ ~ T₂" in output
    assert "$" not in output


def test_backslash_operator():
    """Test \\backslash operator converts to \\ (ASCII backslash)"""
    latex = r"Set difference $A \backslash B$."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "A \\ B" in output or "A \\\\ B" in output  # Markdown may escape it
    assert "$" not in output


def test_ordinal_without_text_th():
    """Test ordinal ^{th} without \\text{} wrapper"""
    latex = r"The $i^{th}$ element and $j^{th}$ item."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "iᵗʰ" in output
    assert "jᵗʰ" in output
    assert "$" not in output


def test_ordinal_without_text_st_nd_rd():
    """Test ordinals ^{st}, ^{nd}, ^{rd} without \\text{} wrapper"""
    latex = r"The $1^{st}$, $2^{nd}$, and $3^{rd}$ items."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "1ˢᵗ" in output
    assert "2ⁿᵈ" in output
    assert "3ʳᵈ" in output
    assert "$" not in output
