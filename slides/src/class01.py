# -*- coding: utf-8 -*-
"""Class 01 — Graphic Standards Manual and course introduction (U01). GSM issued."""
import os
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(1)
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 1

# 1 ── TITLE
title_slide(d, WK, ["ARC 3133", "GRAPHIC STANDARDS MANUAL"],
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

# 4 ── FOUR PROJECTS, NINE ASSIGNMENTS
SHORT = {"GSM": "four-page manual", "P2a": "CSG process sheet", "P2b": "3D printed object",
         "P3a": "module sheet", "P3b": "arrays, two sheets", "P3c": "2D field drawing",
         "P3d": "layered site analysis", "P4a": "SDF volume", "P4b": "laser-cut slices"}
NAMES = {"P1": "GRAPHIC STANDARDS MANUAL", "P2": "CONSTRUCTIVE SOLID GEOMETRY",
         "P3": "PANELING", "P4": "VOLUMETRIC DATA"}


def due_short(m):
    return ("W%d" % m["due"]) if isinstance(m["due"], int) else str(m["due"]).upper()


s = d.slide(CREAM)
s.header("FOUR PROJECTS, NINE ASSIGNMENTS",
         "Each assignment is graded once. Each project carries its geometry into the next.")
y = 1.95
for i, pid in enumerate(["P1", "P2", "P3", "P4"]):
    p = C.PROJECTS[pid]
    ms = p["milestones"]
    total = sum(m.get("weight", 0) for m in ms)
    col = ACCENTS[i % 4]
    s.chip(L, y, 1.0, 0.92, pid, fill=col, size=19)
    s.card(L + 1.25, y, W - 1.25, 0.92, fill=CREAM)
    s.t(L + 1.5, y + 0.1, W - 3.2, 0.32, [s.Ab(NAMES[pid], 13.5)])
    line = []
    for k, m in enumerate(ms):
        gap = "    " if k < len(ms) - 1 else ""
        line += [s.Mb(m["id"], 11.5, bold=True),
                 s.Cb(" %s · due %s%s" % (SHORT[m["id"]], due_short(m), gap), 11.5)]
    s.t(L + 1.5, y + 0.48, W - 2.75, 0.34, [line])
    s.t(W - 0.95, y, 1.6, 0.92, [s.Ab("%d%%" % total, 17)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    y += 1.04
book, part = C.milestone("BOOK"), C.milestone("PART")
s.banner(6.22, "MID-SEMESTER DEADLINE · %s     FINAL BOOKLET · DUE %s · %d%%     "
               "PARTICIPATION · %d%%" % (C.date_long(C.COURSE["midterm_week"]).upper(),
                                         str(book["due"]).upper(), book["weight"], part["weight"]),
         fill=LIME, h=0.6, size=12, align=PP_ALIGN.CENTER)
s.t(L, 6.98, W, 0.3, [s.C("Everything through Arrays is due by Week 10. Later dates are provisional; "
                         "the course site is the reference for every due date.", 11.5, GREY)])

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
    s.Cb("A type hierarchy — four levels at most.", 14),
    s.Cb("A line-weight set — four weights at most.", 14),
    s.Cb("Three colours — black and paper count as two.", 14),
    s.Cb("Three typefaces is the ceiling. Two is better.", 14)], ls=1.4)
s.banner(5.65, "FOUR PAGES. DECIDE IT ONCE, APPLY IT EVERY WEEK, REVISE IT AFTER CRITIQUE. NOT REMADE PER SHEET.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

# 7 ── THE PRECEDENTS
s = d.slide(CREAM)
s.header("THREE MANUALS TO STUDY",
         "Each one is a set of rules, drawn out, and applied to real cases. Read them as systems.")
mans = [("NYCTA", "1970", CYAN, "GRAPHICS STANDARDS MANUAL",
         "A transit signage system."),
        ("NASA", "1975", PINK, "GRAPHICS STANDARDS MANUAL",
         "An agency identity manual."),
        ("MUNICH OLYMPICS", "1972", LIME, "DESIGN GUIDELINES",
         "An Olympic identity system.")]
x = L
for nm, yr, col, kind, body in mans:
    s.chip(x, 1.95, 3.85, 0.5, "%s  ·  %s" % (nm, yr), fill=col, size=13)
    s.card(x, 2.55, 3.85, 2.55, fill=CREAM)
    s.t(x + 0.28, 2.75, 3.3, 0.3, [s.Ab(kind, 11.5, GREY)])
    s.t(x + 0.28, 3.12, 3.3, 0.4, [s.Cb(body, 15, bold=True)])
    s.rule(x + 0.28, 3.72, 3.3, lw=Pt(1.5), color=MUTE)
    s.t(x + 0.28, 3.88, 3.3, 1.1, [s.Cb("Find one rule.", 12.5),
                                   s.Cb("Find the drawing that dimensions it.", 12.5),
                                   s.Cb("Find where it is applied.", 12.5)], ls=1.3)
    x += 4.08
s.banner(5.45, "YOUR TASK: PICK ONE RULE FROM ONE MANUAL. ADOPT IT IN YOUR GSM, AND NAME IT ON THE PAGE "
              "WHERE YOU USE IT.", fill=BLACK, color=CYAN, h=0.72, size=12.5, align=PP_ALIGN.CENTER)
s.t(L, 6.45, W, 0.6, [s.C("All three are linked in full under Reading and documentation. Notice how much "
                          "of each one is rules rather than pictures. Yours is four pages; the "
                          "principle is the same.", 13, GREY)], ls=1.25)

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
                    ("REVISE", "ALL SEMESTER", "Due Week 10, revised again for the booklet.")])

# 8 ── REQUIREMENTS
requirements_slide(d, "GSM",
                   sub="Assessed on visual quality and hierarchy 40%, consistency and usability 30%, "
                       "tested applications 20%, completeness 10%.")

# 9 ── NOW
now_slide(d, "NOW — YOUR FIRST SHEET",
          "Rest of the class: set the page up and put something on it.",
          ["Page size set to 17 × 11 inches, with margins and a column grid",
           "Type hierarchy chosen — up to four levels, and a reason for each",
           "A line-weight set, from hairline to heaviest — four weights at most",
           "Three colours you can defend, black and paper included, that survive printing",
           "One sample sheet, with one decision about hierarchy you can explain"],
          closer="LEAVE WITH A SHEET. IT DOES NOT HAVE TO BE RIGHT YET.",
          bg=CYAN)

# 10 ── BEFORE NEXT CLASS
gsm_cp = C.checkpoints("GSM")[0]
before_next_slide(d, [
    ("WATCH", "U02 — Constructive Solid Geometry. Nodes, parameters, transformations and the three "
              "Boolean operations. Watch the CSG video tutorial (Blender or Rhino + Grasshopper) linked on the Class 02 page."),
    ("INSTALL", "Blender, and a project folder you can open from a clean machine. "
                "File organization is part of the workflow, not an afterthought."),
    ("BRING", "Your sample sheet and the file it came from. The sheet gets an ungraded "
              "identity check next class (%s)." % C.date_long(gsm_cp[0])),
    ("PLAN", "GSM is due at the mid-semester deadline, %s. Study the three manuals and pick your rule "
             "before you lay out page 1." % C.date_long(C.milestone("GSM")["due"])),
])

d.save(os.path.join(OUT, "ARC3133_Class01.pptx"))
print("class01 ok — %d slides" % len(d.prs.slides._sldIdLst))
