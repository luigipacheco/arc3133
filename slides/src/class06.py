# -*- coding: utf-8 -*-
"""Class 06 — Arrays 1D / 2D / 3D (U04, Week 6 steps). P3a due; P3b issued (sheet 1 today);
P2b print checkpoint."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 6
VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")

# 1 ── TITLE
title_slide(d, WK, ["ARRAYS", "1D · 2D · 3D"],
            "P3b BEGINS — SHEET 1: ONE MODULE, MANY POSITIONS", bg=LIME, lfill=PINK, rfill=CYAN,
            foot="P3b ISSUED TODAY  /  P2b PRINT CHECKPOINT TODAY")

# 2 ── AN ARRAY IS A LIST OF POSITIONS
s = d.slide(CREAM)
s.header("AN ARRAY IS A LIST OF POSITIONS",
         "Not a command that duplicates things. A list you compute, then place your module at.")
s.panel(L, 1.95, 5.6, 3.5, "INDEX  →  POSITION", headfill=CYAN)
s.t(L + 0.35, 2.75, 5.0, 2.4, [
    s.Mb("i = 0   →   p = start", 13.5),
    s.Mb("i = 1   →   p = start + step", 13.5),
    s.Mb("i = 2   →   p = start + 2 × step", 13.5),
    s.Mb(" ", 8),
    s.Mb("p[i] = start + i × step", 13.5, bold=True)], ls=1.35)
s.panel(6.6, 1.95, 6.05, 3.5, "THREE THINGS TO READ", headfill=PINK)
s.t(6.9, 2.72, 5.45, 2.5, [
    s.Cb("THE LIST — what is in the collection.", 14),
    s.Cb("THE COUNT — how many there are.", 14),
    s.Cb("THE INDEX — where each one sits in the order.", 14),
    s.Cb(" ", 7),
    s.Cb("The index is the only new idea. It is a counter that tells each copy how far along "
         "it is — and therefore where it goes.", 13.5)], ls=1.35)
s.banner(5.75, "Your P3a module is the component. It does not change in P3b — only where it goes.",
         fill=LIME, h=0.72)

# 3 ── THE REPEAT ZONE
s = d.slide(BLACK)
s.header("THE REPEAT ZONE", "The loop, made visible. Repeat Input, a body, Repeat Output.")
s.panel(L, 2.05, 6.2, 3.3, "WHAT IT IS", headfill=LIME)
s.t(L + 0.35, 2.8, 5.5, 2.3, [
    s.Mb("Repeat Input   →  body  →  Repeat Output", 12.5, bold=True),
    s.Mb(" ", 8),
    s.Cb("Everything between the two runs once per iteration. Whatever you hand to Repeat Input "
         "comes back changed, once for every step of the count.", 13.5)], ls=1.3)
s.panel(7.15, 2.05, 5.5, 3.3, "READ IT SMALL FIRST", headfill=CYAN)
s.t(7.45, 2.8, 4.9, 2.3, [
    s.Cb("Set the count to 3 and look at the spreadsheet.", 13.5),
    s.Cb(" ", 6),
    s.Cb("Then 4. Then 5.", 13.5),
    s.Cb(" ", 6),
    s.Cb("A collection you cannot inspect is a collection you cannot debug. There is no minimum "
         "count and no prize for a large one.", 13.5)], ls=1.3)
s.banner(5.7, "BUILD IT AT A COUNT YOU CAN COUNT. SCALE UP ONLY ONCE IT IS RIGHT.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 4 ── 1D → 2D → 3D
s = d.slide(CREAM)
s.header("ONE COUNTER, TWO, THREE",
         "Linear, nested grid, XYZ cube. Each one is the last one, repeated along a new axis.")
x = L
panels = [("1D — LINEAR", CYAN, "count = n", "n = 5  →  5"),
          ("2D — NESTED GRID", LIME, "count = n × n", "n = 5  →  25"),
          ("3D — XYZ CUBE", PINK, "count = n³", "n = 3  →  27")]
for nm, col, f, ex in panels:
    s.panel(x, 1.95, 3.85, 3.6, nm, headfill=col, tsize=14.5)
    s.t(x + 0.28, 4.55, 3.3, 0.3, [s.Mb(f, 12.5, bold=True)], align=PP_ALIGN.CENTER)
    s.t(x + 0.28, 4.9, 3.3, 0.3, [s.Mb(ex, 11.5)], align=PP_ALIGN.CENTER)
    x += 4.08
G.cartesian(s, L + 0.95, 3.35, cols=5, rows=1, p=0.48, d=0.16)
G.cartesian(s, L + 4.08 + 0.95, 2.72, cols=5, rows=5, p=0.38, d=0.14)
# the cube as three stacked layers, k = 0, 1, 2
cx, cy = L + 8.16 + 0.58, 3.0
for k in range(3):
    lx = cx + k * 1.05
    G.cartesian(s, lx, cy, cols=3, rows=3, p=0.3, d=0.13)
    s.t(lx - 0.2, cy + 0.85, 1.0, 0.3, [s.Mb("k = %d" % k, 10.5)], align=PP_ALIGN.CENTER)
s.banner(5.85, "PREDICT THE TOTAL BEFORE YOU LOOK. COMPARE 3, 4 AND 5 PER AXIS: 27, 64, 125.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 5 ── INDEX ORDER
s = d.slide(BLACK)
s.header("INDEX ORDER",
         "Which counter runs inside decides the order. Label it on the sheet.")
s.panel(L, 2.05, 6.2, 3.65, "A 4 × 3 GRID, i INSIDE j", headfill=LIME)
gx, gy, c = L + 0.9, 2.9, 0.72
for j in range(3):
    for i in range(4):
        idx = i + j * 4
        s.rect(gx + i * c, gy + (2 - j) * c, c, c, fill=[CYAN, LIME, YELLOW][j], line=BLACK, lw=HAIR)
        s.t(gx + i * c, gy + (2 - j) * c, c, c, [s.Mb(str(idx), 13, bold=True)],
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
s.t(gx + 4 * c + 0.2, gy + 0.1, 1.4, 2.0, [s.Mb("j = 2", 11), s.Mb(" ", 11), s.Mb("j = 1", 11),
                                           s.Mb(" ", 11), s.Mb("j = 0", 11)], ls=1.55)
s.t(gx, gy + 3 * c + 0.1, 4 * c, 0.3, [s.Mb("i →  0 · 1 · 2 · 3", 11)], align=PP_ALIGN.CENTER)
s.panel(7.15, 2.05, 5.5, 3.65, "THE FLAT INDEX", headfill=YELLOW)
s.t(7.45, 2.8, 4.9, 2.8, [
    s.Mb("2D:  index = i + j × cols", 13, bold=True),
    s.Mb("3D:  index = i + j × n + k × n²", 13, bold=True),
    s.Mb(" ", 8),
    s.Cb("Swap the loops and the same positions get different numbers. The picture looks the "
         "same; any rule that reads the index does not.", 13.5)], ls=1.35)
s.banner(6.0, "SAY IT OUT LOUD: WHICH WAY DOES i RUN, AND WHAT HAPPENS IF YOU SWAP THE LOOPS?",
         fill=PINK, h=0.68, align=PP_ALIGN.CENTER)

# 6 ── COMPARE + SWITCH IS AN IF
s = d.slide(CREAM)
s.header("COMPARE + SWITCH IS AN IF STATEMENT",
         "Test the index, then act on the answer. One conditional selection is encouraged in P3b.")
s.panel(L, 1.95, 6.0, 3.4, "THE PATTERN", headfill=PINK)
s.t(L + 0.35, 2.7, 5.3, 2.3, [
    s.Mb("Compare   3 <= i <= 5    →  True / False", 12),
    s.Mb("Switch    False → stay", 12),
    s.Mb("          True  → lift", 12),
    s.Mb(" ", 8),
    s.Cb("Compare asks the question. Switch chooses between two answers. Everything conditional "
         "in this course is those two nodes.", 13.5)], ls=1.3)
s.panel(7.0, 1.95, 5.65, 3.4, "AN INDEX RANGE, LIFTED", headfill=LIME, tsize=14.5)
for i in range(9):
    for j in range(3):
        sel = 3 <= i <= 5
        s.dot(7.45 + i * 0.52, 3.05 + j * 0.46 - (0.3 if sel else 0), d=0.16,
              fill=PINK if sel else BLACK)
s.t(7.3, 4.55, 5.05, 0.6, [s.Cb("Indices 3 to 5 moved. The module is the same; only its "
                                "placement changed.", 13)], ls=1.25)
s.banner(5.65, "CHECK THE RESULT AT TWO DIFFERENT COUNTS. IF IT ONLY WORKS AT ONE, IT IS NOT A RULE.",
         fill=CYAN, h=0.72, align=PP_ALIGN.CENTER)

# 7 ── THE SEQUENCE
unit_steps_slide(d, "U04", title="SHEET 1, STEP BY STEP", n=(0, 4),
                 sub="What we build together today: 1D, 2D, 3D, then one conditional.")

# 8 ── P2b CHECKPOINT
s = d.slide(CREAM)
s.header("P2b CHECKPOINT — PRINT GEOMETRY", C.checkpoints("P2b")[0][1])
checks = [("GEOMETRY", CYAN, "Closed and solid. Every edge shared by two faces, no stray pieces."),
          ("UNITS", LIME, "Real millimetres. Within 60 mm on each axis."),
          ("ORIENTATION", YELLOW, "No supports. Orientation is your lever; change the geometry if you must."),
          ("SLICED PREVIEW", PINK, "Read it layer by layer before queueing. Stay within the 200 g allocation.")]
y = 1.95
for nm, col, body in checks:
    s.chip(L, y, 2.6, 0.72, nm, fill=col, size=13)
    s.card(L + 2.9, y, W - 2.9, 0.72, fill=CREAM)
    s.t(L + 3.2, y, W - 3.5, 0.72, [s.Cb(body, 14)], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.92
s.banner(5.85, "P2b IS DUE AT THE MIDTERM, " + C.date_long(10).upper() + ". BRING THE PRINT AND ITS PROCESS SHEET.",
         fill=BLACK, color=LIME, h=0.7, align=PP_ALIGN.CENTER)

# 9 ── ISSUED — P3b
issued_slide(d, "P3b",
             blurb="One assignment, exactly two 17 × 11 sheets, submitted together. Array your P3a "
                   "module without changing it: sheet 1 today, sheet 2 next week.",
             cards=[("SHEET 1 · TODAY", "1D · 2D · 3D", "Linear, nested grid, XYZ cube. Count, spacing, "
                                                          "index order and predicted totals labelled."),
                    ("SHEET 2 · WEEK 7", "HEX · RADIAL · CURVE", "Staggered grid, radial array, and an "
                                                                  "array along a sine-driven curve."),
                    ("THE RULE", "THE MODULE STAYS", "Vary only its placement. Expose count and spacing "
                                                     "or radius in the graph.")])

# 10 ── REQUIREMENTS P3b
requirements_slide(d, "P3b", sub=VISUAL)

# 11 ── NOW
now_slide(d, "NOW — SHEET 1",
          "Rest of the class: three arrays you can predict, and one conditional.",
          ["Your module on a linear array, count and spacing exposed, spreadsheet open",
           "The array nested into a grid, total predicted before you looked",
           "The grid repeated in Z: 3, 4 and 5 per axis compared",
           "Index order labelled, and one index range moved with Compare and Switch",
           "P3a submitted, and your P2b print geometry checked"],
          closer="A COUNT YOU CAN COUNT. NOT A THOUSAND OF ANYTHING, YET.",
          bg=CYAN)

# 12 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "Week 7: hexagonal, radial and curve arrays — sheet 2 of P3b. Bring sheet 1's "
             "graph working; we build on it."),
    ("DUE", "Nothing is due next week; it is a studio-review week. P3b, both sheets together, is "
            + C.due_line("P3b") + "."),
    ("BUILD", "Finish sheet 1: linear, nested grid and XYZ cube, with count, spacing, index "
              "order and predicted totals labelled."),
    ("PRINT", "P2b: fix anything flagged at today's checkpoint, then queue it. It is due at the "
              "midterm, " + C.date_long(10) + "."),
])

d.save(os.path.join(OUT, "ARC3133_Class06.pptx"))
print("class06 ok — %d slides" % len(d.prs.slides._sldIdLst))
