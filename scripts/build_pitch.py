from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "talk" / "index.html"
START, END = "<!-- pitch:start -->", "<!-- pitch:end -->"

SVG_LEFT, SVG_TOP, SVG_W, SVG_H = 1500, 850, 4000, 2220
L, R, T, B = 155, 3847, 151, 2068
CX, CY = 1999, 1109
OLD = (39, 1633, 39, 890)
K = (R - L) / (OLD[1] - OLD[0])
BAND_W = (R - L) / 4


def X(x):
    return round(L + (x - OLD[0]) * K)


def Y(y):
    return round(T + (y - OLD[2]) * (B - T) / (OLD[3] - OLD[2]))


def S(v):
    return round(v * K)
DIVIDERS = [L + BAND_W * i for i in (1, 2, 3)]
BANDS = [("devops", "DevOps"), ("qa", "QA"), ("be", "BE"), ("fe", "FE")]

PLAYERS = [
    ("p8", 8, "Jongbloed", 117, 470),
    ("p20", 20, "Suurbier", 404, 146),
    ("p17", 17, "Rijsbergen", 360, 388),
    ("p2", 2, "Haan", 360, 553),
    ("p12", 12, "Krol", 404, 795),
    ("p6", 6, "Jansen", 710, 291),
    ("p13", 13, "Neeskens", 655, 470),
    ("p3", 3, "Van Hanegem", 710, 650),
    ("p16", 16, "Rep", 1156, 184),
    ("p14", 14, "Cruyff", 1240, 470),
    ("p15", 15, "Rensenbrink", 1156, 757),
]
SHIRT = "M-30 -46 L-12 -54 Q0 -50 12 -54 L30 -46 L44 -28 L30 -18 L26 -24 L26 26 L-26 26 L-26 -24 L-30 -18 L-44 -28 Z"
SHORTS = "M-27 24 L27 24 L30 58 L4 60 L0 44 L-4 60 L-30 58 Z"

LINE = 'fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.95" stroke-linecap="round"'


def markings():
    return "\n".join([
        f'<rect x="{L}" y="{T}" width="{R-L}" height="{B-T}" {LINE}/>',
        f'<line x1="{CX}" y1="{T}" x2="{CX}" y2="{B}" {LINE}/>',
        f'<circle cx="{CX}" cy="{CY}" r="147" {LINE}/>',
        f'<rect x="{L}" y="211" width="224" height="470" {LINE}/>',
        f'<rect x="{R-224}" y="211" width="224" height="470" {LINE}/>',
        f'<rect x="{L}" y="318" width="79" height="250" {LINE}/>',
        f'<rect x="{R-79}" y="318" width="79" height="250" {LINE}/>',
        f'<path d="M263 356 A173 173 0 0 1 263 572" {LINE}/>',
        f'<path d="M{R-224} 356 A173 173 0 0 0 {R-224} 572" {LINE}/>',
        f'<rect x="7" y="368" width="32" height="150" {LINE}/>',
        f'<rect x="{R}" y="368" width="32" height="150" {LINE}/>',
    ])


def bands():
    out = ['<g id="bands">']
    for i, (key, label) in enumerate(BANDS):
        x0 = L + BAND_W * i
        fill = '#151515" fill-opacity="0.16' if i % 2 else '#F4F1E8" fill-opacity="0.10'
        out.append(f'<g data-obj="band-{key}" class="band">')
        out.append(f'<rect x="{x0:.1f}" y="{T}" width="{BAND_W:.1f}" height="{B-T}" fill="{fill}"/>')
        if i:
            out.append(f'<line x1="{x0:.1f}" y1="{T}" x2="{x0:.1f}" y2="{B}" class="divider"/>')
        tx = x0 + BAND_W / 2
        out.append(f'<rect x="{tx-S(70):.1f}" y="{T+S(16)}" width="{S(140)}" height="{S(52)}" rx="{S(4)}" fill="#151515" fill-opacity="0.88"/>')
        out.append(f'<text x="{tx:.1f}" y="{T+S(54)}" class="tag">{label}</text>')
        out.append('</g>')
    out.append('</g>')
    return "\n".join(out)


def players():
    out = ['<g id="players">']
    for key, num, name, x, y in PLAYERS:
        cls = "player gk" if num == 8 else "player"
        out.append(f'<g data-obj="{key}" class="{cls}" style="--hx: {X(x)}px; --hy: {Y(y)}px;">')
        out.append(f'<circle r="{S(50)}" class="halo mover"/>')
        out.append(f'<circle r="{S(50)}" class="halo cover"/>')
        out.append(f'<path d="{SHORTS}" transform="scale(1.9)" class="shorts"/>')
        out.append(f'<path d="{SHIRT}" transform="scale(1.9)" class="shirt"/>')
        out.append(f'<text y="{S(4)}" class="num">{num}</text>')
        out.append(f'<text y="{S(90)}" class="name">{name}</text>')
        out.append(f'<text y="{S(90)}" class="role">engineer</text>')
        out.append('</g>')
    out.append('</g>')
    return "\n".join(out)


def P(d):
    def conv(m):
        return f"{X(float(m.group(1)))} {Y(float(m.group(2)))}"
    import re as _re
    return _re.sub(r"(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)", conv, d)


POS = {k: (x, y) for k, _, _, x, y in PLAYERS}
CHAIN_ORDER = ["p8", "p12", "p3", "p13", "p20", "p6", "p16", "p14"]


def chain_path():
    pts = [POS[k] for k in CHAIN_ORDER] + [(1520, 430)]
    return "M" + " L".join(f"{x} {y}" for x, y in pts)


def trails():
    chain = P(chain_path())
    return "\n".join([
        '<g id="trails">',
        f'<path data-obj="chain" class="trail chain" pathLength="1" d="{chain}"/>',
        f'<path data-obj="trail-move" class="trail move" pathLength="1" d="{P("M404 146 L910 146")}"/>',
        f'<path data-obj="trail-cover" class="trail cover" pathLength="1" d="{P("M655 470 L470 200")}"/>',
        '<g data-obj="possibilities" class="possibilities">',
        f'<path class="dotted" pathLength="1" d="{P("M1240 470 Q1370 300 1500 260")}"/>',
        f'<path class="dotted" pathLength="1" d="{P("M1240 470 Q1420 480 1550 540")}"/>',
        f'<path class="dotted" pathLength="1" d="{P("M1240 470 Q1320 700 1480 760")}"/>',
        '</g>',
        f'<path data-obj="chosen" class="trail move" pathLength="1" d="{P("M1240 470 Q1370 300 1500 260")}"/>',
        f'<path data-obj="support-trail" class="trail cover" pathLength="1" d="{P("M1156 184 L1370 200")}"/>',
        '</g>',
    ])


BALL_ART = '<image href="img/ball.png" x="-52" y="-52" width="104" height="104"/>'


def ball():
    chain = P(chain_path())
    return "\n".join([
        f'<g id="ballg" data-obj="ball" class="ball" style="--hx: {X(150)}px; --hy: {Y(600)}px;">',
        BALL_ART,
        '</g>',
        f'<g id="ball-flight" data-obj="ball-flight" class="ball flight" style="offset-path: path(\'{chain}\');">',
        BALL_ART,
        '</g>',
    ])


def labels():
    return "\n".join([
        '<g id="labels">',
        f'<text data-obj="lbl-movement" x="{X(870)}" y="{Y(110)}" class="hand-lbl orange">Movement</text>',
        f'<text data-obj="lbl-cover" x="{X(380)}" y="{Y(170)}" class="hand-lbl white">Cover</text>',
        f'<text data-obj="lbl-ai" x="{X(1180)}" y="{Y(240)}" class="hand-lbl white">AI assistance</text>',
        '</g>',
    ])


def mirrors():
    ids = ["names1974", "word-engineer", "move-suurbier", "cover-neeskens", "support", "mark-1", "wave-1", "mark-2", "wave-2", "mark-3", "wave-3", "four-line"]
    balls = ["ball-at-cruyff", "ball-at-fe", "ball-at-be-line", "ball-at-qa-line", "ball-start", "ball-w1", "ball-w2", "ball-w3"]
    ticket_ids = ["ticket-at-be", "ticket-at-qa", "ticket-at-ops", "ticket-at-done"]
    eng_ids = ["eng-mark-fe", "eng-move-fe", "eng-mark-be"]
    out = [f'<span data-obj="{i}" data-mirror="players" hidden></span>' for i in ids]
    out += [f'<span data-obj="{i}" data-mirror="ballg" hidden></span>' for i in balls]
    out += [f'<span data-obj="{i}" data-mirror="ticketg" hidden></span>' for i in ticket_ids]
    out += [f'<span data-obj="{i}" data-mirror="engs" hidden></span>' for i in eng_ids]
    return "\n".join(out)


def fragment():
    return "\n".join([
        START,
        f'<svg id="pitch" data-obj="pitch" class="place" viewBox="0 0 {SVG_W} {SVG_H}" overflow="visible" style="left: {SVG_LEFT}px; top: {SVG_TOP}px; width: {SVG_W}px; height: {SVG_H}px;">',
        '<defs>',
        '<filter id="disc-shadow" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="7" stdDeviation="7" flood-color="#000" flood-opacity="0.5"/></filter>',
        '</defs>',
        bands(), trails(), players(), ball(), labels(),
        '</svg>',
        mirrors(),
        END,
    ])


def main():
    html = INDEX.read_text()
    if START in html:
        pre, rest = html.split(START, 1)
        _, post = rest.split(END, 1)
    else:
        marker = '<div class="place placeholder" data-obj="pitch"'
        pre, rest = html.split(marker, 1)
        _, post = rest.split("</div>", 1)
    INDEX.write_text(pre + fragment() + post)
    print("pitch fragment written")


if __name__ == "__main__":
    main()
