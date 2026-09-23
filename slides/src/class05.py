# -*- coding: utf-8 -*-
"""Class 05 — Descriptive geometry continued (U03). Your own module, then material and
lighting for the P3a sheet. Nothing due; nothing issued."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(5)
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 5
VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")


def frame_panel(s, x, y, size, k, fill=LIME, hole=PAPER, lw=HAIR):
    """Plan of a square frame module: outer square, inner aperture of ratio k."""
    s.rect(x, y, size, size, fill=fill, line=BLACK, lw=lw)
    q = size * k
    if q > 0.01:
        s.rect(x + (size - q) / 2, y + (size - q) / 2, q, q, fill=hole, line=BLACK, lw=lw)


# 1 ── TITLE
title_slide(d, WK, ["FROM THE PYRAMID", "TO YOUR MODULE"],
            "BUILD IT, THEN LIGHT IT — THE P3a SHEET", bg=PINK, lfill=YELLOW, rfill=CYAN,
            foot="U03 CONTINUES  /  P3a IN PROGRESS  /  " + C.due_line("P3a").upper())

# 2 ── PARAMETERS FIRST
s = d.slide(CREAM)
s.header("PARAMETERS FIRST",
         "Before a single point: write down the numbers that drive the module, and what each one does.")
s.panel(L, 1.95, 6.3, 3.55, "A PARAMETER TABLE", headfill=CYAN)
rows = [("size", "1.0", "outer edge — also the tiling pitch"),
        ("thickness", "0.1", "depth of the panel"),
        ("aperture k", "0.5", "hole as a share of the size, 0 < k < 1")]
yy = 2.7
s.t(L + 0.3, yy, 1.8, 0.3, [s.Ab("NAME", 11, GREY)])
s.t(L + 2.1, yy, 0.8, 0.3, [s.Ab("VALUE", 11, GREY)])
s.t(L + 3.0, yy, 3.1, 0.3, [s.Ab("WHAT IT CONTROLS", 11, GREY)])
yy += 0.42
for nm, v, what in rows:
    s.rule(L + 0.3, yy - 0.06, 5.7, lw=HAIR, color=LINE)
    s.t(L + 0.3, yy, 1.8, 0.5, [s.Mb(nm, 12.5, bold=True)])
    s.t(L + 2.1, yy, 0.8, 0.5, [s.Mb(v, 12.5)])
    s.t(L + 3.0, yy, 3.1, 0.6, [s.Cb(what, 12.5)], ls=1.15)
    yy += 0.7
s.panel(7.25, 1.95, 5.4, 3.55, "ONE MUST CHANGE THE SHAPE", headfill=PINK, tsize=14.5)
s.t(7.55, 2.7, 4.8, 2.7, [
    s.Cb("Size and thickness only change the box. P3a asks for a shape control beyond overall "
         "dimensions:", 13.5),
    s.Cb(" ", 6),
    s.Ab("APERTURE  ·  FOLD DEPTH  ·  CORNER OFFSET", 12),
    s.Cb(" ", 6),
    s.Cb("The example here is an aperture: a square frame with a square hole. Yours comes "
         "from your precedent.", 13.5)], ls=1.3)
s.banner(5.8, "IF YOU CANNOT SAY WHAT A NUMBER CONTROLS, IT IS NOT A PARAMETER YET.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 3 ── CALCULATE EVERY POINT
s = d.slide(BLACK)
s.header("CALCULATE EVERY POINT",
         "Each position is an expression of the parameters. Never a typed coordinate.")
s.panel(L, 2.05, 5.1, 4.0, "PLAN — TOP RING", headfill=LIME)
ox, oy, sz = L + 1.25, 2.95, 2.6
kk = 0.42
s.rect(ox, oy, sz, sz, fill=CREAM, line=BLACK, lw=THIN)
qd = sz * kk
ix, iy = ox + (sz - qd) / 2, oy + (sz - qd) / 2
s.rect(ix, iy, qd, qd, fill=PAPER, line=BLACK, lw=THIN)
# plan: y up, so index 0 is bottom-left
pts = [(ox, oy + sz, "0"), (ox + sz, oy + sz, "1"), (ox + sz, oy, "2"), (ox, oy, "3"),
       (ix, iy + qd, "4"), (ix + qd, iy + qd, "5"), (ix + qd, iy, "6"), (ix, iy, "7")]
for i, (px, py, lab) in enumerate(pts):
    s.dot(px, py, d=0.15, fill=PINK if i < 4 else CYAN)
    dx = -0.34 if px < ox + sz / 2 else 0.08
    dy = 0.02 if py > oy + sz / 2 else -0.3
    if i >= 4:
        dx = 0.08 if px < ox + sz / 2 else -0.3
        dy = -0.3 if py > oy + sz / 2 else 0.04
    s.t(px + dx, py + dy, 0.3, 0.26, [s.Mb(lab, 11.5, bold=True)])
s.panel(6.05, 2.05, 6.6, 4.0, "THE POINT LIST", headfill=YELLOW)
code = ["h = size / 2              # half size",
        "q = h * k                 # aperture",
        "t = thickness",
        " ",
        "top    = [[-h,-h,t], [ h,-h,t],     # 0 1",
        "          [ h, h,t], [-h, h,t],     # 2 3",
        "          [-q,-q,t], [ q,-q,t],     # 4 5",
        "          [ q, q,t], [-q, q,t]]     # 6 7",
        " ",
        "bottom = the same eight at z = 0    # 8–15",
        "verts  = top + bottom"]
s.t(6.35, 2.8, 6.1, 3.1, [s.Mb(c, 11.5) for c in code], ls=1.2)
s.banner(6.35, "WRITE THE INDEX NEXT TO EVERY POINT. THE FACES ARE LISTS OF THESE NUMBERS.",
         fill=CYAN, h=0.6, align=PP_ALIGN.CENTER, size=12)

# 4 ── FACE ORDER AND CLOSURE
s = d.slide(CREAM)
s.header("FACE ORDER AND CLOSURE",
         "Four kinds of face, each written counter-clockwise as seen from outside the solid.")
s.panel(L, 1.95, 6.9, 3.6, "THE FACE LIST  —  i = 0…3,  n = (i + 1) % 4", headfill=CYAN, tsize=13.5)
fl = [("top", "[i,    n,    4+n,  4+i ]", "normal up"),
      ("bottom", "[12+i, 12+n, 8+n,  8+i ]", "normal down"),
      ("outer", "[i,    8+i,  8+n,  n   ]", "normal outward"),
      ("inner", "[4+i,  4+n,  12+n, 12+i]", "normal into the hole")]
yy = 2.75
for nm, f, note in fl:
    s.chip(L + 0.3, yy, 1.2, 0.45, nm.upper(), fill=LIME, size=11, shadow=False)
    s.t(L + 1.75, yy + 0.08, 3.4, 0.35, [s.Mb(f, 12, bold=True)])
    s.t(L + 5.05, yy + 0.08, 1.7, 0.35, [s.Cb(note, 11.5, GREY)])
    yy += 0.66
s.panel(7.85, 1.95, 4.8, 3.6, "CHECK IT", headfill=PINK)
s.t(8.15, 2.7, 4.2, 2.7, [
    s.Ab("16 VERTICES · 32 EDGES · 16 FACES", 12.5),
    s.Cb(" ", 6),
    s.Cb("Closed: every edge is shared by exactly two faces.", 13.5),
    s.Cb(" ", 4),
    s.Cb("Oriented: a shared edge runs one way in one face and the other way in the next.", 13.5),
    s.Cb(" ", 4),
    s.Cb("A reversed face flips its normal. Show one on the sheet, and say how you found it.", 13.5)],
    ls=1.25)
s.banner(5.85, "PUT ONE FACE ON THE SHEET WITH ITS VERTEX ORDER DRAWN. P3a ASKS FOR IT.",
         fill=YELLOW, h=0.68, align=PP_ALIGN.CENTER)

# 5 ── TILE IT, THEN PUSH IT
s = d.slide(CREAM)
s.header("TILE IT 2 × 2, THEN PUSH THE NUMBERS",
         "A module that only works at one value is a drawing. Find the range where it still closes and tiles.")
s.panel(L, 1.95, 4.3, 3.75, "2 × 2, EDGE TO EDGE", headfill=LIME)
ts = 1.15
tx, ty = L + (4.3 - 2 * ts) / 2, 2.75
for a in range(2):
    for b in range(2):
        frame_panel(s, tx + a * ts, ty + b * ts, ts, 0.45, fill=CREAM, lw=THIN)
s.t(L + 0.3, 5.12, 3.7, 0.45, [s.Cb("Size is the pitch. Shared edges, no gaps.", 12.5)],
    align=PP_ALIGN.CENTER)
s.panel(5.2, 1.95, 7.45, 3.75, "LOW  ·  MIDDLE  ·  HIGH", headfill=YELLOW)
for i, (lab, k, col) in enumerate([("k = 0.15", 0.15, CYAN), ("k = 0.50", 0.50, LIME),
                                   ("k = 0.85", 0.85, PINK)]):
    px = 5.65 + i * 2.35
    frame_panel(s, px, 2.8, 1.6, k, fill=col, lw=THIN)
    s.t(px - 0.2, 4.55, 2.0, 0.3, [s.Mb(lab, 12, bold=True)], align=PP_ALIGN.CENTER)
s.t(5.5, 5.0, 6.9, 0.6, [s.Cb("At k = 0 the hole is gone and the inner faces collapse. At k = 1 the "
                              "frame has no width. Both ends break the mesh.", 12.5)], ls=1.2)
s.banner(6.0, "STATE THE RANGE ON THE SHEET — FOR EXAMPLE 0.15 ≤ k ≤ 0.85 — AND DRAW BOTH ENDS AND THE MIDDLE.",
         fill=BLACK, color=YELLOW, h=0.68, align=PP_ALIGN.CENTER, size=12)

# 6 ── ONE RENDER, ONE MATERIAL
s = d.slide(CREAM)
s.header("ONE RENDER, ONE MATERIAL",
         "A studio render: the module alone, on a ground plane, in one surface.")
cols3 = [("GROUND PLANE", CYAN,
          ["The module sits on it. Its shadow tells the eye where the module is.",
           "Make it large enough to hold the whole shadow."]),
         ("ONE MATERIAL", LIME,
          ["One surface for the whole module: colour, roughness, metal or not.",
           "Write the values down. They go on the sheet."]),
         ("BACKGROUND", PINK,
          ["Plain and continuous. The floor meets the backdrop without a visible edge.",
           "No entourage: no people, trees or context."])]
x = L
for nm, col, body in cols3:
    s.panel(x, 1.95, 3.85, 3.45, nm, headfill=col, tsize=15)
    s.t(x + 0.28, 2.75, 3.3, 2.5, [s.Cb(body[0], 14), s.Cb(" ", 7), s.Cb(body[1], 14)], ls=1.3)
    x += 4.08
s.banner(5.75, "THE GEOMETRY IS THE SUBJECT. THE MATERIAL SHOULD SHOW ITS FORM, NOT COMPETE WITH IT.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 7 ── LIGHT IT ON PURPOSE
s = d.slide(BLACK)
s.header("LIGHT IT ON PURPOSE",
         "Choose one setup. Every light has a job, and you can name it.")
s.panel(L, 2.05, 5.2, 3.6, "KEY · FILL · RIM  (PLAN)", headfill=CYAN, tsize=14.5)
mx, my = L + 2.6, 3.95
s.rect(mx - 0.35, my - 0.35, 0.7, 0.7, fill=LIME, line=BLACK, lw=THIN)
s.chip(mx - 0.55, my + 1.05, 1.1, 0.36, "CAMERA", fill=MUTE, size=9.5, shadow=False)
s.chip(mx - 2.25, my + 0.35, 1.0, 0.36, "KEY", fill=YELLOW, size=10, shadow=False)
s.chip(mx + 1.25, my + 0.2, 1.0, 0.36, "FILL", fill=PAPER, size=10, shadow=False)
s.chip(mx - 0.5, my - 1.2, 1.0, 0.36, "RIM", fill=PINK, size=10, shadow=False)
s.panel(6.1, 2.05, 6.55, 3.6, "TWO SETUPS", headfill=YELLOW)
s.t(6.4, 2.8, 6.0, 2.8, [
    [s.Ab("KEY  ", 12.5), s.Cb("the main light. It sets the shadow direction.", 13)],
    [s.Ab("FILL  ", 12.5), s.Cb("opposite side, weaker. It lifts the dark side.", 13)],
    [s.Ab("RIM  ", 12.5), s.Cb("behind the module. It separates the edge from the background.", 13)],
    [s.Cb(" ", 6)],
    [s.Ab("OR", 12.5)],
    [s.Cb(" ", 4)],
    [s.Ab("SUN  ", 12.5), s.Cb("one direction, sharp shadow.", 13)],
    [s.Ab("SKY  ", 12.5), s.Cb("soft light from everywhere that fills the shadow.", 13)]], ls=1.3)
s.banner(5.95, "LARGE LIGHT, SOFT SHADOW. SMALL LIGHT, SHARP SHADOW. CHOOSE ONE, SAY WHY, "
              "AND RECORD EVERY SETTING.",
         fill=PINK, h=0.72, align=PP_ALIGN.CENTER, size=12)

# 8 ── CAMERA AND SHEET
s = d.slide(CREAM)
s.header("CAMERA AND SHEET",
         "One fixed view, then a layout where the render leads and the lists explain it.")
s.panel(L, 1.95, 5.0, 4.35, "CAMERA", headfill=LIME)
s.t(L + 0.3, 2.7, 4.4, 3.5, [
    s.Cb("One view. Slightly above, three-quarter, so the top and two sides read.", 13.5),
    s.Cb(" ", 5),
    s.Cb("A long enough lens that the module does not distort.", 13.5),
    s.Cb(" ", 5),
    s.Cb("Frame the module and its shadow. Leave air around both.", 13.5),
    s.Cb(" ", 5),
    s.Cb("Render at the proportion of the space it fills on the sheet.", 13.5)], ls=1.25)
s.panel(5.95, 1.95, 6.7, 4.35, "17 × 11 INCH SHEET", headfill=CYAN)
sx, sy, sw, sh_ = 6.8, 2.78, 5.0, 5.0 * 11 / 17
f = sw / 5.9
s.rect(sx, sy, sw, sh_, fill=PAPER, line=BLACK, lw=THIN)
blocks = [(0.12, 0.12, 3.35, 2.45, "STUDIO RENDER", YELLOW),
          (3.6, 0.12, 2.18, 0.72, "PARAMETER TABLE", LIME),
          (3.6, 0.96, 2.18, 0.8, "POINT + FACE LISTS", CYAN),
          (3.6, 1.88, 2.18, 0.69, "ONE FACE, VERTEX ORDER", PINK),
          (0.12, 2.69, 3.35, 0.99, "LOW · MIDDLE · HIGH + 2 × 2", CREAM),
          (3.6, 2.69, 2.18, 0.99, "SETTINGS · CREDIT", CREAM)]
for bx, by, bw, bh, lab, col in blocks:
    bx, by, bw, bh = bx * f, by * f, bw * f, bh * f
    s.rect(sx + bx, sy + by, bw, bh, fill=col, line=BLACK, lw=HAIR)
    s.t(sx + bx + 0.05, sy + by, bw - 0.1, bh, [s.Ab(lab, 9)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
s.banner(6.55, "SETTINGS = MATERIAL VALUES AND EVERY LIGHT. CREDIT = BUILDING, ARCHITECT, SOURCE.",
         fill=BLACK, color=LIME, h=0.56, align=PP_ALIGN.CENTER, size=11.5)

# 9 ── CRITIQUE CHECKLIST
s = d.slide(BLACK)
s.header("CRITIQUE CHECKLIST",
         "What we look at when your sheet goes on the wall. Check it yourself first.")
lists = [("THE MODULE", LIME,
          ["Tiles 2 × 2, edge to edge, with no gaps",
           "Closed: every edge shared by two faces",
           "One shape parameter beyond the box",
           "Ranges stated; low, middle and high drawn",
           "Every point calculated, none typed"]),
         ("THE RENDER", CYAN,
          ["Sits on the ground; the shadow reads",
           "One material, its values recorded",
           "Each light has a job you can name",
           "Plain background, no entourage",
           "The render leads the sheet; lists explain it"])]
x = L
for nm, col, items in lists:
    s.panel(x, 2.05, 5.88, 4.15, nm, headfill=col)
    yy = 2.85
    for it in items:
        s.rect(x + 0.3, yy + 0.05, 0.28, 0.28, fill=CREAM, line=BLACK, lw=THIN)
        s.t(x + 0.8, yy, 4.9, 0.4, [s.Cb(it, 14)], anchor=MSO_ANCHOR.MIDDLE)
        yy += 0.64
    x += 6.12
s.banner(6.5, "IF YOU CANNOT TICK A BOX, THAT IS WHAT YOU WORK ON THIS WEEK.",
         fill=YELLOW, h=0.58, align=PP_ALIGN.CENTER, size=12)

# 10 ── REMINDER — P3a REQUIREMENTS
requirements_slide(d, "P3a", title="REMINDER — P3a REQUIREMENTS", sub=VISUAL)

# 11 ── NOW
now_slide(d, "NOW — BUILD IT, THEN LIGHT IT",
          "Rest of the class: your own module, closed and tiling, in a first test render.",
          ["Parameters written down first, with one shape control beyond the box",
           "Point list calculated from the parameters — no typed coordinates",
           "Faces ordered, normals out, closure checked",
           "2 × 2 tiling working at low, middle and high values",
           "One test render: ground plane, one material, lights placed on purpose"],
          closer="A CLOSED MODULE AND A TEST RENDER. THE SHEET FOLLOWS.",
          bg=LIME)

# 12 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "Week 6 starts arrays: 1D, 2D and 3D — a linear array, a nested grid and an XYZ "
             "cube array. Your module is the component we repeat."),
    ("DUE", "P3a is due next class: one sheet, one studio render, settings recorded. "
            + C.due_line("P3a") + "."),
    ("PRINT", "P2b print checkpoint next class. " + C.checkpoints("P2b")[0][1]),
    ("BRING", "The editable module file — closed, parameterised, tiling. Next class it becomes "
              "the component of every array."),
])

d.save(os.path.join(OUT, "ARC3133_Class05.pptx"))
print("class05 ok — %d slides" % len(d.prs.slides._sldIdLst))
