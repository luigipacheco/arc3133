# -*- coding: utf-8 -*-
"""Class 03 — CSG continued + 3D printing (U02). P2b issued."""
import os
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(3)
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Pt, Inches

OUT = os.environ.get("DECK_OUT", "/home/claude/out")
d = Deck()
WK = 3


def poly(sl, pts, fill, line=BLACK, lw=THIN):
    """Closed polygon from (x, y) points in inches."""
    ff = sl.s.shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    ff.add_line_segments([(Inches(px), Inches(py)) for px, py in pts[1:]], close=True)
    sh = ff.convert_to_shape()
    sh.shadow.inherit = False
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    sh.line.color.rgb = rgb(line); sh.line.width = lw
    return sh


def layers(sl, x, y, w, n, lh, step, fill=LIME):
    """n printed layers, bottom one at y; each layer shifted `step` to the right."""
    for k in range(n):
        sl.rect(x + k * step, y - (k + 1) * lh, w, lh, fill=fill, lw=HAIR)


# 1 ── TITLE
title_slide(d, WK, ["CSG CONTINUED", "+ 3D PRINTING"],
            "GEOMETRY THAT SURVIVES CONTACT WITH A MACHINE", bg=YELLOW, lfill=PINK, rfill=CYAN)

# 2 ── CSG, CONTINUED
s = d.slide(BLACK)
s.header("CSG, CONTINUED",
         "Finish the graph before it goes anywhere near a printer.")
pan = [("EXPOSE THE INPUTS", LIME,
        ["Pick the two or three numbers that change the design.",
         "Expose them. Name them.",
         "Change one, predict the result, then look."]),
       ("CHECK IT IS CLOSED", CYAN,
        ["Every difference and intersection must leave a closed solid.",
         "Look for open edges, stray faces, parts that only touch at an edge.",
         "Fix it in the graph, not on the mesh."]),
       ("FINISH THE P2a DIAGRAM", PINK,
        ["One frame per operation, same view, one verb each.",
         "Mark the kept and the removed solid.",
         "Draw the last frame at building scale."])]
x = L
for ttl, col, lines in pan:
    s.panel(x, 2.05, 3.85, 3.3, ttl, headfill=col, tsize=13.5)
    s.t(x + 0.28, 2.8, 3.3, 2.4, [s.Cb(l, 13.5) for l in lines], ls=1.25, space=8)
    x += 4.08
s.banner(5.75, "ONE GRAPH, TWO ASSIGNMENTS: P2a DRAWS IT, P2b PRINTS IT. KEEP THE HISTORY INTACT.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 3 ── WHAT THE MACHINE DOES
s = d.slide(CREAM)
s.header("WHAT THE MACHINE DOES",
         "One thing, repeatedly. Everything else follows from this.")
s.card(L, 1.95, 4.9, 4.2, fill=PAPER)
bx, by = L + 0.6, 5.35
s.rect(bx - 0.25, by, 3.9, 0.22, fill=BLACK, line=None)                 # bed
layers(s, bx + 0.6, by, 2.2, 8, 0.2, 0.0)
s.rect(bx + 1.35, by - 8 * 0.2 - 0.9, 0.7, 0.55, fill=MUTE, lw=THIN)    # hot end
nz = s.rect(bx + 1.5, by - 8 * 0.2 - 0.36, 0.4, 0.3, fill=PINK, lw=THIN,
            shape=MSO_SHAPE.ISOSCELES_TRIANGLE)
nz.rotation = 180
s.t(bx + 2.25, by - 8 * 0.2 - 0.82, 1.5, 0.3, [s.C("nozzle", 12.5, GREY)])
s.t(bx + 3.0, by - 1.0, 1.0, 0.3, [s.C("layers", 12.5, GREY)])
s.t(bx - 0.25, by + 0.3, 1.5, 0.3, [s.C("bed", 12.5, GREY)])
facts = [("01", "IT BUILDS UPWARD, NEVER SIDEWAYS",
          "Material can only go on material that is already there."),
         ("02", "LAYERS ARE THE WEAK DIRECTION",
          "A print snaps between layers long before it snaps across one."),
         ("03", "EVERY DECISION IS A TIME COST",
          "Finer layers, more material, more supports: all of it is hours on a shared machine.")]
y = 1.95
for n, ttl, body in facts:
    s.chip(5.85, y, 0.8, 1.15, n, fill=ACCENTS[int(n) - 1], size=16)
    s.card(6.95, y, 5.7, 1.15, fill=CREAM)
    s.t(7.2, y + 0.14, 5.25, 0.32, [s.Ab(ttl, 13.5)])
    s.t(7.2, y + 0.5, 5.25, 0.6, [s.Cb(body, 12.5)], ls=1.2)
    y += 1.35
s.banner(6.4, "A NOZZLE DRAWS ONE FLAT LAYER. THE BED DROPS. IT DRAWS THE NEXT.",
         fill=BLACK, color=YELLOW, h=0.62, align=PP_ALIGN.CENTER)

# 4 ── MANIFOLD
s = d.slide(BLACK)
s.header("MANIFOLD OR IT DOES NOT PRINT",
         "A model can look perfect on screen and mean nothing to a slicer.")
mf = [("WATERTIGHT", CYAN,
       "No gaps. Every edge is shared by exactly two faces. If water could leak out, it is not a solid."),
      ("NO SELF-INTERSECTION", LIME,
       "A shape that passes through itself has no clear inside. The slicer cannot decide what to fill."),
      ("NORMALS OUTWARD", PINK,
       "Every face has a front and a back. A flipped face tells the slicer that outside is inside.")]
x = L
for ttl, col, body in mf:
    s.panel(x, 2.05, 3.85, 3.0, ttl, headfill=col, tsize=14)
    s.t(x + 0.28, 2.85, 3.3, 2.0, [s.Cb(body, 14.5)], ls=1.3)
    x += 4.08
s.banner(5.45, "CHECK BEFORE YOU SLICE. A BOOLEAN THAT LEFT AN OPEN EDGE IS THE MOST COMMON CAUSE "
              "OF A FAILED FILE.", fill=YELLOW, h=0.72, align=PP_ALIGN.CENTER)
s.t(L, 6.5, W, 0.4, [s.C("This is the closure check from the CSG slide, seen from the machine's side.",
                         13, MUTE)])

# 5 ── OVERHANGS AND THE LETTER TEST
s = d.slide(CREAM)
s.header("OVERHANGS AND THE LETTER TEST",
         "Each layer needs something under it. How much is the whole question.")
oh = [("VERTICAL", LIME, 0.0, "Every layer sits fully on the one below."),
      ("45°", YELLOW, 0.2, "Each layer steps out as far as it is tall. About the limit."),
      ("STEEP", PINK, 0.28, "Most of the layer hangs in air. It droops or fails.")]
x = L
for ttl, col, step, body in oh:
    s.card(x, 1.95, 3.85, 1.75, fill=CREAM)
    s.rule(x + 0.2, 3.42, 2.0, lw=Pt(3), color=BLACK)
    layers(s, x + 0.3, 3.4, 0.45, 6, 0.2, step, fill=col)
    s.t(x + 2.3, 2.15, 1.4, 0.3, [s.Ab(ttl, 14)])
    s.t(x + 2.3, 2.55, 1.4, 1.1, [s.Cb(body, 12)], ls=1.15)
    x += 4.08
lt = [("H", "BRIDGE", "PRINTS FINE", LIME,
       "The crossbar spans two legs that already exist. Anchored at both ends."),
      ("V", "SLOPE", "FINE TO 45°", CYAN,
       "Each layer steps out a little. Past about 45° it starts to droop."),
      ("T", "CANTILEVER", "DROOPS", PINK,
       "The arms start in mid-air, anchored at one end only."),
      ("Y", "FORK", "CHECK THE ANGLE", YELLOW,
       "Two slopes grow from one stem. Steep arms print; flat arms droop.")]
cw = (W - 0.23 * 3) / 4
x = L
for letter, kind, verdict, col, body in lt:
    s.card(x, 3.95, cw, 2.05, fill=CREAM)
    s.t(x + 0.2, 3.98, 0.9, 0.95, [s.Ab(letter, 44)])
    s.t(x + 1.05, 4.12, cw - 1.2, 0.3, [s.Ab(kind, 12.5)])
    s.chip(x + 1.05, 4.47, cw - 1.25, 0.36, verdict, fill=col, size=10, shadow=False)
    s.t(x + 0.2, 5.0, cw - 0.4, 0.95, [s.Cb(body, 12)], ls=1.2)
    x += cw + 0.23
s.banner(6.22, "THE 45° RULE: PAST ABOUT 45° FROM VERTICAL, A SURFACE NEEDS SUPPORT — OR A "
              "DIFFERENT ORIENTATION.", fill=BLACK, color=YELLOW, h=0.56, size=12,
         align=PP_ALIGN.CENTER)
s.t(L, 6.97, W, 0.3, [s.C("An island, a part that starts with nothing under it, cannot print "
                          "without support. Find all four conditions in your own model.", 12, GREY)])

# 6 ── ORIENTATION
s = d.slide(CREAM)
s.header("ORIENTATION IS YOUR ONLY LEVER",
         "Same geometry. Two ways to place it. Very different prints.")
for i, (ttl, col) in enumerate([("AS MODELLED", PINK), ("ROTATED", LIME)]):
    px = L + i * 6.15
    s.panel(px, 1.95, 5.85, 3.85, ttl, headfill=col)
    s.card(px + 0.3, 2.75, 2.6, 2.75, fill=PAPER, shadow=False, lw=THIN)
    gx, gy = px + 0.5, 5.15
    s.rect(gx - 0.05, gy, 2.3, 0.14, fill=BLACK, line=None)               # bed
    t = 0.38
    if i == 0:   # Γ: stem on the bed, arm hanging out at the top
        s.rect(gx + t + 0.02, gy - 1.6 + t, 1.4 - t - 0.04, 1.6 - t, fill=PINK, line=BLACK,
               lw=HAIR)
        s.t(gx + t + 0.1, gy - 0.75, 1.1, 0.3, [s.Cb("support", 11.5, bold=True)])
        poly(s, [(gx, gy), (gx + t, gy), (gx + t, gy - 1.6 + t), (gx + 1.4, gy - 1.6 + t),
                 (gx + 1.4, gy - 1.6), (gx, gy - 1.6)], CYAN)
        body = ("The arm overhangs. It needs support, which costs material and time, and "
                "scars the surface where it is removed.")
    else:        # L: the same part turned over, the arm lies on the bed
        poly(s, [(gx, gy), (gx + 1.4, gy), (gx + 1.4, gy - 1.6), (gx + 1.4 - t, gy - 1.6),
                 (gx + 1.4 - t, gy - t), (gx, gy - t)], CYAN)
        body = ("The arm now lies on the bed. No support, faster, a cleaner face, and "
                "stronger: the load no longer runs across a layer line.")
    s.t(px + 3.1, 2.8, 2.5, 2.8, [s.Cb(body, 13.5)], ls=1.3)
s.banner(6.1, "NO SUPPORTS ARE ALLOWED ON P2b. IF NO ORIENTATION WORKS, CHANGE THE GEOMETRY "
              "AND EXPLAIN THE CHANGE ON THE PROCESS SHEET.", fill=YELLOW, h=0.72,
         align=PP_ALIGN.CENTER)

# 7 ── THE SLICER AND FOUR SETTINGS
s = d.slide(BLACK)
s.header("WHAT THE SLICER DOES",
         "It turns a solid into a list of moves. You will do the same by hand in Week 12, "
         "%s." % C.week(12)["title"])
steps_ = [("01", "CUT INTO LAYERS", "A stack of horizontal planes cuts the solid."),
          ("02", "OUTLINE EACH LAYER", "Each cut becomes a closed perimeter."),
          ("03", "FILL THE INSIDE", "An infill pattern, usually sparse."),
          ("04", "ORDER THE MOVES", "Perimeters, infill, travel, written as G-code.")]
cw = (W - 0.23 * 3) / 4
x = L
for i, (n, ttl, body) in enumerate(steps_):
    s.chip(x, 1.95, cw, 0.45, n + "   " + ttl, fill=ACCENTS[i], size=11)
    s.card(x, 2.5, cw, 0.95, fill=CREAM)
    s.t(x + 0.2, 2.5, cw - 0.4, 0.95, [s.Cb(body, 12.5)], ls=1.2, anchor=MSO_ANCHOR.MIDDLE)
    x += cw + 0.23
s.t(L, 3.78, W, 0.35, [s.A("FOUR SETTINGS — LEAVE EVERYTHING ELSE AT DEFAULT", 14, YELLOW)])
sets = [("LAYER HEIGHT", "0.2–0.3 mm", "Finer looks better and takes longer. Draft is fine here."),
        ("INFILL", "10–40%", "A lattice inside a shell. Solid is almost never needed."),
        ("WALLS", "2–3", "Perimeters, not infill, make a print feel solid."),
        ("SUPPORTS", "OFF", "Not allowed on P2b. Solve it with orientation.")]
x = L
for i, (ttl, val, body) in enumerate(sets):
    s.card(x, 4.25, cw, 1.75, fill=CREAM)
    s.t(x + 0.2, 4.38, cw - 0.4, 0.3, [s.Ab(ttl, 12, GREY)])
    s.t(x + 0.2, 4.68, cw - 0.4, 0.5, [s.Ab(val, 22)])
    s.t(x + 0.2, 5.25, cw - 0.4, 0.7, [s.Cb(body, 11.5)], ls=1.15)
    x += cw + 0.23
s.banner(6.3, "LIVE NOW — WE SLICE ONE OBJECT TOGETHER AND READ THE PREVIEW: LAYER COUNT, PRINT TIME, "
              "MATERIAL.", fill=PINK, h=0.62, size=12, align=PP_ALIGN.CENTER)

# 8 ── PRINT IT OR CUT IT
s = d.slide(CREAM)
s.header("PRINT IT OR CUT IT",
         "Printing is not the default. It is the expensive option.")
cols = [("CUT IT", CYAN, ["Prismatic: one profile, extruded", "Flat, or made of flat pieces",
                          "Repeated many times", "Larger than your hand"],
         "Minutes per sheet. Many parts at once."),
        ("PRINT IT", PINK, ["Doubly curved: a vault, a shell", "Undercuts a blade cannot reach",
                            "Detail in all three axes at once", "Small and intricate"],
         "Hours per object. One at a time.")]
for i, (ttl, col, items, foot) in enumerate(cols):
    px = L + i * 6.15
    s.panel(px, 1.95, 5.85, 3.55, ttl, headfill=col)
    s.t(px + 0.35, 2.75, 5.2, 2.0, [s.Cb("—  " + it, 14.5) for it in items], ls=1.45)
    s.rule(px + 0.35, 4.72, 5.15, lw=Pt(1.5), color=MUTE)
    s.t(px + 0.35, 4.88, 5.15, 0.4, [s.Cb(foot, 13.5, bold=True)])
s.banner(5.85, "THE TEST: CAN IT BE DESCRIBED AS A STACK OF FLAT PROFILES, OR ONE PROFILE EXTRUDED? "
              "THEN CUT IT. A SIMPLE BOX, PRINTED, IS A BOX YOU WAITED HOURS FOR.",
         fill=YELLOW, h=0.8, align=PP_ALIGN.CENTER)
s.t(L, 6.85, W, 0.35, [s.C("P2b is printed on purpose. The laser cutter comes back in Project 4.",
                           12.5, GREY)])

# 9 ── FAILURES AND FABLAB RULES
s = d.slide(CREAM)
s.header("SIX WAYS IT GOES WRONG",
         "Learn to name the failure. Naming it is most of the diagnosis.")
fails = [("WARPING", "Corners lift; the base curves.", "Clean bed, a brim, no drafts."),
         ("ELEPHANT'S FOOT", "The bottom layers bulge out.", "Slicer setting, or chamfer the base."),
         ("STRINGING", "Fine hairs between parts.", "Retraction on. Fewer travel moves."),
         ("LAYER SEPARATION", "It splits along a layer line.", "Reorient so the load runs along layers."),
         ("DROOP", "An overhang sags into the air.", "Reorient. If that fails, change the geometry."),
         ("SPAGHETTI", "A nest of filament in mid-air.", "Adhesion. Watch the first layer.")]
for k, (ttl, sym, fix) in enumerate(fails):
    fx = L + (k % 3) * 4.08
    fy = 1.95 + (k // 3) * 1.42
    s.card(fx, fy, 3.85, 1.25, fill=CREAM)
    s.rect(fx, fy, 3.85, 0.42, fill=ACCENTS[k % 4], lw=BORDER)
    s.t(fx + 0.2, fy, 3.45, 0.42, [s.Ab(ttl, 12)], anchor=MSO_ANCHOR.MIDDLE)
    s.t(fx + 0.2, fy + 0.5, 3.45, 0.7,
        [[s.Cb(sym, 12)], [s.Cb("FIX  ", 11, bold=True), s.Cb(fix, 12)]], ls=1.15)
s.card(L, 4.95, W, 1.8, fill=BLACK)
s.t(L + 0.35, 5.07, 5.0, 0.35, [s.A("FABLAB RULES", 14, YELLOW)])
rules = ["Finish the FabLab safety orientation first. No orientation, no machine.",
         "Never touch the hot end. The nozzle runs at about 200–250 °C and the bed is hot.",
         "Never restart someone else's print. If a job looks wrong, tell staff.",
         "The queue is first come. A print that starts at the deadline does not finish."]
for k, r in enumerate(rules):
    rx = L + 0.35 + (k % 2) * 5.85
    ry = 5.5 + (k // 2) * 0.55
    s.t(rx, ry, 5.55, 0.5, [s.C(r, 12, CREAM)], ls=1.1)
s.t(L, 7.0, W, 0.3, [s.C("Booking, file naming, pick-up and material allocation: follow the "
                         "procedure posted by FabLab staff.", 11.5, GREY)])

# 10 ── ISSUED TODAY — P2b
issued_slide(d, "P2b",
             blurb="Print a variant of the CSG object you are diagramming for P2a. Small, "
                   "unsupported and documented: the orientation, the slicer settings and a "
                   "photograph go on one process sheet.",
             cards=[("SIZE", "60 mm, 200 g", "Within 60 mm on each axis, inside the 200 g allocation."),
                    ("SUPPORTS", "NONE", "Orientation is the lever. Change geometry only if you must, and say why."),
                    ("SHEET", "ONE PAGE", "Orientation and a photograph. Handed in with the print in Week 10.")])

# 11 ── REQUIREMENTS
s = requirements_slide(d, "P2b", sub="")
s.t(L, 1.38, W, 0.34, [s.C("Visual documentation 20% · computational understanding 20% · technical "
                           "execution 15% · fabrication quality 30% · experimentation 5% · "
                           "requirements and identity 10%.", 12, GREY)])

# 12 ── NOW
now_slide(d, "NOW — PREPARE YOUR PRINT",
          "Rest of the class: take your CSG object from graph to sliced file, with help in the room.",
          ["Solid checked — closed, no self-intersection, normals outward",
           "Scaled to fit within 60 mm on each axis, units confirmed in the slicer",
           "Oriented — no overhang past about 45°, supports off",
           "Sliced — layer count, print time and material written down",
           "Orientation, settings and any geometry change noted for the P2b sheet"],
          closer="LEAVE WITH A SLICED FILE AND ITS NUMBERS WRITTEN DOWN.",
          bg=CYAN)

# 13 ── BEFORE NEXT CLASS
p2a, p2b = C.milestone("P2a"), C.milestone("P2b")
cp_wk, cp_txt = C.checkpoints("P2b")[0]
before_next_slide(d, [
    ("NEXT", "%s. %s: point, line, edge, face, solid, Boolean. P3a is issued."
             % (C.date_long(4), C.week(4)["title"])),
    ("DUE", "P2a, the CSG process sheet, is due next class, %s." % C.date_long(p2a["due"])),
    ("PRINT", "P2b print checkpoint %s: %s P2b is due at the mid-semester deadline, %s."
              % (C.date_long(cp_wk), cp_txt, C.date_long(p2b["due"]))),
    ("FABLAB", "Complete the FabLab safety orientation before the checkpoint. "
               "No orientation, no machine access."),
])

d.save(os.path.join(OUT, "ARC3133_Class03.pptx"))
print("class03 ok — %d slides" % len(d.prs.slides._sldIdLst))
