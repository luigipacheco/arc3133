# -*- coding: utf-8 -*-
"""Class 04 — Arrays and lists I (U04, steps 1–3). P1a due, P2a issued."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 4

# 1 ── TITLE
title_slide(d, WK, ["ARRAYS AND LISTS", "PART ONE"],
            "P2 BEGINS — ONE COMPONENT, MANY POSITIONS", bg=LIME, lfill=PINK, rfill=CYAN)

# 2 ── AN ARRAY IS A LIST OF POSITIONS
s = d.slide(CREAM)
s.header("AN ARRAY IS A LIST OF POSITIONS",
         "Not a command that duplicates things. A list you compute, then place geometry at.")
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
         "it is — and therefore how different it should be.", 13.5)], ls=1.35)
s.banner(5.75, "Your panel is the component. It does not change today — only where it goes.",
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
    s.Cb("Then 5. Then 20.", 13.5),
    s.Cb(" ", 6),
    s.Cb("A collection you cannot inspect is a collection you cannot debug. There is no prize "
         "for a large count.", 13.5)], ls=1.3)
s.banner(5.7, "BUILD IT AT A COUNT YOU CAN COUNT. SCALE UP ONLY ONCE IT IS RIGHT.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 4 ── COMPARE + SWITCH IS AN IF
s = d.slide(CREAM)
s.header("COMPARE + SWITCH IS AN IF STATEMENT",
         "Test a value, then act on the answer. Two nodes, one idea.")
s.panel(L, 1.95, 6.0, 3.4, "THE PATTERN", headfill=PINK)
s.t(L + 0.35, 2.7, 5.3, 2.3, [
    s.Mb("Compare   index  >  4     →  True / False", 12),
    s.Mb("Switch    False → a", 12),
    s.Mb("          True  → b", 12),
    s.Mb(" ", 8),
    s.Cb("Compare asks the question. Switch chooses between two answers. Everything conditional "
         "in this course is those two nodes.", 13.5)], ls=1.3)
s.panel(7.0, 1.95, 5.65, 3.4, "WHAT IT BUYS YOU", headfill=LIME, tsize=14.5)
s.t(7.3, 2.72, 5.05, 2.4, [
    s.Cb("Move only a range of indices.", 14),
    s.Cb("Cull every third element.", 14),
    s.Cb("Give the first row a different height.", 14),
    s.Cb(" ", 7),
    s.Cb("The field stops being uniform the moment a test decides something.", 14)], ls=1.35)
s.banner(5.65, "COMPARE THE RESULT AT TWO DIFFERENT COUNTS. IF IT ONLY WORKS AT ONE, IT IS NOT A RULE.",
         fill=CYAN, h=0.72, align=PP_ALIGN.CENTER)

# 5 ── NEST IT AND YOU HAVE A GRID
s = d.slide(CREAM)
s.header("NEST IT AND YOU HAVE A GRID", "Two counters instead of one. A list of lists.")
s.panel(L, 1.95, 5.6, 3.5, "ONE COUNTER", headfill=CYAN)
G.cartesian(s, L + 0.6, 3.0, cols=8, rows=1, p=0.38, d=0.14)
s.t(L + 0.35, 3.9, 5.0, 1.2, [
    s.Mb("p[i] = start + i × step", 12),
    s.Mb(" ", 7),
    s.Cb("count = 8", 13)], ls=1.3)
s.panel(6.6, 1.95, 6.05, 3.5, "TWO COUNTERS", headfill=LIME)
G.cartesian(s, 7.0, 2.75, cols=8, rows=5, p=0.38, d=0.14)
s.t(6.9, 4.8, 5.45, 0.5, [
    s.Mb("p[i][j] = start + (i × dx, j × dy)      count = 8 × 5 = 40", 12)])
s.banner(5.75, "PREDICT THE TOTAL BEFORE YOU LOOK. IF THE NUMBER SURPRISES YOU, THE NESTING IS WRONG.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

pseudocode_slide(d, "U04",
                 sub="Everything in U04 is in these nine lines — the nested loop, the stagger, the conditional, the sine.",
                 note="THE INDENTATION IS THE NESTING. THAT IS WHY A GRID IS A LOOP INSIDE A LOOP.")

# 6 ── ISSUED — P2a
issued_slide(d, "P2a",
             blurb=C.PROJECTS["P2"]["description"] +
                   "  This milestone is the arrangement half: four ways of placing the same component, "
                   "three of them developed, with the repetition and selection logic built from basic nodes.",
             cards=[("BUILD", "FOUR ARRANGEMENTS", "Linear, nested grid, hexagonal, radial — the grid is required."),
                    ("CONTROL", "ONE CONDITIONAL", "An index range displaced, using Compare and Switch."),
                    ("VARY", "ONE SINE", "Amplitude, frequency and phase, named and demonstrated.")])

# 7 ── REQUIREMENTS
requirements_slide(d, "P2a",
                   sub="Visual quality 35% · computational understanding 25% · technical execution 20% "
                       "· experimentation 10% · requirements and identity 10%.")

# 8 ── NOW
now_slide(d, "NOW — YOUR FIRST ARRAY",
          "Rest of the session: a linear array, a conditional, and a grid you can predict.",
          ["Your panel instanced along a linear array, count and spacing exposed",
           "The spreadsheet open — list, count and index all readable at count = 5",
           "Compare and Switch changing one range of indices",
           "The array nested into a grid, and you predicted the total before looking",
           "Index order explained out loud: which way does i run, and what happens if you swap it"],
          closer="A COUNT YOU CAN COUNT. NOT A THOUSAND OF ANYTHING, YET.",
          bg=CYAN)

# 9 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("CONTINUE", "U04 — the same unit runs into next week. Hexagonal and radial arrangements, "
                 "conditional displacement and sine control."),
    ("BUILD", "P2a is due at the midterm. Start the comparisons now — the sheet is easier when "
              "the graphs already exist."),
    ("BRING", "Your grid, working, at a small count. And P1b — the panel sheet is due next class."),
    ("CHECK", "P1c: print-ready geometry, physical units and orientation get reviewed next week "
              "before anything goes in the queue."),
])

d.save(os.path.join(OUT, "ARC3133_Class04.pptx"))
print("class04 ok — %d slides" % len(d.prs.slides._sldIdLst))
