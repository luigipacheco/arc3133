# -*- coding: utf-8 -*-
"""Class 09 — Attractors continued (U05): layered site analysis. P3d issued; P3c checkpoint;
checklist for the Week 10 mid-semester deadline."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(9)
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 9
DL = C.COURSE["midterm_week"]          # the mid-semester deadline week

VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")

DUE_DL = sorted(m["id"] for m in C.milestones_due(DL))
DUE_DL_TXT = ", ".join(DUE_DL[:-1]) + " and " + DUE_DL[-1]
P3D_DUE = C.milestone("P3d")["due"]

# 1 ── TITLE
title_slide(d, WK, ["LAYERED", "SITE ANALYSIS"],
            "P3d BEGINS — ONE SITE, MEASURED IN LAYERS",
            bg=YELLOW, lfill=PINK, rfill=CYAN,
            foot="P3d ISSUED TODAY  /  P3c CHECKPOINT TODAY  /  MID-SEMESTER DEADLINE NEXT CLASS — %s"
                 % C.date_long(DL).upper())

# 2 ── A SITE ANALYSIS IS A FIELD
s = d.slide(BLACK)
s.header("A SITE ANALYSIS IS A FIELD",
         "Last class you built a field from distance. A site analysis reads the same way.")
X1, X2, CW = L + 1.95, 7.75, 4.9
s.chip(X1, 1.95, CW, 0.45, "ATTRACTOR FIELD — P3c", fill=CYAN, size=12)
s.chip(X2, 1.95, CW, 0.45, "SITE LAYER — P3d", fill=LIME, size=12)
rows = [("MEASURE", YELLOW, "Distance to the attractor, at every point of the grid.",
         "A value at every point of the site's point cloud."),
        ("REMAP", PINK, "Distance range pushed into grey or a line property.",
         "The value range pushed into grey or colour."),
        ("LEGEND", CYAN, "Near → far, with input and output ranges.",
         "What the value means, with its range and units."),
        ("USE", LIME, "The value drives a line in the drawing.",
         "Layers combine into one reading of the site.")]
y = 2.6
for lab, col, a, b in rows:
    s.chip(L, y, 1.7, 0.7, lab, fill=col, size=12.5)
    for xx, body in ((X1, a), (X2, b)):
        s.card(xx, y, CW, 0.7, fill=CREAM)
        s.t(xx + 0.25, y, CW - 0.5, 0.7, [s.Cb(body, 13)], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.85
s.banner(6.1, "MEASURE → REMAP → LEGEND. THE SAME THREE STEPS, REPEATED FOR EVERY LAYER.",
         fill=YELLOW, h=0.62, align=PP_ALIGN.CENTER)

# 3 ── LAYERS
s = d.slide(CREAM)
s.header("THREE KINDS OF LAYER",
         "Each layer is a field: one value per point, its own range, its own legend.")
PW, PY, PH = 3.85, 1.95, 3.65
GX0, GY0, COLS, ROWS, P, Q = 0.55, 2.8, 9, 5, 0.34, 0.27
layers = [("DISTANCE TO POINTS OR CURVES", CYAN, "Near → far from a feature you choose: a path, "
           "a tree line, an entrance.", "LEGEND · NEAR → FAR · m"),
          ("HEIGHT BANDS", LIME, "Every point sorted by its height into bands you set.",
           "LEGEND · BAND EDGES · m"),
          ("RECORDED ATTRIBUTE", PINK, "A value the scan already holds, such as colour or "
           "classification.", "LEGEND · CLASS OR VALUE")]
BAND = ["E8E8E0", "969690", "323230"]
CLASS = [CYAN, LIME, PINK]
x = L
for k, (nm, col, body, leg) in enumerate(layers):
    s.panel(x, PY, PW, PH, nm, headfill=col, headh=0.5, tsize=12.5)
    gx = x + GX0
    if k == 0:
        G.field_point(s, gx, GY0, gx + 0.9, GY0 + 0.55, cols=COLS, rows=ROWS, p=P, q=Q,
                      k=0.2, base=0.2)
    else:
        for i in range(COLS):
            for j in range(ROWS):
                px, py = gx + i * P, GY0 + j * Q
                if k == 1:
                    h = math.exp(-((i - 5.5) ** 2) / 8.0 - ((j - 1.5) ** 2) / 5.0)
                    fill = BAND[0 if h < 0.3 else (1 if h < 0.7 else 2)]
                    s.dot(px, py, d=0.17, fill=fill)
                    s.dot(px, py, d=0.05, fill=BLACK)
                else:
                    c = 0 if j <= 1 and i < 5 else (1 if i + j < 9 else 2)
                    s.dot(px, py, d=0.17, fill=CLASS[c])
    # legend
    s.t(x + 0.25, 4.2, PW - 0.5, 0.25, [s.A(leg, 9.5, GREY)])
    if k == 0:
        G.gray_ramp(s, x + 0.25, 4.47, PW - 0.5, 0.18)
    else:
        sw = (PW - 0.5) / 3
        for i in range(3):
            s.rect(x + 0.25 + i * sw, 4.47, sw, 0.18,
                   fill=(BAND if k == 1 else CLASS)[i], line=BLACK, lw=Pt(1.5))
    s.t(x + 0.25, 4.8, PW - 0.5, 0.75, [s.Cb(body, 12.5)], ls=1.2)
    x += 4.08
s.banner(5.8, "THREE LAYERS AT LEAST. EACH ONE ANSWERS A DIFFERENT QUESTION ABOUT THE SAME SITE.",
         fill=BLACK, color=YELLOW, h=0.6, size=12, align=PP_ALIGN.CENTER)
s.t(L, 6.68, W, 0.4, [s.C("Mixtli, the Blender add-on the instructor provides, does these operations. "
                         "An equivalent tool is fine.", 13, GREY)])

# 4 ── RECORD THE SITE FIRST
s = d.slide(BLACK)
s.header("RECORD THE SITE FIRST",
         "Before any layer, record the point cloud: where it came from and how it sits.")
rec = [("SOURCE", "Where the point cloud came from. Name it on the sheet.", CYAN),
       ("UNITS", "What one unit is. Check it against one known dimension.", LIME),
       ("SCALE", "The scale of each view, with a bar.", YELLOW),
       ("ORIENTATION", "North, and how the cloud is placed relative to it.", PINK)]
x = L
for ttl, body, col in rec:
    s.chip(x, 2.0, 2.85, 0.5, ttl, fill=col, size=12)
    s.card(x, 2.6, 2.85, 1.55, fill=CREAM)
    s.t(x + 0.25, 2.6, 2.35, 1.55, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05
s.panel(L, 4.5, W, 1.35, "AND ONE SENTENCE: WHY THIS SITE", headfill=LIME, tsize=13.5)
s.t(L + 0.3, 5.1, W - 0.6, 0.7, [s.Cb("A site you can document, and a reason you chose it. The reason "
                                       "tells you which layers to map.", 13.5)],
    ls=1.25, anchor=MSO_ANCHOR.MIDDLE)
cp_wk, cp_txt = C.checkpoints("P3d")[0]
s.banner(6.2, "P3d CHECKPOINT NEXT CLASS: " + cp_txt.upper(),
         fill=YELLOW, h=0.62, size=12, align=PP_ALIGN.CENTER)

# 5 ── COMBINING LAYERS
s = d.slide(CREAM)
s.header("COMBINE THE LAYERS INTO ONE READING",
         "The tool computes each layer. How they combine, and what that shows, is your decision.")
flow = [("01", "NORMALIZE", CYAN, "Remap each layer to 0–1 so the layers can be compared. Keep the "
                                  "original range and units on its legend."),
        ("02", "WEIGHT", LIME, "Decide how much each layer counts. Write the weights down."),
        ("03", "COMBINE", YELLOW, "Add, multiply, or keep the lowest or highest value. Say which, "
                                 "and why."),
        ("04", "READ", PINK, "Say what the combined view shows about the site that no single layer "
                            "shows.")]
x = L
for n, ttl, col, body in flow:
    s.panel(x, 1.95, 2.85, 2.45, n + "   " + ttl, headfill=col, tsize=13.5)
    s.t(x + 0.22, 2.7, 2.4, 1.9, [s.Cb(body, 13)], ls=1.3)
    x += 3.05
s.card(L, 4.7, W, 0.75, fill=BLACK)
s.t(L + 0.35, 4.7, W - 0.7, 0.75, [
    s.Mb("combined = w1 × distance + w2 × height + w3 × attribute      # w1 + w2 + w3 = 1", 12.5, YELLOW)],
    anchor=MSO_ANCHOR.MIDDLE)
s.banner(5.75, "SAME LOGIC AS P3c: A MEASURED VALUE, A STATED RANGE, A LEGEND. NOW THREE OF THEM.",
         fill=CYAN, h=0.62, align=PP_ALIGN.CENTER)
s.t(L, 6.55, W, 0.35, [s.C("A combined view with no layers beside it cannot be checked. A colourful "
                           "image with no legend is not an analysis.", 12.5, GREY)])

# 6 ── P3d SHEET LAYOUT
s = d.slide(CREAM)
s.header("THE P3d SHEET — ONE 17 × 11",
         "Small views of each layer beside one larger combined view. Every view has a legend.")
SX, SY, SW, SH = L, 1.95, 7.0, 7.0 * 11 / 17
s.card(SX, SY, SW, SH, fill="FFFFFF")
SMW, SMH, SMG = 2.2, 0.98, 0.1
for i, lab in enumerate(["LAYER A", "LAYER B", "LAYER C"]):
    zy = SY + 0.15 + i * (SMH + SMG)
    s.rect(SX + 0.15, zy, SMW, SMH, fill=PAPER, line=BLACK, lw=Pt(1.5))
    s.chip(SX + 0.25, zy + 0.1, 0.45, 0.3, "01", fill=CYAN, size=9.5, shadow=False)
    s.t(SX + 0.78, zy + 0.07, 1.5, 0.3, [s.Ab(lab, 10)])
    G.gray_ramp(s, SX + 0.3, zy + SMH - 0.3, SMW - 0.3, 0.12)
BX, BY, BW, BH = SX + 2.5, SY + 0.15, 4.35, 3.14
s.rect(BX, BY, BW, BH, fill=PAPER, line=BLACK, lw=Pt(1.5))
s.chip(BX + 0.12, BY + 0.12, 0.45, 0.3, "02", fill=LIME, size=9.5, shadow=False)
s.t(BX + 0.7, BY + 0.08, 3.5, 0.3, [s.Ab("COMBINED VIEW — LARGE", 11)])
s.t(BX + 0.15, BY + BH - 0.72, 4.0, 0.25, [s.A("N ↑     SCALE BAR     LEGEND + UNITS", 9, GREY)])
G.gray_ramp(s, BX + 0.15, BY + BH - 0.4, 2.6, 0.18)
s.rect(BX + 2.95, BY + BH - 0.36, 1.2, 0.09, fill=BLACK, line=None)
s.rect(BX + 3.55, BY + BH - 0.36, 0.6, 0.09, fill="FFFFFF", line=BLACK, lw=Pt(1.0))
IY = SY + 3.4
s.rect(SX + 0.15, IY, SW - 0.3, SH - 3.55, fill=PAPER, line=BLACK, lw=Pt(1.5))
s.chip(SX + 0.27, IY + 0.12, 0.45, 0.3, "03", fill=PINK, size=9.5, shadow=False)
s.t(SX + 0.85, IY + 0.08, 5.8, 0.6, [s.Ab("INTERPRETATION  ·  SITE RECORD  ·  TOOL, INPUTS, RANGES", 10.5)])
s.panel(7.95, 1.95, 4.7, 3.7, " ", headfill=BLACK, tsize=13.5)
s.t(7.95 + 0.25, 1.95, 4.2, 0.55, [s.Ab("EACH ZONE MUST SAY", 13.5, CREAM)],
    anchor=MSO_ANCHOR.MIDDLE)
s.t(8.2, 2.7, 4.2, 2.85, [
    s.Cb("01  Each layer: what it measures, its legend and units.", 13.5),
    s.Cb(" ", 8),
    s.Cb("02  The combination: which layers, which weights, which operation.", 13.5),
    s.Cb(" ", 8),
    s.Cb("03  What the combined view shows about the site — plus source, units, scale, north, "
         "and the tool you used.", 13.5)],
    ls=1.2)
s.banner(5.85, "SAME SCALE AND NORTH IN EVERY VIEW.", x=7.95, w=4.7,
         fill=PINK, h=0.63, size=12.5, align=PP_ALIGN.CENTER)

# 7 ── ISSUED — P3d
issued_slide(d, "P3d",
             blurb="Pick a site you can document and map its point cloud in at least three layers "
                   "with attractor logic. Show each layer small, with its legend, beside one larger "
                   "combined view, and say what the combination shows.",
             cards=[("LAYERS", "THREE AT LEAST", "Distance to points or curves, height bands, a "
                                                  "recorded attribute."),
                    ("SHEET", "ONE 17 × 11", "Small views of each layer beside one larger combined "
                                            "view."),
                    ("TOOL", "MIXTLI OR EQUIVALENT", "The Blender add-on the instructor provides. "
                                                    "Record inputs and ranges.")])

# 8 ── REQUIREMENTS — P3d
requirements_slide(d, "P3d", sub=VISUAL)

# 9 ── P3c CHECKPOINT
s = d.slide(BLACK)
s.header("P3c CHECKPOINT — FIELD + FIRST LINES",
         C.checkpoints("P3c")[0][1] + " Read them side by side.")
chk = [("FIELD", CYAN, "Grayscale field with its legend: near → far, input range written.",
        "Wrong? Fix the remap before the lines."),
       ("LINES", LIME, "First line drawing from the same field, with one mapping.",
        "Wrong? Change one mapping value."),
       ("DENSITY", YELLOW, "Darkest area still separate lines? Lightest area still visible?",
        "Wrong? Change the output range."),
       ("SVG", PINK, "17 × 11 at 100%. Clean curves: no fills, no duplicate lines.",
        "Wrong? Fix the export.")]
x = L
for nm, col, q, fix in chk:
    s.panel(x, 1.95, 2.85, 3.55, nm, headfill=col, tsize=13.5)
    s.t(x + 0.22, 2.7, 2.4, 1.7, [s.Cb(q, 13)], ls=1.3)
    s.rule(x + 0.22, 4.5, 2.4, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.22, 4.62, 2.4, 0.75, [s.Cb(fix, 12.5, bold=True)], ls=1.2)
    x += 3.05
s.banner(5.85, "PLOTTING IS OPTIONAL. IF YOU PLOT, TEST A SMALL CROP FIRST AND KEEP THE TEST FOR THE SHEET.",
         fill=YELLOW, h=0.68, size=12, align=PP_ALIGN.CENTER)

# 10 ── WEEK 10 DEADLINE CHECKLIST
MUST = {"GSM": "Four pages. Each rule beside a tested application.",
        "P2a": "The BIG-style process sheet, with instructions and pseudocode.",
        "P2b": "The print, its process sheet, and the source, mesh and slicer files.",
        "P3a": "One module sheet: studio render, one material, deliberate lighting.",
        "P3b": "Two sheets of arrays, with one conditional selection and its rule.",
        "P3c": "One sheet: line drawing, grayscale field and legend. SVG and graph."}
items = sorted((m for m in C.MILESTONES.values()
                if isinstance(m.get("due"), int) and m["due"] <= DL),
               key=lambda m: (m.get("project") or "", m["id"]))
s = d.slide(CREAM)
s.header("WEEK %d DEADLINE CHECKLIST" % DL,
         "Next class. Everything through Arrays must be in. Tick every line.")
y, h = 1.9, 0.6
for i, m in enumerate(items):
    col = ACCENTS[i % 4]
    s.chip(L, y, 0.95, h, m["id"], fill=col, size=13)
    s.card(L + 1.2, y, W - 1.2, h, fill=CREAM)
    s.t(L + 1.45, y, 3.6, h, [s.Ab(m["title"].split(" — ")[0].upper(), 10.5)], anchor=MSO_ANCHOR.MIDDLE)
    s.t(L + 5.1, y, 5.1, h, [s.Cb(MUST.get(m["id"], ""), 12)], anchor=MSO_ANCHOR.MIDDLE)
    tag = "DUE NEXT CLASS" if m["due"] == DL else "DUE W%d · IN?" % m["due"]
    s.t(W - 1.15, y, 1.7, h, [s.Ab(tag, 10, PINK if m["due"] == DL else GREY)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    y += h + 0.12
s.banner(min(y + 0.05, 6.5), "%s — MID-SEMESTER DEADLINE. %s ARE DUE. NOTHING THROUGH ARRAYS "
                             "IS LEFT OUT." % (C.date_long(DL).upper(), DUE_DL_TXT.replace(" and ", " AND ")),
         fill=BLACK, color=YELLOW, h=0.58, size=12, align=PP_ALIGN.CENTER)

# 11 ── NOW
now_slide(d, "NOW — CHECKPOINT, THEN LAYERS",
          "Rest of the class: P3c review one table at a time, then start the site.",
          ["P3c: field and first line drawing reviewed; one change written down",
           "P3d: site picked — source, units, scale and orientation recorded",
           "P3d: first layer mapped, with its legend and units",
           "P3d: the next two layers chosen, and what each will measure written down",
           "Deadline: every item on the checklist located and ready to submit"],
          closer="TWO LAYERS WITH LEGENDS BY NEXT CLASS.",
          bg=CYAN, closer_color=YELLOW)

# 12 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("DEADLINE", "Next class, %s, is the mid-semester deadline. %s are due; everything "
                 "through Arrays must be in." % (C.date_long(DL).title(), DUE_DL_TXT)),
    ("NEXT", "%s is a regular class: Volumetric Data — signed distance fields (SDF). P4a is issued."
             % C.date_long(DL).title()),
    ("P3d", "Checkpoint next class. %s P3d is due %s."
            % (cp_txt, C.date_long(P3D_DUE).title())),
    ("P3c", "Finish the sheet: line drawing, grayscale field and legend. Submit the SVG, the sheet "
            "PDF and the editable graph. Plotting is optional."),
])

d.save(os.path.join(OUT, "ARC3133_Class09.pptx"))
print("class09 ok — %d slides" % len(d.prs.slides._sldIdLst))
