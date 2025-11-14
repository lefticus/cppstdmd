"""Tests for generate_html_site.py script."""

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path to import generate_html_site
sys.path.insert(0, str(Path(__file__).parent.parent))

import generate_html_site


class TestPureFunctions:
    """Test pure functions with no side effects."""

    def test_get_dot_count_zero_dots(self):
        """Test counting dots in stable names with no dots."""
        assert generate_html_site.get_dot_count("intro") == 0
        assert generate_html_site.get_dot_count("class") == 0
        assert generate_html_site.get_dot_count("array") == 0

    def test_get_dot_count_one_dot(self):
        """Test counting dots in stable names with one dot."""
        assert generate_html_site.get_dot_count("alg.copy") == 1
        assert generate_html_site.get_dot_count("class.ctor") == 1
        assert generate_html_site.get_dot_count("expr.add") == 1

    def test_get_dot_count_multiple_dots(self):
        """Test counting dots in stable names with multiple dots."""
        assert generate_html_site.get_dot_count("alg.find.first.of") == 3
        assert generate_html_site.get_dot_count("a.b.c.d.e") == 4
        assert generate_html_site.get_dot_count("container.vector.overview") == 2

    def test_get_dot_count_ignores_colons(self):
        """Test that :: is not counted as a dot (legacy C++11 notation)."""
        assert generate_html_site.get_dot_count("string::append") == 0
        assert generate_html_site.get_dot_count("vector::push_back") == 0
        assert generate_html_site.get_dot_count("basic_string::npos") == 0

    def test_get_dot_count_ignores_underscores(self):
        """Test that underscores within names are not counted."""
        assert generate_html_site.get_dot_count("alg.all_of") == 1
        assert generate_html_site.get_dot_count("is_trivially_copyable") == 0
        assert generate_html_site.get_dot_count("type_traits.is_const") == 1

    def test_sanitize_filename_safe_names(self):
        """Test that already-safe names are unchanged."""
        assert generate_html_site.sanitize_filename("intro") == "intro"
        assert generate_html_site.sanitize_filename("class") == "class"
        assert generate_html_site.sanitize_filename("alg.copy") == "alg.copy"
        assert generate_html_site.sanitize_filename("test-name") == "test-name"
        assert generate_html_site.sanitize_filename("test_name") == "test_name"

    def test_sanitize_filename_unsafe_characters(self):
        """Test sanitization of unsafe characters."""
        assert generate_html_site.sanitize_filename("test name") == "test_name"
        assert generate_html_site.sanitize_filename("test/name") == "test_name"
        assert generate_html_site.sanitize_filename("test:name") == "test_name"
        assert generate_html_site.sanitize_filename("test?name") == "test_name"

    def test_sanitize_filename_multiple_unsafe(self):
        """Test sanitization with multiple unsafe characters."""
        assert generate_html_site.sanitize_filename("a b/c:d?e") == "a_b_c_d_e"
        assert generate_html_site.sanitize_filename("hello world!") == "hello_world_"

    def test_get_timsong_url_valid_version(self):
        """Test generating timsong URLs for valid versions."""
        url = generate_html_site.get_timsong_url("n4950", "stmt.expr")
        assert url == "https://timsong-cpp.github.io/cppwp/n4950/stmt.expr"

        url = generate_html_site.get_timsong_url("n3337", "class.ctor")
        assert url == "https://timsong-cpp.github.io/cppwp/n3337/class.ctor"

    def test_get_timsong_url_trunk(self):
        """Test that trunk returns None (not published)."""
        url = generate_html_site.get_timsong_url("trunk", "array.size")
        assert url is None

    def test_get_github_markdown_url_default_repo(self):
        """Test GitHub URL generation with default repository."""
        url = generate_html_site.get_github_markdown_url("n4950", "array.overview")
        # array.overview should map to containers chapter
        expected = (
            "https://github.com/lefticus/cppstdmd/blob/main/n4950/containers.md#array.overview"
        )
        assert url == expected

    def test_get_github_markdown_url_custom_repo(self):
        """Test GitHub URL generation with custom repository."""
        url = generate_html_site.get_github_markdown_url(
            "n4950", "class.copy", repo_owner="customuser", repo_name="customrepo"
        )
        expected = "https://github.com/customuser/customrepo/blob/main/n4950/class.md#class.copy"
        assert url == expected

    def test_get_github_markdown_url_different_versions(self):
        """Test GitHub URL generation for different versions."""
        url = generate_html_site.get_github_markdown_url("trunk", "stmt.expr")
        assert "trunk/stmt.md#stmt.expr" in url

        url = generate_html_site.get_github_markdown_url("n3337", "expr.add")
        assert "n3337/expr.md#expr.add" in url

    def test_create_icon_known_icons(self):
        """Test icon creation for known icon names."""
        # Check that it returns HTML <i> element
        icon = generate_html_site.create_icon("home")
        assert icon.startswith('<i class="')
        assert icon.endswith('"></i>')
        assert "fa-" in icon

    def test_create_icon_unknown_icon(self):
        """Test icon creation for unknown icon name."""
        icon = generate_html_site.create_icon("nonexistent-icon")
        # Should return default question mark icon
        assert '<i class="fa-solid fa-question"></i>' == icon

    def test_create_icon_various_types(self):
        """Test that different icon types work."""
        # These should not raise errors and should return valid HTML
        for icon_name in ["list", "search", "external", "file"]:
            icon = generate_html_site.create_icon(icon_name)
            assert icon.startswith('<i class="')
            assert icon.endswith('"></i>')


class TestFileIO:
    """Test functions that involve file I/O."""

    def test_get_file_size_kb_small_file(self):
        """Test getting file size for a small file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("Hello World\n")  # ~12 bytes
            temp_path = Path(f.name)

        try:
            size = generate_html_site.get_file_size_kb(temp_path)
            assert size >= 0  # Small files might round to 0.0
            assert size < 1.0  # Should be less than 1 KB
        finally:
            temp_path.unlink()

    def test_get_file_size_kb_larger_file(self):
        """Test getting file size for a larger file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            # Write ~2KB of data
            f.write("x" * 2048)
            temp_path = Path(f.name)

        try:
            size = generate_html_site.get_file_size_kb(temp_path)
            assert 1.5 < size < 2.5  # Should be around 2 KB
        finally:
            temp_path.unlink()

    def test_get_file_size_kb_nonexistent(self):
        """Test getting file size for nonexistent file."""
        size = generate_html_site.get_file_size_kb(Path("/nonexistent/file.txt"))
        assert size == 0.0

    def test_count_diff_lines_empty(self):
        """Test counting lines in an empty diff."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            temp_path = Path(f.name)

        try:
            count = generate_html_site.count_diff_lines(temp_path)
            assert count == 0
        finally:
            temp_path.unlink()

    def test_count_diff_lines_with_additions(self):
        """Test counting lines with additions."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("diff --git a/file.txt b/file.txt\n")
            f.write("@@ -1,3 +1,5 @@\n")
            f.write(" context line\n")
            f.write("+added line 1\n")
            f.write("+added line 2\n")
            f.write(" another context\n")
            temp_path = Path(f.name)

        try:
            count = generate_html_site.count_diff_lines(temp_path)
            # Should count: @@ line + 2 added lines = 3
            assert count == 3
        finally:
            temp_path.unlink()

    def test_count_diff_lines_with_deletions(self):
        """Test counting lines with deletions."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("diff --git a/file.txt b/file.txt\n")
            f.write("@@ -1,5 +1,3 @@\n")
            f.write(" context line\n")
            f.write("-deleted line 1\n")
            f.write("-deleted line 2\n")
            f.write(" another context\n")
            temp_path = Path(f.name)

        try:
            count = generate_html_site.count_diff_lines(temp_path)
            # Should count: @@ line + 2 deleted lines = 3
            assert count == 3
        finally:
            temp_path.unlink()

    def test_count_diff_lines_mixed(self):
        """Test counting lines with mixed changes."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("diff --git a/file.txt b/file.txt\n")
            f.write("@@ -1,4 +1,4 @@\n")
            f.write(" context\n")
            f.write("-old line\n")
            f.write("+new line\n")
            f.write(" more context\n")
            f.write("@@ -10,2 +10,3 @@\n")
            f.write("+another addition\n")
            temp_path = Path(f.name)

        try:
            count = generate_html_site.count_diff_lines(temp_path)
            # Should count: 2 @@ lines + 1 deletion + 2 additions = 5
            assert count == 5
        finally:
            temp_path.unlink()

    def test_extract_stable_name_from_diff_header(self):
        """Test extracting stable name from diff file header."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("# Stable name: alg.copy\n")
            f.write("\n")
            f.write("diff content here\n")
            temp_path = Path(f.name)

        try:
            stable_name = generate_html_site.extract_stable_name(temp_path)
            assert stable_name == "alg.copy"
        finally:
            temp_path.unlink()

    def test_extract_stable_name_no_header(self):
        """Test extracting stable name when no header present."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("just some diff content\n")
            f.write("no header here\n")
            temp_path = Path(f.name)

        try:
            stable_name = generate_html_site.extract_stable_name(temp_path)
            assert stable_name is None
        finally:
            temp_path.unlink()

    def test_extract_stable_name_complex_name(self):
        """Test extracting complex stable names."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("# Stable name: alg.find.first.of\n")
            temp_path = Path(f.name)

        try:
            stable_name = generate_html_site.extract_stable_name(temp_path)
            assert stable_name == "alg.find.first.of"
        finally:
            temp_path.unlink()


class TestExtractDiffKeywords:
    """Test keyword extraction from diff content."""

    def test_extract_diff_keywords_empty(self):
        """Test extracting keywords from empty diff."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            temp_path = Path(f.name)

        try:
            keywords = generate_html_site.extract_diff_keywords(temp_path)
            assert keywords == []
        finally:
            temp_path.unlink()

    def test_extract_diff_keywords_no_matches(self):
        """Test extracting keywords from diff with no identifier lines."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("Some random text\nNo keywords here\n")
            temp_path = Path(f.name)

        try:
            keywords = generate_html_site.extract_diff_keywords(temp_path)
            assert keywords == []
        finally:
            temp_path.unlink()

    def test_extract_diff_keywords_additions(self):
        """Test extracting keywords from addition lines."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("+void foo();\n+int bar = 42;\n+class MyClass {};\n")
            temp_path = Path(f.name)

        try:
            keywords = generate_html_site.extract_diff_keywords(temp_path)
            # Should extract: foo, bar, MyClass
            assert "foo" in keywords
            assert "bar" in keywords
            assert "MyClass" in keywords
        finally:
            temp_path.unlink()

    def test_extract_diff_keywords_deletions(self):
        """Test extracting keywords from deletion lines."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("-void old_func();\n-int deprecated = 0;\n")
            temp_path = Path(f.name)

        try:
            keywords = generate_html_site.extract_diff_keywords(temp_path)
            # Should extract: old_func, deprecated
            assert "old_func" in keywords
            assert "deprecated" in keywords
        finally:
            temp_path.unlink()

    def test_extract_diff_keywords_cpp_identifiers(self):
        """Test extracting C++ identifiers."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write(
                "+std::vector<int> vec;\n+template<typename T>\n+constexpr auto lambda = []() {};\n"
            )
            temp_path = Path(f.name)

        try:
            keywords = generate_html_site.extract_diff_keywords(temp_path)
            # Should extract various identifiers
            assert "vector" in keywords
            assert "vec" in keywords
            assert "lambda" in keywords
        finally:
            temp_path.unlink()

    def test_extract_diff_keywords_filters_short_words(self):
        """Test that very short words are filtered out."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("+int a;\n+void b();\n+class ABC {};\n")
            temp_path = Path(f.name)

        try:
            keywords = generate_html_site.extract_diff_keywords(temp_path)
            # Short words (a, b) should be filtered (len > 2 filter), ABC should remain
            assert "a" not in keywords
            assert "b" not in keywords
            assert "ABC" in keywords
        finally:
            temp_path.unlink()

    def test_extract_diff_keywords_filters_common_words(self):
        """Test that common stop words are filtered."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write("+the and for this that with from have\n")
            temp_path = Path(f.name)

        try:
            keywords = generate_html_site.extract_diff_keywords(temp_path)
            # Common stop words should be filtered
            assert "the" not in keywords
            assert "and" not in keywords
            assert "for" not in keywords
        finally:
            temp_path.unlink()


class TestGenerateSearchIndex:
    """Test search index generation."""

    def test_generate_search_index_empty_list(self):
        """Test generating index from empty stable names list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            generate_html_site.generate_search_index(
                [], output_dir, "test-slug"  # Empty stable names list
            )

            # Should create an empty JSON file
            index_file = output_dir / "test-slug_search_index.json"
            assert index_file.exists()
            with open(index_file) as f:
                data = json.load(f)
                assert data == []

    def test_generate_search_index_with_diffs(self):
        """Test generating index from stable names with diff files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            output_dir = tmpdir / "output"
            output_dir.mkdir()

            # Create sample diff files
            diff1 = tmpdir / "array.diff"
            diff1.write_text("+void push_back();\n+void pop_back();\n")

            diff2 = tmpdir / "vector.diff"
            diff2.write_text("+void resize();\n+void reserve();\n")

            # Create stable names list
            stable_names = [{"name": "array", "path": diff1}, {"name": "vector", "path": diff2}]

            generate_html_site.generate_search_index(stable_names, output_dir, "test-slug")

            # Should create JSON with indexed keywords
            index_file = output_dir / "test-slug_search_index.json"
            assert index_file.exists()
            with open(index_file) as f:
                data = json.load(f)
                assert len(data) == 2
                # Check structure
                for entry in data:
                    assert "name" in entry
                    assert "keywords" in entry
                    assert isinstance(entry["keywords"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
