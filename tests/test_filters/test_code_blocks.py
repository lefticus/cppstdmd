"""Tests for cpp-code-blocks.lua filter"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-code-blocks.lua")


def run_pandoc_with_filter(latex_content, filter_name="cpp-code-blocks.lua"):
    """Helper to run Pandoc with a filter on LaTeX content"""
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


def test_basic_codeblock():
    """Test basic codeblock conversion"""
    latex = r"""
\begin{codeblock}
int main() {
    return 0;
}
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "``` cpp" in output
    assert "int main()" in output
    assert "return 0" in output


def test_codeblock_with_commentellip():
    r"""Test @\commentellip@ expansion"""
    latex = r"""
\begin{codeblock}
int a, b;
@\commentellip@
a = a + 32760 + b + 5;
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "..." in output
    assert "@" not in output  # @ should be removed


def test_codeblock_with_tcode():
    """Test @\tcode{x}@ expansion"""
    latex = r"""
\begin{codeblock}
void foo(@\tcode{int}@ x) {
}
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "int" in output
    assert "@" not in output


def test_codeblocktu():
    """Test codeblocktu (translation unit) environment"""
    latex = r"""
\begin{codeblocktu}{example.cpp}
int main() { }
\end{codeblocktu}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "``` cpp" in output
    assert "int main()" in output


def test_outputblock():
    """Test outputblock environment"""
    latex = r"""
\begin{outputblock}
Hello, World!
\end{outputblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "```" in output
    assert "Hello, World!" in output


def test_codeblockdigitsep():
    """Test codeblockdigitsep environment"""
    latex = r"""
\begin{codeblockdigitsep}
int x = 1'000'000;
int y = 0b1010'1010;
\end{codeblockdigitsep}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "``` cpp" in output
    assert "1'000'000" in output
    assert "0b1010'1010" in output


def test_libconcept_in_codeblock():
    r"""Test \libconcept{} macro inside code block"""
    latex = r"""
\begin{codeblock}
template<@\libconcept{input_iterator}@ I>
void process(I first, I last);
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "input_iterator" in output
    assert "libconcept" not in output.lower()
    assert "@" not in output


def test_iref_in_codeblock():
    r"""Test \iref{} macro inside code block"""
    latex = r"""
\begin{codeblock}
// See @\iref{basic.scope}@ for details
int x;
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "[basic.scope]" in output
    assert "iref" not in output.lower()
    assert "@" not in output


def test_seebelow_in_codeblock():
    r"""Test \seebelow macro inside code block"""
    latex = r"""
\begin{codeblock}
auto result = function(); // returns @\seebelow@
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "see below" in output
    assert "seebelow" not in output.lower()
    assert "@" not in output


def test_unspec_in_codeblock():
    r"""Test \unspec macro inside code block"""
    latex = r"""
\begin{codeblock}
int value = @\unspec@; // unspecified value
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "unspecified" in output
    assert "@" not in output


def test_expos_in_codeblock():
    r"""Test \expos macro inside code block"""
    latex = r"""
\begin{codeblock}
struct S {
  int member; // @\expos@
};
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "exposition only" in output
    assert "\\expos" not in output
    assert "@" not in output


def test_exposidnc_in_codeblock():
    r"""Test @\exposidnc{}@ macro inside code block (ranges.md/iterators.md bug)"""
    latex = r"""
\begin{codeblock}
template<bool Const, class T>
  using @\exposidnc{maybe-const}@ = conditional_t<Const, const T, T>;   // exposition only
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have just the identifier name
    assert "maybe-const" in output
    # Should NOT have the macro name or corrupted output
    assert "exposidnc" not in output.lower()
    assert "exposition onlyidnc" not in output
    assert "exposition only idnc" not in output
    # @ delimiters should be removed
    assert "@" not in output
    # Backslashes should be gone
    assert "\\" not in output


def test_unsp_with_impldef_in_codeblock():
    r"""Test @\UNSP{\impldef{}}@ nested macros in code block"""
    latex = r"""
\begin{codeblock}
namespace std {
  #if defined(__STDCPP_FLOAT16_T__)
    using float16_t  = @\UNSP{\impldef{type of std::float16_t}}@;
  #endif
}
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "implementation-defined" in output
    # LaTeX commands should be gone
    assert "\\UNSP" not in output
    assert "\\impldef" not in output
    # @ delimiters should be gone
    assert "@" not in output


def test_unsp_simple_in_codeblock():
    r"""Test @\UNSP{text}@ without nested macros"""
    latex = r"""
\begin{codeblock}
auto x = @\UNSP{some value}@;
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "some value" in output
    assert "\\UNSP" not in output
    assert "@" not in output


def test_defnlibxname_in_codeblock():
    r"""Test \defnlibxname{} macro expansion in code blocks"""
    latex = r"""
\begin{codeblock}
#define @\defnlibxname{cpp_lib_addressof_constexpr}@  201603L
#define @\defnlibxname{cpp_lib_optional}@              201606L
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "__cpp_lib_addressof_constexpr" in output
    assert "__cpp_lib_optional" in output
    assert "\\defnlibxname" not in output
    assert "@" not in output


def test_xname_in_codeblock():
    r"""Test \xname{} macro expansion in code blocks"""
    latex = r"""
\begin{codeblock}
@\xname{some_name}@ = 42;
typedef @\xname{type}@ MyType;
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "__some_name" in output
    assert "__type" in output
    assert "\\xname" not in output
    assert "@" not in output


def test_mname_in_codeblock():
    r"""Test \mname{} macro expansion in code blocks"""
    latex = r"""
\begin{codeblock}
#if @\mname{LINE}@ > 100
  #error "Line number is @\mname{LINE}@"
#endif
@\mname{VA_ARGS}@ expansion test
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "__LINE__" in output
    assert "__VA_ARGS__" in output
    assert "\\mname" not in output
    assert "@" not in output


def test_libheader_in_codeblock():
    r"""Test \libheader{} macro expansion in code blocks (plain angle brackets)"""
    latex = r"""
\begin{codeblock}
#include @\libheader{memory}@
#include @\libheader{vector}@
// also in @\libheader{algorithm}@
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "<memory>" in output
    assert "<vector>" in output
    assert "<algorithm>" in output
    # Should be plain angle brackets, not backticks
    assert "`<memory>`" not in output
    assert "\\libheader" not in output
    assert "@" not in output


def test_texttt_in_codeblock():
    r"""Test \texttt{} in code comments"""
    latex = r"""
\begin{codeblock}
T* p1 = new T;  // throws \texttt{bad_alloc} if it fails
T* p2 = new(nothrow) T;  // returns \keyword{nullptr} if it fails
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "bad_alloc" in output
    assert "nullptr" in output
    assert "\\texttt" not in output
    assert "\\keyword" not in output


def test_placeholder_with_empty_braces():
    r"""Test \placeholder{name}{} with empty braces suffix"""
    latex = r"""
\begin{codeblock}
constexpr @\placeholder{bitmask}{}@ operator&(@\placeholder{bitmask}{}@ X, @\placeholder{bitmask}{}@ Y) {
  return static_cast<@\placeholder{bitmask}{}@>(
    static_cast<int_type>(X) & static_cast<int_type>(Y));
}
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have just "bitmask" without the empty braces
    assert "constexpr bitmask operator&" in output
    assert "bitmask X" in output
    assert "bitmask Y" in output
    assert "static_cast<bitmask>" in output
    # Should NOT have empty braces
    assert "bitmask{}" not in output
    assert "\\placeholder" not in output
    assert "@" not in output


def test_ucode_in_textrm_in_codeblock():
    r"""Test \textrm{\ucode{}} nested in code blocks (uax31.md bug)"""
    latex = r"""
\begin{codeblock}
<Start> := XID_Start + @\textrm{\ucode{005f}}@
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "U+005f" in output or "U+005F" in output
    # Should NOT have unprocessed LaTeX
    assert "\\textrm" not in output
    assert "\\ucode" not in output
    assert "@" not in output


def test_nested_macros_in_code_comments():
    r"""Test nested macros like \tcode{\keyword{x}} in code comments (except.md bug)"""
    latex = r"""
\begin{codeblock}
struct B {
  B() noexcept;
  B(const B&) = default;        // implicit exception specification is \tcode{\keyword{noexcept}(\keyword{true})}
  B(B&&, int = (throw 42, 0)) noexcept;
};
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have expanded all nested macros
    assert "noexcept(true)" in output
    # Should NOT have unprocessed LaTeX
    assert "\\tcode" not in output
    assert "\\keyword" not in output


def test_texttt_in_code_comments():
    r"""Test \texttt{} in code comments (support.md bug)"""
    latex = r"""
\begin{codeblock}
T* p2 = new(nothrow) T;         // returns \keyword{nullptr} if it fails
X* p = new X;
new (const_cast<X*>(p)) const X{5}; // \texttt{p} does not point to new object because its type is \keyword{const}
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have expanded all macros
    assert "returns nullptr if it fails" in output
    assert "p does not point to new object" in output
    assert "const" in output
    # Should NOT have unprocessed LaTeX
    assert "\\keyword" not in output
    assert "\\texttt" not in output


def test_math_subscripts_in_codeblock():
    r"""Test math subscripts @$c_1$@ conversion to Unicode in code blocks (Issue #24)"""
    latex = r"""
\begin{codeblock}
operator ""X<'@$c_1$@', '@$c_2$@', ... '@$c_k$@'>()
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have Unicode subscripts
    assert "c₁" in output
    assert "c₂" in output
    assert "cₖ" in output
    # Should NOT have literal underscores
    assert "c_1" not in output
    assert "c_2" not in output
    assert "c_k" not in output
    # Should NOT have raw math delimiters
    assert "$" not in output
    assert "@" not in output


def test_libglobal_in_codeblock():
    r"""Test \libglobal{} macro stripping in code blocks (Issue #24)"""
    latex = r"""
\begin{codeblock}
  using @\libglobal{string}@    = basic_string<char>;
  using @\libglobal{u8string}@  = basic_string<char8_t>;
  using @\libglobal{u16string}@ = basic_string<char16_t>;
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have plain identifiers
    assert "using string    = basic_string<char>" in output
    assert "using u8string  = basic_string<char8_t>" in output
    assert "using u16string = basic_string<char16_t>" in output
    # Should NOT have \libglobal macro
    assert "\\libglobal" not in output
    # Should NOT have @ delimiters
    assert "@" not in output


def test_libmember_in_codeblock():
    r"""Test \libmember{member}{class} macro stripping in code blocks (Issue #24)"""
    latex = r"""
\begin{codeblock}
  class @\libmember{reference}{vector<bool>}@ {
    // member functions
  };
  constexpr empty_view<T> @\libmember{empty}{views}@{};
\end{codeblock}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have plain member names (without class names)
    assert "class reference {" in output
    assert "constexpr empty_view<T> empty{};" in output
    # Should NOT have class names like {vector<bool>} or {views}
    assert "{vector<bool>}" not in output
    assert "{views}" not in output
    # Should NOT have \libmember macro
    assert "\\libmember" not in output
    # Should NOT have @ delimiters
    assert "@" not in output
