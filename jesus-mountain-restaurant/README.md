# Jesus Mountain Restaurant — Prototype 001

A portable, self-contained static homepage prototype for
**Jesus Mountain Restaurant, Spring City, Utah** —
part of *My Jesus-Greg WORLD* by Greg Muller.

Prototype only. Not published. Do not connect a domain or push to GitHub
without Greg's approval after review.

## Files

- `index.html` — homepage
- `styles.css` — all styling (no build step, no dependencies)
- `script.js` — mobile navigation toggle only
- `assets/` — images (see below)

## Preview locally

Open `index.html` in any browser, or serve the folder:

    python3 -m http.server 8000

then visit http://localhost:8000

## Publish on GitHub Pages (when approved)

1. Create a GitHub repository and upload all files and the `assets/` folder,
   keeping the folder structure exactly as-is.
2. In the repository: Settings → Pages → deploy from the main branch, root folder.
3. Relative paths are used throughout, so no configuration is needed.

## Assets: final vs. placeholder

Final supplied assets (real artwork provided by Greg):

- `assets/jesus-mountain-hero.jpg` — the actual photograph of Horseshoe Mountain
  ("Jesus Mountain") above Spring City, converted from the supplied PNG to JPEG.
- `assets/jesus-mountain-logo-original.png` — the supplied black-and-white logo, unaltered.
- `assets/jesus-mountain-logo-transparent.png` — the same logo with the white
  background made transparent (derived, artwork unchanged), used over the hero
  photograph and in the footer.

Temporary placeholder assets (to be replaced with Greg's real photographs):

- `assets/tile-menu-placeholder.jpg`
- `assets/tile-story-placeholder.jpg`
- `assets/tile-gallery-placeholder.jpg`
- `assets/tile-jesus-tv-placeholder.jpg`

These four were cropped from the approved homepage mockup solely so the
prototype tiles look like the design. They are labeled "Placeholder image"
on the page itself and are **not** photographs of the actual restaurant,
food, or property.

## Known limitations of Prototype 001

- The hero photograph supplied is 960 × 540 px, so it softens on very large
  screens. A higher-resolution original would sharpen the hero.
- The mockup's exact typeface was not identified or supplied, so an elegant
  system serif stack is used (Playfair Display if installed, otherwise
  Georgia / Times). No webfonts are loaded, keeping the site self-contained.
- Top navigation follows Assignment 001, §5 (Menu, Our Story, Gallery,
  Jesus TV, Contact). The mockup's Order / Reservations / Visit Us items
  were omitted because ordering and reservations are not being implemented
  and no hours or address have been confirmed.
- The four tiles link to clearly labeled placeholder sections on the same
  page (Menu, Our Story, Gallery, Jesus TV, Contact). No food prices, menu
  descriptions, hours, address, testimonials, ordering, payments, or
  reservations have been invented or implemented.
