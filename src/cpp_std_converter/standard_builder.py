"""
standard_builder.py

Builds a complete C++ standard document from std.tex by:
1. Parsing std.tex to extract chapter order
2. Converting each chapter in order
3. Concatenating with merged cross-reference link definitions
"""

from pathlib import Path
from typing import List, Tuple
import re
import tempfile
from pylatexenc.latexwalker import LatexWalker, LatexMacroNode


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
        self,
        include_frontmatter: bool = True,
        include_backmatter: bool = True
    ) -> List[str]:
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

        content = self.std_tex.read_text(encoding='utf-8')

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
                if node.macroname == 'frontmatter':
                    in_frontmatter = True
                elif node.macroname == 'mainmatter':
                    in_frontmatter = False
                    in_mainmatter = True
                elif node.macroname == 'backmatter':
                    in_mainmatter = False
                    in_backmatter = True
                elif node.macroname == 'include':
                    # Decide whether to include based on section
                    should_include = False
                    if in_frontmatter and include_frontmatter:
                        should_include = True
                    elif in_mainmatter:
                        should_include = True
                    elif in_backmatter and include_backmatter:
                        should_include = True

                    if should_include:
                        # Extract the filename from the argument
                        if node.nodeargd and node.nodeargd.argnlist:
                            arg = node.nodeargd.argnlist[0]
                            if arg and hasattr(arg, 'nodelist'):
                                # Get the text content
                                filename = ''.join(
                                    n.chars if hasattr(n, 'chars') else ''
                                    for n in arg.nodelist
                                )
                                if filename:
                                    chapters.append(filename.strip())

            # Recursively visit child nodes
            if hasattr(node, 'nodelist') and node.nodelist:
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
        content = tex_file.read_text(encoding='utf-8')
        base_dir = tex_file.parent

        # Find all \input{filename} commands
        def expand_input(match):
            filename = match.group(1)
            input_file = base_dir / f"{filename}.tex"

            if input_file.exists():
                # Read and return the input file content
                return input_file.read_text(encoding='utf-8')
            else:
                # If file doesn't exist, keep the \input command
                return match.group(0)

        # Replace \input{filename} with file content
        # Handle both \input{filename} and \input {filename}
        expanded = re.sub(
            r'\\input\s*\{([^}]+)\}',
            expand_input,
            content
        )

        # Create temporary file with expanded content
        tmp = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.tex',
            delete=False,
            encoding='utf-8'
        )
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
            with tex_file.open('r', encoding='utf-8') as f:
                for line in f:
                    # Look for \rSec0[label]{Title} pattern
                    if r'\rSec0[' in line:
                        rsec0_line = line.strip()
                        break

            if not rsec0_line:
                # No \rSec0 found, fall back to filename
                return tex_file.stem

            # Create temporary file with just the \rSec0 line
            # This avoids issues with unclosed LaTeX environments when truncating
            tmp = tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.tex',
                delete=False,
                encoding='utf-8'
            )
            tmp.write(rsec0_line + '\n')
            tmp.close()
            tmp_path = Path(tmp.name)

            try:
                # Convert with Pandoc (cpp-sections.lua extracts the label)
                markdown = converter.convert_file(
                    tmp_path,
                    output_file=None,
                    standalone=False,
                    verbose=False
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
                    stable_name = label.split('.')[0] if '.' in label else label
                    return stable_name

            finally:
                # Clean up temp file
                tmp_path.unlink(missing_ok=True)

        except Exception as e:
            # If extraction fails, fall back to filename
            # This handles files that don't have \rSec tags or conversion errors
            pass

        # Fallback: use filename stem
        return tex_file.stem

    def build_full_standard(
        self,
        converter,
        output_file: Path,
        verbose: bool = False,
        toc_depth: int = 1
    ) -> Tuple[str, List[str]]:
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
            if chapter in ['front', 'back']:
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
                    standalone=False,   # Don't include standalone wrappers
                    verbose=False
                )

                # Extract link definitions and content separately
                content, references = self._split_content_and_references(markdown)
                all_content_parts.append(content)
                all_references.update(references)

                converted_chapters.append(chapter)

            except Exception as e:
                if verbose:
                    print(f"Error converting {chapter}.tex: {e}")
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
        output_file.write_text(full_content, encoding='utf-8')

        # Cleanup temporary files
        for temp_file in temp_files:
            try:
                temp_file.unlink()
            except Exception:
                pass  # Ignore cleanup errors

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
            r'^(#{1,6})\s+(.+?)\s+<a id="([^"]+)">\[\[([^\]]+)\]\]</a>\s*$',
            re.MULTILINE
        )

        # Track section numbers at each level
        section_numbers = [0, 0, 0, 0, 0, 0]  # Support up to H6

        for match in heading_pattern.finditer(markdown_content):
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
            section_num = '.'.join(
                str(section_numbers[i])
                for i in range(level + 1)
            )

            # Create TOC entry with indentation
            indent = '  ' * level
            list_marker = "- "
            toc_entry = f"{indent}{list_marker}{section_num} {title} [[{stable_name}]](#{stable_name})"
            toc_lines.append(toc_entry)

        return '\n'.join(toc_lines)

    def _split_content_and_references(self, markdown: str) -> Tuple[str, dict]:
        """
        Split markdown into content and link reference definitions.

        Returns:
            Tuple of (content, dict of references)
        """
        lines = markdown.split('\n')
        content_lines = []
        references = {}
        in_references = False

        for line in lines:
            if '<!-- Link reference definitions -->' in line:
                in_references = True
                continue

            if in_references:
                # Match [ref]: #ref pattern
                match = re.match(r'\[([^\]]+)\]:\s*#\1', line)
                if match:
                    references[match.group(1)] = True
                    continue

            content_lines.append(line)

        return '\n'.join(content_lines).strip(), references

    def _generate_toc_for_separate_files(
        self,
        output_files: List[Path],
        max_depth: int = 1
    ) -> str:
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
            r'^(#{1,6})\s+(.+?)\s+<a id="([^"]+)">\[\[([^\]]+)\]\]</a>\s*$',
            re.MULTILINE
        )

        # Track section numbers at each level
        section_numbers = [0, 0, 0, 0, 0, 0]  # Support up to H6

        # Process files in order
        for md_file in output_files:
            content = md_file.read_text(encoding='utf-8')
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
                section_num = '.'.join(
                    str(section_numbers[i])
                    for i in range(level + 1)
                )

                # Create TOC entry with cross-file link
                indent = '  ' * level
                list_marker = "- "
                # Format: - section_num title [[stable_name]](filename.md#anchor)
                toc_entry = f"{indent}{list_marker}{section_num} {title} [[{stable_name}]]({filename}.md#{anchor_id})"
                toc_lines.append(toc_entry)

        return '\n'.join(toc_lines)

    def build_separate_chapters(
        self,
        converter,
        output_dir: Path,
        verbose: bool = False,
        toc_depth: int = 1,
    ) -> List[Path]:
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
        output_dir.mkdir(parents=True, exist_ok=True)

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

        # Build label index for cross-file references
        if verbose:
            print("\nBuilding label index for cross-file references...")

        from .label_indexer import LabelIndexer
        indexer = LabelIndexer(self.draft_dir)
        label_index = indexer.build_index(
            use_stable_names=True,
            stable_name_map=chapter_to_stable
        )

        # Write Lua table file
        label_index_file = output_dir / "cpp_std_labels.lua"
        indexer.write_lua_table(label_index_file)

        if verbose:
            stats = indexer.get_statistics()
            print(f"Indexed {stats['labels']} labels across {stats['files']} files")
            if stats['duplicates'] > 0:
                print(f"Warning: Found {stats['duplicates']} duplicate labels")

        for i, chapter in enumerate(chapters, 1):
            chapter_file = self.draft_dir / f"{chapter}.tex"

            if not chapter_file.exists():
                if verbose:
                    print(f"Warning: {chapter}.tex not found, skipping")
                continue

            # Get stable name for this chapter
            stable_name = chapter_to_stable.get(chapter, chapter)

            if verbose:
                print(f"[{i}/{len(chapters)}] Converting {chapter}.tex...")

            # Expand \input{} commands for chapters that use them
            file_to_convert = chapter_file
            if chapter in ['front', 'back']:
                try:
                    file_to_convert = self._expand_input_commands(chapter_file)
                    temp_files.append(file_to_convert)
                except Exception as e:
                    if verbose:
                        print(f"Warning: Could not expand inputs in {chapter}.tex: {e}")

            # Convert chapter to markdown using stable name for output
            output_file = output_dir / f"{stable_name}.md"
            try:
                converter.convert_file(
                    file_to_convert,
                    output_file=output_file,
                    standalone=True,
                    verbose=False,
                    current_file_stem=stable_name,
                    label_index_file=label_index_file,
                )
                output_files.append(output_file)

            except Exception as e:
                if verbose:
                    print(f"Error converting {chapter}.tex: {e}")
                continue

        # Note: Cross-file links are now handled during conversion via label indexing
        # The old post-processing approach (fix_cross_file_links) is no longer needed

        # Generate TOC and append to front.md (or its stable name equivalent)
        front_stable_name = chapter_to_stable.get('front', 'front')
        front_file = output_dir / f"{front_stable_name}.md"
        if front_file.exists() and output_files:
            if verbose:
                print("\nGenerating table of contents...")

            toc = self._generate_toc_for_separate_files(output_files, max_depth=toc_depth)

            # Append TOC to front.md
            front_content = front_file.read_text(encoding='utf-8')

            # Add separator and TOC
            updated_front = front_content + "\n\n---\n\n" + toc
            front_file.write_text(updated_front, encoding='utf-8')

            if verbose:
                print(f"Added table of contents to front.md")

        # Cleanup temporary files
        for temp_file in temp_files:
            try:
                temp_file.unlink()
            except Exception:
                pass  # Ignore cleanup errors

        if verbose:
            print(f"\nWrote {len(output_files)} chapter files to {output_dir}")

        return output_files
