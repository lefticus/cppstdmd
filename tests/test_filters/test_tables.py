"""Tests for table handling in cpp-tables.lua filter"""
import subprocess
from pathlib import Path
import sys
import re

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-tables.lua")

def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with tables filter"""
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

def normalize_table_whitespace(text):
    """Normalize whitespace in table rows for comparison.

    Collapses multiple spaces between | characters to single spaces,
    allowing tests to check table content regardless of column padding.
    """
    lines = text.split('\n')
    normalized_lines = []
    for line in lines:
        if line.strip().startswith('|'):
            # Split by |, strip each cell, rejoin with single spaces
            cells = line.split('|')
            normalized_cells = [cell.strip() for cell in cells]
            normalized_line = '| ' + ' | '.join(normalized_cells[1:-1]) + ' |'
            normalized_lines.append(normalized_line)
        else:
            normalized_lines.append(line)
    return '\n'.join(normalized_lines)

def test_simple_floattable():
    r"""Test basic floattable conversion"""
    latex = r"""
\begin{floattable}{Test Table}{test.label}
{ll}
\topline
\lhdr{Column 1} & \rhdr{Column 2} \\ \rowsep
\tcode{value1} & \tcode{value2} \\
\tcode{value3} & \tcode{value4} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    normalized = normalize_table_whitespace(output)
    assert "**Table: Test Table**" in output
    assert "| Column 1 | Column 2 |" in normalized
    assert "| `value1` | `value2` |" in normalized
    assert "| `value3` | `value4` |" in normalized

def test_floattable_with_xname():
    r"""Test floattable with \xname{} macro in caption"""
    latex = r"""
\begin{floattable}{\xname{has_cpp_attribute} values}{cpp.cond.ha}
{ll}
\topline
\lhdr{Attribute} & \rhdr{Value} \\ \rowsep
\tcode{assume} & \tcode{202207L} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    assert "**Table: __has_cpp_attribute values**" in output
    assert "| Attribute | Value |" in normalized
    assert "| `assume` | `202207L` |" in normalized

def test_longtable_basic():
    r"""Test basic LongTable conversion with \defnxname macros

    \defnxname uses \xname which produces __name (prefix only, no trailing underscores).
    In tables, this should be wrapped in backticks to render as code, not markdown bold.
    """
    latex = r"""
\begin{LongTable}{Feature-test macros}{cpp.predefined.ft}{ll}
\\ \topline
\lhdr{Macro name} & \rhdr{Value} \\ \capsep
\endfirsthead
\continuedcaption \\
\hline
\lhdr{Name} & \rhdr{Value} \\ \capsep
\endhead
\defnxname{cpp_concepts} & \tcode{202002L} \\ \rowsep
\defnxname{cpp_constexpr} & \tcode{202211L} \\ \rowsep
\end{LongTable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    assert "**Table: Feature-test macros**" in output
    assert "| Macro name | Value |" in normalized
    # \defnxname should produce `__name` (with backticks, no trailing underscores)
    assert "| `__cpp_concepts` | `202002L` |" in normalized
    assert "| `__cpp_constexpr` | `202211L` |" in normalized
    # Should NOT have markdown bold formatting (which would happen without backticks)
    assert "| __cpp_concepts__ |" not in output
    assert "| __cpp_constexpr__ |" not in output

def test_floattable_multiple_rows():
    r"""Test floattable with multiple rows"""
    latex = r"""
\begin{floattable}{Attributes}{attr.label}
{ll}
\topline
\lhdr{Attribute} & \rhdr{Value} \\ \rowsep
\tcode{deprecated} & \tcode{201309L} \\
\tcode{fallthrough} & \tcode{201603L} \\
\tcode{likely} & \tcode{201803L} \\
\tcode{unlikely} & \tcode{201803L} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Check that all rows are present
    assert output.count("| `") == 8  # 4 rows * 2 cells per row

def test_longtable_defnxname():
    r"""Test that \defnxname is correctly expanded

    \defnxname uses \xname which produces __name (prefix only, no trailing underscores).
    In tables, this should be wrapped in backticks to render as code, not markdown bold.
    """
    latex = r"""
\begin{LongTable}{Test Macros}{test.label}{ll}
\\ \topline
\lhdr{Name} & \rhdr{Value} \\ \capsep
\endfirsthead
\endhead
\defnxname{cpp_test_macro} & \tcode{202000L} \\ \rowsep
\end{LongTable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # \defnxname should produce `__name` (with backticks, no trailing underscores)
    assert "`__cpp_test_macro`" in output
    assert "`202000L`" in output
    # Should NOT have markdown bold formatting or trailing underscores
    assert "__cpp_test_macro__" not in output

def test_floattable_caption_with_nested_braces():
    r"""Test caption with nested braces is correctly extracted"""
    latex = r"""
\begin{floattable}{\xname{has_cpp_attribute} values}{label}
{ll}
\topline
\lhdr{Attr} & \rhdr{Val} \\ \rowsep
\tcode{x} & \tcode{y} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # \xname should be expanded to __has_cpp_attribute
    assert "__has_cpp_attribute" in output

def test_table_separator_row():
    r"""Test that separator row is correctly generated"""
    latex = r"""
\begin{floattable}{Test}{label}
{ll}
\topline
\lhdr{A} & \rhdr{B} \\ \rowsep
\tcode{1} & \tcode{2} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have separator row with dashes
    assert re.search(r'\| -+ \| -+ \|', normalized)

def test_libsumtab_with_refs():
    r"""Test libsumtab with \ref{} macros in cells - should track references"""
    latex = r"""
\begin{libsumtab}{Language support library summary}{support.summary}
\ref{support.arith.types} & Arithmetic types & \tcode{<cstdint>}, \tcode{<stdfloat>} \\ \rowsep
\iref{support.dynamic} & Dynamic memory management & \tcode{<new>} \\ \rowsep
\tref{support.exception} & Exception handling & \tcode{<exception>} \\
\end{libsumtab}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # \ref{}, \iref{}, and \tref{} should be converted to [x]
    assert "[[support.arith.types]]" in output
    assert "[[support.dynamic]]" in output
    assert "[[support.exception]]" in output
    # LaTeX commands should not appear
    assert "\\ref{" not in output
    assert "\\iref{" not in output
    assert "\\tref{" not in output
    # IMPORTANT: Should have link definitions for all three references (single brackets in definition)
    assert "[support.arith.types]: #support.arith.types" in output
    assert "[support.dynamic]: #support.dynamic" in output
    assert "[support.exception]: #support.exception" in output

def test_libsumtab_multiline_rows():
    r"""Test libsumtab with multi-line rows - rows spanning multiple lines should be parsed correctly"""
    latex = r"""
\begin{libsumtab}{Test Table}{test.label}
\ref{support.types}       & Common definitions        &
  \tcode{<cstddef>}, \tcode{<cstdlib>}   \\ \rowsep
\ref{support.limits}      & Implementation properties &
  \tcode{<cfloat>}, \tcode{<climits>}    \\ \rowsep
\ref{support.arith.types} & Arithmetic types          &   \tcode{<cstdint>}, \tcode{<stdfloat>}  \\
\end{libsumtab}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # All three rows should have all three cells
    assert "[[support.types]] | Common definitions | `<cstddef>`, `<cstdlib>`" in normalized
    assert "[[support.limits]] | Implementation properties | `<cfloat>`, `<climits>`" in normalized
    assert "[[support.arith.types]] | Arithmetic types | `<cstdint>`, `<stdfloat>`" in normalized
    # All references should have link definitions (single brackets in definition)
    assert "[support.types]: #support.types" in output
    assert "[support.limits]: #support.limits" in output
    assert "[support.arith.types]: #support.arith.types" in output

def test_floattable_with_keyword():
    r"""Test floattable with \keyword{} macros - should strip keyword markup"""
    latex = r"""
\begin{floattable}{Minimum width}{basic.fundamental.width}{ll}
\topline
\lhdr{Type} & \rhdr{Minimum width $N$} \\
\capsep
\tcode{\keyword{signed} \keyword{char}} & 8 \\
\tcode{\keyword{short} \keyword{int}} & 16 \\
\keyword{int} & 16 \\
\tcode{\keyword{long} \keyword{int}} & 32 \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # All rows should be present (including first row with signed char)
    assert "`signed char`" in output
    assert "`short int`" in output
    assert "| int |" in normalized  # Plain keyword without \tcode
    assert "`long int`" in output
    # Should NOT have LaTeX commands leaking
    assert "\\keyword" not in output
    assert "\\texttt" not in output
    # Should have 4 data rows - only 3 have backticks (int row has none)
    assert output.count("| `") >= 3  # At least 3 cells with backticks

def test_floattable_with_hline():
    r"""Test floattable with \\ \hline - should strip \hline from cells"""
    latex = r"""
\begin{floattable}{Test Table}{test.label}{ll}
\topline
\lhdr{Column 1} & \rhdr{Column 2} \\ \rowsep
\tcode{value1} & \tcode{value2} \\ \hline
\tcode{value3} & \tcode{value4} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    assert "| `value1` | `value2` |" in normalized
    assert "| `value3` | `value4` |" in normalized
    # Should NOT have LaTeX commands leaking
    assert "\\hline" not in output
    assert "\\\\" not in output

def test_floattable_with_cline():
    r"""Test floattable with \\ \cline{...} - should strip \cline from cells"""
    latex = r"""
\begin{floattable}{Test Table}{test.label}{lll}
\topline
\lhdr{A} & \rhdr{B} & \rhdr{C} \\ \rowsep
\tcode{a1} & \tcode{b1} & \tcode{c1} \\ \cline{2-3}
\tcode{a2} & \tcode{b2} & \tcode{c2} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    assert "| `a1` | `b1` | `c1` |" in normalized
    assert "| `a2` | `b2` | `c2` |" in normalized
    # Should NOT have LaTeX commands leaking
    assert "\\cline" not in output
    assert "\\\\" not in output

def test_libsumtab_with_hline():
    r"""Test libsumtab with \\ \hline - should strip \hline from cells"""
    latex = r"""
\begin{libsumtab}{Test Library Summary}{test.summary}
\ref{test.sub1} & Description 1 & \tcode{<header1>} \\ \hline
\ref{test.sub2} & Description 2 & \tcode{<header2>} \\
\end{libsumtab}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    assert "[test.sub1]" in output
    assert "[test.sub2]" in output
    assert "Description 1" in output
    assert "Description 2" in output
    # Should NOT have LaTeX commands leaking
    assert "\\hline" not in output
    assert "\\\\" not in output

def test_libsumtab_with_rowsep_no_newline():
    r"""Test libsumtab with \\ \rowsep where next line starts immediately (real-world pattern)"""
    latex = r"""
\begin{libsumtab}{Containers library summary}{containers.summary}
\ref{container.requirements} & Requirements & \\ \rowsep
\ref{sequences} & Sequence containers &
  \tcode{<array>}, \tcode{<deque>} \\ \rowsep
\ref{associative} & Associative containers & \tcode{<map>} \\
\end{libsumtab}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # All three rows should be present
    assert "[container.requirements]" in output
    assert "[sequences]" in output
    assert "[associative]" in output
    # Should handle multiline cells (second row spans multiple lines in LaTeX)
    assert "`<array>`, `<deque>`" in output or "`<array>`,`<deque>`" in output
    # Should NOT have LaTeX commands leaking
    assert "\\rowsep" not in output
    assert "\\\\" not in output

def test_floattable_no_headers():
    r"""Test floattable with no \lhdr/\rhdr headers (should generate dummy headers)"""
    latex = r"""
\begin{floattable}{Container types with compatible nodes}{container.node.compat}
{ll}
\topline
\tcode{map<K, T, C1, A>} & \tcode{map<K, T, C2, A>} \\
\rowsep
\tcode{map<K, T, C1, A>} & \tcode{multimap<K, T, C2, A>} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have both data rows
    assert "`map<K, T, C1, A>`" in output
    assert "`map<K, T, C2, A>`" in output
    assert "`multimap<K, T, C2, A>`" in output
    # Should have separator row (---) for valid markdown
    assert re.search(r'\| -+ \| -+ \|', normalized)
    # Should NOT have LaTeX commands
    assert "\\rowsep" not in output
    assert "\\topline" not in output

def test_floattable_with_hdstyle_headers():
    r"""Test floattable with \hdstyle{...} headers (alternate header format)"""
    latex = r"""
\begin{floattable}{Library categories}{library.categories}
{ll}
\topline
\hdstyle{Clause} & \hdstyle{Category} \\ \capsep
\ref{support} & Language support library \\
\ref{diagnostics} & Diagnostics library \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should extract headers from \hdstyle{...} format
    assert "| Clause | Category |" in normalized
    # Should have data rows
    assert "[[support]]" in output
    assert "[[diagnostics]]" in output
    assert "Language support library" in output
    assert "Diagnostics library" in output
    # Should NOT have LaTeX commands
    assert "\\hdstyle" not in output
    assert "\\capsep" not in output

def test_floattable_trailing_blank_line():
    r"""Test that tables have trailing blank lines to separate from following content"""
    latex = r"""
\begin{floattable}{Test Table}{test.label}
{ll}
\topline
\lhdr{Col1} & \rhdr{Col2} \\ \rowsep
\tcode{a} & \tcode{b} \\
\end{floattable}
This is text after the table.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Table should have trailing blank line (double newline at end)
    # The output should have the table ending, then blank line, then "This is text"
    # Check that the table ends with a newline and "This is text" is NOT on the same line
    lines = output.split('\n')
    # Find the last table row
    last_table_line_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and '`b`' in line:
            last_table_line_idx = i
            break

    assert last_table_line_idx is not None, "Could not find last table row"
    # Check that there's at least one blank line before "This is text"
    found_blank = False
    for i in range(last_table_line_idx + 1, len(lines)):
        if lines[i].strip() == '':
            found_blank = True
        elif 'This is text' in lines[i]:
            assert found_blank, "No blank line between table and following text"
            break

def test_floattable_with_uname():
    r"""Test floattable with \uname{} for Unicode character names"""
    latex = r"""
\begin{floattable}{Unicode characters}{unicode.chars}
{lll}
\topline
\lhdr{Code} & \rhdr{Name} & \rhdr{Symbol} \\ \rowsep
\tcode{U+0009} & \uname{character tabulation} & \tcode{\\t} \\
\tcode{U+0020} & \uname{space} & \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # \uname should be stripped, leaving plain text
    assert "character tabulation" in output
    assert "space" in output
    # Should NOT have LaTeX commands
    assert "\\uname" not in output

def test_floattable_with_unicode_macro():
    r"""Test floattable with \unicode{}{} macro for code point + description"""
    latex = r"""
\begin{floattable}{Test Table}{test.unicode}
{ll}
\topline
\lhdr{Character} & \rhdr{Description} \\ \rowsep
\tcode{x} & Uses \unicode{007d}{right curly bracket} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # \unicode{XXXX}{desc} should become U+XXXX (desc)
    assert "U+007d" in output or "U+007D" in output
    assert "right curly bracket" in output
    # Should NOT have LaTeX commands
    assert "\\unicode" not in output

def test_floattable_with_textbf():
    r"""Test floattable with \textbf{} for bold text"""
    latex = r"""
\begin{floattable}{Iterator categories}{iterator.categories}
{ll}
\topline
\textbf{Category} & \textbf{Requirements} \\ \rowsep
Input & Readable \\
Output & Writable \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # \textbf should become markdown bold
    assert "**Category**" in output
    assert "**Requirements**" in output
    # Should NOT have LaTeX commands
    assert "\\textbf" not in output

def test_floattable_with_libglobal():
    r"""Test floattable with \libglobal{} for library globals"""
    latex = r"""
\begin{floattable}{Type traits}{type.traits}
{ll}
\topline
\lhdr{Trait} & \rhdr{Description} \\ \rowsep
\libglobal{is_integral} & Checks if integral \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # \libglobal should become backticked code
    assert "`is_integral`" in output
    # Should NOT have LaTeX commands
    assert "\\libglobal" not in output

def test_floattable_with_escaped_special_chars():
    r"""Test floattable with escaped special characters in \texttt{}"""
    latex = r"""
\begin{floattable}{Special characters}{special.chars}
{ll}
\topline
\lhdr{Code} & \rhdr{Character} \\ \rowsep
\tcode{U+007b} & \texttt{\{} \\
\tcode{U+007d} & \texttt{\}} \\
\tcode{U+007e} & \texttt{\textasciitilde} \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Escaped special chars should be rendered correctly
    assert "`{`" in output
    assert "`}`" in output
    assert "`~`" in output
    # Should NOT have LaTeX commands
    assert "\\texttt{\\{" not in output
    assert "\\textasciitilde" not in output

def test_floattable_with_special_char_macros():
    r"""Test floattable with \caret and \unun macros"""
    latex = r"""
\begin{floattable}{Operators}{operators.table}
{ll}
\topline
\lhdr{Symbol} & \rhdr{Name} \\ \rowsep
\caret & XOR \\
\unun & Reserved prefix \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Macros should expand to actual characters
    assert "^" in output
    assert "__" in output
    # Should NOT have LaTeX commands
    assert "\\caret" not in output
    assert "\\unun" not in output

def test_oldconcepttable_basic():
    r"""Test basic oldconcepttable conversion (Cpp17* requirements)"""
    latex = r"""
\begin{oldconcepttable}{EqualityComparable}{}{cpp17.equalitycomparable}
{x{1in}x{1in}p{3in}}
\topline
\hdstyle{Expression} & \hdstyle{Return type} & \hdstyle{Requirement} \\ \capsep
\tcode{a == b} &
\tcode{decltype(a == b)} &
\tcode{==} is an equivalence relation \\
\end{oldconcepttable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Caption should be "Cpp17{NAME} requirements{EXTRA}"
    assert "**Table: Cpp17EqualityComparable requirements**" in output
    # Should have headers
    assert "| Expression | Return type | Requirement |" in normalized
    # Should have data row
    assert "| `a == b` |" in normalized
    assert "| `decltype(a == b)` |" in normalized or "`decltype(a == b)`" in output
    assert "`==` is an equivalence relation" in output
    # Should NOT have LaTeX commands
    assert "\\hdstyle" not in output
    assert "\\capsep" not in output
    assert "\\oldconcepttable" not in output

def test_oldconcepttable_with_extra():
    r"""Test oldconcepttable with extra text in caption"""
    latex = r"""
\begin{oldconcepttable}{CopyConstructible}{ (in addition to MoveConstructible)}{cpp17.copyconstructible}
{p{1in}p{4.15in}}
\topline
\hdstyle{Expression} & \hdstyle{Post-condition} \\ \capsep
\tcode{T u = v;} & the value of \tcode{v} is unchanged \\ \rowsep
\tcode{T(v)} &
  the value of \tcode{v} is unchanged \\
\end{oldconcepttable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Caption should include EXTRA text
    assert "**Table: Cpp17CopyConstructible requirements (in addition to MoveConstructible)**" in output
    # Should have headers
    assert "| Expression | Post-condition |" in normalized
    # Should have data rows
    assert "| `T u = v;` |" in normalized
    assert "| `T(v)` |" in normalized
    # Should NOT have LaTeX commands
    assert "\\rowsep" not in output

def test_oldconcepttable_multiple_columns():
    r"""Test oldconcepttable with 4 columns"""
    latex = r"""
\begin{oldconcepttable}{MoveAssignable}{}{cpp17.moveassignable}
{p{1in}p{1in}p{1in}p{1.9in}}
\topline
\hdstyle{Expression} & \hdstyle{Return type} & \hdstyle{Return value} & \hdstyle{Post-condition} \\ \capsep
\tcode{t = rv} & \tcode{T\&} & \tcode{t} &
  \tcode{t} is equivalent to the value of \tcode{rv} \\
\end{oldconcepttable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have 4 headers
    assert "| Expression | Return type | Return value | Post-condition |" in normalized
    # Should have 4-column separator
    assert re.search(r'\| -+ \| -+ \| -+ \| -+ \|', normalized)
    # Should have all 4 cells in data row
    assert "| `t = rv` | `T&` | `t` |" in normalized
    # Caption should be Cpp17MoveAssignable
    assert "**Table: Cpp17MoveAssignable requirements**" in output

def test_concepttable_basic():
    r"""Test basic concepttable conversion (C++20 concepts)"""
    latex = r"""
\begin{concepttable}{BasicFormatter requirements}{formatter.basic}
{p{1.2in}p{1in}p{2.9in}}
\topline
\hdstyle{Expression} & \hdstyle{Return type} & \hdstyle{Requirement} \\ \capsep
\tcode{g.parse(pc)} &
\tcode{PC::iterator} &
Parses format-spec for type \tcode{T} \\
\end{concepttable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Caption should be used as-is (not modified like oldconcepttable)
    assert "**Table: BasicFormatter requirements**" in output
    # Should have headers
    assert "| Expression | Return type | Requirement |" in normalized
    # Should have data row
    assert "| `g.parse(pc)` |" in normalized
    assert "| `PC::iterator` |" in normalized or "`PC::iterator`" in output
    # Should NOT have LaTeX commands
    assert "\\hdstyle" not in output
    assert "\\capsep" not in output

def test_simpletypetable_basic():
    r"""Test basic simpletypetable conversion"""
    latex = r"""
\begin{simpletypetable}
{Base of integer-literals}
{lex.icon.base}
{lr}
\topline
\lhdr{Kind of integer-literal} & \rhdr{base $N$} \\ \capsep
binary-literal & 2 \\
octal-literal & 8 \\
decimal-literal & 10 \\
hexadecimal-literal & 16 \\
\end{simpletypetable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Caption should be used as-is
    assert "**Table: Base of integer-literals**" in output
    # Should have headers (using \lhdr and \rhdr)
    assert "| Kind of integer-literal | base $N$ |" in normalized or "base" in output
    # Should have data rows
    assert "| binary-literal | 2 |" in normalized
    assert "| octal-literal | 8 |" in normalized
    assert "| decimal-literal | 10 |" in normalized
    assert "| hexadecimal-literal | 16 |" in normalized
    # Should NOT have LaTeX commands
    assert "\\lhdr" not in output
    assert "\\rhdr" not in output
    assert "\\simpletypetable" not in output

def test_simpletypetable_with_code():
    r"""Test simpletypetable with \tcode{} and \keyword{} macros"""
    latex = r"""
\begin{simpletypetable}
{Types of floating-point-literals}
{lex.fcon.type}
{ll}
\topline
\lhdr{floating-point-suffix} & \rhdr{type} \\ \capsep
none & \keyword{double} \\
\tcode{f} or \tcode{F} & \keyword{float} \\
\tcode{l} or \tcode{L} & \keyword{long} \keyword{double} \\
\end{simpletypetable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: Types of floating-point-literals**" in output
    # Should strip \keyword markup
    assert "| none | double |" in normalized
    assert "| `f` or `F` | float |" in normalized
    assert "| `l` or `L` | long double |" in normalized
    # Should NOT have LaTeX commands
    assert "\\keyword" not in output
    assert "\\tcode" not in output

def test_oldconcepttable_with_lhdr_rhdr():
    r"""Test oldconcepttable with \lhdr and \rhdr headers instead of \hdstyle"""
    latex = r"""
\begin{oldconcepttable}{DefaultConstructible}{}{cpp17.defaultconstructible}
{x{2.15in}p{3in}}
\topline
\lhdr{Expression} & \rhdr{Post-condition} \\ \capsep
\tcode{T t;} & object \tcode{t} is default-initialized \\ \rowsep
\tcode{T u\{\};} & object \tcode{u} is value-initialized \\
\end{oldconcepttable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption with Cpp17 prefix
    assert "**Table: Cpp17DefaultConstructible requirements**" in output
    # Should have headers from \lhdr and \rhdr
    assert "| Expression | Post-condition |" in normalized
    # Should have data rows
    assert "| `T t;` |" in normalized
    assert "| `T u{};` |" in normalized or "`T u{}`" in output
    # Should NOT have LaTeX commands
    assert "\\lhdr" not in output
    assert "\\rhdr" not in output

def test_floattable_with_nested_texttt():
    r"""Test floattable with nested \texttt{} (from cpp-macros.lua \keyword conversion)

    This simulates what happens when cpp-macros.lua converts:
    \tcode{\keyword{signed} \keyword{char}} -> \texttt{\texttt{signed} \texttt{char}}

    Should render as single backticked `signed char`, not broken `signed` `char`
    """
    latex = r"""
\begin{floattable}{Minimum width}{basic.fundamental.width}{ll}
\topline
\lhdr{Type} & \rhdr{Minimum width} \\ \capsep
\texttt{\texttt{signed} \texttt{char}} & 8 \\
\texttt{\texttt{short} \texttt{int}} & 16 \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have single backticked spans, not broken adjacent backticks
    assert "`signed char`" in output
    assert "`short int`" in output
    # Should NOT have broken rendering with adjacent backticks or nested \texttt
    assert "\\texttt{signed}" not in output
    assert "\\texttt{char}" not in output
    assert "`signed` `char`" not in output
    assert "`short` `int`" not in output
    # Should NOT have LaTeX commands leaking
    assert "\\texttt" not in output

def test_oldconcepttable_with_multicolumn():
    r"""Test oldconcepttable with \multicolumn for spanning cells"""
    latex = r"""
\begin{oldconcepttable}{MoveConstructible}{}{cpp17.moveconstructible}
{p{1in}p{4.15in}}
\topline
\hdstyle{Expression} & \hdstyle{Post-condition} \\ \capsep
\tcode{T u = rv;} & \tcode{u} is equivalent to the value of \tcode{rv} \\ \rowsep
\multicolumn{2}{|p{5.3in}|}{
  \tcode{rv}'s state is unspecified
}\\
\end{oldconcepttable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: Cpp17MoveConstructible requirements**" in output
    # Should expand multicolumn content with span indicator
    assert "*[spans 2 columns]*" in output
    assert "`rv`'s state is unspecified" in output
    # Should NOT have LaTeX commands
    assert "\\multicolumn" not in output

def test_oldconcepttable_with_itemize():
    r"""Test oldconcepttable with \begin{itemize} lists in cells"""
    latex = r"""
\begin{oldconcepttable}{EqualityComparable}{}{cpp17.equalitycomparable}
{x{1in}p{3in}}
\topline
\hdstyle{Expression} & \hdstyle{Requirement} \\ \capsep
\tcode{a == b} &
\tcode{==} is an equivalence relation:
\begin{itemize}
\item For all \tcode{a}, \tcode{a == a}.
\item If \tcode{a == b}, then \tcode{b == a}.
\item If \tcode{a == b} and \tcode{b == c}, then \tcode{a == c}.
\end{itemize} \\
\end{oldconcepttable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: Cpp17EqualityComparable requirements**" in output
    # Should convert itemize to semicolon-separated list
    assert "For all `a`, `a == a`" in output
    assert "If `a == b`, then `b == a`" in output
    assert "If `a == b` and `b == c`, then `a == c`" in output
    # Items should be separated by semicolons
    assert ";" in output
    # Should NOT have LaTeX commands
    assert "\\begin{itemize}" not in output
    assert "\\item" not in output
    assert "\\end{itemize}" not in output

def test_oldconcepttable_with_tailnote():
    r"""Test oldconcepttable with \begin{tailnote} for footnotes"""
    latex = r"""
\begin{oldconcepttable}{Destructible}{}{cpp17.destructible}
{p{1in}p{4.15in}}
\topline
\hdstyle{Expression} & \hdstyle{Post-condition} \\ \capsep
\tcode{u.\~T()} & All resources owned by \tcode{u} are reclaimed \\ \rowsep
\multicolumn{2}{|l|}{
  \begin{tailnote}
  Array types and non-object types are not \oldconcept{Destructible}.
  \end{tailnote}
} \\
\end{oldconcepttable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: Cpp17Destructible requirements**" in output
    # Should convert tailnote to italic
    assert "*Array types and non-object types are not Cpp17Destructible.*" in output
    # Should expand \oldconcept{Destructible} to Cpp17Destructible
    assert "Cpp17Destructible" in output
    # Should NOT have LaTeX commands
    assert "\\begin{tailnote}" not in output
    assert "\\end{tailnote}" not in output
    assert "\\oldconcept" not in output

def test_floattable_with_br():
    r"""Test floattable with \br line breaks"""
    latex = r"""
\begin{floattable}{Test Table}{test.br}{ll}
\topline
\lhdr{Code} & \rhdr{Meaning} \\ \capsep
\tcode{T()} \br \tcode{T\{\}} & value-initialized or aggregate-initialized \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should convert \br to <br>
    assert "`T()` <br> `T{}`" in output or "`T()`<br>`T{}`" in output
    # Should NOT have LaTeX commands
    assert "\\br" not in output

def test_floattable_with_lhdrx_column_spanning():
    r"""Test floattable with \lhdrx{N}{text} column-spanning headers

    The character sets table in lex.tex uses \lhdrx{2}{character} which
    spans 2 columns, followed by \rhdr{glyph} for a total of 3 columns.
    This should generate a proper 3-column markdown table.
    """
    latex = r"""
\begin{floattable}{Basic character set}{lex.charset.basic}{lll}
\topline
\lhdrx{2}{character} & \rhdr{glyph} \\ \capsep
\tcode{U+0009} & character tabulation & \\
\tcode{U+000B} & line tabulation & \\
\tcode{U+0020} & space & \\
\tcode{U+0021} & & ! \\
\tcode{U+0022} & & " \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: Basic character set**" in output
    # Should have 3 columns (character spans 2, glyph is 1)
    # Header should be: | character |  | glyph |
    assert "| character |" in normalized
    assert "| glyph |" in normalized
    # Should have separator for 3 columns
    assert re.search(r'\| -+ \| -+ \| -+ \|', normalized)
    # Should have all data rows with 3 columns
    assert "| `U+0009` | character tabulation |  |" in normalized
    assert "| `U+000B` | line tabulation |  |" in normalized
    assert "| `U+0020` | space |  |" in normalized
    assert "| `U+0021` |  | ! |" in normalized
    assert "| `U+0022` |  | \" |" in normalized
    # Middle column should NOT be missing
    assert "character tabulation" in output
    assert "line tabulation" in output

def test_floattable_with_multiline_headers():
    r"""Test floattable with headers split across multiple lines

    The perm_options table in iostreams.tex has \lhdr{Name} & on one line
    and \rhdr{Meaning} on the next line. Both headers should be captured.
    """
    latex = r"""
\begin{floattable}
{Enum class \tcode{perm_options}}{fs.enum.perm.opts}{ll}
\topline
\lhdr{Name} &
  \rhdr{Meaning} \\ \capsep
\tcode{replace} &
  \tcode{permissions} shall replace bits \\ \rowsep
\tcode{add} &
  \tcode{permissions} shall add bits \\
\end{floattable}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: Enum class `perm_options`**" in output
    # Should have both headers (not just Meaning)
    assert "| Name | Meaning |" in normalized
    # Should have 2-column separator
    assert re.search(r'\| -+ \| -+ \|', normalized)
    # Should have data rows with both columns
    assert "| `replace` | `permissions` shall replace bits |" in normalized
    assert "| `add` | `permissions` shall add bits |" in normalized
    # Name column should NOT be missing
    assert "Name" in output

def test_libefftab_basic():
    r"""Test libefftab (effects table for enum/bitmask types)"""
    latex = r"""
\begin{libefftab}
  {\tcode{syntax_option_type} effects}
  {re.synopt}
\tcode{icase} &
Specifies that matching shall be performed without regard to case.
\\ \rowsep
\tcode{nosubs} &
Specifies that no sub-expressions shall be considered to be marked.
\\ \rowsep
\end{libefftab}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: `syntax_option_type` effects**" in output
    # Should have implicit headers
    assert "| Element | Effect(s) if set |" in normalized
    # Should have data rows
    assert "| `icase` | Specifies that matching shall be performed without regard to case. |" in normalized
    assert "| `nosubs` | Specifies that no sub-expressions shall be considered to be marked. |" in normalized
    # Should NOT have LaTeX commands
    assert "\\tcode" not in output
    assert "\\rowsep" not in output

def test_longlibefftab_basic():
    r"""Test longlibefftab (long effects table for enum/bitmask types)"""
    latex = r"""
\begin{longlibefftab}
  {\tcode{match_flag_type} effects}
  {re.matchflag}
\tcode{match_not_bol} &
The first character shall be treated as though it is not at the beginning of a line.
\\ \rowsep
\tcode{match_not_eol} &
The last character shall be treated as though it is not at the end of a line.
\\ \rowsep
\tcode{match_continuous} &
The expression shall only match a sub-sequence that begins at first.
\\ \rowsep
\end{longlibefftab}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: `match_flag_type` effects**" in output
    # Should have implicit headers
    assert "| Element | Effect(s) if set |" in normalized
    # Should have data rows
    assert "| `match_not_bol` |" in normalized
    assert "| `match_not_eol` |" in normalized
    assert "| `match_continuous` |" in normalized
    # Should NOT have LaTeX commands
    assert "\\tcode" not in output

def test_longliberrtab_basic():
    r"""Test longliberrtab (error value table)"""
    latex = r"""
\begin{longliberrtab}
  {\tcode{error_type} values in the C locale}
  {re.err}
\tcode{error_collate} &
The expression contains an invalid collating element name.
\\ \rowsep
\tcode{error_ctype} &
The expression contains an invalid character class name.
\\ \rowsep
\tcode{error_escape} &
The expression contains an invalid escaped character, or a trailing escape.
\\ \rowsep
\end{longliberrtab}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    normalized = normalize_table_whitespace(output)
    # Should have caption
    assert "**Table: `error_type` values in the C locale**" in output
    # Should have implicit headers (different from libefftab!)
    assert "| Value | Error condition |" in normalized
    # Should have data rows
    assert "| `error_collate` | The expression contains an invalid collating element name. |" in normalized
    assert "| `error_ctype` | The expression contains an invalid character class name. |" in normalized
    assert "| `error_escape` |" in normalized
    # Should NOT have LaTeX commands
    assert "\\tcode" not in output
    assert "\\rowsep" not in output
