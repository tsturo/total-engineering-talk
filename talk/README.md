# Total Engineering talk

One poster, a linear camera tour, driven by a clicker. Built on impress.js 2.0.0 (vendored, 2D only).

## Run

Double-click `index.html`, or drag it into Chrome. No server needed.

A local server is only needed for the speaker console (`P`), which Chrome blocks from file URLs:

```
python3 -m http.server 8000
```

then open http://localhost:8000/talk/.

## Keys

- PageDown, Right, Space, Down: next click
- PageUp, Left, Up: previous click
- `b` or `.`: black screen
- `P`: speaker console (notes, target time per stop, clock, next view)
- F5 and Escape are swallowed so a clicker's play button cannot leave fullscreen. Enter fullscreen from the browser menu before starting.

## URL switches

- `?nomotion` disables camera transitions (rehearsal and reduced motion)
- `?print` same, for PDF export
- `#/s04-totaal` jumps to a stop by id

## PDF fallback

```
npx decktape impress "http://localhost:8000/talk/?print" talk.pdf -s 1920x1080 --pause 1500
```

## Editing

- Poster objects live inside `#poster` in `index.html` and carry `data-obj` ids.
- Each step and substep declares the complete visible set in `data-scene`. Nothing depends on the previous click.
- The pitch SVG is generated: edit `scripts/build_pitch.py` and run it.
- `node scripts/check.mjs` validates that every scene references existing objects and every step has camera data and notes.

## Rehearsal checklist

1. Chrome, local server, fullscreen.
2. Test at a 16:10 window size as well as 16:9.
3. Test the real clicker on a key logger page first; add any unexpected key in `js/director.js`.
4. Click through forward and backward once; every backward click must restore the previous picture.
