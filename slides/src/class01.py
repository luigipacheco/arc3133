# -*- coding: utf-8 -*-
"""Class 01 — Visual identity and course introduction (U01)."""
import os
from nb import *
from slidekit import *
import coursedata as C
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 1

# 1 ── TITLE
title_slide(d, WK, ["ARC 3133", "VISUAL IDENTITY"],
            "HOW THE WORK WILL LOOK, BEFORE THERE IS ANY WORK",
            bg=LIME, right_tag="NOTHING DUE", foot="GSM ISSUED TODAY")

# 2 ── WHAT THIS COURSE IS
s = d.slide(BLACK)
s.header("WHAT THIS COURSE IS",
         "Computational methods for architectural representation and digital fabrication.")
s.panel(L, 2.05, 6.2, 3.3, "WHAT YOU WILL DO", headfill=LIME)
s.t(L + 0.35, 2.8, 5.5, 2.4, [
    s.Cb("Set your own graphic standards.", 14.5),
    s.Cb("Describe geometry with parameters.", 14.5),
    s.Cb("Repeat it, and vary it.", 14.5),
    s.Cb("Work with sampled and volumetric data.", 14.5),
    s.Cb("Turn all of it into drawings and physical parts.", 14.5)], ls=1.45)
s.panel(7.15, 2.05, 5.5, 3.3, "WHAT CARRIES THROUGH", headfill=CYAN)
s.t(7.45, 2.8, 4.9, 2.4, [
    s.Cb("Visual quality stays central all semester — composition, hierarchy, line weight, "
         "colour, rendering, photography.", 14),
    s.Cb(" ", 7),
    s.Cb("A working graph supports those decisions. It does not replace them.", 14)], ls=1.3)
s.banner(5.7, "EACH PROJECT CARRIES ITS GEOMETRY INTO THE NEXT. YOU NEVER START FROM AN UNRELATED OBJECT.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 3 ── THREE PARADIGMS
s = d.slide(CREAM)
s.header("THREE PARADIGMS", "Each one a strict extension of the one before it.")
para = [("01", "PROCEDURAL", CYAN, "Form as a fixed sequence of operations. You define the steps.",
         "Output is expected."),
        ("02", "PARAMETRIC", LIME, "Relationships between inputs and form. You define the rules of variation.",
         "Output is a family — you know the range, not each member."),
        ("03", "GENERATIVE", PINK, "A rule applied to its own output, repeatedly. You define the rule and the starting state.",
         "Output is unknown, within a spectrum you set.")]
x = L
for n, nm, col, body, out in para:
    s.chip(x, 1.95, 3.85, 0.5, n + "   " + nm, fill=col, size=13)
    s.card(x, 2.55, 3.85, 2.85, fill=CREAM)
    s.t(x + 0.28, 2.8, 3.3, 1.5, [s.Cb(body, 13.5)], ls=1.3)
    s.rule(x + 0.28, 4.45, 3.3, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.28, 4.62, 3.3, 0.7, [s.Cb(out, 12.5, bold=True)], ls=1.25)
    x += 4.08
s.banner(5.75, "A procedure is a fixed recipe. A parametric system is a recipe with dials. "
              "A generative system reads its own output and decides what to do next.",
         fill=CYAN, h=0.72)

# 4 ── FOUR PROJECTS
s = d.slide(CREAM)
s.header("FOUR PROJECTS", "Ten short assignments, assembled into four. Nothing is graded twice.")
y = 2.0
for i, pid in enumerate(["P1", "P2", "P3", "P4"]):
    p = C.PROJECTS[pid]
    ms = p["milestones"]
    total = sum(m.get("weight", 0) for m in ms)
    col = ACCENTS[i % 4]
    s.chip(L, y, 1.15, 1.0, pid, fill=col, size=19)
    s.card(L + 1.45, y, W - 1.45, 1.0, fill=CREAM)
    s.t(L + 1.75, y + 0.13, W - 3.6, 0.35, [s.Ab(p["title"], 14)])
    s.t(L + 1.75, y + 0.55, W - 3.6, 0.35,
        [s.Cb("  →  ".join(m["title"] for m in ms), 12)])
    s.t(W - 1.3, y, 1.6, 1.0, [s.Ab("%d%%" % total, 17)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    y += 1.15
s.banner(6.7, "You do the short assignment, then revise it inside its project. "
              "The project itself adds no second grade — the revision is what the booklet rewards.",
         fill=LIME, h=0.62, size=12)

# 5 ── HOW A CLASS RUNS
s = d.slide(BLACK)
s.header("HOW A CLASS RUNS", "The same four things, every week.")
steps_ = [("01", "REVIEW OF WORK", "We open the files. Bring the editable file, not a screenshot of it."),
          ("02", "DEMONSTRATION", "A short tutorial or discussion of the week's unit."),
          ("03", "GUIDED PRACTICE", "You build the small exercise while help is in the room."),
          ("04", "WORKING CRITIQUE", "We look at what is on screen and say what it needs.")]
y = 2.05
for n, ttl, body in steps_:
    s.chip(L, y, 0.85, 0.9, n, fill=CYAN, size=17)
    s.card(L + 1.15, y, W - 1.15, 0.9, fill=CREAM)
    s.t(L + 1.45, y + 0.12, W - 1.75, 0.33, [s.Ab(ttl, 13.5)])
    s.t(L + 1.45, y + 0.48, W - 1.75, 0.33, [s.Cb(body, 12.5)])
    y += 1.05
s.banner(6.35, "YOU WILL BE ASKED TO CHANGE ONE PARAMETER AND PREDICT WHAT HAPPENS. FROM THE FIRST REVIEW.",
         fill=PINK, h=0.62, size=12.5)

# 6 ── WHY IDENTITY FIRST
s = d.slide(CREAM)
s.header("WHY THIS COMES FIRST",
         "Every sheet you make for the next fifteen weeks uses the system you build now.")
s.panel(L, 1.95, 6.0, 3.4, "A DRAWING IS READ BEFORE IT IS UNDERSTOOD", headfill=PINK, tsize=14)
s.t(L + 0.35, 2.72, 5.3, 2.4, [
    s.Cb("Hierarchy is what makes an architectural drawing legible — not detail, and not effort.", 14),
    s.Cb(" ", 7),
    s.Cb("Line weight, spacing and restraint do more work than anything you will model this semester. "
         "A good system makes weak work readable. A bad one hides good work.", 14)], ls=1.3)
s.panel(7.0, 1.95, 5.65, 3.4, "WHAT A SYSTEM IS", headfill=LIME, tsize=14.5)
s.t(7.3, 2.72, 5.05, 2.4, [
    s.Cb("Page size and margins.", 14),
    s.Cb("A column grid.", 14),
    s.Cb("A type hierarchy — three levels, no more.", 14),
    s.Cb("A line-weight set — four weights.", 14),
    s.Cb("A palette of three colours, and the black is one of them.", 14),
    s.Cb("Three typefaces is the ceiling. Two is better.", 14)], ls=1.4)
s.banner(5.65, "DECIDE IT ONCE, APPLY IT EVERY WEEK, REVISE IT AT THE MIDTERM. IT IS NOT REMADE PER SHEET.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

# 7 ── THE PRECEDENTS
s = d.slide(CREAM)
s.header("THREE MANUALS WORTH STEALING FROM",
         "This document type has a history. Each one is a page grid, a type hierarchy, "
         "and a rule for every case that comes up.")
mans = [("NYCTA GRAPHICS STANDARDS", CYAN,
         "Massimo Vignelli and Bob Noorda, Unimark - 1970 - archive.org/details/nycta-gs-manual",
         "A binder of cases. Every sign in the New York subway, drawn at size, with the rule "
         "beside it. The manual is the design - the signs are what falls out of it.",
         "Add: a spread from the NYCTA manual - a signage case with its dimensioned rule."),
        ("NASA GRAPHICS STANDARDS", PINK,
         "Richard Danne and Bruce Blackburn - 1975 - archive.org/details/NASA_Graphics_Standards_Manual",
         "One mark, and a hundred pages of where it is allowed to go. What is being designed "
         "is the consistency, not the logotype.",
         "Add: a page from the NASA manual - the mark with its clearance and placement rules."),
        ("MUNICH 1972", LIME,
         "Otl Aicher - 1967 to 1972 - otlaicher.de, 'the rainbow games'",
         "A grid, a fixed set of angles, and one component varied across a whole field of "
         "pictograms. You will build a system with this exact structure in Week 4.",
         "Add: the Munich 1972 pictogram sheet, and the construction grid behind one figure.")]
x = L
for nm, col, credit, body, placeholder in mans:
    s.card(x, 1.95, 3.85, 1.9, fill=PAPER)
    s.t(x + 0.3, 1.95, 3.25, 1.9, [s.Cb(placeholder, 11.5, GREY)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    s.chip(x, 3.95, 3.85, 0.48, nm, fill=col, size=11)
    s.t(x + 0.05, 4.58, 3.75, 0.28, [s.Cb(credit, 10.5, GREY)])
    s.t(x + 0.05, 4.95, 3.75, 1.15, [s.Cb(body, 12.5)], ls=1.3)
    x += 4.08
s.banner(6.2, "YOURS IS FOUR PAGES, NOT THREE HUNDRED. THE PRINCIPLE IS IDENTICAL: "
              "DECIDE ONCE, WRITE IT DOWN, APPLY IT EVERY TIME.",
         fill=BLACK, color=CYAN, h=0.65, size=12, align=PP_ALIGN.CENTER)
s.t(L, 7.0, W, 0.3, [s.C("All three are online in full, linked on the U01 lesson page and under "
                         "Reading. Look at how much of each one is rules rather than pictures.", 12, GREY)])

pseudocode_slide(d, "U01", title="A VISUAL IDENTITY IS A PARAMETER SET",
                 sub="A short list of values, decided once. Every sheet this semester reads them.",
                 note="A BINDER OF RULES AND THIS SHORT LIST ARE THE SAME DOCUMENT, AT DIFFERENT SCALES.",
                 note_fill=CYAN)

# 8 ── ISSUED TODAY — GSM
issued_slide(d, "GSM",
             blurb="Build the graphic system you will communicate every later project with. "
                   "It is the only assignment in the course that does not require a computational graph — "
                   "it is judged purely on whether the system works and whether you used it.",
             badgefill=CYAN,
             cards=[("DECIDE", "THE SYSTEM", "Grid, margins, type, line weights, colour. Written down, not improvised."),
                    ("TEST", "ON REAL WORK", "A diagram and a rendered image, made with the rules you just set."),
                    ("REVISE", "ALL SEMESTER", "Due at the midterm, revised again for the booklet.")])

# 8 ── REQUIREMENTS
requirements_slide(d, "GSM",
                   sub="Assessed on visual quality and hierarchy 40%, consistency and usability 30%, "
                       "tested applications 20%, completeness 10%.")

# 9 ── NOW
now_slide(d, "NOW — YOUR FIRST SHEET",
          "Rest of the session: set the page up and put something on it.",
          ["Page size set to 17 × 11 inches, with margins and a column grid",
           "Type hierarchy chosen — three levels, and a reason for each",
           "A line-weight set, from hairline to heaviest — four weights",
           "Three colours you can defend, black included, that survive being printed",
           "One sample sheet, with one decision about hierarchy you can explain"],
          closer="LEAVE WITH A SHEET. IT DOES NOT HAVE TO BE RIGHT YET.",
          bg=CYAN)

# 10 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("WATCH", "U02 — Transformations and CSG. The node editor, parameters, and the three Boolean "
              "operations. Check the unit page; watch a recording only once a link is posted."),
    ("INSTALL", "Blender, and set up a project folder you can open from a clean machine. "
                "File organization is part of the workflow, not an afterthought."),
    ("BRING", "Your sample sheet and the file it came from."),
    ("LOOK", "Three architectural drawings you think are well made. Be ready to say what makes "
             "each one readable."),
])

d.save(os.path.join(OUT, "ARC3133_Class01.pptx"))
print("class01 ok — %d slides" % len(d.prs.slides._sldIdLst))
