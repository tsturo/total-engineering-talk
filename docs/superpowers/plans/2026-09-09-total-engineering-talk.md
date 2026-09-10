# Total Engineering Talk Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A zoomable one-poster presentation for the Total Engineering talk, driven by a clicker, with a central pitch whose objects appear and disappear per click.

**Architecture:** impress.js v2.0.0 (vendored, 2D only) moves a camera over one absolutely positioned poster element. Steps are transparent 1920x1080 camera frames carrying camera coordinates, speaker notes and a declarative scene string; substeps carry scene strings too. A small director script turns scene strings into `.on` classes on poster objects, so any stop, substep, back-click or reload rebuilds the full picture. The pitch is inline SVG over the photographic pitch.png.

**Tech Stack:** HTML, CSS, vanilla JS, impress.js 2.0.0, inline SVG, Python http.server for the speaker console, Node for the check script.

**Spec:** `total-engineering-proposal.md` (sections 3, 6, 7) plus `total-engineering-talk.md` for script text.

## Global Constraints

- No build step. `talk/index.html` opens from a local static server (`python3 -m http.server`), never needs a bundler.
- One dependency only: `talk/vendor/impress.js` at v2.0.0, unmodified.
- 2D only: `data-perspective="0"`, no `data-rotate*` anywhere, no `will-change` on root, canvas or steps.
- Canvas 7000 x 3940 virtual px; pitch 3000 x 1940 at x 2000..5000, y 1200..3140.
- Every step and substep fully declares its visible set in `data-scene`; scenes never depend on the previous click.
- Palette: paper #F4F1E8, ink #151515, orange #F36C21. Orange never as text or thin strokes on grass. Labels on grass carry a dark outline.
- Fonts: Anton (titles, numbers), Permanent Marker (handwriting), Archivo (small text), loaded from Google Fonts with local fallbacks.
- Copy rules: no slogans, no em dashes, only verified facts (1974 line-up, Beck wording).
- Clicker keys: PageUp, PageDown, Left, Right, Space advance or go back; `b` and `.` blackout; F5 and Escape are suppressed.

---

## File structure

```
talk/
  index.html            poster DOM, pitch SVG, steps with notes and scenes
  vendor/impress.js     v2.0.0 bundle
  css/poster.css        layers, poster objects, on/off transitions, step frames
  css/pitch.css         pitch SVG object styles and transitions
  js/scene.js           parseScene(string) -> Set of object ids (pure, testable)
  js/director.js        wires impress events to applyScene; clicker safety
  js/notes.js           per-step target times shown in the speaker console
  img/                  pitch.png copy, title-no-bg.png copy, placeholders
scripts/
  check.mjs             validates index.html: scene ids exist, steps unique, notes present
```

---

### Task 1: Skeleton with camera route

**Files:**
- Create: `talk/index.html`, `talk/css/poster.css`, `talk/js/scene.js`, `talk/js/director.js`, `talk/vendor/impress.js`, `scripts/check.mjs`

**Interfaces:**
- Produces: `parseScene(text: string): Set<string>` in `talk/js/scene.js`, exported as a global `parseScene` and as an ES module export for the check script; `applyScene(root: Element, ids: Set<string>)` toggles class `on` on every `[data-obj]` element under root.
- Produces: the DOM convention `div#poster > [data-obj="<id>"]` for showable objects and `div.step[data-scene]` plus `.substep[data-scene]` for stops.

- [ ] **Step 1: Write the failing check for scene parsing**

`scripts/check.mjs`:

```js
import { readFileSync } from 'node:fs';
import { parseScene } from '../talk/js/scene.js';

const html = readFileSync(new URL('../talk/index.html', import.meta.url), 'utf8');
const objIds = new Set([...html.matchAll(/data-obj="([^"]+)"/g)].map(m => m[1]));
const scenes = [...html.matchAll(/data-scene="([^"]*)"/g)].map(m => m[1]);
const stepIds = [...html.matchAll(/class="step[^"]*"[^>]*id="([^"]+)"/g)].map(m => m[1]);
let failed = false;
for (const scene of scenes) for (const id of parseScene(scene)) if (!objIds.has(id)) { console.error(`scene references unknown object: ${id}`); failed = true; }
if (new Set(stepIds).size !== stepIds.length) { console.error('duplicate step ids'); failed = true; }
if (stepIds.length === 0) { console.error('no steps'); failed = true; }
console.log(failed ? 'check failed' : `ok: ${stepIds.length} steps, ${objIds.size} objects, ${scenes.length} scenes`);
process.exit(failed ? 1 : 0);
```

- [ ] **Step 2: Run it, expect failure**

Run: `node scripts/check.mjs`
Expected: error, `scene.js` not found.

- [ ] **Step 3: Write scene.js**

```js
export function parseScene(text) {
  const ids = new Set();
  for (const token of (text || '').trim().split(/\s+/)) {
    if (!token) continue;
    if (token.startsWith('-')) ids.delete(token.slice(1));
    else ids.add(token.replace(/^\+/, ''));
  }
  return ids;
}
export function applyScene(root, ids) {
  for (const el of root.querySelectorAll('[data-obj]')) el.classList.toggle('on', ids.has(el.dataset.obj));
}
if (typeof window !== 'undefined') { window.parseScene = parseScene; window.applyScene = applyScene; }
```

- [ ] **Step 4: Vendor impress.js**

Run: `mkdir -p talk/vendor && curl -sL -o talk/vendor/impress.js https://cdn.jsdelivr.net/gh/impress/impress.js@2.0.0/js/impress.js`

- [ ] **Step 5: Write index.html skeleton**

Root with `data-perspective="0"`, `data-transition-duration="1100"`, `data-width="1920"`, `data-height="1080"`, `data-max-scale="4"`, `data-min-scale="0"`. Inside: `div#poster` (7000x3940, `position:absolute; left:-3500px; top:-1970px` so canvas 0,0 is the poster centre) with placeholder rectangles carrying `data-obj`. Steps:

```html
<div id="s00-title" class="step" data-x="0" data-y="-1430" data-scale="1.15" data-scene="title"><div class="notes">There's a Dutch idea behind this title.</div></div>
<div id="s01-works" class="step" data-x="-2550" data-y="780" data-scale="0.7" data-scene="title laptop"><div class="substep" data-scene="title laptop laptop-result"></div><div class="substep" data-scene="title laptop laptop-result laptop-itworks"></div><div class="notes">...</div></div>
```

Camera rule: `data-scale` is the ratio of canvas px to screen px at 1080p; the whole poster is scale 3.65.

- [ ] **Step 6: Write director.js**

```js
(function () {
  const root = document.getElementById('poster');
  function sceneOf(el) { return parseScene(el.getAttribute('data-scene')); }
  document.addEventListener('impress:stepenter', e => applyScene(root, sceneOf(e.target)));
  document.addEventListener('impress:substep:enter', e => applyScene(root, sceneOf(e.detail.substep)));
  document.addEventListener('impress:substep:leave', e => {
    const step = e.target; const prev = step.querySelectorAll('.substep-visible');
    applyScene(root, prev.length ? sceneOf(prev[prev.length - 1]) : sceneOf(step));
  });
  window.addEventListener('keydown', e => { if (e.key === 'F5' || e.key === 'Escape') { e.preventDefault(); e.stopImmediatePropagation(); } }, true);
  let busy = false;
  window.addEventListener('keydown', e => {
    const nav = ['PageDown', 'PageUp', 'ArrowLeft', 'ArrowRight', ' '];
    if (!nav.includes(e.key)) return;
    if (busy) { e.preventDefault(); e.stopImmediatePropagation(); return; }
    busy = true; setTimeout(() => { busy = false; }, 1150);
  }, true);
  impress().init();
})();
```

Note on the substep leave handler: after impress removes `substep-visible` from the leaving element, the remaining visible substeps define the state; when none remain the step's own scene applies.

- [ ] **Step 7: Run the check, expect pass**

Run: `node scripts/check.mjs`
Expected: `ok: N steps, M objects, K scenes`.

- [ ] **Step 8: Verify in a browser**

Run: `python3 -m http.server 8000` from the project root, open `http://localhost:8000/talk/`, click through with PageDown, confirm every step arrives, `b` blanks, `P` opens the console. Fix camera coordinates that miss their target.

---

### Task 2: Pitch SVG with real grass

**Files:**
- Create: `talk/css/pitch.css`, `talk/img/pitch.jpg`
- Modify: `talk/index.html` (pitch group inside `#poster`)

**Interfaces:**
- Produces: `svg#pitch` with viewBox `0 0 3000 1940`, positioned at poster x 2000, y 1200. Groups: `g#markings`, `g#bands` (objects `band-fe band-be band-qa band-devops`), `g#players` (objects `p1..p11`, each `<g data-obj="pN" class="player"><circle/><text class="num"/><text class="name"/></g>`), `g#ball` (`ball`, positioned by CSS custom properties `--x --y`), `g#trails` (`trail-move trail-cover chain`), `g#labels` (`lbl-movement lbl-cover lbl-totaalvoetbal`).

- [ ] **Step 1: Prepare the grass**

Run: `sips -s format jpeg -s formatOptions 85 pitch.png --out talk/img/pitch.jpg`. Place as `<image href="img/pitch.jpg" width="3000" height="1940" preserveAspectRatio="none"/>` at the bottom of the SVG, masked by a `<clipPath>` rectangle with a 40 px torn-edge path later.

- [ ] **Step 2: Draw markings as vector**

Reuse the geometry from `design/generate.py` scaled by 3000/1050: touchlines, halfway line, centre circle r 261, penalty areas 471 deep, goal areas 157 deep, penalty arcs, goals. Stroke white, width 10, opacity 0.9.

- [ ] **Step 3: Players**

Marker: circle r 62, fill #F36C21, stroke #151515 width 8, drop shadow filter. Number in Anton 60 px white. Name in Archivo 700 44 px white with `paint-order: stroke; stroke: #151515; stroke-width: 10` below the disc. Positions as CSS custom properties on the group: `style="--x: 371; --y: 970"` with `transform: translate(calc(var(--x) * 1px), calc(var(--y) * 1px))` and `transition: transform 1.2s cubic-bezier(.45,0,.15,1)`.

1974 positions (attack right, canvas px in the 3000x1940 box): Jongbloed 8 (157,970); Suurbier 20 (600,300); Rijsbergen 17 (520,800); Haan 2 (520,1140); Krol 12 (600,1640); Jansen 6 (1150,600); Neeskens 13 (1050,970); Van Hanegem 3 (1150,1340); Rep 16 (1950,380); Cruyff 14 (2100,970); Rensenbrink 15 (1950,1560).

- [ ] **Step 4: Bands, ball, trails, labels**

Bands: four rects at quarter widths, alternate fill #F4F1E8 opacity 0.08 and #151515 opacity 0.14, dividers dashed #151515 opacity 0.75 width 14, tags Archivo 700 52 px white on #151515 at the top touchline. Ball: circle r 36 white, stroke #151515 width 7, positioned like players. Trails: paths with `stroke-dasharray: var(--len); stroke-dashoffset: var(--len)` transitioning to 0 over 1.2 s when `.on`. Labels: Permanent Marker 72 px, `paint-order: stroke`, dark outline.

- [ ] **Step 5: on/off transitions**

`pitch.css`: every `[data-obj]` in the SVG has `opacity: 0; transition: opacity .4s`; `.on { opacity: 1 }`. Players additionally transition transform.

- [ ] **Step 6: Check and look**

Run: `node scripts/check.mjs`, then open the pitch stop in the browser and compare with the design canvas' pitch artboard.

---

### Task 3: The pitch stay, all scenes

**Files:**
- Modify: `talk/index.html` (steps s03 to s08 and their substeps)

**Interfaces:**
- Consumes: object ids from Task 2.
- Produces: player position variants via extra classes toggled by scene ids `move-7 cover-2` (the director toggles `.on` on `[data-obj]`; position variants are elements too: `<g data-obj="pos-move" ...>` is not possible for the same node, so variants are implemented as CSS: `#players.on-move-7 [data-obj="p16"] { --x: 2500; --y: 420 }` driven by a helper object `<span data-obj="move-7" hidden>` whose `.on` state the director mirrors to `#players` class `on-move-7`).

- [ ] **Step 1: Extend the director for state mirrors**

In `director.js` after `applyScene`, mirror: for each `[data-obj][data-mirror]` element, add or remove class `on-<id>` on the element with id `data-mirror` according to its `.on` state.

```js
function mirror(root) {
  for (const el of root.querySelectorAll('[data-obj][data-mirror]')) {
    document.getElementById(el.dataset.mirror).classList.toggle('on-' + el.dataset.obj, el.classList.contains('on'));
  }
}
```

Call `mirror(root)` at the end of every scene application.

- [ ] **Step 2: Write the scenes**

Base set for the pitch: `title pitch photo1974 p8 p20 p17 p2 p12 p6 p13 p3 p16 p14 p15 names1974`.

| Step | Substep scenes (each adds to the base) |
| --- | --- |
| s03-1974 | base; base + `caption1974` |
| s04-totaal | base + `chain`; base + `chain ball-at-cruyff`; base + `move-suurbier cover-neeskens trail-move trail-cover lbl-movement lbl-cover`; base + `compress` |
| s05-formation | base `-names1974 -photo1974` + `band-fe`; + `band-be`; + `band-qa`; + `band-devops`; + `ball-at-fe`; + `ball-at-be-line`; + `ball-at-qa-line` |
| s06-total | camera widens; bands gone: base-without-names + `move-suurbier cover-neeskens trail-move trail-cover`; + `possibilities`; + `chosen support`; + `word-engineer` |
| s07-alibis | previous + `alibi1`; + `alibi1 strike1`; + `alibi2`; + `alibi2 strike2`; + `alibi3`; + `alibi3 strike3` |
| s08-tenpercent | previous + `tenpercent` |

Movement targets in CSS: `#players.on-move-suurbier [data-obj="p20"] { --x: 1500; --y: 300 }`, `#players.on-cover-neeskens [data-obj="p13"] { --x: 700; --y: 420 }`, `#players.on-compress` shifts every player 350 px toward the centre.

- [ ] **Step 3: Passing chain**

`<path data-obj="chain" d="M157 970 L600 1640 L1150 1340 L1050 970 L600 300 L1150 600 L1950 380 L1500 970 L2100 970 L2700 800"/>` drawn with the dash trick over 2.5 s; a marker circle animates along it with `offset-path` in Chrome.

- [ ] **Step 4: Check and rehearse the stay**

Run: `node scripts/check.mjs`. In the browser, click through s03 to s08 forward and backward; every backward click must restore the previous picture exactly.

---

### Task 4: Off-pitch places and notes

**Files:**
- Modify: `talk/index.html`, `talk/css/poster.css`
- Create: `talk/img/title.png` (copy of title-no-bg.png), `talk/img/laptop-placeholder.svg`

- [ ] **Step 1: Title** at poster centre-top (x 2500..4500, y 120..760): `<img data-obj="title" src="img/title.png">`.
- [ ] **Step 2: Laptop** lower left (x 300..1500, y 2300..3200): a photo frame with a screen area `data-obj="laptop-result"` and a handwritten `IT WORKS` `data-obj="laptop-itworks"`.
- [ ] **Step 3: Beck note** upper right (x 5500..6600, y 900..1700): taped paper card, Archivo, the full post text `data-obj="beck-full"`, the last sentence large `data-obj="beck-last"`, the follow-up line `data-obj="beck-next"`. Wording verbatim from the proposal's sources.
- [ ] **Step 4: Notebook** lower right (x 5300..6800, y 2300..3400): open spread, left page sketch `data-obj="nb-sketch"`, the missing connection `data-obj="nb-link"`, right page three handwritten steps `nb-step1 nb-step2 nb-step3`.
- [ ] **Step 5: Alibis** in the pitch's right margin (x 5100..5450, y 1300..2900) rotated 90 degrees? No: keep upright, three short lines in Permanent Marker under the Beck note, each with an orange strike path `strike1..3`.
- [ ] **Step 6: Notes** for every step from `total-engineering-talk.md`, trimmed to the new order; `data-target="mm:ss"` per step.
- [ ] **Step 7: Check, then click through the whole route**.

---

### Task 5: Presenter safety and export

**Files:**
- Modify: `talk/js/director.js`, `talk/css/poster.css`
- Create: `talk/js/notes.js`

- [ ] **Step 1: Reduced motion**: `@media (prefers-reduced-motion: reduce) { #impress .step, .impress-canvas { transition-duration: 0s !important } }` plus `?nomotion` query parameter that sets `data-transition-duration="0"` before init.
- [ ] **Step 2: Speaker console**: enable `data-console-autolaunch="false"`, `P` opens it; `data-console-css-iframe` hides `img.photo` and `.paper` in previews. `notes.js` renders `target` and elapsed per step into the notes panel.
- [ ] **Step 3: Print mode**: `?print` zeroes transitions; document the DeckTape command in `talk/README.md`: `npx decktape impress http://localhost:8000/talk/?print talk.pdf -s 1920x1080 --pause 1500`.
- [ ] **Step 4: Cursor hide** after 3 s via the mouse-timeout plugin class.
- [ ] **Step 5: Rehearsal checklist** in `talk/README.md`: Chrome, local server, 16:10 window test, clicker test with a key logger page.

---

### Task 6: Ground texture

**Files:**
- Modify: `talk/css/poster.css`, `talk/img/`

- [ ] **Step 1: Placeholder ground**: paper colour with a CSS noise gradient until the regenerated reference arrives.
- [ ] **Step 2: When the reference image is in the project**: downscale a copy to 7000 px wide as `talk/img/ground.jpg`, mask out the areas under the title, laptop, Beck note, notebook and pitch, place real objects on top.
- [ ] **Step 3: Final pullback check**: the 1x view must read as a poster with title, pitch and five recognisable objects and no small text.
