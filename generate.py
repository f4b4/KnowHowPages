#!/usr/bin/env python3
"""Static site generator for KnowHowPages.

This script scans a content directory full of Markdown files (nested folders allowed),
converts each one to HTML with server-side syntax highlighting, and produces a
fully static web site in the output directory.  A collapsible tree navigation on
the left reflects the folder structure; the current page is highlighted and its
branch is kept open.  Each <pre><code> block gets a "Copy" button powered by a
4-line inline JS helper.  No other JavaScript is included.

Dependencies (install via pip):
    markdown pygments

Usage (from project root):
    python generate.py               # uses ./content → ./site
    python generate.py -i docs -o build
"""

import argparse
import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Optional

import markdown
from pygments.formatters import HtmlFormatter

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_INPUT_DIR = Path("content")
DEFAULT_OUTPUT_DIR = Path("site")
ASSETS_DIR = Path("assets")  # Folder with global assets to be copied verbatim

# ---------------------------------------------------------------------------
# HTML Template - IMPORTANT: Keep this template formatted with proper indentation
# ---------------------------------------------------------------------------
TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <base href="{base_href}"/>
  <title>{title}</title>
  <link rel="icon" href="favicon.ico" type="image/x-icon">
  <link rel="manifest" href="manifest.json" />
  <link rel="stylesheet" href="static/style.css"/>
</head>
<body>
  <button class="menu-btn" onclick="toggleNav()">☰</button>
  <div class="layout">
    <nav class="sidebar">
      {nav}
    </nav>
    <main>
      {body}
    </main>
  </div>
  <script>
    function copyCode(btn) {{
      const code = btn.nextElementSibling.innerText;
      navigator.clipboard.writeText(code).then(() => {{
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = 'Copy', 2000);
        
      }});
    }}

    function toggleNav() {{
      const sidebar = document.querySelector('.sidebar');
      sidebar.classList.toggle('open');
    }}

    document.addEventListener('DOMContentLoaded', () => {{
      const sidebar = document.querySelector('.sidebar');
      sidebar.addEventListener('click', (e) => {{
        if (e.target.tagName === 'A') {{
          sidebar.classList.remove('open');
        }}
      }});
    }});
  </script>
</body>
</html>"""

# ---------------------------------------------------------------------------
# CSS Styles - IMPORTANT: Maintain this CSS with proper formatting and indentation
# ---------------------------------------------------------------------------
BASE_CSS = """:root {
  --sidebar: #f6f8fa;
  --border: #d0d7de;
  --accent: #0969da;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
}

@media(prefers-color-scheme: dark) {
  :root {
    --sidebar: #161b22;
    --border: #30363d;
    --accent: #58a6ff;
    background: #0d1117;
    color: #c9d1d9;
  }
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

body {
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  display: flex;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  position: absolute;
}

.layout {
  flex: 1;
  display: flex;
  flex-direction: row;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.sidebar {
  width: 20rem;
  background: var(--sidebar);
  border-right: 1px solid var(--border);
  overflow-x: hidden;
  overflow-y: auto;
  height: 100%;
  padding: 2rem;
}

main {
  flex: 1;
  padding: 2rem;
  overflow: auto;
}

/* Indentation for nested folders */
nav details {
  margin-left: 0;
}

nav details details {
  margin-left: 1rem;
}

nav details details details {
  margin-left: 1.5rem;
}

nav details details details details {
  margin-left: 2rem;
}

/* Style for disclosure triangles */
nav details > summary {
  list-style-type: none;
  position: relative;
  cursor: pointer;
}

nav details > summary::before {
  content: "▶";
  display: inline-block;
  width: 1em;
  font-size: 0.8em;
  margin-right: 0.2em;
  transition: transform 0.2s;
}

nav details[open] > summary::before {
  transform: rotate(90deg);
}

nav a, nav summary {
  display: block;
  color: inherit;
  text-decoration: none;
  padding: 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

nav a.active {
  font-weight: bold;
}

/* Mobile: Show full text when expanded */
nav a.expanded, nav summary.expanded {
  white-space: normal;
  overflow: visible;
  background-color: rgba(0, 0, 0, 0.05);
}

@media(prefers-color-scheme: dark) {
  nav a.expanded, nav summary.expanded {
    background-color: rgba(255, 255, 255, 0.1);
  }
}

pre {
  overflow-x: auto;
  overflow-y: hidden;
  padding: 1rem;
  border: 1px solid var(--border);
}

/* Code blocks and script styling */
pre, code {
  background-color: #f6f8fa;
  color: #24292e;
}

@media(prefers-color-scheme: dark) {
  pre, code {
    background-color: #161b22;
    color: #c9d1d9;
  }
}

@media(prefers-color-scheme: dark) {
  script {
    background-color: #0d1117;
    color: #e6edf3;
  }
}

.copy-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  font-size: .8rem;
  padding: 2px 6px;
  background: var(--accent);
  color: #fff;
  border: 0;
  cursor: pointer;
  opacity: .7;
}

.copy-btn:hover {
  opacity: 1;
}

/* -------------------------------------------------
   Responsive sidebar and hamburger menu
--------------------------------------------------*/
.menu-btn {
  display: none;
  position: fixed;
  top: 1rem;
  right: 1rem;
  font-size: 1.25rem;
  padding: 0.4rem 0.6rem;
  background: var(--sidebar);
  color: var(--accent);
  border: 1px solid var(--border);
  border-radius: 4px;
  opacity: 1;
  cursor: pointer;
  z-index: 1100;
}

@media (max-width: 768px) {
  .menu-btn {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 1000;
    padding-top: 4rem;
  }
  .sidebar.open {
    transform: translateX(0);
  }
}"""

# ---------------------------------------------------------------------------
# Helper data structures
# ---------------------------------------------------------------------------

class Node:
    """Represents a directory or markdown file in the nav tree."""

    def __init__(self, name: str, path: Path, is_dir: bool):
        self.name = name
        self.path = path  # absolute path
        self.is_dir = is_dir
        self.children: List["Node"] = []  # for dirs only

    def add_child(self, node: "Node"):
        self.children.append(node)


# ---------------------------------------------------------------------------
# Tree construction and nav rendering
# ---------------------------------------------------------------------------

def build_tree(root: Path) -> Node:
    """Recursively build a tree mirroring the directory structure."""
    root_node = Node(root.name, root, True)
    for child in sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        if child.is_dir():
            root_node.add_child(build_tree(child))
        elif child.suffix.lower() == ".md":
            root_node.add_child(Node(child.stem, child, False))
    return root_node


def render_nav(node: Node, current_md: Optional[Path], root: Path, depth: int = 0) -> str:
    """Return HTML nav markup with inline indentation based on depth."""
    indent_px = depth * 16  # 1rem ≈ 16px
    style_attr = f" style=\"margin-left:{indent_px}px\"" if depth else ""

    if node.is_dir:
        # Determine if this folder needs to be open
        open_attr = " open" if current_md and current_md.is_relative_to(node.path) else ""
        parts = [f"<details{open_attr}{style_attr}><summary title=\"{node.name}\">{node.name}</summary>"]
        for child in node.children:
            parts.append(render_nav(child, current_md, root, depth + 1))
        parts.append("</details>")
        return "\n".join(parts)
    else:
        rel_md_path = node.path.relative_to(root)
        html_href = rel_md_path.with_suffix(".html")
        class_attr = " class=\"active\"" if current_md and rel_md_path == current_md.relative_to(root) else ""
        return f"<a href=\"{html_href.as_posix()}\"{class_attr}{style_attr} title=\"{node.name}\">{node.name}</a>"


# ---------------------------------------------------------------------------
# Markdown → HTML with copy buttons
# ---------------------------------------------------------------------------

def md_to_html(text: str, formatter: HtmlFormatter) -> str:
    # Convert Jekyll-style code blocks to standard markdown code blocks
    text = re.sub(r'{%\s*highlight\s+(\w+)\s*%}(.*?){%\s*endhighlight\s*%}', 
                 r'```\1\2```', 
                 text, 
                 flags=re.DOTALL)
    
    md = markdown.Markdown(extensions=[
        "fenced_code",
        "tables",
        "toc",
        "codehilite",  # adds Pygments classes
    ], extension_configs={
        "codehilite": {
            "guess_lang": False,
            "use_pygments": True,
            "noclasses": False,
        }
    })
    html = md.convert(text)
    # Inject copy buttons before each <pre><code>
    def _inject(match):
        return ("<button class=\"copy-btn\" onclick=\"copyCode(this)\">Copy</button>" + match.group(0))

    html = re.sub(r"<pre><code[\s\S]*?</code></pre>", _inject, html)
    return html


# ---------------------------------------------------------------------------
# Site generation
# ---------------------------------------------------------------------------

def generate_site(input_dir: Path, output_dir: Path):
    if output_dir.exists():
        shutil.rmtree(output_dir)
    (output_dir / "static").mkdir(parents=True, exist_ok=True)

    # Prepare CSS (base + pygments theme)
    formatter = HtmlFormatter(style="default")
    pygments_css = formatter.get_style_defs(".codehilite")
    css_path = output_dir / "static" / "style.css"
    css_path.write_text(BASE_CSS + "\n" + pygments_css, encoding="utf8")

    tree = build_tree(input_dir)

    for md_path in input_dir.rglob("*.md"):
        rel_md = md_path.relative_to(input_dir)
        html_out_path = output_dir / rel_md.with_suffix(".html")
        html_out_path.parent.mkdir(parents=True, exist_ok=True)

        # Calculate base href for this page (to reach site root)
        depth = len(rel_md.parts) - 1  # How many directories deep is this file
        base_href = "../" * depth if depth > 0 else "./"

        body_html = md_to_html(md_path.read_text(encoding="utf8"), formatter)
        title = extract_title(body_html) or md_path.stem
        
        # Exclude the content root folder itself from the sidebar; start at its children
        nav_html = "\n".join(
            render_nav(child, md_path, input_dir, depth=0) for child in tree.children
        )
        page_html = TEMPLATE.format(title=title, nav=nav_html, body=body_html, base_href=base_href)

        html_out_path.write_text(page_html, encoding="utf8")
        print(f"✓ {rel_md} → {html_out_path.relative_to(output_dir)}")

    # Optional: copy non-md assets (e.g., images) maintaining structure
    for asset in input_dir.rglob("*"):
        if asset.is_file() and asset.suffix.lower() not in {".md"}:
            dest = output_dir / asset.relative_to(input_dir)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, dest)

    # -----------------------------------------------------------
    # Copy global assets (favicon, manifest, images, etc.)
    # -----------------------------------------------------------
    if ASSETS_DIR.exists():
        for asset in ASSETS_DIR.rglob("*"):
            if asset.is_file():
                dest = output_dir / asset.relative_to(ASSETS_DIR)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(asset, dest)
                print(f"⇢ assets/{asset.relative_to(ASSETS_DIR)} → {dest.relative_to(output_dir)}")

    # Write index.html redirecting to first article (if any)
    first_page = next((p for p in input_dir.rglob("*.md")), None)
    if first_page:
        first_html = first_page.relative_to(input_dir).with_suffix(".html")
        idx_path = output_dir / "index.html"
        idx_path.write_text(f"<meta http-equiv=\"refresh\" content=\"0; url={first_html.as_posix()}\">", encoding="utf8")


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def extract_title(html: str) -> Optional[str]:
    match = re.search(r"<h[1-3][^>]*>(.*?)</h[1-3]>", html)
    return match.group(1) if match else None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a static site from Markdown.")
    parser.add_argument("-i", "--input", default=DEFAULT_INPUT_DIR, type=Path, help="Markdown source directory (default: ./content)")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR, type=Path, help="Output directory (default: ./site)")
    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"Input directory {args.input} does not exist.")

    generate_site(args.input, args.output)
    print(f"\nSite generated at {args.output.resolve()}") 