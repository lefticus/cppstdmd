#!/usr/bin/env python3
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
