# -*- coding: utf-8 -*-
"""ARC3133 Class 03 — appends the arrays primer and the precedent brief to the
existing 3D-printing deck, and rewrites the closing slide.

Run once against a clean copy of ARC3133_Class03.pptx; it is idempotent in the
sense that it rebuilds from SRC each time.
"""
import math, sys
from nb import *
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

import os
_here = os.path.dirname(os.path.abspath(__file__))
# SRC must be the PRISTINE printing-only deck, never the patched output —
# re-running against the output would append the three slides a second time.
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_here, "src", "ARC3133_Class03_base.pptx")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(_here, "..", "presentations", "ARC3133_Class03.pptx")

d = Deck(SRC)
n_before = len(d.prs.slides._sldIdLst)
LAST = n_before - 1          # the existing "BEFORE NEXT CLASS" slide

# ─────────────────────────────── + ARRAYS BEGIN HERE
s = d.slide(BLACK)
s.header("ARRAYS BEGIN HERE",
         "The second half of today, and the whole of next week. Same lesson as the slicer.")
s.panel(L, 2.05, 6.2, 3.3, "A SLICER MAKES A LIST", headfill=LIME)
s.t(L + 0.35, 2.8, 5.5, 2.3, [
    s.Cb("You just watched a solid become a stack of profiles, ordered, then written out as moves.", 14),
    s.Cb(" ", 7),
    s.Cb("A list of positions, computed by a rule, executed in order. That is an array, and it is "
         "the whole of Module 1.", 14)], ls=1.3)
s.panel(7.15, 2.05, 5.5, 3.3, "INDEX  →  POSITION", headfill=CYAN)
s.t(7.5, 2.85, 4.85, 2.3, [
    s.Mb("i = 0   →   p = start", 13),
    s.Mb("i = 1   →   p = start + step", 13),
    s.Mb("i = 2   →   p = start + 2 × step", 13),
    s.Mb(" ", 8),
    s.Mb("p[i] = start + i × step", 13, bold=True)], ls=1.35)
s.banner(5.7, "AN ARRAY IS NOT A COMMAND THAT DUPLICATES THINGS. IT IS A LIST YOU COMPUTE, "
              "THEN PLACE GEOMETRY AT.", fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# ─────────────────────────────── + FOUR WAYS TO GENERATE THE LIST
s = d.slide(CREAM)
s.header("FOUR WAYS TO GENERATE THE LIST",
         "Named today so you can recognize them in a building. Built next week.")
CW, CY = 2.85, 1.95
xs = [L, L + 3.05, L + 6.10, L + 9.15]
names = ["CARTESIAN", "RADIAL", "HEXAGONAL", "ON CURVE"]
cols = [CYAN, PINK, LIME, YELLOW]
formulas = ["two counters, i and j", "angle and radius", "odd rows offset by dx/2",
            "sampled at t = i/n"]
for x, nm, col, fm in zip(xs, names, cols, formulas):
    s.panel(x, CY, CW, 3.2, nm, headfill=col, tsize=14.5)
    s.t(x + 0.22, CY + 2.6, CW - 0.44, 0.4, [s.Mb(fm, 10.5)], anchor=MSO_ANCHOR.MIDDLE)
# cartesian
gx, gy = xs[0] + 0.62, CY + 0.95
for i in range(6):
    for j in range(4):
        s.dot(gx + i * 0.32, gy + j * 0.32)
# radial
cx, cy = xs[1] + 1.42, CY + 1.62
for rr in (0.38, 0.68, 0.98):
    for k in range(96):
        a = 2 * math.pi * k / 96.0
        s.dot(cx + rr * math.cos(a), cy + rr * math.sin(a), d=0.022, fill=MUTE)
for rr in (0.38, 0.68, 0.98):
    for k in range(12):
        a = 2 * math.pi * k / 12.0 - math.pi / 2
        s.dot(cx + rr * math.cos(a), cy + rr * math.sin(a), d=0.10)
s.dot(cx, cy, d=0.15, fill=PINK)
# hexagonal
hx, hy = xs[2] + 0.52, CY + 0.95
for j in range(4):
    off = 0.16 if j % 2 else 0.0
    for i in range(6 if j % 2 == 0 else 5):
        s.dot(hx + off + i * 0.32, hy + j * 0.32)
# on curve
ax = xs[3] + 0.32
def cy_(t): return CY + 2.05 - 0.72 * math.sin(t * math.pi)
for k in range(60):
    t = k / 59.0
    s.dot(ax + t * 2.2, cy_(t), d=0.028, fill=MUTE)
for k in range(9):
    t = k / 8.0
    s.dot(ax + t * 2.2, cy_(t), d=0.115, fill=YELLOW)
s.banner(5.45, "Every one of these is the same operation — move, repeated, with the amount driven "
              "by a counter. Only the rule for the counter changes.", fill=CYAN, h=0.72)

# ─────────────────────────────── + FIND A MODULAR FAÇADE
s = d.slide(CREAM)
s.header("FIND A TILED FAÇADE",
         "Due next class, before anything is modeled. Look at what the building is made of, not at the building.")
cards = [("WHAT COUNTS", CYAN,
          "A façade made of one repeated part — a panel, a brick, a shingle, a cast block, "
          "a perforated plate. Look at it the way you look at a brick wall and see the brick."),
         ("WHAT DOESN'T", PINK,
          "A curtain wall of plain glass. A one-off sculptural surface. Anything where you cannot "
          "point at the part and say: this, again and again."),
         ("BRING", YELLOW,
          "A flat-on elevation photograph or drawing. The repeated part outlined on it. Its width, "
          "height and depth in millimetres."),
         ("BE READY TO SAY", LIME,
          "What the part is. What rule places the copies — stacked, offset, rotated, coursed.")]
x = L
for nm, col, body in cards:
    s.panel(x, 1.95, 2.85, 2.75, nm, headfill=col, tsize=14.5)
    s.t(x + 0.25, 2.72, 2.35, 1.85, [s.Cb(body, 12.5)], ls=1.3)
    x += 3.05
s.banner(5.05, "YOU ARE NOT TRACING IT. NEXT WEEK YOU DESIGN YOUR OWN TILE, DRIVEN BY THIS BUILDING.",
         fill=BLACK, color=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 5.95, W, 0.4, [s.C("A short approved list goes out tonight. Propose your own for approval "
                         "if it is not on it.", 13.5, GREY)])

# ─────────────────────────────── rewrite the closing slide
old = d.prs.slides[LAST]
for sh in list(old.shapes):
    sh._element.getparent().remove(sh._element)
s = S(old, CREAM)
s.header("BEFORE NEXT CLASS")
s.actionrow(1.95, "WATCH", "Tutorial 1.1 — points, lists, loops and conditionals. Cartesian, radial, "
                           "hexagonal, along a curve. Sent tonight.", fill=CYAN)
s.actionrow(3.11, "BRING", "Your tiled façade precedent — flat-on image, the repeated part outlined, "
                           "dimensions. We design your tile from it next class.", fill=LIME)
s.actionrow(4.27, "FINISH", "0.1 is due next class: the axonometric sequence, the written procedure, "
                            "the precedent analysis.", fill=PINK)
s.actionrow(5.43, "CHECK", "Your print is in the queue. It is presented at the Midterm, not next "
                           "week — but the file has to exist.", fill=YELLOW)

# put the three new slides before the closing slide
n = len(d.prs.slides._sldIdLst)
for i in range(3):
    d.move(n - 1 - i, LAST)

d.save(OUT)
print("class03 ok —", n, "slides")
