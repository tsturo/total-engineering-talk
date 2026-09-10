import math
from pathlib import Path

OUT = Path(__file__).parent
W, H = 1200, 760
PX, PY, PW, PH = 75, 40, 1050, 680
CX, CY = PX + PW / 2, PY + PH / 2
S = 10

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Permanent+Marker&family=Archivo:wght@500;700&display=swap">'

PLAYERS = [
    (1, 130, 380), (2, 260, 150), (4, 250, 300), (5, 250, 460), (3, 260, 610),
    (6, 450, 240), (8, 430, 380), (10, 450, 520), (7, 720, 170), (9, 760, 380), (11, 720, 590),
]
DIVIDERS = [PX + PW * q for q in (0.25, 0.5, 0.75)]
BANDS = ["FE", "BE", "QA", "DevOps"]


def markings(stroke, width, opacity=1):
    dy = math.sqrt(91.5**2 - 55**2)
    a = f'fill="none" stroke="{stroke}" stroke-width="{width}" stroke-opacity="{opacity}" stroke-linecap="round"'
    parts = [
        f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" {a}/>',
        f'<line x1="{CX}" y1="{PY}" x2="{CX}" y2="{PY+PH}" {a}/>',
        f'<circle cx="{CX}" cy="{CY}" r="91.5" {a}/>',
        f'<circle cx="{CX}" cy="{CY}" r="{width}" fill="{stroke}" fill-opacity="{opacity}"/>',
        f'<rect x="{PX}" y="{CY-201.6}" width="165" height="403.2" {a}/>',
        f'<rect x="{PX+PW-165}" y="{CY-201.6}" width="165" height="403.2" {a}/>',
        f'<rect x="{PX}" y="{CY-91.6}" width="55" height="183.2" {a}/>',
        f'<rect x="{PX+PW-55}" y="{CY-91.6}" width="55" height="183.2" {a}/>',
        f'<circle cx="{PX+110}" cy="{CY}" r="{width}" fill="{stroke}" fill-opacity="{opacity}"/>',
        f'<circle cx="{PX+PW-110}" cy="{CY}" r="{width}" fill="{stroke}" fill-opacity="{opacity}"/>',
        f'<path d="M{PX+165} {CY-dy:.1f} A91.5 91.5 0 0 1 {PX+165} {CY+dy:.1f}" {a}/>',
        f'<path d="M{PX+PW-165} {CY-dy:.1f} A91.5 91.5 0 0 0 {PX+PW-165} {CY+dy:.1f}" {a}/>',
        f'<rect x="{PX-24}" y="{CY-36.6}" width="24" height="73.2" {a}/>',
        f'<rect x="{PX+PW}" y="{CY-36.6}" width="24" height="73.2" {a}/>',
        f'<path d="M{PX+10} {PY} A10 10 0 0 0 {PX} {PY+10}" {a}/>',
        f'<path d="M{PX+PW-10} {PY} A10 10 0 0 1 {PX+PW} {PY+10}" {a}/>',
        f'<path d="M{PX} {PY+PH-10} A10 10 0 0 0 {PX+10} {PY+PH}" {a}/>',
        f'<path d="M{PX+PW} {PY+PH-10} A10 10 0 0 1 {PX+PW-10} {PY+PH}" {a}/>',
    ]
    return "\n".join(parts)


def stripes(c1, c2, n=12):
    w = PW / n
    return "\n".join(
        f'<rect x="{PX+i*w:.1f}" y="{PY}" width="{w:.1f}" height="{PH}" fill="{c1 if i%2 else c2}"/>' for i in range(n)
    )


def page(title, body, extra_style=""):
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  {FONTS}
  <style>
    body {{ margin: 0; background: #F4F1E8; }}
    a {{ color: #F36C21; }} a:hover {{ color: #c4531a; }}
    {extra_style}
  </style>
</helmet>
{body}
</x-dc>
</body>
</html>
"""


def caption(name, motivation, tradeoff):
    return f"""<div style="display: flex; flex-direction: column; gap: 6px; padding: 18px 24px 22px 24px; font-family: Archivo, 'Helvetica Neue', Arial, sans-serif; color: #151515;">
  <div style="font-family: Anton, Impact, 'Arial Narrow', sans-serif; font-size: 30px; letter-spacing: 0.01em; text-transform: uppercase;">{name}</div>
  <div style="font-size: 16px; line-height: 1.45;">{motivation}</div>
  <div style="font-size: 16px; line-height: 1.45; color: #6b5f52;">Trade-off: {tradeoff}</div>
</div>"""


def direction_a():
    body = []
    body.append(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" style="display: block; background: #EDE7D8;">')
    body.append(f'<rect x="{PX-14}" y="{PY-14}" width="{PW+28}" height="{PH+28}" fill="#173F35"/>')
    body.append(stripes("#1B4A3D", "#1E5243"))
    body.append(markings("#FFFFFF", 4, 0.92))
    bw = PW / 4
    for i, name in enumerate(BANDS):
        if i % 2:
            body.append(f'<rect x="{PX+i*bw:.1f}" y="{PY}" width="{bw:.1f}" height="{PH}" fill="#F4F1E8" fill-opacity="0.08"/>')
        tx = PX + i * bw + bw / 2
        body.append(f'<rect x="{tx-40}" y="{PY+8}" width="80" height="30" rx="3" fill="#151515" fill-opacity="0.85"/>')
        body.append(f'<text x="{tx}" y="{PY+29}" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="17" fill="#F4F1E8">{name}</text>')
    for x in DIVIDERS:
        body.append(f'<line x1="{x:.1f}" y1="{PY}" x2="{x:.1f}" y2="{PY+PH}" stroke="#151515" stroke-opacity="0.7" stroke-width="5" stroke-dasharray="20 12" stroke-linecap="round"/>')
    body.append(f'<path d="M720 170 L900 210" fill="none" stroke="#F36C21" stroke-width="8" stroke-linecap="round"/>')
    body.append(f'<path d="M260 150 L470 200" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-opacity="0.9"/>')
    body.append('<defs><filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity="0.45"/></filter></defs>')
    for n, x, y in PLAYERS:
        hi = n in (7, 2)
        r = 26 if hi else 22
        body.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F36C21" stroke="#151515" stroke-width="3" filter="url(#sh)"/>')
        if hi:
            body.append(f'<circle cx="{x}" cy="{y}" r="{r+6}" fill="none" stroke="#FFFFFF" stroke-width="3"/>')
        body.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="{26 if hi else 22}" fill="#FFFFFF">{n}</text>')
    bx = DIVIDERS[0] - 22
    body.append(f'<circle cx="{bx}" cy="330" r="13" fill="#FFFFFF" stroke="#151515" stroke-width="2.5" filter="url(#sh)"/>')
    body.append(f'<circle cx="{bx}" cy="330" r="4" fill="#151515"/>')
    body.append('<text x="900" y="245" font-family="Permanent Marker, cursive" font-size="26" fill="#F36C21" transform="rotate(-8 900 245)">Movement</text>')
    body.append('<text x="470" y="235" font-family="Permanent Marker, cursive" font-size="26" fill="#FFFFFF" transform="rotate(-8 470 235)">Cover</text>')
    body.append('</svg>')
    body.append(caption("A. Tactics board",
        "Deep restrained green with faint mowing stripes, painted white lines, and the departments drawn as grease pencil on top: charcoal dashed dividers, faint band tint, small black tags. Players are numbered orange magnetic discs. Orange only as filled shapes, never as text on green.",
        "the least scrapbook of the three; the paper mood has to come from the poster around it, not from the pitch itself."))
    return page("Tactics board", "\n".join(body))


def direction_b():
    body = []
    body.append(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" style="display: block; background: #EDE7D8;">')
    body.append('<defs><pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="14" stroke="#F4F1E8" stroke-opacity="0.22" stroke-width="2"/></pattern></defs>')
    body.append(f'<rect x="{PX-14}" y="{PY-14}" width="{PW+28}" height="{PH+28}" fill="#12352B"/>')
    body.append(markings("#F4F1E8", 4, 0.85))
    bw = PW / 4
    for i, name in enumerate(BANDS):
        if i % 2:
            body.append(f'<rect x="{PX+i*bw:.1f}" y="{PY}" width="{bw:.1f}" height="{PH}" fill="url(#hatch)"/>')
        tx = PX + i * bw + bw / 2
        body.append(f'<text x="{tx}" y="{PY+42}" text-anchor="middle" font-family="Permanent Marker, cursive" font-size="30" fill="#F4F1E8" transform="rotate(-4 {tx} {PY+42})">{name}</text>')
    for x in DIVIDERS:
        body.append(f'<line x1="{x:.1f}" y1="{PY}" x2="{x:.1f}" y2="{PY+PH}" stroke="#F4F1E8" stroke-width="4" stroke-linecap="round" stroke-opacity="0.9"/>')
    body.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#F4F1E8"/></marker><marker id="arro" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#F36C21"/></marker></defs>')
    body.append('<path d="M745 175 Q 830 170 895 205" fill="none" stroke="#F36C21" stroke-width="5" stroke-linecap="round" marker-end="url(#arro)"/>')
    body.append('<path d="M285 155 Q 380 160 465 195" fill="none" stroke="#F4F1E8" stroke-width="5" stroke-dasharray="12 10" stroke-linecap="round" marker-end="url(#arr)"/>')
    for n, x, y in PLAYERS:
        hi = n in (7, 2)
        if hi:
            body.append(f'<circle cx="{x}" cy="{y}" r="24" fill="#F36C21" stroke="#F4F1E8" stroke-width="3"/>')
            body.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="24" fill="#12352B">{n}</text>')
        else:
            body.append(f'<circle cx="{x}" cy="{y}" r="22" fill="#12352B" stroke="#F4F1E8" stroke-width="3.5"/>')
            body.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="22" fill="#F4F1E8">{n}</text>')
    bx = DIVIDERS[0] - 22
    body.append(f'<circle cx="{bx}" cy="330" r="12" fill="#F4F1E8"/>')
    body.append('<text x="905" y="245" font-family="Permanent Marker, cursive" font-size="26" fill="#F36C21" transform="rotate(-6 905 245)">Movement</text>')
    body.append('<text x="475" y="235" font-family="Permanent Marker, cursive" font-size="26" fill="#F4F1E8" transform="rotate(-6 475 235)">Cover</text>')
    body.append('</svg>')
    body.append(caption("B. Chalk on slate",
        "Flat, very dark green with chalk-white lines and handwriting, like a coach's board at half time. Only the two players in the story are orange; everyone else is an outline. Highest contrast of the three on a cheap projector, and the fewest visual layers to animate.",
        "no grass, no texture, least connected to the 1974 photographs; the orange is rationed so hard the pitch may feel cold next to the scrapbook."))
    return page("Chalk on slate", "\n".join(body))


def direction_c():
    body = []
    body.append(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" style="display: block; background: #EDE7D8;">')
    body.append(f'<rect x="{PX-10}" y="{PY-10}" width="{PW+20}" height="{PH+20}" fill="#F4F1E8" transform="rotate(-0.6 {CX} {CY})"/>')
    body.append(stripes("#2E7A3A", "#347F3E"))
    body.append(markings("#FFFFFF", 4, 0.95))
    bw = PW / 4
    for i, name in enumerate(BANDS):
        x0 = PX + i * bw
        body.append(f'<path d="M{x0+6:.1f} {PY+56} L{x0+bw-6:.1f} {PY+52} L{x0+bw-8:.1f} {PY+PH-40} L{x0+8:.1f} {PY+PH-36} Z" fill="#F4F1E8" fill-opacity="{0.42 if i%2 else 0.3}"/>')
        tx = x0 + bw / 2
        body.append(f'<rect x="{tx-52}" y="{PY+10}" width="104" height="34" fill="#F4F1E8" stroke="#c9bfa8" stroke-width="1" transform="rotate({-2 if i%2 else 2} {tx} {PY+27})"/>')
        body.append(f'<rect x="{tx-18}" y="{PY+4}" width="36" height="12" fill="#F36C21" fill-opacity="0.85" transform="rotate({-2 if i%2 else 2} {tx} {PY+27})"/>')
        body.append(f'<text x="{tx}" y="{PY+34}" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="18" fill="#151515" transform="rotate({-2 if i%2 else 2} {tx} {PY+27})">{name}</text>')
    body.append('<defs><marker id="pen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#C8321E"/></marker></defs>')
    body.append('<path d="M748 178 C 800 150, 850 230, 895 205" fill="none" stroke="#C8321E" stroke-width="4.5" stroke-linecap="round" marker-end="url(#pen)"/>')
    body.append('<path d="M288 158 C 350 130, 420 220, 465 195" fill="none" stroke="#C8321E" stroke-width="4.5" stroke-dasharray="10 8" stroke-linecap="round" marker-end="url(#pen)"/>')
    body.append('<defs><filter id="sh2" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="1" dy="3" stdDeviation="2.5" flood-color="#000" flood-opacity="0.5"/></filter></defs>')
    for n, x, y in PLAYERS:
        hi = n in (7, 2)
        r = 25 if hi else 22
        body.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F36C21" filter="url(#sh2)"/>')
        body.append(f'<circle cx="{x}" cy="{y}" r="{r-5}" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>')
        body.append(f'<text x="{x}" y="{y+7}" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="{22 if hi else 19}" fill="#FFFFFF">{n}</text>')
    bx = DIVIDERS[0] - 22
    body.append(f'<circle cx="{bx}" cy="330" r="13" fill="#7A4A1E" stroke="#3b2410" stroke-width="2" filter="url(#sh2)"/>')
    body.append(f'<path d="M{bx-6} 326 L{bx+5} 323 L{bx+7} 334 L{bx-4} 337 Z" fill="none" stroke="#3b2410" stroke-width="1.5"/>')
    body.append('<text x="905" y="248" font-family="Permanent Marker, cursive" font-size="26" fill="#C8321E" transform="rotate(-8 905 248)">Movement</text>')
    body.append('<text x="475" y="238" font-family="Permanent Marker, cursive" font-size="26" fill="#C8321E" transform="rotate(-8 475 238)">Cover</text>')
    body.append('</svg>')
    body.append(caption("C. Scrapbook overlay",
        "The brighter grass of the pitch reference, sitting slightly askew on paper. Departments are strips of translucent paper with typed labels taped on. Movement and cover are red pen arrows, like the map in the mood board. A leather ball. Closest to bg1 in spirit.",
        "the busiest and the lowest contrast: red pen on bright green is the combination the projector research warns about, and every animated element has a paper texture to manage."))
    return page("Scrapbook overlay", "\n".join(body))


def wire(title, boxes, motivation, tradeoff, pitch):
    w, h = 1400, 788
    body = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" style="display: block; background: #F4F1E8;">']
    body.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#F4F1E8"/>')
    px, py, pw, ph = pitch
    body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#173F35"/>')
    body.append(f'<rect x="{px+8}" y="{py+8}" width="{pw-16}" height="{ph-16}" fill="none" stroke="#F4F1E8" stroke-width="2" stroke-opacity="0.8"/>')
    body.append(f'<line x1="{px+pw/2}" y1="{py+8}" x2="{px+pw/2}" y2="{py+ph-8}" stroke="#F4F1E8" stroke-width="2" stroke-opacity="0.8"/>')
    body.append(f'<circle cx="{px+pw/2}" cy="{py+ph/2}" r="{ph*0.13}" fill="none" stroke="#F4F1E8" stroke-width="2" stroke-opacity="0.8"/>')
    for (x, y, bw, bh, label, kind) in boxes:
        if kind == "photo":
            body.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="#c9c2b4" stroke="#151515" stroke-width="2"/>')
            body.append(f'<line x1="{x}" y1="{y}" x2="{x+bw}" y2="{y+bh}" stroke="#151515" stroke-width="1" stroke-opacity="0.4"/>')
            body.append(f'<line x1="{x+bw}" y1="{y}" x2="{x}" y2="{y+bh}" stroke="#151515" stroke-width="1" stroke-opacity="0.4"/>')
        elif kind == "card":
            body.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="#FBF8F0" stroke="#151515" stroke-width="2" stroke-dasharray="6 4"/>')
        elif kind == "title":
            body.append(f'<text x="{x+bw/2}" y="{y+bh*0.55}" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="{bh*0.6}" fill="#151515">TOTAL FOOTBALL</text>')
            body.append(f'<line x1="{x+bw*0.28}" y1="{y+bh*0.58}" x2="{x+bw*0.78}" y2="{y+bh*0.42}" stroke="#F36C21" stroke-width="{bh*0.09}" stroke-linecap="round"/>')
            body.append(f'<text x="{x+bw*0.62}" y="{y+bh*0.95}" text-anchor="middle" font-family="Permanent Marker, cursive" font-size="{bh*0.42}" fill="#F36C21" transform="rotate(-6 {x+bw*0.62} {y+bh*0.95})">Engineering</text>')
            continue
        elif kind == "clutter":
            body.append(f'<ellipse cx="{x+bw/2}" cy="{y+bh/2}" rx="{bw/2}" ry="{bh/2}" fill="#d8d0bf" stroke="#151515" stroke-width="1.5" stroke-opacity="0.6"/>')
        body.append(f'<text x="{x+bw/2}" y="{y+bh/2+5}" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="500" font-size="15" fill="#151515">{label}</text>')
    body.append('</svg>')
    body.append(caption(title, motivation, tradeoff))
    return page(title, "\n".join(body))


def layout_sparse():
    boxes = [
        (400, 20, 600, 100, "", "title"),
        (60, 190, 200, 140, "1974 archive photo", "photo"),
        (60, 460, 220, 160, "First creation", "photo"),
        (1160, 190, 190, 130, "Beck note", "card"),
        (1160, 360, 190, 150, "House rules", "card"),
        (1130, 560, 230, 170, "Sprint card", "card"),
        (300, 720, 120, 40, "tape", "clutter"),
        (1000, 730, 90, 36, "tulip", "clutter"),
    ]
    return wire("1. Spacious editorial", boxes,
        "The proposal's layout. Six places with wide paper margins between them, so every close view is clean and the pitch is the only dense object. Scrapbook objects only in the gaps.",
        "reads calmer than the mood board; some of bg1's warmth is lost, and the empty paper must carry texture well or it looks unfinished.",
        (330, 160, 740, 480))


def layout_dense():
    boxes = [
        (430, 15, 540, 90, "", "title"),
        (30, 130, 230, 150, "1974 photo", "photo"),
        (40, 300, 130, 90, "ticket", "clutter"),
        (30, 410, 230, 150, "First creation", "photo"),
        (60, 590, 180, 120, "map", "photo"),
        (280, 620, 200, 130, "postcard", "photo"),
        (1110, 120, 250, 150, "stadium photo", "photo"),
        (1160, 290, 200, 120, "Beck note", "card"),
        (1130, 430, 230, 150, "House rules", "card"),
        (1110, 600, 250, 150, "Sprint card", "card"),
        (520, 660, 330, 110, "notebook / sketches", "card"),
        (880, 640, 200, 120, "boots", "clutter"),
        (280, 120, 120, 60, "tape", "clutter"),
        (990, 20, 110, 70, "pennant", "clutter"),
    ]
    return wire("2. Scrapbook wall", boxes,
        "The bg1 mood taken literally: objects edge to edge, the pitch as one object among many. Strongest at the overview, and the closest to the reference you liked.",
        "every close view has neighbours bleeding in, there is nowhere to put new elements, and the eye has no rest at the final pullback; most of the photos would have to be real to be honest.",
        (420, 130, 660, 470))


def layout_pitch():
    boxes = [
        (450, 10, 500, 80, "", "title"),
        (40, 120, 160, 110, "1974 photo", "photo"),
        (40, 560, 170, 130, "First creation", "photo"),
        (1200, 120, 160, 110, "Beck note", "card"),
        (1200, 330, 160, 130, "House rules", "card"),
        (1190, 560, 170, 140, "Sprint card", "card"),
        (240, 720, 90, 30, "tape", "clutter"),
    ]
    return wire("3. Pitch dominant", boxes,
        "The pitch takes three quarters of the width and everything else is small and marginal, like notes pinned around a tactics board. The talk is mostly on the pitch anyway, so the overview shows what the talk was about.",
        "the side places are small at the overview and need deeper zooms to read, which means larger camera moves; the first creation and Beck note feel like footnotes.",
        (230, 105, 940, 600))


(OUT / "SpaciousEditorial.dc.html").write_text(layout_sparse())
(OUT / "ScrapbookWall.dc.html").write_text(layout_dense())
(OUT / "PitchDominant.dc.html").write_text(layout_pitch())
print("ok")


def direction_d():
    IW, IH = 1200, 675
    ix0, iy0, ix1, iy1 = 30, 30, 1170, 640
    def mp(x, y):
        return ix0 + (x - PX) / PW * (ix1 - ix0), iy0 + (y - PY) / PH * (iy1 - iy0)
    body = []
    import base64
    b64 = base64.b64encode((OUT / "grass.jpg").read_bytes()).decode()
    body.append(f'<div style="position: relative; width: {IW}px; height: {IH}px; overflow: hidden; background: #2E7A3A;">')
    body.append(f'<img src="data:image/jpeg;base64,{b64}" alt="" style="position: absolute; left: 0; top: 0; width: {IW}px; height: {IH}px; object-fit: cover; display: block;">')
    body.append(f'<svg viewBox="0 0 {IW} {IH}" width="{IW}" height="{IH}" xmlns="http://www.w3.org/2000/svg" style="display: block; position: absolute; left: 0; top: 0;">')
    body.append('<defs><filter id="sh3" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="3.5" flood-color="#000" flood-opacity="0.55"/></filter></defs>')
    bw = (ix1 - ix0) / 4
    for i, name in enumerate(BANDS):
        if i % 2:
            body.append(f'<rect x="{ix0+i*bw:.1f}" y="{iy0}" width="{bw:.1f}" height="{iy1-iy0}" fill="#151515" fill-opacity="0.16"/>')
        tx = ix0 + i * bw + bw / 2
        body.append(f'<rect x="{tx-42}" y="{iy0+10}" width="84" height="32" rx="3" fill="#151515" fill-opacity="0.85"/>')
        body.append(f'<text x="{tx}" y="{iy0+32}" text-anchor="middle" font-family="Archivo, Arial, sans-serif" font-weight="700" font-size="18" fill="#F4F1E8">{name}</text>')
    for q in (0.25, 0.5, 0.75):
        x = ix0 + (ix1 - ix0) * q
        body.append(f'<line x1="{x:.1f}" y1="{iy0}" x2="{x:.1f}" y2="{iy1}" stroke="#151515" stroke-opacity="0.75" stroke-width="5" stroke-dasharray="20 12" stroke-linecap="round"/>')
    x7, y7 = mp(720, 170); x2, y2 = mp(260, 150)
    body.append(f'<path d="M{x7:.0f} {y7:.0f} L{x7+190:.0f} {y7+40:.0f}" fill="none" stroke="#F36C21" stroke-width="8" stroke-linecap="round" filter="url(#sh3)"/>')
    body.append(f'<path d="M{x2:.0f} {y2:.0f} L{x2+220:.0f} {y2+45:.0f}" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" filter="url(#sh3)"/>')
    for n, x, y in PLAYERS:
        px, py = mp(x, y)
        hi = n in (7, 2)
        r = 26 if hi else 22
        body.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r}" fill="#F36C21" stroke="#151515" stroke-width="3" filter="url(#sh3)"/>')
        if hi:
            body.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r+6}" fill="none" stroke="#FFFFFF" stroke-width="3"/>')
        body.append(f'<text x="{px:.0f}" y="{py+8:.0f}" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="{26 if hi else 22}" fill="#FFFFFF">{n}</text>')
    bx, by = mp(DIVIDERS[0] - 22, 330)
    body.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="13" fill="#FFFFFF" stroke="#151515" stroke-width="2.5" filter="url(#sh3)"/>')
    body.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="4" fill="#151515"/>')
    body.append(f'<text x="{x7+195:.0f}" y="{y7+80:.0f}" font-family="Permanent Marker, cursive" font-size="26" fill="#F36C21" stroke="#151515" stroke-width="4" paint-order="stroke" transform="rotate(-8 {x7+195:.0f} {y7+80:.0f})">Movement</text>')
    body.append(f'<text x="{x2+225:.0f}" y="{y2+30:.0f}" font-family="Permanent Marker, cursive" font-size="26" fill="#FFFFFF" stroke="#151515" stroke-width="4" paint-order="stroke" transform="rotate(-8 {x2+225:.0f} {y2+30:.0f})">Cover</text>')
    body.append('</svg></div>')
    body.append(caption("Pitch stage: real grass",
        "Your pitch.png as the ground, untouched, with the same grease-pencil departments, orange discs and trails laid over it as vector. This is what the build actually does: photographic texture underneath, everything that moves or reads on top. The most literal pitch of the four.",
        "the grass is mid-tone and busy, so every label needs a dark outline and the thin white lines will soften at deep zoom unless redrawn as vector; the texture also has to be masked into the paper edge rather than ending in a hard rectangle."))
    return page("Real grass", "\n".join(body))


(OUT / "Main.dc.html").write_text(direction_d())
