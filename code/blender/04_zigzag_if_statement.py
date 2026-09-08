# ARC 3133 — Module 1: POINT
# Script 4 of 5 — Zig zag: the conditional
#
# Script 3 asked chance for the height. This one asks a question instead.
#
#   if <something is true>:
#       do this
#   else:
#       do the other thing
#
# The loop still runs the same number of times. What changes is that each
# pass now makes a decision.

import bpy

NAME = "04_zigzag"

# ---- PARAMETERS -------------------------------------------------------

COUNT = 20        # how many points
STEP = 1.0        # distance between them along X
LOW = 0.0         # height on even points
HIGH = 2.0        # height on odd points     <- change this one first

# ---- LOGIC ------------------------------------------------------------

points = []
for i in range(COUNT):
    x = i * STEP
    y = 0.0

    if i % 2 == 0:        # is the remainder of i divided by 2 zero?
        z = LOW           #   yes — i is even
    else:
        z = HIGH          #   no  — i is odd

    points.append((x, y, z))

edges = []
for i in range(COUNT - 1):
    edges.append((i, i + 1))

print("points:", len(points))
print("first four:", points[0:4])

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])        # vertices, edges, faces
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# READING  i % 2 == 0
#
#   %   the remainder after dividing.  7 % 2 is 1.  8 % 2 is 0.
#   ==  asks "are these equal?" and answers True or False.
#   =   assigns a value. They are different operators. Mixing them up is
#       the single most common error in this script.
#
#   So  i % 2 == 0  is the question "is i even?"
#
#   Type  print(7 % 2)  in the console. Then  print(7 % 3).
#   Then  print(7 == 7)  and  print(7 == 8).
#
# TRY IT
#
#   1. HIGH = 6.0. Then HIGH = -2.0. Run each.
#   2. Change the test to  i % 3 == 0. The rhythm changes from 2 to 3.
#   3. Change  y = 0.0  to  y = z  and run. Still a zigzag — in plan now.
#   4. Add a third state with elif:
#
#          if i % 3 == 0:
#              z = LOW
#          elif i % 3 == 1:
#              z = HIGH
#          else:
#              z = HIGH * 0.5
#
#      elif is short for "else, if". Python tests each in order and stops
#      at the first one that is True.
#
#   5. Drive x instead of z:  if i % 2 == 0: x = i * STEP  else: x = i * STEP * 0.4
#      Same rule, different property. Ask what else a condition could drive:
#      spacing, rotation, whether a point exists at all.
#
# WHAT A CONDITIONAL IS FOR
#
#   This zigzag jumps between two fixed states. There is no in-between.
#   That is what a conditional does — it sorts things into cases.
#
#   Sorting into cases is exactly what Assignment 2A asks for when it
#   requires a filter that removes or modifies a subset of profiles based
#   on a tested property. Same operator, larger geometry.
#
#   For variation with an in-between, you need script 5.
#
# BREAK IT  — run these to see the real errors
#
#   a) Write  if i % 2 = 0:
#         SyntaxError — one equals sign assigns, it cannot ask a question.
#
#   b) Delete the  else:  branch entirely.
#
#      NO ERROR APPEARS — and the result is flat. Every z is LOW.
#
#      Trace it. On pass 0, i is even, so z = LOW. On pass 1, i is odd,
#      nothing assigns z — but z still holds LOW from the pass before.
#      Python does not clear it between iterations. The odd points quietly
#      inherit the previous point's height, and the zigzag disappears.
#
#      Now change the loop to  for i in range(1, COUNT):  so it starts on
#      an odd number, and run again:
#
#          NameError: name 'z' is not defined
#
#      Same missing else. Same bug. One version crashes and one version
#      lies, and which you get depends only on where the loop starts.
#
#      An if without an else is a hole. Ask what your code does on the
#      pass where the condition is False — that is where wrong geometry
#      comes from.
#
#   c) Indent the  else:  to line up with  z = LOW  instead of  if.
#         SyntaxError: invalid syntax
# =======================================================================
