# -*- coding: utf-8 -*-
"""Class 03 — Geometry from scratch (U03). P1b + P1c issued."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 3

# 1 ── TITLE
title_slide(d, WK, ["GEOMETRY", "FROM SCRATCH"],
            "P1 CONTINUES — WHAT A SOLID IS MADE OF, UNDERNEATH", bg=YELLOW, lfill=CYAN, rfill=LIME)

# 2 ── THE LADDER
s = d.slide(BLACK)
s.header("POINT → LINE → EDGE → FACE → SOLID",
         "Five steps, and each one is a list of the thing before it.")
rungs = [("POINT", CYAN, "three numbers", "[x, y, z]"),
         ("LINE", LIME, "two positions", "[p1, p2]"),
         ("EDGE", YELLOW, "two vertices", "[v1, v2]"),
         ("FACE", PINK, "ordered corners", "[v1, v2, v3]"),
         ("MESH", CYAN, "many faces", "[f1, f2, f3…]")]
x = L
wd = (W - 0.2 * 4) / 5
for nm, col, sub, code in rungs:
    s.chip(x, 2.1, wd, 0.5, nm, fill=col, size=13)
    s.card(x, 2.7, wd, 1.9, fill=CREAM)
    s.t(x + 0.2, 2.95, wd - 0.4, 0.5, [s.Cb(sub, 12.5)], align=PP_ALIGN.CENTER)
    s.t(x + 0.2, 3.6, wd - 0.4, 0.5, [s.Mb(code, 11.5)], align=PP_ALIGN.CENTER)
    x += wd + 0.2
s.banner(4.95, "A POSITION IS NOT A DISPLACEMENT. THE SAME THREE NUMBERS MEAN DIFFERENT THINGS "
              "DEPENDING ON WHICH ONE YOU MEANT.", fill=YELLOW, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 5.9, W, 0.9, [s.C("Nothing here is new geometry. It is the same collection, read at a "
                         "different level: a face is a list of vertices, a mesh is a list of faces, "
                         "and next week an array will be a list of copies.", 13.5, MUTE)], ls=1.3)

# 3 ── A FACE IS AN ORDERED LIST
s = d.slide(CREAM)
s.header("A FACE IS AN ORDERED LIST OF CORNERS",
         "Same three vertices, two different faces. The order is the difference.")
s.panel(L, 1.95, 6.0, 3.4, "WINDING ORDER", headfill=CYAN)
cx0, cy0 = L + 1.4, 3.6
tri = [(cx0, cy0 - 0.7), (cx0 - 0.75, cy0 + 0.55), (cx0 + 0.75, cy0 + 0.55)]
for i, (px, py) in enumerate(tri):
    s.dot(px, py, d=0.16, fill=BLACK)
    s.t(px - 0.35, py - 0.42, 0.7, 0.3, [s.Mb("v%d" % i, 11)], align=PP_ALIGN.CENTER)
s.t(L + 3.0, 2.75, 2.8, 2.3, [
    s.Mb("f = [v0, v1, v2]", 12, bold=True),
    s.Mb("  normal → toward you", 11),
    s.Mb(" ", 8),
    s.Mb("f = [v0, v2, v1]", 12, bold=True),
    s.Mb("  normal → away", 11)], ls=1.4)
s.panel(7.0, 1.95, 5.65, 3.4, "WHY IT MATTERS LATER", headfill=PINK, tsize=14.5)
s.t(7.3, 2.72, 5.05, 2.4, [
    s.Cb("A flipped face tells a renderer the inside is the outside.", 14),
    s.Cb(" ", 7),
    s.Cb("It tells a slicer there is nothing to fill.", 14),
    s.Cb(" ", 7),
    s.Cb("Most failed prints this semester will start here, not at the printer.", 14)], ls=1.3)
s.banner(5.65, "CLOSED MEANS EVERY EDGE IS SHARED BY EXACTLY TWO FACES. CHECK IT BEFORE YOU BELIEVE IT.",
         fill=LIME, h=0.72, align=PP_ALIGN.CENTER)

# 4 ── THE PYRAMID
s = d.slide(BLACK)
s.header("THE PYRAMID", "Five vertices, eight edges, five faces. Built by hand, driven by three numbers.")
s.panel(L, 2.05, 6.2, 3.3, "WHAT YOU ASSEMBLE", headfill=LIME)
counts = [("5", "VERTICES", "four base corners and an apex"),
          ("8", "EDGES", "four around the base, four to the apex"),
          ("5", "FACES", "four triangular sides and the base")]
y = 2.85
for n, nm, body in counts:
    s.chip(L + 0.35, y, 0.75, 0.62, n, fill=CYAN, size=17)
    s.t(L + 1.35, y, 4.6, 0.3, [s.Ab(nm, 12.5)])
    s.t(L + 1.35, y + 0.3, 4.6, 0.3, [s.Cb(body, 11.5)])
    y += 0.78
s.panel(7.15, 2.05, 5.5, 3.3, "EXPOSED INPUTS", headfill=YELLOW)
s.t(7.45, 2.85, 4.9, 2.2, [
    s.Mb("Width", 14, bold=True), s.Mb("Depth", 14, bold=True), s.Mb("Height", 14, bold=True),
    s.Mb(" ", 8),
    s.Cb("Three numbers, and the whole solid rebuilds. That is the entire point of the exercise.", 13)], ls=1.4)
s.banner(5.7, "DO NOT FORGET THE BASE FACE. A PYRAMID WITH FOUR SIDES AND NO BOTTOM IS NOT A SOLID.",
         fill=PINK, h=0.7, align=PP_ALIGN.CENTER)

# 5 ── IT BECOMES THE CUTTER
s = d.slide(CREAM)
s.header("AND THEN IT GOES BACK INTO LAST WEEK'S FILE",
         "The pyramid is not an exercise. It is the cutter for the study you already built.")
flow = [("01", "BUILD IT", CYAN, "Five vertices, five faces, closed, with Width / Depth / Height exposed."),
        ("02", "SUBTRACT IT", LIME, "Cube minus pyramid. The same Boolean from Week 2, with your own solid."),
        ("03", "DRIVE IT", YELLOW, "Change the three inputs and show at least three settings of the result."),
        ("04", "EXPLAIN IT", PINK, "Face order, normals, closure — why it cuts cleanly instead of failing.")]
x = L
wd = (W - 0.23 * 3) / 4
for n, ttl, col, body in flow:
    s.chip(x, 1.95, wd, 0.5, n + "   " + ttl, fill=col, size=12.5)
    s.card(x, 2.55, wd, 2.2, fill=CREAM)
    s.t(x + 0.25, 2.55, wd - 0.5, 2.2, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += wd + 0.23
s.banner(5.05, "THIS IS WHY P1 IS ONE PROJECT AND NOT THREE ASSIGNMENTS.",
         fill=BLACK, color=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 5.95, W, 0.8, [s.C("Every project in this course does the same thing — the geometry you make "
                          "in one milestone becomes the input to the next. You will never start from "
                          "an unrelated object.", 13.5, GREY)], ls=1.3)

pseudocode_slide(d, "U03",
                 sub="A mesh is two lists. That is the entire idea, and it fits on one slide.",
                 note="verts IS A LIST OF POSITIONS. faces IS A LIST OF INDICES INTO IT.")

# 6 ── ISSUED — P1b
issued_slide(d, "P1b",
             blurb="Find a panel in a building you like, keep it simple, and build it out of two lists - "
                   "points and faces. It is the component you will array in P2 and the object you will "
                   "print, so choose something that tiles.",
             cards=[("FIND", "A PANEL", "One precedent, simple. It has to sit beside itself and close."),
                    ("DECIDE", "WHAT MOVES", "The parameters, first. One has to change its shape, not its box."),
                    ("BUILD", "FROM TWO LISTS", "Every point an expression of those numbers. Never a typed coordinate."),
                    ("SHOW", "THE RANGE", "Low, middle, high - still closing, still tiling. P2b drives it.")])

# 7 ── REQUIREMENTS P1b
requirements_slide(d, "P1b",
                   sub="Visual quality 35% · computational understanding 25% · technical execution 20% "
                       "· experimentation 10% · requirements and identity 10%.")

# 8 ── ALSO ISSUED — P1c
issued_slide(d, "P1c", badge="ALSO ISSUED", badgefill=PINK,
             blurb="The same geometry, made real. A printable variant of the project you have been "
                   "building for two weeks — presented as a physical object at the midterm.",
             cards=[("LIMIT", "60 MM, 200 G", "Each axis within 60 mm. The allocation includes failures."),
                    ("RULE", "NO SUPPORTS", "Orientation is your only lever. Change the geometry if you must."),
                    ("DUE", "AT THE MIDTERM", "The queue has latency the two-week cycle does not.")])

# 9 ── REQUIREMENTS P1c
requirements_slide(d, "P1c",
                   sub="Fabrication milestone — visual documentation 20% · computational understanding 20% "
                       "· technical execution 15% · fabrication quality 30% · experimentation 5% · "
                       "requirements 10%.")

# 10 ── NOW
now_slide(d, "NOW — BUILD THE PYRAMID",
          "Rest of the session: from a single point to a closed solid that cuts.",
          ["One point placed from an XYZ vector, and you can say why it is a position",
           "Four base corners and an apex, with Width / Depth / Height exposed",
           "All five faces joined — four sides and the base",
           "Closure checked: every edge shared by exactly two faces",
           "Cube minus pyramid working, off the same three inputs",
           "Your own panel named, and the numbers that will drive it written down"],
          closer="LEAVE WITH A SOLID THAT CUTS. THE SHEET IS THE EASY PART.",
          bg=CYAN)

# 11 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("WATCH", "U04 — Arrays and lists. Repeat Zone, Compare and Switch, and the nested grid. "
              "We start small and inspectable before anything scales up."),
    ("FINISH", "P1a is due next class: eight or nine numbered diagrams, the last one developed at "
               "building scale with a figure and planting, and the sequence written as pseudocode."),
    ("FIND", "The panel. One building, one repeating component, simple enough to write as two "
             "lists, and it has to sit beside itself without a gap. Name the building and your "
             "source, and bring its point and face lists started - next week it gets repeated."),
    ("CHECK", "Your FabLab orientation, before you need the machine rather than after."),
])

d.save(os.path.join(OUT, "ARC3133_Class03.pptx"))
print("class03 ok — %d slides" % len(d.prs.slides._sldIdLst))
