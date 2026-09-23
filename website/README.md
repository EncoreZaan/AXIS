# AXIS — Landing Page

Official landing page for the AXIS research project. Static site, no build
step, no framework, no external JS dependency.

## Stack

- Plain HTML5 / CSS3 / vanilla JS (ES5-compatible, no bundler).
- Fonts: [Fraunces](https://fonts.google.com/specimen/Fraunces) (display
  serif) and [Inter](https://fonts.google.com/specimen/Inter) (UI sans),
  loaded from Google Fonts.
- All visuals (the hero architectural composition, the isometric diagram,
  icons) are hand-built with inline SVG/CSS — no photographs, no generated
  images, no third-party image assets.
- i18n: a small dictionary in `js/i18n.js` (FR default, EN available),
  applied via `data-i18n="path.to.key"` attributes in `index.html` and
  toggled client-side by `js/main.js`. The chosen language persists in
  `localStorage`.

## Run locally

No install required:

```bash
cd website
python3 -m http.server 8000
# open http://localhost:8000
```

## Structure

```
website/
├── index.html       # all sections, semantic HTML, data-i18n attributes
├── css/styles.css   # design tokens (palette/type), layout, animations
├── js/i18n.js        # FR/EN translation dictionary
├── js/main.js        # nav, reveal-on-scroll, counters, parallax, lang switch
└── assets/           # favicon (SVG only)
```

## Keeping content accurate

Every number and status claim on this page (65,342 assets, the
0.0517 m / 2.7739 m evaluation figures, the 98.14% reduction, the 200/200
Gold Set V3 counts, the RUN-023 metrics — 1,006 test examples, 63.12%
topological reasoning accuracy vs 14.51% base, 100% format adherence, 0%
hallucination, VDI 1.28 — and the validated/experimental/unproven/blocked
breakdown) is sourced directly from `PROJECT_STATUS.md`, `docs/PROJECT_STATUS.md`,
`docs/SCIENTIFIC_TIMELINE.md`, `DATASET.md`, `EVALUATION.md`, `ARCHITECTURE.md`,
`ROADMAP.md`, and the `RUN-019` through `RUN-023` folders at the repository
root. If those documents are updated, this page's copy (in both `index.html`
and `js/i18n.js`) must be updated to match — never the other way around. Do
not restate a number here that isn't already documented in those files.

"AXIS-Clearance", "AXIS-Spatial", and "AXIS-Unified" (used in the Models
section) are this page's own public names for three internal components
documented in `ARCHITECTURE.md` §2.3/2.5 (`SpatialRelationMLP`, the
`Qwen2-VL-7B-Instruct + LoRA` adapter from `RUN-022`, and the planned
`Unified Architectural Transformer`) — a presentation layer, not a rename
of those documents' own identifiers. AXIS Studio is presented as planned
and not yet started, because no implementation, interface, or mockup for
it exists anywhere in this repository; do not add feature claims for it
here until a real component exists to document.

## Accessibility & performance notes

- Respects `prefers-reduced-motion` (all entrance/scroll/parallax
  animations are disabled).
- No scroll-linked JS listeners for animation — reveals use
  `IntersectionObserver`; the only `scroll` listener toggles a CSS class
  for the nav's shrink state.
- No build tooling, no client-side router, no heavy dependencies.

## Deployment (GitHub Pages)

This site is published automatically by
[`.github/workflows/deploy-website.yml`](../.github/workflows/deploy-website.yml).

- **Trigger:** every push to `main` that touches `website/**` (or the
  workflow file itself), plus a manual `workflow_dispatch` button in the
  Actions tab.
- **How:** the workflow uploads the `website/` folder as-is (no build step)
  using the official `actions/upload-pages-artifact` +
  `actions/deploy-pages` actions, and publishes it via GitHub's native
  Pages deployment (not the legacy `gh-pages` branch).
- **URL:** `https://<github-username>.github.io/AXIS/` — the repository is
  served under the `/AXIS/` sub-path, not at the domain root.
- **One-time manual setup required:** GitHub Pages must be switched to
  "GitHub Actions" as its source before the first deployment can succeed.
  A repository admin does this once in **Settings → Pages → Build and
  deployment → Source → GitHub Actions**. Until that's done, the workflow
  runs but the deploy step fails with a "Pages site not found" error; no
  code change fixes that, only this one Settings toggle.
- **Every subsequent push to `main` under `website/` redeploys
  automatically** — no manual action needed after the initial setup.

### Why no path changes were needed for `/AXIS/`

All asset references in `index.html` (`css/styles.css`, `js/i18n.js`,
`js/main.js`, `assets/favicon.svg`) are relative, not root-absolute, so
they resolve correctly whether the site is served at `/` (local dev) or
under `/AXIS/` (GitHub Pages project site). In-page navigation uses plain
`#fragment` anchors, which are path-independent. `localStorage` (used only
for the FR/EN language preference) is scoped per-origin by the browser and
unaffected by the sub-path. No code changes were required for Pages
compatibility.

## Known limitations

- No CI job lints this page yet — see the main repository CI
  (`.github/workflows/tests.yml`), which covers the Python package only.
- The GitHub Pages source must be switched to "GitHub Actions" manually
  once, as described above — no workflow can do that from inside itself.
