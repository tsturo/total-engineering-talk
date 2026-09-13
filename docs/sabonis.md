# Add Arvydas Sabonis to the talk

One new stop, right after the "Does not exist" stamp (step `s11-ultra` in `talk/index.html`). The message: the closest thing to a total player existed, in another sport. A 2.21 m centre who shot three-pointers and passed like a guard.

Read `talk/README.md` first. The Editing section explains how stops and scenes work.

## Researcher

Collect his real career facts. Pick six stats for a card in the same style as the footballer cards in `talk/index.html` (class `card`, six bars, `hi` / `mid` / `lo` colours). Add a one-line source note.

## Builder

Add the stop after `s11-ultra`: a step with camera data, the portrait `talk/img/sabonis.png`, the card, a small "Almost" stamp, and speaker notes in plain language, no slogans. Do not touch other stops.

## Checker

Run `node scripts/check.mjs`. Confirm the new stop appears and no other stop's scene changed. Reject with a reason if not.

## Rules

Do not commit. Finish with a summary of what changed.
