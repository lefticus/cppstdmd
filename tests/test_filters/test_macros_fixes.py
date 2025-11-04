"""Tests for macro filter improvements (impldef, tcode with special chars)"""
import subprocess
from pathlib import Path
import pytest

FILTER_PATH = Path("src/cpp_std_converter/filters/cpp-macros.lua")

def run_pandoc_with_filter(latex_content):
    """Helper to run Pandoc with macros filter"""
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

def test_impldef_simple():
    """Test \\impldef macro conversion"""
    latex = r"The value is \impldef{description text}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*implementation-defined*" in output
    # The description should not appear
    assert "description text" not in output

def test_impldef_with_nested_tcode():
    """Test \\impldef with nested \\tcode macro"""
    latex = r"The value is \impldef{search locations for \tcode{<>} header}."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "*implementation-defined*" in output
    # Neither the description nor the nested tcode should appear
    assert "search locations" not in output
    assert "<>" not in output

def test_tcode_with_hash():
    """Test \\tcode{\\#} conversion"""
    latex = r"It does not begin with a \tcode{\#} at the start."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`#`" in output
    assert "does not begin with a" in output

def test_tcode_with_double_hash():
    """Test \\tcode{\\#\\#} conversion"""
    latex = r"The \tcode{\#\#} operator is used for concatenation."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`##`" in output
    assert "operator" in output

def test_tcode_in_sentence():
    """Test \\tcode with various special characters"""
    latex = r"The macro \tcode{EMPTY} is defined."
    output, code = run_pandoc_with_filter(latex)
    assert code == 0
    assert "`EMPTY`" in output
    assert "macro" in output
    assert "defined" in output
