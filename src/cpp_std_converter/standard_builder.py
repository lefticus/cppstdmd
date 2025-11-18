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
standard_builder.py

Builds a complete C++ standard document from std.tex by:
1. Parsing std.tex to extract chapter order
2. Converting each chapter in order
3. Concatenating with merged cross-reference link definitions
"""

import contextlib
import os
import re
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from pylatexenc.latexwalker import LatexMacroNode, LatexWalker

from .utils import cleanup_temp_files, ensure_dir, expand_latex_inputs


def _convert_chapter_worker(
    work_unit: dict,
    draft_dir: Path,
    output_dir: Path,
    label_index_file: Path,
    verbose: bool = False,
) -> dict:
    """
    Worker function for parallel chapter conversion.

    Must be at module level to be picklable for multiprocessing.

    Args:
        work_unit: Dictionary describing the work to do:
            - type: 'single' or 'collision'
            - stable_name: Output file stem
            - chapter: Chapter name (for single)
            - chapters: List of chapter names (for collision/merge)
        draft_dir: Path to cplusplus/draft source directory
        output_dir: Path to output directory
        label_index_file: Path to label index Lua file
        verbose: Print progress (usually False for parallel workers)

    Returns:
        Dictionary with conversion results:
            - success: bool
            - output_file: Path to output file (if successful)
            - stable_name: str
            - error: str (if failed)
    """
    from .converter import Converter

    draft_dir = Path(draft_dir)
    output_dir = Path(output_dir)
    stable_name = work_unit["stable_name"]

    try:
        # Create converter instance for this worker
        converter = Converter()

        # Determine input file(s)
        temp_files = []

        if work_unit["type"] == "collision":
            # Merge multiple files
            chapters = work_unit["chapters"]
            chapter_files = []
            for ch in chapters:
                ch_file = draft_dir / f"{ch}.tex"
                if ch_file.exists():
                    chapter_files.append(ch_file)

            # Merge files into temporary file
            merged_content = []
            for tex_file in chapter_files:
                content = tex_file.read_text(encoding="utf-8")
                merged_content.append(content)

            # Create temporary merged file
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".tex", delete=False, encoding="utf-8"
            )
            tmp.write("\n\n".join(merged_content))
            tmp.close()
            file_to_convert = Path(tmp.name)
            temp_files.append(file_to_convert)

        else:
            # Single file conversion
            chapter = work_unit["chapter"]
            chapter_file = draft_dir / f"{chapter}.tex"

            if not chapter_file.exists():
                return {
                    "success": False,
                    "stable_name": stable_name,
                    "error": f"{chapter}.tex not found",
                }

            file_to_convert = chapter_file

            # Expand \input{} commands for front/back
            if chapter in ["front", "back"]:
                content = chapter_file.read_text(encoding="utf-8")
                base_dir = chapter_file.parent
                expanded = expand_latex_inputs(content, base_dir)

                tmp = tempfile.NamedTemporaryFile(
                    mode="w", suffix=".tex", delete=False, encoding="utf-8"
                )
                tmp.write(expanded)
                tmp.close()
                file_to_convert = Path(tmp.name)
                temp_files.append(file_to_convert)

        # Convert to markdown
        output_file = output_dir / f"{stable_name}.md"
        converter.convert_file(
            file_to_convert,
            output_file=output_file,
            standalone=True,
            verbose=False,
            current_file_stem=stable_name,
            label_index_file=label_index_file,
        )

        # Cleanup temporary files
        cleanup_temp_files(temp_files)

        return {"success": True, "output_file": output_file, "stable_name": stable_name}

    except Exception as e:
        # Cleanup temporary files on error
        cleanup_temp_files(temp_files)

        return {"success": False, "stable_name": stable_name, "error": str(e)}


class StandardBuilder:
    """Builds complete standard document from std.tex driver file"""

    def __init__(self, draft_dir: Path):
        """
        Args:
            draft_dir: Path to cplusplus/draft source directory
        """
        self.draft_dir = Path(draft_dir)
        self.std_tex = self.draft_dir / "std.tex"

    def extract_chapter_order(
        self, include_frontmatter: bool = True, include_backmatter: bool = True
    ) -> list[str]:
        r"""
        Parse std.tex to extract ordered list of chapter filenames.

        Uses pylatexenc to parse LaTeX and extract \include{filename} commands.

        Args:
            include_frontmatter: Include frontmatter chapters (cover, TOC)
            include_backmatter: Include backmatter chapters (index)

        Returns:
            List of chapter filenames (without .tex extension)
        """
        if not self.std_tex.exists():
            raise FileNotFoundError(f"std.tex not found at {self.std_tex}")

        content = self.std_tex.read_text(encoding="utf-8")

        # Use pylatexenc to parse the LaTeX
        walker = LatexWalker(content)
        nodelist, _, _ = walker.get_latex_nodes()

        chapters = []
        in_frontmatter = False
        in_mainmatter = False
        in_backmatter = False

        # Walk through nodes looking for \include{} commands
        def visit_node(node):
            nonlocal in_frontmatter, in_mainmatter, in_backmatter

            if isinstance(node, LatexMacroNode):
                # Track document sections
                if node.macroname == "frontmatter":
                    in_frontmatter = True
                elif node.macroname == "mainmatter":
                    in_frontmatter = False
                    in_mainmatter = True
                elif node.macroname == "backmatter":
                    in_mainmatter = False
                    in_backmatter = True
                elif node.macroname == "include":
                    # Decide whether to include based on section
                    should_include = False
                    if (
                        (in_frontmatter and include_frontmatter)
                        or in_mainmatter
                        or (in_backmatter and include_backmatter)
                    ):
                        should_include = True

                    if should_include and node.nodeargd and node.nodeargd.argnlist:
                        # Extract the filename from the argument
                        arg = node.nodeargd.argnlist[0]
                        if arg and hasattr(arg, "nodelist"):
                            # Get the text content
                            filename = "".join(
                                n.chars if hasattr(n, "chars") else "" for n in arg.nodelist
                            )
                            if filename:
                                chapters.append(filename.strip())

            # Recursively visit child nodes
            if hasattr(node, "nodelist") and node.nodelist:
                for child in node.nodelist:
                    visit_node(child)

        for node in nodelist:
            visit_node(node)

        return chapters

    def _expand_input_commands(self, tex_file: Path) -> Path:
        """
        Expand \\input{} commands in a LaTeX file by inlining referenced files.

        Creates a temporary file with all \\input{filename} commands replaced
        by the content of filename.tex.

        Args:
            tex_file: Path to LaTeX file that may contain \\input{} commands

        Returns:
            Path to temporary file with expanded content
        """
        content = tex_file.read_text(encoding="utf-8")
        base_dir = tex_file.parent
        expanded = expand_latex_inputs(content, base_dir)

        # Create temporary file with expanded content
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8")
        tmp.write(expanded)
        tmp.close()

        return Path(tmp.name)

    def extract_stable_name_from_tex(self, tex_file: Path, converter) -> str:
        """
        Extract stable section name from a .tex file using Pandoc.

        Uses the existing Pandoc + cpp-sections.lua pipeline to parse the LaTeX
        and extract the first section's stable name (the label in \rSec0[label]{Title}).

        Args:
            tex_file: Path to .tex file
            converter: Converter instance to use for parsing

        Returns:
            Stable name prefix (e.g., "expr" for expressions.tex)
            Falls back to filename stem if extraction fails

        Examples:
            expressions.tex → "expr" (from \rSec0[expr]{Expressions})
            statements.tex → "stmt" (from \rSec0[stmt.stmt]{Statements})
            preprocessor.tex → "cpp" (from \rSec0[cpp]{Preprocessing directives})
        """
        try:
            # Find the first \rSec0[label] line in the file
            # This is the top-level section that defines the stable name
            rsec0_line = None
            with tex_file.open("r", encoding="utf-8") as f:
                for line in f:
                    # Look for \rSec0[label]{Title} pattern
                    if r"\rSec0[" in line:
                        rsec0_line = line.strip()
                        break

            if not rsec0_line:
                # No \rSec0 found, fall back to filename
                return tex_file.stem

            # Create temporary file with just the \rSec0 line
            # This avoids issues with unclosed LaTeX environments when truncating
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".tex", delete=False, encoding="utf-8"
            )
            tmp.write(rsec0_line + "\n")
            tmp.close()
            tmp_path = Path(tmp.name)

            try:
                # Convert with Pandoc (cpp-sections.lua extracts the label)
                markdown = converter.convert_file(
                    tmp_path, output_file=None, standalone=False, verbose=False
                )

                # Extract first <a id="..."> anchor created by cpp-sections.lua
                # Format: <a id="stable.name">[stable.name]</a>
                match = re.search(r'<a id="([^"]+)">', markdown)
                if match:
                    label = match.group(1)
                    # Extract prefix before first dot
                    # "expr.prim" → "expr"
                    # "stmt.stmt" → "stmt"
                    # "intro.scope" → "intro"
                    stable_name = label.split(".")[0] if "." in label else label
                    return stable_name

            finally:
                # Clean up temp file
                tmp_path.unlink(missing_ok=True)

        except (OSError, UnicodeDecodeError, re.error):
            # If extraction fails, fall back to filename
            # This handles files that don't have \rSec tags or conversion errors
            pass

        # Fallback: use filename stem
        return tex_file.stem

    def detect_stable_name_collisions(
        self, chapters: list[str], chapter_to_stable: dict[str, str], verbose: bool = False
    ) -> dict[str, list[str]]:
        """
        Detect stable name collisions and group chapters that need to be merged.

        When multiple source files have the same stable name prefix (e.g., classes.tex,
        access.tex, derived.tex all have 'class' prefix), they must be merged into a
        single output file to avoid data loss.

        This happens in older C++ standards (C++11/n3337) where topics were split across
        multiple files but later consolidated.

        Args:
            chapters: Ordered list of chapter names from std.tex
            chapter_to_stable: Mapping from chapter name to stable name
            verbose: Print collision information

        Returns:
            Dictionary mapping stable_prefix -> [ordered_list_of_chapters]
            Only includes entries with 2+ chapters (collision groups)

        Example:
            Input:
                chapters = ['classes', 'derived', 'access', 'declarations', 'declarators']
                chapter_to_stable = {'classes': 'class', 'derived': 'class', 'access': 'class',
                                    'declarations': 'dcl', 'declarators': 'dcl'}
            Output:
                {'class': ['classes', 'derived', 'access'],
                 'dcl': ['declarations', 'declarators']}
        """
        # Group chapters by stable name
        stable_to_chapters = {}
        for chapter in chapters:
            stable_name = chapter_to_stable.get(chapter)
            if not stable_name:
                continue

            if stable_name not in stable_to_chapters:
                stable_to_chapters[stable_name] = []
            stable_to_chapters[stable_name].append(chapter)

        # Find collision groups (stable names with 2+ chapters)
        collision_groups = {
            stable: chapters_list
            for stable, chapters_list in stable_to_chapters.items()
            if len(chapters_list) > 1
        }

        if verbose and collision_groups:
            print(f"\nDetected {len(collision_groups)} stable name collision(s):")
            for stable_name, chapters_list in collision_groups.items():
                print(f"  {stable_name}: {len(chapters_list)} files will be merged")
                for chapter in chapters_list:
                    print(f"    - {chapter}.tex")

        return collision_groups

    def _merge_tex_files(self, chapter_files: list[Path], verbose: bool = False) -> Path:
        r"""
        Merge multiple LaTeX files into a single temporary file.

        Concatenates the content of multiple .tex files in order, preserving
        all \rSec0, \label{}, and other LaTeX commands. The merged file can
        then be converted as a single unit.

        Args:
            chapter_files: Ordered list of .tex files to merge
            verbose: Print merge information

        Returns:
            Path to temporary file containing merged content
        """
        if verbose:
            print(f"    Merging {len(chapter_files)} files:")
            for f in chapter_files:
                print(f"      + {f.name}")

        # Concatenate file contents with separators
        merged_content = []
        for tex_file in chapter_files:
            content = tex_file.read_text(encoding="utf-8")
            merged_content.append(content)

        # Create temporary file with merged content
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8")
        # Join with double newline to ensure proper spacing
        tmp.write("\n\n".join(merged_content))
        tmp.close()

        return Path(tmp.name)

    def build_full_standard(
        self, converter, output_file: Path, verbose: bool = False, toc_depth: int = 1
    ) -> tuple[str, list[str]]:
        """
        Build complete standard by converting chapters in order and concatenating.

        Args:
            converter: LatexToMarkdownConverter instance
            output_file: Path to write complete standard
            verbose: Print progress messages
            toc_depth: Maximum heading depth for table of contents (1=H1 only, 2=H1+H2, etc.)

        Returns:
            Tuple of (markdown_content, list of converted chapters)
        """
        chapters = self.extract_chapter_order()

        if verbose:
            print(f"Found {len(chapters)} chapters in std.tex")

        converted_chapters = []
        all_content_parts = []
        all_references = {}  # Collect all references from all chapters
        temp_files = []  # Track temporary files for cleanup

        for i, chapter in enumerate(chapters, 1):
            chapter_file = self.draft_dir / f"{chapter}.tex"

            if not chapter_file.exists():
                if verbose:
                    print(f"Warning: {chapter}.tex not found, skipping")
                continue

            if verbose:
                print(f"[{i}/{len(chapters)}] Converting {chapter}.tex...")

            # Expand \input{} commands for chapters that use them
            # (front.tex and back.tex contain \input{} references)
            file_to_convert = chapter_file
            if chapter in ["front", "back"]:
                try:
                    file_to_convert = self._expand_input_commands(chapter_file)
                    temp_files.append(file_to_convert)
                except Exception as e:
                    if verbose:
                        print(f"Warning: Could not expand inputs in {chapter}.tex: {e}")

            # Convert chapter to markdown
            try:
                markdown = converter.convert_file(
                    file_to_convert,
                    output_file=None,  # Return as string
                    standalone=False,  # Don't include standalone wrappers
                    verbose=False,
                )

                # Extract link definitions and content separately
                content, references = self._split_content_and_references(markdown)
                all_content_parts.append(content)
                all_references.update(references)

                converted_chapters.append(chapter)

            except Exception as e:
                # Always print conversion errors to prevent silent failures
                print(f"ERROR: Failed to convert {chapter}.tex: {e}", file=sys.stderr)
                if verbose:
                    import traceback

                    traceback.print_exc()
                continue

        # Build final document
        full_content = "\n\n---\n\n".join(all_content_parts)

        # Generate and prepend Table of Contents
        toc = self._generate_toc(full_content, max_depth=toc_depth)
        full_content = toc + "\n\n---\n\n" + full_content

        # Add all link definitions at the end
        if all_references:
            link_defs = "\n<!-- Link reference definitions -->\n"
            for ref in sorted(all_references.keys()):
                link_defs += f"[{ref}]: #{ref}\n"
            full_content += "\n\n" + link_defs

        # Write to output file
        output_file.write_text(full_content, encoding="utf-8")

        # Cleanup temporary files
        cleanup_temp_files(temp_files)

        if verbose:
            print(f"\nWrote complete standard to {output_file}")
            print(f"Converted {len(converted_chapters)}/{len(chapters)} chapters")
            print(f"Total cross-references: {len(all_references)}")

        return full_content, converted_chapters

    def _generate_toc(self, markdown_content: str, max_depth: int = 1) -> str:
        """
        Generate a Table of Contents from markdown headings.

        Extracts headings with format: # Title <a id="label">[label]</a>
        Generates TOC entries with format: <section num> <title> [<stable name>]

        Args:
            markdown_content: Full markdown content with headings
            max_depth: Maximum heading depth to include (1=H1 only, 2=H1+H2, etc.)

        Returns:
            TOC as a string
        """
        toc_lines = []
        toc_lines.append("# Table of Contents\n")

        # Pattern to match headings with embedded anchors
        # Matches: ## Title <a id="label">[[label]]</a>
        heading_pattern = re.compile(
            r'^(#{1,6})\s+(.+?)\s+<a id="([^"]+)">\[\[([^\]]+)\]\]</a>\s*$', re.MULTILINE
        )

        # Track section numbers at each level
        section_numbers = [0, 0, 0, 0, 0, 0]  # Support up to H6

        for match in heading_pattern.finditer(markdown_content):
            hashes = match.group(1)
            title = match.group(2).strip()
            stable_name = match.group(4)

            level = len(hashes) - 1  # H1=0, H2=1, etc.

            # Update section numbers (always update for correct numbering)
            section_numbers[level] += 1
            # Reset deeper levels
            for i in range(level + 1, 6):
                section_numbers[i] = 0

            # Skip headings deeper than max_depth
            if level >= max_depth:
                continue

            # Build section number string (e.g., "1.2.3")
            section_num = ".".join(str(section_numbers[i]) for i in range(level + 1))

            # Create TOC entry with indentation
            indent = "  " * level
            list_marker = "- "
            toc_entry = (
                f"{indent}{list_marker}{section_num} {title} [[{stable_name}]](#{stable_name})"
            )
            toc_lines.append(toc_entry)

        return "\n".join(toc_lines)

    def _split_content_and_references(self, markdown: str) -> tuple[str, dict]:
        """
        Split markdown into content and link reference definitions.

        Returns:
            Tuple of (content, dict of references)
        """
        lines = markdown.split("\n")
        content_lines = []
        references = {}
        in_references = False

        for line in lines:
            if "<!-- Link reference definitions -->" in line:
                in_references = True
                continue

            if in_references:
                # Match [ref]: #ref pattern
                match = re.match(r"\[([^\]]+)\]:\s*#\1", line)
                if match:
                    references[match.group(1)] = True
                    continue

            content_lines.append(line)

        return "\n".join(content_lines).strip(), references

    def _generate_toc_for_separate_files(self, output_files: list[Path], max_depth: int = 1) -> str:
        """
        Generate a Table of Contents with links to separate markdown files.

        Similar to _generate_toc() but generates cross-file links:
        [intro.scope](intro.md#intro.scope) instead of [intro.scope](#intro.scope)

        Args:
            output_files: List of output markdown files
            max_depth: Maximum heading depth to include (1=H1 only, 2=H1+H2, etc.)

        Returns:
            TOC as a string with cross-file links
        """
        toc_lines = []
        toc_lines.append("# Table of Contents\n")

        # Pattern to match headings with embedded anchors
        # Matches: ## Title <a id="label">[[label]]</a>
        heading_pattern = re.compile(
            r'^(#{1,6})\s+(.+?)\s+<a id="([^"]+)">\[\[([^\]]+)\]\]</a>\s*$', re.MULTILINE
        )

        # Track section numbers at each level
        section_numbers = [0, 0, 0, 0, 0, 0]  # Support up to H6

        # Process files in order
        for md_file in output_files:
            content = md_file.read_text(encoding="utf-8")
            filename = md_file.stem

            for match in heading_pattern.finditer(content):
                hashes = match.group(1)
                title = match.group(2).strip()
                anchor_id = match.group(3)
                stable_name = match.group(4)

                level = len(hashes) - 1  # H1=0, H2=1, etc.

                # Update section numbers (always update for correct numbering)
                section_numbers[level] += 1
                # Reset deeper levels
                for i in range(level + 1, 6):
                    section_numbers[i] = 0

                # Skip headings deeper than max_depth
                if level >= max_depth:
                    continue

                # Build section number string (e.g., "1.2.3")
                section_num = ".".join(str(section_numbers[i]) for i in range(level + 1))

                # Create TOC entry with cross-file link
                indent = "  " * level
                list_marker = "- "
                # Format: - section_num title [[stable_name]](filename.md#anchor)
                toc_entry = f"{indent}{list_marker}{section_num} {title} [[{stable_name}]]({filename}.md#{anchor_id})"
                toc_lines.append(toc_entry)

        return "\n".join(toc_lines)

    def build_separate_chapters(
        self,
        converter,
        output_dir: Path,
        verbose: bool = False,
        toc_depth: int = 1,
    ) -> list[Path]:
        """
        Build separate markdown files for each chapter with cross-file linking.

        Converts each chapter in std.tex to a separate .md file, then fixes
        cross-file reference links so they point to the correct file.
        Generates a table of contents and appends it to front.md.

        Args:
            converter: LatexToMarkdownConverter instance
            output_dir: Directory to write chapter markdown files
            verbose: Print progress messages
            toc_depth: Maximum heading depth for table of contents (1=H1 only, 2=H1+H2, etc.)

        Returns:
            List of output file paths
        """
        chapters = self.extract_chapter_order()

        if verbose:
            print(f"Found {len(chapters)} chapters in std.tex")

        output_dir = Path(output_dir)
        ensure_dir(output_dir)

        output_files = []
        temp_files = []  # Track temporary files for cleanup
        chapter_to_stable = {}  # Mapping from source filename to stable name

        # Pre-extract stable names for all chapters
        # This is done upfront to avoid repeated conversions
        if verbose:
            print("Extracting stable names...")

        for chapter in chapters:
            chapter_file = self.draft_dir / f"{chapter}.tex"
            if chapter_file.exists():
                stable_name = self.extract_stable_name_from_tex(chapter_file, converter)
                chapter_to_stable[chapter] = stable_name
                if verbose and stable_name != chapter:
                    print(f"  {chapter}.tex → {stable_name}.md")

        # Detect stable name collisions
        collision_groups = self.detect_stable_name_collisions(chapters, chapter_to_stable, verbose)

        # Build label index for cross-file references
        if verbose:
            print("\nBuilding label index for cross-file references...")

        from .label_indexer import LabelIndexer

        indexer = LabelIndexer(self.draft_dir)
        indexer.build_index(use_stable_names=True, stable_name_map=chapter_to_stable)

        # Write Lua table file
        label_index_file = output_dir / "cpp_std_labels.lua"
        indexer.write_lua_table(label_index_file)

        if verbose:
            stats = indexer.get_statistics()
            print(f"Indexed {stats['labels']} labels across {stats['files']} files")
            if stats["duplicates"] > 0:
                print(f"Warning: Found {stats['duplicates']} duplicate labels")

        # Create work units for parallel processing
        # Each work unit is either a single chapter or a collision group
        work_units = []
        processed_chapters = set()

        for chapter in chapters:
            # Skip if already processed as part of a collision group
            if chapter in processed_chapters:
                continue

            chapter_file = self.draft_dir / f"{chapter}.tex"
            if not chapter_file.exists():
                if verbose:
                    print(f"Warning: {chapter}.tex not found, skipping")
                continue

            # Get stable name for this chapter
            stable_name = chapter_to_stable.get(chapter, chapter)

            # Check if this chapter is part of a collision group
            if stable_name in collision_groups:
                # Collision group - create work unit for merged files
                chapters_to_merge = collision_groups[stable_name]
                work_units.append(
                    {
                        "type": "collision",
                        "stable_name": stable_name,
                        "chapters": chapters_to_merge,
                    }
                )
                processed_chapters.update(chapters_to_merge)
            else:
                # Normal single-file conversion
                work_units.append(
                    {
                        "type": "single",
                        "stable_name": stable_name,
                        "chapter": chapter,
                    }
                )
                processed_chapters.add(chapter)

        # Process work units in parallel
        if verbose:
            print(f"\nConverting {len(work_units)} chapters in parallel...")

        # Use conservative worker count (4 workers, or CPU count if less)
        max_workers = min(4, os.cpu_count() or 1)

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all work units
            future_to_unit = {}
            for work_unit in work_units:
                future = executor.submit(
                    _convert_chapter_worker,
                    work_unit,
                    self.draft_dir,
                    output_dir,
                    label_index_file,
                    verbose=False,  # Workers don't print progress
                )
                future_to_unit[future] = work_unit

            # Collect results as they complete (but preserve chapter order later)
            results_by_stable_name = {}
            completed = 0
            for future in as_completed(future_to_unit):
                work_unit = future_to_unit[future]
                completed += 1

                try:
                    result = future.result()

                    if result["success"]:
                        # Store result by stable_name for ordering later
                        results_by_stable_name[result["stable_name"]] = result["output_file"]
                        if verbose:
                            print(
                                f"[{completed}/{len(work_units)}] Completed {result['stable_name']}.md"
                            )
                    else:
                        # Print conversion errors
                        print(
                            f"ERROR: Failed to convert {result['stable_name']}: {result.get('error', 'Unknown error')}",
                            file=sys.stderr,
                        )

                except Exception as e:
                    # Handle worker exceptions
                    stable_name = work_unit.get("stable_name", "unknown")
                    print(f"ERROR: Worker exception for {stable_name}: {e}", file=sys.stderr)
                    if verbose:
                        import traceback

                        traceback.print_exc()

        # Reconstruct output_files in correct chapter order
        for work_unit in work_units:
            stable_name = work_unit["stable_name"]
            if stable_name in results_by_stable_name:
                output_files.append(results_by_stable_name[stable_name])

        # Note: Cross-file links are now handled during conversion via label indexing
        # The old post-processing approach (fix_cross_file_links) is no longer needed

        # Generate TOC and append to front.md (or its stable name equivalent)
        front_stable_name = chapter_to_stable.get("front", "front")
        front_file = output_dir / f"{front_stable_name}.md"
        if front_file.exists() and output_files:
            if verbose:
                print("\nGenerating table of contents...")

            toc = self._generate_toc_for_separate_files(output_files, max_depth=toc_depth)

            # Append TOC to front.md
            front_content = front_file.read_text(encoding="utf-8")

            # Add separator and TOC
            updated_front = front_content + "\n\n---\n\n" + toc
            front_file.write_text(updated_front, encoding="utf-8")

            if verbose:
                print("Added table of contents to front.md")

        # Cleanup temporary files
        cleanup_temp_files(temp_files)

        if verbose:
            print(f"\nWrote {len(output_files)} chapter files to {output_dir}")

        return output_files
