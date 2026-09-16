# -*- coding: utf-8 -*-
"""Class 08 — Attractors (U05): 2D field and pen plotter. P3b due. P3c and P3d issued."""
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
WK = 8

VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")
FABRICATION = ("Visual documentation 20% · computational understanding 20% · technical execution 15% "
               "· fabrication quality 30% · experimentation 5% · requirements and identity 10%.")


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


# 1 ── TITLE
title_slide(d, WK, ["ATTRACTORS", "2D FIELD + PLOTTER"],
            "P3 CONTINUES — A FIELD FIRST, THEN LINES A PEN CAN DRAW", bg=CYAN, lfill=PINK, rfill=LIME)

# 2 ── AN ATTRACTOR IS A NUMBER
s = d.slide(BLACK)
s.header("AN ATTRACTOR IS A NUMBER",
         "For every point: how far is it from something? Use that number to drive a property.")
s.panel(L, 2.05, 6.2, 3.3, "THE WHOLE IDEA", headfill=LIME)
s.t(L + 0.4, 2.85, 5.4, 2.2, [
    s.Mb("for each point p:", 15),
    s.Mb("    d = distance(p, a)", 15),
    s.Mb("    value = f(d)", 15),
    s.Mb(" ", 8),
    s.Mb("Everything else this week", 13.5),
    s.Mb("is a choice of f.", 13.5)], ls=1.35)
s.panel(7.15, 2.05, 5.5, 3.3, "MEASURE IT FIRST", headfill=CYAN)
s.t(7.45, 2.85, 4.9, 2.2, [
    s.Mb("d = √((px − ax)² + (py − ay)²)", 13),
    s.Cb(" ", 6),
    s.Cb("Pythagoras, once per point. The answer is in model units.", 14),
    s.Cb(" ", 6),
    s.Cb("Index told you where in the sequence. Distance tells you how far from something "
         "outside the collection.", 14)], ls=1.3)
s.banner(5.7, "LAST WEEK YOU BUILT THE POSITIONS. THIS WEEK YOU MEASURE THEM.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 3 ── READ THE FIELD FIRST
s = d.slide(BLACK)
s.header("READ THE FIELD BEFORE YOU CHANGE ANYTHING",
         "Distance is a value at every point. Look at it as grey before it becomes geometry.")
seq = [("01", "MEASURE", "Every point on a flat 2D grid gets a number: how far to the attractor.", CYAN),
       ("02", "DISPLAY", "Show those numbers as grey. This is a drawing already.", LIME),
       ("03", "REMAP", "Push that range into the range your property needs.", YELLOW),
       ("04", "DRIVE", "Only now does anything change. The field was finished first.", PINK)]
x = L
for n, ttl, body, col in seq:
    s.chip(x, 2.0, 2.85, 0.5, n + "   " + ttl, fill=col, size=12)
    s.card(x, 2.6, 2.85, 1.5, fill=CREAM)
    s.t(x + 0.25, 2.6, 2.35, 1.5, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05
s.t(L, 4.45, W, 0.3, [s.A("THE FIELD, READ AS A GREY VALUE ACROSS THE PLANE   ·   NEAR → FAR", 11, MUTE)])
G.gray_ramp(s, L, 4.78, W, 0.5)
s.banner(5.62, "IF THE GREY IMAGE IS NOT ALREADY A GOOD DRAWING, THE LINES WILL NOT SAVE IT.",
         fill=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 6.55, W, 0.4, [s.C("P3c requires the grayscale field, with a legend, beside the line drawing. "
                          "That order is the assignment.", 13.5, MUTE)])

# 4 ── REMAP AND CLAMP
s = d.slide(CREAM)
s.header("REMAP, AND SAY WHERE YOU CLAMPED",
         "Distance comes out in model units. Your property needs a specific range.")
s.panel(L, 1.95, 6.0, 3.4, "THE OPERATION", headfill=CYAN)
s.t(L + 0.35, 2.7, 5.3, 2.3, [
    s.Mb("t   = (d − dmin) / (dmax − dmin)", 13),
    s.Mb("t   = clamp(t, 0, 1)", 13),
    s.Mb("out = outmin + t × (outmax − outmin)", 13),
    s.Mb(" ", 8),
    s.Mb("d    0 … 8.4 units    ← input", 13),
    s.Mb("out  2 … 12 mm length ← output", 13)], ls=1.4)
s.panel(7.0, 1.95, 5.65, 3.4, "SUBTRACT. DIVIDE. MULTIPLY. ADD.", headfill=LIME, tsize=14)
s.t(7.3, 2.7, 5.05, 2.3, [
    s.Cb("Nothing here is new. It is the arithmetic of a transformation, applied to a distance "
         "instead of a coordinate.", 14),
    s.Cb(" ", 7),
    s.Cb("Clamping is a decision, not a safety net. Decide what happens past the end of your "
         "range and say so.", 14)], ls=1.3)
s.banner(5.65, "P3c REQUIRES INPUT AND OUTPUT RANGES, CLAMPING AND FALLOFF LABELLED ON THE SHEET.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

# 5 ── FALLOFF + THREE KINDS
s = d.slide(CREAM)
s.header("FALLOFF, AND WHAT YOU MEASURE TO",
         "f shapes the drawing. The attractor type changes only what the distance is measured to.")
fall = [("LINEAR", CYAN, "v = 1 − t", lambda t: 1 - t),
        ("INVERSE", PINK, "v = 1 / (1 + k·t)", lambda t: 1 / (1 + 6 * t)),
        ("SMOOTH", LIME, "eased at both ends", lambda t: 1 - (3 * t * t - 2 * t ** 3)),
        ("STEP", YELLOW, "on / off at a cut", lambda t: 1.0 if t < 0.45 else 0.0)]
x = L
for nm, col, eq, fn in fall:
    s.panel(x, 1.9, 2.85, 1.95, nm, headfill=col, headh=0.45, tsize=13)
    s.t(x + 0.22, 2.45, 2.4, 0.3, [s.Mb(eq, 11)])
    G.falloff(s, x + 0.32, 3.45, fn, h=0.6)
    s.rule(x + 0.28, 3.57, 2.3, lw=Pt(1.0), color=MUTE)
    x += 3.05
kinds = [("ONE POINT", CYAN, "d = distance(p, a)"),
         ("NEAREST OF SEVERAL", PINK, "d = min(distance(p, ai))"),
         ("NEAREST ON A CURVE", LIME, "d = distance(p, closest(c, p))")]
x = L
for nm, col, fm in kinds:
    s.panel(x, 4.05, 3.85, 2.2, nm, headfill=col, headh=0.45, tsize=13)
    s.t(x + 0.2, 5.72, 3.45, 0.4, [s.Mb(fm, 10.5)], anchor=MSO_ANCHOR.MIDDLE,
        align=PP_ALIGN.CENTER)
    x += 4.08
P, Q, GY = 0.3, 0.16, 4.72
G.field_point(s, L + 0.72, GY, L + 1.9, GY + 0.35, p=P, q=Q, rows=6, k=0.2, base=0.17)
G.field_multi(s, L + 4.8, GY, [(L + 5.3, GY + 0.1), (L + 6.8, GY + 0.7)],
              p=P, q=Q, rows=6, k=0.2, base=0.17)
G.field_curve(s, L + 8.88, GY, L + 8.88, 2.4, lambda t: GY + 0.72 - 0.55 * math.sin(t * math.pi),
              p=P, q=Q, rows=6, k=0.25, base=0.17)
s.banner(6.45, "SAME GRID, SAME MAPPING, THREE ATTRACTORS: P3c SHOWS WHAT THE ATTRACTOR ALONE CHANGES.",
         fill=BLACK, color=YELLOW, h=0.6, size=12, align=PP_ALIGN.CENTER)

# 6 ── LINES, NOT PIXELS
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

# 7 ── FOUR TRANSLATIONS
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

# 8 ── EXPORT, TEST PLOT, COMMON PROBLEMS
s = d.slide(CREAM)
s.header("EXPORT AT SIZE. TEST SMALL. FIX IT IN THE SVG.",
         "The SVG is the drawing the plotter receives. Check it before the pen touches paper.")
blocks = [(L, "01   EXPORT THE SVG", CYAN,
           [("CURVES", "Keep strokes as curves. No mesh, no filled shape."),
            ("SIZE", "17 × 11 in, or the confirmed plotter size, at 100%."),
            ("UNITS", "Know the file unit. Measure one known line."),
            ("PEN", "One pen weight, or one layer per declared pen."),
            ("MARGIN", "Every stroke inside the paper, with a margin.")]),
          (6.8, "02   TEST PLOT SMALL FIRST", LIME,
           [("CROP", "A small, dense corner of the real drawing."),
            ("PEN", "Check tip and ink. A dry pen skips."),
            ("PAPER", "Real paper, fixed flat, right way round."),
            ("SPEED", "Slower for dense areas. Watch the first strokes."),
            ("COMPARE", "Test beside screen. Change the mapping, not the pen.")])]
for bx, ttl, col, rws in blocks:
    s.panel(bx, 1.9, 5.85, 3.2, ttl, headfill=col, headh=0.5, tsize=13.5)
    y = 2.58
    for i, (chip, body) in enumerate(rws):
        s.chip(bx + 0.22, y, 1.3, 0.36, chip, fill=ACCENTS[i % 4], size=10, shadow=False)
        s.t(bx + 1.68, y - 0.02, 4.05, 0.4, [s.Cb(body, 12)], anchor=MSO_ANCHOR.MIDDLE)
        y += 0.49
s.t(L, 5.3, W, 0.3, [s.A("03   COMMON PROBLEMS — EACH ONE IS VISIBLE IN THE SVG BEFORE IT IS ON PAPER",
                         11, GREY)])
probs = [("DUPLICATE LINES", PINK, "Strokes on top of each other. Remove overlaps."),
         ("TOO-DENSE HATCHING", YELLOW, "Lines closer than the pen blot. Space them wider."),
         ("FILLS", CYAN, "A fill has no stroke to follow. Turn it into hatching."),
         ("TINY STROKES", LIME, "Thousands of short segments. Simplify or lower the count.")]
x = L
for nm, col, fix in probs:
    s.chip(x, 5.68, 2.85, 0.38, nm, fill=col, size=10.5)
    s.card(x, 6.12, 2.85, 0.78, fill=CREAM)
    s.t(x + 0.18, 6.12, 2.5, 0.78, [s.Cb(fix, 11.5)], ls=1.15, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05

# 9 ── ISSUED — P3c
issued_slide(d, "P3c",
             blurb="Take the field off the screen. Sample it on a flat grid, turn every value into a "
                   "line, and let a pen plotter draw it. Same grid, same mapping, three attractors: "
                   "the drawing shows what the attractor alone changes.",
             cards=[("FIELD", "GREY FIRST", "The grayscale field, with a legend, before any line."),
                    ("LINES", "ONE MAPPING", "Length, rotation, spacing or hatch density, driven by distance."),
                    ("PLOT", "SVG TO PAPER", "Export at plotted size, test small, then plot the sheet.")])

# 10 ── REQUIREMENTS — P3c
s = requirements_slide(d, "P3c", sub=FABRICATION)
# the fabrication rubric is long: keep it on one line above the first row
for sh in s.s.shapes:
    if sh.has_text_frame and sh.text_frame.text == FABRICATION:
        for r in sh.text_frame.paragraphs[0].runs:
            r.font.size = Pt(12)

# 11 ── ISSUED — P3d
issued_slide(d, "P3d", badge="ALSO ISSUED TODAY", badgefill=LIME,
             blurb="Pick a real site and analyze it with Mixtli, the Blender add-on the instructor "
                   "provides. Read its output as a field — the same distance-and-remap logic as P3c — "
                   "and use it to make one spatial decision. Mixtli is taught in detail next class.",
             cards=[("SITE", "RECORD IT", "Source, units, scale and orientation, before any analysis."),
                    ("ANALYZE", "ONE COMPARISON", "One analysis with a legend and units, and one comparison."),
                    ("DECIDE", "YOUR READING", "The add-on computes. The question and the reading are yours.")])

# 12 ── REQUIREMENTS — P3d
requirements_slide(d, "P3d", sub=VISUAL)

# 13 ── NOW
now_slide(d, "NOW — FIELD TO PAPER",
          "Rest of the class: build the field, translate it, export it, test it.",
          ["Build the 2D field: a flat grid, distance at every sample, shown as grey with a legend",
           "Write down input and output ranges, clamp and falloff — actual numbers",
           "Translate the field into lines: length, rotation, spacing or hatch density",
           "Export an SVG at plotted size and measure one known line",
           "Run a small test plot and compare it with the screen"],
          closer="MOVE THE ATTRACTOR. IF YOU CANNOT PREDICT WHAT HAPPENS, STOP AND READ THE FIELD.",
          bg=LIME)

# 14 ── BEFORE NEXT CLASS
cp_c = C.checkpoints("P3c")[0][1]
cp_d = C.checkpoints("P3d")[0][1]
due_ids = sorted((m["id"] for m in C.milestones_due(10)), key=lambda i: (i == "MID", i))
due_mid = ", ".join(due_ids[:-1]) + " and " + due_ids[-1]
before_next_slide(d, [
    ("NEXT", "%s: site analysis with Mixtli, the Blender add-on the instructor provides."
             % C.date_long(9).title()),
    ("P3c", "Checkpoint next class. %s" % cp_c),
    ("P3d", "Checkpoint next class. %s" % cp_d),
    ("MIDTERM", "%s: midterm review of Projects 1–3. Due then: %s. Do not leave prints or "
                "plots to the last week." % (C.date_long(10).title(), due_mid)),
])

d.save(os.path.join(OUT, "ARC3133_Class08.pptx"))
print("class08 ok — %d slides" % len(d.prs.slides._sldIdLst))
