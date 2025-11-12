# C++ Standard Evolution Interactive Viewer - Implementation Plan

**Date**: 2025-11-12
**Status**: Ready for Implementation
**Repository**: cpp_standard_tools/converted/cppstdmd
**Deployment**: gh-pages branch of this repository

---

## Executive Summary

This document contains the complete research and implementation plan for creating an interactive, educational C++ standard evolution viewer using diff2html and GitHub Pages.

**Goal**: Enable developers to easily explore how the C++ standard evolved across versions by viewing focused, side-by-side diffs of individual stable name sections (e.g., `[array]`, `[class.copy]`, `[ranges.adaptors]`).

**Scope**: Focus on **5 adjacent version pairs** (C++11→14, C++14→17, C++17→20, C++20→23, C++23→26) with **Tier 1 stable names** (~572 per version: 0-dot and 1-dot depth).

**Deliverable**: ~2,860 static HTML pages (~435MB total) deployed to the `gh-pages` branch of this repository.

**Timeline**: 6-8 weeks MVP, ~60 hours total effort

---

## Table of Contents

1. [Data Analysis](#data-analysis)
2. [Architecture Design](#architecture-design)
3. [Implementation Steps](#implementation-steps)
4. [Technical Specifications](#technical-specifications)
5. [Code Examples](#code-examples)
6. [Deployment Guide](#deployment-guide)
7. [Future Enhancements](#future-enhancements)

---

## Data Analysis

### Dataset Overview

We have generated 41,575 stable name diff files across 15 version pairs. For the interactive viewer, we focus on **5 adjacent pairs**:

| Version Pair | Total Diffs | Tier 1 Estimate | Size |
|--------------|-------------|-----------------|------|
| n3337 → n4140 (C++11→14) | 862 | ~150 | 6.2 MB |
| n4140 → n4659 (C++14→17) | 1,957 | ~400 | 20 MB |
| n4659 → n4861 (C++17→20) | 2,650 | ~550 | 24 MB |
| n4861 → n4950 (C++20→23) | 2,478 | ~500 | 23 MB |
| n4950 → trunk (C++23→26) | 2,421 | ~480 | 24 MB |
| **Total** | **10,368** | **~2,080** | **~97 MB** |

### Stable Name Hierarchy

Analysis of stable name depth (based on dot count):

- **0 dots (top-level)**: ~122 names (5%) - Examples: `array`, `vector`, `algorithms`, `class`, `thread`
- **1 dot**: ~450 names (40%) - Examples: `array.cons`, `vector.modifiers`, `class.copy`, `ranges.adaptors`
- **2 dots**: ~987 names (40%) - Examples: `alg.binary.search`, `container.requirements.general`
- **3+ dots**: ~374 names (15%) - Examples: `class.copy.ctor`, `basic.lookup.qual.general`

### Tier 1 Definition

**Tier 1 (Featured)**: Stable names with 0-1 dots (~572 per version)
- **Rationale**: These represent major library components and chapter sections that developers care about
- **Coverage**: ~50% of all stable names, ~80% of educational value
- **Examples**: `array`, `vector`, `class.copy`, `ranges.adaptors`, `concepts.callable`, `thread.mutex`

**Tier 2 (Advanced)**: Remaining stable names with 2+ dots (~1,900 per version)
- **Rationale**: Too granular for browsing, can be added later or accessed via search
- **Examples**: `class.conv.ctor.general`, `basic.stc.dynamic.allocation.general`

### File Size Distribution

- **Most diffs**: 1-50 KB (excellent for browser rendering)
- **Large diffs**: 23 files >100 KB per adjacent pair
- **Largest diffs** (n4861→n4950):
  - `utilities.diff`: 621 KB
  - `containers.diff`: 470 KB
  - `ranges.diff`: 432 KB (12,400 lines!)
  - `basic.diff`: 268 KB

**Mitigation**: Use lazy loading for diffs >100KB

---

## Architecture Design

### Approach: Hub-and-Spoke Multi-Page

**Structure**:
```
gh-pages branch:
├── index.html (landing page)
├── versions/
│   ├── cpp11-to-cpp14.html (version pair overview)
│   ├── cpp14-to-cpp17.html
│   ├── cpp17-to-cpp20.html
│   ├── cpp20-to-cpp23.html
│   └── cpp23-to-cpp26.html
├── diffs/
│   ├── cpp11-to-cpp14/
│   │   ├── array.html
│   │   ├── vector.html
│   │   └── ... (572 files)
│   ├── cpp14-to-cpp17/
│   │   └── ... (572 files)
│   └── ... (5 subdirectories)
├── css/
│   ├── diff2html.min.css
│   └── custom.css
└── js/
    ├── diff2html-ui.min.js
    └── navigation.js
```

**URL Structure**:
- Landing: `https://[username].github.io/cppstdmd/`
- Version overview: `https://[username].github.io/cppstdmd/versions/cpp20-to-cpp23.html`
- Diff viewer: `https://[username].github.io/cppstdmd/diffs/cpp20-to-cpp23/array.html`

### Why This Approach?

**Pros**:
- ✅ Clean URLs (SEO-friendly)
- ✅ Fast page loads (only load one diff at a time)
- ✅ Browser history works intuitively
- ✅ Works without JavaScript (progressive enhancement)
- ✅ Mobile-friendly
- ✅ Each page is indexable by search engines

**Cons**:
- More files to generate (~2,860 HTML pages)
- Requires some JavaScript for enhanced navigation

### Alternative Approaches Considered

1. **Single-Page App**: Instant navigation but requires JavaScript, poor SEO
2. **Jekyll/Hugo Static Site**: Adds build complexity, unnecessary for this use case
3. **Markdown Tables**: GitHub rendering limitations, no diff visualization
4. **Hybrid with Lazy Loading**: Best for large diffs, can add in Phase 2

**Verdict**: Hub-and-Spoke is optimal for educational use case

---

## Implementation Steps

### Phase 1: Generator Script (Weeks 1-2, ~20 hours)

**Objective**: Create `generate_html_site.py` to convert stable name diffs to interactive HTML pages

**Tasks**:
1. **Install dependencies**:
   ```bash
   npm install -g diff2html-cli
   pip install jinja2 beautifulsoup4
   ```

2. **Parse existing diffs**:
   - Read from `diffs/*/by_stable_name/`
   - Filter to Tier 1 (0-1 dot stable names)
   - Extract metadata (size, stable name, version pair)

3. **Generate HTML per diff**:
   - Use diff2html-cli: `diff2html -i file -F output.html --style side`
   - Post-process: Inject navigation, breadcrumbs, version timeline
   - For large diffs (>100KB): Add lazy-loading placeholder

4. **Create index and overview pages**:
   - Landing page: Grid of 5 version pairs
   - Version overview: Searchable list of all Tier 1 stable names
   - Include statistics, highlights, quick navigation

5. **Add cross-linking**:
   - External links: eel.is/c++draft, cppreference.com
   - Internal links: Previous/next version of same stable name
   - Related sections: Parent/child stable names

6. **Test on sample diffs**:
   - Generate HTML for 10 sample diffs (array, vector, class, etc.)
   - Verify rendering, links, navigation
   - Benchmark performance

### Phase 2: Templates & Design (Week 3, ~15 hours)

**Objective**: Create beautiful, responsive HTML templates

**Tasks**:
1. **Landing page design**:
   - Hero section: "Explore C++ Evolution"
   - Grid of 5 version pair cards with highlights
   - Quick navigation: Search, browse by category, statistics

2. **Version overview page**:
   - Breadcrumbs: Home > C++20→23
   - Search/filter input
   - Categorized list: Core Language, Library Components, etc.
   - Size indicators (small/medium/large change)

3. **Diff viewer page**:
   - Header: Breadcrumbs, version timeline, metadata
   - Body: Side-by-side diff (diff2html)
   - Sidebar: External links, related sections
   - Footer: Quick actions (copy link, download, view raw)

4. **Responsive CSS**:
   - Mobile: Stacked layout, hamburger menu
   - Tablet: Two-column with collapsible sidebar
   - Desktop: Three-column with fixed sidebar
   - Dark mode support (optional)

5. **Custom styling**:
   - Clean, educational aesthetic
   - Syntax highlighting
   - Smooth scrolling
   - Accessible (WCAG 2.1 AA)

### Phase 3: Content Generation (Week 4, ~10 hours)

**Objective**: Generate all Tier 1 HTML pages

**Tasks**:
1. **Run generator on all 5 adjacent pairs**:
   ```bash
   ./generate_html_site.py --tier 1 --output site/
   ```

2. **Generate ~2,860 HTML pages**:
   - 5 version pairs × 572 Tier 1 stable names = 2,860 pages
   - Estimated size: ~430MB (3x expansion from diff files)

3. **Validate output**:
   - Check all links work (no 404s)
   - Verify diffs render correctly
   - Test large diffs load properly
   - Validate HTML (W3C validator)

4. **Create site README**:
   - Explain project purpose
   - Link to source repository
   - Provide usage examples
   - Credit contributors

### Phase 4: Deployment (Week 5, ~8 hours)

**Objective**: Deploy to gh-pages branch of this repository

**Tasks**:
1. **Create gh-pages branch**:
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   # Add generated site files
   cp -r site/* .
   git add .
   git commit -m "Initial deployment of C++ Standard Evolution Viewer"
   git push origin gh-pages
   ```

2. **Configure GitHub Pages**:
   - Go to repository settings
   - Enable GitHub Pages from `gh-pages` branch
   - Add `.nojekyll` file (disable Jekyll processing)

3. **Test deployment**:
   - Visit `https://[username].github.io/cppstdmd/`
   - Test on multiple devices/browsers
   - Check page load times (<2s on 3G)

4. **Optional: Custom domain**:
   - Add CNAME file if using custom domain
   - Configure DNS records
   - Test HTTPS works

### Phase 5: Polish & Launch (Week 6, ~7 hours)

**Objective**: Add finishing touches and announce

**Tasks**:
1. **Implement search**:
   - Client-side search with Fuse.js
   - Fuzzy matching
   - Filter by version pair
   - Highlight results

2. **Add statistics page**:
   - Most changed sections
   - Growth over time (line count, size)
   - New features per version
   - Interactive charts (Chart.js)

3. **Enhance version timeline**:
   - Visual timeline for each stable name
   - "Jump to" dropdown
   - Keyboard shortcuts (j/k for next/prev)

4. **Launch announcement**:
   - Write blog post / README
   - Share on r/cpp, Twitter, Hacker News
   - Contact C++ Weekly (Jason Turner)
   - Submit to ISO C++ Foundation newsletter

**Total MVP: 6-8 weeks, ~60 hours**

---

## Technical Specifications

### Technology Stack

- **Generator**: Python 3.10+ with Jinja2 templates
- **Diff Rendering**: diff2html 3.x (latest stable)
- **Frontend**: Vanilla JavaScript (no framework)
- **Styling**: Custom CSS with CSS Grid/Flexbox
- **Deployment**: GitHub Pages (gh-pages branch)
- **CDN**: jsDelivr or unpkg for diff2html

### diff2html Configuration

**Recommended settings**:
```javascript
{
  outputFormat: 'side-by-side',
  matching: 'none',  // Performance: disable for large files
  drawFileList: false,
  highlight: true,
  renderNothingWhenEmpty: false,
  matchWordsThreshold: 0.25,
  maxLineSizeInBlockForComparison: 200
}
```

**For large diffs (>100KB)**:
```javascript
{
  matching: 'none',  // Critical for performance
  highlight: false,  // Disable syntax highlighting
  renderNothingWhenEmpty: true
}
```

### Performance Optimizations

1. **Lazy Loading**:
   ```html
   <!-- For large diffs -->
   <div id="diff-container" data-diff-url="/data/diffs/cpp20-23/ranges.diff">
     <button onclick="loadDiff()">Load Large Diff (432 KB)</button>
   </div>
   ```

2. **CDN Loading**:
   ```html
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/diff2html/bundles/css/diff2html.min.css">
   <script src="https://cdn.jsdelivr.net/npm/diff2html/bundles/js/diff2html-ui.min.js"></script>
   ```

3. **Compression**:
   - GitHub Pages automatically enables gzip/brotli
   - Minify CSS/JS
   - Optimize images (if any)

4. **Caching**:
   - Set appropriate Cache-Control headers (GitHub Pages handles this)
   - Service worker for offline access (optional)

### Cross-Linking Strategy

#### External Links

1. **eel.is/c++draft**: Link to current draft
   - Format: `https://eel.is/c++draft/array`
   - Always points to latest draft

2. **cppreference.com**: Link to practical documentation
   - Format: `https://en.cppreference.com/w/cpp/container/array`
   - Best for examples and usage

3. **open-std.org**: Link to official PDFs
   - Format: `https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/n4861.pdf`
   - For authoritative reference

4. **GitHub source**: Link back to markdown chapters
   - Format: `https://github.com/[username]/cppstdmd/blob/main/n4950/containers.md#array`
   - For full context

#### Internal Navigation

1. **Version Timeline**: Navigate same stable name across versions
   ```html
   <nav class="version-timeline">
     <a href="/diffs/cpp11-to-cpp14/array.html">C++11→14</a>
     <a href="/diffs/cpp14-to-cpp17/array.html">C++14→17</a>
     <a href="/diffs/cpp17-to-cpp20/array.html">C++17→20</a>
     <a href="/diffs/cpp20-to-cpp23/array.html" class="active">C++20→23</a>
     <a href="/diffs/cpp23-to-cpp26/array.html">C++23→26</a>
   </nav>
   ```

2. **Related Sections**: Link to parent/child stable names
   ```html
   <aside class="related-sections">
     <h3>Related Sections</h3>
     <ul>
       <li><a href="array.html">[array]</a> (parent)</li>
       <li><a href="array.overview.html">[array.overview]</a></li>
       <li><a href="array.members.html">[array.members]</a></li>
     </ul>
   </aside>
   ```

3. **Search**: Client-side search across all stable names
   - Fuzzy matching with Fuse.js
   - Filter by version pair
   - Highlight in results

---

## Code Examples

### Generator Script Outline

```python
#!/usr/bin/env python3
"""
generate_html_site.py

Generate static HTML site for C++ standard evolution viewer.
"""

import os
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json

# Version pairs (adjacent only)
VERSION_PAIRS = [
    ('n3337', 'n4140', 'C++11', 'C++14'),
    ('n4140', 'n4659', 'C++14', 'C++17'),
    ('n4659', 'n4861', 'C++17', 'C++20'),
    ('n4861', 'n4950', 'C++20', 'C++23'),
    ('n4950', 'trunk', 'C++23', 'C++26'),
]

def extract_stable_name(diff_file):
    """Extract stable name from diff header."""
    with open(diff_file) as f:
        for line in f:
            if line.startswith('# Stable name:'):
                return line.split(':', 1)[1].strip()
    return None

def classify_stable_name(name):
    """Determine tier (1 = featured, 2 = detailed)."""
    dot_count = name.count('.')
    return 1 if dot_count <= 1 else 2

def generate_diff_html(diff_file, output_file, context):
    """Generate HTML for a single diff using diff2html."""
    # Use diff2html-cli
    cmd = [
        'diff2html',
        '-i', 'file',
        '-F', str(output_file),
        '--style', 'side',
        '--title', context['title'],
        str(diff_file)
    ]
    subprocess.run(cmd, check=True)

    # Post-process: inject custom navigation
    inject_navigation(output_file, context)

def inject_navigation(html_file, context):
    """Inject custom navigation into generated HTML."""
    from bs4 import BeautifulSoup

    with open(html_file) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Add breadcrumbs
    header = soup.new_tag('header')
    # ... (add navigation elements)

    soup.body.insert(0, header)

    with open(html_file, 'w') as f:
        f.write(str(soup))

def generate_site(output_dir='site'):
    """Main generation logic."""
    env = Environment(loader=FileSystemLoader('templates/'))
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate landing page
    template = env.get_template('index.html')
    content = template.render(version_pairs=VERSION_PAIRS)
    (output_path / 'index.html').write_text(content)

    # Generate version overview and diff pages
    for from_tag, to_tag, from_name, to_name in VERSION_PAIRS:
        generate_version_pair(from_tag, to_tag, from_name, to_name,
                            output_path, env)

def generate_version_pair(from_tag, to_tag, from_name, to_name,
                         output_path, env):
    """Generate pages for one version pair."""
    diff_dir = Path(f'diffs/{from_tag}_to_{to_tag}/by_stable_name')

    # Collect Tier 1 stable names
    stable_names = []
    for diff_file in sorted(diff_dir.glob('*.diff')):
        name = extract_stable_name(diff_file)
        if name and classify_stable_name(name) == 1:
            stable_names.append({
                'name': name,
                'size': diff_file.stat().st_size,
                'file': diff_file.stem
            })

    # Generate overview page
    template = env.get_template('version_overview.html')
    content = template.render(
        from_name=from_name,
        to_name=to_name,
        stable_names=stable_names
    )
    version_dir = output_path / 'versions'
    version_dir.mkdir(exist_ok=True)
    (version_dir / f'{from_tag}-to-{to_tag}.html').write_text(content)

    # Generate individual diff pages
    diff_output_dir = output_path / 'diffs' / f'{from_tag}-to-{to_tag}'
    diff_output_dir.mkdir(parents=True, exist_ok=True)

    for item in stable_names:
        context = {
            'title': f'[{item["name"]}] - {from_name} → {to_name}',
            'stable_name': item['name'],
            'from_version': from_name,
            'to_version': to_name,
        }

        diff_file = diff_dir / f'{item["file"]}.diff'
        output_file = diff_output_dir / f'{item["file"]}.html'

        generate_diff_html(diff_file, output_file, context)
        print(f'Generated: {output_file}')

if __name__ == '__main__':
    generate_site()
```

### HTML Template Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/diff2html/bundles/css/diff2html.min.css">
    <link rel="stylesheet" href="/css/custom.css">
</head>
<body>
    <header>
        <nav class="breadcrumb">
            <a href="/">Home</a> &gt;
            <a href="/versions/{{ version_slug }}.html">{{ from_version }} → {{ to_version }}</a> &gt;
            <span>[{{ stable_name }}]</span>
        </nav>

        <div class="version-timeline">
            <span>Evolution Timeline:</span>
            {% for pair in version_pairs %}
            <a href="/diffs/{{ pair.slug }}/{{ stable_name_file }}.html"
               class="{% if pair.slug == current_slug %}active{% endif %}">
                {{ pair.short }}
            </a>
            {% endfor %}
        </div>
    </header>

    <main>
        <h1>[{{ stable_name }}]</h1>

        <div class="metadata">
            <span class="version-badge">{{ from_version }} → {{ to_version }}</span>
            <span class="size-badge">{{ file_size_kb }} KB</span>
        </div>

        <div class="external-links">
            <a href="https://eel.is/c++draft/{{ stable_name }}" target="_blank">📖 Current Draft</a>
            <a href="{{ cppreference_link }}" target="_blank">📚 cppreference</a>
            <a href="{{ github_link }}" target="_blank">📄 Full Chapter</a>
        </div>

        <div id="diff-container">
            {{ diff_html | safe }}
        </div>
    </main>

    <footer>
        <p>Generated from <a href="https://github.com/[username]/cppstdmd">cppstdmd</a></p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/diff2html/bundles/js/diff2html-ui.min.js"></script>
    <script src="/js/navigation.js"></script>
</body>
</html>
```

---

## Deployment Guide

### Step-by-Step Deployment to gh-pages

**1. Generate site locally**:
```bash
cd /home/jason/notes/cpp_standard_tools/converted/cppstdmd
python3 generate_html_site.py --output site/
```

**2. Create gh-pages branch**:
```bash
# Create orphan branch (no history)
git checkout --orphan gh-pages

# Remove all files from staging
git rm -rf .

# Copy generated site files
cp -r site/* .
cp site/.nojekyll .

# Add and commit
git add .
git commit -m "Initial deployment: C++ Standard Evolution Viewer

- 2,860 HTML pages (Tier 1 stable names)
- 5 adjacent version pairs (C++11→14 through C++23→26)
- Interactive side-by-side diffs with diff2html
- Clean navigation and cross-linking"

# Push to GitHub
git push origin gh-pages
```

**3. Configure GitHub Pages**:
- Go to repository Settings → Pages
- Source: Deploy from branch `gh-pages`
- Root directory: `/`
- Save

**4. Access site**:
- URL: `https://[your-username].github.io/cppstdmd/`
- Wait ~2 minutes for initial deployment

**5. Test deployment**:
```bash
# Check homepage
curl -I https://[your-username].github.io/cppstdmd/

# Check diff page
curl -I https://[your-username].github.io/cppstdmd/diffs/cpp20-to-cpp23/array.html
```

### Continuous Deployment (Optional)

**GitHub Actions workflow** (`.github/workflows/deploy-site.yml`):
```yaml
name: Deploy C++ Standard Viewer

on:
  push:
    branches: [main]
    paths:
      - 'diffs/**'
      - 'generate_html_site.py'
      - 'templates/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install diff2html-cli
        run: npm install -g diff2html-cli

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Python dependencies
        run: pip install jinja2 beautifulsoup4

      - name: Generate site
        run: python3 generate_html_site.py --output site/

      - name: Deploy to gh-pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
          force_orphan: true
```

---

## Future Enhancements

### Phase 2 Features (Optional)

1. **Advanced Search**:
   - Full-text search across diff content
   - Regular expression support
   - Search within specific version pair

2. **Statistics Dashboard**:
   - Most changed sections over time
   - Growth charts (line count, file size)
   - New feature introduction timeline

3. **Comparison Mode**:
   - View multiple versions side-by-side (e.g., C++11 vs C++17 vs C++23)
   - Highlight differences across 3+ versions

4. **Dark Mode**:
   - Toggle dark/light theme
   - Respect system preference
   - Persist user choice

5. **PDF Export**:
   - Generate PDF for individual diffs
   - Useful for offline reference

6. **Community Features**:
   - Comments/annotations (via GitHub Discussions)
   - Favorite/bookmark sections
   - Share custom diff comparisons

### Phase 3 Features (Advanced)

1. **Tier 2 Diffs**:
   - Add remaining ~7,500 diffs
   - On-demand generation or full pre-generation

2. **Historical Versions**:
   - Extend back to C++98, C++03
   - Requires source data from older standards

3. **API Access**:
   - REST API for programmatic access
   - JSON endpoints for diff metadata

4. **Proposal Tracking**:
   - Link diffs to C++ proposals (P0000R0 papers)
   - Show which paper introduced each change

5. **Mobile App**:
   - Progressive Web App (PWA)
   - Offline-first with service workers

---

## Success Metrics

**Performance**:
- ✅ Page load time: <2 seconds on 3G
- ✅ Lighthouse score: >90
- ✅ Mobile-friendly: Yes
- ✅ Accessible: WCAG 2.1 AA

**Coverage**:
- ✅ Major library components: 100%
- ✅ Core language features: 100%
- ✅ Educational value: High

**Engagement (post-launch)**:
- ⬜ 500+ visitors in first month
- ⬜ Featured in r/cpp or C++ Weekly
- ⬜ Positive community feedback
- ⬜ 50+ GitHub stars

---

## Appendix: Design Mockups

### Landing Page Layout
```
┌─────────────────────────────────────────────────┐
│  C++ STANDARD EVOLUTION EXPLORER                │
│  Interactive diffs across C++ versions          │
├─────────────────────────────────────────────────┤
│                                                 │
│  Choose a version transition:                   │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 🔵 C++11 → C++14 (862 changes)            │ │
│  │ Highlights: auto, lambdas, constexpr       │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 🔵 C++14 → C++17 (1,957 changes)          │ │
│  │ Highlights: structured bindings, if conste│ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  [... C++17→20, C++20→23, C++23→26 ...]        │
│                                                 │
│  🔍 [Search stable names]  📊 [View stats]     │
└─────────────────────────────────────────────────┘
```

### Diff Viewer Page Layout
```
┌─────────────────────────────────────────────────┐
│ Home > C++20→23 > [array]               [🔍💾] │
├─────────────────────────────────────────────────┤
│ [array] - std::array fixed-size container       │
│                                                 │
│ Version Timeline:                               │
│ C++11→14 | C++14→17 | C++17→20 | 👉C++20→23 | C++23→26 │
│                                                 │
│ External Links:                                 │
│ [📖 eel.is] [📚 cppreference] [📄 Full Chapter] │
│                                                 │
│ ┌─────────────────────────────────────────────┐│
│ │         Side-by-Side Diff (diff2html)      ││
│ │                                             ││
│ │  C++20 (n4861)      │  C++23 (n4950)       ││
│ │ ────────────────────┼───────────────────   ││
│ │  [Syntax-highlighted diff content]          ││
│ │                                             ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ Related Sections:                               │
│ • [array.overview] • [array.cons]               │
└─────────────────────────────────────────────────┘
```

---

## Conclusion

This plan provides a comprehensive roadmap for creating an educational C++ standard evolution viewer. The focus on Tier 1 stable names and adjacent version pairs keeps the scope manageable while delivering maximum educational value.

**Key Decisions**:
- ✅ Use this repository's gh-pages branch (no new repo needed)
- ✅ Focus on 5 adjacent pairs (C++11→14 through C++23→26)
- ✅ Tier 1 filtering (0-1 dot stable names, ~572 per version)
- ✅ Hub-and-spoke multi-page architecture
- ✅ diff2html for rendering
- ✅ Static HTML (no JavaScript required, enhanced with JS)

**Next Steps**:
1. Install dependencies (diff2html-cli, jinja2)
2. Create `generate_html_site.py` generator script
3. Build templates (landing, overview, diff viewer)
4. Generate Tier 1 HTML pages (~2,860 files)
5. Deploy to gh-pages branch
6. Launch and gather feedback

**Timeline**: 6-8 weeks for MVP, ~60 hours total effort

**Questions?** Refer back to this document or contact the project maintainer.

---

**Document Version**: 1.0
**Last Updated**: 2025-11-12
**Author**: Claude Code + Jason Turner
