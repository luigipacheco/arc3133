# ARC 3133 — Module 1: POINT
# Script 6 of 14 — The rectangular array
#
# A loop inside a loop makes a field of points.
# The points are connected in the order they were made, so the object is
# also a path — and the order comes from which loop is on the outside.

import bpy

NAME = "06_rect_array"

# ---- PARAMETERS -------------------------------------------------------

COUNT_X = 12
COUNT_Y = 8
SPACING = 1.0

# ---- LOGIC ------------------------------------------------------------

points = []
for j in range(COUNT_Y):              # outer — moves slowly
    for i in range(COUNT_X):          # inner — runs all the way, every time
        points.append((i * SPACING, j * SPACING, 0.0))

edges = []
for k in range(len(points) - 1):      # join each point to the next
    edges.append((k, k + 1))

print("points:", len(points), "=", COUNT_X, "x", COUNT_Y)

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# SWAP THE LOOPS
#
#   Change the two for lines to:
#
#       for i in range(COUNT_X):
#           for j in range(COUNT_Y):
#
#   Run. Not one point moved. The drawing is completely different — it
#   combs vertically instead of horizontally.
#
#   Nested loops decide where the points are AND what order they are made
#   in. Order is invisible in a point field and obvious in a path.
#
# THAT PATH IS A TOOLPATH
#
#   A plotter draws in the order you send it. The long line running back
#   across the field at the end of each row is a real stroke.
#
#   Draw odd rows backwards and it disappears. Inside the inner loop:
#
#       if j % 2 == 1:
#           step = COUNT_X - 1 - i
#       else:
#           step = i
#       points.append((step * SPACING, j * SPACING, 0.0))
#
#   Same points, one continuous stroke, no wasted travel. This is
#   Assignment 1B, met in Week 4.
#
# TRY IT
#
#   1. COUNT_X = 40, COUNT_Y = 25 — Assignment 1A's thousand elements.
#   2. Delete the edge loop. Press TAB. The field is still there.
#   3. Add height:  import math  at the top, then
#      z = math.sin(i * 0.5) * math.cos(j * 0.5)  in the append.
#
# BREAK IT
#
#   Change the edge loop to  range(len(points)).
#   No error, nothing turns red. The last edge points at a vertex that was
#   never made. Add  print(mesh.validate())  after mesh.update() — it
#   prints True and quietly deletes it. Wrong geometry that runs costs
#   more than code that crashes.
# =======================================================================
