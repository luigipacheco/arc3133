# -*- coding: utf-8 -*-
"""Class 10 — Mid-semester deadline (everything through Arrays is in), then Volumetric Data
(U07): SDF. GSM, P2b and P3c due. P3d checkpoint. P4a issued."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(10)
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 10

VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")
DUE_TODAY = sorted(m["id"] for m in C.milestones_due(WK))


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
title_slide(d, WK, ["DEADLINE WEEK", "+ VOLUMETRIC DATA"],
            "EVERYTHING THROUGH ARRAYS IS IN · PROJECT 4 BEGINS",
            bg=PINK, lfill=YELLOW, rfill=CYAN,
            foot="MID-SEMESTER DEADLINE  /  P4a ISSUED TODAY  /  P3d CHECKPOINT TODAY")

# 2 ── DUE TODAY
SUBMIT = {"GSM": "Four pages, each rule beside a tested application. Revised again for the booklet.",
          "P2b": "The print and its process sheet, handed in, with the source, mesh and slicer files.",
          "P3c": "One 17 × 11 sheet: line drawing, grayscale field and legend. SVG, PDF and graph."}
s = d.slide(BLACK)
s.header("DUE TODAY — THE MID-SEMESTER DEADLINE",
         "Everything through Arrays must be in today. This is a regular class after that.")
y = 1.95
for i, mid in enumerate(DUE_TODAY):
    m = C.milestone(mid)
    s.chip(L, y, 1.1, 0.95, mid, fill=ACCENTS[i % 4], size=16)
    s.card(L + 1.35, y, W - 1.35, 0.95, fill=CREAM)
    s.t(L + 1.6, y + 0.1, 6.5, 0.35, [s.Ab(m["title"].upper(), 13)])
    s.t(W - 3.3, y + 0.1, 3.8, 0.35, [s.A(C.due_line(mid), 10.5, GREY)], align=PP_ALIGN.RIGHT)
    s.t(L + 1.6, y + 0.48, W - 1.9, 0.4, [s.Cb(SUBMIT.get(mid, ""), 12.5)])
    y += 1.1
earlier = sorted(m["id"] for m in C.MILESTONES.values()
                 if isinstance(m.get("due"), int) and m["due"] < WK)
s.t(L, y + 0.02, W, 0.35, [s.C("Already due and expected in: %s." % ", ".join(earlier), 13, MUTE)])
cp_d = C.checkpoints("P3d")[0][1]
s.banner(5.55, "P3d CHECKPOINT TODAY · " + cp_d.upper(), fill=YELLOW, h=0.62, size=12,
         align=PP_ALIGN.CENTER)
s.t(L, 6.4, W, 0.4, [s.C("P3d is due next class, %s. P4a is issued today."
                         % C.date_long(C.milestone("P3d")["due"]).title(), 13, MUTE)])

# 4 ── MESH VS FIELD
s = d.slide(CREAM)
s.header("A MESH OR A FIELD",
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

# 9 ── ISSUED — P4a
issued_slide(d, "P4a",
             blurb="Project 4 begins. Build a volume from signed distance fields — the CSG logic from P2, "
                   "applied to fields instead of meshes — and choose the one you will slice and "
                   "laser-cut in P4b.",
             cards=[("COMPARE", "SAME FIELDS", "Union, intersection and difference of the same sources."),
                    ("VARY", "THREE VARIANTS", "Three controlled parameter changes on the chosen result."),
                    ("STATE", "HOW IT WAS READ", "Resolution, extraction settings, and the spatial intention.")])

# 10 ── REQUIREMENTS — P4a
requirements_slide(d, "P4a", sub=VISUAL)

# 11 ── NOW
now_slide(d, "NOW — YOUR FIRST FIELD VOLUME",
          "Rest of the class: two primitives, three Booleans, one surface.",
          ["A sphere field sampled on a grid and extracted at zero",
           "A box field beside it, each with its size exposed",
           "Union as min, then swapped for max, then for max(a, −b)",
           "A smooth blend, with k changed until you can see the joint",
           "The same volume extracted at two resolutions, and the numbers written down"],
          closer="IF YOU CAN SAY WHERE ZERO IS, YOU CAN SAY WHERE THE SURFACE IS.",
          bg=LIME)

# 12 ── BEFORE NEXT CLASS
cp = C.checkpoints("P4a")[0]
before_next_slide(d, [
    ("NEXT", "%s: SDF volume studio work — primitives, the three Booleans, smooth blend, noise and "
             "surface extraction." % C.date_long(11).title()),
    ("P3d", "Due next class, %s: one sheet with each layer small, with its legend, beside the "
            "combined view, and the working file." % C.date_long(C.milestone("P3d")["due"]).title()),
    ("P4a", "Checkpoint %s. %s" % (C.date_long(cp[0]).title(), cp[1])),
    ("DUE", "P4a is due %s (%d%%): two sheets, the editable graph and the source fields. Later "
            "dates are provisional." % (C.date_long(C.milestone("P4a")["due"]).title(),
                                        C.milestone("P4a")["weight"])),
])

d.save(os.path.join(OUT, "ARC3133_Class10.pptx"))
print("class10 ok — %d slides" % len(d.prs.slides._sldIdLst))
