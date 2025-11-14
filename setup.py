"""Minimal setup.py for development and testing.

This setup.py is used for:
1. Installing dependencies from requirements.txt via `pip install -e .`
2. Making the package importable for tests
3. Including Lua filters as package data

User-facing scripts are in the root directory and can be run directly:
- convert.py - LaTeX to Markdown converter
- generate_diffs.py - Diff generator
- generate_html_site.py - HTML site generator
"""

from setuptools import find_packages, setup

with open("requirements.txt", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cpp-std-converter",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=requirements,
    package_data={
        "cpp_std_converter": ["filters/*.lua"],
    },
)
