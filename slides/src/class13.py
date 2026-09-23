# -*- coding: utf-8 -*-
"""Class 13 — Parts for the laser cutter (U09, second class). P4b checkpoint."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(13)
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 13
FAB_RUBRIC = ("Visual documentation 20% · computational understanding 20% · technical execution 15% "
              "· fabrication quality 30% · experimentation 5% · requirements and identity 10%.")

# 1 ── TITLE
title_slide(d, WK, ["PARTS FOR THE", "LASER CUTTER"],
            "P4b CONTINUES — A CONTOUR BECOMES A PART YOU CAN HOLD", bg=YELLOW, lfill=PINK, rfill=CYAN,
            right_tag="P4b CHECKPOINT")

# 2 ── THICKNESS
s = d.slide(CREAM)
s.header("THICKNESS IS A DIMENSION",
         "Last week a slice was a curve. Today it has a thickness, and the thickness is real.")
cases = [("INTERVAL = THICKNESS", CYAN, 0.0, "Parts touch. A solid stack with stepped edges."),
         ("INTERVAL > THICKNESS", LIME, 0.14, "Gaps between parts. Light passes; something must hold them."),
         ("INTERVAL < THICKNESS", PINK, -1, "Parts collide. Change the interval or the material.")]
x = L
for nm, col, gap, cap in cases:
    s.panel(x, 1.95, 3.85, 3.3, nm, headfill=col, tsize=13.5)
    th = 0.14
    yy = 2.8
    for k in range(6):
        w = 2.6 - abs(k - 2.5) * 0.3
        if gap < 0:
            s.rect(x + (3.85 - w) / 2, yy, w, th, fill=MUTE if k % 2 else PAPER, line=BLACK, lw=HAIR)
            yy += th * 0.6
        else:
            s.rect(x + (3.85 - w) / 2, yy, w, th, fill=MUTE, line=BLACK, lw=HAIR)
            yy += th + gap
    s.t(x + 0.28, 4.3, 3.3, 0.85, [s.Cb(cap, 13)], ls=1.3, align=PP_ALIGN.CENTER)
    x += 4.08
s.banner(5.55, "MEASURE THE SHEET YOU WILL CUT. A NOMINAL THICKNESS IS NOT A MEASURED ONE — "
              "DESIGN TO THE NUMBER YOU MEASURED.", fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)
s.t(L, 6.5, W, 0.5, [s.C("Slice count × thickness + gaps = assembled height. Check it against the 300 mm limit "
                         "before you cut anything.", 13.5, GREY)], ls=1.3)

# 3 ── REGISTRATION
s = d.slide(BLACK)
s.header("REGISTRATION: HOW PARTS FIND EACH OTHER",
         "Twelve loose parts are not an assembly. Choose one system and draw it into every part.")
reg = [("SPINE", CYAN, "A cross member with notches. Each slice has a matching slot and drops onto it.",
        "Order is fixed by the notches."),
       ("DOWEL", LIME, "Two or more holes through every slice. Rods pass through and align the stack.",
        "Holes must line up on every part."),
       ("SPACER", PINK, "Separate small pieces set the gap between slices. Used with a dowel or glue.",
        "Spacers count as parts on the sheet.")]
x = L
for nm, col, body, note in reg:
    s.panel(x, 2.05, 3.85, 3.35, nm, headfill=col, tsize=15)
    s.t(x + 0.28, 2.8, 3.3, 1.5, [s.Cb(body, 13.5)], ls=1.3)
    s.rule(x + 0.28, 4.3, 3.3, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.28, 4.45, 3.3, 0.8, [s.Cb(note, 12.5, GREY)], ls=1.25)
    x += 4.08
s.banner(5.8, "THE REGISTRATION IS PART OF THE DESIGN. IT IS VISIBLE, SO DRAW IT ON THE PROCESS SHEET.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 4 ── KERF AND FIT
s = d.slide(CREAM)
s.header("KERF, AND THE FIT TEST",
         "The beam removes a thin strip of material. Every edge moves by half of it.")
s.panel(L, 1.95, 6.2, 3.55, "THE TEST COUPON", headfill=CYAN)
s.rect(L + 0.4, 2.85, 5.4, 1.1, fill=PAPER, line=BLACK, lw=THIN)
widths = [0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22]
xx = L + 0.75
for i, wv in enumerate(widths):
    s.rect(xx, 2.85, wv, 0.6, fill=CREAM, line=BLACK, lw=HAIR)
    s.t(xx - 0.2, 3.55, wv + 0.4, 0.3, [s.Mb("%02d" % (i + 1), 9)], align=PP_ALIGN.CENTER)
    xx += wv + 0.55
s.t(L + 0.4, 4.1, 5.4, 1.3, [
    s.Cb("A strip of slots in steps of width, cut from your actual sheet. Push a scrap of the same "
         "sheet into each. The one that holds without forcing is your fit.", 13)], ls=1.3)
s.panel(7.15, 1.95, 5.5, 3.55, "WHAT TO RECORD", headfill=LIME)
s.t(7.45, 2.7, 4.9, 2.7, [
    s.Cb("—  the measured sheet thickness", 13.5),
    s.Cb("—  the slot width that fit", 13.5),
    s.Cb("—  the kerf you measured", 13.5),
    s.Cb("—  the offset you applied: kerf / 2", 13.5),
    s.Cb("—  the machine settings the FabLab used", 13.5)], ls=1.3, space=5)
s.banner(5.8, "TEST BEFORE THE BATCH. THE COUPON AND ANY FAILED PARTS COUNT AGAINST YOUR ONE SHEET.",
         fill=PINK, h=0.7, align=PP_ALIGN.CENTER)
s.t(L, 6.7, W, 0.4, [s.C("Coupon slot widths above are a diagram, not values to copy.", 12.5, GREY)])

# 5 ── CLOSE AND CLEAN
s = d.slide(BLACK)
s.header("CLOSE AND CLEAN THE PROFILES",
         "A contour from a mesh is rarely a clean part. Fix it before it becomes a cutting file.")
rows = [("CLOSED", CYAN, "Every part outline is one closed curve. An open curve is not a part."),
        ("SINGLE", LIME, "No duplicate or overlapping lines. The beam cuts twice where lines overlap."),
        ("SIMPLE", YELLOW, "Remove tiny fragments and islands you could not hold or glue."),
        ("SOUND", PINK, "Check the thinnest neck of each part. If it would snap, change the profile.")]
y = 2.0
for nm, col, body in rows:
    s.chip(L, y, 1.9, 0.78, nm, fill=col, size=14)
    s.card(L + 2.2, y, W - 2.2, 0.78, fill=CREAM)
    s.t(L + 2.5, y, W - 2.8, 0.78, [s.Cb(body, 14)], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.98
s.banner(6.0, "CLEAN THE PROFILES IN THE GRAPH, NOT BY HAND IN THE CUTTING FILE — OR THE NEXT CHANGE UNDOES IT.",
         fill=LIME, h=0.7, align=PP_ALIGN.CENTER)

# 6 ── LABEL, ORDER, NEST
s = d.slide(CREAM)
s.header("LABEL, ORDER, NEST",
         "The slice order from last week becomes the part numbers. Then the parts go onto one sheet.")
s.panel(L, 1.95, 5.6, 3.6, "LABEL AND ORDER", headfill=YELLOW)
s.t(L + 0.3, 2.7, 5.0, 2.7, [
    s.Cb("—  Number every part in slice order: 01, 02, 03 …", 13.5),
    s.Cb("—  Engrave the number on a face the assembly will hide", 13.5),
    s.Cb("—  Add a mark for which way is up and which side faces front", 13.5),
    s.Cb("—  Keep a list: part, slice position, registration", 13.5)], ls=1.3, space=5)
s.panel(6.55, 1.95, 6.1, 3.6, "NEST ON ONE SHEET", headfill=CYAN)
s.rect(6.85, 2.75, 3.1, 2.55, fill=PAPER, line=BLACK, lw=THIN)
parts = [(6.95, 2.85, 1.3, 0.6), (8.35, 2.85, 1.0, 0.6), (6.95, 3.55, 0.9, 0.9), (7.95, 3.55, 1.15, 0.5),
         (7.95, 4.15, 0.75, 0.5), (8.8, 4.15, 0.45, 0.5), (6.95, 4.55, 0.9, 0.35), (9.45, 2.85, 0.4, 1.2)]
for i, (px, py, pw, ph) in enumerate(parts):
    s.rect(px, py, pw, ph, fill=CREAM, line=BLACK, lw=HAIR)
    s.t(px, py, pw, ph, [s.Mb("%02d" % (i + 1), 8)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
s.t(10.15, 2.75, 2.35, 2.6, [
    s.Cb("Keep a margin from the sheet edge", 12),
    s.Cb("Leave a gap between parts", 12),
    s.Cb("Reserve room for the coupon and one spare", 12)], ls=1.25, space=8)
s.banner(5.85, "P4b: FIT THE ASSEMBLY IN ONE CONFIRMED SHEET. IF IT DOES NOT NEST, CHANGE THE SLICES, "
              "NOT THE RULE.", fill=BLACK, color=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 7 ── FILE HYGIENE AND FABLAB
s = d.slide(BLACK)
s.header("THE CUTTING FILE, AND THE LAB",
         "The machine reads lines, not intentions. Use the conventions the FabLab gives you.")
s.panel(L, 2.05, 5.85, 3.55, "FILE HYGIENE", headfill=LIME)
s.t(L + 0.3, 2.8, 5.25, 2.7, [
    s.Cb("—  Vector lines only. Nothing is cut from an image.", 13.5),
    s.Cb("—  Cut and engrave lines kept apart, by the color or layer the lab specifies", 13.5),
    s.Cb("—  Real units, drawn at 1:1. Check one known dimension.", 13.5),
    s.Cb("—  Stroke weight set as the lab specifies", 13.5),
    s.Cb("—  Text converted to outlines", 13.5)], ls=1.25, space=4)
s.panel(6.8, 2.05, 5.85, 3.55, "FABLAB PROCEDURES", headfill=PINK)
s.t(7.1, 2.8, 5.25, 2.7, [
    s.Cb("—  Safety orientation completed before you use a machine", 13.5),
    s.Cb("—  Book machine time; check what the lab has confirmed", 13.5),
    s.Cb("—  Confirm your material is approved for cutting", 13.5),
    s.Cb("—  Stay with the machine while it runs", 13.5),
    s.Cb("—  Follow staff instructions over anything on this slide", 13.5)], ls=1.25, space=4)
s.banner(5.9, "REGENERATE THE CUTTING FILE AFTER ANY GEOMETRY OR MATERIAL CHANGE. NEVER PATCH AN OLD ONE.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 8 ── REQUIREMENTS (REMINDER)
s = requirements_slide(d, "P4b", sub=None, title="REMINDER — P4b")
s.t(L, 1.4, W, 0.34, [s.C(FAB_RUBRIC, 12, GREY)])

# 9 ── NOW
now_slide(d, "NOW — CHECKPOINT, THEN PARTS",
          "Rest of the class: review with me first, then turn contours into parts.",
          ["Section direction and interval chosen, with the comparison to show why",
           "Sheet thickness measured, and a registration system drawn into the parts",
           "A kerf and fit coupon drawn, ready for the lab",
           "Profiles closed and cleaned; every part numbered in slice order",
           "A first nesting layout on one sheet, with room for the coupon"],
          closer="NOTHING GOES TO THE CUTTER UNTIL THE COUPON FITS.",
          bg=CYAN)

# 10 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "Week 14 (target " + C.date_long(14).split("— ")[1] + ") — Final production and assembly, "
             "photographing the work, and the booklet."),
    ("TEST", "Cut the kerf and fit coupon under FabLab procedures. Record the fit and update the parts "
             "and the cutting file."),
    ("PREPARE", "A production-ready cutting file: labeled, nested on one sheet, regenerated after "
                "the test."),
    ("TRACK", "P4b is due at the final review (%d%% of the grade). Keep" % C.milestone("P4b")["weight"] +
              " the test cuts and failed parts: they belong in the documentation."),
])

d.save(os.path.join(OUT, "ARC3133_Class13.pptx"))
print("class13 ok — %d slides" % len(d.prs.slides._sldIdLst))
