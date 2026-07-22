# 🍎 8-Bit Orchard

A pixel-art catalogue of apple cultivars — the **Apple Dex**. Browse apple
breeds as little 8-bit stat cards: origins, sweetness / tartness / crispness
meters, best uses, harvest season, and a bit of RPG-flavoured flair.

Python is the data layer; the browser does the pixel art.

## Run it

```bash
python serve.py
```

Then open <http://localhost:8000>. That rebuilds the data and serves the site
in one step. Press `Esc` to close a card.

> Serve over `http://` (not by opening `index.html` as a `file://`), otherwise
> the browser blocks the `apples.json` fetch.

## How it fits together

```
data/apples.py   ← source of truth (Python dataclasses, one Apple each)
build.py         ← emits web/apples.json
serve.py         ← build + serve web/ locally
web/
  index.html     ← markup
  style.css      ← the 8-bit theme (small NES-ish palette, scanlines)
  app.js         ← filtering, sorting, and the pixel-apple sprite generator
  apples.json    ← generated; don't edit by hand
```

### Sprites

There's no per-apple artwork to draw. `app.js` holds one 16×16 apple
silhouette and recolours it from each cultivar's `skin` hex — adding a diagonal
highlight, a dark outline, and a glint — so every apple renders as its own
pixel gem. Adding an apple is just adding data.

Bicolour varieties also set an optional `blush` hex, layered as vertical
striping on the sun side of the fruit; uniform apples leave it `None` and
render solid.

## Add an apple

Append an `Apple(...)` to `APPLES` in `data/apples.py`, then re-run
`python serve.py`. Stats are 1–5. `build.py` validates ids, stat ranges, and
colours, so bad data fails loudly.

## Ideas for later

- More cultivars (there are always more heirlooms and cider apples)
- A print / export view for a favourite list

Each detail card links out to Wikipedia — a direct article when the data
sets a `wiki` URL, otherwise a name-based Wikipedia search.

Done so far: light/dark theme, bicolour striped sprites, a "surprise me"
random apple button, pixel-art country flags, a harvest-season filter,
favourites saved to `localStorage`, a mutable chiptune blip on card open,
shareable `#slug` links, a two-apple compare view, a back-to-top button,
and per-apple Wikipedia links.
