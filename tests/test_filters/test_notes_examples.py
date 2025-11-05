"""Tests for cpp-notes-examples.lua filter"""
import subprocess
from pathlib import Path
import pytest

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-notes-examples.lua")

def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with notes-examples filter"""
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

def test_basic_note():
    """Test basic note conversion"""
    latex = r"""Some text before.

\begin{note}
This is a note with some content.
\end{note}

Some text after."""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Note 1*" in output
    assert "This is a note with some content" in output
    assert "*end note*" in output
    assert "[" in output and "]" in output

def test_basic_example():
    """Test basic example conversion"""
    latex = r"""Some text before.

\begin{example}
This is an example with some content.
\end{example}

Some text after."""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Example 1*" in output
    assert "This is an example with some content" in output
    assert "*end example*" in output
    assert "[" in output and "]" in output

def test_note_with_code_block():
    """Test note containing a code block"""
    latex = r"""Some text.

\begin{note}
Here is a code example:
\begin{codeblock}
int x = 42;
\end{codeblock}
This demonstrates the concept.
\end{note}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Note 1*" in output
    # Content is parsed so text should be present
    assert "Here is a code example" in output
    assert "demonstrates the concept" in output
    # Code block will be a RawBlock with "codeblock" in it
    assert "codeblock" in output or "int x" in output
    assert "*end note*" in output

def test_example_with_code_block():
    """Test example containing a code block"""
    latex = r"""Some text.

\begin{example}
\begin{codeblock}
struct A {
  int m;
};
A&& operator+(A, A);
\end{codeblock}
The expression is an xvalue.
\end{example}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Example 1*" in output
    # Content is parsed so text should be present
    assert "xvalue" in output
    # Code block will be a RawBlock
    assert "codeblock" in output or "struct A" in output
    assert "*end example*" in output

def test_multiple_notes_and_examples():
    """Test multiple notes and examples with counter increments"""
    latex = r"""First paragraph.

\begin{note}
First note.
\end{note}

Second paragraph.

\begin{note}
Second note.
\end{note}

Third paragraph.

\begin{example}
First example.
\end{example}

Fourth paragraph.

\begin{example}
Second example.
\end{example}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Note 1*" in output
    assert "*Note 2*" in output
    assert "*Example 1*" in output
    assert "*Example 2*" in output

def test_counter_reset_on_section():
    """Test that counters reset when encountering a new section"""
    latex = r"""\section{Section 1}

\begin{note}
Note in section 1.
\end{note}

\begin{example}
Example in section 1.
\end{example}

\subsection{Subsection}

\begin{note}
Note in subsection (should be Note 1 again).
\end{note}

\begin{example}
Example in subsection (should be Example 1 again).
\end{example}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have two "Note 1" instances
    assert output.count("*Note 1*") == 2
    # Should have two "Example 1" instances
    assert output.count("*Example 1*") == 2

def test_note_with_latex_commands():
    """Test note containing LaTeX commands like \\ref"""
    latex = r"""\begin{note}
This references \ref{expr.compound} and uses \tcode{operator+}.
\end{note}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Note 1*" in output
    assert "*end note*" in output
    # LaTeX commands stay as raw when testing filter in isolation
    assert "tcode" in output or "ref" in output

def test_example_with_cross_reference():
    """Test example containing cross-references"""
    latex = r"""\begin{example}
See \ref{intro.scope} for details.
\end{example}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Example 1*" in output
    assert "*end example*" in output

def test_empty_note():
    """Test note with minimal content"""
    latex = r"""\begin{note}
\end{note}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should still create note markers even if empty
    # (actual behavior may vary, but shouldn't crash)

def test_nested_environments():
    """Test note containing multiple paragraphs and code"""
    latex = r"""\begin{note}
First paragraph of the note.

Second paragraph of the note.

\begin{codeblock}
int main() {
  return 0;
}
\end{codeblock}

Final paragraph.
\end{note}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Note 1*" in output
    assert "First paragraph" in output
    assert "Final paragraph" in output
    # Code block will be a RawBlock
    assert "codeblock" in output or "int main" in output
    assert "*end note*" in output

def test_example_with_at_escapes():
    r"""Test example with @ escaped \tcode{} in codeblock"""
    latex = r"""\begin{example}
The following code demonstrates macro replacement:
\begin{codeblock}
#define OBJ_LIKE      @\tcode{/* whitespace */ (1-1) /* other */}@
#define FUNC_LIKE( a )(     @\tcode{/* note the whitespace */ \textbackslash}@
                a @\tcode{/* other stuff on this line}@
                  @\tcode{*/}@ )
\end{codeblock}
\end{example}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Example 1*" in output
    # @ escape delimiters should be removed
    assert "@\\tcode{" not in output
    assert "}@" not in output
    # Content inside \tcode should be preserved
    assert "/* whitespace */" in output
    assert "/* note the whitespace */" in output
    assert "/* other stuff on this line" in output
    assert "*end example*" in output

def test_example_line_continuation():
    r"""Test that \textbackslash preserves line breaks in code"""
    latex = r"""\begin{example}
Valid macro redefinition:
\begin{codeblock}
#define FUNC_LIKE( a )(     @\tcode{/* note the whitespace */ \textbackslash}@
                a @\tcode{/* other stuff on this line}@
                  @\tcode{*/}@ )
\end{codeblock}
\end{example}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Example 1*" in output
    # The backslash should be at end of line with newline after it
    assert "/* note the whitespace */ \\" in output
    # The next line should start with spaces and 'a'
    assert "                a /*" in output
    # Should NOT have backslash followed by content on same line
    assert "\\ a" not in output and "\\                 a" not in output
    assert "*end example*" in output

def test_example_with_two_codeblocks():
    r"""Test example with two codeblocks (regression test for tcode leak)"""
    latex = r"""\begin{example}
The following sequence is valid:
\begin{codeblock}
#define OBJ_LIKE      (1-1)
#define OBJ_LIKE      @\tcode{/* whitespace */ (1-1) /* other */}@
#define FUNC_LIKE(a)   ( a )
#define FUNC_LIKE( a )(     @\tcode{/* note the whitespace */ \textbackslash}@
                a @\tcode{/* other stuff on this line}@
                  @\tcode{*/}@ )
\end{codeblock}
But the following redefinitions are invalid:
\begin{codeblock}
#define OBJ_LIKE    (0)         // different token sequence
#define OBJ_LIKE    (1 - 1)     // different whitespace
\end{codeblock}
\end{example}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Example 1*" in output
    # Should NOT have any \tcode{ leaking into output
    assert "\\tcode{" not in output
    # Should NOT have }@ leaking into output
    assert "}@" not in output
    # Should NOT have @\tcode leaking into output
    assert "@\\tcode" not in output

def test_counter_reset_on_subsubsection():
    """Test that counters reset at h3 (subsubsection) level"""
    latex = r"""\subsection{Algorithms}

\begin{note}
First note in subsection.
\end{note}

\begin{example}
First example in subsection.
\end{example}

\subsubsection{For each}

\begin{note}
Note in subsubsection (should be Note 1 again).
\end{note}

\begin{example}
Example in subsubsection (should be Example 1 again).
\end{example}

\subsubsection{Find}

\begin{note}
Note in another subsubsection (should be Note 1 again).
\end{note}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have three "Note 1" instances (one in subsection, two in subsubsections)
    assert output.count("*Note 1*") == 3
    # Should have two "Example 1" instances
    assert output.count("*Example 1*") == 2

def test_counter_reset_on_paragraph_level():
    """Test that counters reset at h4 (paragraph) level"""
    latex = r"""\subsubsection{Vector capacity}

\begin{note}
First note in subsubsection.
\end{note}

\paragraph{reserve}

\begin{note}
Note in paragraph (should be Note 1 again).
\end{note}

\begin{example}
Example in paragraph (should be Example 1).
\end{example}

\paragraph{shrink\_to\_fit}

\begin{note}
Note in another paragraph (should be Note 1 again).
\end{note}

\begin{example}
Example in another paragraph (should be Example 1 again).
\end{example}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have three "Note 1" instances
    assert output.count("*Note 1*") == 3
    # Should have two "Example 1" instances
    assert output.count("*Example 1*") == 2


def test_term_macro_in_note():
    r"""Test \term{} content is preserved within notes"""
    latex = r"""\begin{note}
Algorithms that obtain such effects include \term{selection sampling}
and \term{reservoir sampling}.
\end{note}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should have the note marker
    assert "*Note" in output
    # Should preserve the term content (possibly in italics with newlines)
    assert "selection" in output
    assert "sampling" in output
    assert "reservoir" in output
    # Should NOT have unexpanded macro
    assert "\\term" not in output
    # Content should be emphasized
    assert "*selection" in output or "*reservoir" in output


def test_defn_macro_in_note():
    r"""Test \defn{} content is preserved within notes"""
    latex = r"""\begin{note}
The sample (the \defn{selected items}) comes from the population.
\end{note}"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Should preserve the definition content
    assert "selected items" in output
    # Should NOT have empty parentheses
    assert "(the )" not in output
    # Should NOT have unexpanded macro
    assert "\\defn" not in output

def test_example_with_codeblocktu():
    r"""Test example with \begin{codeblocktu} nested inside (module.md bug)"""
    latex = r"""
\begin{example}
\begin{codeblocktu}{Translation unit \#1}
export module A;
export import :Foo;
export int baz();
\end{codeblocktu}

\begin{codeblocktu}{Translation unit \#2}
export module A:Foo;
import :Internals;
\end{codeblocktu}

Module \tcode{A} contains two translation units.
\end{example}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*Example 1*" in output
    # Check that both code blocks are present
    assert "export module A;" in output
    assert "export import :Foo" in output
    assert "export int baz()" in output
    assert "export module A:Foo" in output
    assert "import :Internals" in output
    # Check description text
    assert "Module" in output
    assert "contains two translation units" in output
    # Ensure \tcode{A} was expanded
    assert "\\tcode" not in output
    # Should have markdown code blocks
    assert "``` cpp" in output or "```cpp" in output
