# -*- coding: utf-8 -*-
"""Class 12 — Discretizing Geometry (U09). P4a due, P4b issued, BOOK checkpoint."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(12)
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 12
FAB_RUBRIC = ("Visual documentation 20% · computational understanding 20% · technical execution 15% "
              "· fabrication quality 30% · experimentation 5% · requirements and identity 10%.")


def slices(s, cx, cy, rx, ry, n, vertical=False, col=BLACK, t=0.045):
    """Section a (lumpy) ellipse with n evenly spaced planes; draw each contour as a bar."""
    def half(u):  # half-width of the blob at normalised position u in [-1, 1]
        return max(0.0, 1 - u * u) ** 0.5 * (1 + 0.18 * math.sin(3 * u + 0.6))
    for k in range(n):
        u = -1 + (k + 0.5) * 2.0 / n
        if vertical:
            hh = ry * half(u)
            s.rect(cx + u * rx - t / 2, cy - hh, t, 2 * hh, fill=col, line=None)
        else:
            hw = rx * half(u)
            s.rect(cx - hw, cy + u * ry - t / 2, 2 * hw, t, fill=col, line=None)


# 1 ── TITLE
title_slide(d, WK, ["DISCRETIZING", "GEOMETRY"],
            "P4 CONTINUES — FROM A CONTINUOUS VOLUME TO ORDERED PARTS", bg=PINK, lfill=YELLOW, rfill=CYAN)

# 2 ── TODAY
s = d.slide(BLACK)
s.header("TODAY", "Three things change hands before we cut a single section.")
today = [("DUE", CYAN, "P4a — SDF VOLUME", C.due_line("P4a"),
          "Two sheets as PDF, plus the editable field graph with the source fields retained."),
         ("CHECKPOINT", LIME, "BOOK — PROGRESS CHECK", C.date_long(WK),
          C.checkpoints("BOOK")[0][1] + " Ungraded."),
         ("ISSUED", YELLOW, "P4b — SLICES", C.due_line("P4b"),
          "Your P4a volume becomes laser-cut parts. Brief at the end of the class.")]
x = L
for tag, col, ttl, meta, body in today:
    s.chip(x, 2.05, 3.85, 0.5, tag, fill=col, size=13)
    s.card(x, 2.7, 3.85, 2.75, fill=CREAM)
    s.t(x + 0.28, 2.9, 3.3, 0.4, [s.Ab(ttl, 14.5)])
    s.t(x + 0.28, 3.35, 3.3, 0.35, [s.Ab(meta, 10.5, GREY)])
    s.t(x + 0.28, 3.85, 3.3, 1.5, [s.Cb(body, 13)], ls=1.3)
    x += 4.08
s.banner(5.85, "THE VOLUME YOU SELECTED ON P4a SHEET 2 IS THE ONE YOU SLICE. DO NOT START A NEW ONE.",
         fill=PINK, h=0.7, align=PP_ALIGN.CENTER)

# 3 ── FOUR DECISIONS
s = d.slide(CREAM)
s.header("FOUR DECISIONS BEFORE ANY CUT",
         "A slice set is not a setting. Each of these changes what the assembly says about the volume.")
dec = [("PLANE", CYAN, "What cuts the volume: a plane, repeated. The contour is where they meet."),
       ("DIRECTION", LIME, "Which way the planes face. It decides which profiles you see."),
       ("INTERVAL", YELLOW, "The distance between planes. It sets the gaps, the light and the part count."),
       ("ORDER", PINK, "Which slice is first. The order becomes the labels and the assembly.")]
y = 1.95
for nm, col, body in dec:
    s.chip(L, y, 2.2, 0.82, nm, fill=col, size=14)
    s.card(L + 2.5, y, 4.4, 0.82, fill=CREAM)
    s.t(L + 2.75, y, 3.95, 0.82, [s.Cb(body, 12.5)], ls=1.2, anchor=MSO_ANCHOR.MIDDLE)
    y += 1.02
s.card(8.1, 1.95, 4.55, 3.88, fill=CREAM)
s.t(8.35, 2.1, 4.0, 0.3, [s.Ab("ONE VOLUME, 12 HORIZONTAL PLANES", 10.5, GREY)])
slices(s, 10.37, 4.0, 1.7, 1.45, 12)
s.t(8.35, 5.5, 4.0, 0.3, [s.Cb("01 at the bottom · 12 at the top", 10.5, GREY)])
s.banner(6.15, "P4b asks for at least 12 ordered slices. Twelve is the floor, not the target.",
         fill=BLACK, color=LIME, h=0.68, align=PP_ALIGN.CENTER)

# 4 ── COMPARE
s = d.slide(CREAM)
s.header("COMPARE BEFORE YOU COMMIT",
         "Same volume, three slice sets. P4b asks you to compare two directions or two intervals.")
cmp_ = [("HORIZONTAL · WIDE", CYAN, dict(n=10), "Reads as a stack. Clear profile, open gaps."),
        ("VERTICAL · WIDE", LIME, dict(n=10, vertical=True), "Reads as fins. The silhouette changes with view."),
        ("HORIZONTAL · TIGHT", PINK, dict(n=20, t=0.03), "Nearly continuous. More parts, less light.")]
x = L
for nm, col, kw, cap in cmp_:
    s.panel(x, 1.95, 3.85, 3.7, nm, headfill=col, tsize=14)
    slices(s, x + 1.925, 3.6, 1.35, 0.95, **kw)
    s.t(x + 0.28, 4.75, 3.3, 0.8, [s.Cb(cap, 13)], ls=1.3, align=PP_ALIGN.CENTER)
    x += 4.08
for x, nm, col, body in [(L, "LOST", MUTE, "Everything between the planes. Curvature becomes steps."),
                         (6.8, "GAINED", LIME, "Gaps, light and a reading of the form. Parts a machine can cut.")]:
    s.chip(x, 5.95, 1.4, 0.95, nm, fill=col, size=13)
    s.card(x + 1.6, 5.95, 4.25, 0.95, fill=CREAM)
    s.t(x + 1.85, 5.95, 3.8, 0.95, [s.Cb(body, 13)], anchor=MSO_ANCHOR.MIDDLE, ls=1.2)

# 5 ── DESIGNED PARTS, NOT PRINTER LAYERS
s = d.slide(BLACK)
s.header("SLICES ARE DESIGNED PARTS",
         "In Week 3 a slicer made the layers for you. Here, every section is a part you decide on.")
s.panel(L, 2.05, 5.85, 3.4, "PRINTER LAYERS", headfill=MUTE)
s.t(L + 0.3, 2.8, 5.25, 2.5, [
    s.Cb("Generated by the slicer, not by you.", 14),
    s.Cb(" ", 6),
    s.Cb("Hundreds of them, fused into one object.", 14),
    s.Cb(" ", 6),
    s.Cb("You never see one on its own.", 14)], ls=1.3)
s.panel(6.8, 2.05, 5.85, 3.4, "SECTION PARTS", headfill=LIME)
s.t(7.1, 2.8, 5.25, 2.5, [
    s.Cb("Chosen: direction, interval, order.", 14),
    s.Cb(" ", 6),
    s.Cb("A countable set, each with a thickness, a label and a place in the assembly.", 14),
    s.Cb(" ", 6),
    s.Cb("Every one is visible in the finished piece.", 14)], ls=1.3)
s.banner(5.8, "DECIDE WHICH CURVES ARE PART BOUNDARIES BEFORE YOU ASSIGN THICKNESS OR SEND A MACHINE FILE.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 6 ── THE UNIT, STEP BY STEP
unit_steps_slide(d, "U09", title="THE SEQUENCE",
                 sub="Steps 1 and 2 today. Steps 3 and 4 are next week's class.")

# 7 ── PSEUDOCODE
pseudocode_slide(d, "U09",
                 sub="Slice in order, then prepare each part. The loop is the same one you wrote for arrays.",
                 note="THE FIRST LOOP IS TODAY. THE SECOND LOOP — KERF, LABEL, NEST — IS NEXT WEEK.",
                 size=11)

# 8 ── ISSUED — P4b
issued_slide(d, "P4b",
             blurb="Take the volume you selected in P4a and translate it into at least twelve ordered "
                   "sections. Compare two directions or intervals, give the slices a thickness and a "
                   "registration system, then laser-cut and assemble them within one sheet of material.",
             cards=[("COMPARE", "TWO SLICE SETS", "Two directions or two intervals, from the same volume."),
                    ("MAKE", "12+ PARTS", "Thickness, registration, labels, nesting. Within 300 mm."),
                    ("SHOW", "ONE PROCESS SHEET", "Volume, sections, cutting layout, assembly, photographs.")])

# 9 ── REQUIREMENTS
s = requirements_slide(d, "P4b", sub=None)
s.t(L, 1.4, W, 0.34, [s.C(FAB_RUBRIC, 12, GREY)])

# 10 ── NOW
now_slide(d, "NOW — CUT THE VOLUME",
          "Rest of the class: sections from your P4a volume, compared before anything is chosen.",
          ["P4a submitted, and your booklet spread and contents list checked",
           "Your selected volume sectioned by a sequence of planes",
           "The contours ordered, with slice 01 identified",
           "A second slice set: another direction or another interval",
           "The two sets set side by side, with a sentence on what each one shows"],
          closer="IF THE TWO SETS LOOK THE SAME, CHANGE MORE.",
          bg=LIME)

# 11 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "Week 13 (target " + C.date_long(13).split("— ")[1] + ") — Parts for the laser cutter: "
             "registration, kerf and fit, labels and nesting."),
    ("BRING", "A candidate slice set: at least 12 ordered contours, with the direction and interval "
              "written down, and your comparison of two sets."),
    ("CHECK", "P4b checkpoint, " + C.date_long(13).title() + " (target): " + C.checkpoints("P4b")[0][1]),
    ("FIND", "Your material: measure the sheet you plan to use and confirm its size and thickness "
             "with the FabLab before you design parts around it."),
])

d.save(os.path.join(OUT, "ARC3133_Class12.pptx"))
print("class12 ok — %d slides" % len(d.prs.slides._sldIdLst))
