"""Tests for cpp-itemdecl.lua filter"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-itemdecl.lua")
NOTES_FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-notes-examples.lua")


def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with itemdecl filter"""
    # Inject simplified_macros.tex preprocessing
    latex_with_macros = inject_macros(latex_content)

    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        "--wrap=none",  # Disable line wrapping for consistent test output
        f"--lua-filter={FILTER_PATH}",
    ]
    result = subprocess.run(
        cmd,
        input=latex_with_macros,
        capture_output=True,
        text=True,
    )
    return result.stdout, result.returncode


def run_pandoc_with_both_filters(latex_content):
    """Helper to run Pandoc with both itemdecl and notes-examples filters
    This matches production behavior where both filters run in sequence.
    Used for tests that check note/example formatting inside itemdescr blocks.
    """
    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        "--wrap=none",
        f"--lua-filter={FILTER_PATH}",
        f"--lua-filter={NOTES_FILTER_PATH}",
    ]
    result = subprocess.run(
        cmd,
        input=latex_content,
        capture_output=True,
        text=True,
    )
    return result.stdout, result.returncode


def test_mandates_label():
    r"""Test \mandates label conversion"""
    latex = r"""
\begin{itemdescr}
\mandates
The type \tcode{T} shall be copyable.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Mandates:*" in output
    assert "***Mandates:***" not in output  # Should be italic, not bold-italic
    assert "`T`" in output
    assert "copyable" in output


def test_effects_label():
    r"""Test \effects label conversion"""
    latex = r"""
\begin{itemdescr}
\effects
Increments the counter.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Effects:*" in output
    assert "***Effects:***" not in output  # Should be italic, not bold-italic
    assert "Increments" in output


def test_returns_label():
    r"""Test \returns label conversion"""
    latex = r"""
\begin{itemdescr}
\returns
\tcode{true} if successful.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Returns:*" in output
    assert "***Returns:***" not in output  # Should be italic, not bold-italic
    assert "`true`" in output


def test_complexity_label():
    r"""Test \complexity label conversion"""
    latex = r"""
\begin{itemdescr}
\complexity
Linear in \tcode{n}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Complexity:*" in output
    assert "***Complexity:***" not in output  # Should be italic, not bold-italic
    assert "`n`" in output


def test_constraints_rendering():
    r"""Test \constraints macro expansion"""
    latex = r"""
\begin{itemdescr}
\constraints
\tcode{is_move_constructible_v<T>} is \tcode{true} and
\tcode{is_move_assignable_v<T>} is \tcode{true}.

\effects
Moves the value.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Constraints:*" in output
    assert "***Constraints:***" not in output  # Should be italic, not bold-italic
    assert "`is_move_constructible_v<T>`" in output
    assert "`is_move_assignable_v<T>`" in output
    assert "*Effects:*" in output


def test_new_fundesc_labels():
    r"""Test newly added Fundesc labels: \recommended, \required, \default, \sync, \replaceable, \returntype, \ctype, \templalias, \implimits"""
    latex = r"""
\begin{itemdescr}
\recommended
Always validate input before processing.

\required
Implementation must throw an exception on invalid input.

\default
Returns an empty container.

\sync
Access to the same object from multiple threads must be synchronized.

\replaceable
This function may be replaced by user-defined versions.

\returntype
\tcode{std::size_t}

\ctype
\tcode{typename T::value_type}

\templalias
\tcode{using value_type = T;}

\implimits
Maximum recursion depth is 1024.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Recommended practice:*" in output
    assert "*Required behavior:*" in output
    assert "*Default behavior:*" in output
    assert "*Synchronization:*" in output
    assert "*Replaceable:*" in output
    assert "*Return type:*" in output
    assert "*Type:*" in output
    assert "*Alias template:*" in output
    assert "*Implementation limits:*" in output


def test_bigoh_expansion():
    r"""Test \bigoh{} macro expansion"""
    latex = r"""
\begin{itemdescr}
\complexity
\bigoh{\tcode{last - first}} applications.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Complexity:*" in output
    assert "***Complexity:***" not in output  # Should be italic, not bold-italic
    assert "𝑂(" in output
    assert "last - first" in output
    assert "applications" in output


def test_bigoh_with_log():
    r"""Test \bigoh{} with \log expansion"""
    latex = r"""
\begin{itemdescr}
\complexity
\bigoh{\log(\tcode{N})} comparisons.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "𝑂(log(" in output
    assert "N" in output
    assert "comparisons" in output


def test_tcode_conversion():
    r"""Test \tcode{} to \texttt{} conversion"""
    latex = r"""
\begin{itemdescr}
\returns
The value \tcode{x + y}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`x + y`" in output


def test_range_conversion():
    r"""Test \range{}{} conversion (half-open range)"""
    latex = r"""
\begin{itemdescr}
\returns
All elements in \range{first}{last}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "[`first`, `last`)" in output


def test_crange_conversion():
    r"""Test \crange{}{} conversion (closed range)"""
    latex = r"""
\begin{itemdescr}
\expects
In the range \crange{first}{last}, no modifications occur.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape brackets in GFM
    assert "`first`, `last`]" in output or "`first`, `last`\\]" in output
    assert "no modifications" in output


def test_countedrange_conversion():
    r"""Test \countedrange{}{} conversion (counted range)"""
    latex = r"""
\begin{itemdescr}
\expects
\countedrange{result}{n} does not overlap with \countedrange{first}{n}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape brackets in GFM
    assert "`result`+[0" in output or "`result`+\\[0" in output
    assert "`first`+[0" in output or "`first`+\\[0" in output
    assert "does not overlap" in output


def test_brange_conversion():
    r"""Test \brange{}{} conversion (both-exclusive range)"""
    latex = r"""
\begin{itemdescr}
\expects
\tcode{result} is not in the range \brange{first}{last}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "(`first`, `last`)" in output


def test_orange_conversion():
    r"""Test \orange{}{} conversion (open range - both exclusive, alias for brange)"""
    latex = r"""
\begin{itemdescr}
\expects
All iterators in the range \orange{position}{last} are dereferenceable.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "(`position`, `last`)" in output


def test_codeblock_environment():
    r"""Test \begin{codeblock} conversion to fenced code block"""
    latex = r"""
\begin{itemdescr}
\effects
Equivalent to:
\begin{codeblock}
if (x > 0)
  return x;
return 0;
\end{codeblock}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "```" in output or "``` cpp" in output
    assert "if (x > 0)" in output
    assert "return x" in output


def test_codeblock_with_macros():
    """Test codeblock with nested \tcode{} macros"""
    latex = r"""
\begin{itemdescr}
\effects
Equivalent to:
\begin{codeblock}
using U = \tcode{decay_t}<T>;
return U();
\end{codeblock}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "decay_t" in output
    assert "return U()" in output


def test_at_escape_delimiters():
    r"""Test @ escape delimiter handling in code"""
    latex = r"""
\begin{itemdescr}
\effects
Equivalent to:
\begin{codeblock}
return @\tcode{value}@;
\end{codeblock}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "return" in output
    assert "value" in output
    # @ delimiters should be removed from the code block
    assert output.count("@") == 0


def test_placeholdernc_in_code():
    r"""Test @\placeholdernc{} converts to plain text, not \textit"""
    latex = r"""
\begin{itemdescr}
\effects
Equivalent to:
\begin{codeblock}
::new (@\placeholdernc{voidify}@(*first))
    typename T::value_type();
\end{codeblock}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "voidify" in output
    # Should NOT contain LaTeX commands
    assert "\\textit{" not in output
    assert "\\texttt{" not in output


def test_note_environment():
    r"""Test \begin{note} processing in itemdescr"""
    latex = r"""
\begin{itemdescr}
\returns
The result value.
\begin{note}
This may throw an exception.
\end{note}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Note: When run standalone, notes become divs. Full filter chain processes them.
    assert "exception" in output
    # Could be either formatted note or HTML div
    assert "Note" in output or "note" in output


def test_example_environment():
    r"""Test \begin{example} processing in itemdescr"""
    latex = r"""
\begin{itemdescr}
\returns
The sum.
\begin{example}
\tcode{add(1, 2)} returns \tcode{3}.
\end{example}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Example: When run standalone, examples become divs. Full filter chain processes them.
    assert "`add(1, 2)`" in output
    assert "`3`" in output
    assert "Example" in output or "example" in output


def test_multiple_spec_labels():
    """Test multiple specification labels in sequence"""
    latex = r"""
\begin{itemdescr}
\mandates
Type \tcode{T} is copyable.

\effects
Copies the value.

\returns
The copied value.

\complexity
Constant time.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Mandates:*" in output
    assert "*Effects:*" in output
    assert "*Returns:*" in output
    assert "*Complexity:*" in output
    assert "***Mandates:***" not in output  # Should be italic, not bold-italic
    assert "***Effects:***" not in output
    assert "***Returns:***" not in output
    assert "***Complexity:***" not in output


def test_ref_preservation():
    r"""Test \ref{} cross-reference preservation"""
    latex = r"""
\begin{itemdescr}
\returns
As specified in \ref{intro.defs}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Pandoc may escape the brackets in GFM output
    assert "intro.defs" in output
    assert "[" in output or "\\[" in output


def test_iref_preservation():
    r"""Test \iref{} cross-reference preservation"""
    latex = r"""
\begin{itemdescr}
\returns
See \iref{basic.types}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "basic.types" in output
    assert "[" in output or "\\[" in output


def test_tref_preservation():
    r"""Test \tref{} table reference preservation"""
    latex = r"""
\begin{itemdescr}
\returns
As shown in \tref{tab.concepts}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "tab.concepts" in output
    assert "[" in output or "\\[" in output


def test_libconcept_conversion():
    r"""Test \libconcept{} conversion"""
    latex = r"""
\begin{itemdescr}
\mandates
The type satisfies \libconcept{copyable}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`copyable`" in output


def test_placeholder_conversion():
    r"""Test \placeholder{} conversion"""
    latex = r"""
\begin{itemdescr}
\returns
The value \placeholder{result}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*result*" in output


def test_oldconcept_conversion():
    r"""Test \oldconcept{} conversion"""
    latex = r"""
\begin{itemdescr}
\mandates
Meets the \oldconcept{CopyConstructible} requirements.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # \oldconcept{X} should expand to Cpp17X
    assert "*Cpp17CopyConstructible*" in output


def test_bigoh_unicode():
    r"""Test \bigoh{} uses Unicode Mathematical Italic O"""
    latex = r"""
\begin{itemdescr}
\complexity
\bigoh{N \log N} comparisons.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "𝑂(N log N)" in output
    assert "comparisons" in output


def test_nested_placeholdernc_in_tcode():
    r"""Test nested \tcode{\placeholdernc{}} becomes italic, not code"""
    latex = r"""
\begin{itemdescr}
\returns
Define \tcode{\placeholdernc{GENERALIZED_SUM}(op, a1, ..., aN)} as follows.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should be italic, not in backticks
    assert "*GENERALIZED_SUM*" in output
    # Should NOT have unparsed LaTeX commands
    assert "\\placeholdernc" not in output
    assert "\\tcode" not in output


def test_nested_tcode_in_placeholdernc_with_math():
    r"""Test complex nested pattern from utilities.tex: \tcode{\placeholdernc{FUN}($\tcode{T}_j$)}"""
    latex = r"""
\begin{itemdescr}
\returns
The overload \tcode{\placeholdernc{FUN}($\tcode{T}_j$)} selected by overload resolution.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Placeholder should be italic
    assert "*FUN*" in output
    # Math mode variable should be present (not wrapped in code)
    assert "T" in output and "j" in output
    # Should NOT have unparsed LaTeX commands
    assert "\\placeholdernc" not in output
    assert "\\tcode" not in output
    # Should NOT have malformed LaTeX like \texttt{T_j$)}
    assert "\\texttt" not in output
    assert "\\textit" not in output


def test_phantom_extraction():
    r"""Test \phantom{} content extraction"""
    latex = r"""
\begin{itemdescr}
\returns
\tcode{op(\phantom{op(}value)}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Content should be extracted
    assert "op(" in output
    assert "value" in output
    # \phantom command should be gone
    assert "\\phantom" not in output


def test_indexlibrary_stripped():
    r"""Test \indexlibrary{} is completely removed"""
    latex = r"""
\indexlibrary{test_name@\tcode{test}}%
\begin{itemdescr}
\returns
The result.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "result" in output
    # Index library markup should be completely gone
    assert "\\indexlibrary" not in output
    assert "test_name" not in output


def test_generalized_sum_definition():
    r"""Test full GENERALIZED_SUM definition rendering"""
    latex = r"""
\begin{itemdescr}
\returns
Define \tcode{\placeholdernc{GENERALIZED_SUM}(op, a1, ..., aN)} as
\tcode{\placeholdernc{GENERALIZED_NONCOMMUTATIVE_SUM}(op, b1, ..., bN)},
where \tcode{b1, ..., bN} may be any permutation.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Placeholders should be italic
    assert "*GENERALIZED_SUM*" in output
    assert "*GENERALIZED_NONCOMMUTATIVE_SUM*" in output
    # No unparsed LaTeX
    assert "\\placeholdernc" not in output


# ============================================================================
# Regression Tests for Recent Features (commit cbec0bf9)
# ============================================================================


def test_placeholder_conversion_in_itemdescr():
    """Test that @@REF:label@@ placeholders are converted to [[label]] in itemdescr"""
    latex = r"""
\begin{itemdescr}
\returns
As specified in \iref{intro.defs}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have double brackets for visible stable name
    assert "[[intro.defs]]" in output
    # Should NOT have placeholder
    assert "@@REF:" not in output


def test_placeholder_conversion_in_notes_inside_itemdescr():
    """Test placeholder conversion in notes within itemdescr"""
    latex = r"""
\begin{itemdescr}
\returns
Some value.
\begin{note}
See \iref{basic.types} for details.
\end{note}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Link should be converted
    assert "[[basic.types]]" in output
    # No placeholder should remain
    assert "@@REF:" not in output
    # Note may appear as Div block or formatted note
    assert "note" in output.lower() or "[[basic.types]]" in output


def test_placeholder_conversion_in_examples_inside_itemdescr():
    """Test placeholder conversion in examples within itemdescr"""
    latex = r"""
\begin{itemdescr}
\returns
A result.
\begin{example}
For usage, see \iref{expr.call}.
\end{example}
\end{itemdescr}
"""
    output, code = run_pandoc_with_both_filters(latex)
    assert code == 0
    # Link should be converted
    assert "[[expr.call]]" in output
    # No placeholder
    assert "@@REF:" not in output
    # Should be in example formatting
    assert "*Example" in output


def test_multiple_placeholders_in_same_line():
    """Test multiple cross-references in same line"""
    latex = r"""
\begin{itemdescr}
\returns
See \iref{basic.def}, \iref{basic.types}, and \tref{tab.concepts}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # All three should be converted
    assert "[[basic.def]]" in output
    assert "[[basic.types]]" in output
    assert "[[tab.concepts]]" in output
    assert "@@REF:" not in output


def test_nested_brace_extraction_in_indexlibrary():
    """Test that nested braces in \\indexlibrary{} are handled correctly"""
    # This is a regression test for commit cbec0bf9
    # Previously, \\indexlibrary{\\idxcode{terminate}} would break
    latex = r"""
\begin{itemdescr}
\effects
The function shall be called.\indexlibrary{\idxcode{terminate}}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should not crash, and indexlibrary should be stripped
    assert "\\indexlibrary" not in output
    assert "\\idxcode" not in output
    assert "shall be called" in output


def test_div_block_note_handling():
    """Test that Pandoc-generated Div blocks for notes are handled"""
    # When Pandoc parses \begin{note} after itemdescr macro expansion,
    # it creates Div blocks which need special handling
    latex = r"""
\begin{itemdescr}
\expects
Some condition.
\begin{note}
This refers to \iref{library.c} for clarification.
\end{note}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Link should be converted even though it's in a Div block
    assert "[[library.c]]" in output
    assert "@@REF:" not in output


def test_cross_reference_types_all_converted():
    """Test that \\ref, \\iref, and \\tref are all converted"""
    latex = r"""
\begin{itemdescr}
\returns
See \ref{intro.scope}, \iref{expr.prim}, and \tref{tab.names}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # All reference types should be converted
    assert "[[intro.scope]]" in output
    assert "[[expr.prim]]" in output
    assert "[[tab.names]]" in output


def test_placeholder_in_complex_note_with_code():
    """Test placeholder conversion in notes containing code blocks"""
    latex = r"""
\begin{itemdescr}
\returns
A value.
\begin{note}
Example from \iref{basic.fundamental}:
\begin{codeblock}
int x = 42;
\end{codeblock}
\end{note}
\end{itemdescr}
"""
    output, code = run_pandoc_with_both_filters(latex)
    assert code == 0
    # Link should be converted
    assert "[[basic.fundamental]]" in output
    # Code block should be present as fenced block
    assert "int x = 42" in output
    assert "```" in output


def test_placeholder_conversion_in_bulletlist():
    """Test that @@REF: placeholders are converted in BulletList items

    This is a regression test for the issue where placeholders in bulleted lists
    within itemdescr blocks were not being converted to [[label]] syntax.
    The bug was that only Para blocks were processed, not BulletList blocks.
    """
    latex = r"""
\begin{itemdescr}
\returns
An unspecified value such that
\begin{itemize}
\item \tcode{x.owner_before(y)} defines a strict weak ordering as defined in~\ref{alg.sorting};
\item under the equivalence relation defined by \tcode{owner_before}, two instances are equivalent.
\end{itemize}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # The cross-reference should be converted to [[label]] syntax
    assert "[[alg.sorting]]" in output
    # Should NOT have unconverted @@REF: placeholders
    assert "@@REF:" not in output
    # Check that it's in a list context
    assert "- " in output or "* " in output  # Bullet list marker
    assert "owner_before" in output


def test_placeholder_conversion_in_orderedlist():
    """Test that @@REF: placeholders are converted in OrderedList items"""
    latex = r"""
\begin{itemdescr}
\returns
A value satisfying:
\begin{enumerate}
\item The first requirement from \iref{basic.types};
\item The second requirement from \ref{expr.eq}.
\end{enumerate}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Both cross-references should be converted
    assert "[[basic.types]]" in output
    assert "[[expr.eq]]" in output
    # Should NOT have unconverted @@REF: placeholders
    assert "@@REF:" not in output
    # Check that it's an ordered list
    assert "1." in output or "1)" in output  # Ordered list marker


def test_placeholder_spacing_for_readability():
    r"""Test that spaces are added before [[ for readability when missing

    In LaTeX, \iref{} is inline and doesn't require a space, but in Markdown
    we add a space before [[ for better readability (e.g., 'type[[label]]' -> 'type [[label]]')
    """
    latex = r"""
\begin{itemdescr}
\returns
A type\iref{basic.types} that satisfies\ref{cpp17.defaultconstructible}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Spaces should be added for readability
    assert "type [[basic.types]]" in output
    assert "satisfies [[cpp17.defaultconstructible]]" in output
    # Should NOT have references without space (harder to read)
    assert "type[[" not in output
    assert "satisfies[[" not in output


def test_placeholder_spacing_preserves_existing_spaces():
    """Test that existing spaces before references are preserved"""
    latex = r"""
\begin{itemdescr}
\returns
As specified in~\ref{alg.sorting} and described in \iref{basic.types}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # ~ becomes non-breaking space (\xa0), and we add regular space
    # So we check for " [[" (space before bracket)
    assert " [[alg.sorting]]" in output
    # Space should be added for \iref
    assert " [[basic.types]]" in output
    # Should not have references directly attached to words
    assert "in[[" not in output
    assert "described[[" not in output


def test_empty_cross_reference():
    """Test handling of empty cross-reference (edge case)"""
    latex = r"""
\begin{itemdescr}
\returns
Invalid reference: \iref{}.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should not crash, but behavior depends on implementation
    # At minimum, no unparsed LaTeX should remain
    assert "\\iref" not in output


def test_code_block_in_bullet_list():
    r"""Test that code blocks inside bullet lists are upgraded to fenced format"""
    latex = r"""
\begin{itemdescr}
\returns
A value where:
\begin{itemize}
\item First condition holds.
\item Second condition demonstrated by:
\begin{codeblock}
int x = 42;
return x;
\end{codeblock}
\end{itemize}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "```" in output  # Should be fenced
    assert "cpp" in output or "```cpp" in output  # Should have cpp language
    assert "int x = 42" in output
    assert "return x" in output
    # List markers (either - or *)
    assert "- " in output or "* " in output


def test_code_block_in_ordered_list():
    r"""Test that code blocks inside ordered lists are upgraded to fenced format"""
    latex = r"""
\begin{itemdescr}
\effects
Performs the following steps:
\begin{enumerate}
\item Initialize the value.
\item Execute:
\begin{codeblock}
value = compute();
\end{codeblock}
\item Return the result.
\end{enumerate}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "```" in output  # Should be fenced
    assert "cpp" in output or "```cpp" in output  # Should have cpp language
    assert "value = compute()" in output
    # Ordered list markers
    assert "1." in output or "1)" in output


def test_deep_nesting_note_list_code():
    r"""Test 3-level nesting: itemdescr → note → list → code

    This regression test verifies that recursive upgrade_code_blocks()
    correctly handles deep nesting scenarios.
    """
    latex = r"""
\begin{itemdescr}
\returns
The result.
\begin{note}
Consider these cases:
\begin{itemize}
\item Case 1 with code:
\begin{codeblock}
foo();
\end{codeblock}
\item Case 2 with code:
\begin{codeblock}
bar();
\end{codeblock}
\end{itemize}
\end{note}
\end{itemdescr}
"""
    output, code = run_pandoc_with_both_filters(latex)
    assert code == 0
    assert "```" in output  # Should be fenced
    assert "cpp" in output or "```cpp" in output  # Should have cpp language
    assert "foo()" in output
    assert "bar()" in output
    assert "*Note" in output  # Note formatting from cpp-notes-examples


def test_multiple_code_blocks_in_note():
    r"""Test that multiple code blocks in a note are all upgraded to fenced format"""
    latex = r"""
\begin{itemdescr}
\returns
A value.
\begin{note}
First example:
\begin{codeblock}
int x = 1;
\end{codeblock}
Second example:
\begin{codeblock}
int y = 2;
\end{codeblock}
\end{note}
\end{itemdescr}
"""
    output, code = run_pandoc_with_both_filters(latex)
    assert code == 0
    # At least 4 backticks (2 code blocks × 2 fences each)
    assert output.count("```") >= 4
    assert "int x = 1" in output
    assert "int y = 2" in output


def test_empty_code_block():
    r"""Test that empty code blocks don't crash (edge case)"""
    latex = r"""
\begin{itemdescr}
\effects
Equivalent to:
\begin{codeblock}
\end{codeblock}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should not crash, exact output may vary but should be valid


def test_nested_keyword_in_tcode_itemdescr():
    r"""Test that \keyword{} inside \tcode{} doesn't create nested backticks

    Issue: When simplified_macros.tex converts \keyword{const} to \texttt{const},
    and then \tcode{\texttt{const_cast}<X \texttt{const}\&>} is processed by
    cpp-itemdecl.lua, we were getting nested \texttt{\texttt{...}} which pandoc.read()
    converted to nested backticks like `const_cast``<X ``const``&>`.

    Fix: Strip \texttt{} from inside \tcode{} before converting to \texttt{}.
    """
    latex = r"""
\begin{itemdescr}
\returns
\tcode{\keyword{const_cast}<X \keyword{const}\&>(a).rbegin()}
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have proper inline code without nested backticks
    assert "`const_cast<X const&>(a).rbegin()`" in output

    # Should NOT have nested backticks
    assert "``" not in output

    # Should have the Returns label
    assert "*Returns:*" in output


def test_bigoh_with_nested_braces():
    r"""Test \bigoh{} macro with nested \text{} braces (regression test for trunk)"""
    latex = r"""
\begin{itemdescr}
\complexity
\bigoh{$\text{size of state}$} operations.
\end{itemdescr}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0, f"Pandoc failed with code {code}"

    # Should preserve math delimiters and nested content
    assert "𝑂($" in output or "𝑂(\\$" in output  # Math delimiter
    assert "size of state" in output
    assert "operations" in output

    # Should not have malformed delimiters
    assert ")$}" not in output  # This would indicate the bug
