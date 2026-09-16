# -*- coding: utf-8 -*-
"""Class 07 — Arrays: hexagonal, radial, curve (U04, Week 7 steps). P3b sheet 2.
Studio-review week: nothing due."""
import os, math
from nb import *
from slidekit import *
import coursedata as C
import diagrams as G
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 7
VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")


def sine_pts(x, y, w, amp, freq, phase, n):
    """n points on y = amp·sin(2π·freq·t + phase), t in 0..1, slide coordinates (y down)."""
    out = []
    for k in range(n):
        t = k / (n - 1.0)
        a = 2 * math.pi * freq * t + phase
        out.append((x + t * w, y - amp * math.sin(a),
                    -amp * 2 * math.pi * freq * math.cos(a) / w))  # slope dy/dx
    return out


def sine_line(s, x, y, w, amp, freq, phase, col=MUTE, d=0.03, n=70):
    for px, py, _ in sine_pts(x, y, w, amp, freq, phase, n):
        s.dot(px, py, d=d, fill=col)


def curve_array(s, x, y, w, amp, freq, phase, n, size=0.2, col=YELLOW):
    sine_line(s, x, y, w, amp, freq, phase)
    for px, py, m in sine_pts(x, y, w, amp, freq, phase, n):
        sh = s.rect(px - size / 2, py - size / 2, size, size, fill=col, line=BLACK, lw=HAIR)
        sh.rotation = math.degrees(math.atan(m))


# 1 ── TITLE
title_slide(d, WK, ["ARRAYS", "HEX · RADIAL · CURVE"],
            "P3b SHEET 2 — STAGGER IT, SPIN IT, BEND IT", bg=PINK, lfill=CYAN, rfill=YELLOW,
            foot="STUDIO-REVIEW WEEK — NOTHING DUE TODAY  /  P3b " + C.due_line("P3b").upper())

# 2 ── THREE ARRANGEMENTS
s = d.slide(CREAM)
s.header("SHEET 2: THREE MORE RULES",
         "Same module. Three new rules for turning an index into a position.")
CY = 1.95
x = L
for nm, col, sub in [("HEXAGONAL", YELLOW, "stagger alternate rows"),
                     ("RADIAL", PINK, "radius, count, angular step"),
                     ("CURVE", CYAN, "resample, place, align")]:
    s.panel(x, CY, 3.85, 3.5, nm, headfill=col, tsize=15)
    s.t(x + 0.25, CY + 2.9, 3.35, 0.45, [s.Mb(sub, 11)], align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE)
    x += 4.08
G.hexagonal(s, L + 0.95, CY + 0.9, cols=7, rows=5, p=0.34)
G.radial(s, L + 4.08 + 1.92, CY + 1.72, rings=(0.36, 0.66, 0.96), n=12, d=0.1)
curve_array(s, L + 8.16 + 0.45, CY + 1.72, 2.95, 0.55, 1.0, 0.0, 9, size=0.2)
s.banner(5.75, "Sheet 1 counted along axes. Sheet 2 keeps the counter and changes the rule that "
              "turns it into a position.", fill=LIME, h=0.72)

# 3 ── HEXAGONAL
s = d.slide(BLACK)
s.header("HEXAGONAL IS A GRID WITH AN ODD/EVEN TEST",
         "Stagger alternate rows by half the spacing. Set the row spacing on its own.")
s.panel(L, 2.05, 6.2, 3.35, "THE TEST", headfill=LIME)
s.t(L + 0.35, 2.8, 5.5, 2.3, [
    s.Mb("offset = (j mod 2 == 0) ? 0 : dx / 2", 12.5, bold=True),
    s.Mb(" ", 8),
    s.Cb("Modulo asks: is this row odd or even? Compare turns that into True or False, and "
         "Switch picks the offset. The same two nodes as last week.", 13.5),
    s.Cb(" ", 6),
    s.Cb("Row spacing is not dx. For a true hex field it is dx × √3 / 2. Use dx for both and "
         "you get a squashed grid.", 13.5)], ls=1.3)
s.panel(7.15, 2.05, 5.5, 3.35, "WHAT IT LOOKS LIKE", headfill=CYAN)
G.hexagonal(s, 7.95, 2.95, cols=7, rows=6, p=0.4, d=0.13)
s.banner(5.75, "A BRICK BOND IS A STAGGERED ARRAY. SO IS A HONEYCOMB. SO IS HALF THE PAVING YOU WALK ON.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 4 ── RADIAL
s = d.slide(CREAM)
s.header("RADIAL IS POLAR ARITHMETIC", "Radius, count, angular step. The index drives the angle.")
s.panel(L, 1.95, 6.0, 3.5, "THE RULE", headfill=PINK)
s.t(L + 0.35, 2.7, 5.3, 2.4, [
    s.Mb("step  = 360 / count", 12.5),
    s.Mb("θ[i]  = i × step", 12.5),
    s.Mb("p[i]  = c + r · (cos θ, sin θ)", 12.5, bold=True),
    s.Mb(" ", 8),
    s.Cb("The rotation arithmetic from Week 2 — where x and y have to talk to each other — "
         "now generating positions instead of moving a solid.", 13.5)], ls=1.3)
s.panel(7.0, 1.95, 5.65, 3.5, "THREE KNOBS", headfill=LIME, tsize=14.5)
G.radial(s, 9.85, 3.6, rings=(0.36, 0.66, 0.96), n=12, d=0.10)
s.t(7.3, 4.75, 5.05, 0.6, [s.Cb("Change the count and the step changes with it. "
                                "Change the radius and the ring opens up.", 13)], ls=1.25)
s.banner(5.65, "IF YOUR LAST COPY LANDS ON TOP OF YOUR FIRST, YOU DIVIDED BY THE WRONG NUMBER.",
         fill=CYAN, h=0.72, align=PP_ALIGN.CENTER)

# 5 ── CURVE ARRAY
s = d.slide(BLACK)
s.header("AN ARRAY ALONG A CURVE",
         "The curve supplies the positions. Its tangent supplies the direction.")
s.panel(L, 2.05, 5.2, 3.5, "THREE STEPS", headfill=CYAN)
steps3 = [("01", "RESAMPLE", "Divide the curve into a count of evenly spaced points."),
          ("02", "PLACE", "Put one copy of the module on each point."),
          ("03", "ALIGN", "Rotate each copy to the curve's tangent at that point.")]
yy = 2.8
for n, nm, body in steps3:
    s.chip(L + 0.3, yy, 0.6, 0.6, n, fill=[LIME, YELLOW, PINK][int(n) - 1], size=12, shadow=False)
    s.t(L + 1.1, yy - 0.02, 3.9, 0.3, [s.Ab(nm, 12.5)])
    s.t(L + 1.1, yy + 0.28, 3.9, 0.5, [s.Cb(body, 12.5)], ls=1.15)
    yy += 0.88
s.panel(6.1, 2.05, 6.55, 3.5, "NOT ALIGNED  ·  ALIGNED", headfill=YELLOW)
for py, aligned in [(3.25, False), (4.65, True)]:
    sine_line(s, 6.6, py, 5.5, 0.4, 1.0, 0.0)
    for px, qy, m in sine_pts(6.6, py, 5.5, 0.4, 1.0, 0.0, 11):
        sh = s.rect(px - 0.11, qy - 0.11, 0.22, 0.22, fill=LIME if aligned else MUTE,
                    line=BLACK, lw=HAIR)
        if aligned:
            sh.rotation = math.degrees(math.atan(m))
s.banner(5.9, "WITHOUT THE TANGENT, EVERY COPY FACES THE SAME WAY. WITH IT, THE ROW FOLLOWS THE CURVE.",
         fill=PINK, h=0.7, align=PP_ALIGN.CENTER)

# 6 ── SINE-DRIVEN CURVE
s = d.slide(CREAM)
s.header("DRIVE THE CURVE WITH SINE",
         "Three words describe the whole curve. Sheet 2 asks you to label all three.")
s.panel(L, 1.95, 5.3, 3.75, "THREE PARAMETERS", headfill=CYAN)
tri = [("AMPLITUDE", "how far it swings"),
       ("FREQUENCY", "how many swings along the curve"),
       ("PHASE", "where in the swing it starts")]
yy = 2.75
for nm, body in tri:
    s.chip(L + 0.3, yy, 1.9, 0.52, nm, fill=LIME, size=11, shadow=False)
    s.t(L + 2.4, yy, 2.7, 0.52, [s.Cb(body, 13)], anchor=MSO_ANCHOR.MIDDLE)
    yy += 0.7
s.t(L + 0.3, 4.95, 4.8, 0.5, [s.Mb("y = amplitude × sin(x × frequency + phase)", 11, bold=True)])
s.panel(6.2, 1.95, 6.45, 3.75, "CHANGE ONE AT A TIME", headfill=YELLOW)
variants = [("AMPLITUDE ×2", 0.36, 1.0, 0.0),
            ("FREQUENCY ×2", 0.18, 2.0, 0.0),
            ("PHASE + 90°", 0.18, 1.0, math.pi / 2)]
yy = 2.95
for lab, amp, fr, ph in variants:
    s.t(6.45, yy - 0.15, 1.75, 0.3, [s.Ab(lab, 10.5)])
    sine_line(s, 8.3, yy, 4.0, 0.18, 1.0, 0.0, col=MUTE, d=0.03)
    for px, py, _ in sine_pts(8.3, yy, 4.0, amp, fr, ph, 15):
        s.dot(px, py, d=0.1, fill=PINK)
    yy += 0.92
s.t(6.45, 5.3, 6.0, 0.3, [s.Cb("Grey: the base curve. Pink: one value changed.", 11.5, GREY)])
s.banner(6.0, "SET EACH VALUE ON PURPOSE AND WRITE IT ON THE SHEET. A SINE NOBODY CAN READ IS DECORATION.",
         fill=BLACK, color=YELLOW, h=0.68, align=PP_ALIGN.CENTER)

# 7 ── TWO WAYS TO REPEAT
s = d.slide(CREAM)
s.header("TWO WAYS TO REPEAT", "Worth being precise about, because they look alike and are not.")
s.panel(L, 1.95, 6.0, 3.4, "EXPLICIT ITERATION", headfill=PINK)
s.t(L + 0.35, 2.7, 5.3, 2.4, [
    s.Cb("A Repeat Zone runs a body once per step, in order, carrying a value forward.", 14),
    s.Cb(" ", 7),
    s.Cb("Use it when step n depends on step n − 1 — and when you want to watch the loop happen.", 14)], ls=1.3)
s.panel(7.0, 1.95, 5.65, 3.4, "PER-ELEMENT EVALUATION", headfill=CYAN)
s.t(7.3, 2.7, 5.05, 2.4, [
    s.Cb("A field is evaluated for every element at once. There is no order and no carry.", 14),
    s.Cb(" ", 7),
    s.Cb("It is usually faster — but nothing on screen tells you a loop happened, which is why "
         "we built the explicit one first. A field is not a Repeat Zone.", 14)], ls=1.3)
s.banner(5.65, "NEXT WEEK'S ATTRACTORS ARE MEASURED PER ELEMENT. KNOW WHICH KIND OF REPETITION YOU ARE USING.",
         fill=BLACK, color=CYAN, h=0.72, align=PP_ALIGN.CENTER, size=12)

# 8 ── THE SEQUENCE
unit_steps_slide(d, "U04", title="SHEET 2, STEP BY STEP", n=(4, 7),
                 sub="What we build together today: hexagonal, radial, curve.")

# 9 ── PSEUDOCODE
pseudocode_slide(d, "U04",
                 title="THE WHOLE UNIT, WRITTEN OUT",
                 sub="Last week you could read the loops. Today you can read all of it.",
                 note="j % 2 IS THE ODD/EVEN TEST · if IS COMPARE AND SWITCH · sin IS THE MATH NODE",
                 note_fill=CYAN)

# 10 ── REMINDER — P3b REQUIREMENTS
requirements_slide(d, "P3b", title="REMINDER — P3b REQUIREMENTS", sub=VISUAL)

# 11 ── NOW
now_slide(d, "NOW — SHEET 2",
          "Nothing is due today; this is a studio-review week. Use the class to build sheet 2.",
          ["Hexagonal array working, the odd/even test visible and row spacing set",
           "Radial array working from radius, count and angular step",
           "Your module placed along a resampled curve, aligned to its tangent",
           "A sine-driven curve, with amplitude, frequency and phase written down",
           "Sheet 1 reviewed at your desk — count, spacing, index order labelled"],
          closer="TWO SHEETS, ONE MODULE, SIX ARRAYS. NOTHING ELSE CHANGES.",
          bg=LIME)

# 12 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "Week 8: attractors — distance, a 2D grayscale field, remap, clamp and falloff; "
             "point, multi-point and curve attractors."),
    ("DUE", "P3b is due next class — both sheets, submitted together as one assignment. "
            + C.due_line("P3b") + "."),
    ("FINISH", "Sheet 2: hexagonal, radial and curve arrays, the sine values labelled. Check "
               "sheet 1 against the requirements again."),
    ("PRINT", "P2b — the printed object and its process sheet are due at the midterm, "
              + C.date_long(10) + ". If it is not queued yet, queue it now."),
])

d.save(os.path.join(OUT, "ARC3133_Class07.pptx"))
print("class07 ok — %d slides" % len(d.prs.slides._sldIdLst))
