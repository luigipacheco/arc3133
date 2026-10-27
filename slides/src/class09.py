# -*- coding: utf-8 -*-
"""Class 09 — Attractors (U05). Three field studies (3.4) and the architectural application (3.5) issued.
The midterm upload closed on Sunday; nothing is due today."""
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

VISUAL = ("Visual quality 35% · computational understanding 25% · technical execution 20% "
          "· experimentation 10% · requirements and identity 10%.")

# 1 ── TITLE
title_slide(d, WK, ["ATTRACTORS"],
            "P3 CONTINUES: THE RULE STOPS COMING FROM THE INDEX",
            bg=CYAN, lfill=PINK, rfill=LIME, right_tag="MIDTERM UPLOAD CLOSED")

# 2 ── AN ATTRACTOR IS A NUMBER
s = d.slide(BLACK)
s.header("AN ATTRACTOR IS A NUMBER",
         "For every panel: how far is it from something? Use that number to drive a parameter.")
s.panel(L, 2.05, 6.2, 3.3, "THE WHOLE IDEA", headfill=LIME)
s.t(L + 0.4, 2.85, 5.4, 2.2, [
    s.Mb("for each panel p:", 15),
    s.Mb("    d = distance(p, a)", 15),
    s.Mb("    value = f(d)", 15),
    s.Mb(" ", 8),
    s.Mb("Everything else this week", 13.5),
    s.Mb("is a choice of f.", 13.5)], ls=1.35)
s.panel(7.15, 2.05, 5.5, 3.3, "MEASURE IT FIRST", headfill=CYAN)
s.t(7.45, 2.85, 4.9, 2.2, [
    s.Mb("d = √((px − ax)² + (py − ay)²)", 13),
    s.Cb(" ", 6),
    s.Cb("Pythagoras, once per panel. The answer is in model units.", 14),
    s.Cb(" ", 6),
    s.Cb("Index told you where in the sequence. Distance tells you how far from something "
         "outside the collection.", 14)], ls=1.3)
s.banner(5.7, "IN ARRAYS YOU BUILT THE POSITIONS. NOW YOU MEASURE THEM.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 3 ── READ THE FIELD FIRST
s = d.slide(BLACK)
s.header("READ THE FIELD BEFORE YOU CHANGE ANYTHING",
         "Distance is a value at every location. Look at it as grey before it becomes geometry.")
seq = [("01", "MEASURE", "Every location on the facade grid gets a number: how far to the attractor.", CYAN),
       ("02", "DISPLAY", "Show those numbers as grey. This is a diagram already.", LIME),
       ("03", "REMAP", "Push that range into the range your parameter needs.", YELLOW),
       ("04", "DRIVE", "Only now does the panel change. The field was finished first.", PINK)]
x = L
for n, ttl, body, col in seq:
    s.chip(x, 2.0, 2.85, 0.5, n + "   " + ttl, fill=col, size=12)
    s.card(x, 2.6, 2.85, 1.5, fill=CREAM)
    s.t(x + 0.25, 2.6, 2.35, 1.5, [s.Cb(body, 13)], ls=1.3, anchor=MSO_ANCHOR.MIDDLE)
    x += 3.05
s.t(L, 4.45, W, 0.3, [s.A("THE FIELD, READ AS A GREY VALUE ACROSS THE FACADE   ·   NEAR → FAR", 11, MUTE)])
G.gray_ramp(s, L, 4.78, W, 0.5)
s.banner(5.62, "IF THE GREY IMAGE IS NOT ALREADY A GOOD DIAGRAM, THE PANEL WILL NOT SAVE IT.",
         fill=CYAN, h=0.68, align=PP_ALIGN.CENTER)
s.t(L, 6.55, W, 0.4, [s.C("3.4 shows the attractors and the resulting variation side by side, "
                          "with the parameter labelled. That order is the assignment.", 13.5, MUTE)])

# 4 ── REMAP AND CLAMP
s = d.slide(CREAM)
s.header("REMAP, AND SAY WHERE YOU CLAMPED",
         "Distance comes out in model units. Your parameter needs a specific range.")
s.panel(L, 1.95, 6.0, 3.4, "THE OPERATION", headfill=CYAN)
s.t(L + 0.35, 2.7, 5.3, 2.3, [
    s.Mb("t   = (d − dmin) / (dmax − dmin)", 13),
    s.Mb("t   = clamp(t, 0, 1)", 13),
    s.Mb("out = outmin + t × (outmax − outmin)", 13),
    s.Mb(" ", 8),
    s.Mb("d    0 … 4 units        ← input", 13),
    s.Mb("out  0.85 … 0.15 opening ← output", 13)], ls=1.4)
s.panel(7.0, 1.95, 5.65, 3.4, "SUBTRACT. DIVIDE. MULTIPLY. ADD.", headfill=LIME, tsize=14)
s.t(7.3, 2.7, 5.05, 2.3, [
    s.Cb("Nothing here is new. It is the arithmetic of a transformation, applied to a distance "
         "instead of a coordinate.", 14),
    s.Cb(" ", 7),
    s.Cb("Clamping is a decision, not a safety net. Decide what happens past the end of your "
         "range and say so. Swap the two output values and the pattern inverts.", 14)], ls=1.3)
s.banner(5.65, "3.4 LABELS THE PARAMETER AND SAYS, IN PLAIN WORDS, HOW DISTANCE CHANGES IT.",
         fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)

# 5 ── FALLOFF + THREE KINDS
s = d.slide(CREAM)
s.header("FALLOFF, AND WHAT YOU MEASURE TO",
         "f shapes the result. The attractor type changes only what the distance is measured to.")
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
s.banner(6.45, "SAME FACADE, SAME PANEL, SAME PARAMETER, THREE ATTRACTORS: 3.4 SHOWS WHAT THE ATTRACTOR ALONE CHANGES.",
         fill=BLACK, color=YELLOW, h=0.6, size=12, align=PP_ALIGN.CENTER)

# 6 ── THE SAME THING, WRITTEN OUT
pseudocode_slide(d, "U05",
                 sub="Measure, remap, clamp, shape the falloff, then drive one parameter. In that order.",
                 note="LINE 2 IS THE ONLY LINE THAT CHANGES BETWEEN THE THREE ATTRACTOR TYPES.")

# 7 ── THE NUMBER DRIVES YOUR PANEL
s = d.slide(BLACK)
s.header("THE NUMBER DRIVES YOUR 3.1 PANEL",
         "Not a sphere, not a cube. The panel you already built, rebuilt at every location with a different input.")
cards = [("MEASURE", CYAN, "Distance from each facade location to the attractor. Object Info, set to Relative, "
                           "so the attractor and the facade share one coordinate system."),
         ("REMAP", LIME, "One Map Range, Float, Linear, Clamp on. Input 0 to the reach of the attractor. "
                         "Output: the safe range of your parameter, in its own units."),
         ("DRIVE", PINK, "Instance on Points repeats a thing that is already built. To rebuild the panel "
                         "per location with its own Opening, Depth or Height, the value goes into "
                         "a For Each Element zone and reaches the panel's input inside it.")]
x = L
wd = (W - 0.46) / 3
for i, (tag, col, body) in enumerate(cards):
    s.chip(x, 2.0, wd, 0.5, "%02d   %s" % (i + 1, tag), fill=col, size=12)
    s.card(x, 2.6, wd, 2.55, fill=CREAM)
    s.t(x + 0.28, 2.75, wd - 0.56, 2.3, [s.Cb(body, 13)], ls=1.3)
    x += wd + 0.23
s.banner(5.55, "IF ALL PANELS LOOK THE SAME: THE VALUE ENTERED THE ZONE OUTSIDE, BUT NEVER REACHED THE INPUT INSIDE.",
         fill=YELLOW, h=0.68, size=12, align=PP_ALIGN.CENTER)
s.t(L, 6.45, W, 0.4, [s.C("Attractors.blend, scenes 05 to 08: the supplied panel, then one point, several points "
                          "and a curve driving its Opening.", 13, MUTE)])

# 8 ── ISSUED — 3.4
issued_slide(d, "P3study",
             badge="ISSUED TODAY",
             blurb="One facade, one panel, one controlled parameter, three attractors. Each diagram shows "
                   "the attractor and the variation it produces, with the parameter labelled. No separate "
                   "upload and no separate grade: it is page 1 of the 3.5 package.",
             cards=[("DIAGRAM 1", "ONE POINT", "Distance to a single point drives the parameter."),
                    ("DIAGRAM 2", "SEVERAL POINTS", "Say how they combine: nearest point, or an average."),
                    ("DIAGRAM 3", "ONE CURVE", "Distance to the nearest location along a curve.")])

# 9 ── ISSUED — 3.5
issued_slide(d, "P3c", title="Architectural application",
             blurb="Reuse your 3.1 panel to design a simple facade, wall, canopy, pavilion or similar. Give it "
                   "a purpose and a scale, choose the attractor that serves that purpose, and show why the "
                   "variation matters architecturally.",
             cards=[("PURPOSE", "WHAT IT DOES", "What the panel system encloses, screens, shades or defines."),
                    ("COMPARE", "ONE CONTROLLED TEST", "The attractor, the parameter it drives, and the difference it makes."),
                    ("RESOLVE", "ELEVATION + ISOMETRIC", "Two sheets with 3.4: studies first, then the application.")])

# 10 ── REQUIREMENTS — 3.5
requirements_slide(d, "P3c", sub=VISUAL)

# 11 ── NOW
now_slide(d, "NOW — YOUR FIRST FIELD",
          "Rest of the class: measure, look, remap, and only then attach your panel.",
          ["Distance to one point, measured across the facade grid you already have",
           "The field shown as grey on its own, before any panel changes",
           "Input and output ranges written down, in your parameter's units, with the clamp",
           "One parameter of your 3.1 panel driven: Opening, Depth, Height or similar. Just one",
           "The attractor moved, and the change predicted before you look"],
          closer="MOVE THE ATTRACTOR. IF YOU CANNOT PREDICT WHAT HAPPENS, STOP AND READ THE FIELD.",
          bg=LIME)

# 12 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "%s: 3.4 and 3.5 are submitted together at the start of class. Then 4.1 is introduced: "
             "the supplied field groups and a two-parameter matrix." % C.date_long(10).title()),
    ("3.4", "All three attractor types running on the same facade, same panel, same parameter. "
            "The comparison is what is being graded."),
    ("3.5", "Pick the purpose first, then the attractor that serves it. One controlled comparison, "
            "one elevation, one isometric."),
    ("PANEL", "Your 3.1 panel as a node group with the driven parameter exposed. Test two values by hand "
              "before you connect an attractor."),
])

d.save(os.path.join(OUT, "ARC3133_Class09.pptx"))
print("class09 ok — %d slides" % len(d.prs.slides._sldIdLst))
