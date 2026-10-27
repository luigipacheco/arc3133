# -*- coding: utf-8 -*-
"""Class 08 — Supported practice (Arrays 1 and 2). No new topic; nothing due today.
Everything through Arrays is uploaded on the Sunday that follows."""
import os
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(8)
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 8
DL = C.COURSE["midterm_week"]                       # the week whose Sunday closes the upload
DUE = sorted(C.milestones_due(DL), key=lambda m: m["id"])
WHEN = C.due_label(DUE[0]["id"]).upper()            # 'SUN OCT 18, 11:59 PM'

# 1 ── TITLE
title_slide(d, WK, ["SUPPORTED", "PRACTICE"],
            "ARRAYS 1 AND 2. NO NEW TOPIC. FIX IT BEFORE SUNDAY.",
            bg=YELLOW, lfill=CYAN, rfill=PINK,
            foot="UPLOAD CLOSES " + WHEN)

# 2 ── WHAT THIS CLASS IS FOR
s = d.slide(BLACK)
s.header("WHAT THIS CLASS IS FOR",
         "A working session. Every sheet you bring gets looked at; nothing new is taught.")
cols = [("BRING", CYAN, ["All three array sheets: repetition, conditional patterns, application",
                         "Anything still open from 1, 2.1, 2.2 and 3.1",
                         "The editable files, not screenshots of them"]),
        ("WE CHECK", LIME, ["Loops, counts and spacing in the 1D, 2D and 3D arrays",
                            "if/Switch patterns in 2D, then the same rules in 3D",
                            "That the module resizes to its cell when counts and spacing change"]),
        ("YOU LEAVE WITH", PINK, ["A list of what to fix, in order",
                                  "Captions that name the rule in plain words",
                                  "Files that reopen and reproduce every sheet"])]
x = L
wd = (W - 0.46) / 3
for tag, col, rows in cols:
    s.panel(x, 2.0, wd, 3.6, tag, headfill=col)
    s.t(x + 0.28, 2.75, wd - 0.56, 2.7, [s.Cb("·  " + r, 13) for r in rows], ls=1.5)
    x += wd + 0.23
s.banner(5.95, "SMALL COUNTS FIRST. A PATTERN YOU CANNOT CHECK BY EYE IS NOT CHECKED.",
         fill=YELLOW, h=0.68, align=PP_ALIGN.CENTER)

# 3 ── THE CHECKLIST
now_slide(d, "CHECK EVERY LINE BEFORE YOU UPLOAD",
          "Open each file cold. If a step below fails, that is what to fix today.",
          ["Change a count or a spacing: every array rebuilds, the module fits its cell, totals stay right",
           "Each of the four patterns names its rule and what happens when it is true and false",
           "One modulo rule and one index-driven parameter change are among the four",
           "The application reads as one object, with a view that explains module and pattern",
           "Materials noted, textures packed, and the file reopens showing exactly the sheets"],
          closer="IF YOU HAVE TO MOVE SOMETHING BY HAND AFTER CHANGING A COUNT, IT IS NOT PARAMETRIC YET.",
          bg=CYAN)

# 4 ── THE UPLOAD
s = d.slide(CREAM)
s.header("THE MID-SEMESTER UPLOAD",
         "Everything through Arrays, in one upload, by %s. This is the record for the midterm grade." % WHEN.title())
y = 1.95
for i, m in enumerate(DUE):
    col = ACCENTS[i % len(ACCENTS)]
    s.chip(L, y, 1.3, 0.62, m["id"], fill=col, size=13)
    s.card(L + 1.55, y, W - 1.55, 0.62, fill=CREAM)
    s.t(L + 1.85, y, 7.6, 0.62, [s.Cb(m["title"], 13.5)], anchor=MSO_ANCHOR.MIDDLE)
    s.t(L + W - 2.9, y, 2.6, 0.62, [s.Ab("%d%%" % m["weight"], 13.5)], anchor=MSO_ANCHOR.MIDDLE,
        align=PP_ALIGN.RIGHT)
    y += 0.78
s.banner(min(y + 0.15, 6.4), "NOTHING IS DUE TODAY. SUNDAY IS THE DEADLINE, NOT A SUGGESTION.",
         fill=PINK, h=0.66, align=PP_ALIGN.CENTER)

# 5 ── BEFORE NEXT CLASS
rel = sorted(m["id"] for m in C.milestones_released(9))
before_next_slide(d, [
    ("UPLOAD", "%s. Everything through Arrays. After that the midterm grade is computed from what is in." % WHEN.title()),
    ("NEXT", "%s: Attractors. Distance replaces the index as the rule. %s issued."
             % (C.date_long(9).title(), " and ".join(rel))),
    ("PANEL", "Bring your 3.1 panel as a node group with one parameter exposed. Next week an attractor drives it."),
    ("FILES", "Save a copy of the uploaded files before you keep working. The upload is the record."),
])

d.save(os.path.join(OUT, "ARC3133_Class08.pptx"))
print("class08 ok — %d slides" % len(d.prs.slides._sldIdLst))
