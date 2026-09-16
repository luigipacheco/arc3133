# -*- coding: utf-8 -*-
"""Class 02 — Transformations and CSG (U02). P1a issued."""
import os
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 2

# 1 ── TITLE
title_slide(d, WK, ["TRANSFORMATIONS", "AND CSG"],
            "P1 BEGINS — DESCRIBE A SOLID AS AN EDITABLE SEQUENCE", bg=CYAN, lfill=PINK, rfill=YELLOW)

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
    s.Cb("CUBE  +  SPHERE  →  SUBTRACT  →  RESULT", 14, bold=True),
    s.Cb(" ", 8),
    s.Cb("Every input is still a live node. Change the radius and everything downstream "
         "recomputes itself.", 14)], ls=1.35)
s.banner(5.75, "P1a REQUIRES YOUR OPERATION HISTORY TO BE INTACT. YOU WILL BE ASKED TO CHANGE A "
              "PARAMETER IN FRONT OF THE CLASS.", fill=PINK, h=0.72, align=PP_ALIGN.CENTER)

# 3 ── TRANSFORMATIONS ARE ARITHMETIC
s = d.slide(CREAM)
s.header("TRANSFORMATIONS ARE ARITHMETIC",
         "Three operations you already know, written as what they actually do.")
tr = [("MOVE", CYAN, "=  ADD", ["x' = x + dx", "y' = y + dy", "z' = z + dz"], "(2, 1)  +  (3, 0)   →   (5, 1)"),
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
s.banner(5.65, "Move and scale treat each coordinate on its own. Rotation is the only one where "
              "x and y have to talk to each other.", fill=YELLOW, h=0.72)

# 4 ── THREE BOOLEANS
s = d.slide(CREAM)
s.header("THREE BOOLEANS", "Everything in P1a is built from these, applied in order.")
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
s.t(L, 6.25, W, 0.8, [s.C("P1a asks for at least three Booleans, so one of them can be a reversed subtraction. "
                          "Do it once deliberately and you will never confuse the operands again.",
                          13.5, GREY)], ls=1.3)

# 5 ── THE UNIT, STEP BY STEP
unit_steps_slide(d, "U02", title="THE SEQUENCE",
                 sub="What we build together, in order, this session.")

# 6 ── THE NOTATION
s = d.slide(CREAM)
s.header("THE NOTATION",
         "Write the procedure as pseudocode. Formal enough to be unambiguous, plain enough to read aloud.")
s.panel(L, 1.95, 5.6, 3.5, "THE OPERATIONS", headfill=CYAN)
s.t(L + 0.35, 2.7, 5.0, 2.5, [
    s.Mb("box(x, y, z)      cylinder(r, h)", 12),
    s.Mb("sphere(r)         cone(r, h)", 12),
    s.Mb(" ", 7),
    s.Mb("move(s, x, y, z)  rotate(s, axis, deg)", 12),
    s.Mb("scale(s, factor)", 12),
    s.Mb(" ", 7),
    s.Mb("union(a, b)       subtract(a, b)", 12),
    s.Mb("intersect(a, b)", 12)], ls=1.35)
s.panel(6.6, 1.95, 6.05, 3.5, "WORKED EXAMPLE", headfill=LIME)
s.t(6.9, 2.7, 5.45, 2.5, [
    s.Mb("base   = box(6, 4, 3)", 12),
    s.Mb("tower  = box(2, 2, 6)", 12),
    s.Mb("tower  = move(tower, 2, 0, 3)", 12),
    s.Mb("void   = cylinder(r=1, h=5)", 12),
    s.Mb("void   = move(void, -1.5, 0, 0)", 12),
    s.Mb(" ", 7),
    s.Mb("mass   = union(base, tower)", 12),
    s.Mb("result = subtract(mass, void)", 12)], ls=1.35)
s.banner(5.65, "THREE RULES: EVERY SHAPE IS BORN AT THE ORIGIN · UNITS ARE ABSTRACT · "
              "EVERY STEP ASSIGNS A NAME, SO A SUBTRACTION IS NEVER IN DOUBT.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

pseudocode_slide(d, "U02",
                 note="THIS IS THE NOTATION FROM THE LAST SLIDE, AND IT IS ALSO PYTHON. MORE ON THAT IN DECEMBER.")

# 7 ── ISSUED TODAY
m = C.milestone("P1a")
issued_slide(d, "P1a", blurb=C.PROJECTS["P1"]["description"] +
             "  This first milestone is the massing study: an ordered sequence of primitives and "
             "Booleans, diagrammed so another person could follow it.",
             cards=[("STAGE 1", "THE SEQUENCE", "Three primitives, three transformations, three Booleans, in a stated order."),
                    ("STAGE 2", "THE DIAGRAMS", "Eight or nine, numbered. One operation each, read left to right."),
                    ("STAGE 3", "THE LAST ONE", "Drawn, not diagrammed: building scale, a figure, planting, ground, shadow.")])

# 8 ── REQUIREMENTS
requirements_slide(d, "P1a",
                   sub="Visual quality 35% · computational understanding 25% · technical execution 20% "
                       "· experimentation 10% · requirements and identity 10%.")

# 9 ── NOW
now_slide(d, "NOW — BUILD THE SEQUENCE",
          "Rest of the session: a working graph with something you can change in front of me.",
          ["Object chosen — orthogonal massing, 5–10 clear moves, no complex curves",
           "First three primitives placed, each born at the origin and moved from there",
           "At least one Boolean working, with the operands named",
           "Two useful inputs exposed, so a variant is one number away",
           "Operation history intact — nothing collapsed or applied"],
          closer="LEAVE WITH A GRAPH YOU CAN CHANGE, NOT A MESH YOU CANNOT.",
          bg=LIME)

# 10 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("WATCH", "U03 — Geometry from scratch. Point, line, edge, face, mesh, solid. The Blender lesson "
              "file for this one already exists; check the unit page."),
    ("BUILD", "Keep going on P1a. It is due Week 4 — eight or nine numbered diagrams, the last one "
              "developed in context, and the sequence written out as pseudocode."),
    ("WRITE", "Your procedure as pseudocode, using the notation above. Read it aloud to someone who "
              "has not seen your model and fix what they cannot follow."),
    ("BRING", "The editable file, and one question about something in it that behaves oddly."),
    ("READ", "Di Mari and Yoo, Operative Design, and Di Mari, Conditional Design. Find the spatial "
             "verb your own sequence performs, and name it on the sheet."),
])

d.save(os.path.join(OUT, "ARC3133_Class02.pptx"))
print("class02 ok — %d slides" % len(d.prs.slides._sldIdLst))
