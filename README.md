# hermionegranger.example

A personal portfolio site for Hermione Granger. Static HTML, CSS, and a small
amount of progressive-enhancement JavaScript. No build step, no framework, no
dependencies at runtime, no tracking.

## Run it locally

Any static file server works, because there is nothing to compile:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Layout

```
index.html                  single-page site (hero, about, work, projects, writing, speaking, contact)
404.html                    not-found page
robots.txt  sitemap.xml     crawler directives
site.webmanifest            installable-site metadata
assets/css/styles.css       design tokens, layout, components, print styles
assets/js/main.js           theme toggle, mobile nav, active-section nav, footer year
assets/img/*.svg            hand-authored artwork (portrait, favicon, social card, touch icon)
assets/img/*.png            rasterised versions of the two SVGs that need them
assets/hermione-granger-cv.pdf  generated one-page CV
tools/render-images.mjs     regenerates the PNGs from their SVG sources
tools/make-cv.py            regenerates the CV PDF (standard library only)
```

## What "best practices" means here

**Accessibility**
- Semantic landmarks (`header`, `nav`, `main`, `section`, `footer`) and one `h1`, with headings in order.
- A skip link, visible focus rings (`:focus-visible`, 3px, high-contrast), and keyboard-operable controls.
- The mobile menu button carries `aria-expanded`/`aria-controls`; Escape closes it and returns focus.
- The theme button is a toggle with `aria-pressed` and a label that changes with its state.
- Nav links set `aria-current` on the section in view; activating one moves focus to that section.
- Text and interactive colours meet WCAG AA contrast in both themes; colour never carries meaning alone.
- `prefers-reduced-motion` disables smooth scrolling, transitions, and hover lift.
- Images have real alternative text; decorative shapes are `aria-hidden`.

**Performance**
- No frameworks or web fonts: one stylesheet, one deferred 4 KB script, system font stacks.
- Artwork is SVG where it can be, so it stays sharp at any size and costs a few kilobytes.
- The hero portrait declares `width`/`height` (no layout shift) and `fetchpriority="high"`.
- Layout is CSS Grid with intrinsic `minmax()` tracks, so there are few breakpoints to maintain.

**SEO and sharing**
- Unique title and meta description, `link rel="canonical"`, `sitemap.xml`, and `robots.txt`.
- Open Graph and Twitter card tags with a 1200×630 PNG preview image.
- JSON-LD `Person` structured data.

**Resilience and privacy**
- The page is complete without JavaScript: the menu button is revealed by the script, so with
  scripting off the navigation renders expanded instead of sitting behind a dead button.
- `localStorage` access is wrapped in `try`/`catch`, so private-mode browsing degrades to the
  system colour scheme instead of throwing.
- An inline head script applies the saved theme before first paint to avoid a flash of the wrong theme.
- No analytics, cookies, or third-party requests of any kind.

## Before this goes live

The site is live at <https://knudergud.github.io/hermione/> and every URL in it
points there. The content is still a portfolio for a fictional person. Replace,
in this order:

1. `hello@hermionegranger.example` and the three "Elsewhere" links in the contact
   section, which do not resolve.
2. `assets/img/portrait.svg` — swap in a real photograph, keeping the `width`/`height`
   attributes accurate so the layout does not shift.
3. `assets/hermione-granger-cv.pdf` — the generated file is a placeholder; drop in the real CV.
4. `sitemap.xml` `lastmod`, whenever the content changes.

After changing either SVG that has a PNG twin, regenerate them:

```bash
npm install --no-save @resvg/resvg-js
node tools/render-images.mjs
```

## Deploying

The repository root is the document root, so GitHub Pages serves it directly
from `main` with no build step.

`.nojekyll` at the root turns Jekyll off. Without it, Pages runs the repository
through Jekyll with the primer theme, which injects a generated
`assets/css/style.css`, and which will render `README.md` as the home page for
any commit that has no `index.html`. Keep the file.

Paths are relative everywhere except `404.html`, because a not-found page can be
served at any depth and relative paths would resolve against the missing URL. Its
three absolute paths carry the `/hermione/` project prefix.

### Moving to a custom domain

1. Drop the `/hermione/` prefix from the three absolute paths in `404.html`.
2. Replace `https://knudergud.github.io/hermione/` with the new origin in
   `index.html` (canonical, Open Graph, JSON-LD), `robots.txt`, `sitemap.xml`,
   and the footer text of `assets/img/og-card.svg`, then re-run `tools/render-images.mjs`.
3. Add a `CNAME` file at the root containing the bare domain.

The relative paths in `index.html` and `site.webmanifest` need no changes either way.
