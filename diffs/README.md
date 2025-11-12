# C++ Standard Evolution Diffs

This directory contains comprehensive diffs between different versions of the C++ standard, generated from the official cplusplus/draft repository.

## Overview

Understanding how the C++ standard has evolved is crucial for:
- **Tracking feature introductions** - When did concepts appear? Ranges? Modules?
- **Understanding language changes** - How did class semantics evolve from C++11 to C++23?
- **Studying design decisions** - Why were certain features reorganized or merged?
- **Planning migrations** - What changed between the version you're using and the latest?

## Directory Structure

Each subdirectory represents a version pair (e.g., `n3337_to_n4950/` for C++11 → C++23):

```
n3337_to_n4950/
  README.md              # Summary with statistics and links
  class.diff             # Chapter-specific diffs
  expr.diff
  utilities.diff
  ...
  full_standard.diff     # Complete standard diff (large file)
```

## Available Version Pairs

| Directory | Description | Key Changes |
|-----------|-------------|-------------|
| `n3337_to_n4140` | C++11 → C++14 | Binary literals, generic lambdas, decltype(auto) |
| `n4140_to_n4659` | C++14 → C++17 | Structured bindings, if constexpr, fold expressions |
| `n4659_to_n4861` | C++17 → C++20 | Concepts, ranges, coroutines, modules |
| `n4861_to_n4950` | C++20 → C++23 | std::expected, ranges improvements, deducing this |
| `n4950_to_trunk` | C++23 → C++26 (WD) | Latest developments (working draft) |
| `n3337_to_n4950` | C++11 → C++23 | Complete evolution over 12 years |
| `n3337_to_trunk` | C++11 → C++26 (WD) | Full historical evolution |

## How to Use These Diffs

### Quick Navigation

1. **Start with the summary** - Each directory's `README.md` provides:
   - New chapters added (new language features)
   - Removed chapters (restructuring)
   - Chapter-by-chapter statistics (size changes, line counts)
   - Links to individual chapter diffs

2. **Focus on specific topics** - Click chapter links to see detailed changes:
   - `class.diff` - How class definitions and semantics evolved
   - `containers.diff` - New containers and container features
   - `expr.diff` - New expression types and evaluation rules
   - `utilities.diff` - Library utilities like std::optional, std::variant

3. **Study major features** - Look at new chapters:
   - `concepts.md` - Appeared in C++20
   - `ranges.md` - Appeared in C++20
   - `module.md` - Appeared in C++20

### Viewing on GitHub

**Per-chapter diffs render well** (all under 512 KB except a few):
- Navigate to any `.diff` file and GitHub will display it with syntax highlighting
- Use GitHub's diff view controls to jump between changes
- Example: `diffs/n3337_to_n4950/class.diff`

**Full standard diffs don't render** (too large, 5-9 MB):
- Download and view locally with a diff viewer
- Use `less` or `vim` for terminal viewing
- Example: `less diffs/n3337_to_n4950/full_standard.diff`

### Command-Line Viewing

```bash
# View specific chapter diff
less diffs/n3337_to_n4950/class.diff

# Side-by-side comparison
diff -y n3337/class.md n4950/class.md | less

# Search for specific changes
grep "concept" diffs/n3337_to_n4950/*.diff

# Word-level diff for better readability
git diff --no-index --word-diff n3337/class.md n4950/class.md
```

## Key Insights from the Diffs

### C++11 → C++23 Evolution

**Language grew 90%:** From 3.3 MB to 6.2 MB total content

**Biggest chapter expansions:**
- `containers.md`: +153% (215 KB → 544 KB) - New containers, views, ranges adaptors
- `algorithms.md`: +294% (103 KB → 405 KB) - Ranges algorithms
- `class.md`: +93% (95 KB → 184 KB) - Expanded semantics

**New major features (new chapters):**
- Concepts library (`concepts.md`) - C++20
- Ranges library (`ranges.md`) - C++20
- Modules (`module.md`) - C++20
- Time library (`time.md`) - C++20
- Memory management (`mem.md`) - Reorganized

**Removed/merged chapters:**
- `atomics.md` → Merged into `thread.md`
- `special.md` → Merged into `class.md`
- `language.md` → Reorganized into `support.md`

## Generating Fresh Diffs

To regenerate all diffs (e.g., after updating standards):

```bash
# From project root
./generate_diffs.py

# Or for specific version pair
./generate_diffs.py n4950 trunk
```

## Technical Details

**Diff Format:** Unified diff format (git diff style)
- Lines removed: Prefixed with `-`
- Lines added: Prefixed with `+`
- Context lines: No prefix (for orientation)

**Generation:**
- Per-chapter diffs: `git diff --no-index --unified=3`
- Full diffs: Concatenated chapters then diff
- Statistics: File size, line counts, percentage changes

**Requirements:**
- Separate chapter files (built by `./setup-and-build.sh`)
- Full standard files (`full/*.md`, also built by `./setup-and-build.sh`)

## Contributing

Found an interesting pattern in the diffs? Add it to this README!

**Good additions:**
- Notable feature introductions with line references
- Interesting refactorings or reorganizations
- Migration guides derived from diff analysis
- Tools or scripts for analyzing diff data

## See Also

- [CLAUDE.md](../CLAUDE.md#generating-diffs-between-standard-versions) - Detailed usage guide
- [generate_diffs.py](../generate_diffs.py) - Diff generation script
- [setup-and-build.sh](../setup-and-build.sh) - Builds all required files
