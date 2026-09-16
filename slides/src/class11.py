# -*- coding: utf-8 -*-
"""Class 11 — SDF volume studio work (U07, second class). P4a checkpoint."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 11
RUBRIC = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")


def sign_field(s, x, y, cols, rows, p, fn, inside=PINK, outside=CYAN, zero=YELLOW, k=0.09):
    """Dots coloured by the sign of fn(px, py); size grows with distance from zero."""
    for i in range(cols):
        for j in range(rows):
            px, py = x + i * p, y + j * p
            v = fn(px, py)
            if abs(v) < p * 0.5:
                s.dot(px, py, d=0.15, fill=zero)
            else:
                s.dot(px, py, d=min(0.2, 0.05 + abs(v) * k), fill=inside if v < 0 else outside)


# 1 ── TITLE
title_slide(d, WK, ["SDF VOLUME", "STUDIO WORK"],
            "P4 CONTINUES — ONE SHAPE, WRITTEN AS A FUNCTION", bg=LIME, lfill=PINK, rfill=CYAN,
            right_tag="P3d DUE · P4a CHECKPOINT",
            foot="P3d DUE TODAY  /  P4a CHECKPOINT TODAY")

# 2 ── A FIELD HAS A SIGN
s = d.slide(BLACK)
s.header("A FIELD HAS A SIGN",
         "At every point the function returns one number: how far to the surface, and on which side.")
s.card(L, 2.05, 5.2, 3.45, fill=CREAM)
cx, cy, r = L + 2.6, 3.78, 1.05
sign_field(s, L + 0.35, 2.3, 14, 9, 0.345, lambda px, py: math.hypot(px - cx, py - cy) - r)
rows = [("NEGATIVE", PINK, "Inside the shape. The further in, the more negative."),
        ("ZERO", YELLOW, "Exactly on the surface. This is the shape you will see."),
        ("POSITIVE", CYAN, "Outside the shape. The value is the distance to the surface.")]
y = 2.05
for nm, col, body in rows:
    s.chip(6.2, y, 2.0, 1.0, nm, fill=col, size=13)
    s.card(8.45, y, 4.2, 1.0, fill=CREAM)
    s.t(8.7, y, 3.75, 1.0, [s.Cb(body, 13)], ls=1.2, anchor=MSO_ANCHOR.MIDDLE)
    y += 1.225
s.banner(5.85, "sphere(p) = length(p − center) − radius     ·     THE SURFACE IS WHERE THE FIELD EQUALS 0",
         fill=LIME, h=0.7, align=PP_ALIGN.CENTER, font="Courier New", size=13)

# 3 ── PRIMITIVES
s = d.slide(CREAM)
s.header("PRIMITIVES ARE FUNCTIONS",
         "Each one takes a point and returns a signed distance. Position and size are inputs.")
prims = [("SPHERE", CYAN, ["d = length(p − c) − r"],
          "Distance to the center, minus the radius. The simplest exact field."),
         ("BOX", LIME, ["q = abs(p − c) − half", "d = distance past the", "    nearest face"],
          "Negative inside, zero on each face, positive outside."),
         ("PLANE", PINK, ["d = dot(p, n) − h"],
          "One side is negative, the other positive. Useful to cut or to slice.")]
x = L
for nm, col, lines, body in prims:
    s.panel(x, 1.95, 3.85, 3.45, nm, headfill=col, tsize=15)
    s.t(x + 0.28, 2.75, 3.3, 1.1, [s.Mb(l, 12) for l in lines], ls=1.3)
    s.rule(x + 0.28, 4.0, 3.3, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.28, 4.15, 3.3, 1.1, [s.Cb(body, 13)], ls=1.3)
    x += 4.08
s.banner(5.75, "Start with two primitives you can name and move. Expose center and size as inputs, "
              "so every variant on the sheet is one number away.", fill=YELLOW, h=0.72)

# 4 ── BOOLEANS ON FIELDS
s = d.slide(CREAM)
s.header("THE P2 BOOLEANS, WRITTEN ON NUMBERS",
         "Same operands, same order rules. The operation is now a comparison of two values.")
ops = [("UNION", CYAN, "min(a, b)", "Keep the nearer surface. Inside either field counts as inside."),
       ("INTERSECTION", LIME, "max(a, b)", "Keep the farther surface. Inside only where both are negative."),
       ("DIFFERENCE", PINK, "max(a, −b)", "Flip b inside out, then intersect. a with b carved away.")]
x = L
for nm, col, fm, body in ops:
    s.panel(x, 1.95, 3.85, 3.2, nm, headfill=col, tsize=15)
    s.t(x + 0.2, 2.75, 3.45, 0.7, [s.Mb(fm, 24, bold=True)], align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE)
    s.t(x + 0.28, 3.75, 3.3, 1.2, [s.Cb(body, 13)], ls=1.3, align=PP_ALIGN.CENTER)
    x += 4.08
s.banner(5.45, "max(a, −b) IS NOT max(b, −a). NAME THE OPERANDS ON THE SHEET, AS YOU DID IN P2a.",
         fill=BLACK, color=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 6.35, W, 0.7, [s.C("P4a asks for all three from the same source fields. Change nothing but the "
                          "operation, so the comparison is fair.", 13.5, GREY)], ls=1.3)

# 5 ── SMOOTH BLEND AND NOISE
s = d.slide(BLACK)
s.header("SMOOTH BLEND, AND WHAT NOISE DOES",
         "Two ways to move past hard Booleans. Only one of them keeps the field an exact distance.")
s.panel(L, 2.05, 5.85, 3.5, "SMOOTH MIN", headfill=LIME)
s.t(L + 0.3, 2.8, 5.25, 2.6, [
    s.Mb("d = smooth_min(a, b, k)", 14),
    s.Cb(" ", 7),
    s.Cb("k = 0 gives the plain union. A larger k widens the fillet where the two shapes meet.", 14),
    s.Cb(" ", 7),
    s.Cb("k is in model units. Write its value on the sheet.", 14)], ls=1.3)
s.panel(6.8, 2.05, 5.85, 3.5, "NOISE", headfill=PINK)
s.t(7.1, 2.8, 5.25, 2.6, [
    s.Mb("d = field(p) + amp × noise(p)", 14),
    s.Cb(" ", 7),
    s.Cb("Noise changes the field, and the zero surface moves with it.", 14),
    s.Cb(" ", 7),
    s.Cb("The values are no longer exact distances. Call the result an implicit field, "
         "not an SDF.", 14)], ls=1.3)
s.banner(5.85, "CHANGE ONE INFLUENCE AT A TIME: k, OR amp, OR NOISE SCALE — NEVER TWO IN THE SAME VARIANT.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 6 ── RESOLUTION
s = d.slide(CREAM)
s.header("RESOLUTION: DETAIL AGAINST COST",
         "The field is continuous. You only ever see it at the points where you sample it.")
res = [("COARSE", CYAN, 4, "32 per axis", "32,768 samples", "Fast. Thin parts vanish."),
       ("MEDIUM", LIME, 6, "64 per axis", "262,144 samples", "Good for testing variants."),
       ("FINE", PINK, 9, "128 per axis", "2,097,152 samples", "Detail, but slow to change.")]
x = L
for nm, col, n, per, tot, cap in res:
    s.panel(x, 1.95, 3.85, 3.55, nm, headfill=col, tsize=15)
    p = 1.5 / (n - 1)
    G.cartesian(s, x + 0.35, 2.85, cols=n, rows=n, p=p, d=max(0.05, 0.14 - n * 0.01))
    s.t(x + 2.1, 2.85, 1.6, 0.3, [s.Mb(per, 11)])
    s.t(x + 2.1, 3.2, 1.6, 0.6, [s.Mb(tot, 11)], ls=1.2)
    s.t(x + 2.1, 3.85, 1.6, 0.6, [s.Cb(cap, 11.5)], ls=1.2)
    s.t(x + 0.35, 4.6, 3.2, 0.7, [s.Cb("Diagram, not to count.", 10, GREY)])
    x += 4.08
s.banner(5.8, "DOUBLE THE RESOLUTION ON EACH AXIS AND THE SAMPLE COUNT GROWS EIGHT TIMES. "
              "WORK COARSE, FINISH FINE.", fill=BLACK, color=LIME, h=0.7, align=PP_ALIGN.CENTER)
s.t(L, 6.7, W, 0.4, [s.C("P4a requires the sampling resolution stated on the sheet.", 13.5, GREY)])

# 7 ── SURFACE EXTRACTION
s = d.slide(BLACK)
s.header("SURFACE EXTRACTION",
         "The mesh is the last step, not the design. Everything upstream is still a number per sample.")
seq = [("01", "DEFINE", "Write the field: primitives, Booleans, blend.", CYAN),
       ("02", "SAMPLE", "Evaluate it on a grid inside stated bounds.", LIME),
       ("03", "EXTRACT", "Build the surface where the value crosses the threshold.", YELLOW),
       ("04", "COMPARE", "Extract at two resolutions. Keep both.", PINK)]
x = L
for n, ttl, body, col in seq:
    s.chip(x, 2.0, 2.85, 0.5, n + "   " + ttl, fill=col, size=12)
    s.card(x, 2.6, 2.85, 1.35, fill=CREAM)
    s.t(x + 0.25, 2.6, 2.35, 1.35, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05
s.card(L, 4.3, 7.4, 1.95, fill=CREAM)
s.t(L + 0.3, 4.45, 6.9, 1.7, [
    s.Mb("def field(p):", 13),
    s.Mb("    return smooth_min(a(p), b(p), k)", 13),
    s.Mb("grid    = sample(field, bounds, resolution)", 13),
    s.Mb("surface = extract(grid, iso=0.0)", 13)], ls=1.35)
s.panel(8.35, 4.3, 4.3, 1.95, "STATE ON THE SHEET", headfill=YELLOW, tsize=13.5)
s.t(8.6, 4.95, 3.85, 1.2, [s.Cb("Bounds · resolution · threshold (iso) · any smoothing after extraction", 13)],
    ls=1.3)
s.t(L, 6.55, W, 0.4, [s.C("Keep the source fields live. The extracted mesh is what you will slice in Week 12.",
                          13.5, MUTE)])

# 8 ── TWO SHEETS
s = d.slide(CREAM)
s.header("P4a — TWO SHEETS, TWO JOBS",
         "Two 17 × 11 inch sheets. One explains the field. The other argues for a volume.")
sheets = [("SHEET 1 — THE FIELD LOGIC", CYAN,
           ["The source fields, named, with their inputs",
            "A diagram of the field: inside, outside, zero",
            "Union, intersection and difference from the same sources",
            "The implicit function named: density, SDF or other"]),
          ("SHEET 2 — THE VOLUME", PINK,
           ["The chosen result, large",
            "Three controlled variants, one parameter each",
            "Sampling resolution and extraction settings",
            "The volume selected for P4b, and its spatial intention"])]
x = L
for ttl, col, items in sheets:
    s.panel(x, 1.95, 5.85, 3.2, ttl, headfill=col, tsize=14.5)
    s.t(x + 0.35, 2.8, 5.2, 2.3, [s.Cb("—  " + it, 15) for it in items], ls=1.35, space=8)
    x += 6.15
s.banner(5.5, "Sheet 2 ends with a decision. If you cannot say why this volume should be sliced, "
              "you are not done with P4a.", fill=YELLOW, h=0.72)

# 9 ── REQUIREMENTS (REMINDER)
requirements_slide(d, "P4a", sub=RUBRIC, title="REMINDER — P4a")

# 10 ── NOW
now_slide(d, "NOW — CHECKPOINT AND WORK",
          "P3d is handed in today. Then the P4a checkpoint — items 1, 2 and 5 — then keep building.",
          ["An SDF diagram: inside, outside and the zero surface, for your own fields",
           "Union, intersection and difference from the same two source fields",
           "One smooth-min or noise variant, with the changed value written down",
           "The surface extracted at two resolutions, both kept",
           "A candidate volume for slicing, with one sentence of intention"],
          closer="IF YOU CANNOT SAY WHICH SIDE IS NEGATIVE, START THERE.",
          bg=CYAN)

# 11 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "Week 12 (target " + C.date_long(12).split("— ")[1] + ") — Discretizing Geometry: "
             "section planes, direction, interval and order. Watch U09 before class."),
    ("SUBMIT", "P4a is due next class. " + C.due_line("P4a").title() + ". Two sheets as PDF, "
               "plus the editable field graph with the source fields retained."),
    ("BRING", "BOOK checkpoint, " + C.date_long(12).title() + ": one booklet spread and your "
              "contents list, for an ungraded progress check."),
    ("CHOOSE", "The volume you will slice. Export or keep the extracted surface ready to cut with "
               "section planes next week."),
])

d.save(os.path.join(OUT, "ARC3133_Class11.pptx"))
print("class11 ok — %d slides" % len(d.prs.slides._sldIdLst))
