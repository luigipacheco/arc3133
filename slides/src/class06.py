# -*- coding: utf-8 -*-
"""Class 06 — Arrays 1: line, grid, cube, curve (U04, Week 6). Plain repetition only; patterns are Class 07.
2.1 due tonight; 3.2 issued (Sheet 1 today); 2.2 print check.

Loops are explained as readable Python, never as node-editor screenshots.
Colour that explains a direction follows Blender's axes: X red, Y green, Z blue.
Images in img/class06/c*.png are renders of Arrays-Lists-Session-1.blend scenes 01–04,
coloured by position (X→R, Y→G, Z→B) and cropped. Re-render them if the file changes."""
import os, re
from nb import *
from slidekit import *
import coursedata as C
C.require_current_deck(6)
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img", "class06")
OUT = os.environ.get("DECK_OUT", os.path.join(HERE, ".."))
d = Deck()
WK = 6

# Blender's axis colours — fills (black text on top) and a darker set for text on cream
AX = {"X": "FF3352", "Y": "8BDC00", "Z": "2890FF"}
AXT = {"i": "D7263D", "j": "3E8E00", "k": "1F6FD1"}

A21, A22, A32 = C.milestone("P2a"), C.milestone("P2b"), C.milestone("P3b")
N21, N22, N32, N31 = A21["number"], A22["number"], A32["number"], C.milestone("P3a")["number"]


def picture(s, name, x, y, w, h, frame=None):
    """Fit an image inside a box, centred, aspect kept."""
    path = os.path.join(IMG, name)
    iw, ih = Image.open(path).size
    k = min(w / iw, h / ih)
    pw, ph = iw * k, ih * k
    px, py = x + (w - pw) / 2, y + (h - ph) / 2
    if frame:
        s.rect(px, py, pw, ph, fill=None, line=frame, lw=BORDER)
    s.s.shapes.add_picture(path, Inches(px), Inches(py), Inches(pw), Inches(ph))


TOKEN = re.compile(r"\b(i|j|k)\b")


def code(s, x, y, w, lines, size=12, step=0.3):
    """Readable Python, one line per row. i, j, k take their axis colour."""
    for ln in lines:
        runs, pos = [], 0
        body, _, comment = ln.partition("#")
        for m in TOKEN.finditer(body):
            if m.start() > pos:
                runs.append((body[pos:m.start()], "Courier New", size, None, BLACK))
            runs.append((m.group(1), "Courier New", size, True, AXT[m.group(1)]))
            pos = m.end()
        if pos < len(body):
            runs.append((body[pos:], "Courier New", size, None, BLACK))
        if comment:
            runs.append(("#" + comment, "Courier New", size, None, GREY))
        s.t(x, y, w, step, [runs or [(" ", "Courier New", size, None, BLACK)]])
        y += step


def weights(mid):
    out = []
    for line in C.milestone(mid)["brief"]["evaluation"]:
        out.append(line.split(":**")[0].strip("* ").replace(" - ", " "))
    return " · ".join(out) + "."


# 1 ── TITLE
title_slide(d, WK, ["ARRAYS 1", "LINE · GRID · CUBE · CURVE"],
            "ONE MODULE, MANY POSITIONS", bg=LIME, lfill=PINK, rfill=CYAN,
            right_tag="%s DUE %s" % (N21, C.due_label("P2a").split(",")[0].upper()),
            foot="%s ISSUED TODAY  /  %s PRINT CHECK TODAY" % (N32, N22))

# 2 ── AN ARRAY IS A LIST OF POSITIONS
s = d.slide(CREAM)
s.header("AN ARRAY IS A LIST OF POSITIONS",
         "Not a command that duplicates things. A list you compute, then place your module at.")
s.panel(L, 1.95, 5.6, 3.5, "INDEX  →  POSITION", headfill=CYAN)
code(s, L + 0.35, 2.75, 5.0, ["i = 0   →   p = start",
                              "i = 1   →   p = start + step",
                              "i = 2   →   p = start + 2 × step",
                              "",
                              "p[i] = start + i × step"], size=13.5, step=0.36)
s.panel(6.6, 1.95, 6.05, 3.5, "THREE THINGS TO READ", headfill=PINK)
s.t(6.9, 2.72, 5.45, 2.5, [
    s.Cb("THE LIST — what is in the collection.", 14),
    s.Cb("THE COUNT — how many there are.", 14),
    s.Cb("THE INDEX — where each one sits in the order.", 14),
    s.Cb(" ", 7),
    s.Cb("The index is the only new idea. It is a counter that tells each copy how far along "
         "it is — and therefore where it goes.", 13.5)], ls=1.35)
s.banner(5.75, "Your %s module is the component. On Sheet 1 it does not change — only where it goes." % N31,
         fill=LIME, h=0.72)

# 3 ── TODAY: ONE LOOP, FOUR WAYS
s = d.slide(BLACK)
s.header("TODAY: ONE LOOP, FOUR WAYS",
         "Class file Arrays Part 1, scenes 01–04. Colour is position: X red, Y green, Z blue.")
steps = [("LINE", "c01_row.png", "i", AX["X"]), ("GRID", "c02_grid.png", "i, j", AX["Y"]),
         ("CUBE", "c03_cube_n4.png", "i, j, k", AX["Z"]), ("CURVE", "c04_curve_module.png", "i along a curve", YELLOW)]
x, wd = L, (W - 0.25 * 3) / 4
for n, (nm, img, ctr, col) in enumerate(steps, 1):
    s.chip(x, 2.0, wd, 0.48, "%02d  %s" % (n, nm), fill=col, size=12)
    picture(s, img, x, 2.62, wd, wd / 1.6, frame=CREAM)
    s.t(x, 2.72 + wd / 1.6, wd, 0.35, [s.M(ctr, 12, MUTE)], align=PP_ALIGN.CENTER)
    x += wd + 0.25
s.t(L, 5.0, W, 0.9, [s.C("Line, grid and cube add one counter at a time. The curve changes where a position "
                          "comes from. No rules yet: every copy is treated the same. Patterns start next week.", 15)], ls=1.3)
s.banner(6.1, "EVERY STEP IS THE SAME LOOP. ONLY THE COUNTERS AND THE SOURCE OF POSITION CHANGE.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 4 ── THE LOOP, WRITTEN OUT
s = d.slide(CREAM)
s.header("THE LOOP, WRITTEN OUT", "Scene 01 — Linear loop, as a script you can read aloud.")
s.card(L, 1.95, 7.1, 3.55, fill=CREAM)
code(s, L + 0.3, 2.15, 6.7, [
    "count   = 8",
    "spacing = 0.8",
    "points  = []                  # the list starts empty",
    "",
    "for i in range(count):        # i = 0, 1, 2 … 7",
    "    x = i * spacing           # position from the index",
    "    points.append((x, 0, 0))  # one more item",
    "",
    "place(module, points)         # a copy at every point"], size=12.5, step=0.36)
s.panel(8.0, 1.95, 4.65, 3.55, "READ IT AS A SENTENCE", headfill=AX["X"], tsize=14)
s.t(8.3, 2.7, 4.1, 2.7, [
    s.Cb("Start with an empty list.", 13),
    s.Cb("Count times: work out x from i, and add that point to the list. Each pass, i is one bigger.", 13),
    s.Cb("Then put the module at every point.", 13)], ls=1.3, space=6)
s.t(L, 5.65, W, 0.4, [s.Cb("In the class file:  for → Repeat Zone   ·   i → Iteration   ·   append → Join Geometry"
                           "   ·   place → Instance on Points", 13, GREY)], align=PP_ALIGN.CENTER)
s.banner(6.25, "i IS THE INDEX. EVERYTHING ELSE IN THE LOOP IS ARITHMETIC ON IT.",
         fill=YELLOW, h=0.66, align=PP_ALIGN.CENTER)

# 5 ── READ IT SMALL FIRST
s = d.slide(BLACK)
s.header("READ IT SMALL FIRST", "The loop, and a spreadsheet open beside it.")
s.panel(L, 1.95, 6.0, 3.4, "WHAT THE LOOP DOES", headfill=LIME)
s.t(L + 0.35, 2.7, 5.3, 2.5, [
    s.Cb("Everything inside the loop runs once per pass. Whatever goes in comes back with one more "
         "item, once for every step of the count.", 13.5)], ls=1.3)
s.panel(7.0, 1.95, 5.65, 3.4, "HOW TO CHECK IT", headfill=CYAN)
s.t(7.3, 2.7, 5.05, 2.5, [
    s.Cb("Set Count to 3 and read the spreadsheet: three rows, three positions.", 13.5),
    s.Cb(" ", 6),
    s.Cb("Then 4. Then 5. Say the last X before you look.", 13.5),
    s.Cb(" ", 6),
    s.Cb("A list you cannot inspect is a list you cannot debug. There is no minimum count.", 13.5)], ls=1.3)
s.banner(5.65, "BUILD IT AT A COUNT YOU CAN COUNT. SCALE UP ONLY ONCE IT IS RIGHT.",
         fill=YELLOW, h=0.7, align=PP_ALIGN.CENTER)

# 6 ── 01 · LINE
s = d.slide(BLACK)
s.header("01 · LINE", "Scene 01 — Linear loop · Count 8 · Spacing 0.8")
picture(s, "c01_row.png", L, 1.95, 7.0, 4.375, frame=CREAM)
s.panel(8.0, 1.95, 4.65, 4.375, "READ THE ROW", headfill=AX["X"], tsize=14.5)
code(s, 8.3, 2.7, 4.1, ["i   0    1    2   …   7",
                        "x   0.0  0.8  1.6 …   5.6",
                        "",
                        "count = 8",
                        "last  = 7 × 0.8 = 5.6"], size=13, step=0.36)
s.t(8.3, 4.65, 4.1, 1.5, [s.Cb("Colour is position: X → red. The darkest copy is i = 0, the brightest i = 7.", 13)],
    ls=1.3)
s.banner(6.6, "THE LAST COPY IS AT 7 × SPACING, NOT 8. COUNTING STARTS AT ZERO.",
         fill=CYAN, h=0.58, size=12, align=PP_ALIGN.CENTER)

# 7 ── 02 · GRID
s = d.slide(CREAM)
s.header("02 · GRID — A LOOP INSIDE A LOOP", "Scene 02 — Nested grid · Rows 5 · Columns 5 · Spacing 0.8")
picture(s, "c02_grid.png", L, 1.95, 7.0, 4.375, frame=BLACK)
s.panel(8.0, 1.95, 4.65, 4.375, "TWO COUNTERS", headfill=AX["Y"], tsize=14.5)
code(s, 8.3, 2.7, 4.1, ["for j in range(rows):",
                        "    for i in range(columns):",
                        "        place(i*dx, j*dy, 0)",
                        "",
                        "5 × 5 = 25"], size=12.5, step=0.36)
s.t(8.3, 4.65, 4.1, 1.5, [s.Cb("i runs along the row; j picks which row. Red grows with X, green with Y.", 13)],
    ls=1.3)
s.banner(6.6, "THE INNER LOOP MAKES A ROW. THE OUTER LOOP COLLECTS THE ROWS.",
         fill=LIME, h=0.58, size=12, align=PP_ALIGN.CENTER)

# 8 ── INDEX ORDER
s = d.slide(BLACK)
s.header("INDEX ORDER", "Which counter runs inside decides the order. Label it on the sheet.")
s.panel(L, 2.05, 6.2, 3.65, "A 4 × 3 GRID, i INSIDE j", headfill=LIME)
gx, gy, c = L + 0.9, 2.9, 0.72
for j in range(3):
    for i in range(4):
        s.rect(gx + i * c, gy + (2 - j) * c, c, c, fill=CREAM, line=BLACK, lw=HAIR)
        s.t(gx + i * c, gy + (2 - j) * c, c, c, [s.Mb(str(i + j * 4), 13, bold=True)],
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
for j in range(3):
    s.t(gx + 4 * c + 0.2, gy + (2 - j) * c, 1.2, c, [s.Mb("j = %d" % j, 11.5, AXT["j"], bold=True)],
        anchor=MSO_ANCHOR.MIDDLE)
s.t(gx, gy + 3 * c + 0.1, 4 * c, 0.3, [s.Mb("i →  0 · 1 · 2 · 3", 11.5, AXT["i"], bold=True)],
    align=PP_ALIGN.CENTER)
s.panel(7.15, 2.05, 5.5, 3.65, "THE FLAT INDEX", headfill=YELLOW)
code(s, 7.45, 2.8, 4.9, ["2D:  index = i + j × nx",
                         "3D:  index = i + j × nx + k × nx × ny"], size=12, step=0.34)
s.t(7.45, 3.6, 4.9, 2.0, [s.Cb("Swap the loops and the same positions get different numbers. The picture looks the "
                               "same; any rule that reads the index — next week's if/Switch — does not.", 13.5)],
    ls=1.35)
s.banner(6.0, "SAY IT OUT LOUD: WHICH WAY DOES i RUN, AND WHAT HAPPENS IF YOU SWAP THE LOOPS?",
         fill=PINK, h=0.68, align=PP_ALIGN.CENTER)

# 9 ── 03 · CUBE
s = d.slide(BLACK)
s.header("03 · CUBE — THE GRID, REPEATED IN Z",
         "Scene 03 — 3D array · Spacing 1.25 · Cube Size 0.75 · one camera for all three")
x, wd = L, (W - 0.23 * 2) / 3
for n in (3, 4, 5):
    picture(s, "c03_cube_n%d.png" % n, x, 1.95, wd, wd / 1.6, frame=CREAM)
    s.chip(x, 4.55, wd, 0.5, "COUNT %d  →  %d × %d × %d = %d" % (n, n, n, n, n ** 3), fill=YELLOW, size=12.5)
    x += wd + 0.23
s.card(L, 5.3, W, 0.62, fill=CREAM, shadow=False)
code(s, L + 0.3, 5.43, W - 0.6, ["for k in range(n):  for j in range(n):  for i in range(n):   place(i*dx, j*dy, k*dz)"],
     size=12.5, step=0.36)
s.banner(6.2, "PREDICT THE TOTAL BEFORE YOU LOOK: 27, 64, 125. X, Y AND Z TOGETHER MAKE THE RGB CUBE.",
         fill=AX["Z"], h=0.66, size=12, align=PP_ALIGN.CENTER)

# 10 ── 04 · CURVE
s = d.slide(CREAM)
s.header("04 · CURVE — THE ROW BENDS", "Scene 04 — Along a curve · Spacing 0.8 · the same module as the line. Edit the curve; the row follows.")
picture(s, "c04_curve_module.png", L, 1.95, 6.6, 4.125, frame=BLACK)
s.panel(7.55, 1.95, 5.1, 4.125, "WHERE IS COPY i?", headfill=YELLOW, tsize=14.5)
code(s, 7.8, 2.7, 4.7, ["count = int(length / spacing) + 1",
                        "for i in range(count):",
                        "    t = i / (count - 1)  # 0 → 1",
                        "    p = point_on(curve, t)",
                        "    d = direction_on(curve, t)",
                        "    place(module, p, facing=d)"], size=11.5, step=0.33)
s.t(7.8, 4.85, 4.6, 1.1, [s.Cb("The line said x = i × spacing. Here the curve answers the same question, "
                               "and also says which way to face.", 12.5)], ls=1.25)
s.banner(6.4, "SAME LOOP AS THE LINE. THE CURVE GIVES THE POSITION INSTEAD OF i × SPACING.",
         fill=YELLOW, h=0.66, size=12, align=PP_ALIGN.CENTER)

# 13 ── THE EVOLUTION
s = d.slide(BLACK)
s.header("THE EVOLUTION", "Line to curve, one change at a time.")
rows = [("01 LINE", "One counter, i. Position = i × spacing.", AX["X"]),
        ("02 GRID", "i inside j. Total = rows × columns.", AX["Y"]),
        ("03 CUBE", "i inside j inside k. Total = count cubed.", AX["Z"]),
        ("04 CURVE", "One counter again — but the curve gives the position and the direction.", YELLOW),
        ("NEXT WEEK", "Patterns: a rule that reads the index. First example — a brick wall, every other course shifted.", PINK)]
y = 1.9
for lab, body, col in rows:
    s.actionrow(y, lab, body, fill=col, h=0.78)
    y += 0.9
s.banner(6.5, "ONE LOOP. EACH STEP ADDS A COUNTER OR CHANGES WHERE THE POSITION COMES FROM.",
         fill=YELLOW, h=0.6, size=12, align=PP_ALIGN.CENTER)

# 14 ── STEPS (U04 steps 1–5, verbatim from course.yml)
s = unit_steps_slide(d, "U04", title="TODAY, STEP BY STEP", n=(0, 4),
                 sub="Plain repetition: every copy treated the same. The curve is in-class practice; Sheet 1 is your module, then 1D, 2D, 3D.")

# 15 ── 2.2 PRINT CHECK
s = d.slide(CREAM)
s.header("%s PRINT CHECK — BEFORE YOU QUEUE" % N22, C.checkpoints("P2b")[0][1])
checks = [("GEOMETRY", CYAN, "Closed and solid. Every edge shared by two faces, no stray pieces."),
          ("UNITS", LIME, "Real millimetres. Within 60 mm on each axis."),
          ("ORIENTATION", YELLOW, "No supports. Orientation is your lever; change the geometry if you must."),
          ("SLICED PREVIEW", PINK, "Read it layer by layer before queueing. Stay within the 200 g allocation.")]
y = 1.95
for nm, col, body in checks:
    s.chip(L, y, 2.6, 0.72, nm, fill=col, size=13)
    s.card(L + 2.9, y, W - 2.9, 0.72, fill=CREAM)
    s.t(L + 3.2, y, W - 3.5, 0.72, [s.Cb(body, 14)], anchor=MSO_ANCHOR.MIDDLE)
    y += 0.92
s.banner(5.85, "%s: FILES, NOTES AND A PHOTO OF YOUR PRINT ON TEAMS BY %s."
         % (N22, C.due_label("P2b").upper()), fill=BLACK, color=LIME, h=0.7, size=12, align=PP_ALIGN.CENTER)

# 16 ── ISSUED — 3.2
s = d.slide(BLACK)
s.issued("ISSUED TODAY", "%s — %s" % (N32, A32["title"].upper()), C.due_line("P3b"),
         "Three 17 × 11 sheets, submitted together as one assignment. Sheet 1 is today; "
         "Sheets 2 and 3 are next week's class.", badgefill=YELLOW)
nxt = C.date_long(7).split(" — ")[0]
cards = [("SHEET 1 · TODAY", "MODULE, 1D, 2D, 3D", "Your %s module alone, then in a row, a grid and layers. Label counts, spacing, axes and totals." % N31),
         ("SHEET 2 · " + nxt, "FOUR FAÇADE PATTERNS", "Your module in a 2D array, changed by if/Switch conditions. Each rule and its outcome captioned."),
         ("SHEET 3 · " + nxt, "RULES IN 3D", "Rules on row, column and layer switch a cube parameter between two values. Two isometrics, each rule captioned.")]
x, wd = L, (W - 0.23 * 2) / 3
for i, (tag, ttl, body) in enumerate(cards):
    s.chip(x, 3.95, wd, 0.45, tag, fill=[CYAN, LIME, PINK][i], size=11)
    s.card(x, 4.5, wd, 1.75, fill=CREAM)
    s.t(x + 0.28, 4.66, wd - 0.56, 0.35, [s.Ab(ttl, 13.5)])
    s.t(x + 0.28, 5.06, wd - 0.56, 1.1, [s.Cb(body, 12)], ls=1.22)
    x += wd + 0.23

# 17 ── REQUIREMENTS — 3.2 (verbatim from course.yml)
requirements_slide(d, "P3b", title="REQUIREMENTS — %s" % N32, sub=weights("P3b"))

# 18 ── NOW
now_slide(d, "NOW — SHEET 1",
          "Predict every total before you look.",
          ["A row: Count and Spacing exposed, spreadsheet open, the last X said out loud",
           "The row nested into a grid: rows × columns predicted first",
           "The grid repeated in Z — 3, 4 and 5 per axis compared",
           "Your row bent onto a curve: edit the curve and watch the row follow",
           "%s print checked before you queue it; everything through Arrays is due %s" % (N22, C.due_label("P3b"))],
          closer="A COUNT YOU CAN COUNT. NOT A THOUSAND OF ANYTHING, YET.", bg=CYAN)

# 19 ── BEFORE NEXT CLASS
before_next_slide(d, [
    ("NEXT", "%s: patterns — a brick wall with every other course shifted, if/Switch façade patterns, and the same rules in a 3D array of cubes (Sheets 2 and 3). "
             "Bring Sheet 1's graph working; we build on it." % C.date_long(7).title()),
    ("DUE", "Nothing graded next week (studio reviews) or the week after. Everything through Arrays — the manual, %s, the %s print, %s and %s, all three sheets — is due %s."
            % (N21, N22, N31, N32, C.due_label("P3b"))),
    ("BUILD", "Finish Sheet 1: module alone, then 1D, 2D and 3D — counts, spacing, axes and totals labelled."),
    ("PRINT", "Fix anything today's check flagged, then queue %s." % N22),
])

path = os.path.join(OUT, "ARC3133_Class06.pptx")
d.save(path)
print("class06 ok — %d slides -> %s" % (len(d.prs.slides._sldIdLst), os.path.abspath(path)))
