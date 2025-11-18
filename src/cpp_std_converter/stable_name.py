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
        content = tex_file.read_text(encoding="utf-8", errors="ignore")

        match = re.search(r"\\renewcommand\{\\stablenamestart\}\{([^}]+)\}", content)
        if match:
            return match.group(1)

        return None

    except (OSError, UnicodeDecodeError):
        return None
