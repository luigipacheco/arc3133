# -*- coding: utf-8 -*-
"""ARC3133 Class 04 — Module 1: Tiling + Arrays"""
import math
from nb import *
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Pt

d = Deck()

# ─────────────────────────────── 1 · TITLE
s = d.slide(LIME)
s.title_slide(
    "CLASS 04  /  SEP 15",
    ["MODULE 1 — FIELDS", "TILING + ARRAYS"],
    "BRING YOUR PRECEDENT — WE MODEL IT TODAY",
    "0.1 DUE",
    "1.1 ISSUED TODAY  /  TILING + ARRAYS",
)

# ─────────────────────────────── 2 · WHERE WE JUST MOVED TO
s = d.slide(BLACK)
s.header("WHERE WE JUST MOVED TO", "Module 0 is finished. The ground has changed.")
s.panel(L, 2.05, 5.85, 3.35, "MODULE 0 — DONE", headfill=MUTE)
s.t(L + 0.3, 2.75, 5.25, 0.4, [s.Ab("PROCEDURAL", 13)])
s.t(L + 0.3, 3.2, 5.25, 2.0, [
    s.Cb("A fixed sequence of operations.", 14.5),
    s.Cb("You defined the steps.", 14.5),
    s.Cb("One expected result.", 14.5)], ls=1.45)
s.panel(6.8, 2.05, 5.85, 3.35, "MODULES 1–3 — NOW", headfill=LIME)
s.t(7.1, 2.75, 5.25, 0.4, [s.Ab("PARAMETRIC", 13)])
s.t(7.1, 3.2, 5.25, 2.0, [
    s.Cb("Relationships between inputs and form.", 14.5),
    s.Cb("You define the rules of variation.", 14.5),
    s.Cb("A family — you know the range,", 14.5),
    s.Cb("not each member.", 14.5)], ls=1.45)
s.banner(5.75, "An array on its own is still procedural — repeat this N times. It becomes parametric "
              "the moment a parameter governs how the copies differ.", fill=YELLOW, h=0.72)

# ─────────────────────────────── 3 · AN ARRAY IS A LIST OF POSITIONS
s = d.slide(CREAM)
s.header("AN ARRAY IS A LIST OF POSITIONS",
         "Not a command that duplicates things. A list you compute, then place geometry at.")
s.panel(L, 1.95, 5.6, 3.5, "INDEX  →  POSITION", headfill=CYAN)
s.t(L + 0.35, 2.75, 5.0, 2.4, [
    s.Mb("i = 0   →   p = start", 13.5),
    s.Mb("i = 1   →   p = start + step", 13.5),
    s.Mb("i = 2   →   p = start + 2 × step", 13.5),
    s.Mb("i = 3   →   p = start + 3 × step", 13.5),
    s.Mb(" ", 8),
    s.Mb("p[i] = start + i × step", 13.5, bold=True)], ls=1.35)
s.panel(6.6, 1.95, 6.05, 3.5, "YOU ALREADY KNOW THIS", headfill=PINK)
s.t(6.9, 2.72, 5.45, 2.5, [
    s.Cb("Move is addition. An array is move, repeated, with the amount driven by the index.", 14.5),
    s.Cb(" ", 7),
    s.Cb("The index is the only new idea: a counter that tells each copy how far along the "
         "sequence it is — and therefore how different it should be.", 14.5)], ls=1.3)
s.banner(5.75, "The index is what makes variation possible. Without it every copy is the same copy.",
         fill=LIME, h=0.72)

# ─────────────────────────────── 4 · A TESSELLATION IS A MODULE PLUS A RULE
s = d.slide(CREAM)
s.header("A TILING IS ONE TILE PLUS A RULE",
         "Escher fills a plane with the same shape, over and over. So does a brick wall.")
cards = [
    ("THE TILE", CYAN, "One part, repeated. A panel, a brick, a shingle. Simple on purpose — "
                       "it is about to be copied a thousand times."),
    ("THE RULE", LIME, "How copies are placed relative to each other. Spacing, offset, "
                       "rotation, course. Say it in one sentence."),
    ("THE SEAM", YELLOW, "Where two copies meet. A tile that tiles resolves at the seam. "
                         "One that merely repeats leaves a gap or a collision."),
    ("ALWAYS THE SAME", PINK, "Every copy is identical. Panels that change shape across a "
                              "curved surface are Module 3 — a different, harder problem."),
]
x = L
for name, col, body in cards:
    s.panel(x, 1.95, 2.85, 3.5, name, headfill=col, tsize=15)
    s.t(x + 0.25, 2.75, 2.35, 2.5, [s.Cb(body, 13)], ls=1.3)
    x += 3.05
s.banner(5.75, "IF YOU CANNOT DRAW ONE TILE AND SAY HOW THE NEXT ONE SITS AGAINST IT, YOU DO NOT HAVE A TILING.",
         fill=BLACK, color=CYAN, h=0.72, align=PP_ALIGN.CENTER)

# ─────────────────────────────── 5 · FINDING THE MODULE
s = d.slide(BLACK)
s.header("FROM FAÇADE TO TILE", "You brought the building. Four steps to get from it to one small object.")
steps = [
    ("01", "FLATTEN THE ELEVATION",
     "One photograph, straight on. Perspective hides the repeat — correct it or find a drawing."),
    ("02", "OUTLINE THE REPEATED PART",
     "Slide a rectangle across the façade until it lands on itself. Inside it is the part you are after."),
    ("03", "DIMENSION IT",
     "Width, height, depth, and how the next one sits against it. Real millimetres, from a drawing or a scale figure."),
    ("04", "DESIGN YOUR OWN",
     "Not a trace. Your tile, driven by theirs. Three to five primitives, at the origin, manifold, closed."),
]
y = 2.0
for n, ttl, body in steps:
    s.chip(L, y, 0.85, 0.95, n, fill=LIME, size=17)
    s.card(L + 1.15, y, W - 1.15, 0.95, fill=CREAM)
    s.t(L + 1.45, y + 0.13, W - 1.75, 0.35, [s.Ab(ttl, 13.5)])
    s.t(L + 1.45, y + 0.5, W - 1.75, 0.35, [s.Cb(body, 13)])
    y += 1.1
s.banner(6.5, "EVERY FACE YOU ADD IS PAID FOR A THOUSAND TIMES. KEEP THE TILE CHEAP.",
         fill=PINK, h=0.62, size=12.5)

# ─────────────────────────────── 6 · FOUR ARRAYS
s = d.slide(CREAM)
s.header("FOUR ARRAYS, PICK THREE", "Same tile, four ways of generating the list of positions. You build three.")

CW, CH, CY = 2.85, 3.5, 1.95
xs = [L, L + 3.05, L + 6.10, L + 9.15]
names = ["CARTESIAN", "RADIAL", "HEXAGONAL", "ON CURVE"]
cols = [CYAN, PINK, LIME, YELLOW]
formulas = ["p[i][j] = p₀ + (i·dx, j·dy)", "p[i] = c + r·(cos θ, sin θ)",
            "offset odd rows by dx/2", "p[i] = curve at t = i/n"]
for x, nm, col, fm in zip(xs, names, cols, formulas):
    s.panel(x, CY, CW, CH, nm, headfill=col, tsize=14.5)
    s.t(x + 0.22, CY + 2.85, CW - 0.44, 0.5,
        [s.Mb(fm, 10.5)], anchor=MSO_ANCHOR.MIDDLE)

# diagram: cartesian
gx, gy = xs[0] + 0.55, CY + 0.95
for i in range(6):
    for j in range(5):
        s.dot(gx + i * 0.34, gy + j * 0.34)
# diagram: radial
cx, cy = xs[1] + 1.42, CY + 1.72
for rr in (0.44, 0.80, 1.16):
    for k in range(96):
        a = 2 * math.pi * k / 96.0
        s.dot(cx + rr * math.cos(a), cy + rr * math.sin(a), d=0.022, fill=MUTE)
for rr in (0.44, 0.80, 1.16):
    for k in range(12):
        a = 2 * math.pi * k / 12.0 - math.pi / 2
        s.dot(cx + rr * math.cos(a), cy + rr * math.sin(a), d=0.105)
s.dot(cx, cy, d=0.16, fill=PINK)
# diagram: hexagonal
hx, hy = xs[2] + 0.45, CY + 0.95
for j in range(5):
    off = 0.17 if j % 2 else 0.0
    for i in range(6 if j % 2 == 0 else 5):
        s.dot(hx + off + i * 0.34, hy + j * 0.34)
# diagram: on curve
ax, ay = xs[3] + 0.30, CY + 1.05
for k in range(49):
    t = k / 48.0
    s.dot(ax + t * 2.25, ay + 0.95 + 0.85 * math.sin(t * math.pi) * -1 + 0.85,
          d=0.028, fill=MUTE)
for k in range(9):
    t = k / 8.0
    s.dot(ax + t * 2.25, ay + 0.95 + 0.85 * math.sin(t * math.pi) * -1 + 0.85,
          d=0.12, fill=YELLOW)
s.banner(5.75, "A cartesian array is a list of lists — two counters instead of one. "
              "Hold that thought; it returns in Module 3 as a panel field.", fill=CYAN, h=0.72)

# ─────────────────────────────── 7 · REPETITION IS NOT THE POINT
s = d.slide(BLACK)
s.header("THE TILE IS CONSTANT. THE FIELD IS NOT.",
         "The same tile, the same array, twice. One is wallpaper. The other is a system.", tsize=30)
s.panel(L, 2.05, 5.85, 3.4, "PROCEDURAL", headfill=MUTE)
s.t(L + 0.3, 2.72, 5.25, 0.35, [s.Ab("REPETITION", 13)])
gx, gy = L + 0.55, 3.35
for i in range(9):
    for j in range(4):
        s.dot(gx + i * 0.55, gy + j * 0.5, d=0.20)
s.t(L + 0.3, 4.98, 5.25, 0.35, [s.Cb("Same tile, same spacing. The index is generated and then ignored.", 12)])
s.panel(6.8, 2.05, 5.85, 3.4, "PARAMETRIC", headfill=LIME)
s.t(7.1, 2.72, 5.25, 0.35, [s.Ab("VARIATION", 13)])
gx = 7.05
for i in range(9):
    for j in range(4):
        sz = 0.07 + 0.032 * (i + j * 0.7)
        s.dot(gx + i * 0.55, gy + j * 0.5, d=min(sz, 0.30))
s.t(7.1, 4.98, 5.25, 0.35, [s.Cb("Same tile — scale, rotation and culling driven by the index.", 12)])
s.banner(6.15, "YOU MAY NOT MODEL A SECOND TILE. EVERYTHING THAT VARIES, VARIES IN THE ARRAY.",
         fill=PINK, h=0.68)

# ─────────────────────────────── 8 · TESSELLATED FAÇADES
s = d.slide(CREAM)
s.header("TILED FAÇADES", "Look for the part and the rule, not the image.")
imgs = [("SCREEN / MASHRABIYA", "Add: a perforated screen built from one repeated block."),
        ("BRICK BOND", "Add: a brick or block wall where the bond is the whole design."),
        ("CAST PANEL", "Add: a façade of one repeated cast or folded panel.")]
x = L
for ttl, cap in imgs:
    s.card(x, 1.95, 3.85, 2.45, fill=PAPER)
    s.t(x + 0.25, 1.95, 3.35, 2.45, [s.Cb(cap, 12.5, GREY)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    s.chip(x, 4.5, 3.85, 0.5, ttl, fill=LIME, size=11)
    x += 4.08
s.panel(L, 5.35, W, 1.5, "FOR YOUR PRECEDENT, ANSWER THREE QUESTIONS", headfill=YELLOW, tsize=14)
qs = ["What is the tile?", "What rule places the copies?", "Where do two of them meet?"]
qx = L + 0.35
for q in qs:
    s.t(qx, 6.05, 3.7, 0.5, [s.Cb(q, 14.5, bold=True)], anchor=MSO_ANCHOR.MIDDLE)
    qx += 3.85

# ─────────────────────────────── 9 · ISSUED TODAY
s = d.slide(BLACK)
s.issued("ISSUED TODAY", "1.1 — TILING + ARRAYS", "DUE CLASS 6 — SEP 29   /   7%",
         "You brought a façade made of one repeated part. Design your own tile from it, model it once, then tile "
         "the plane three ways. The precedent drives the tile; you supply the systems that place it and the "
         "parameter that makes the field differ. No attractors in this one — that is next week.")
stages = [("STAGE 1", "THE PRECEDENT", "The building, the repeated part, the rule. Measured drawing.", CYAN),
          ("STAGE 2", "THE TILE", "Your design, from theirs. 3–5 primitives, at the origin, manifold.", LIME),
          ("STAGE 3", "THREE ARRAYS", "Any three of cartesian, radial, hexagonal, on curve.", YELLOW)]
x = L
for tag, ttl, body, col in stages:
    s.chip(x, 3.85, 3.85, 0.45, tag, fill=col, size=11)
    s.card(x, 4.4, 3.85, 1.55, fill=CREAM)
    s.t(x + 0.28, 4.58, 3.3, 0.35, [s.Ab(ttl, 14)])
    s.t(x + 0.28, 5.0, 3.3, 0.85, [s.Cb(body, 12.5)], ls=1.25)
    x += 4.08
s.banner(6.25, "ONE TILE.  THREE ARRAYS, YOUR CHOICE WHICH.  EVERYTHING THAT VARIES, VARIES IN THE ARRAY.",
         fill=YELLOW, h=0.68, align=PP_ALIGN.CENTER)

# ─────────────────────────────── 10 · REQUIREMENTS
s = d.slide(CREAM)
s.header("REQUIREMENTS", "Counting these earns a C. The rest is judgement.")
reqs = [("1", "precedent analysis — building, repeated part, rule, in 3–4 sentences with a measured drawing", YELLOW),
        ("1", "tile designed from that precedent — 3–5 primitives, manifold, at the origin, dimensioned", YELLOW),
        ("3", "array types built with that tile, from cartesian, radial, hexagonal, along a curve", LIME),
        ("3", "finished compositions — one per array type", LIME),
        ("1,000+", "elements in at least one composition", CYAN),
        ("1+", "conditional that removes or alters a subset based on a tested property", CYAN),
        ("1+", "array where changing element order visibly changes the result — paired before/after", CYAN),
        ("1+", "composition resolved spatially in 3D", CYAN),
        ("2", "sheets minimum, 17\" × 11\", in your visual identity", PINK)]
y = 1.85
for chip, body, col in reqs:
    s.numrow(y, chip, body, chipfill=col, h=0.46, csize=12, size=13.5)
    y += 0.545
s.banner(6.78, "One tile only. Arrays authored from base components — array add-ons and scatter tools are prohibited.",
         fill=PINK, h=0.6, size=12.5)

# ─────────────────────────────── 11 · NOW
s = d.slide(CYAN)
s.header("NOW — DESIGN YOUR TILE", tsize=33)
s.t(L, 1.85, 11.5, 0.4, [s.Cb("Rest of the session: part dimensioned, tile modeled, first array running.", 16)])
rows = ["Precedent approved — a façade made of one repeated part",
        "The part outlined over the elevation, with dimensions",
        "Your tile modeled — one object, at the origin, manifold, 3–5 primitives",
        "Your first array running, count and spacing controllable",
        "One property driven by the index, so the field is not wallpaper"]
y = 2.55
for r in rows:
    s.checkrow(y, r)
    y += 0.78
s.card(L, 6.55, 8.2, 0.62, fill=BLACK)
s.t(L, 6.55, 8.2, 0.62, [s.Ab("LEAVE WITH A TILE. THE ARRAYS ARE THE EASY PART.", 13, CYAN)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ─────────────────────────────── 12 · BEFORE NEXT CLASS
s = d.slide(CREAM)
s.header("BEFORE NEXT CLASS")
s.actionrow(1.95, "WATCH", "Tutorial 1.2 — fields and attractors. Distance, falloff, remapping — "
                           "and reading the field as a 2D image before it drives anything. Sent tonight.", fill=CYAN)
s.actionrow(3.11, "BRING", "Your tile and your working arrays. Next week we drive them with attractors, "
                           "so bring a file you can build on.", fill=LIME)
s.actionrow(4.27, "READ", "Your own 0.1 procedure, out loud, to someone who has not seen the model. Rewrite whatever they cannot follow.", fill=PINK)
s.actionrow(5.43, "CHOOSE", "A site, for next week. You will import it as a point field and diagram it with "
                            "attractors — pick somewhere you know well enough to have a question about.", fill=YELLOW)
d.save("/home/claude/out/ARC3133_Class04.pptx")
print("class04 ok")
