"""
Stable name extraction for C++ standard chapters.

The C++ standard uses 'stable names' - shortened chapter identifiers that
remain consistent across versions (e.g., expressions.tex uses stable name 'expr').
"""

import re
from pathlib import Path


def extract_stable_name_from_tex(tex_file: Path) -> str | None:
    """
    Extract stable name from a .tex file.

    The stable name is defined using \\renewcommand{\\stablenamestart}{name}
    in the LaTeX source.

    Args:
        tex_file: Path to .tex file

    Returns:
        Stable name if found, otherwise None
    """
    try:
        content = tex_file.read_text(encoding='utf-8', errors='ignore')

        # Look for \renewcommand{\stablenamestart}{name}
        match = re.search(r'\\renewcommand\{\\stablenamestart\}\{([^}]+)\}', content)
        if match:
            return match.group(1)

        # Fallback: use filename stem
        return None

    except Exception:
        return None
