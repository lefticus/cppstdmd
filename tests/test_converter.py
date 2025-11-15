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

"""Unit tests for Converter class"""

import tempfile
from pathlib import Path

from cpp_std_converter.converter import Converter


class TestFixCrossFileLinks:
    """Test fix_cross_file_links method"""

    def test_empty_file_list(self):
        """Test with empty file list returns empty stats"""
        converter = Converter()
        stats = converter.fix_cross_file_links([])

        assert stats["files_updated"] == 0
        assert stats["links_updated"] == 0

    def test_no_cross_file_links(self):
        """Test with only same-file links (no updates needed)"""
        converter = Converter()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create file with anchors and same-file link definitions
            file1 = tmpdir / "intro.md"
            file1.write_text(
                """# Introduction <a id="intro.scope">[intro.scope]</a>

Some content referencing [intro.scope].

<!-- Link reference definitions -->
[intro.scope]: #intro.scope
"""
            )

            stats = converter.fix_cross_file_links([file1])

            # No updates should happen (same-file link)
            assert stats["files_updated"] == 0
            assert stats["links_updated"] == 0

            # Verify file unchanged
            content = file1.read_text()
            assert "[intro.scope]: #intro.scope" in content

    def test_cross_file_links_updated(self):
        """Test cross-file links are updated correctly"""
        converter = Converter()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create intro.md with anchor
            intro = tmpdir / "intro.md"
            intro.write_text(
                """# Introduction <a id="intro.scope">[intro.scope]</a>

Some intro content.

<!-- Link reference definitions -->
[intro.scope]: #intro.scope
"""
            )

            # Create expressions.md with reference to intro.scope
            expr = tmpdir / "expressions.md"
            expr.write_text(
                """# Expressions <a id="expr.typeid">[expr.typeid]</a>

Reference to [intro.scope] from expressions.

<!-- Link reference definitions -->
[intro.scope]: #intro.scope
[expr.typeid]: #expr.typeid
"""
            )

            stats = converter.fix_cross_file_links([intro, expr])

            # expressions.md should be updated
            assert stats["files_updated"] == 1
            assert stats["links_updated"] == 1

            # Verify intro.md unchanged (same-file reference)
            intro_content = intro.read_text()
            assert "[intro.scope]: #intro.scope" in intro_content

            # Verify expressions.md updated (cross-file reference)
            expr_content = expr.read_text()
            assert "[intro.scope]: intro.md#intro.scope" in expr_content
            # Same-file reference should remain unchanged
            assert "[expr.typeid]: #expr.typeid" in expr_content

    def test_multiple_cross_file_links(self):
        """Test multiple cross-file links in multiple files"""
        converter = Converter()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # intro.md with anchor
            intro = tmpdir / "intro.md"
            intro.write_text(
                """# Introduction <a id="intro.scope">[intro.scope]</a>
<a id="intro.defs">[intro.defs]</a>

<!-- Link reference definitions -->
[intro.scope]: #intro.scope
[expr.typeid]: #expr.typeid
"""
            )

            # expressions.md with anchor
            expr = tmpdir / "expressions.md"
            expr.write_text(
                """# Expressions <a id="expr.typeid">[expr.typeid]</a>

<!-- Link reference definitions -->
[intro.scope]: #intro.scope
[intro.defs]: #intro.defs
[expr.typeid]: #expr.typeid
"""
            )

            # basic.md with anchors
            basic = tmpdir / "basic.md"
            basic.write_text(
                """# Basic <a id="basic.def">[basic.def]</a>

<!-- Link reference definitions -->
[intro.scope]: #intro.scope
[expr.typeid]: #expr.typeid
"""
            )

            stats = converter.fix_cross_file_links([intro, expr, basic])

            # All 3 files should be updated
            assert stats["files_updated"] == 3
            # intro: 1, expr: 2, basic: 2 = 5 total
            assert stats["links_updated"] == 5

            # Verify intro.md
            intro_content = intro.read_text()
            assert "[intro.scope]: #intro.scope" in intro_content  # Same-file
            assert "[expr.typeid]: expressions.md#expr.typeid" in intro_content  # Cross-file

            # Verify expressions.md
            expr_content = expr.read_text()
            assert "[intro.scope]: intro.md#intro.scope" in expr_content
            assert "[intro.defs]: intro.md#intro.defs" in expr_content
            assert "[expr.typeid]: #expr.typeid" in expr_content  # Same-file

            # Verify basic.md
            basic_content = basic.read_text()
            assert "[intro.scope]: intro.md#intro.scope" in basic_content
            assert "[expr.typeid]: expressions.md#expr.typeid" in basic_content

    def test_nonexistent_label_unchanged(self):
        """Test that link definitions for non-existent anchors are left unchanged"""
        converter = Converter()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # intro.md with reference to non-existent label
            intro = tmpdir / "intro.md"
            intro.write_text(
                """# Introduction <a id="intro.scope">[intro.scope]</a>

Reference to [nonexistent.label].

<!-- Link reference definitions -->
[intro.scope]: #intro.scope
[nonexistent.label]: #nonexistent.label
"""
            )

            stats = converter.fix_cross_file_links([intro])

            # No updates (nonexistent label not in mapping)
            assert stats["files_updated"] == 0
            assert stats["links_updated"] == 0

            # Verify file unchanged
            content = intro.read_text()
            assert "[nonexistent.label]: #nonexistent.label" in content
