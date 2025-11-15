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

"""Tests for nested content structures (examples in notes, footnotes, etc.)"""

import subprocess


def test_example_nested_in_note():
    """Test that examples nested inside notes are properly extracted."""
    latex = r"""
\begin{note}
The variable created in the condition is destroyed and created with each
iteration of the loop.
\begin{example}
\begin{codeblock}
struct A {
  int val;
  A(int i) : val(i) { }
  ~A() { }
  operator bool() { return val != 0; }
};
int i = 1;
while (A a = i) {
  // ...
  i = 0;
}
\end{codeblock}
In the while-loop, the constructor and destructor are each called twice,
once for the condition that succeeds and once for the condition that
fails.
\end{example}
\end{note}
"""
    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        "--lua-filter=src/cpp_std_converter/filters/cpp-notes-examples.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-code-blocks.lua",
    ]
    result = subprocess.run(
        cmd,
        input=latex,
        capture_output=True,
        text=True,
        cwd="/home/jason/notes/cpp_standard_tools/converted/cppstdmd",
    )

    output = result.stdout

    # Should contain the note text
    assert "The variable created in the condition is destroyed" in output

    # Should contain the example marker
    assert "[*Example" in output
    assert "end example*" in output  # Check for end marker

    # Should contain the code
    assert "struct A {" in output
    assert "int val;" in output
    assert "operator bool()" in output

    # Should contain the explanation after the code
    assert "constructor and destructor are each called twice" in output

    print("OUTPUT:", repr(output))


def test_multiple_examples_nested_in_note():
    """Test that multiple examples nested inside a single note are extracted."""
    latex = r"""
\begin{note}
If the \grammarterm{statement} cannot syntactically be a
\grammarterm{declaration}, there is no ambiguity.
\begin{example}
Assuming \tcode{T} is a type,
\begin{codeblock}
T(a)->m = 7;        // expression-statement
T(a)++;             // expression-statement
\end{codeblock}
\end{example}

The remaining cases are \grammarterm{declaration}{s}.
\begin{example}
\begin{codeblock}
T(a);               //  declaration
T(*b)();            //  declaration
\end{codeblock}
\end{example}
\end{note}
"""
    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        "--lua-filter=src/cpp_std_converter/filters/cpp-macros.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-notes-examples.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-code-blocks.lua",
    ]
    result = subprocess.run(
        cmd,
        input=latex,
        capture_output=True,
        text=True,
        cwd="/home/jason/notes/cpp_standard_tools/converted/cppstdmd",
    )

    output = result.stdout

    # Should contain both examples
    assert output.count("[*Example") == 2
    assert output.count("end example*") >= 2  # May have escaped bracket \]

    # Should contain code from first example
    assert "T(a)->m = 7;" in output
    assert "expression-statement" in output

    # Should contain the text between examples
    assert "The remaining cases are" in output

    # Should contain code from second example
    assert "T(a);" in output
    assert "declaration" in output

    print("OUTPUT:", repr(output))


def test_footnote_conversion():
    """Test that footnotes are converted to native GFM footnotes."""
    latex = r"""
In the second form of \keyword{if} statement
(the one including \keyword{else}), if the first substatement is also an
\keyword{if} statement then that inner \tcode{if} statement shall contain
an \keyword{else} part.
\begin{footnote}
In other words, the \keyword{else} is associated with the nearest un-elsed
\keyword{if}.
\end{footnote}
"""
    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        "--lua-filter=src/cpp_std_converter/filters/cpp-macros.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-notes-examples.lua",
    ]
    result = subprocess.run(
        cmd,
        input=latex,
        capture_output=True,
        text=True,
        cwd="/home/jason/notes/cpp_standard_tools/converted/cppstdmd",
    )

    output = result.stdout

    # Should contain the main text (keywords may be \texttt or backticks depending on context)
    assert (
        "In the second form of `if` statement" in output
        or "In the second form of \\texttt{if} statement" in output
    )
    # Check for else keyword (may have newline between keyword and "part")
    assert "`else`" in output or "\\texttt{else}" in output
    assert "part" in output  # Separately check for "part" word

    # Should contain GFM footnote reference marker
    assert "[^" in output  # Footnote reference like [^1]

    # Should contain footnote definition marker
    assert output.count("[^") >= 2  # At least one reference and one definition

    # Should contain the footnote content at the bottom
    assert "In other words" in output
    assert "nearest un-elsed" in output

    print("OUTPUT:", repr(output))


def test_footnote_in_declaration_statement():
    """Test footnote about switch/case jump converted to native GFM footnotes."""
    latex = r"""
Upon each transfer of control within a function from point $P$ to point $Q$,
all variables with automatic storage duration
that are active at $P$ and not at $Q$ are destroyed.
Then, all variables that are active at $Q$ but not at $P$ are initialized;
unless all such variables have vacuous initialization,
the transfer of control shall not be a jump.
\begin{footnote}
The transfer from the condition of a \keyword{switch} statement to a
\keyword{case} label is considered a jump in this respect.
\end{footnote}
"""
    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        "--lua-filter=src/cpp_std_converter/filters/cpp-macros.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-notes-examples.lua",
    ]
    result = subprocess.run(
        cmd,
        input=latex,
        capture_output=True,
        text=True,
        cwd="/home/jason/notes/cpp_standard_tools/converted/cppstdmd",
    )

    output = result.stdout

    # Should contain main text
    assert "Upon each transfer of control" in output

    # Should contain GFM footnote markers
    assert "[^" in output  # Footnote reference
    assert output.count("[^") >= 2  # Reference and definition

    # Should contain footnote content at the bottom
    assert "transfer from the condition of a `switch` statement" in output
    # May have line break between `case` and label due to wrapping
    assert "`case`" in output and "label is considered a jump" in output

    print("OUTPUT:", repr(output))
