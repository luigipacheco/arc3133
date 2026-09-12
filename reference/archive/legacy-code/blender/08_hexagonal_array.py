# ARC 3133 — Module 1: POINT
# Script 8 of 14 — The hexagonal array
#
# A rectangular grid with two changes:
#
#   1. Every other row shifts sideways by half a step.
#   2. The rows sit closer together, by sqrt(3)/2.
#
# The second one is the part people skip. Do only the shift and the points
# are not equidistant — they only look as though they are.

import bpy
import math

NAME = "08_hex_array"

# ---- PARAMETERS -------------------------------------------------------

COUNT_X = 16
COUNT_Y = 12
SPACING = 1.0

# ---- LOGIC ------------------------------------------------------------

ROW_SPACING = SPACING * math.sqrt(3.0) / 2.0     # 0.866 — see the note

points = []
for j in range(COUNT_Y):

    if j % 2 == 0:
        offset = 0.0                      # even rows start at zero
    else:
        offset = SPACING * 0.5            # odd rows start half a step over

    for i in range(COUNT_X):
        points.append((i * SPACING + offset, j * ROW_SPACING, 0.0))

edges = []
for k in range(len(points) - 1):
    edges.append((k, k + 1))

# is it really hexagonal? measure two neighbours of point 0
print("points:", len(points))
print("to the right:   ", round(math.dist(points[0], points[1]), 4))
print("to the row above:", round(math.dist(points[0], points[COUNT_X]), 4))

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# WHERE sqrt(3)/2 COMES FROM
#
#   Three neighbouring points form an equilateral triangle of side
#   SPACING. The point above sits half a step across and some height up:
#
#       (SPACING/2)^2 + height^2 = SPACING^2
#       height = SPACING * sqrt(3)/2 = 0.866
#
#   Replace ROW_SPACING with plain SPACING and read the console. The two
#   distances stop matching — 1.0 and 1.118. A 13% error your eye will not
#   catch. It still looks like a staggered grid. It is not a hex grid.
#
#   This is the most common quiet mistake in a panelised facade: the
#   pattern reads fine on screen and the panels do not fit. Read the
#   numbers, not the picture.
#
# THE SERPENTINE BONUS
#
#   Draw odd rows backwards:
#
#       if j % 2 == 1:
#           step = COUNT_X - 1 - i
#       else:
#           step = i
#       points.append((step * SPACING + offset, j * ROW_SPACING, 0.0))
#
#   Because odd rows are already offset by half a step, the turn at each
#   end is short and even, and the whole field draws in one stroke with no
#   travel moves at all. Compare with the square grid in script 6, where
#   the same turn is abrupt.
#
#   Of the three arrays this is the best one for a plotter, and the reason
#   is geometric rather than a matter of taste. That is the kind of claim
#   Assignment 1B wants you making.
#
# TRY IT
#
#   1. COUNT_X = 40, COUNT_Y = 30. Over a thousand points, one stroke.
#   2. Skip every third row — inside the outer loop:  if j % 3 == 2: continue
#   3. Keep this grid. In Module 3 you will map a panel onto every point.
#
# math.dist
#
#   Returns the straight-line distance between two points. Here it only
#   checks the packing. In script 9 it becomes the subject.
# =======================================================================
