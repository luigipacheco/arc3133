# -*- coding: utf-8 -*-
"""ARC3133 Class 05 — Module 1: Attractors + Site Analysis"""
import math
from nb import *
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

d = Deck()

# ─────────────────────────────── 1 · TITLE
s = d.slide(CYAN)
s.title_slide("CLASS 05  /  SEP 22", ["MODULE 1 — FIELDS", "ATTRACTORS + SITE"],
              "DISTANCE DRIVES FORM",
              "0.2 DUE",
              "1.2 ISSUED TODAY  /  1.1 DUE NEXT CLASS",
              lfill=PINK, rfill=YELLOW)

# ─────────────────────────────── 2 · AN ATTRACTOR IS A NUMBER
s = d.slide(BLACK)
s.header("AN ATTRACTOR IS A NUMBER",
         "For every point: how far is it from something? Use that number to drive a property.")
s.panel(L, 2.05, 6.2, 3.3, "THE WHOLE IDEA", headfill=LIME)
s.t(L + 0.4, 2.85, 5.4, 2.2, [s.Mb("for each point p:", 15),
                              s.Mb("    d = distance(p, attractor)", 15),
                              s.Mb("    size = f(d)", 15),
                              s.Mb(" ", 8),
                              s.Mb("That is it. Everything else", 13.5),
                              s.Mb("is a choice of f.", 13.5)], ls=1.35)
s.panel(7.15, 2.05, 5.5, 3.3, "TWO NUMBERS, SAME JOB", headfill=CYAN)
s.t(7.45, 2.85, 4.9, 2.2, [
    s.Cb("INDEX told you where in the sequence.", 14),
    s.Cb(" ", 6),
    s.Cb("DISTANCE tells you how far from something.", 14),
    s.Cb(" ", 6),
    s.Cb("Both are just numbers driving a property — that is the only idea in this module.", 14)], ls=1.3)
s.banner(5.7, "LAST WEEK YOU BUILT THE POSITIONS. THIS WEEK YOU MEASURE THEM.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# ─────────────────────────────── 3 · THREE KINDS
s = d.slide(CREAM)
s.header("THREE KINDS", "Same maths. What changes is what you measure the distance to.")
kinds = [("SINGLE POINT", CYAN, "distance(p, a)"),
         ("MULTIPLE POINTS", PINK, "min over all attractors"),
         ("CURVE", LIME, "distance to nearest curve point")]
x = L
for nm, col, fm in kinds:
    s.panel(x, 1.95, 3.85, 3.45, nm, headfill=col, tsize=15)
    s.t(x + 0.25, 4.75, 3.35, 0.5, [s.Mb(fm, 11.5)], anchor=MSO_ANCHOR.MIDDLE)
    x += 4.08
# single point field
cx, cy = L + 1.92, 3.5
for i in range(9):
    for j in range(7):
        px, py = L + 0.55 + i * 0.34, 2.75 + j * 0.24
        dd = math.hypot(px - cx, (py - cy) * 1.4)
        s.dot(px, py, d=max(0.045, 0.24 - dd * 0.16))
s.dot(cx, cy, d=0.13, fill=PINK)
# multiple points
ax1, ay1 = L + 4.08 + 1.1, 3.05
ax2, ay2 = L + 4.08 + 2.75, 3.95
for i in range(9):
    for j in range(7):
        px, py = L + 4.63 + i * 0.34, 2.75 + j * 0.24
        dd = min(math.hypot(px - ax1, (py - ay1) * 1.4), math.hypot(px - ax2, (py - ay2) * 1.4))
        s.dot(px, py, d=max(0.045, 0.22 - dd * 0.15))
s.dot(ax1, ay1, d=0.13, fill=PINK); s.dot(ax2, ay2, d=0.13, fill=PINK)
# curve
def cvy(t): return 3.55 - 0.62 * math.sin(t * math.pi)
for k in range(70):
    t = k / 69.0
    s.dot(L + 8.71 + t * 2.9, cvy(t), d=0.03, fill=PINK)
for i in range(9):
    for j in range(7):
        px, py = L + 8.71 + i * 0.34, 2.75 + j * 0.24
        tt = (px - (L + 8.71)) / 2.9
        dd = abs(py - cvy(min(max(tt, 0), 1))) * 1.3
        s.dot(px, py, d=max(0.045, 0.22 - dd * 0.20))
s.banner(5.75, "Whatever you measure to, the output is the same thing: one number per point. "
              "The attractor is not an object — it is a question you ask of every point.",
         fill=CYAN, h=0.72)

# ─────────────────────────────── 4 · FALLOFF IS THE FUNCTION
s = d.slide(CREAM)
s.header("FALLOFF IS THE FUNCTION",
         "f is your decision. It is where the graphic quality actually comes from.")
fall = [("LINEAR", CYAN, "v = d", "Even change all the way across.", lambda t: 1 - t),
        ("INVERSE", PINK, "v = 1 / d", "Sharp near the attractor, flat far off.", lambda t: 1 / (1 + 6 * t)),
        ("SMOOTH", LIME, "eased", "Soft at both ends. Usually the best-looking.", lambda t: 1 - (3 * t * t - 2 * t ** 3)),
        ("THRESHOLD", YELLOW, "on / off at a cut", "No gradient at all. Two populations.", lambda t: 1.0 if t < 0.45 else 0.0)]
x = L
for nm, col, eq, cap, fn in fall:
    s.panel(x, 1.95, 2.85, 3.5, nm, headfill=col, tsize=14.5)
    s.t(x + 0.22, 2.68, 2.4, 0.3, [s.Mb(eq, 11.5)])
    for k in range(26):
        t = k / 25.0
        v = max(0.0, min(1.0, fn(t)))
        s.dot(x + 0.32 + t * 2.2, 3.9 - v * 0.75, d=0.055, fill=BLACK)
    s.rule(x + 0.28, 4.02, 2.3, lw=Pt(1.0), color=MUTE)
    s.t(x + 0.25, 4.15, 2.35, 0.3, [s.Cb("distance →", 10, GREY)])
    s.t(x + 0.25, 4.55, 2.35, 0.8, [s.Cb(cap, 12.5)], ls=1.25)
    x += 3.05
s.banner(5.75, "Two students with the same attractor and different falloff produce completely "
              "different images. This is a design decision, not a setting.", fill=PINK, h=0.72)

# ─────────────────────────────── 5 · THE FIELD IS AN IMAGE  (NEW)
s = d.slide(BLACK)
s.header("THE FIELD IS AN IMAGE",
         "Build it in 2D and look at it before you attach a single tile.")
seq = [("01", "DISTANCE", "Every point on the plane gets a number: how far to the attractor.", CYAN),
       ("02", "FALLOFF", "That number is bent by f. Now it is a gradient you can see.", LIME),
       ("03", "REMAP", "The gradient is pushed into the range your property needs.", YELLOW),
       ("04", "TILE", "Only now does geometry appear. The field was already finished.", PINK)]
x = L
for n, ttl, body, col in seq:
    s.chip(x, 2.0, 2.85, 0.5, n + "   " + ttl, fill=col, size=12)
    s.card(x, 2.6, 2.85, 1.5, fill=CREAM)
    s.t(x + 0.25, 2.6, 2.35, 1.5, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05
# grayscale ramp strip
s.t(L, 4.45, W, 0.3, [s.A("THE FIELD, READ AS A GREY VALUE ACROSS THE PLANE", 11, MUTE)])
ramp = ["FFFDF7", "E8E8E0", "CFCFC6", "B4B4AC", "969690", "757570", "525250", "323230", "1C1C1C"]
bx = L
for c in ramp:
    s.rect(bx, 4.78, W / 9.0, 0.5, fill=c, line=BLACK, lw=Pt(1.5))
    bx += W / 9.0
s.banner(5.62, "IF THE GREY IMAGE IS NOT ALREADY A GOOD DRAWING, THE TILE WILL NOT SAVE IT.",
         fill=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 6.55, W, 0.4, [s.C("1.2 requires one field submitted this way — on its own, as an image, with its falloff named.", 13.5, MUTE)])

# ─────────────────────────────── 6 · REMAP
s = d.slide(CREAM)
s.header("REMAP", "Distance comes out in model units. Your property needs a specific range. "
                  "Remap is the bridge.")
s.panel(L, 1.95, 6.0, 3.4, "THE OPERATION", headfill=CYAN)
s.t(L + 0.35, 2.7, 5.3, 2.3, [s.Mb("t   = (d − dmin) / (dmax − dmin)", 13.5),
                              s.Mb("out = outmin + t × (outmax − outmin)", 13.5),
                              s.Mb(" ", 8),
                              s.Mb("d    0 … 8.4 units", 13.5),
                              s.Mb("out  0.1 … 1.0 radius", 13.5)], ls=1.4)
s.panel(7.0, 1.95, 5.65, 3.4, "SUBTRACT. DIVIDE. MULTIPLY. ADD.", headfill=LIME, tsize=14)
s.t(7.3, 2.7, 5.05, 2.3, [
    s.Cb("Nothing here is new. It is the arithmetic from Week 2, applied to a distance instead of a coordinate.", 14),
    s.Cb(" ", 7),
    s.Cb("Get the ranges wrong and everything is the same size, or one element swallows the sheet.", 14)], ls=1.3)
s.banner(5.65, "1.2 REQUIRES YOUR REMAP RANGES DOCUMENTED ON THE SHEET — INPUT RANGE IN, OUTPUT RANGE OUT.",
         fill=YELLOW, h=0.72)

# ─────────────────────────────── 7 · TWO ATTRACTORS, THREE ANSWERS
s = d.slide(CREAM)
s.header("TWO ATTRACTORS, THREE ANSWERS",
         "With more than one attractor each point has a list of distances. How you reduce it is a design choice.")
red = [("MIN", CYAN, "nearest one wins", lambda d1, d2: 1.0 / (1.0 + 2.2 * min(d1, d2))),
       ("MAX", PINK, "farthest one wins", lambda d1, d2: 1.0 / (1.0 + 1.1 * max(d1, d2))),
       ("MULTIPLY", LIME, "both, multiplied", lambda d1, d2: 1.0 / (1.0 + 1.6 * d1 * d2))]
x = L
for nm, col, cap, fn in red:
    s.panel(x, 1.95, 3.85, 3.5, nm, headfill=col, tsize=15)
    a1 = (x + 1.15, 3.35); a2 = (x + 2.75, 4.25)
    for i in range(10):
        for j in range(8):
            px, py = x + 0.45 + i * 0.32, 2.75 + j * 0.235
            d1 = math.hypot(px - a1[0], (py - a1[1]) * 1.35)
            d2 = math.hypot(px - a2[0], (py - a2[1]) * 1.35)
            v = max(0.0, min(1.0, fn(d1, d2)))
            s.dot(px, py, d=0.05 + v * 0.20)
    s.dot(a1[0], a1[1], d=0.12, fill=PINK)
    s.dot(a2[0], a2[1], d=0.12, fill=PINK)
    s.t(x + 0.25, 4.8, 3.35, 0.4, [s.Cb(cap, 13, bold=True)], align=PP_ALIGN.CENTER)
    x += 4.08
s.banner(5.75, "Same two attractors in all three. Only the reduction changed — territories, "
              "a single central blob, or two peaks with a pinch between them.", fill=YELLOW, h=0.72)

# ─────────────────────────────── 8 · UNDERNEATH, IT IS LISTS
s = d.slide(BLACK)
s.header("UNDERNEATH, IT IS LISTS", "Points, distances, sizes. Three lists, same length, same order.")
cols = [("POINTS", ["p₀", "p₁", "p₂", "p₃", "p₄"], CYAN),
        ("DISTANCES", ["2.1", "0.4", "5.8", "3.2", "1.0"], LIME),
        ("SIZES", ["0.42", "0.95", "0.10", "0.28", "0.71"], YELLOW)]
x = L
for nm, vals, col in cols:
    s.chip(x, 2.0, 2.6, 0.5, nm, fill=col, size=12)
    y = 2.65
    for i, v in enumerate(vals):
        fill = PINK if i == 2 else CREAM
        s.card(x, y, 2.6, 0.5, fill=fill)
        s.t(x + 0.2, y, 0.6, 0.5, [s.Mb("[%d]" % i, 11, GREY)], anchor=MSO_ANCHOR.MIDDLE)
        s.t(x + 0.95, y, 1.5, 0.5, [s.Mb(v, 13)], anchor=MSO_ANCHOR.MIDDLE)
        y += 0.6
    x += 2.85
s.panel(9.2, 2.0, 3.45, 3.75, "PARALLEL LISTS", headfill=PINK, tsize=14)
s.t(9.45, 2.75, 2.95, 2.85, [
    s.Cb("Item [2] in every list describes the same element.", 13),
    s.Cb(" ", 6),
    s.Cb("Break that correspondence — by sorting or culling one of them — and the sizes attach to the wrong points.", 13),
    s.Cb(" ", 6),
    s.Cb("That is what “managing lists” means, and it is next week's whole subject.", 13)], ls=1.25)
s.banner(6.15, "When a field looks scrambled, it is almost always a broken correspondence — not a broken formula.",
         fill=CYAN, h=0.68)

# ─────────────────────────────── 9 · THE SITE IS ALSO A LIST  (NEW)
s = d.slide(BLACK)
s.header("THE SITE IS ALSO A LIST",
         "A real place, imported, is a few hundred thousand points. You already know what to do with points.")
pipe = [("01", "PICK THE SITE", "Somewhere you know. Google 3D Tiles, streamed into Blender.", CYAN),
        ("02", "IMPORT THE TILE", "Photorealistic mesh, georeferenced. Set the origin and the scale before anything else.", LIME),
        ("03", "SAMPLE TO POINTS", "Distribute points on the surface, or take the vertices. Now it is a point cloud.", YELLOW),
        ("04", "DECIMATE", "Half a million points will not survive an instanced module. Cut it down and state both counts.", PINK)]
y = 2.0
for n, ttl, body, col in pipe:
    s.chip(L, y, 0.85, 0.95, n, fill=col, size=17)
    s.card(L + 1.15, y, W - 1.15, 0.95, fill=CREAM)
    s.t(L + 1.45, y + 0.13, W - 1.75, 0.35, [s.Ab(ttl, 13.5)])
    s.t(L + 1.45, y + 0.5, W - 1.75, 0.35, [s.Cb(body, 13)])
    y += 1.1
s.banner(6.5, "THE DIFFERENCE FROM LAST WEEK: YOU DID NOT PLACE THESE POINTS. YOU RECEIVED THEM.",
         fill=CYAN, h=0.62)


# ─────────────────────────────── 10 · A DIAGRAM MAKES A CLAIM
s = d.slide(CREAM)
s.header("A DIAGRAM MAKES A CLAIM",
         "A render shows you the site. A diagram argues something about it. 1.2 wants the second one.")
s.panel(L, 1.95, 5.9, 3.4, "A PICTURE OF A SITE", headfill=MUTE, tsize=15)
s.t(L + 0.35, 2.72, 5.2, 2.4, [
    s.Cb("Shows what is there.", 14),
    s.Cb("Reads the same from any angle.", 14),
    s.Cb("Could be of anywhere.", 14),
    s.Cb(" ", 7),
    s.Cb("Nothing has been measured, so nothing can be wrong — and nothing can be argued with.", 14)], ls=1.35)
s.panel(6.75, 1.95, 5.9, 3.4, "A DIAGRAM OF A SITE", headfill=LIME, tsize=15)
s.t(7.1, 2.72, 5.2, 2.4, [
    s.Cb("Shows one thing, measured.", 14),
    s.Cb("Suppresses everything else on purpose.", 14),
    s.Cb("Could only be of this place.", 14),
    s.Cb(" ", 7),
    s.Cb("Someone can look at it and disagree. That is the test.", 14)], ls=1.35)
s.card(L, 5.6, W, 1.35, fill=CREAM)
s.t(L + 0.35, 5.78, W - 0.7, 0.35, [s.Ab("THREE THINGS YOUR SHEET HAS TO STATE", 13.5)])
three = ["WHAT YOU MEASURED", "WHERE THE ATTRACTOR SITS, AND WHY", "WHAT VARIES, AND OVER WHAT RANGE"]
qx = L + 0.35
for q in three:
    s.t(qx, 6.25, 3.9, 0.5, [s.Cb(q, 13.5, bold=True)])
    qx += 3.9

# ─────────────────────────────── 11 · WHAT COUNTS AS SITE INFORMATION
s = d.slide(BLACK)
s.header("WHAT COUNTS AS SITE INFORMATION",
         "Your choice of subject. Not your choice whether to defend it.")
cats = [("ACCESS + MOVEMENT", CYAN,
         "Entrances, desire lines, stops, crossings, parking. Distance from how people actually arrive."),
        ("ENVIRONMENT", LIME,
         "Sun and shade, prevailing wind, noise sources, canopy, water, elevation and flood line."),
        ("PROGRAM + USE", YELLOW,
         "What each mass does. Density, frontage, vacancy, opening hours, where people stop rather than pass."),
        ("EDGE + BOUNDARY", PINK,
         "Property lines, setbacks, thresholds, walls, the seam where one condition becomes another.")]
x = L
for nm, col, body in cats:
    s.panel(x, 2.0, 2.85, 2.55, nm, headfill=col, tsize=13.5)
    s.t(x + 0.25, 2.75, 2.35, 1.7, [s.Cb(body, 12.5)], ls=1.3)
    x += 3.05
s.banner(4.9, "PICK ONE AND GO DEEP. FOUR SHALLOW LAYERS IS A MAP, NOT A DIAGRAM.",
         fill=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 5.85, W, 0.9, [
    s.C("The attractor is where your claim lives. “The field intensifies toward the north entrance” is a claim. "
        "“I put a point there because it looked good” is not — and it is visible in the drawing either way.",
        13.5, MUTE)], ls=1.3)
# ─────────────────────────────── 12 · WHEN TWO LISTS MEET
s = d.slide(CREAM)
s.header("WHEN TWO LISTS MEET",
         "4 points, 2 attractors. How do they pair up? The software decides — unless you decide.")
modes = [("LONGEST LIST", CYAN, "4 results", "The short list repeats its last item."),
         ("SHORTEST LIST", PINK, "2 results", "Stops when the short list runs out."),
         ("CROSS REFERENCE", LIME, "8 results", "Every point against every attractor.")]
x = L
for nm, col, cnt, cap in modes:
    s.panel(x, 1.95, 3.85, 3.45, nm, headfill=col, tsize=14)
    for i in range(4):
        s.dot(x + 0.6, 2.85 + i * 0.36, d=0.16, fill=BLACK)
    for i in range(2):
        s.dot(x + 3.15, 3.05 + i * 0.72, d=0.16, fill=PINK)
    s.t(x + 0.25, 4.35, 1.4, 0.3, [s.Cb("POINTS", 10, GREY)], align=PP_ALIGN.CENTER)
    s.t(x + 2.45, 4.35, 1.4, 0.3, [s.Cb("ATTRACTORS", 10, GREY)], align=PP_ALIGN.CENTER)
    s.t(x + 0.25, 4.7, 3.35, 0.3, [s.Ab(cnt, 13)], align=PP_ALIGN.CENTER)
    s.t(x + 0.25, 5.02, 3.35, 0.4, [s.Cb(cap, 11.5)], align=PP_ALIGN.CENTER)
    x += 4.08
s.banner(5.65, "This is why your two-attractor field went wrong. Longest List is the default, "
              "and the default is a decision someone else made for you.", fill=YELLOW, h=0.72)

# ─────────────────────────────── 13 · GRAFT, FLATTEN, WRAP
s = d.slide(CREAM)
s.header("GRAFT, FLATTEN, WRAP",
         "Three operations that change list structure rather than list contents.")
ops = [("GRAFT", CYAN, "one list  →  one branch each",
        "Each item becomes its own branch, so the next operation treats them separately instead of pairing them off."),
       ("FLATTEN", PINK, "many branches  →  one list",
        "The opposite. Useful at the end — destructive in the middle, because it throws away the structure you built."),
       ("WRAP", LIME, "index past the end  →  back to the start",
        "i mod n. An index of 6 in a list of 4 becomes 2. Cheap repetition, and the source of a lot of accidental patterns.")]
x = L
for nm, col, sub, cap in ops:
    s.panel(x, 1.95, 3.85, 3.45, nm, headfill=col, tsize=15)
    s.t(x + 0.25, 2.68, 3.35, 0.3, [s.Mb(sub, 10.5)])
    s.t(x + 0.25, 3.15, 3.35, 2.0, [s.Cb(cap, 13)], ls=1.3)
    x += 4.08
s.banner(5.65, "Structure is not content. Every one of these leaves the numbers alone and changes "
              "only who is grouped with whom.", fill=CYAN, h=0.72)


# ─────────────────────────────── 14 · ISSUED TODAY
s = d.slide(BLACK)
s.issued("ISSUED TODAY", "1.2 — POINT: SITE ANALYSIS FIELDS",
         "STUDY A REVIEWED CLASS 6 — SEP 29  ·  DUE CLASS 8 — OCT 13, WITH THE MIDTERM   /   7%",
         "An attractor turns distance into a value you can draw with. Study A builds that instrument on a "
         "flat plane, where you can see exactly what it does. Study B points it at a real site and uses it "
         "to diagram something you found there.", badgefill=CYAN)
st = [("STUDY A", "THE INSTRUMENT", "Attractors on a flat field, driving your 1.1 tile. "
                                    "The field shown as an image before it drives anything.", LIME),
      ("STUDY B", "THE SITE", "A site of your choosing, imported as a point field, "
                              "diagrammed with attractors anchored in what you found there.", YELLOW)]
x = L
for tag, ttl, body, col in st:
    s.chip(x, 3.95, 5.9, 0.45, tag, fill=col, size=11)
    s.card(x, 4.5, 5.9, 1.6, fill=CREAM)
    s.t(x + 0.3, 4.68, 5.3, 0.35, [s.Ab(ttl, 14)])
    s.t(x + 0.3, 5.1, 5.3, 0.9, [s.Cb(body, 13)], ls=1.25)
    x += 6.1
s.banner(6.4, "STUDY A IS PINNED UP IN TWO WEEKS. IT IS NOT A DRAFT OF STUDY B — IT IS HOW YOU LEARN THE TOOL.",
         fill=YELLOW, h=0.62, align=PP_ALIGN.CENTER)

# ─────────────────────────────── 15 · REQUIREMENTS
s = d.slide(CREAM)
s.header("REQUIREMENTS", "Counting these earns a C. The rest is judgement.")
reqs = [("3", "attractor types across the set: single point, multiple points, curve", CYAN),
        ("1", "field shown on its own as a 2D image, before it drives geometry, falloff named", CYAN),
        ("3+", "distinct parameters driven by distance — scale, rotation, density, height, colour", CYAN),
        ("1+", "explicit remap, with input and output ranges stated on the sheet", LIME),
        ("1", "site imported and reduced to a point field — counts stated before and after, scale and origin declared", YELLOW),
        ("1", "site condition measured and named — access, environment, use, or edge", YELLOW),
        ("1+", "attractor whose position is argued from that condition, in one written sentence", YELLOW),
        ("2", "sheets minimum, covering both studies, in your visual identity", PINK)]
y = 1.9
for chip, body, col in reqs:
    s.numrow(y, chip, body, chipfill=col, h=0.48, csize=12, size=13.5)
    y += 0.575
s.banner(6.65, "Falloff built, not called from a preset. The imported site is expected — a preset attractor plugin is not.",
         fill=PINK, h=0.62, size=12.5)

# ─────────────────────────────── 16 · NOW
s = d.slide(LIME)
s.header("NOW — 1.1 CLINIC, THEN YOUR FIRST FIELD")
s.t(L, 1.85, 11.5, 0.4, [s.Cb("1.1 is due next class. Bring your problems to the front, then start Study A.", 16)])
rows = ["Tile modeled, and three arrays running — which three, and why those",
        "One attractor working on a 1.1 array, any falloff",
        "The field looked at on its own, as a flat image, before the tile is attached",
        "Remap ranges written down, ready to put on the sheet",
        "A site named for Study B — and one sentence on what you want to find out about it"]
y = 2.5
for r in rows:
    s.checkrow(y, r)
    y += 0.78
s.card(L, 6.5, 9.0, 0.62, fill=BLACK)
s.t(L, 6.5, 9.0, 0.62, [s.Ab("THREE DIFFERENT SCALES IS NOT THREE PARAMETERS.", 13, LIME)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ─────────────────────────────── 17 · BEFORE NEXT CLASS
s = d.slide(CREAM)
s.header("BEFORE NEXT CLASS")
s.actionrow(1.95, "FINISH", "1.1 is due next class. Two sheets minimum, in your visual identity — "
                            "precedent, tile, and three arrays.", fill=CYAN)
s.actionrow(3.11, "INSTALL", "The Google 3D Tiles importer in Blender, and get one tile of your site to load. "
                             "Do this before the studio session, not during it.", fill=LIME)
s.actionrow(4.27, "WRITE", "One sentence: what you want your site diagram to show. If you cannot write it, "
                           "you do not have a diagram yet.", fill=YELLOW)
s.actionrow(5.43, "BRING", "Study A running, even badly. Next class is a clinic and it is worth more "
                           "with something on screen.", fill=PINK)

d.save("/home/claude/out/ARC3133_Class05.pptx")
print("class05 ok")
