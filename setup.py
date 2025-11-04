from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cpp-std-converter",
    version="0.1.0",
    author="Jason Turner",
    description="Convert C++ draft standard LaTeX to Markdown using Pandoc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cpp-standard-tools",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cpp-std-convert=cpp_std_converter.converter:main",
        ],
    },
    package_data={
        "cpp_std_converter": ["filters/*.lua"],
    },
)
