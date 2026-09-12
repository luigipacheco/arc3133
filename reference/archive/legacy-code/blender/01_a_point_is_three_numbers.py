# ARC 3133 — Module 1: POINT
# Script 1 of 5 — A point is three numbers
#
# A vertex is a position in space. That is all it is: three numbers, in order.
# Everything else this semester is a list of these.
#
# To see it: run the script, select the object, press TAB for Edit Mode.
# A single vertex has no surface, so there is nothing to shade in Object Mode.
# You are looking at data, not at an object yet.

import bpy

NAME = "01_a_point"

# ---- PARAMETERS -------------------------------------------------------
# Change one number, run again, watch what moves.

x = 0.0      # left (-) / right (+)
y = 0.0      # back (-) / forward (+)
z = 3.0      # down (-) / up (+)        <- change this one first

# ---- LOGIC ------------------------------------------------------------

point = (x, y, z)      # one vertex — three numbers, grouped in order
points = [point]       # a list, currently holding one vertex
edges = []             # no edges: a single point has nothing to connect to

print("points:", points)
print("how many:", len(points))

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])        # vertices, edges, faces
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# TRY IT
#
#   1. Set z to -3.0. Run. Which way did it go?
#   2. Set x to 5.0 and z back to 0.0. Run.
#   3. Add a second point by hand:
#
#          point_b = (2.0, 0.0, 2.0)
#          points  = [point, point_b]
#
#      Run, press TAB, and count the vertices.
#   4. Now imagine writing a thousand of these by hand.
#      That problem is what script 3 solves.
#
# THE VOCABULARY
#
#   variable    a name that holds a value            x = 0.0
#   float       a number with a decimal point        3.0
#   tuple       a fixed group, in order              (x, y, z)
#   list        a collection you can add to          [point]
#   index       the position of an item in a list    points[0]
#
# Order matters. (0, 0, 3) and (3, 0, 0) are different places.
#
# BREAK IT  — run these to see the real errors
#
#   a) Write  point = (x, y)  with only two numbers.
#         RuntimeError: internal error setting the array
#         A famously unhelpful message. It does not say "you gave me two
#         numbers and I need three" — but that is what it means. Some
#         errors name the problem; some only tell you where you were
#         standing when it happened.
#
#   b) Write  z = "3.0"  with quotes.
#         Runs without complaint, then fails at from_pydata. "3.0" is
#         text that looks like a number. Quotes make it a label, not a
#         quantity — you cannot measure with it.
# =======================================================================
