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

"""
Tests for itemdecl/itemdescr formatting improvements.

Tests the visual separation between function declarations and their descriptions,
including blockquote indentation and italic (not bold-italic) labels.
"""

import subprocess
import sys
from pathlib import Path

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros


def run_pandoc_with_filter(latex_content: str, filter_name: str = "cpp-itemdecl.lua") -> str:
    """Helper to run Pandoc with a specific Lua filter."""
    # Inject simplified_macros.tex preprocessing
    latex_with_macros = inject_macros(latex_content)

    filters_dir = Path(__file__).parent.parent.parent / "src" / "cpp_std_converter" / "filters"
    filter_path = filters_dir / filter_name

    result = subprocess.run(
        ["pandoc", "--from=latex+raw_tex", "--to=gfm", f"--lua-filter={filter_path}"],
        input=latex_with_macros,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def test_result_macro_conversion():
    """Test that \\result becomes *Returns:* (italic, not bold-italic)."""
    latex = r"""
\begin{itemdecl}
iterator begin();
\end{itemdecl}

\begin{itemdescr}
\pnum
\result
\tcode{iterator}.

\pnum
\returns
An iterator referring to the first element.
\end{itemdescr}
"""
    output = run_pandoc_with_filter(latex)

    # Should convert \result to *Returns:*
    assert "*Returns:*" in output
    # Should NOT be bold-italic
    assert "***Returns:***" not in output
    # The \result field should now appear as a labeled section
    assert "`iterator`" in output


def test_labels_are_italic_not_bold():
    """Test that all labels are *Label:* not ***Label:***."""
    latex = r"""
\begin{itemdecl}
void func();
\end{itemdecl}

\begin{itemdescr}
\pnum
\expects
Condition must be true.

\pnum
\effects
Does something.

\pnum
\returns
Nothing.

\pnum
\complexity
Constant.

\pnum
\remarks
Some remark.
\end{itemdescr}
"""
    output = run_pandoc_with_filter(latex)

    # Should be italic only
    assert "*Preconditions:*" in output
    assert "*Effects:*" in output
    assert "*Returns:*" in output
    assert "*Complexity:*" in output
    assert "*Remarks:*" in output

    # Should NOT be bold-italic
    assert "***Preconditions:***" not in output
    assert "***Effects:***" not in output
    assert "***Returns:***" not in output
    assert "***Complexity:***" not in output
    assert "***Remarks:***" not in output


def test_itemdescr_blockquote():
    """Test that itemdescr content is formatted without blockquote for better readability."""
    latex = r"""
\begin{itemdecl}
void operator delete(void* ptr) noexcept;
\end{itemdecl}

\begin{itemdescr}
\pnum
\expects
\tcode{ptr} is a null pointer or its value represents an address.

\pnum
\effects
The deallocation function.
\end{itemdescr}
"""
    output = run_pandoc_with_filter(latex)

    # Labels should be present and properly formatted (without blockquote)
    assert "*Preconditions:*" in output
    assert "*Effects:*" in output

    # Content should be present
    assert "`ptr`" in output
    assert "deallocation function" in output

    # Verify no blockquote markers are present
    lines = output.split("\n")
    for line in lines:
        if line.strip() and not line.startswith("```") and not line.startswith("void"):
            # Content lines should not start with >
            assert not line.startswith(">")


def test_multiple_labels_in_blockquote():
    """Test function with multiple description labels formatted without blockquote."""
    latex = r"""
\begin{itemdecl}
template<class T>
void swap(T& a, T& b);
\end{itemdecl}

\begin{itemdescr}
\pnum
\mandates
\tcode{T} meets the requirements.

\pnum
\expects
Values are valid.

\pnum
\effects
Exchanges values.

\pnum
\ensures
Values are swapped.

\pnum
\complexity
Constant time.
\end{itemdescr}
"""
    output = run_pandoc_with_filter(latex)

    # All labels should be italic and properly formatted (without blockquote)
    assert "*Mandates:*" in output
    assert "*Preconditions:*" in output
    assert "*Effects:*" in output
    assert "*Ensures:*" in output  # Note: \ensures -> Ensures: in the filter
    assert "*Complexity:*" in output


def test_single_function_complete_formatting():
    """Integration test showing complete formatting for a single function."""
    latex = r"""
\begin{itemdecl}
size_t size() const noexcept;
\end{itemdecl}

\begin{itemdescr}
\pnum
\returns
The number of elements in the container.

\pnum
\complexity
Constant.
\end{itemdescr}
"""
    output = run_pandoc_with_filter(latex)

    # Should have code block
    assert "``` cpp" in output
    assert "size_t size() const noexcept;" in output
    assert "```" in output

    # Should have description with italic labels (without blockquote)
    assert "*Returns:*" in output
    assert "*Complexity:*" in output

    # Should have content (without blockquote)
    assert "The number of elements" in output
    assert "Constant" in output


def test_ensures_vs_postconditions():
    """Test that \\ensures becomes *Ensures:* not *Postconditions:*."""
    latex = r"""
\begin{itemdecl}
void func();
\end{itemdecl}

\begin{itemdescr}
\pnum
\ensures
Something is true afterwards.

\pnum
\postconditions
Another thing is true.
\end{itemdescr}
"""
    output = run_pandoc_with_filter(latex)

    # Both should appear as italic (without blockquote)
    assert "*Ensures:*" in output
    assert "*Postconditions:*" in output
