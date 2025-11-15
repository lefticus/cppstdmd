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

"""Wrapper for LaTeX to Markdown converter - runs without installation.

This script provides a direct entry point to the C++ standard LaTeX to Markdown
converter without requiring pip installation. It automatically adds the src/
directory to the Python path to enable imports.

Usage:
    ./convert.py intro.tex -o intro.md
    ./convert.py --build-separate -o n4950/ --git-ref n4950
    ./convert.py --build-full -o full.md --git-ref n4950
    ./convert.py --list-tags
"""
import sys
from pathlib import Path

# Add src to path so imports work without installation
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cpp_std_converter.converter import main

if __name__ == "__main__":
    sys.exit(main())
