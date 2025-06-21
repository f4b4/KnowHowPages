# Plan for KnowHowPages project
_Exported on 6/20/2025 at 19:36:03 GMT+2 from Cursor (1.1.4)_

---

**User**

I want to plan a project called KnowHowPages.
the features:
- edit pages with an editor in markdown
- manage the markdown files in git
- the files are structured in folders
  - the folder are displayed in the web site as tree nodes to navigate to the pages
- when changes are pushed to the git repository, a static html file generator should be running
- code snipptes in the markdown shold be presented with syntax coloring in the web site
- the web site should have a light and a dark theme, a toggle switch should be in the right corner
- wenn possible, the theme should have an auto mode, depending on the os setting

Please generate a detailed plan to create this project iteratively wit ai assitment.

---

**Cursor**

Below is an opinionated, step-by-step roadmap for building "KnowHowPages".  
It is broken into small iterations so you can continuously deliver value, lean on AI help, and keep scope under control.  
Each iteration ends with a demoable milestone and a short "AI Pairing Checklist" that tells you what to ask the assistant next.

──────────────────────────────── Iteration 0 — Foundations
Goal: Skeleton repo, toolchain, and continuous deployment of "Hello World" site.

1. Decide workspace layout  
   • /content              → Markdown sources  
   • /src                  → React / SSG framework code  
   • /scripts              → helper scripts (git hooks, generators)  
   • /static               → favicons, images

2. Pick the main tech stack  
   Suggested:  
   • Framework – Next.js (13 with App Router) or Astro (pure SSG).  
   • Styling – Tailwind CSS (dark/light via class).  
   • Syntax highlight – Shiki + rehype-shiki (markdown to HTML).  
   • Editor – Monaco or CodeMirror in the browser.  
   • Git engine – isomorphic-git in the browser OR server-side git CLI.  
   • CI/CD – GitHub Actions → GitHub Pages / Vercel.

3. Create GitHub repo "KnowHowPages"; push initial README.

4. Add CI job "deploy.yml"  
   • On main branch push → install deps → build static site → deploy.  
   • Verify that the job publishes the placeholder site.

AI Pairing Checklist  
⧁ Ask: "Generate deploy.yml for Next.js static export."  
⧁ Ask: "Create a minimal Next.js page with Tailwind dark/light toggle."

──────────────────────────────── Iteration 1 — Markdown ingestion & theming
Goal: Render existing markdown as styled pages with light/dark/auto mode.

1. Install gray-matter, remark, rehype-shiki.  
2. Add a build-time script that walks /content, converts each .md into HTML, and produces a JSON manifest { slug, title, filepath }.  
3. In layout.tsx implement:  
   • Dark/light CSS variables (prefers-color-scheme: dark) for "auto".  
   • Toggle in top-right; selection persisted in localStorage.  
4. Use Shiki theme "github-light" / "github-dark" to stay consistent.

Milestone demo: Markdown files show syntax-highlighted code, navigation tree is hard-coded.

AI Pairing Checklist  
⧁ Ask: "Write a Node script that walks /content and outputs manifest.json."  
⧁ Ask: "Add Shiki-powered MDX renderer with Tailwind typography."

──────────────────────────────── Iteration 2 — Folder-based navigation tree
Goal: Auto-generate sidebar tree from folder structure.

1. Reuse the manifest to build a nested tree of { name, children, page? }.  
2. Create a React component <TreeNav> that renders folders as expandable nodes, pages as links.  
3. Keep current path open/selected in the tree (use usePathname).

Milestone demo: Clicking nodes navigates; deep links reload correctly.

AI Pairing Checklist  
⧁ Ask: "Transform manifest array into recursive tree data."  
⧁ Ask: "Build <TreeNav> with indented folders and CSS transitions."

──────────────────────────────── Iteration 3 — In-browser Markdown editor
Goal: Edit a page and commit the change to Git.

1. Add protected route /edit/[...slug].  
2. Embed Monaco editor with markdown language.  
3. Provide "Save" → calls API route /api/git/commit:  
   • Writes file to repo working tree.  
   • Runs `git add` & `git commit -m 'edit page'`.  
   • Option A (client-side): use isomorphic-git in browser + push via GitHub PAT.  
   • Option B (server-side): call git CLI (needs server runtime like Vercel functions). Pick whichever matches your hosting.

4. After commit, redirect back to the page.

Milestone demo: Change text, refresh, new content live.

AI Pairing Checklist  
⧁ Ask: "Integrate isomorphic-git to commit from browser."  
⧁ Ask: "Securely store and use GitHub token in Next.js API route."

──────────────────────────────── Iteration 4 — Live preview & diff
Goal: Writer UX polish.

1. Split editor page into editor (left) + live preview (right) using same renderer pipeline.  
2. Add gist-style diff view of uncommitted changes.  
3. Keyboard shortcuts: Ctrl+S, Cmd+B/I for bold/italic.

Milestone demo: WYSIWYG-ish editing.

AI Pairing Checklist  
⧁ Ask: "Implement debounce live preview for markdown."  
⧁ Ask: "Show git diff between working tree and HEAD for a file."

──────────────────────────────── Iteration 5 — Full CI Static Generator
Goal: Ensure every push triggers fresh static export, including new pages.

1. Promote the manifest and HTML generation scripts to part of "build".  
2. Optionally pre-render to /public for ultra-fast hosting (Astro or Next export).  
3. Cache npm deps in GitHub Actions.  
4. Smoke test build in CI (broken links, missing headings, etc.).

Milestone demo: Push → GitHub Actions → updated website in ~1 minute.

AI Pairing Checklist  
⧁ Ask: "Add link-checker step to CI."  
⧁ Ask: "Speed up build by caching .next/cache."

──────────────────────────────── Iteration 6 — Quality-of-life & polish
Idea backlog—order as needed:
• Search bar with FlexSearch or Fuse.js (index built at build-time).  
• Mermaid & PlantUML diagram support.  
• Per-page front-matter options: hide TOC, draft, tags.  
• RSS feed & sitemap.  
• "Copy code" button in code blocks.  
• Internationalization (next-i18next).  
• Keyboard navigation for tree.  
• Responsive mobile drawer for nav.

──────────────────────────────── Best practices & conventions
1. Treat /content as the source of truth; never write to /src during editing.  
2. Use Conventional Commits for clarity (docs: edit-page, feat: editor, etc.).  
3. Keep a "docs/decisions" folder to record architectural choices (ADR-style).  
4. Write unit tests for helper utilities; snapshot test markdown render.  
5. Use Renovate or Dependabot for dependency updates.  
6. Protect main branch; feature branches + PRs.

──────────────────────────────── Tooling & AI usage tips
• Ask the assistant to generate scaffolding, boilerplate, or tricky regexes.  
• Provide file paths & show current code when asking for targeted edits.  
• For anything security-sensitive (tokens), request guidance but paste secrets yourself.  
• Keep questions small: "Write Tailwind class for dark-mode table" is better than "Finish the whole page".

──────────────────────────────── Outcome
Following these iterations you'll have:

✔ Git-versioned markdown knowledge base  
✔ Interactive web editor with git commit flow  
✔ Auto-generated, syntax-highlighted, themeable static site  
✔ CI pipeline that rebuilds on every push  
✔ Clear backlog for future enhancements

Happy building!

# KnowHowPages Implementation Plan with GitHub Pages and GitHub Actions

## 1. Repository Setup
- Create a new GitHub repository named "KnowHowPages"
- Initialize with README.md, .gitignore for Python
- Upload existing content and code

## 2. Configure GitHub Pages
- Go to repository Settings → Pages
- Set source to GitHub Actions

## 3. Create GitHub Actions Workflow
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy KnowHowPages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Generate site
        run: python generate.py
        
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v1
        with:
          path: ./site
          
  deploy:
    needs: build
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

## 4. Update Project Structure
- Ensure requirements.txt is complete:
  ```
  markdown
  pygments
  ```
- Add a .nojekyll file to prevent GitHub Pages from processing with Jekyll

## 5. Content Management Process
1. Clone repository locally
2. Add/edit Markdown files in the content directory
3. Commit and push changes
4. GitHub Actions automatically builds and deploys the site

## 6. Custom Domain Setup (Optional)
- Purchase domain if needed
- Add CNAME record pointing to your GitHub Pages URL
- Add CNAME file to repository
- Configure custom domain in GitHub Pages settings

## 7. Testing and Validation
- Verify site builds correctly locally before pushing
- Check GitHub Actions logs for any build issues
- Test site navigation and content rendering

## 8. Future Enhancements
- Add search functionality
- Implement site analytics
- Create contribution guidelines for team members

