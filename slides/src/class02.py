# -*- coding: utf-8 -*-
"""Class 02 — Constructive Solid Geometry (U02). P2a issued."""
import os
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(2)
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt, Inches
from pptx.enum.shapes import MSO_SHAPE

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 2

# 1 ── TITLE
title_slide(d, WK, ["CONSTRUCTIVE", "SOLID GEOMETRY"],
            "P2 BEGINS — DESCRIBE A SOLID AS AN EDITABLE SEQUENCE", bg=CYAN, lfill=PINK, rfill=YELLOW)

# 2 ── WHY NON-DESTRUCTIVE
s = d.slide(BLACK)
s.header("WHY NON-DESTRUCTIVE",
         "The same two solids, subtracted. One keeps its history; one throws it away.")
s.panel(L, 2.05, 5.85, 3.35, "DESTRUCTIVE", headfill=MUTE)
s.t(L + 0.3, 2.8, 5.25, 2.2, [
    s.Cb("CUBE  −  SPHERE  →  ONE MESH", 14, bold=True),
    s.Cb(" ", 8),
    s.Cb("The sphere is gone. Its radius is gone. To change anything you rebuild from scratch.", 14)], ls=1.35)
s.panel(6.8, 2.05, 5.85, 3.35, "NON-DESTRUCTIVE", headfill=LIME)
s.t(7.1, 2.8, 5.25, 2.2, [
    s.Cb("CUBE  +  SPHERE  →  DIFFERENCE  →  RESULT", 14, bold=True),
    s.Cb(" ", 8),
    s.Cb("Every input is still a live node. Change the radius and everything downstream "
         "recomputes itself.", 14)], ls=1.35)
s.banner(5.75, "P2a REQUIRES YOUR OPERATION HISTORY TO BE INTACT. YOU WILL BE ASKED TO CHANGE A "
              "PARAMETER IN FRONT OF THE CLASS.", fill=PINK, h=0.72, align=PP_ALIGN.CENTER)

# 3 ── TRANSFORMATIONS ARE ARITHMETIC
s = d.slide(CREAM)
s.header("TRANSFORMATIONS ARE ARITHMETIC",
         "Three operations you already know, written as what they actually do.")
tr = [("TRANSLATE", CYAN, "=  ADD", ["x' = x + dx", "y' = y + dy", "z' = z + dz"], "(2, 1)  +  (3, 0)   →   (5, 1)"),
      ("SCALE", LIME, "=  MULTIPLY", ["x' = x × f", "y' = y × f", "z' = z × f"], "(2, 1)  ×  2        →   (4, 2)"),
      ("ROTATE", PINK, "=  MIX x AND y", ["x' = x·cosθ − y·sinθ", "y' = x·sinθ + y·cosθ"], "(1, 0)  rot 90°    →   (0, 1)")]
x = L
for nm, col, sub, lines, ex in tr:
    s.panel(x, 1.95, 3.85, 3.4, nm, headfill=col, tsize=15)
    s.t(x + 0.28, 2.68, 3.3, 0.3, [s.Ab(sub, 12)])
    s.t(x + 0.28, 3.1, 3.3, 1.2, [s.Mb(l, 11.5) for l in lines], ls=1.35)
    s.rule(x + 0.28, 4.5, 3.3, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.28, 4.68, 3.3, 0.5, [s.Mb(ex, 10.5)])
    x += 4.08
s.banner(5.65, "Translation and scale treat each coordinate on its own. Rotation is the only one where "
              "x and y have to talk to each other.", fill=YELLOW, h=0.72)

# 4 ── THREE BOOLEANS
s = d.slide(CREAM)
s.header("THREE BOOLEANS", "Everything in P2a is built from these, applied in order.")
bl = [("UNION", CYAN, "A + B", "Everything either solid occupies."),
      ("DIFFERENCE", PINK, "A − B", "A, with B carved out of it."),
      ("INTERSECTION", LIME, "A ∩ B", "Only where both solids overlap.")]
x = L
for nm, col, sym, body in bl:
    s.panel(x, 1.95, 3.85, 3.1, nm, headfill=col, tsize=15)
    s.t(x + 0.28, 2.85, 3.3, 0.7, [s.Ab(sym, 30)], align=PP_ALIGN.CENTER)
    s.t(x + 0.28, 3.95, 3.3, 0.8, [s.Cb(body, 13)], ls=1.3, align=PP_ALIGN.CENTER)
    x += 4.08
s.banner(5.35, "ORDER MATTERS. A − B IS NOT B − A, AND YOUR DIAGRAM MUST MAKE THE OPERANDS UNAMBIGUOUS.",
         fill=BLACK, color=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 6.25, W, 0.8, [s.C("P2a asks for all three. In every subtraction, label the solid you keep and the "
                          "solid you remove. Reverse one once, deliberately, and you will not confuse "
                          "the operands again.", 13.5, GREY)], ls=1.3)

# 5 ── THE UNIT, STEP BY STEP
unit_steps_slide(d, "U02", title="THE SEQUENCE",
                 sub="What we build together, in order, this class.", n=(0, 4))

# 6 ── THE NOTATION
s = d.slide(CREAM)
s.header("THE NOTATION",
         "Write the procedure as pseudocode. Formal enough to be unambiguous, plain enough to read aloud.")
s.panel(L, 1.95, 5.6, 3.5, "THE OPERATIONS", headfill=CYAN)
s.t(L + 0.35, 2.7, 5.0, 2.5, [
    s.Mb("cube(size)        sphere(r)", 12),
    s.Mb("cylinder(r, h)", 12),
    s.Mb(" ", 7),
    s.Mb("translate(s, x, y, z)", 12),
    s.Mb("rotate(s, x, y, z)    # degrees", 12),
    s.Mb("scale(s, factor)", 12),
    s.Mb(" ", 7),
    s.Mb("union(a, b)       intersection(a, b)", 12),
    s.Mb("difference(keep, remove)", 12)], ls=1.3)
s.panel(6.6, 1.95, 6.05, 3.5, "WORKED EXAMPLE", headfill=LIME)
s.t(6.9, 2.7, 5.45, 2.5, [
    s.Mb("base   = cube(6)", 12),
    s.Mb("tower  = cube(2)", 12),
    s.Mb("tower  = scale(tower, 1.5)", 12),
    s.Mb("tower  = translate(tower, 2, 0, 4)", 12),
    s.Mb("void   = cylinder(r=1, h=8)", 12),
    s.Mb(" ", 7),
    s.Mb("mass   = union(base, tower)", 12),
    s.Mb("result = difference(mass, void)", 12)], ls=1.35)
s.banner(5.65, "THREE RULES: EVERY SHAPE STARTS AT THE ORIGIN · EVERY STEP ASSIGNS A NAME · "
              "EVERY DIFFERENCE NAMES WHAT IT KEEPS AND WHAT IT REMOVES.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

pseudocode_slide(d, "U02",
                 note="SAME NOTATION AS THE LAST SLIDE. NINE NUMBERED STEPS, NINE FRAMES — THAT IS YOUR P2a SHEET.")


# 8 ── HOW TO DRAW A BIG-STYLE PROCESS DIAGRAM
def poly(sl, pts, fill, line=BLACK, lw=THIN):
    ff = sl.s.shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    ff.add_line_segments([(Inches(px), Inches(py)) for px, py in pts[1:]], close=True)
    sh = ff.convert_to_shape()
    sh.shadow.inherit = False
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    sh.line.color.rgb = rgb(line); sh.line.width = lw
    return sh


s = d.slide(CREAM)
s.header("HOW TO DRAW A BIG-STYLE PROCESS DIAGRAM",
         "Explain the building as a row of simple moves: one move per frame, read left to right.",
         tsize=30)
fw, fh, ag = 2.0, 1.55, 0.5
fy = 1.95
verbs = ["01  PLACE", "02  STACK", "03  SHIFT", "04  CARVE", "05  KEEP"]
for i, verb in enumerate(verbs):
    fx = L + i * (fw + ag)
    s.card(fx, fy, fw, fh, fill=CREAM, lw=THIN)
    gy = fy + fh - 0.25                     # ground line
    s.rule(fx + 0.15, gy, fw - 0.3, lw=Pt(1.5), color=GREY)
    bx, bw, bh = fx + 0.45, 1.1, 0.55       # base block
    tw, th = 0.5, 0.45                      # top block
    tx0 = bx + 0.3
    if i == 0:
        s.rect(bx, gy - bh, bw, bh, fill=CYAN, lw=THIN)
    elif i == 1:
        s.rect(bx, gy - bh, bw, bh, fill=PAPER, lw=THIN)
        s.rect(tx0, gy - bh - th, tw, th, fill=CYAN, lw=THIN)
    elif i == 2:
        s.rect(bx, gy - bh, bw, bh, fill=PAPER, lw=THIN)
        s.rect(tx0, gy - bh - th, tw, th, fill=None, line=MUTE, lw=HAIR)
        s.rect(bx + bw - tw, gy - bh - th, tw, th, fill=CYAN, lw=THIN)
    elif i == 3:
        s.rect(bx, gy - bh, bw, bh, fill=PAPER, lw=THIN)
        s.rect(bx + bw - tw, gy - bh - th, tw, th, fill=PAPER, lw=THIN)
        s.rect(bx - 0.12, gy - 0.32, 0.5, 0.32, fill=PINK, lw=THIN)
    else:
        n = 0.38
        poly(s, [(bx + n, gy), (bx + bw, gy), (bx + bw, gy - bh - th),
                 (bx + bw - tw, gy - bh - th), (bx + bw - tw, gy - bh), (bx, gy - bh),
                 (bx, gy - 0.32), (bx + n, gy - 0.32)], LIME)
    s.chip(fx, fy + fh + 0.12, fw, 0.4, verb, fill=YELLOW if i < 4 else LIME, size=11,
           shadow=False)
    if i < len(verbs) - 1:
        s.rect(fx + fw + 0.1, fy + fh / 2 - 0.15, ag - 0.2, 0.3, fill=BLACK, line=None,
               shape=MSO_SHAPE.RIGHT_ARROW)
rules = [("FRAMES", "Eight or nine, numbered, all the same size, in one row or a grid."),
         ("ONE MOVE", "One operation per frame. If a frame needs two verbs, split it."),
         ("SAME VIEW", "Same camera, same scale in every frame, so only the move changes."),
         ("VERBS", "Caption each frame with one verb: place, stack, shift, turn, carve."),
         ("ARROWS", "Arrows or numbers carry the order. Nobody should have to guess it."),
         ("KEPT / REMOVED", "The new part is the only colour. A removed solid gets its own colour.")]
cw = (W - 0.3) / 2
for k, (tag, body) in enumerate(rules):
    cx = L + (k % 2) * (cw + 0.3)
    cy = 4.2 + (k // 2) * 0.72
    s.chip(cx, cy, 1.75, 0.56, tag, fill=ACCENTS[k % 4], size=11)
    s.t(cx + 1.95, cy, cw - 1.95, 0.56, [s.Cb(body, 12.5)], anchor=MSO_ANCHOR.MIDDLE)
s.t(L, 6.45, W, 0.6, [s.C("Legend above: cyan is the move in this frame, grey is what already exists, "
                          "pink is the solid being removed, lime is the result.", 12.5, GREY)])


# 9 ── ISSUED TODAY
issued_slide(d, "P2a", blurb=C.PROJECTS["P2"]["description"] +
             "  This first assignment is the process sheet: an ordered sequence of primitives, "
             "transformations and Booleans, drawn so another person could rebuild it.",
             cards=[("STAGE 1", "THE SEQUENCE", "Three primitives. Translate, rotate, scale. Union, difference, intersection."),
                    ("STAGE 2", "THE FRAMES", "Eight or nine, numbered. One operation each, read in sequence."),
                    ("STAGE 3", "THE LAST ONE", "At building scale: a 1.75 m figure, vegetation, ground, shadow.")])

# 8 ── REQUIREMENTS
requirements_slide(d, "P2a",
                   sub="Visual quality 35% · computational understanding 25% · technical execution 20% "
                       "· experimentation 10% · requirements and identity 10%.")

# 9 ── NOW
now_slide(d, "NOW — BUILD THE SEQUENCE",
          "Rest of the class: a working graph with something you can change in front of me.",
          ["Object chosen — simple massing, eight or nine clear moves, no complex curves",
           "First three primitives placed, each born at the origin and moved from there",
           "At least one Boolean working, with the kept and removed solids named",
           "Two useful inputs exposed, so a variant is one number away",
           "Operation history intact — nothing collapsed or applied"],
          closer="LEAVE WITH A GRAPH YOU CAN CHANGE, NOT A MESH YOU CANNOT.",
          bg=LIME)

# 10 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "%s — CSG continued, and 3D printing. P2b, the printed version of your CSG "
             "object, is issued." % C.date_long(3)),
    ("BUILD", "Keep going on P2a, due %s: eight or nine frames, the last one at building scale, "
              "and instructions with matching pseudocode beside them." % C.date_long(C.milestone("P2a")["due"])),
    ("BRING", "The editable file with its inputs exposed. Next class we check that the solid is "
              "closed and measure it for printing."),
    ("READ", "Di Mari and Yoo, Operative Design, and Di Mari, Conditional Design. Find the spatial "
             "operation your own sequence explores, and name it on the sheet."),
])

d.save(os.path.join(OUT, "ARC3133_Class02.pptx"))
print("class02 ok — %d slides" % len(d.prs.slides._sldIdLst))
