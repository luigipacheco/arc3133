# -*- coding: utf-8 -*-
"""Class 09 — Attractors continued (U05): plotter workflow, Mixtli working review,
midterm checklist. P3c and P3d checkpoints. Nothing issued."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.util import Pt, Inches

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 9


def stroke(s, x1, y1, x2, y2, lw=Pt(1.5), col=BLACK):
    """One straight pen stroke — the only mark a plotter makes."""
    ln = s.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                  Inches(x2), Inches(y2))
    ln.line.color.rgb = rgb(col)
    ln.line.width = lw
    return ln


def field(u, v, ax=0.25, ay=0.35):
    """0 near the attractor, 1 far away (u, v in 0..1)."""
    return min(1.0, math.hypot(u - ax, (v - ay) * 0.7) / 0.85)


def hatch_cell(s, x, y, w, h, n, lw=Pt(1.0)):
    for k in range(n):
        xx = x + (k + 0.5) * w / n
        stroke(s, xx, y, xx, y + h, lw=lw)


DUE_MID = sorted(m["id"] for m in C.milestones_due(10))

# 1 ── TITLE
title_slide(d, WK, ["PLOTTER WORKFLOW", "AND SITE REVIEW"],
            "P3c + P3d CHECKPOINT — FIELD TO LINES, SITE TO DECISION",
            bg=YELLOW, lfill=PINK, rfill=CYAN,
            foot="MIDTERM NEXT CLASS — %s" % C.date_long(10).upper())

# 2 ── LINES, NOT PIXELS
s = d.slide(BLACK)
s.header("A PLOTTER DRAWS LINES, NOT PIXELS",
         "A screen can show any grey. A pen is either down or up.")
s.panel(L, 2.0, 5.85, 2.75, "ON SCREEN — A VALUE PER PIXEL", headfill=MUTE, tsize=13.5)
G.gray_ramp(s, L + 0.3, 2.85, 5.25, 0.75)
s.t(L + 0.3, 3.8, 5.25, 0.8, [s.Cb("Every sample can be any grey. Nothing needs to be drawn.", 13.5)],
    ls=1.25)
s.panel(6.8, 2.0, 5.85, 2.75, "ON PAPER — A STROKE OR NOTHING", headfill=LIME, tsize=13.5)
cw = 5.25 / 9
for i in range(9):
    s.rect(7.1 + i * cw, 2.85, cw, 0.75, fill=CREAM, line=BLACK, lw=Pt(1.0))
    hatch_cell(s, 7.1 + i * cw, 2.85, cw, 0.75, i, lw=Pt(1.0))
s.t(7.1, 3.8, 5.25, 0.8, [s.Cb("Every stroke is the same darkness. Grey comes from how many "
                               "lines, how long and how close.", 13.5)], ls=1.25)
s.banner(5.1, "SO THE FIELD MUST BECOME GEOMETRY: CURVES WITH A START AND AN END. "
              "AN IMAGE WILL NOT PLOT.", fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)
s.t(L, 6.1, W, 0.7, [s.C("The grayscale field stays on the sheet as the legend. The line drawing is "
                         "what the pen draws.", 13.5, MUTE)], ls=1.3)

# 3 ── FOUR TRANSLATIONS
s = d.slide(CREAM)
s.header("TRANSLATE THE FIELD INTO LINES",
         "Same field, same remap. Only what the output number drives changes. Pick one.")
tr = [("LINE LENGTH", CYAN, "length = out", "Long near, short far."),
      ("ROTATION", PINK, "angle = out", "Lines turn with distance."),
      ("SPACING", LIME, "gap = out", "Rows open up with distance."),
      ("HATCH DENSITY", YELLOW, "lines per cell = out", "More strokes, darker cell.")]
x = L
pw = 2.85
for k, (nm, col, eq, cap) in enumerate(tr):
    s.panel(x, 1.95, pw, 3.55, nm, headfill=col, tsize=14)
    s.t(x + 0.22, 2.62, pw - 0.44, 0.3, [s.Mb(eq, 11)])
    gx, gy, gw, gh = x + 0.35, 3.1, pw - 0.7, 1.45
    cols, rows = 6, 4
    cx, cy = gw / cols, gh / rows
    if k == 0:
        for i in range(cols):
            for j in range(rows):
                t = field(i / (cols - 1), j / (rows - 1))
                ln = cx * (0.9 - 0.7 * t)
                mx, my = gx + (i + 0.5) * cx, gy + (j + 0.5) * cy
                stroke(s, mx - ln / 2, my, mx + ln / 2, my)
    elif k == 1:
        for i in range(cols):
            for j in range(rows):
                t = field(i / (cols - 1), j / (rows - 1))
                a = t * math.pi / 2
                ln = min(cx, cy) * 0.8
                mx, my = gx + (i + 0.5) * cx, gy + (j + 0.5) * cy
                dx, dy = math.cos(a) * ln / 2, math.sin(a) * ln / 2
                stroke(s, mx - dx, my - dy, mx + dx, my + dy)
    elif k == 2:
        yy, gap = gy, 0.06
        while yy <= gy + gh:
            stroke(s, gx, yy, gx + gw, yy, lw=Pt(1.25))
            gap *= 1.35
            yy += gap
    else:
        hc = 5
        for i in range(hc):
            for j in range(3):
                t = field(i / (hc - 1), j / 2.0)
                n = int(round(7 * (1 - t)))
                hatch_cell(s, gx + i * gw / hc, gy + j * gh / 3, gw / hc, gh / 3 - 0.06, n,
                           lw=Pt(0.9))
    s.t(x + 0.22, 4.78, pw - 0.44, 0.5, [s.Cb(cap, 12.5)])
    x += 3.05
s.card(L, 5.8, W, 1.0, fill=BLACK)
s.t(L + 0.35, 5.8, W - 0.7, 1.0, [
    s.Mb("t = remap(distance(p, a))         # the field, unchanged", 12.5, CREAM),
    s.Mb("line(p, angle, length)            # the last line is the translation", 12.5, YELLOW)],
    anchor=MSO_ANCHOR.MIDDLE, ls=1.3)

# 4 ── EXPORT
s = d.slide(CREAM)
s.header("KEEP IT A CURVE. EXPORT AT SIZE.",
         "The SVG is the drawing the plotter receives. Check it before the pen touches paper.")
rows = [("CURVES", "Keep strokes as curves to the end. Do not convert them to a mesh or a filled shape."),
        ("SIZE", "Set the drawing to the plotted size — 17 × 11 inches, or the confirmed plotter size — "
                 "and export at 100%."),
        ("UNITS", "Know the unit of the file and of the export. Measure one known line in the SVG."),
        ("PEN", "One pen weight, or a declared set of pens, one layer or colour per pen."),
        ("MARGINS", "Keep every stroke inside the paper, with a margin the pen can reach.")]
y = 1.95
for i, (chip, body) in enumerate(rows):
    s.numrow(y, chip, body, chipfill=ACCENTS[i % 4], cw=1.7, h=0.62, size=14)
    y += 0.8
s.banner(6.05, "OPEN THE EXPORTED SVG ON ITS OWN AND MEASURE IT. WHAT YOU SEE THERE IS WHAT WILL PLOT.",
         fill=PINK, h=0.7, align=PP_ALIGN.CENTER)

# 5 ── TEST PLOT
s = d.slide(BLACK)
s.header("TEST PLOT SMALL FIRST",
         "A small crop of the real drawing, on the real paper, with the real pen.")
steps = [("01", "CROP", "Take a small, dense corner of the drawing. Same line weight, same spacing.", CYAN),
         ("02", "PEN", "Check the tip and the ink. A dry or worn pen skips.", LIME),
         ("03", "PAPER", "Fixed flat, the right size, the right way round.", YELLOW),
         ("04", "SPEED", "Slower for dense areas. Watch the first strokes.", PINK)]
x = L
for n, ttl, body, col in steps:
    s.chip(x, 2.0, 2.85, 0.5, n + "   " + ttl, fill=col, size=12)
    s.card(x, 2.6, 2.85, 1.55, fill=CREAM)
    s.t(x + 0.25, 2.6, 2.35, 1.55, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05
s.panel(L, 4.5, W, 1.35, "THEN COMPARE THE TEST WITH THE SCREEN", headfill=CYAN, tsize=13.5)
s.t(L + 0.3, 5.1, W - 0.6, 0.7, [s.Cb("Does the darkest area still read as separate lines? Does the "
                                       "lightest area still read at all? Change the mapping, not the pen.", 13.5)],
    ls=1.25, anchor=MSO_ANCHOR.MIDDLE)
s.banner(6.2, "P3c CHECKPOINT TODAY: A SMALL TEST PLOT, IN YOUR HAND.",
         fill=YELLOW, h=0.62, align=PP_ALIGN.CENTER)

# 6 ── COMMON PROBLEMS
s = d.slide(CREAM)
s.header("COMMON PROBLEMS", "Each one is visible in the SVG before it is visible on paper.")
probs = [("DUPLICATE LINES", PINK, "Two strokes on top of each other. The pen draws both: darker ink, "
                                   "longer plot, weaker paper.", "Remove overlaps before export."),
         ("TOO-DENSE HATCHING", YELLOW, "Lines closer than the pen is wide merge into a blot and can "
                                        "wet through the paper.", "Keep spacing above the pen width."),
         ("FILLS", CYAN, "A filled shape has no stroke to follow. It will not plot, or it plots only "
                         "its outline.", "Turn fills into hatching."),
         ("TOO MANY TINY STROKES", LIME, "Thousands of very short segments make a slow plot with "
                                        "little to see.", "Simplify, or lower the count.")]
x = L
for nm, col, body, fix in probs:
    s.panel(x, 1.95, 2.85, 3.75, nm, headfill=col, tsize=12.5)
    s.t(x + 0.22, 2.7, 2.4, 1.9, [s.Cb(body, 13)], ls=1.3)
    s.rule(x + 0.22, 4.75, 2.4, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.22, 4.9, 2.4, 0.7, [s.Cb(fix, 13, bold=True)], ls=1.2)
    x += 3.05
s.banner(6.05, "IF IT LOOKS WRONG AT 100% ON SCREEN, IT WILL LOOK WORSE ON PAPER.",
         fill=BLACK, color=YELLOW, h=0.68, align=PP_ALIGN.CENTER)

# 7 ── MIXTLI: THE SITE
s = d.slide(BLACK)
s.header("MIXTLI WORKING REVIEW — THE SITE",
         "Mixtli is the Blender add-on provided for site analysis. Before any analysis, record the site.")
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

# 8 ── MIXTLI: ANALYSIS TO DECISION
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

# 9 ── MIDTERM CHECKLIST
s = requirements_slide(d, "MID", title="MIDTERM CHECKLIST — PROJECTS 1–3",
                       sub="Next class. Due then: %s. Tick every line before you print."
                           % " · ".join(DUE_MID))

# 10 ── NOW
now_slide(d, "NOW — CHECKPOINTS",
          "Rest of the class: one table at a time, then work on what the review found.",
          ["P3c: grayscale field with a legend, beside the line translation",
           "P3c: an SVG at plotted size, and a small test plot",
           "P3d: site recorded — source, units, scale, orientation",
           "P3d: one Mixtli analysis with a legend and units, and a stated question",
           "Midterm: every item on the checklist located, printed or booked for printing"],
          closer="FIX THE MAPPING TODAY. NEXT WEEK THERE IS NO TIME TO REPLOT.",
          bg=CYAN, closer_color=YELLOW)

# 11 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("MIDTERM", "%s is the midterm review of Projects 1–3. Due then: %s."
                % (C.date_long(10).title(), ", ".join(DUE_MID))),
    ("PLOT", "Plot the final P3c drawing at full size. Keep the SVG, a photograph or scan of the plot "
             "and the editable graph."),
    ("SHEET", "Finish the P3d sheet: annotated site, mapped analysis with legend and units, one "
              "comparison, one decision."),
    ("BRING", "Printed sheets, the plotted drawing, the 3D print, and editable files with "
              "dependencies. Be ready to change a parameter live."),
])

d.save(os.path.join(OUT, "ARC3133_Class09.pptx"))
print("class09 ok — %d slides" % len(d.prs.slides._sldIdLst))
