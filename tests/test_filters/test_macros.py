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

"""Tests for cpp-macros.lua filter"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-macros.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with macro filter"""
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


def test_cpp_macro():
    r"""Test \Cpp{} expansion"""
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
    r"""Test \keyword{} expansion"""
    latex = r"Use \keyword{const} for constants."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`const`" in output


def test_grammarterm_macro():
    r"""Test \grammarterm{} expansion"""
    latex = r"A \grammarterm{constant-expression} is required."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*constant-expression*" in output


def test_grammarterm_with_suffix():
    r"""Test \grammarterm{term}{suffix} expansion (normal plural form)"""
    latex = r"The remaining cases are \grammarterm{declaration}{s}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Normal case: suffix is outside emphasis
    assert "*declaration*s" in output
    # Ensure no malformed output
    assert "**declaration" not in output
    assert "\\*\\*{declaration}" not in output


def test_grammarterm_empty_first_arg():
    r"""Test \grammarterm{}{term} with empty first argument (n3337/n4140 bug)"""
    latex = r"The contained \grammarterm{}{statement} is executed."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*statement*" in output
    # Ensure no malformed output like **statement or \*\*{statement}
    assert "**statement" not in output
    assert "\\*\\*{statement}" not in output
    assert "{statement}" not in output


def test_grammarterm_empty_first_arg_with_plural():
    r"""Test \grammarterm{}{term}{s} with empty first argument and plural (n3337/n4140 bug)"""
    latex = r"The contained \grammarterm{}{statement} or \grammarterm{}{statement}{s} appear."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*statement*" in output
    # Plural suffix should be outside italics for consistency with normal pattern
    assert "*statement*s" in output
    # Ensure no malformed output
    assert "**statement" not in output
    assert "\\*\\*{statement}" not in output
    assert "{statement}" not in output


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
    r"""Test \IsoC{} expansion"""
    latex = r"As defined in \IsoC{}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "ISO/IEC 9899:2018" in output


def test_libheader_macro():
    r"""Test \libheader{} expansion"""
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
    r"""Test \iref{} expansion for inline cross-references - should create link definitions"""
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
    r"""Test \iref{} with comma-separated labels - should split into individual links"""
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
    r"""Test \defnx{plural}{singular} expansion"""
    latex = r"These are \defnx{unevaluated operands}{unevaluated operand}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*unevaluated operands*" in output


def test_defnadj_macro():
    r"""Test \defnadj{adjective}{noun} expansion"""
    latex = r"The \defnadj{built-in}{operators} are used."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*built-in operators*" in output


def test_indextext_stripping():
    r"""Test that \indextext{} commands are stripped completely"""
    latex = r"\indextext{\idxcode{operator new}|seealso{\tcode{new}}}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should be completely removed, no artifacts
    assert "operator" not in output
    assert "new}}" not in output
    assert output.strip() == ""


def test_index_stripping():
    r"""Test that \index{} commands are stripped completely"""
    latex = r"Some text \index{keyword} more text."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Index command should be removed, but surrounding text preserved
    assert "Some text" in output
    assert "more text" in output
    assert "index" not in output


def test_nested_keyword_in_tcode():
    """Test nested \\keyword{} inside \tcode{} is expanded"""
    latex = r"The type \tcode{\keyword{unsigned} \keyword{char}} is used."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`unsigned char`" in output
    # Should NOT have literal \keyword in output
    assert "\\keyword" not in output


def test_nested_ctype_in_tcode():
    """Test nested \\ctype{} inside \tcode{} is expanded"""
    latex = r"Use \tcode{\ctype{size_t}} for sizes."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`size_t`" in output
    # Should NOT have literal \ctype in output
    assert "\\ctype" not in output


def test_cv_braces_expansion():
    r"""Test \cv{} with braces is expanded"""
    latex = r"A cv{} qualified type."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cv qualified" in output
    # Should NOT have literal cv{} in output
    assert "cv{}" not in output


def test_cv_inside_tcode():
    r"""Test \cv{} macro inside \tcode{} blocks (n4950 pattern)"""
    latex = r"\tcode{\cv{} TD\&}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`cv TD&`" in output
    # Should NOT contain literal cv{} or escaped \cv
    assert "cv{}" not in output
    assert "\\cv" not in output


def test_cv_with_hyphen():
    r"""Test \cv-qualified and \cv-unqualified patterns (n3337 usage)"""
    latex = r"A pointer to \cv-qualified or \cv-unqualified type."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "cv-qualified" in output
    assert "cv-unqualified" in output
    # Should NOT lose hyphens
    assert "cvqualified" not in output
    assert "cvunqualified" not in output


def test_iref_macro_old():
    r"""Test \iref{} expansion for inline references - NOW creates link definitions (bug fix)"""
    latex = r"As specified in \iref{lex.ext}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should create reference-style link [[ref]]
    assert "[[lex.ext]]" in output
    # CHANGED: \iref NOW creates link definitions (single brackets in definition)
    assert "[lex.ext]: #lex.ext" in output


def test_iref_in_code_comment():
    r"""Test \iref{} works in code comments too"""
    latex = r"""Some code
// See \iref{basic.scope}
More text"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "[basic.scope]" in output


def test_libconcept_macro():
    r"""Test \libconcept{} expansion"""
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
    r"""Test \opt{} expansion (optional grammar element with Unicode subscript)"""
    latex = r"The parameter is \opt{noexcept} in this context."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should render with Unicode subscript: noexceptₒₚₜ
    assert "noexceptₒₚₜ" in output
    assert "\\opt" not in output


def test_libglobal_macro():
    r"""Test \libglobal{} expansion (library global function/type)"""
    latex = r"The \libglobal{swap} function is provided."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`swap`" in output
    assert "\\libglobal" not in output


def test_exposidnc_macro():
    r"""Test \exposidnc{} expansion (exposition-only identifier without correction)

    Should render as italic code: *`hidden-member`* (not just italic *hidden-member*)
    This ensures the identifier is both emphasized and formatted as code.
    """
    latex = r"The \exposidnc{hidden-member} is not part of the interface."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should produce italic code: *`hidden-member`*
    assert "*`hidden-member`*" in output
    assert "\\exposidnc" not in output


def test_exposconceptnc_macro():
    r"""Test \exposconceptnc{} expansion (exposition-only concept without correction) - Issue #49

    Should render as italic code: *`tuple-like`* (not just italic *tuple-like*)
    This ensures the concept name is both emphasized and formatted as code.
    """
    latex = r"template<\exposconceptnc{tuple-like} TTuple, \exposconceptnc{tuple-like} UTuple>"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should produce italic code: *`tuple-like`*
    assert "*`tuple-like`*" in output
    assert "\\exposconceptnc" not in output
    # Should not have the malformed "exposition onlyconceptnc" pattern
    assert "exposition onlyconceptnc" not in output


def test_seebelownc_macro():
    r"""Test \seebelownc expansion (see below without correction) - Issue #49"""
    latex = r"concept tuple-like = \seebelownc;"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*see below*" in output
    assert "\\seebelownc" not in output
    # Should not have the malformed "see belownc" pattern
    assert "see belownc" not in output


def test_seebelownc_with_empty_braces():
    r"""Test \seebelownc{} with empty braces - must consume the {} - Issue #49

    In containers.tex, \seebelownc{} is used with empty braces which must be consumed.
    """
    latex = r"using value_type = \seebelownc{};"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*see below*" in output
    # Must NOT have extra {} in output
    assert "*see below*{}" not in output
    assert "see below{}" not in output
    assert "\\seebelownc" not in output


def test_indexlibraryctor_strips_exposid():
    r"""Test \indexlibraryctor{} with \exposid{} inside - must strip entire macro - Issue #49

    The \indexlibraryctor{} macro is an indexing macro that should be completely stripped.
    Even if it contains \exposid{} inside its argument, the entire macro should disappear.
    This was causing *`iterator`* to appear in ranges.md when it shouldn't.
    """
    latex = r"\indexlibraryctor{repeat_view::\exposid{iterator}}%"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Entire index macro should be stripped - NO output at all
    assert output.strip() == ""
    # Must not have any trace of iterator or the index macro
    assert "iterator" not in output
    assert "\\indexlibraryctor" not in output
    assert "\\exposid" not in output


def test_defnxname_macro():
    r"""Test \defnxname{} expansion (define identifier with __ prefix)"""
    latex = r"The \defnxname{cpp_lib_optional} macro indicates support."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # GFM escapes underscores in italics, so check for escaped version
    assert "*__cpp_lib_optional*" in output or "*\\_\\_cpp_lib_optional*" in output
    assert "\\defnxname" not in output


def test_defnadjx_macro():
    r"""Test \defnadjx{} expansion (define term with adjective + plural) - Issue #29"""
    latex = r"collectively called \defnadjx{scalar}{types}{type}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*scalar types*" in output
    assert "\\defnadjx" not in output
    # Verify no dropped content - the sentence should be complete
    assert "collectively called ." not in output


def test_defnadjx_macro_multiple():
    r"""Test multiple \defnadjx{} instances with different terms - Issue #29"""
    latex = r"""Scalar types are collectively called \defnadjx{trivially copyable}{types}{type}.
Arrays are collectively called \defnadjx{standard-layout}{types}{type}."""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*trivially copyable types*" in output
    assert "*standard-layout types*" in output
    assert "\\defnadjx" not in output
    # Verify no dropped content
    assert "collectively called ." not in output


def test_defnx_macro_with_index():
    r"""Test \defnx{} expansion with index key (Issue #25)"""
    latex = r"The process is called \defnx{name lookup}{lookup!name}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*name lookup*" in output
    assert "\\defnx" not in output
    # Verify index key is stripped
    assert "lookup!name" not in output


def test_defnx_macro_in_table():
    r"""Test \defnx{} in table cells - Issue #25"""
    latex = r"""| none | \defnx{ordinary character literal}{literal!character!ordinary} | `char` |
| `u8` | \defnx{UTF-8 character literal}{literal!character!UTF-8} | `char8_t` |"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*ordinary character literal*" in output
    # UTF-8 may have newline from table formatting
    assert "UTF-8" in output and "character literal" in output
    assert "\\defnx" not in output
    # Verify index keys are stripped
    assert "literal!character!ordinary" not in output
    assert "literal!character!UTF-8" not in output


def test_defnlibxname_macro():
    r"""Test \defnlibxname{} expansion (define library identifier with __ prefix)"""
    latex = r"The \defnlibxname{has_unique_object_representations} trait is defined."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # GFM escapes underscores in italics, so check for escaped version
    assert (
        "*__has_unique_object_representations*" in output
        or "*\\_\\_has_unique_object_representations*" in output
    )
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
    assert "**Change:**" in output or "\\*\\*Change:\\*\\*" in output
    assert "\\change" not in output


def test_rationale_macro():
    r"""Test \rationale expansion (rationale description label)"""
    latex = r"\rationale This improves consistency with other facilities."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape asterisks in some contexts
    assert "**Rationale:**" in output or "\\*\\*Rationale:\\*\\*" in output
    assert "\\rationale" not in output


def test_effect_macro():
    r"""Test \effect expansion (effect on original feature label)"""
    latex = r"\effect The previous behavior is deprecated."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape asterisks in some contexts
    assert (
        "**Effect on original feature:**" in output
        or "\\*\\*Effect on original feature:\\*\\*" in output
    )
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
    # GFM escapes # as \# to prevent it from being interpreted as a heading
    assert "UAX \\#31" in output or "UAX #31" in output
    assert "\\UAX" not in output


def test_cvqual_macro():
    r"""Test \cvqual{} expansion (cv-qualifier metavariable)"""
    latex = r"Two types \cvqual{cv1} T1 and \cvqual{cv2} T2 are related."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # cvqual should output its argument in italics (rendered as *cv1*, *cv2* in markdown)
    assert "*cv1*" in output
    assert "*cv2*" in output
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


def test_cpp_macro_in_sentence():
    r"""Test \Cpp{} macro expands to 'C++' in a sentence"""
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
    r"""Test \notdef macro expands to 'not defined'"""
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
    # GFM escapes [ as \[ to prevent it from being interpreted as a link
    assert "[" in output or "\\[" in output
    assert "first" in output
    assert "last" in output
    assert ")" in output
    # Should NOT have unexpanded macro
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
    # GFM may insert line breaks for wrapping, so check components separately
    assert "*importable" in output
    assert "library headers*" in output
    assert "C++" in output

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


def test_discretionary_hyphen_in_tcode():
    """Test that discretionary hyphens (\\-) are removed from \tcode{} content"""
    latex = r"If \tcode{Forward\-Iter\-ator2} meets the requirements."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have single continuous code span, no doubled backticks
    assert "`ForwardIterator2`" in output
    # Should NOT have broken code spans
    assert "``" not in output
    assert "`Forward``Iter``ator2`" not in output


def test_libmember_in_tcode():
    """Test that \\libmember{}{} is converted correctly in \\tcode{} contexts

    Regression test for issue #46 - \\libmember{member}{class} macro not converted.
    The macro should extract the member name and discard the class name (used for indexing).
    """
    latex = r"The member is \tcode{\libmember{value_type}{expected}}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have extracted member name only
    assert "`value_type`" in output
    # Should NOT have raw macro or class name
    assert "\\libmember" not in output
    assert "expected" not in output


def test_libmember_multiple_in_tcode():
    """Test multiple \\libmember{}{} instances in same \\tcode{}"""
    latex = (
        r"\tcode{\libmember{ptr}{allocation_result}}, \tcode{\libmember{count}{allocation_result}}"
    )
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`ptr`" in output
    assert "`count`" in output
    assert "\\libmember" not in output
    assert "allocation_result" not in output


def test_libmember_in_table_tcode():
    """Test \\libmember{}{} in \\tcode{} within table context

    This is the actual pattern from C++ standard where issue #46 appears.
    """
    latex = r"Values: \tcode{\libmember{none}{file_type}}, \tcode{\libmember{regular}{file_type}}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have enum member names without macro
    assert "`none`" in output
    assert "`regular`" in output
    assert "\\libmember" not in output
    assert "file_type" not in output  # Class name should be discarded


def test_libglobal_in_tcode():
    """Test that \\libglobal{} is converted correctly in \\tcode{} contexts

    Related to issue #24 - \\libglobal{} macro not converted.
    """
    latex = r"The type is \tcode{\libglobal{file_type}}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have extracted type name
    assert "`file_type`" in output
    # Should NOT have raw macro
    assert "\\libglobal" not in output


def test_escaped_tilde_in_inline_code():
    r"""Test \~ (escaped tilde) converts to ~ in inline code (Issue #8)

    This tests inline code contexts like:
    - Grammar productions: '\~ type-name'
    - Table cells: `u.\~T()`
    - Prose text: `\~Q`
    """
    latex = r"""
In the grammar, we have '\tcode{\~}' type-name.
The destructor syntax is \tcode{u.\~T()}.
Lookup is performed as if \tcode{\~Q} appeared.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # All tildes should be converted
    assert "`~`" in output
    assert "`u.~T()`" in output
    assert "`~Q`" in output
    # No escaped tildes should remain
    assert "\\~" not in output


def test_land_operator_in_tcode():
    """Test \\land operator in \\tcode{} converts to ∧ (Issue #52)

    This tests inline math with logical operators inside \\tcode{} macros.
    The actual pattern from C++ standard templates.tex:
    \\tcode{C1<T> $\\land$ C2<T>}
    """
    latex = (
        r"The associated constraints of \tcode{f4} and \tcode{f5} are \tcode{C1<T> $\land$ C2<T>}."
    )
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have converted \land to ∧
    assert "`C1<T> ∧ C2<T>`" in output
    # Should NOT have raw LaTeX \land
    assert "\\land" not in output
    # Should NOT have $ delimiters
    assert "$" not in output


def test_lor_operator_in_tcode():
    """Test \\lor operator in \\tcode{} converts to ∨ (related to Issue #52)

    Tests that all logical operators are handled consistently.
    """
    latex = r"The constraint is \tcode{A<T> $\lor$ B<T>}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have converted \lor to ∨
    assert "`A<T> ∨ B<T>`" in output
    # Should NOT have raw LaTeX \lor
    assert "\\lor" not in output
    # Should NOT have $ delimiters
    assert "$" not in output


def test_nested_tcode_with_subscript_in_math():
    r"""Test nested \tcode{} with subscript: \tcode{decay_t<$\tcode{T}_i$>}

    From n4659/utilities.tex:14258 - inner \tcode{} should be stripped (not
    converted to nested backticks), and subscript should convert to Unicode.
    Expected: `decay_t<Tᵢ>` (single backticks, Unicode subscript)
    NOT: `` decay_t<`T`_i> `` (nested backticks, unconverted subscript)
    """
    latex = r"\tcode{decay_t<$\tcode{T}_i$>}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have single backticks with Unicode subscript
    assert "`decay_t<Tᵢ>`" in output
    # Should NOT have nested backticks
    assert "``" not in output
    assert "`T`" not in output  # Inner T should not have backticks
    # Should NOT have unconverted subscript
    assert "_i" not in output


def test_multiple_nested_tcode_in_math():
    r"""Test multiple nested \tcode{} with subscripts in single outer \tcode{}

    Pattern: \tcode{template<$\tcode{T}_i$, $\tcode{U}_j$>}
    Both inner subscripts should convert correctly without nested backticks.
    """
    latex = r"\tcode{template<$\tcode{T}_i$, $\tcode{U}_j$>}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have all subscripts converted to Unicode
    assert "`template<Tᵢ, Uⱼ>`" in output
    # Should NOT have nested backticks or double backticks
    assert "``" not in output
    # Should NOT have unconverted subscripts
    assert "_i" not in output and "_j" not in output


def test_nested_tcode_with_superscript():
    r"""Test nested \tcode{} with superscript: \tcode{X<$\tcode{T}^i$>}

    Superscripts should behave the same as subscripts - convert to Unicode
    without creating nested backticks.
    """
    latex = r"\tcode{X<$\tcode{T}^i$>}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have superscript converted to Unicode
    assert "`X<Tⁱ>`" in output
    # Should NOT have nested backticks
    assert "``" not in output
    # Should NOT have unconverted superscript
    assert "^i" not in output


# NOTE: $\tcode{T}_i$ (tcode inside math, in running text) is a different scenario
# from nested \tcode{} and requires handling in cpp-math.lua - out of scope for this fix


def test_textregistered():
    r"""Test \textregistered conversion to ® symbol (Issue #14)"""
    latex = r"Test POSIX\textregistered\ text."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "®" in output
    assert "textregistered" not in output


def test_exposconceptx():
    r"""Test \exposconceptx{}{} exposition-only concept conversion (Issue #68)"""
    latex = r"The type models \exposconceptx{boolean-testable}{boolean-testable}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have formatted concept name (italic code: *`text`*)
    assert "*`boolean-testable`*" in output
    # Should NOT have raw LaTeX command
    assert "exposconceptx" not in output


def test_bigoh_complexity():
    r"""Test \bigoh{} Big-O complexity notation conversion in paragraph contexts (Issue #38)"""
    latex = r"Member functions have complexity \bigoh{\tcode{size() * str.size()}} at worst."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have Mathematical Italic O (U+1D442) - same as cpp-common.lua
    assert "𝑂(" in output
    assert "`size() * str.size()`" in output or "size() * str.size()" in output
    # Should NOT have raw LaTeX commands
    assert "\\bigoh" not in output
    assert "\\tcode" not in output
    assert "\\texttt" not in output


def test_techterm_macro():
    r"""Test \techterm{} macro renders as italic (Issue #79)

    The \techterm{} macro was used in n3337-n4659 but is obsolete in newer versions.
    Without handling, it causes incomplete sentences like "known as the " with missing terms.
    """
    latex = r"""
Externally-supplied quantities known as the \techterm{parameters of the distribution}.
Four categories: \techterm{uniform random number generators}, \techterm{random number engines},
\techterm{random number engine adaptors}, and \techterm{random number distributions}.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have italic terms (may wrap across lines, so normalize whitespace)
    output_normalized = " ".join(output.split())
    assert "*parameters of the distribution*" in output_normalized
    assert "*uniform random number generators*" in output_normalized
    assert "*random number engines*" in output_normalized
    assert "*random number engine adaptors*" in output_normalized
    assert "*random number distributions*" in output_normalized
    # Should NOT have raw LaTeX command
    assert "\\techterm" not in output
    # Should NOT have incomplete "known as the " pattern
    assert "known as the ." not in output
    assert "known as the \n" not in output


def test_notes_realnotes_macros():
    r"""Test \notes and \realnotes macros render as italic labels (Issue #80)

    These macros were used in n3337-n4140 but caused incomplete comma-delimited lists
    when unhandled, leaving double commas like ", , Error conditions:".
    """
    latex = r"""
The \requires, \effects, \postconditions, \returns, \throws, \complexity, \notes, \errors, and \realnotes
specified for the function invocations.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have all spec labels in italic
    assert "*Requires:*" in output
    assert "*Effects:*" in output
    assert "*Postconditions:*" in output
    assert "*Returns:*" in output
    assert "*Throws:*" in output
    assert "*Complexity:*" in output
    assert "*Remarks:*" in output  # \notes -> Remarks:
    assert "*Error conditions:*" in output  # \errors
    assert "*Notes:*" in output  # \realnotes -> Notes:
    # Should NOT have raw LaTeX commands
    assert "\\notes" not in output
    assert "\\realnotes" not in output
    # Should NOT have incomplete ", , " pattern
    assert ", , " not in output


def test_libnoheader_macro():
    r"""Test \libnoheader{} macro renders as code with angle brackets (Issue #80)

    This macro is used in n4861+ to list reserved/absent header names.
    Without handling, it causes incomplete lists like "The header names , , , and".
    """
    latex = r"""
The header names \libnoheader{ccomplex}, \libnoheader{ciso646}, \libnoheader{cstdalign},
\libnoheader{cstdbool}, and \libnoheader{ctgmath} are reserved for previous standardization.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have all header names as inline code with angle brackets
    assert "`<ccomplex>`" in output
    assert "`<ciso646>`" in output
    assert "`<cstdalign>`" in output
    assert "`<cstdbool>`" in output
    assert "`<ctgmath>`" in output
    # Should NOT have raw LaTeX command
    assert "\\libnoheader" not in output
    # Should NOT have incomplete "header names , , " pattern
    assert "header names , ," not in output


def test_fakegrammarterm_macro():
    r"""Test \fakegrammarterm{} macro renders as italics (Issue #27/#17)

    This macro is used in intro.tex to explain grammar naming conventions.
    For example: \fakegrammarterm{X-name} is a use of an identifier...
    """
    latex = r"""
\fakegrammarterm{X-name} is a use of an identifier in a context that determines its meaning.
\fakegrammarterm{X-id} is an identifier with no context-dependent meaning.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have italicized placeholder names
    assert "*X-name*" in output
    assert "*X-id*" in output
    # Should NOT have raw LaTeX command
    assert "\\fakegrammarterm" not in output
    # Should NOT have the content stripped entirely
    assert "is a use of an identifier" in output
