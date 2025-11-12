# C++ Standard Evolution Viewer - HTML Site Generator

This document explains how to generate and deploy the interactive C++ Standard Evolution Viewer website.

## Overview

The HTML site generator creates a static website with:
- Interactive side-by-side diffs of C++ standard sections across versions
- Clean, responsive design
- Version timeline navigation
- Search and filtering capabilities
- ~2,860 HTML pages (Tier 1 sections only)

## Prerequisites

### System Requirements

1. **Node.js and npm** (for diff2html-cli)
   ```bash
   # Check if installed
   node --version
   npm --version
   ```

2. **Python 3.10+** with virtual environment
   ```bash
   python3 --version
   ```

3. **diff2html-cli** (npm package)
   ```bash
   npm install -g diff2html-cli
   # Verify installation
   diff2html --version
   ```

4. **Python dependencies** (installed automatically by script):
   - jinja2
   - beautifulsoup4
   - lxml

### Initial Setup

If you haven't already, run the main setup script:
```bash
./setup-and-build.sh
```

Then install the additional Python dependencies:
```bash
source venv/bin/activate
pip install jinja2 beautifulsoup4 lxml
```

## Usage

### Test Mode (Recommended First Step)

Generate a small test site with 10 diffs from one version pair:

```bash
# Set PATH if needed (for npm global installs)
export PATH="$HOME/.npm/node_modules/bin:$PATH"

# Activate virtual environment
source venv/bin/activate

# Run in test mode
python3 generate_html_site.py --test
```

This will create:
- `site/index.html` - Landing page
- `site/versions/cpp11-to-cpp14.html` - Version overview
- `site/diffs/cpp11-to-cpp14/*.html` - 10 diff pages
- `site/css/custom.css` - Custom styles
- `site/js/navigation.js` - JavaScript enhancements
- `site/.nojekyll` - Disables Jekyll processing

### View Locally

```bash
cd site
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

### Full Generation (All 5 Version Pairs)

Generate the complete Tier 1 site (~2,860 pages):

```bash
# Activate virtual environment
source venv/bin/activate

# Set PATH if needed
export PATH="$HOME/.npm/node_modules/bin:$PATH"

# Generate full site
python3 generate_html_site.py --output site/
```

**Estimated time**: 30-60 minutes (depends on CPU speed)
**Estimated size**: ~430 MB

### Custom Options

```bash
# Generate with a limit per version pair (for testing)
python3 generate_html_site.py --output site/ --limit 50

# Generate Tier 2 sections (2+ dots, more granular)
python3 generate_html_site.py --output site/ --tier 2

# View help
python3 generate_html_site.py --help
```

## Deployment to GitHub Pages

### Option 1: Manual Deployment

```bash
# 1. Generate the site
python3 generate_html_site.py --output site/

# 2. Go back to main branch
git checkout main
git commit -am "Update site generator"

# 3. Create gh-pages branch (if not exists)
git checkout --orphan gh-pages
git rm -rf .

# 4. Copy site files
cp -r site/* .
cp site/.nojekyll .

# 5. Commit and push
git add .
git commit -m "Deploy C++ Standard Evolution Viewer

- 2,860+ HTML pages (Tier 1 sections)
- 5 version pairs (C++11→14 through C++23→26)
- Interactive side-by-side diffs with diff2html
- Responsive design with search and filtering"

git push origin gh-pages
```

### Option 2: Automated Deployment (GitHub Actions)

Create `.github/workflows/deploy-site.yml` in your main branch:

```yaml
name: Deploy C++ Standard Viewer

on:
  push:
    branches: [main]
    paths:
      - 'generate_html_site.py'
      - 'templates/**'
      - 'diffs/**'

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
        run: pip install jinja2 beautifulsoup4 lxml

      - name: Generate site
        run: python3 generate_html_site.py --output site/

      - name: Deploy to gh-pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
          force_orphan: true
```

### Configure GitHub Pages

1. Go to repository Settings → Pages
2. Source: Deploy from branch `gh-pages`
3. Directory: `/` (root)
4. Save

Your site will be available at: `https://[username].github.io/cppstdmd/`

## Project Structure

```
.
├── generate_html_site.py          # Main generator script
├── templates/                      # Jinja2 templates
│   ├── index.html                  # Landing page template
│   ├── version_overview.html      # Version overview template
│   ├── css/
│   │   └── custom.css              # Custom styles
│   └── js/
│       └── navigation.js           # JavaScript enhancements
├── diffs/                          # Input: Generated diff files
│   ├── n3337_to_n4140/
│   │   └── by_stable_name/*.diff
│   ├── n4140_to_n4659/
│   │   └── by_stable_name/*.diff
│   └── ...
└── site/                           # Output: Generated HTML site
    ├── index.html
    ├── .nojekyll
    ├── versions/
    │   ├── cpp11-to-cpp14.html
    │   ├── cpp14-to-cpp17.html
    │   ├── cpp17-to-cpp20.html
    │   ├── cpp20-to-cpp23.html
    │   └── cpp23-to-cpp26.html
    ├── diffs/
    │   ├── cpp11-to-cpp14/
    │   │   ├── array.html
    │   │   ├── vector.html
    │   │   └── ... (Tier 1 sections)
    │   ├── cpp14-to-cpp17/
    │   └── ...
    ├── css/
    │   └── custom.css
    └── js/
        └── navigation.js
```

## Features

### Tier 1 Sections

The site focuses on **Tier 1 stable names** (0-1 dots):
- **0 dots**: Top-level sections (e.g., `array`, `vector`, `thread`)
- **1 dot**: Major subsections (e.g., `array.cons`, `class.copy`, `ranges.adaptors`)

This covers ~572 sections per version pair, representing the most educationally valuable content.

### Navigation Features

1. **Version Timeline**: Jump between versions for the same section
2. **Breadcrumbs**: Home > Version Pair > Section
3. **Search**: Filter sections by name on overview pages
4. **Size Indicators**: Visual indicators for small/medium/large changes
5. **External Links**: Links to eel.is, cppreference, GitHub
6. **Keyboard Shortcuts**:
   - `h` - Go to home
   - `/` - Focus search (on overview pages)
   - `Esc` - Clear search

### Responsive Design

- **Mobile**: Stacked layout, touch-friendly
- **Tablet**: Two-column with collapsible sidebar
- **Desktop**: Three-column with fixed sidebar
- **Dark Mode**: Automatic based on system preference (via diff2html)

## Troubleshooting

### diff2html not found

If you get "diff2html: command not found":

```bash
# Check npm global bin path
npm config get prefix

# Add to PATH
export PATH="$(npm config get prefix)/bin:$PATH"

# Or for non-standard npm configs
export PATH="$HOME/.npm/node_modules/bin:$PATH"
```

### Python dependencies missing

```bash
source venv/bin/activate
pip install jinja2 beautifulsoup4 lxml
```

### Large file warnings

Files >100KB get a warning banner. This is normal for sections like:
- `utilities.diff` (621 KB)
- `containers.diff` (470 KB)
- `ranges.diff` (432 KB)

These render fine but may be slow on older devices.

### Generation is slow

Full generation takes 30-60 minutes. Speed improvements:
- Use `--limit` for testing
- Use SSD storage
- Close other applications
- Run on a faster CPU

## Statistics

### Tier 1 (Generated by Default)

| Version Pair | Sections | Est. Size |
|--------------|----------|-----------|
| C++11 → C++14 | ~150 | 25 MB |
| C++14 → C++17 | ~400 | 80 MB |
| C++17 → C++20 | ~550 | 110 MB |
| C++20 → C++23 | ~500 | 100 MB |
| C++23 → C++26 | ~480 | 95 MB |
| **Total** | **~2,080** | **~410 MB** |

### Tier 2 (Optional)

Tier 2 includes 2+ dot sections (more granular):
- ~1,900 additional sections per version pair
- ~1.2 GB total size
- Use `--tier 2` to generate

## Performance

### Browser Requirements

- Modern browser (Chrome 90+, Firefox 88+, Safari 14+)
- JavaScript enabled (for enhanced features)
- Works without JavaScript (progressive enhancement)

### Loading Times

- **Landing page**: <1 second
- **Overview pages**: 1-2 seconds
- **Small diffs** (<50 KB): 1-2 seconds
- **Large diffs** (>100 KB): 3-5 seconds

## Maintenance

### Updating Diffs

When you regenerate diffs (via `generate_diffs.py`):

```bash
# 1. Regenerate diffs
python3 generate_diffs.py --versions n4950 trunk --by-stable-name

# 2. Regenerate site
python3 generate_html_site.py --output site/

# 3. Redeploy to GitHub Pages
# (follow deployment steps above)
```

### Customizing Appearance

Edit `templates/css/custom.css` to customize:
- Colors
- Fonts
- Layout
- Dark mode styles

Changes require regenerating the site.

## Credits

- **diff2html**: https://github.com/rtfpessoa/diff2html
- **cplusplus/draft**: https://github.com/cplusplus/draft
- **Pandoc**: https://pandoc.org/

## License

Same license as the parent project (see LICENSE file).

## Questions?

Refer to the main project documentation or open an issue on GitHub.
