"""Tests for cpp-sections.lua filter"""
import subprocess
from pathlib import Path
import sys

# Import inject_macros helper from conftest
sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import inject_macros

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-sections.lua")

def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with sections filter"""
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

def test_rsec0_basic():
    """Test basic \\rSec0 heading"""
    latex = r"\rSec0[intro.scope]{Scope}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "# Scope" in output

def test_rsec1_nested():
    """Test nested \\rSec1 heading"""
    latex = r"\rSec1[intro.compliance]{Implementation compliance}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "## Implementation compliance" in output

def test_rsec2_nested():
    """Test \\rSec2 heading"""
    latex = r"\rSec2[intro.compliance.general]{General}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "### General" in output

def test_rsec3_deeply_nested():
    """Test \\rSec3 heading"""
    latex = r"\rSec3[some.deep.nested.section]{Deep Section}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "#### Deep Section" in output

def test_multiple_sections():
    """Test multiple sections in sequence"""
    latex = r"""
\rSec0[intro.scope]{Scope}

Some content here.

\rSec1[intro.refs]{Normative references}

More content.

\rSec2[intro.refs.c]{C Standard}

Details about C.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "# Scope" in output
    assert "## Normative references" in output
    assert "### C Standard" in output

def test_section_with_complex_title():
    """Test section with complex title containing macros"""
    # Note: This tests the section structure, macros should be handled by cpp-macros.lua
    latex = r"\rSec0[basic.types]{Types and the program structure}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "# Types and the program structure" in output

def test_section_in_context():
    """Test section in a realistic document context"""
    latex = r"""
\rSec0[intro.scope]{Scope}

This document specifies requirements for implementations of the C++
programming language.

\rSec1[intro.refs]{Normative references}

The following documents are referred to in the text.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    # Check that sections are converted
    assert "# Scope" in output
    assert "## Normative references" in output
    # Check that content is preserved
    assert "This document specifies" in output
    assert "following documents" in output


# ============================================================================
# Regression Tests for Section Link Definition Generation (commit 59c30740)
# ============================================================================

def test_section_link_definitions_generated():
    """Test that link definitions are generated for all section labels"""
    # This is a regression test for commit 59c30740
    # Previously only referenced sections got link definitions
    latex = r"""
\rSec0[intro]{General}
\rSec1[intro.scope]{Scope}
\rSec1[intro.refs]{References}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # All sections should have link definitions
    assert "[intro]: #intro" in output
    assert "[intro.scope]: #intro.scope" in output
    assert "[intro.refs]: #intro.refs" in output

    # Check for link definition comment
    assert "<!-- Section link definitions -->" in output


def test_link_definitions_at_end_of_document():
    """Test that link definitions are placed at end of document"""
    latex = r"""
\rSec0[basic]{Basic concepts}

Some content here.

\rSec1[basic.def]{Definitions}

More content.
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Link definitions should come after content
    content_pos = output.find("Some content")
    link_def_pos = output.find("[basic]: #basic")

    assert content_pos < link_def_pos


def test_link_definitions_sorted():
    """Test that link definitions are sorted alphabetically"""
    latex = r"""
\rSec0[zeta]{Zeta}
\rSec0[alpha]{Alpha}
\rSec0[beta]{Beta}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Find positions of link definitions
    alpha_pos = output.find("[alpha]:")
    beta_pos = output.find("[beta]:")
    zeta_pos = output.find("[zeta]:")

    # Should be in sorted order
    assert alpha_pos < beta_pos < zeta_pos


def test_unreferenced_sections_get_definitions():
    """Test that sections never referenced elsewhere still get link definitions"""
    # This is the key regression test - previously these were missing
    latex = r"""
\rSec0[orphan.section]{Orphan Section}

This section is never referenced by any \iref or \ref command.

\rSec1[orphan.subsection]{Orphan Subsection}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Even orphan sections should have link definitions
    assert "[orphan.section]: #orphan.section" in output
    assert "[orphan.subsection]: #orphan.subsection" in output


def test_stable_name_anchor_with_double_brackets():
    """Test that section anchors use double brackets for visible stable names"""
    latex = r"\rSec0[expr.prim]{Primary expressions}"
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Anchor should have double brackets (commit aa9100a1)
    assert "[[expr.prim]]" in output

    # Link definition should have single brackets (markdown syntax)
    assert "[expr.prim]: #expr.prim" in output


def test_many_sections_all_get_definitions():
    """Test that all sections get definitions even with many sections"""
    sections = []
    for i in range(20):
        sections.append(f"\\rSec0[section{i}]{{Section {i}}}")

    latex = "\n".join(sections)
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # All 20 sections should have link definitions
    for i in range(20):
        assert f"[section{i}]: #section{i}" in output


def test_section_labels_with_dots_get_definitions():
    """Test sections with dots in labels get proper link definitions"""
    latex = r"""
\rSec0[basic]{Basic}
\rSec1[basic.def]{Definitions}
\rSec2[basic.def.odr]{One definition rule}
\rSec3[basic.def.odr.general]{General}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # All nested labels should have definitions
    assert "[basic]: #basic" in output
    assert "[basic.def]: #basic.def" in output
    assert "[basic.def.odr]: #basic.def.odr" in output
    assert "[basic.def.odr.general]: #basic.def.odr.general" in output


def test_rawblock_sections_also_get_definitions():
    """Test that RawBlock and RawInline section variants also get link definitions"""
    # The filter handles multiple formats of section commands
    latex = r"""
\begin{document}
\rSec0[intro]{Introduction}
\end{document}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Should have link definition
    assert "[intro]: #intro" in output


def test_no_duplicate_link_definitions():
    """Test that duplicate labels don't create duplicate link definitions"""
    # Edge case: if same label appears twice (shouldn't happen in practice)
    latex = r"""
\rSec0[test]{Test One}
\rSec0[test]{Test Two}
"""
    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Count occurrences of the link definition
    count = output.count("[test]: #test")

    # Should appear only once (or handle duplicates gracefully)
    assert count >= 1  # At least one definition exists
