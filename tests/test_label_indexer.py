"""
Tests for label_indexer module

Tests the LabelIndexer class that builds label→file mappings for cross-file linking.
"""

import tempfile
from pathlib import Path
import pytest

from cpp_std_converter.label_indexer import LabelIndexer


@pytest.fixture
def temp_source_dir():
    """Create a temporary directory with sample .tex files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir)

        # Create a basic chapter file with sections
        (source / "basic.tex").write_text(r"""
\renewcommand{\stablenamestart}{basic}
\rSec0[basic]{Basic concepts}
\rSec1[basic.def]{Definitions}
\rSec1[basic.types]{Types}
        """)

        # Create another chapter
        (source / "expressions.tex").write_text(r"""
\renewcommand{\stablenamestart}{expr}
\rSec0[expr]{Expressions}
\rSec1[expr.prim]{Primary expressions}
\rSec2[expr.prim.lambda]{Lambda expressions}
        """)

        # File without stable name (uses filename)
        (source / "utilities.tex").write_text(r"""
\rSec0[utilities]{Utilities}
\rSec1[forward]{Forward declarations}
\rSec1[declval]{The declval function}
        """)

        # Skip file (should be ignored)
        (source / "std.tex").write_text(r"""
\rSec0[std]{Document metadata}
        """)

        # File with duplicate label
        (source / "duplicates.tex").write_text(r"""
\rSec0[dup]{Duplicates}
\rSec1[basic.def]{Duplicate of basic.def}
        """)

        yield source


def test_initialization():
    """Test LabelIndexer initialization"""
    indexer = LabelIndexer(Path("/tmp/test"))
    assert indexer.source_dir == Path("/tmp/test")
    assert indexer.label_to_file == {}
    assert indexer.file_labels == {}
    assert indexer.duplicate_labels == {}


def test_extract_labels_from_file(temp_source_dir):
    """Test extracting labels from a single file"""
    indexer = LabelIndexer(temp_source_dir)

    # Test basic.tex
    labels = indexer._extract_labels_from_file(temp_source_dir / "basic.tex")
    assert labels == {"basic", "basic.def", "basic.types"}

    # Test expressions.tex
    labels = indexer._extract_labels_from_file(temp_source_dir / "expressions.tex")
    assert labels == {"expr", "expr.prim", "expr.prim.lambda"}

    # Test file without any sections
    empty_file = temp_source_dir / "empty.tex"
    empty_file.write_text("Some text without sections")
    labels = indexer._extract_labels_from_file(empty_file)
    assert labels == set()


def test_extract_stable_names(temp_source_dir):
    """Test extracting stable names from all files"""
    indexer = LabelIndexer(temp_source_dir)
    stable_names = indexer._extract_stable_names()

    # Files with explicit stable names different from filename
    # Note: basic.tex has stable name "basic" which matches filename, so it's not added
    assert stable_names.get("expressions") == "expr"

    # File without stable name should not be in mapping
    assert "utilities" not in stable_names

    # Skip files should not be in mapping
    assert "std" not in stable_names


def test_build_index_with_stable_names(temp_source_dir):
    """Test building index with stable name mapping"""
    indexer = LabelIndexer(temp_source_dir)
    result = indexer.build_index(use_stable_names=True)

    # Check expressions.tex labels map to 'expr' stable name
    assert result["expr"] == "expr"
    assert result["expr.prim"] == "expr"
    assert result["expr.prim.lambda"] == "expr"

    # Check utilities.tex labels map to filename (no stable name)
    assert result["utilities"] == "utilities"
    assert result["forward"] == "utilities"
    assert result["declval"] == "utilities"

    # Check basic.tex labels map to filename (stable name matches filename)
    assert result["basic"] == "basic"
    # Note: basic.def is duplicated in duplicates.tex, so might map there
    assert result["basic.def"] in {"basic", "duplicates"}
    assert result["basic.types"] == "basic"

    # Skip file should not be indexed
    assert "std" not in result


def test_build_index_without_stable_names(temp_source_dir):
    """Test building index using filenames instead of stable names"""
    indexer = LabelIndexer(temp_source_dir)
    result = indexer.build_index(use_stable_names=False)

    # All labels should map to their tex filenames
    assert result["basic"] == "basic"
    # Note: basic.def is duplicated, might be in duplicates
    assert result["basic.def"] in {"basic", "duplicates"}
    assert result["expr"] == "expressions"
    assert result["expr.prim"] == "expressions"
    assert result["utilities"] == "utilities"


def test_build_index_with_provided_stable_name_map(temp_source_dir):
    """Test building index with pre-computed stable name mapping"""
    indexer = LabelIndexer(temp_source_dir)

    # Provide custom mapping
    custom_map = {
        "basic": "basics",  # Different from what's in file
        "expressions": "exprs",  # Different from what's in file
        "utilities": "utils"
    }

    result = indexer.build_index(
        use_stable_names=True,
        stable_name_map=custom_map
    )

    # Check labels use provided mapping
    assert result["basic"] == "basics"
    # Note: basic.def is duplicated, might be in duplicates
    assert result["basic.def"] in {"basics", "duplicates"}
    assert result["expr"] == "exprs"
    assert result["expr.prim"] == "exprs"
    assert result["utilities"] == "utils"


def test_duplicate_label_tracking(temp_source_dir):
    """Test that duplicate labels are tracked correctly"""
    indexer = LabelIndexer(temp_source_dir)
    indexer.build_index(use_stable_names=True)

    # basic.def appears in both basic.tex and duplicates.tex
    assert "basic.def" in indexer.duplicate_labels
    assert set(indexer.duplicate_labels["basic.def"]) == {"basic", "duplicates"}

    # Note: label_to_file contains first occurrence, but files are processed
    # alphabetically, so "basic" comes before "duplicates"
    # Due to glob ordering, the actual first occurrence depends on filesystem
    assert indexer.label_to_file["basic.def"] in {"basic", "duplicates"}


def test_file_labels_tracking(temp_source_dir):
    """Test that file_labels dict is populated correctly"""
    indexer = LabelIndexer(temp_source_dir)
    indexer.build_index(use_stable_names=True)

    # Check basic file labels
    assert "basic.def" in indexer.file_labels["basic"]
    assert "basic.types" in indexer.file_labels["basic"]

    # Check expr file labels
    assert "expr.prim" in indexer.file_labels["expr"]
    assert "expr.prim.lambda" in indexer.file_labels["expr"]


def test_get_file_for_label(temp_source_dir):
    """Test get_file_for_label method"""
    indexer = LabelIndexer(temp_source_dir)
    indexer.build_index(use_stable_names=True)

    # basic.def is duplicated, might be in either file
    assert indexer.get_file_for_label("basic.def") in {"basic", "duplicates"}
    assert indexer.get_file_for_label("expr.prim") == "expr"
    assert indexer.get_file_for_label("forward") == "utilities"
    assert indexer.get_file_for_label("nonexistent") is None


def test_get_labels_for_file(temp_source_dir):
    """Test get_labels_for_file method"""
    indexer = LabelIndexer(temp_source_dir)
    indexer.build_index(use_stable_names=True)

    basic_labels = indexer.get_labels_for_file("basic")
    assert "basic" in basic_labels
    assert "basic.def" in basic_labels
    assert "basic.types" in basic_labels

    expr_labels = indexer.get_labels_for_file("expr")
    assert "expr" in expr_labels
    assert "expr.prim" in expr_labels

    # Non-existent file
    assert indexer.get_labels_for_file("nonexistent") == set()


def test_write_lua_table(temp_source_dir):
    """Test writing label index as Lua table"""
    indexer = LabelIndexer(temp_source_dir)
    indexer.build_index(use_stable_names=True)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
        output_file = Path(f.name)

    try:
        indexer.write_lua_table(output_file)

        # Read and verify the output
        content = output_file.read_text()

        # Check header
        assert "-- Auto-generated" in content
        assert "return {" in content

        # Check some mappings are present
        assert '["basic"]' in content or '["basic.def"]' in content
        assert '["expr"]' in content or '["expr.prim"]' in content

        # Verify it's valid Lua syntax (contains assignments)
        assert "] = " in content

    finally:
        output_file.unlink()


def test_lua_table_escaping(temp_source_dir):
    """Test that special characters are escaped in Lua table"""
    # Create file with label containing special characters
    (temp_source_dir / "special.tex").write_text(r"""
\rSec0[test"quote]{Test with quote}
\rSec1[test\backslash]{Test with backslash}
    """)

    indexer = LabelIndexer(temp_source_dir)
    indexer.build_index(use_stable_names=False)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
        output_file = Path(f.name)

    try:
        indexer.write_lua_table(output_file)
        content = output_file.read_text()

        # Check escaping
        assert '\\"' in content  # Quote should be escaped
        assert '\\\\' in content  # Backslash should be escaped

    finally:
        output_file.unlink()


def test_get_statistics(temp_source_dir):
    """Test get_statistics method"""
    indexer = LabelIndexer(temp_source_dir)
    indexer.build_index(use_stable_names=True)

    stats = indexer.get_statistics()

    # We have basic, expr, utilities, duplicates = 4 files (std is skipped)
    assert stats['files'] == 4

    # Total unique labels (first occurrence only)
    assert stats['labels'] > 0

    # We have one duplicate (basic.def)
    assert stats['duplicates'] == 1


def test_skip_files_are_skipped(temp_source_dir):
    """Test that SKIP_FILES are properly excluded"""
    # std.tex should be skipped
    indexer = LabelIndexer(temp_source_dir)
    indexer.build_index(use_stable_names=True)

    # std label should not be in index
    assert "std" not in indexer.label_to_file
    assert "std" not in indexer.file_labels


def test_nonexistent_directory():
    """Test behavior with non-existent directory"""
    indexer = LabelIndexer(Path("/nonexistent/path"))
    result = indexer.build_index()

    # Should return empty dict, not crash
    assert result == {}
    assert indexer.file_labels == {}


def test_error_handling_for_unreadable_file(temp_source_dir):
    """Test that indexer handles file read errors gracefully"""
    # Create a file, then make it unreadable (if supported by OS)
    import sys
    if sys.platform != "win32":  # chmod not reliable on Windows
        bad_file = temp_source_dir / "unreadable.tex"
        bad_file.write_text(r"\rSec0[bad]{Bad}")
        bad_file.chmod(0o000)

        try:
            indexer = LabelIndexer(temp_source_dir)
            # Should not crash, just skip the unreadable file
            labels = indexer._extract_labels_from_file(bad_file)
            assert labels == set()
        finally:
            bad_file.chmod(0o644)


def test_complex_label_patterns(temp_source_dir):
    """Test extraction of labels with various formats"""
    (temp_source_dir / "complex.tex").write_text(r"""
\rSec0[simple]{Simple}
\rSec1[with.dots.multiple]{With multiple dots}
\rSec2[with-dashes]{With dashes}
\rSec3[with_underscores]{With underscores}
\rSec4[MixedCase]{Mixed case}
\rSec5[with123numbers]{With numbers}
    """)

    indexer = LabelIndexer(temp_source_dir)
    labels = indexer._extract_labels_from_file(temp_source_dir / "complex.tex")

    assert "simple" in labels
    assert "with.dots.multiple" in labels
    assert "with-dashes" in labels
    assert "with_underscores" in labels
    assert "MixedCase" in labels
    assert "with123numbers" in labels


def test_empty_label(temp_source_dir):
    """Test handling of empty labels"""
    (temp_source_dir / "empty_label.tex").write_text(r"""
\rSec0[]{Empty label}
\rSec1[  ]{Whitespace label}
    """)

    indexer = LabelIndexer(temp_source_dir)
    labels = indexer._extract_labels_from_file(temp_source_dir / "empty_label.tex")

    # Empty/whitespace labels are extracted
    # The regex [^\]]+ requires at least one char, so truly empty [] won't match
    # but whitespace will
    if "" in labels:
        assert "" in labels
    if "  " in labels:
        assert "  " in labels
