#!/usr/bin/env python3
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
C++ Standard LaTeX to Markdown Converter

Converts C++ draft standard LaTeX sources to GitHub Flavored Markdown
using Pandoc with custom Lua filters.
"""

import contextlib
import re
import sys
from pathlib import Path

import click

from .label_indexer import LabelIndexer
from .repo_manager import DraftRepoManager, RepoManagerError
from .stable_name import extract_stable_name_from_tex
from .standard_builder import StandardBuilder
from .utils import SKIP_FILES, CommandError, ensure_dir, run_command, temp_tex_file


def unescape_wikilinks(markdown: str) -> str:
    r"""
    Unescape wikilinks that Pandoc's markdown writer escaped.

    Pandoc escapes square brackets in certain contexts to prevent ambiguity:
    - [[ref]] inside bold/emphasis becomes \[\[ref\]\]
    - [*Note* at start of line becomes \[*Note*

    This function reverses that escaping for our wikilink syntax.

    Args:
        markdown: The markdown text with escaped wikilinks

    Returns:
        Markdown with unescaped wikilinks
    """
    # Unescape wikilink patterns: \[\[ref\]\] → [[ref]]
    # This handles references that were escaped when inside bold/emphasis
    markdown = re.sub(r"\\\[\\\[([^\]]+)\\\]\\\]", r"[[\1]]", markdown)

    # Unescape opening brackets at start of notes/examples: \[*Note* → [*Note*
    # This handles the pattern where Pandoc escapes [ at line start
    markdown = re.sub(r"^\\\[\*", r"[*", markdown, flags=re.MULTILINE)
    markdown = re.sub(r"^\\\[\*\*", r"[**", markdown, flags=re.MULTILINE)

    # Unescape closing brackets after emphasis in notes/examples: *end note*\] → *end note*]
    # Pandoc escapes ] after emphasis to avoid ambiguity with link syntax
    markdown = re.sub(r"\*\\\]", r"*]", markdown)

    # Fix spacing after opening parenthesis: ( [[ → ([[
    # This improves readability for patterns like ( [[tag]]) -> ([[tag]])
    markdown = re.sub(r"\( \[\[", r"([[", markdown)

    # These macros appear in table cells where Pandoc processes them before our filters run
    markdown = re.sub(r"\\libmember\{([^}]+)\}\{[^}]+\}", r"\1", markdown)
    markdown = re.sub(r"\\libglobal\{([^}]+)\}", r"\1", markdown)

    return markdown


class ConverterError(Exception):
    """Base exception for converter errors"""

    pass


def _handle_repo_error(func):
    """Decorator to handle RepoManagerError with consistent error reporting.

    Catches RepoManagerError, displays error message to stderr, and exits with code 1.

    Args:
        func: Function to wrap with error handling

    Returns:
        Wrapped function with repo error handling
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RepoManagerError as e:
            click.echo(f"Repository error: {e}", err=True)
            sys.exit(1)

    return wrapper


def _require_output(output: Path | None, context: str) -> Path:
    """Ensure output path is provided, exit with error if not.

    Args:
        output: Optional output path
        context: Description of the context (e.g., "--build-full", "directory conversion")

    Returns:
        The output Path

    Raises:
        SystemExit: If output is None
    """
    if not output:
        click.echo(f"Error: --output required for {context}", err=True)
        sys.exit(1)
    return output


def _ensure_repo_ready(repo_manager: DraftRepoManager, git_ref: str | None, verbose: bool) -> None:
    """Ensure repository exists and checkout specified ref if provided.

    Args:
        repo_manager: Repository manager instance
        git_ref: Git reference to checkout (optional)
        verbose: Print verbose output

    Raises:
        RepoManagerError: If repository operations fail
    """
    if not repo_manager.exists():
        click.echo("Cloning C++ draft repository...", err=True)
        repo_manager.clone(shallow=False)

    if git_ref:
        repo_manager.checkout(git_ref)

    if verbose and git_ref:
        ref_info = repo_manager.get_current_ref()
        click.echo(
            f"Using version: {ref_info['ref']} ({ref_info['short_sha']})",
            err=True,
        )


def _handle_list_tags(draft_repo: Path | None) -> None:
    """Handle --list-tags option to display available C++ standard versions."""
    repo_manager = DraftRepoManager(draft_repo)
    if not repo_manager.exists():
        click.echo("Cloning C++ draft repository...", err=True)
        repo_manager.clone(shallow=False)

    click.echo("Available C++ standard version tags:", err=True)
    tags = repo_manager.get_tags()
    for tag in tags:
        click.echo(f"  {tag}")


@_handle_repo_error
def _handle_build_full(
    draft_repo: Path | None,
    git_ref: str | None,
    output: Path | None,
    filters_dir: Path | None,
    verbose: bool,
    toc_depth: int,
) -> None:
    """Handle --build-full option to build concatenated full standard."""
    repo_manager = DraftRepoManager(draft_repo)
    _ensure_repo_ready(repo_manager, git_ref, verbose)
    output = _require_output(output, "--build-full")

    output_file = Path(output)
    builder = StandardBuilder(repo_manager.source_dir)
    converter = Converter(filters_dir=filters_dir)

    click.echo("Building full standard from std.tex...", err=True)
    try:
        content, chapters = builder.build_full_standard(
            converter, output_file, verbose=verbose, toc_depth=toc_depth
        )
        click.echo(f"\nSuccessfully built full standard to {output_file}", err=True)
        click.echo(f"Converted {len(chapters)} chapters", err=True)
    except Exception as e:
        click.echo(f"Error building full standard: {e}", err=True)
        sys.exit(1)


@_handle_repo_error
def _handle_build_separate(
    draft_repo: Path | None,
    git_ref: str | None,
    output: Path | None,
    filters_dir: Path | None,
    verbose: bool,
    toc_depth: int,
) -> None:
    """Handle --build-separate option to build separate chapter files."""
    repo_manager = DraftRepoManager(draft_repo)
    _ensure_repo_ready(repo_manager, git_ref, verbose)
    output = _require_output(output, "--build-separate")

    output_dir = Path(output)
    builder = StandardBuilder(repo_manager.source_dir)
    converter = Converter(filters_dir=filters_dir)

    click.echo("Building separate chapter files from std.tex...", err=True)
    try:
        output_files = builder.build_separate_chapters(
            converter,
            output_dir,
            verbose=verbose,
            toc_depth=toc_depth,
        )
        click.echo(
            f"\nSuccessfully built {len(output_files)} chapter files to {output_dir}",
            err=True,
        )
    except Exception as e:
        click.echo(f"Error building separate chapters: {e}", err=True)
        sys.exit(1)


def _handle_file_conversion(
    converter: "Converter", input_path: Path, output: Path | None, standalone: bool, verbose: bool
) -> None:
    """Handle single file conversion."""
    result = converter.convert_file(
        input_path,
        output_file=output,
        standalone=standalone,
        verbose=verbose,
    )

    if not output:
        # Print to stdout
        click.echo(result)


def _handle_directory_conversion(
    converter: "Converter", input_path: Path, output: Path | None, verbose: bool
) -> None:
    """Handle directory conversion."""
    output = _require_output(output, "directory conversion")

    output_files = converter.convert_directory(
        input_path,
        output,
        verbose=verbose,
    )

    click.echo(f"\nConverted {len(output_files)} files", err=True)


class Converter:
    """Main converter class that wraps Pandoc with custom filters"""

    def __init__(self, filters_dir: Path | None = None):
        """
        Initialize converter

        Args:
            filters_dir: Directory containing Lua filters. If None, uses default.
        """
        if filters_dir is None:
            # Always use source directory filters (package is never installed)
            # Filters are at src/cpp_std_converter/filters/ relative to this file
            filters_dir = Path(__file__).parent / "filters"

        self.filters_dir = Path(filters_dir)

        # Verify filters exist
        # Order matters: sections → itemdecl/itemdescr → code blocks → definitions → notes/examples → lists (early) → macros → math → grammar → tables → strip-metadata (LAST)
        # cpp-lists runs early to merge multi-block list items before macro/grammar processing
        # strip-metadata runs LAST to remove YAML front matter from output (after all filters that need metadata)
        self.filters = [
            self.filters_dir / "cpp-sections.lua",
            self.filters_dir / "cpp-itemdecl.lua",
            self.filters_dir / "cpp-code-blocks.lua",
            self.filters_dir / "cpp-definitions.lua",
            self.filters_dir / "cpp-notes-examples.lua",
            self.filters_dir / "cpp-lists.lua",
            self.filters_dir / "cpp-macros.lua",
            self.filters_dir / "cpp-math.lua",
            self.filters_dir / "cpp-grammar.lua",
            self.filters_dir / "cpp-tables.lua",
            self.filters_dir
            / "cpp-notes-examples.lua",  # Second pass: catch notes from cpp-macros.lua's pandoc.read()
            self.filters_dir / "strip-metadata.lua",  # Must be LAST
        ]

        for filter_path in self.filters:
            if not filter_path.exists():
                raise ConverterError(f"Filter not found: {filter_path}")

    def convert_file(
        self,
        input_file: Path,
        output_file: Path | None = None,
        standalone: bool = True,
        verbose: bool = False,
        current_file_stem: str | None = None,
        label_index_file: Path | None = None,
    ) -> str:
        """
        Convert a single LaTeX file to Markdown

        Args:
            input_file: Path to input .tex file
            output_file: Path to output .md file (if None, returns as string)
            standalone: Whether to produce a standalone document
            verbose: Print verbose output
            current_file_stem: Current file's stem for cross-ref detection
            label_index_file: Path to Lua label index file

        Returns:
            Markdown content as string

        Raises:
            ConverterError: If conversion fails
        """
        input_file = Path(input_file)

        if not input_file.exists():
            raise ConverterError(f"Input file not found: {input_file}")

        # Preprocessing: inject simplified macro definitions for Pandoc
        # This allows Pandoc to expand common macros natively, reducing Lua filter complexity
        macros_file = self.filters_dir / "simplified_macros.tex"

        # Read input content
        input_content = input_file.read_text(encoding="utf-8")

        # Fix n3337-specific LaTeX syntax errors before processing
        # Issue: n3337 has `[\textit{Example}` instead of `\enterexample`
        # This confuses Pandoc's LaTeX parser (different from filter issues)
        input_content = re.sub(r"\[\\textit\{Example\}", r"\\enterexample", input_content)

        # Combine with macro definitions if available
        if macros_file.exists():
            macros_content = macros_file.read_text(encoding="utf-8")
            combined_content = macros_content + "\n\n" + input_content
        else:
            combined_content = input_content

        # Use temp file context manager for conversion
        with temp_tex_file(combined_content) as file_to_convert:
            # Build pandoc command
            cmd = [
                "pandoc",
                str(file_to_convert),
                "--from=latex+raw_tex",
                "--to=gfm",
            ]

            # Pass metadata to Lua filters for cross-file linking
            if current_file_stem:
                cmd.append(f"--metadata=current_file:{current_file_stem}")
            if label_index_file:
                cmd.append(f"--metadata=label_index_file:{label_index_file}")

            # Pass source directory for dynamic config loading
            source_dir = input_file.parent
            cmd.append(f"--metadata=source_dir:{source_dir}")

            # Add filters in order
            for filter_path in self.filters:
                cmd.append(f"--lua-filter={filter_path}")

            if standalone:
                cmd.append("--standalone")

            if output_file:
                cmd.extend(["-o", str(output_file)])

            if verbose:
                click.echo(f"Running: {' '.join(cmd)}", err=True)

            try:
                # Run pandoc
                result = run_command(cmd)

                # Post-process: unescape wikilinks that Pandoc escaped
                if output_file:
                    # Read generated markdown, unescape, and write back
                    markdown = output_file.read_text()
                    markdown = unescape_wikilinks(markdown)
                    output_file.write_text(markdown)
                    click.echo(f"Converted: {input_file} -> {output_file}", err=True)
                    return markdown
                else:
                    # Unescape stdout before returning
                    markdown = result.stdout
                    return unescape_wikilinks(markdown)

            except CommandError as e:
                raise ConverterError(f"Pandoc conversion failed:\n{e}") from e

    def convert_directory(
        self,
        input_dir: Path,
        output_dir: Path,
        pattern: str = "*.tex",
        verbose: bool = False,
        fix_cross_file_links: bool = True,
    ) -> list[Path]:
        """
        Convert all .tex files in a directory

        Args:
            input_dir: Directory containing .tex files
            output_dir: Directory for output .md files
            pattern: Glob pattern for input files
            verbose: Print verbose output
            fix_cross_file_links: Fix cross-file reference links (default: True)

        Returns:
            List of output file paths

        Raises:
            ConverterError: If conversion fails
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)

        if not input_dir.exists():
            raise ConverterError(f"Input directory not found: {input_dir}")

        # Create output directory
        ensure_dir(output_dir)

        # Build label index for cross-file references
        label_index_file = None
        if fix_cross_file_links:
            if verbose:
                click.echo("Building label index for cross-file references...", err=True)

            indexer = LabelIndexer(input_dir)
            indexer.build_index(use_stable_names=True)

            # Write Lua table file
            label_index_file = output_dir / "cpp_std_labels.lua"
            indexer.write_lua_table(label_index_file)

            if verbose:
                stats = indexer.get_statistics()
                click.echo(
                    f"Indexed {stats['labels']} labels across {stats['files']} files", err=True
                )
                if stats["duplicates"] > 0:
                    click.echo(f"Warning: Found {stats['duplicates']} duplicate labels", err=True)

        # Find all .tex files
        tex_files = sorted(input_dir.glob(pattern))

        if not tex_files:
            raise ConverterError(f"No files matching '{pattern}' found in {input_dir}")

        output_files = []

        for tex_file in tex_files:
            # Skip common non-chapter files
            if tex_file.stem in SKIP_FILES:
                if verbose:
                    click.echo(f"Skipping: {tex_file.name}", err=True)
                continue

            output_file = output_dir / f"{tex_file.stem}.md"

            # Extract stable name for this file (e.g., "mem" from memory.tex)
            # This is used for cross-file link resolution
            stable_name = None
            with contextlib.suppress(Exception):
                stable_name = extract_stable_name_from_tex(tex_file)

            try:
                self.convert_file(
                    tex_file,
                    output_file,
                    standalone=True,
                    verbose=verbose,
                    current_file_stem=stable_name or tex_file.stem,
                    label_index_file=label_index_file,
                )
                output_files.append(output_file)
            except ConverterError as e:
                click.echo(f"Error converting {tex_file}: {e}", err=True)
                if not verbose:
                    click.echo("Use --verbose to see detailed errors", err=True)

        # Fix cross-file links if requested
        if fix_cross_file_links and output_files:
            stats = self.fix_cross_file_links(output_files, verbose=verbose)
            if verbose and stats["links_updated"] > 0:
                click.echo(
                    f"Fixed {stats['links_updated']} cross-file links in {stats['files_updated']} files",
                    err=True,
                )

        return output_files

    def fix_cross_file_links(
        self,
        output_files: list[Path],
        verbose: bool = False,
    ) -> dict[str, int]:
        """
        Fix cross-file reference links in separately-converted markdown files.

        When converting multiple .tex files to separate .md files, cross-references
        need to point to the correct file. This scans all files to build a mapping
        of labels to files, then updates link definitions accordingly.

        Link definitions in the same file remain unchanged as [label]: #label
        Cross-file references are updated to [label]: filename.md#label

        Args:
            output_files: List of .md files to process
            verbose: Print verbose output

        Returns:
            Dict with statistics: {'files_updated': N, 'links_updated': N}
        """
        if not output_files:
            return {"files_updated": 0, "links_updated": 0}

        if verbose:
            click.echo("Building label-to-file mapping...", err=True)

        # Step 1: Build label-to-file mapping by scanning for <a id="label"> anchors
        label_to_file = {}
        for md_file in output_files:
            content = md_file.read_text(encoding="utf-8")
            # Find all HTML anchors: <a id="label">
            for match in re.finditer(r'<a id="([^"]+)">', content):
                label = match.group(1)
                label_to_file[label] = md_file.stem  # Store filename without extension

        if verbose:
            click.echo(
                f"Found {len(label_to_file)} labels across {len(output_files)} files", err=True
            )
            click.echo("Updating cross-file link definitions...", err=True)

        # Step 2: Update link definitions in each file
        stats = {"files_updated": 0, "links_updated": 0}

        for md_file in output_files:
            content = md_file.read_text(encoding="utf-8")
            updated_content = content
            file_updated = False

            # Find all link definitions: [label]: #label
            # Use re.finditer to find all matches, then replace them
            matches = list(re.finditer(r"\[([^\]]+)\]: #\1\b", content))

            for match in matches:
                label = match.group(1)

                # Check if label exists and is in a different file
                if label in label_to_file:
                    target_file = label_to_file[label]

                    if target_file != md_file.stem:
                        # Cross-file reference - update to relative path
                        old_def = f"[{label}]: #{label}"
                        new_def = f"[{label}]: {target_file}.md#{label}"

                        # Replace this specific occurrence
                        updated_content = updated_content.replace(old_def, new_def, 1)

                        stats["links_updated"] += 1
                        file_updated = True

                        if verbose:
                            click.echo(
                                f"  {md_file.name}: [{label}] -> {target_file}.md#{label}", err=True
                            )

            # Write back if updated
            if file_updated:
                md_file.write_text(updated_content, encoding="utf-8")
                stats["files_updated"] += 1

        if verbose:
            click.echo(
                f"Updated {stats['links_updated']} cross-file links in {stats['files_updated']} files",
                err=True,
            )

        return stats


@click.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path), required=False)
@click.option("-o", "--output", type=click.Path(path_type=Path), help="Output file or directory")
@click.option(
    "--standalone/--no-standalone", default=True, help="Produce standalone document (default: yes)"
)
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.option(
    "--filters-dir",
    type=click.Path(exists=True, path_type=Path),
    help="Directory containing Lua filters",
)
@click.option(
    "--git-ref", type=str, help="Git reference (tag, branch, or SHA) to checkout before conversion"
)
@click.option(
    "--draft-repo",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to cplusplus/draft repository (default: ~/cplusplus-draft)",
)
@click.option("--list-tags", is_flag=True, help="List available C++ standard version tags and exit")
@click.option(
    "--build-full",
    is_flag=True,
    help="Build full standard from std.tex driver file (concatenates all chapters)",
)
@click.option(
    "--build-separate",
    is_flag=True,
    help="Build separate markdown files for each chapter with cross-file linking",
)
@click.option(
    "--toc-depth",
    type=int,
    default=3,
    help="Maximum heading depth for table of contents (1=H1 only, 2=H1+H2, etc. Default: 3)",
)
def main(
    input_path: Path | None,
    output: Path | None,
    standalone: bool,
    verbose: bool,
    filters_dir: Path | None,
    git_ref: str | None,
    draft_repo: Path,
    list_tags: bool,
    build_full: bool,
    build_separate: bool,
    toc_depth: int,
):
    """
    Convert C++ standard LaTeX files to Markdown.

    INPUT_PATH can be a single .tex file or a directory containing .tex files.

    When converting a directory, cross-chapter references are automatically detected
    and converted to relative links (e.g., [forward] in concepts.md links to
    utilities.md#forward). This enables proper navigation in separately-converted
    markdown files hosted on GitHub/GitLab.

    Examples:

        # Convert single file to stdout
        ./convert.py intro.tex

        # Convert single file to output file
        ./convert.py intro.tex -o intro.md

        # Convert all .tex files in directory (with automatic cross-file linking)
        ./convert.py /path/to/source -o /path/to/output

        # Convert specific C++ standard version
        ./convert.py ~/cplusplus-draft/source/intro.tex --git-ref n4950

        # Build full standard from std.tex (all chapters concatenated)
        ./convert.py --build-full -o full_standard.md --git-ref n4950

        # Build separate markdown files for each chapter with cross-file linking
        ./convert.py --build-separate -o output_dir/ --git-ref n4950

        # List available version tags
        ./convert.py --list-tags
    """
    try:
        # Handle --list-tags option
        if list_tags:
            _handle_list_tags(draft_repo)
            return

        # Handle --build-full option
        if build_full:
            _handle_build_full(draft_repo, git_ref, output, filters_dir, verbose, toc_depth)
            return

        # Handle --build-separate option
        if build_separate:
            _handle_build_separate(draft_repo, git_ref, output, filters_dir, verbose, toc_depth)
            return

        # INPUT_PATH is required if not using special build modes
        if not input_path:
            click.echo(
                "Error: INPUT_PATH required (unless using --list-tags, --build-full, or --build-separate)",
                err=True,
            )
            sys.exit(1)

        # Handle git ref checkout if specified
        if git_ref:
            repo_manager = DraftRepoManager(draft_repo)
            _handle_repo_error(lambda: repo_manager.ensure_ready(ref=git_ref, shallow=False))()
            if verbose:
                ref_info = repo_manager.get_current_ref()
                click.echo(
                    f"Using draft version: {ref_info['ref']} ({ref_info['short_sha']})",
                    err=True,
                )

        # Create converter instance
        converter = Converter(filters_dir=filters_dir)

        # Handle file or directory conversion
        if input_path.is_file():
            _handle_file_conversion(converter, input_path, output, standalone, verbose)
        elif input_path.is_dir():
            _handle_directory_conversion(converter, input_path, output, verbose)
        else:
            click.echo(f"Error: Invalid input path: {input_path}", err=True)
            sys.exit(1)

    except ConverterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
