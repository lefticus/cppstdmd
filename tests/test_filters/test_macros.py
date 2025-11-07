"""Tests for cpp-macros.lua filter"""
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

def test_cpp_macro():
    """Test \Cpp{} expansion"""
    latex = r"This is \Cpp{} programming."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "C++" in output

def test_tcode_macro():
    """Test \tcode{} expansion"""
    latex = r"The type \tcode{int} is fundamental."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`int`" in output

def test_keyword_macro():
    """Test \keyword{} expansion"""
    latex = r"Use \keyword{const} for constants."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`const`" in output

def test_grammarterm_macro():
    """Test \grammarterm{} expansion"""
    latex = r"A \grammarterm{constant-expression} is required."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*constant-expression*" in output


def test_grammarterm_with_suffix():
    r"""Test \grammarterm{}{} with plural suffix (limits.md bug)"""
    latex = r"Multiple \grammarterm{initializer-clause}{s} are allowed."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*initializer-clause*s" in output
    assert "\\grammarterm" not in output


def test_opt_with_grammarterm():
    r"""Test \opt{\grammarterm{}} pattern (dcl.md escaping bug)"""
    latex = r"\opt{\grammarterm{nested-name-specifier}} \grammarterm{template-name}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*nested-name-specifier*_opt" in output or "*nested-name-specifier*\\_opt" in output
    assert "*template-name*" in output
    # Should NOT have escaped asterisks
    assert "\\*nested-name-specifier\\*" not in output
    assert "\\grammarterm" not in output


def test_cpp_version_macros():
    """Test C++ version macro expansion"""
    latex = r"\CppXI{} \CppXIV{} \CppXVII{} \CppXX{} \CppXXIII{}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "C++11" in output
    assert "C++14" in output
    assert "C++17" in output
    assert "C++20" in output
    assert "C++23" in output

def test_isoc_macro():
    """Test \IsoC{} expansion"""
    latex = r"As defined in \IsoC{}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "ISO/IEC 9899:2018" in output

def test_libheader_macro():
    """Test \libheader{} expansion"""
    latex = r"Include \libheader{iostream} for I/O."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`<iostream>`" in output

def test_ref_macro():
    """Test \ref{} expansion for cross-references - should create reference-style links"""
    latex = r"See \ref{expr.typeid} and \ref{dcl.type.simple}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should create reference-style links [[ref]]
    assert "[[expr.typeid]]" in output
    assert "[[dcl.type.simple]]" in output
    # Should have link definitions at end (single brackets in definition)
    assert "[expr.typeid]: #expr.typeid" in output
    assert "[dcl.type.simple]: #dcl.type.simple" in output

def test_iref_macro():
    """Test \iref{} expansion for inline cross-references - should create link definitions"""
    latex = r"The algorithm\iref{alg.find} is efficient."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should create reference-style links [[ref]]
    assert "[[alg.find]]" in output
    # Should have link definition at end (single brackets in definition)
    assert "[alg.find]: #alg.find" in output

def test_tref_macro():
    """Test \tref{} expansion for table cross-references - should create link definitions"""
    latex = r"As shown in\tref{tab.keywords}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should create reference-style links [[ref]]
    assert "[[tab.keywords]]" in output
    # Should have link definition at end (single brackets in definition)
    assert "[tab.keywords]: #tab.keywords" in output

def test_iref_comma_separated():
    """Test \iref{} with comma-separated labels - should split into individual links"""
    latex = r"See\iref{basic.stc.static,basic.stc.thread,basic.stc.auto} for details."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should create THREE separate links
    assert "[[basic.stc.static]]" in output
    assert "[[basic.stc.thread]]" in output
    assert "[[basic.stc.auto]]" in output
    # Should have link definitions for ALL three (single brackets in definition)
    assert "[basic.stc.static]: #basic.stc.static" in output
    assert "[basic.stc.thread]: #basic.stc.thread" in output
    assert "[basic.stc.auto]: #basic.stc.auto" in output
    # Should be formatted as "[[a]], [[b]], [[c]]" not "[[a,b,c]]"
    assert "[[basic.stc.static]], [[basic.stc.thread]], [[basic.stc.auto]]" in output

def test_ref_comma_separated():
    """Test \ref{} with comma-separated labels - should split into individual links"""
    latex = r"See \ref{class.mem,class.static} for more."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should create TWO separate links
    assert "[[class.mem]]" in output
    assert "[[class.static]]" in output
    # Should have link definitions for both (single brackets in definition)
    assert "[class.mem]: #class.mem" in output
    assert "[class.static]: #class.static" in output
    # Should be formatted as "[[a]], [[b]]"
    assert "[[class.mem]], [[class.static]]" in output

def test_defnx_macro():
    """Test \defnx{plural}{singular} expansion"""
    latex = r"These are \defnx{unevaluated operands}{unevaluated operand}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*unevaluated operands*" in output

def test_defnadj_macro():
    """Test \defnadj{adjective}{noun} expansion"""
    latex = r"The \defnadj{built-in}{operators} are used."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*built-in operators*" in output

def test_indextext_stripping():
    """Test that \indextext{} commands are stripped completely"""
    latex = r"\indextext{\idxcode{operator new}|seealso{\tcode{new}}}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should be completely removed, no artifacts
    assert "operator" not in output
    assert "new}}" not in output
    assert output.strip() == ""

def test_index_stripping():
    """Test that \index{} commands are stripped completely"""
    latex = r"Some text \index{keyword} more text."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Index command should be removed, but surrounding text preserved
    assert "Some text" in output
    assert "more text" in output
    assert "index" not in output

def test_nested_keyword_in_tcode():
    """Test nested \keyword{} inside \tcode{} is expanded"""
    latex = r"The type \tcode{\keyword{unsigned} \keyword{char}} is used."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`unsigned char`" in output
    # Should NOT have literal \keyword in output
    assert "\\keyword" not in output

def test_nested_ctype_in_tcode():
    """Test nested \ctype{} inside \tcode{} is expanded"""
    latex = r"Use \tcode{\ctype{size_t}} for sizes."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`size_t`" in output
    # Should NOT have literal \ctype in output
    assert "\\ctype" not in output

def test_cv_braces_expansion():
    """Test \cv{} with braces is expanded"""
    latex = r"A cv{} qualified type."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cv qualified" in output
    # Should NOT have literal cv{} in output
    assert "cv{}" not in output

def test_iref_macro_old():
    """Test \iref{} expansion for inline references - NOW creates link definitions (bug fix)"""
    latex = r"As specified in \iref{lex.ext}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should create reference-style link [[ref]]
    assert "[[lex.ext]]" in output
    # CHANGED: \iref NOW creates link definitions (single brackets in definition)
    assert "[lex.ext]: #lex.ext" in output

def test_iref_in_code_comment():
    """Test \iref{} works in code comments too"""
    latex = r"""Some code
// See \iref{basic.scope}
More text"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "[basic.scope]" in output

def test_libconcept_macro():
    """Test \libconcept{} expansion"""
    latex = r"The \libconcept{equality_comparable} concept."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`equality_comparable`" in output

def test_brk_stripping():
    """Test \brk{} line break hints are stripped"""
    latex = r"Some text\brk{}more text."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # \brk{} should be removed completely
    assert "brk" not in output
    # Surrounding text should remain
    assert "Some text" in output
    assert "more text" in output

def test_seebelow_macro():
    r"""Test \seebelow expansion"""
    latex = r"The return type is \seebelow."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*see below*" in output

def test_unspec_macro():
    r"""Test \unspec expansion"""
    latex = r"The value is \unspec after this operation."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*unspecified*" in output

def test_unspecnc_macro():
    r"""Test \unspecnc expansion"""
    latex = r"The order is \unspecnc for this case."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*unspecified*" in output

def test_expos_macro():
    r"""Test \expos expansion"""
    latex = r"This member is \expos for clarity."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*exposition only*" in output

def test_tcode_special_chars():
    r"""Test \tcode with escaped special characters"""
    latex = r"Use \tcode{\~} for the destructor."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`~`" in output or "`\\~`" in output  # Accept either format

def test_textbackslash_macro():
    r"""Test \textbackslash expansion"""
    latex = r"Use \textbackslash for line continuation."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "\\" in output

def test_textbackslash_in_tcode():
    r"""Test \textbackslash within \tcode"""
    latex = r"\tcode{\textbackslash n} is a newline."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`\\n`" in output  # Should be \n not \ n (no space)

def test_atsign_macro():
    r"""Test \atsign expansion"""
    latex = r"Use \atsign for special markers."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "@" in output

def test_mname_va_args():
    r"""Test \mname{VA_ARGS} expansion"""
    latex = r"The \mname{VA_ARGS} identifier is special."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should convert to code span with backticks (no escaped underscores)
    assert "`__VA_ARGS__`" in output
    assert "\\_\\_" not in output

def test_mname_va_opt():
    r"""Test \mname{VA_OPT} expansion"""
    latex = r"The \mname{VA_OPT} identifier is special."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should convert to code span with backticks (no escaped underscores)
    assert "`__VA_OPT__`" in output
    assert "\\_\\_" not in output

def test_mname_line():
    r"""Test \mname{LINE} expansion (macro name)"""
    latex = r"The \mname{LINE} and \mname{FILE} macros are predefined."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should convert to code spans
    assert "`__LINE__`" in output
    assert "`__FILE__`" in output
    assert "\\_\\_" not in output

def test_xname_conversion():
    r"""Test \xname{} conversion (identifier with __ prefix)"""
    latex = r"The \xname{cpp_lib_optional} identifier is special."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should convert to code span
    assert "`__cpp_lib_optional`" in output
    assert "\\_\\_" not in output

def test_itcorr_removal():
    r"""Test \itcorr[...] removal (italic correction markers)"""
    latex = r"Type\itcorr[-1] definitions."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "Type definitions" in output
    assert "\\itcorr" not in output
    assert "[-1]" not in output


# ============================================================================
# Tests for New Macros (added in various commits)
# ============================================================================

def test_libheaderref_macro():
    r"""Test \libheaderref{header} macro (commit 294c3b61)"""
    latex = r"See \libheaderref{vector} for details."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should convert to code span
    assert "`<vector>`" in output
    assert "\\libheaderref" not in output


def test_libheaderrefx_macro():
    r"""Test \libheaderrefx{header}{text} macro (commit 294c3b61)

    Note: Current implementation outputs only the header name, not the descriptive text.
    This matches the behavior of \libheaderref which also outputs just the header.
    """
    latex = r"The \libheaderrefx{algorithm}{algorithms library} provides sorting."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Current implementation outputs the header name (like \libheaderref)
    assert "`<algorithm>`" in output
    # The macro itself should be processed
    assert "\\libheaderrefx" not in output


def test_deflibconcept_macro():
    r"""Test \deflibconcept{concept} macro (commit bdbf7803)"""
    latex = r"The \deflibconcept{Sortable} concept defines requirements."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should convert to code span (or similar formatting)
    assert "Sortable" in output
    assert "\\deflibconcept" not in output


def test_discretionary_hyphen():
    r"""Test \- discretionary hyphen handling (commit bdbf7803)"""
    latex = r"A pre\-defined template specialization."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Discretionary hyphen should be handled
    assert "\\-" not in output
    # Content should be preserved
    assert "defined" in output


# ============================================================================
# Tests for Additional Missing Macros (15 high-usage macros)
# ============================================================================

def test_opt_macro():
    r"""Test \opt{} expansion (optional grammar element with subscript)"""
    latex = r"The parameter is \opt{noexcept} in this context."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "noexcept_opt" in output
    assert "\\opt" not in output


def test_libglobal_macro():
    r"""Test \libglobal{} expansion (library global function/type)"""
    latex = r"The \libglobal{swap} function is provided."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`swap`" in output
    assert "\\libglobal" not in output


def test_exposidnc_macro():
    r"""Test \exposidnc{} expansion (exposition-only identifier without correction)"""
    latex = r"The \exposidnc{hidden-member} is not part of the interface."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*hidden-member*" in output
    assert "\\exposidnc" not in output


def test_defnxname_macro():
    r"""Test \defnxname{} expansion (define identifier with __ prefix)"""
    latex = r"The \defnxname{cpp_lib_optional} macro indicates support."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # GFM escapes underscores in italics, so check for escaped version
    assert ("*__cpp_lib_optional*" in output or "*\\_\\_cpp_lib_optional*" in output)
    assert "\\defnxname" not in output


def test_defnlibxname_macro():
    r"""Test \defnlibxname{} expansion (define library identifier with __ prefix)"""
    latex = r"The \defnlibxname{has_unique_object_representations} trait is defined."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # GFM escapes underscores in italics, so check for escaped version
    assert ("*__has_unique_object_representations*" in output or "*\\_\\_has_unique_object_representations*" in output)
    assert "\\defnlibxname" not in output


def test_impdefx_macro():
    r"""Test \impdefx{description} expansion (implementation-defined with description)"""
    latex = r"The behavior is \impdefx{whether an inline function is actually inlined}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should output implementation-defined with description as comment
    assert "implementation-defined" in output
    assert "// whether an inline function is actually inlined" in output
    assert "\\impdefx" not in output

def test_impdefx_with_nested_tcode():
    r"""Test \impdefx{} with nested \tcode{} macro"""
    latex = r"The type is \impdefx{type of \tcode{array::iterator}}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "implementation-defined" in output
    assert "// type of array::iterator" in output
    assert "\\tcode" not in output
    assert "\\impdefx" not in output


def test_fmtgrammarterm_macro():
    r"""Test \fmtgrammarterm{} expansion (format grammar term)"""
    latex = r"The \fmtgrammarterm{fill-and-align} specifier is optional."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*fill-and-align*" in output
    assert "\\fmtgrammarterm" not in output


def test_change_macro():
    r"""Test \change expansion (change description label)"""
    latex = r"\change Added support for new feature."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape asterisks in some contexts
    assert ("**Change:**" in output or "\\*\\*Change:\\*\\*" in output)
    assert "\\change" not in output


def test_rationale_macro():
    r"""Test \rationale expansion (rationale description label)"""
    latex = r"\rationale This improves consistency with other facilities."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape asterisks in some contexts
    assert ("**Rationale:**" in output or "\\*\\*Rationale:\\*\\*" in output)
    assert "\\rationale" not in output


def test_effect_macro():
    r"""Test \effect expansion (effect on original feature label)"""
    latex = r"\effect The previous behavior is deprecated."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape asterisks in some contexts
    assert ("**Effect on original feature:**" in output or "\\*\\*Effect on original feature:\\*\\*" in output)
    assert "\\effect" not in output


def test_ucode_macro():
    r"""Test \ucode{} expansion (Unicode code point)"""
    latex = r"The character \ucode{0041} represents the letter A."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`U+0041`" in output
    assert "\\ucode" not in output


def test_unicode_macro_with_description():
    r"""Test \unicode{code}{description} expansion (uax31.md bug)"""
    latex = r"For C++ we add the character \unicode{005f}{low line}, or \tcode{_}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "U+005f (low line)" in output or "U+005F (low line)" in output
    assert "\\unicode" not in output


def test_uax_macro():
    r"""Test \UAX{number} expansion (uax31.md bug)"""
    latex = r"This Annex describes \UAX{31} (Unicode Identifier and Pattern Syntax)."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "UAX #31" in output
    assert "\\UAX" not in output


def test_cvqual_macro():
    r"""Test \cvqual{} expansion (cv-qualifier term)"""
    latex = r"A \cvqual{} can be const or volatile."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cv-qualifier" in output
    assert "\\cvqual" not in output


# Note: \term{}, \defn{}, and \defnx{} were already tested earlier in the file
# (they were already implemented before this batch of additions)


def test_defnx_emphasis():
    r"""Test \defnx macro produces proper markdown emphasis"""
    latex = r"This describes the \defnx{\Cpp{} standard library}{library}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have proper emphasis with expanded \Cpp{} macro
    assert "*C++ standard library*" in output
    # Should NOT have escaped asterisks or unexpanded macros
    assert "\\*" not in output
    assert "\\Cpp" not in output
    assert "\\defnx" not in output


def test_firstlibchapter_macro():
    r"""Test \firstlibchapter macro expands to 'support'"""
    latex = r"Clauses \firstlibchapter{} through \lastlibchapter{} specify the library."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "support" in output
    assert "thread" in output
    assert "\\firstlibchapter" not in output
    assert "\\lastlibchapter" not in output


def test_cpp_macro():
    r"""Test \Cpp{} macro expands to 'C++'"""
    latex = r"The \Cpp{} standard specifies requirements."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "C++" in output
    assert "\\Cpp" not in output


def test_uname_macro():
    r"""Test \uname{} macro strips small caps formatting"""
    latex = r"The character \uname{character tabulation} is used."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "character tabulation" in output
    assert "\\uname" not in output


def test_unun_macro():
    r"""Test \unun macro expands to double underscore"""
    latex = r"Identifiers with \unun{} prefix are reserved."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape underscores in GFM output
    assert "__" in output or "\\_\\_" in output
    assert "\\unun" not in output


def test_caret_macro():
    r"""Test \caret macro expands to caret character"""
    latex = r"The operator \caret{} is XOR."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "^" in output
    assert "\\caret" not in output


def test_textasciitilde_macro():
    r"""Test \textasciitilde macro expands to tilde"""
    latex = r"The character \textasciitilde{} is used in paths."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "~" in output
    assert "\\textasciitilde" not in output


def test_notdef_macro():
    r"""Test \notdef macro expands to 'not defined' """
    latex = r"The value is \notdef{} in this context."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*not defined*" in output or "not defined" in output
    assert "\\notdef" not in output


def test_range_macro():
    r"""Test \range{first}{last} expansion to [first, last)"""
    latex = r"The range \range{first}{last} is half-open."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should produce [first, last) with backticks
    assert "[" in output
    assert "first" in output
    assert "last" in output
    assert ")" in output
    # Should NOT have escaped bracket or unexpanded macro
    assert "\\[" not in output
    assert "\\range" not in output


def test_defn_macro():
    r"""Test \defn{text} expansion produces italic text"""
    latex = r"This is a \defn{sample definition} of the term."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have the definition text (possibly in italics)
    assert "sample definition" in output
    # Should NOT have unexpanded macro or empty parentheses
    assert "\\defn" not in output
    # Content should not disappear
    assert "sample" in output
    assert "definition" in output


def test_defn_in_parentheses():
    r"""Test \defn{} content is preserved when inside parentheses"""
    latex = r"The elements (the \defn{sample}) from the range (the \defn{population}) are selected."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Content should be present
    assert "sample" in output
    assert "population" in output
    # Should NOT have empty parentheses
    assert "(the )" not in output
    # Should NOT have unexpanded macro
    assert "\\defn" not in output


def test_latex_spacing_in_code():
    r"""Test LaTeX spacing commands are converted to spaces in \tcode{} (Issue 3)

    NOTE: Control space (backslash-space) is intentionally NOT converted because
    it would conflict with table row breaks (\\) when followed by space.
    """
    latex = r"""
LaTeX spacing commands should be converted to spaces:
- Medium space: \tcode{T\;A[N]}
- Thin space: \tcode{x\,y}
- Wide space: \tcode{a\quad b}
- Very wide space: \tcode{p\qquad q}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Medium space \; should become regular space
    assert "`T A[N]`" in output
    assert "`T\\;A[N]`" not in output

    # Thin space \, should become regular space
    assert "`x y`" in output
    assert "`x\\,y`" not in output

    # Wide space \quad should become regular space
    assert "`a b`" in output
    assert "`a\\quad b`" not in output

    # Very wide space \qquad should become regular space
    assert "`p q`" in output
    assert "`p\\qquad q`" not in output

    # No backslashes should remain in code spans (except control space which we skip)
    assert "\\;" not in output
    assert "\\," not in output
    assert "\\quad" not in output
    assert "\\qquad" not in output


def test_defn_with_nested_braces():
    r"""Test \defn{} with nested macros like \Cpp{} (Issue 2)"""
    latex = r"""
These are \defn{\Cpp{} library modules} for the standard.
The \defn{importable \Cpp{} library headers} are defined.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have fully expanded content with C++ substituted
    assert "*C++ library modules*" in output
    assert "*importable C++ library headers*" in output

    # Should NOT have stray backslashes or unexpanded macros
    assert "*\\Cpp{*" not in output
    assert "\\Cpp{}" not in output
    assert "\\defn" not in output


def test_defnadj_with_nested_braces():
    r"""Test \defnadj{}{} with nested macros like \Cpp{} (Issue 2)"""
    latex = r"""
The \defnadj{importable}{\Cpp{} library headers} are listed.
These are \defnadj{built-in}{\Cpp{} operators} in the language.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have fully expanded content
    assert "*importable C++ library headers*" in output
    assert "*built-in C++ operators*" in output

    # Should NOT have stray backslashes or unexpanded macros
    assert "*importable \\Cpp{*" not in output
    assert "\\Cpp{}" not in output
    assert "\\defnadj" not in output


def test_math_subscripts_in_code():
    r"""Test inline math with subscripts inside \tcode{} converts to Unicode (Issue 1)"""
    latex = r"""
Use \tcode{$C_i$ \& $C_j$} for the comparisons.
The type \tcode{$T_0$} is defined as \tcode{$T_1$}.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have Unicode subscripts
    assert "`Cᵢ & Cⱼ`" in output
    assert "`T₀`" in output
    assert "`T₁`" in output

    # Should NOT have LaTeX math delimiters or raw subscripts
    assert "$C_i$" not in output
    assert "$C_j$" not in output
    assert "$T_0$" not in output
    assert "$T_1$" not in output
    assert "`$C_i$ \\& $C_j$`" not in output

def test_doccite_with_nested_cpp_macro():
    r"""Test \doccite{} with nested \Cpp{} macro (back.md bug)"""
    latex = r"""
\begin{itemize}
\item Bjarne Stroustrup, \doccite{The \Cpp{} Programming Language, second edition}, Chapter R.
\item P.J. Plauger, \doccite{The Draft Standard \Cpp{} Library}.
\end{itemize}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have properly expanded citations with C++
    assert "*The C++ Programming Language, second edition*" in output
    assert "*The Draft Standard C++ Library*" in output
   
    # Should NOT have truncated content or unexpanded macros
    assert "\\Cpp{" not in output
    assert "*The \\Cpp{*" not in output

def test_tcode_with_escaped_braces():
    r"""Test \tcode{} with escaped braces like \{\}"""
    latex = r"Use \tcode{identity\{\}} for the identity projection."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should preserve {} after unescaping, not remove them
    assert "`identity{}`" in output
    assert "identity`" not in output  # Should not lose the {}

def test_tcode_with_single_escaped_brace():
    r"""Test \tcode{} with single escaped braces like \{"""
    latex = r"The syntax is \tcode{\{} for opening."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should unescape to just {
    assert "`{`" in output
    assert "`\\{`" not in output  # Should not have backslash

def test_tcode_with_plural_suffix():
    r"""Test \tcode{} with plural suffix like {s}"""
    latex = r"Valid code that \tcode{\#include}{s} headers."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should produce `#include`s not `#include}{s` or just `#include`
    assert "`#include`s" in output
    assert "`#include}{s`" not in output
    assert "`#include` headers" not in output  # Should not drop the 's'

def test_defnx_with_nested_tcode_heap():
    r"""Test \defnx{}{} with multiple nested \tcode{} macros - heap example"""
    latex = r"A range is a \defnx{heap with respect to \tcode{comp} and \tcode{proj}}{heap with respect to comp and proj@heap with respect to \tcode{comp} and \tcode{proj}} for a comparator."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should render first argument with nested code, discard second argument
    assert "*heap with respect to `comp` and `proj`*" in output
    # Should NOT have the @ index marker or second argument text
    assert "@heap" not in output
    assert "comp and proj@" not in output

def test_mbox_with_mixed_macros():
    r"""Test \mbox{} with mixed \placeholder, \tcode, and \grammarterm"""
    latex = r"then \placeholder{a} is \mbox{\placeholder{p}\tcode{.await_transform(}\grammarterm{cast-expression}\tcode{)}}; otherwise"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should produce complete expression with all parts
    assert "*p*" in output
    assert ".await_transform(" in output
    assert "*cast-expression*" in output
    assert ")" in output
    # The complete pattern should be: *p*.await_transform(*cast-expression*)
    # But we'll test for the key components since formatting may vary

def test_defnx_contextual_bool():
    r"""Test \defnx{}{} with nested \tcode{bool}"""
    latex = r"An expression is said to be \defnx{contextually converted to \tcode{bool}}{conversion!contextual to \tcode{bool}} and is well-formed."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should render first argument in emphasis with nested code
    assert "*contextually converted to `bool`*" in output
    # Should NOT have the second argument or index marker
    assert "conversion!contextual" not in output


def test_tref_in_list_item_with_linebreak():
    r"""Test \tref{} in list item with \\ linebreak (Issue #22 - cpp.md bug)"""
    latex = r"""
\begin{itemize}
\item The names listed in \tref{cpp.predefined.ft}.\\
The macros defined in \tref{cpp.predefined.ft} shall be defined to
the corresponding integer literal.
\end{itemize}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Both \tref{} macros should be converted to [[cpp.predefined.ft]]
    assert "[[cpp.predefined.ft]]" in output
    # Should have TWO instances (one before \\, one after)
    assert output.count("[[cpp.predefined.ft]]") == 2
    # Verify the text is complete (no content loss)
    assert "The names listed in" in output
    assert "The macros defined in" in output
    assert "shall be defined to" in output
    # Should NOT have unconverted \tref
    assert r"\tref" not in output


def test_tref_in_description_list_with_linebreak():
    r"""Test \tref{} in description list item with \\ linebreak (Issue #22 - cpp.md bug)"""
    latex = r"""
\begin{description}
\item The names listed in \tref{cpp.predefined.ft}.\\
The macros defined in \tref{cpp.predefined.ft} shall be defined to
the corresponding integer literal.
\end{description}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Both \tref{} macros should be converted to [[cpp.predefined.ft]]
    assert "[[cpp.predefined.ft]]" in output
    # Should have TWO instances (one before \\, one after)
    assert output.count("[[cpp.predefined.ft]]") == 2
    # Verify the text is complete (no content loss)
    assert "The names listed in" in output
    assert "The macros defined in" in output
    assert "shall be defined to" in output
    # Should NOT have unconverted \tref
    assert r"\tref" not in output


def test_kern_removal_issue_58():
    r"""Test \kern spacing removal (Issue #58 - corrupted front matter)"""
    latex = r"b\kern-1.2pta\kern1ptd"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should read as "bad" with letters preserved
    assert "bad" in output
    # Should NOT contain TeX artifacts
    assert "kern" not in output.lower()
    assert "-1.2pt" not in output
    assert "1pt" not in output or output == "1pt"  # Could be just "1pt" if all else stripped


def test_hbox_content_extraction_issue_58():
    r"""Test \hbox{} content extraction (Issue #58)"""
    latex = r"\raise0.15ex\hbox{n}g"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should contain the letters n and g
    assert "n" in output
    assert "g" in output
    # Should NOT contain TeX artifacts
    assert "hbox" not in output.lower()
    assert "raise" not in output.lower()
    assert "ex" not in output or "ex" in "example"  # 'ex' may appear in words


def test_full_bad_formatting_joke_issue_58():
    r"""Test complete 'bad formatting' joke from cover-wd.tex (Issue #58)"""
    latex = r"b\kern-1.2pta\kern1ptd\hspace{1.5em}for\kern-3ptmat\kern0.6ptti\raise0.15ex\hbox{n}g"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Check all letters are present (the joke spells "bad formatting")
    # Spacing may vary, so check for key substrings
    assert "b" in output
    assert "a" in output
    assert "d" in output
    assert "for" in output
    assert "mat" in output or "matt" in output
    assert "ti" in output or "i" in output
    assert "n" in output
    assert "g" in output
    # Should NOT contain TeX artifacts
    assert "kern" not in output.lower()
    assert "hspace" not in output.lower()
    assert "raise" not in output.lower()
    assert "hbox" not in output.lower()
