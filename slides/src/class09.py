# -*- coding: utf-8 -*-
"""Class 09 — Attractors continued (U05): site analysis with Mixtli, P3c and P3d
checkpoints, midterm checklist. Nothing issued."""
import os
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 9

VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")

DUE_MID = sorted((m["id"] for m in C.milestones_due(10)), key=lambda i: (i == "MID", i))

# 1 ── TITLE
title_slide(d, WK, ["SITE ANALYSIS", "WITH MIXTLI"],
            "P3c + P3d CHECKPOINT — FIELD TO SITE, SITE TO DECISION",
            bg=YELLOW, lfill=PINK, rfill=CYAN,
            foot="MIDTERM NEXT CLASS — %s" % C.date_long(10).upper())

# 2 ── A SITE ANALYSIS IS A FIELD
s = d.slide(BLACK)
s.header("A SITE ANALYSIS IS A FIELD",
         "Last class you built a field from distance. A site analysis reads the same way.")
X1, X2, CW = L + 1.95, 7.75, 4.9
s.chip(X1, 1.95, CW, 0.45, "ATTRACTOR FIELD — P3c", fill=CYAN, size=12)
s.chip(X2, 1.95, CW, 0.45, "SITE FIELD — P3d", fill=LIME, size=12)
rows = [("MEASURE", YELLOW, "Distance to the attractor, at every point of the grid.",
         "A site value at every point, computed by Mixtli."),
        ("REMAP", PINK, "Distance range pushed into grey or a line property.",
         "The value range pushed into colour."),
        ("LEGEND", CYAN, "Near → far, with input and output ranges.",
         "What the colour means, with units."),
        ("USE", LIME, "The value drives a line the pen draws.",
         "The reading informs one spatial decision.")]
y = 2.6
for lab, col, a, b in rows:
    s.chip(L, y, 1.7, 0.7, lab, fill=col, size=12.5)
    for xx, body in ((X1, a), (X2, b)):
        s.card(xx, y, CW, 0.7, fill=CREAM)
        s.t(xx + 0.25, y, CW - 0.5, 0.7, [s.Cb(body, 13)], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.85
s.banner(6.1, "MEASURE → REMAP → LEGEND. THE SAME THREE STEPS. THE SITE VERSION ENDS IN A DECISION.",
         fill=YELLOW, h=0.62, align=PP_ALIGN.CENTER)

# 3 ── MIXTLI: THE SITE
s = d.slide(BLACK)
s.header("MIXTLI — RECORD THE SITE FIRST",
         "Mixtli is a Blender add-on provided by the instructor. Before any analysis, record the site.")
rec = [("SOURCE", "Where the site model or data came from. Name it on the sheet.", CYAN),
       ("UNITS", "What one unit is. Check it against one known dimension.", LIME),
       ("SCALE", "The scale of the site plan or base view, with a bar.", YELLOW),
       ("ORIENTATION", "North, and how the model is placed relative to it.", PINK)]
x = L
for ttl, body, col in rec:
    s.chip(x, 2.0, 2.85, 0.5, ttl, fill=col, size=12)
    s.card(x, 2.6, 2.85, 1.55, fill=CREAM)
    s.t(x + 0.25, 2.6, 2.35, 1.55, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05
s.panel(L, 4.5, W, 1.35, "AND ONE SENTENCE: WHY THIS SITE", headfill=LIME, tsize=13.5)
s.t(L + 0.3, 5.1, W - 0.6, 0.7, [s.Cb("A site you can document, and a reason you chose it. The reason "
                                       "becomes your analysis question.", 13.5)],
    ls=1.25, anchor=MSO_ANCHOR.MIDDLE)
s.banner(6.2, "P3d CHECKPOINT TODAY: YOUR SITE, ONE ANALYSIS WITH A LEGEND, AND A QUESTION.",
         fill=YELLOW, h=0.62, align=PP_ALIGN.CENTER)

# 4 ── MIXTLI: ANALYSIS TO DECISION
s = d.slide(CREAM)
s.header("ONE ANALYSIS, ONE DECISION",
         "The add-on does the computation. The question, the comparison and the reading are yours.")
flow = [("01", "ANALYZE", CYAN, "One analysis. Record its type, inputs and settings. Legend and units on "
                               "the image."),
        ("02", "COMPARE", LIME, "Change one thing — a setting, a time or a condition — and show both."),
        ("03", "INTERPRET", YELLOW, "Say what the output measures. Read it as a field: a value at every "
                                   "point, remapped to colour."),
        ("04", "DECIDE", PINK, "Name one spatial decision the reading supports, and draw it on the plan.")]
x = L
for n, ttl, col, body in flow:
    s.panel(x, 1.95, 2.85, 3.3, n + "   " + ttl, headfill=col, tsize=13.5)
    s.t(x + 0.22, 2.7, 2.4, 2.4, [s.Cb(body, 13.5)], ls=1.3)
    x += 3.05
s.banner(5.55, "SAME LOGIC AS P3c: A MEASURED VALUE, A STATED RANGE, A LEGEND, THEN A CONSEQUENCE.",
         fill=CYAN, h=0.7, align=PP_ALIGN.CENTER)
s.t(L, 6.5, W, 0.4, [s.C("A colourful image with no legend and no decision is not an analysis.",
                         13.5, GREY)])

# 5 ── P3d SHEET LAYOUT
s = d.slide(CREAM)
s.header("THE P3d SHEET — ONE 17 × 11",
         "Four zones on one landscape sheet. Every zone answers to the same question.")
SX, SY, SW, SH = L, 1.95, 7.0, 7.0 * 11 / 17
s.card(SX, SY, SW, SH, fill="FFFFFF")
zones = [(SX + 0.15, SY + 0.15, 3.65, 3.1, "01", "ANNOTATED SITE PLAN\nOR BASE VIEW", CYAN),
         (SX + 3.95, SY + 0.15, 2.9, 1.5, "02", "MAPPED ANALYSIS", LIME),
         (SX + 3.95, SY + 1.8, 2.9, 1.45, "03", "ONE COMPARISON", YELLOW),
         (SX + 0.15, SY + 3.4, 6.7, SH - 3.55, "04", "INTERPRETATION  →  ONE DECISION", PINK)]
for zx, zy, zw, zh, n, lab, col in zones:
    s.rect(zx, zy, zw, zh, fill=PAPER, line=BLACK, lw=Pt(1.5))
    s.chip(zx + 0.12, zy + 0.12, 0.55, 0.34, n, fill=col, size=10.5, shadow=False)
    s.t(zx + 0.8, zy + 0.08, zw - 0.9, 0.7, [s.Ab(ln, 11) for ln in lab.split("\n")], ls=1.1)
# plan zone: north arrow, scale bar, source line
s.t(SX + 0.35, SY + 2.35, 3.3, 0.3, [s.A("N ↑     SCALE BAR     SOURCE · UNITS", 9.5, GREY)])
s.rect(SX + 0.35, SY + 2.72, 1.6, 0.1, fill=BLACK, line=None)
s.rect(SX + 1.15, SY + 2.72, 0.8, 0.1, fill="FFFFFF", line=BLACK, lw=Pt(1.0))
# analysis zone: legend with units
s.t(SX + 4.1, SY + 1.0, 2.6, 0.25, [s.A("LEGEND + UNITS", 9, GREY)])
G.gray_ramp(s, SX + 4.1, SY + 1.28, 2.6, 0.2)
# comparison zone: two frames side by side
s.rect(SX + 4.1, SY + 2.45, 1.25, 0.65, fill="FFFFFF", line=BLACK, lw=Pt(1.0))
s.rect(SX + 5.45, SY + 2.45, 1.25, 0.65, fill="FFFFFF", line=BLACK, lw=Pt(1.0))
s.t(SX + 4.1, SY + 2.6, 1.25, 0.3, [s.A("A", 11, GREY)], align=PP_ALIGN.CENTER)
s.t(SX + 5.45, SY + 2.6, 1.25, 0.3, [s.A("B", 11, GREY)], align=PP_ALIGN.CENTER)
s.panel(7.95, 1.95, 4.7, 3.7, " ", headfill=BLACK, tsize=13.5)
s.t(7.95 + 0.25, 1.95, 4.2, 0.55, [s.Ab("EACH ZONE MUST SAY", 13.5, CREAM)],
    anchor=MSO_ANCHOR.MIDDLE)
s.t(8.2, 2.7, 4.2, 2.85, [
    s.Cb("01  Where: the site, annotated. Source, units, scale, north.", 13.5),
    s.Cb(" ", 8),
    s.Cb("02  What: the analysis, mapped, with a legend and units.", 13.5),
    s.Cb(" ", 8),
    s.Cb("03  Against what: one change of setting, time or condition.", 13.5),
    s.Cb(" ", 8),
    s.Cb("04  So what: what the output measures, and the one decision it informs.", 13.5)],
    ls=1.2)
s.banner(5.85, "ONE SHEET. ONE QUESTION. ONE DECISION.", x=7.95, w=4.7,
         fill=PINK, h=0.63, size=12.5, align=PP_ALIGN.CENTER)

# 6 ── P3c CHECKPOINT
s = d.slide(BLACK)
s.header("P3c CHECKPOINT — READ THE TEST PLOT",
         "Bring the grayscale field, the line translation and a small test plot. Read the paper, not the screen.")
chk = [("PEN", CYAN, "Does it draw clean from first stroke to last? No skips, no blots.",
        "Wrong? Change the pen or the speed."),
       ("PAPER", LIME, "Right size and weight, fixed flat. Does the ink bleed or wet through?",
        "Wrong? Change the paper."),
       ("LINE DENSITY", YELLOW, "Darkest area still separate lines? Lightest area still visible?",
        "Wrong? Change the mapping."),
       ("SIZE", PINK, "Crop plotted at 100%. Final set to 17 × 11 or the confirmed plotter size.",
        "Wrong? Fix the SVG export.")]
x = L
for nm, col, q, fix in chk:
    s.panel(x, 1.95, 2.85, 3.55, nm, headfill=col, tsize=13.5)
    s.t(x + 0.22, 2.7, 2.4, 1.7, [s.Cb(q, 13)], ls=1.3)
    s.rule(x + 0.22, 4.5, 2.4, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.22, 4.62, 2.4, 0.75, [s.Cb(fix, 12.5, bold=True)], ls=1.2)
    x += 3.05
s.banner(5.85, "ONE CHANGE AT A TIME. REPLOT THE SAME CROP. KEEP BOTH TESTS FOR THE SHEET.",
         fill=YELLOW, h=0.68, align=PP_ALIGN.CENTER)

# 7 ── REQUIREMENTS — P3d (reminder)
requirements_slide(d, "P3d", title="REMINDER — P3d REQUIREMENTS", sub=VISUAL)

# 8 ── MIDTERM CHECKLIST
requirements_slide(d, "MID", title="MIDTERM CHECKLIST — PROJECTS 1–3",
                   sub="Next class. Due then: %s. Tick every line before you print."
                       % " · ".join(DUE_MID))

# 9 ── NOW
now_slide(d, "NOW — CHECKPOINTS",
          "Rest of the class: one table at a time, then work on what the review found.",
          ["P3c: test plot read for pen, paper, line density and size",
           "P3c: mapping fixed, final plot at full size booked",
           "P3d: site recorded — source, units, scale, orientation — and one question",
           "P3d: one Mixtli analysis with legend and units, one comparison, one decision",
           "Midterm: every item on the checklist located, printed or booked for printing"],
          closer="FIX THE MAPPING TODAY. NEXT WEEK THERE IS NO TIME TO REPLOT.",
          bg=CYAN, closer_color=YELLOW)

# 10 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("MIDTERM", "Next class, %s, is the midterm review of Projects 1–3. Due then: %s."
                % (C.date_long(10).title(), ", ".join(DUE_MID[:-1]) + " and " + DUE_MID[-1])),
    ("PLOT", "Plot the final P3c drawing at full size. Keep the SVG, a photograph or scan of the plot "
             "and the editable graph."),
    ("SHEET", "Finish the P3d sheet: annotated site, mapped analysis with legend and units, one "
              "comparison, one decision."),
    ("BRING", "Printed sheets, the plotted drawing, the 3D print, and editable files with "
              "dependencies. Be ready to change a parameter live."),
])

d.save(os.path.join(OUT, "ARC3133_Class09.pptx"))
print("class09 ok — %d slides" % len(d.prs.slides._sldIdLst))
