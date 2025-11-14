"""Tests for link reference definition generation

Tests that verify link reference definitions are generated correctly
without duplicates.
"""

import re
import subprocess
import tempfile
from pathlib import Path

import pytest


def run_pandoc_with_filter(latex: str):
    """Helper to run pandoc with filters on LaTeX input"""
    # Read simplified macros
    macros_file = Path("src/cpp_std_converter/filters/simplified_macros.tex")
    if macros_file.exists():
        macros = macros_file.read_text()
    else:
        macros = ""

    latex_with_macros = macros + "\n\n" + latex if macros else latex

    # Run pandoc with filters in the correct order
    cmd = [
        "pandoc",
        "--from=latex+raw_tex",
        "--to=gfm",
        "--lua-filter=src/cpp_std_converter/filters/cpp-sections.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-itemdecl.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-code-blocks.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-definitions.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-notes-examples.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-lists.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-macros.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-math.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-grammar.lua",
        "--lua-filter=src/cpp_std_converter/filters/cpp-tables.lua",
    ]

    result = subprocess.run(
        cmd,
        input=latex_with_macros,
        capture_output=True,
        text=True,
    )

    return result.stdout, result.returncode


def test_no_duplicate_link_definitions():
    """Test that link reference definitions don't have duplicates

    Regression test for issue #2: cpp-sections.lua and cpp-macros.lua
    both generate link definitions, causing duplicates when a section
    is both defined and referenced.
    """
    latex = r"""
\rSec0[stmt]{Statements}
\rSec1[stmt.break]{Break statement}

The break statement \ref{stmt.break} terminates the loop.
It has the form \iref{stmt.break}.

\rSec1[stmt.continue]{Continue statement}

The continue statement \ref{stmt.continue} skips to next iteration.
    """

    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Extract all link reference definitions (lines matching [label]: target)
    link_defs = re.findall(r'^\[([^\]]+)\]:\s*(.+)$', output, re.MULTILINE)

    # Group by label to find duplicates
    labels = {}
    for label, target in link_defs:
        if label not in labels:
            labels[label] = []
        labels[label].append(target)

    # Check for duplicates
    duplicates = {label: targets for label, targets in labels.items() if len(targets) > 1}

    assert duplicates == {}, (
        f"Found duplicate link definitions:\n" +
        "\n".join(f"  [{label}]: appears {len(targets)} times with targets {targets}"
                  for label, targets in duplicates.items())
    )


def test_section_labels_have_definitions():
    """Test that all section labels get link definitions"""
    latex = r"""
\rSec0[basic]{Basic concepts}
\rSec1[basic.def]{Definitions}
\rSec1[basic.types]{Types}
    """

    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Check that link definitions exist for all sections
    assert "[basic]:" in output
    assert "[basic.def]:" in output
    assert "[basic.types]:" in output


def test_referenced_labels_have_definitions():
    """Test that all referenced labels get link definitions"""
    latex = r"""
\rSec0[basic]{Basic concepts}

See \ref{expr} for details on expressions.
Also see \iref{stmt.break} for break statements.
    """

    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Check that link definitions exist for all references
    assert "[expr]:" in output
    assert "[stmt.break]:" in output


def test_cross_file_vs_same_file_links():
    """Test that link targets are correct for cross-file vs same-file references"""
    latex = r"""
\rSec0[stmt]{Statements}
\rSec1[stmt.break]{Break statement}

Self-reference: \ref{stmt.break}
Cross-file reference: \ref{expr.prim}
    """

    output, code = run_pandoc_with_filter(latex)
    assert code == 0

    # Same-file reference should use #anchor
    assert re.search(r'\[stmt\.break\]:\s*#stmt\.break', output), \
        "Same-file reference should use #anchor"

    # Note: Cross-file reference behavior depends on label index
    # This test just verifies the link definition exists
    assert "[expr.prim]:" in output
