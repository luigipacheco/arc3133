# -*- coding: utf-8 -*-
"""Class 06 — Attractors (U05). P2b issued."""
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

# 1 ── TITLE
title_slide(d, WK, ["ATTRACTORS"],
            "P2 CONTINUES — THE RULE STOPS COMING FROM THE INDEX", bg=CYAN, lfill=PINK, rfill=LIME)

# 2 ── AN ATTRACTOR IS A NUMBER
s = d.slide(BLACK)
s.header("AN ATTRACTOR IS A NUMBER",
         "For every point: how far is it from something? Use that number to drive a property.")
s.panel(L, 2.05, 6.2, 3.3, "THE WHOLE IDEA", headfill=LIME)
s.t(L + 0.4, 2.85, 5.4, 2.2, [
    s.Mb("for each point p:", 15),
    s.Mb("    d = distance(p, attractor)", 15),
    s.Mb("    size = f(d)", 15),
    s.Mb(" ", 8),
    s.Mb("That is it. Everything else", 13.5),
    s.Mb("is a choice of f.", 13.5)], ls=1.35)
s.panel(7.15, 2.05, 5.5, 3.3, "TWO NUMBERS, SAME JOB", headfill=CYAN)
s.t(7.45, 2.85, 4.9, 2.2, [
    s.Cb("INDEX told you where in the sequence.", 14),
    s.Cb(" ", 6),
    s.Cb("DISTANCE tells you how far from something outside the collection.", 14),
    s.Cb(" ", 6),
    s.Cb("Both are numbers driving a property. That is the only idea this week.", 14)], ls=1.3)
s.banner(5.7, "LAST WEEK YOU BUILT THE POSITIONS. THIS WEEK YOU MEASURE THEM.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 3 ── READ THE FIELD FIRST
s = d.slide(BLACK)
s.header("READ THE FIELD BEFORE YOU CHANGE ANYTHING",
         "Distance is a value at every point. Look at it as grey before it becomes geometry.")
seq = [("01", "MEASURE", "Every point gets a number: how far to the attractor.", CYAN),
       ("02", "DISPLAY", "Show those numbers as grey. This is a drawing already.", LIME),
       ("03", "REMAP", "Push that range into the range your property needs.", YELLOW),
       ("04", "DRIVE", "Only now does the component change. The field was finished first.", PINK)]
x = L
for n, ttl, body, col in seq:
    s.chip(x, 2.0, 2.85, 0.5, n + "   " + ttl, fill=col, size=12)
    s.card(x, 2.6, 2.85, 1.5, fill=CREAM)
    s.t(x + 0.25, 2.6, 2.35, 1.5, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05
s.t(L, 4.45, W, 0.3, [s.A("THE FIELD, READ AS A GREY VALUE ACROSS THE PLANE", 11, MUTE)])
G.gray_ramp(s, L, 4.78, W, 0.5)
s.banner(5.62, "IF THE GREY IMAGE IS NOT ALREADY A GOOD DRAWING, THE COMPONENT WILL NOT SAVE IT.",
         fill=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 6.55, W, 0.4, [s.C("P2b requires the measured field shown before the geometric result. "
                          "That order is the assignment.", 13.5, MUTE)])

# 4 ── THREE KINDS
s = d.slide(CREAM)
s.header("THREE KINDS", "Same arithmetic. What changes is what you measure the distance to.")
kinds = [("SINGLE POINT", CYAN, "distance(p, a)"),
         ("MULTIPLE POINTS", PINK, "nearest of several"),
         ("CURVE", LIME, "nearest location on a curve")]
x = L
for nm, col, fm in kinds:
    s.panel(x, 1.95, 3.85, 3.45, nm, headfill=col, tsize=15)
    s.t(x + 0.25, 4.75, 3.35, 0.5, [s.Mb(fm, 11.5)], anchor=MSO_ANCHOR.MIDDLE)
    x += 4.08
G.field_point(s, L + 0.55, 2.75, L + 1.92, 3.5)
G.field_multi(s, L + 4.63, 2.75, [(L + 5.18, 3.05), (L + 6.83, 3.95)])
G.field_curve(s, L + 8.71, 2.75, L + 8.71, 2.9, lambda t: 3.55 - 0.62 * math.sin(t * math.pi))
s.banner(5.75, "Whatever you measure to, the output is the same thing: one number per point. "
              "The attractor is not an object — it is a question you ask of every point.",
         fill=CYAN, h=0.72)

# 5 ── REMAP AND CLAMP
s = d.slide(CREAM)
s.header("REMAP, AND SAY WHERE YOU CLAMPED",
         "Distance comes out in model units. Your property needs a specific range.")
s.panel(L, 1.95, 6.0, 3.4, "THE OPERATION", headfill=CYAN)
s.t(L + 0.35, 2.7, 5.3, 2.3, [
    s.Mb("t   = (d − dmin) / (dmax − dmin)", 13),
    s.Mb("out = outmin + t × (outmax − outmin)", 13),
    s.Mb(" ", 8),
    s.Mb("d    0 … 8.4 units      ← source", 13),
    s.Mb("out  0.1 … 1.0 radius   ← target", 13)], ls=1.4)
s.panel(7.0, 1.95, 5.65, 3.4, "SUBTRACT. DIVIDE. MULTIPLY. ADD.", headfill=LIME, tsize=14)
s.t(7.3, 2.7, 5.05, 2.3, [
    s.Cb("Nothing here is new — it is the arithmetic from Week 2 applied to a distance instead "
         "of a coordinate.", 14),
    s.Cb(" ", 7),
    s.Cb("Clamping is a decision, not a safety net. Decide what happens past the end of your "
         "range and say so.", 14)], ls=1.3)
s.banner(5.65, "P2b REQUIRES SOURCE AND TARGET RANGES, CLAMPING AND FALLOFF STATED ON THE SHEET.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

# 6 ── FALLOFF
s = d.slide(CREAM)
s.header("FALLOFF IS THE FUNCTION",
         "f is your decision. It is where the graphic quality actually comes from.")
fall = [("LINEAR", CYAN, "v = d", "Even change all the way across.", lambda t: 1 - t),
        ("INVERSE", PINK, "v = 1 / d", "Sharp near the attractor, flat far off.", lambda t: 1 / (1 + 6 * t)),
        ("SMOOTH", LIME, "eased", "Soft at both ends. Usually the best-looking.",
         lambda t: 1 - (3 * t * t - 2 * t ** 3)),
        ("THRESHOLD", YELLOW, "on / off at a cut", "No gradient at all. Two populations.",
         lambda t: 1.0 if t < 0.45 else 0.0)]
x = L
for nm, col, eq, cap, fn in fall:
    s.panel(x, 1.95, 2.85, 3.5, nm, headfill=col, tsize=14.5)
    s.t(x + 0.22, 2.68, 2.4, 0.3, [s.Mb(eq, 11.5)])
    G.falloff(s, x + 0.32, 3.9, fn)
    s.rule(x + 0.28, 4.02, 2.3, lw=Pt(1.0), color=MUTE)
    s.t(x + 0.25, 4.15, 2.35, 0.3, [s.Cb("distance →", 10, GREY)])
    s.t(x + 0.25, 4.55, 2.35, 0.8, [s.Cb(cap, 12.5)], ls=1.25)
    x += 3.05
s.banner(5.75, "Two students with the same attractor and different falloff produce completely "
              "different images. This is a design decision, not a setting.", fill=PINK, h=0.72)

pseudocode_slide(d, "U05",
                 sub="Measure, remap, clamp, shape the falloff, then place. In that order.",
                 note="LINE 2 IS THE ONLY LINE THAT CHANGES BETWEEN THE THREE ATTRACTOR TYPES.")

# 7 ── ISSUED — P2b
issued_slide(d, "P2b",
             blurb="Hold the component and the arrangement constant, and change only what you measure "
                   "against. The comparison is the assignment: three attractor types, one field logic, "
                   "and an architectural intention you can defend.",
             cards=[("COMPARE", "THREE TYPES", "Single point, multiple points, and a curve — same array."),
                    ("SHOW", "FIELD FIRST", "The measured field, then the geometric result."),
                    ("ARGUE", "ONE INTENTION", "A spatial or architectural reason, demonstrated live.")])

# 8 ── REQUIREMENTS
requirements_slide(d, "P2b",
                   sub="Visual quality 35% · computational understanding 25% · technical execution 20% "
                       "· experimentation 10% · requirements and identity 10%.")

# 9 ── NOW
now_slide(d, "NOW — YOUR FIRST FIELD",
          "Rest of the session: measure, look, remap, and only then attach geometry.",
          ["Distance to one point measured across your existing array",
           "The field displayed as grey, on its own, before anything changes shape",
           "Source and target ranges written down — actual numbers, not guesses",
           "One property driven: size, height or rotation. Just one, for now",
           "The attractor moved, and you can explain the response without looking at the graph"],
          closer="MOVE THE ATTRACTOR. IF YOU CANNOT PREDICT WHAT HAPPENS, STOP AND READ THE FIELD.",
          bg=LIME)

# 10 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("WATCH", "U06 — Tessellation and lattices. The same measurement-and-remap logic, applied to a "
              "connected system instead of loose components."),
    ("BUILD", "P2b is due Week 9. Get all three attractor types running on the same array — the "
              "comparison is what is being graded."),
    ("BRING", "To the midterm: the grayscale field and a first geometric response, as work in progress."),
    ("FINISH", "P2a and P1c are both due at the midterm, along with the GSM. Do not leave the print "
               "to the last week — the queue is shared."),
])

d.save(os.path.join(OUT, "ARC3133_Class06.pptx"))
print("class06 ok — %d slides" % len(d.prs.slides._sldIdLst))
