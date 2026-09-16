# -*- coding: utf-8 -*-
"""Class 10 — Midterm review (Projects 1–3), then Volumetric Data (U07): SDF.
GSM, P2b, P3c, P3d and MID due. P4a issued."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 10

VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")
DUE_MID = sorted(m["id"] for m in C.milestones_due(WK))


def sdf_dots(s, x, y, fn, cols=11, rows=8, p=0.26, band=0.09):
    """Sample a 2D signed distance function on a grid of dots.
    Inside (negative) = pink, outside (positive) = grey, near zero = black."""
    for i in range(cols):
        for j in range(rows):
            px, py = i * p, j * p
            v = fn(px, py)
            if abs(v) < band:
                s.dot(x + px, y + py, d=0.12, fill=BLACK)
            elif v < 0:
                s.dot(x + px, y + py, d=0.10, fill=PINK)
            else:
                s.dot(x + px, y + py, d=0.05, fill=MUTE)


def circle(cx, cy, r):
    return lambda px, py: math.hypot(px - cx, py - cy) - r


def box(cx, cy, bx, by):
    def f(px, py):
        qx, qy = abs(px - cx) - bx, abs(py - cy) - by
        return math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0)
    return f


# 1 ── TITLE
title_slide(d, WK, ["MIDTERM REVIEW", "+ VOLUMETRIC DATA"],
            "PART 1 — PROJECTS 1–3 ON THE WALL · PART 2 — P4 BEGINS",
            bg=PINK, lfill=YELLOW, rfill=CYAN, right_tag="MIDTERM — %d DUE" % len(DUE_MID))

# 2 ── RUNNING ORDER
s = d.slide(BLACK)
s.header("PART 1 — RUNNING ORDER",
         "Due today: %s. Everything is on the wall before the first presentation." % " · ".join(DUE_MID))
order = [("01", "PIN UP", "Prints, the plotted drawing and the 3D print, in project order."),
         ("02", "PROJECT 1", "The manual, and one rule you can point to on every other sheet."),
         ("03", "PROJECT 2", "The process sheet, the print, and what changed for printability."),
         ("04", "PROJECT 3", "Module, arrays, plotted field, site analysis — as one sequence."),
         ("05", "LIVE", "Open the file. Change one thing in front of the room.")]
y = 2.0
for i, (n, ttl, body) in enumerate(order):
    s.chip(L, y, 0.7, 0.58, n, fill=ACCENTS[i % 4], size=13)
    s.t(L + 0.95, y, 1.9, 0.58, [s.A(ttl, 13)], anchor=MSO_ANCHOR.MIDDLE)
    s.t(L + 2.85, y, 3.9, 0.58, [s.C(body, 12.5)], anchor=MSO_ANCHOR.MIDDLE, ls=1.15)
    y += 0.8
s.panel(7.95, 2.0, 4.7, 3.9, "THE LIVE CHANGE", headfill=YELLOW, tsize=14)
s.t(8.25, 2.75, 4.1, 3.0, [
    s.Cb("CHOOSE", 13.5, bold=True),
    s.Cb("One parameter: an attractor position, a count, a radius, a setting.", 13.5),
    s.Cb("PREDICT", 13.5, bold=True),
    s.Cb("Say what will happen before you touch it.", 13.5),
    s.Cb("CHANGE AND EXPLAIN", 13.5, bold=True),
    s.Cb("Name the nodes, or the analysis settings, that made it happen.", 13.5)], ls=1.2)
s.banner(6.2, "IF THE PREDICTION WAS WRONG, SAY WHY. THAT IS ALSO UNDERSTANDING.",
         fill=CYAN, h=0.62, align=PP_ALIGN.CENTER)

# 3 ── WHAT IS ASSESSED
s = requirements_slide(d, "MID", title="PART 1 — WHAT IS ASSESSED",
                       sub="Revision and coherence across Projects 1–3, presented and changed live.")

# 4 ── MESH VS FIELD
s = d.slide(CREAM)
s.header("PART 2 — A MESH OR A FIELD",
         "Two ways to describe the same solid. Until now you have only used one.")
s.panel(L, 1.95, 5.85, 3.5, "MESH — THE SKIN", headfill=MUTE)
s.t(L + 0.3, 2.7, 5.25, 2.6, [
    s.Mb("vertices + edges + faces", 13),
    s.Cb(" ", 6),
    s.Cb("Stores only the surface. Inside and outside are implied by the faces.", 14),
    s.Cb(" ", 6),
    s.Cb("A Boolean has to cut and rebuild faces, and can fail.", 14)], ls=1.3)
s.panel(6.8, 1.95, 5.85, 3.5, "FIELD — A VALUE EVERYWHERE", headfill=LIME)
s.t(7.1, 2.7, 5.25, 2.6, [
    s.Mb("value = f(x, y, z)", 13),
    s.Cb(" ", 6),
    s.Cb("Every point in space has a number. The surface is where the number crosses a threshold.", 14),
    s.Cb(" ", 6),
    s.Cb("A Boolean is arithmetic on two numbers. It cannot fail.", 14)], ls=1.3)
s.banner(5.75, "YOU HAVE ALREADY DRAWN A FIELD: THE P3c GRAYSCALE. THIS IS THE SAME IDEA, IN 3D.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

# 5 ── DENSITY VS SIGNED DISTANCE
s = d.slide(BLACK)
s.header("DENSITY OR SIGNED DISTANCE",
         "Two kinds of field. P4a is built on the second.")
s.panel(L, 2.0, 3.9, 3.9, "DENSITY", headfill=CYAN, tsize=14.5)
s.t(L + 0.25, 2.75, 3.4, 3.0, [
    s.Cb("How much is here.", 14, bold=True),
    s.Cb(" ", 5),
    s.Cb("Counted from samples, such as points within a radius. High inside a cluster, zero far "
         "away.", 13.5),
    s.Cb(" ", 5),
    s.Cb("The surface is a threshold you choose.", 13.5)], ls=1.3)
s.panel(4.8, 2.0, 3.9, 3.9, "SIGNED DISTANCE", headfill=LIME, tsize=14.5)
s.t(5.05, 2.75, 3.4, 3.0, [
    s.Cb("How far to the surface, with a sign.", 14, bold=True),
    s.Cb(" ", 5),
    s.Mb("d < 0   inside", 13),
    s.Mb("d = 0   the boundary", 13),
    s.Mb("d > 0   outside", 13),
    s.Cb(" ", 5),
    s.Cb("The surface is always at zero.", 13.5)], ls=1.3)
s.card(8.95, 2.0, 3.7, 3.9, fill=CREAM)
sdf_dots(s, 9.23, 2.3, circle(1.3, 0.95, 0.8), cols=12, rows=8, p=0.285)
s.t(9.2, 4.75, 3.25, 1.0, [
    [s.Ab("● ", 12, PINK), s.Cb("inside   ", 12), s.Ab("● ", 12, BLACK), s.Cb("zero", 12)],
    [s.Ab("● ", 12, MUTE), s.Cb("outside — a circle, sampled", 12)]], ls=1.3)
s.banner(6.2, "INSIDE, OUTSIDE AND THE ZERO BOUNDARY: SAY WHICH ONE YOU ARE LOOKING AT.",
         fill=YELLOW, h=0.62, align=PP_ALIGN.CENTER)

# 6 ── PRIMITIVES AS FUNCTIONS
s = d.slide(CREAM)
s.header("A SHAPE IS A FUNCTION",
         "Give it a point, get back a signed distance. No vertices anywhere.")
s.panel(L, 1.95, 5.85, 3.7, "SPHERE", headfill=CYAN)
s.t(L + 0.3, 2.7, 5.25, 1.2, [
    s.Mb("sphere(p, c, r):", 13),
    s.Mb("    return length(p − c) − r", 13)], ls=1.35)
s.t(L + 0.3, 3.45, 5.25, 0.7, [
    s.Cb("Distance to the centre, minus the radius. On the surface that is exactly zero.", 13.5)],
    ls=1.3)
sdf_dots(s, L + 3.35, 4.25, circle(0.55, 0.55, 0.45), cols=5, rows=5, p=0.24)
s.panel(6.8, 1.95, 5.85, 3.7, "BOX", headfill=PINK)
s.t(7.1, 2.7, 5.25, 1.2, [
    s.Mb("box(p, c, b):", 13),
    s.Mb("    q = abs(p − c) − b", 13),
    s.Mb("    return length(max(q, 0))", 13),
    s.Mb("         + min(max(q.x, q.y, q.z), 0)", 13)], ls=1.35)
s.t(7.1, 4.2, 2.6, 1.3, [
    s.Cb("b is the half-size on each axis. Same idea, one more line.", 13.5)], ls=1.3)
sdf_dots(s, 10.1, 4.25, box(0.6, 0.55, 0.42, 0.3), cols=6, rows=5, p=0.24)
s.banner(5.95, "CHANGE r OR b AND THE WHOLE FIELD CHANGES. THE PARAMETER IS STILL LIVE.",
         fill=LIME, h=0.68, align=PP_ALIGN.CENTER)

# 7 ── CSG AS MIN AND MAX
s = d.slide(CREAM)
s.header("THE BOOLEANS AGAIN — AS MIN AND MAX",
         "The same three operations from P2. On fields, each is one line.")
a = circle(0.78, 0.78, 0.6)
b = circle(1.42, 0.78, 0.6)
ops = [("UNION", CYAN, "min(a, b)", lambda x, y: min(a(x, y), b(x, y))),
       ("INTERSECTION", LIME, "max(a, b)", lambda x, y: max(a(x, y), b(x, y))),
       ("DIFFERENCE", PINK, "max(a, −b)", lambda x, y: max(a(x, y), -b(x, y)))]
x = L
for nm, col, eq, fn in ops:
    s.panel(x, 1.95, 3.85, 3.55, nm, headfill=col, tsize=15)
    s.t(x + 0.25, 2.62, 3.35, 0.4, [s.Mb(eq, 16, bold=True)], align=PP_ALIGN.CENTER)
    sdf_dots(s, x + 0.78, 3.2, fn, cols=10, rows=7, p=0.23, band=0.08)
    x += 4.08
s.banner(5.8, "UNION KEEPS THE NEARER SURFACE. INTERSECTION KEEPS THE FARTHER. DIFFERENCE FLIPS b "
              "INSIDE OUT, THEN INTERSECTS.", fill=BLACK, color=YELLOW, h=0.72, align=PP_ALIGN.CENTER)
s.t(L, 6.7, W, 0.4, [s.C("Same operands as P2, so the same rule: a − b is not b − a.", 13.5, GREY)])

# 8 ── BLEND, RESOLUTION, EXTRACTION
s = d.slide(BLACK)
s.header("BLEND, SAMPLE, EXTRACT",
         "Three steps turn a function into something you can see, slice and cut.")
steps = [("SMOOTH BLEND", CYAN, "smooth_min(a, b, k)",
          "k = 0 is a hard union. Larger k fills the joint with a soft fillet. A mesh Boolean "
          "cannot do this."),
         ("RESOLUTION", LIME, "sample(field, bounds, n)",
          "The field is read on a grid. Coarse is fast and faceted. Fine is smooth and slow. State "
          "the number."),
         ("SURFACE EXTRACTION", YELLOW, "extract(grid, iso=0.0)",
          "A mesh is built where the samples cross zero. Only now does the volume have faces.")]
x = L
for nm, col, eq, body in steps:
    s.panel(x, 2.0, 3.85, 3.6, nm, headfill=col, tsize=14.5)
    s.t(x + 0.25, 2.72, 3.35, 0.4, [s.Mb(eq, 11.5)])
    s.rule(x + 0.25, 3.25, 3.35, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.25, 3.45, 3.35, 2.0, [s.Cb(body, 13.5)], ls=1.3)
    x += 4.08
s.banner(6.0, "P4a ASKS YOU TO STATE THE SAMPLING RESOLUTION AND THE EXTRACTION SETTINGS.",
         fill=PINK, h=0.68, align=PP_ALIGN.CENTER)

# 9 ── PSEUDOCODE
pseudocode_slide(d, "U07", size=9.5,
                 sub="The top half reads a point cloud. Today is the bottom half: a shape as a function.",
                 note="FROM “def field” DOWN IS P4a: TWO FIELDS, ONE BLEND, ONE GRID, ONE SURFACE AT ZERO.")

# 10 ── ISSUED — P4a
issued_slide(d, "P4a",
             blurb="Project 4 begins. Build a volume from signed distance fields — the CSG logic from P2, "
                   "applied to fields instead of meshes — and choose the one you will slice and "
                   "laser-cut in P4b.",
             cards=[("COMPARE", "SAME FIELDS", "Union, intersection and difference of the same sources."),
                    ("VARY", "THREE VARIANTS", "Three controlled parameter changes on the chosen result."),
                    ("STATE", "HOW IT WAS READ", "Resolution, extraction settings, and the spatial intention.")])

# 11 ── REQUIREMENTS — P4a
requirements_slide(d, "P4a", sub=VISUAL)

# 12 ── NOW
now_slide(d, "NOW — YOUR FIRST FIELD VOLUME",
          "After the review: two primitives, three Booleans, one surface.",
          ["A sphere field sampled on a grid and extracted at zero",
           "A box field beside it, each with its size exposed",
           "Union as min, then swapped for max, then for max(a, −b)",
           "A smooth blend, with k changed until you can see the joint",
           "The same volume extracted at two resolutions, and the numbers written down"],
          closer="IF YOU CAN SAY WHERE ZERO IS, YOU CAN SAY WHERE THE SURFACE IS.",
          bg=LIME)

# 13 ── BEFORE NEXT CLASS
cp = C.checkpoints("P4a")[0]
before_next_slide(d, [
    ("NEXT", "%s: SDF volume studio work — primitives, the three Booleans, smooth blend, noise and "
             "surface extraction." % C.date_long(11).title()),
    ("P4a", "Checkpoint %s. %s" % (C.date_long(cp[0]).title(), cp[1])),
    ("DUE", "P4a is due %s (%d%%): two sheets, the editable graph and the source fields."
            % (C.date_long(C.milestone("P4a")["due"]).title(), C.milestone("P4a")["weight"])),
    ("NOTE", "Dates after the midterm are provisional. Check the course site each week."),
])

d.save(os.path.join(OUT, "ARC3133_Class10.pptx"))
print("class10 ok — %d slides" % len(d.prs.slides._sldIdLst))
