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
Gold Set V3 counts, the validated/experimental/planned/blocked breakdown)
is sourced directly from `PROJECT_STATUS.md`, `DATASET.md`, `EVALUATION.md`
and `ROADMAP.md` at the repository root. If those documents are updated,
this page's copy (in both `index.html` and `js/i18n.js`) must be updated to
match — never the other way around. Do not restate a number here that
isn't already documented in those files.

## Accessibility & performance notes

- Respects `prefers-reduced-motion` (all entrance/scroll/parallax
  animations are disabled).
- No scroll-linked JS listeners for animation — reveals use
  `IntersectionObserver`; the only `scroll` listener toggles a CSS class
  for the nav's shrink state.
- No build tooling, no client-side router, no heavy dependencies.

## Known limitations

- No CI job lints or deploys this page yet — see the main repository CI
  (`.github/workflows/tests.yml`), which currently only covers the Python
  package.
- GitHub Pages / other static hosting is not yet wired up; enabling it
  requires a repository-admin action (Settings → Pages) that this session
  cannot perform.
