# -*- coding: utf-8 -*-
"""Class 05 — Arrays and lists II (U04, steps 4–7). P1b due."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 5

# 1 ── TITLE
title_slide(d, WK, ["ARRAYS AND LISTS", "PART TWO"],
            "STAGGER IT, SPIN IT, BEND IT", bg=PINK, lfill=CYAN, rfill=YELLOW,
            foot="U04 CONTINUES  /  P2a IN PROGRESS, DUE AT THE MIDTERM")

# 2 ── FOUR ARRANGEMENTS
s = d.slide(CREAM)
s.header("FOUR ARRANGEMENTS", "Same component, four rules for generating the list of positions.")
CY = 1.95
xs = [L, L + 3.05, L + 6.10, L + 9.15]
names = ["LINEAR", "GRID", "HEXAGONAL", "RADIAL"]
cols = [CYAN, LIME, YELLOW, PINK]
subs = ["one counter", "two counters", "stagger alternate rows", "radius, count, angular step"]
for x, nm, col, sub in zip(xs, names, cols, subs):
    s.panel(x, CY, 2.85, 3.5, nm, headfill=col, tsize=14.5)
    s.t(x + 0.22, CY + 2.85, 2.41, 0.5, [s.Mb(sub, 10.5)], anchor=MSO_ANCHOR.MIDDLE)
G.cartesian(s, xs[0] + 0.42, CY + 1.72, cols=7, rows=1, p=0.34)
G.cartesian(s, xs[1] + 0.55, CY + 0.95, cols=6, rows=5, p=0.34)
G.hexagonal(s, xs[2] + 0.45, CY + 0.95, cols=6, rows=5, p=0.34)
G.radial(s, xs[3] + 1.42, CY + 1.72, rings=(0.44, 0.80, 1.16), n=12)
s.banner(5.75, "Every one of these is the same operation — move, repeated, with the amount driven "
              "by a counter. Only the rule for the counter changes.", fill=CYAN, h=0.72)

# 3 ── HEXAGONAL
s = d.slide(BLACK)
s.header("HEXAGONAL IS A GRID WITH AN ODD/EVEN TEST",
         "Stagger alternate rows by half the spacing. Keep the row spacing consistent.")
s.panel(L, 2.05, 6.2, 3.35, "THE TEST", headfill=LIME)
s.t(L + 0.35, 2.8, 5.5, 2.3, [
    s.Mb("offset = (j mod 2 == 0) ? 0 : dx / 2", 12.5, bold=True),
    s.Mb(" ", 8),
    s.Cb("Modulo asks: is this row odd or even? Compare turns that into True or False, and "
         "Switch picks the offset. The same two nodes as last week.", 13.5),
    s.Cb(" ", 6),
    s.Cb("Row spacing is not dx. If you use the same number for both, you get a squashed grid, "
         "not a hex field.", 13.5)], ls=1.3)
s.panel(7.15, 2.05, 5.5, 3.35, "WHAT IT LOOKS LIKE", headfill=CYAN)
G.hexagonal(s, 7.75, 2.95, cols=7, rows=6, p=0.36, d=0.13)
s.banner(5.75, "A BRICK BOND IS A HEXAGONAL ARRAY. SO IS A HONEYCOMB. SO IS HALF THE PAVING YOU WALK ON.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 4 ── RADIAL
s = d.slide(CREAM)
s.header("RADIAL IS POLAR ARITHMETIC", "Radius, count, angular step. The index drives the angle.")
s.panel(L, 1.95, 6.0, 3.5, "THE RULE", headfill=PINK)
s.t(L + 0.35, 2.7, 5.3, 2.4, [
    s.Mb("step  = 360 / count", 12.5),
    s.Mb("θ[i]  = i × step", 12.5),
    s.Mb("p[i]  = c + r · (cos θ, sin θ)", 12.5, bold=True),
    s.Mb(" ", 8),
    s.Cb("The same rotation arithmetic from Week 2 — the one place where x and y have to talk "
         "to each other — now generating positions instead of moving a solid.", 13.5)], ls=1.3)
s.panel(7.0, 1.95, 5.65, 3.5, "TWO KNOBS", headfill=LIME, tsize=14.5)
G.radial(s, 9.85, 3.35, rings=(0.42, 0.78, 1.14), n=12, d=0.10)
s.t(7.3, 4.85, 5.05, 0.5, [s.Cb("Change the count and the step changes with it. "
                                "Change the radius per ring and it opens up.", 13)], ls=1.25)
s.banner(5.65, "IF YOUR LAST ELEMENT LANDS ON TOP OF YOUR FIRST, YOU DIVIDED BY THE WRONG NUMBER.",
         fill=CYAN, h=0.72, align=PP_ALIGN.CENTER)

# 5 ── CONDITIONAL DISPLACEMENT
s = d.slide(CREAM)
s.header("MOVE ONLY SOME OF THEM", "Select a range of indices with comparisons, and displace just those.")
s.panel(L, 1.95, 5.6, 3.5, "BEFORE", headfill=MUTE)
G.cartesian(s, L + 0.8, 3.0, cols=9, rows=4, p=0.42, d=0.15)
s.t(L + 0.35, 4.85, 5.0, 0.4, [s.Cb("Every element identical. The index is computed, then ignored.", 12.5)])
s.panel(6.6, 1.95, 6.05, 3.5, "AFTER", headfill=LIME)
for i in range(9):
    for j in range(4):
        lift = -0.32 if 3 <= i <= 5 else 0.0
        s.dot(7.0 + i * 0.42, 3.0 + j * 0.42 + lift, d=0.15,
              fill=PINK if 3 <= i <= 5 else BLACK)
s.t(6.9, 4.85, 5.45, 0.4, [s.Cb("Indices 3 to 5 lifted. One Compare, one Switch, one Set Position.", 12.5)])
s.banner(5.75, "THE FIELD STOPS BEING WALLPAPER THE MOMENT A TEST DECIDES SOMETHING.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

# 6 ── SINE
s = d.slide(BLACK)
s.header("SINE GIVES YOU A SMOOTH RULE",
         "Math set to Sine, driven by the index. Three words describe the whole curve.")
s.panel(L, 2.05, 6.2, 3.3, "THREE PARAMETERS", headfill=CYAN)
tri = [("AMPLITUDE", "how far it swings"),
       ("FREQUENCY", "how many swings across the set"),
       ("PHASE", "where in the swing it starts")]
y = 2.85
for nm, body in tri:
    s.chip(L + 0.35, y, 2.0, 0.55, nm, fill=LIME, size=11)
    s.t(L + 2.6, y, 3.3, 0.55, [s.Cb(body, 13)], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.72
s.t(L + 0.35, 5.0, 5.5, 0.35, [s.Mb("h[i] = amp × sin(i × freq + phase)", 12.5, bold=True)])
s.panel(7.15, 2.05, 5.5, 3.3, "READ IT AS A CURVE", headfill=YELLOW)
G.sine_row(s, 7.6, 3.3, w=4.6, amp=0.55, n=15, cycles=1.0)
s.t(7.45, 4.35, 4.9, 0.9, [s.Cb("Connect the ordered points and the list becomes a curve. "
                                "That is the same list — read as a shape instead of as positions.",
                                13)], ls=1.3)
s.banner(5.7, "NAME THE THREE VALUES ON YOUR SHEET. P2a ASKS FOR THEM EXPLICITLY.",
         fill=PINK, h=0.7, align=PP_ALIGN.CENTER)

# 7 ── THE TRAP
s = d.slide(CREAM)
s.header("TWO WAYS TO REPEAT", "Worth being precise about, because they look alike and are not.")
s.panel(L, 1.95, 6.0, 3.4, "EXPLICIT ITERATION", headfill=PINK)
s.t(L + 0.35, 2.7, 5.3, 2.4, [
    s.Cb("A Repeat Zone runs a body once per step, in order, carrying a value forward.", 14),
    s.Cb(" ", 7),
    s.Cb("Use it when step n depends on step n−1 — and when you want to watch the loop happen.", 14)], ls=1.3)
s.panel(7.0, 1.95, 5.65, 3.4, "PER-ELEMENT EVALUATION", headfill=CYAN)
s.t(7.3, 2.7, 5.05, 2.4, [
    s.Cb("The other kind is evaluated across every element at once. There is no order and no carry.", 14),
    s.Cb(" ", 7),
    s.Cb("It is faster and it is usually what you want — but nothing on screen tells you a loop "
         "happened, which is exactly why we built the explicit one first.", 14)], ls=1.3)
s.banner(5.65, "NEXT WEEK THIS GETS A NAME. FOR NOW: ONE CARRIES A VALUE FORWARD, THE OTHER DOES NOT.",
         fill=BLACK, color=CYAN, h=0.72, align=PP_ALIGN.CENTER)

pseudocode_slide(d, "U04",
                 title="THE SAME NINE LINES, A WEEK LATER",
                 sub="Last week you could read the first three lines. Today you can read all of it.",
                 note="j % 2 IS THE ODD/EVEN TEST · if IS COMPARE AND SWITCH · sin IS THE MATH NODE",
                 note_fill=CYAN)

# 8 ── NOW
now_slide(d, "NOW — FINISH THE FOUR",
          "Rest of the session: hexagonal, radial, the conditional and the sine.",
          ["Hexagonal array working, with the odd/even test visible and row spacing correct",
           "Radial array working from radius, count and angular step",
           "One index range displaced — and you can say which indices and why",
           "Sine driving height, with amplitude, frequency and phase written down",
           "Three of the four chosen for the sheet, including the nested grid"],
          closer="P2a IS THREE COMPARISONS, NOT FOUR UNRELATED PICTURES.",
          bg=LIME)

# 9 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("WATCH", "U05 — Attractors. Distance, remap, clamp and falloff. Next week the rule stops "
              "coming from the index and starts coming from a measurement."),
    ("BRING", "Your four arrangements, working. We drive them with attractors next class, so bring "
              "a file you can build on."),
    ("CHECK", "P1c — print-ready geometry, physical units, orientation and the sliced preview get "
              "reviewed today before anything is queued."),
    ("FINISH", "P1b is due today. P2a is due at the midterm; keep the comparisons moving."),
])

d.save(os.path.join(OUT, "ARC3133_Class05.pptx"))
print("class05 ok — %d slides" % len(d.prs.slides._sldIdLst))
