# ARC 3133 — Module 1: POINT
# Script 9 of 14 — Distance
#
# Every attractor is this one question, asked once per point:
#
#       how far is this point from that one?
#
# The answer is a number attached to every point in the array. This script
# only measures it. Using it is script 10.

import bpy
import math

NAME = "09_distance"

# ---- PARAMETERS -------------------------------------------------------

COUNT_X = 30
COUNT_Y = 20
SPACING = 1.0

TARGET = (15.0, 10.0, 0.0)      # what everything measures itself against
SCALE = 0.25                    # how much the distance lifts each point

# ---- LOGIC ------------------------------------------------------------

points = []
for i in range(COUNT_X):
    for j in range(COUNT_Y):
        x = i * SPACING
        y = j * SPACING

        d = math.dist((x, y, 0.0), TARGET)      # <- the whole script

        points.append((x, y, d * SCALE))

edges = []

print("points:", len(points))
print("nearest: ", round(min(p[2] for p in points) / SCALE, 3))
print("furthest:", round(max(p[2] for p in points) / SCALE, 3))

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# WHAT math.dist DOES
#
#   Pythagoras in three dimensions. Written out:
#
#       dx = x - TARGET[0]
#       dy = y - TARGET[1]
#       dz = 0.0 - TARGET[2]
#       d  = math.sqrt(dx*dx + dy*dy + dz*dz)
#
#   Replace math.dist with those four lines and run. Identical result.
#   Use math.dist afterwards — but write it out once first.
#
# LOOK AT WHAT YOU MADE
#
#   Press TAB. The field lifts into a cone with its point at TARGET. That
#   cone IS the distance function, drawn. Every attractor in the next four
#   scripts is a modification of that shape.
#
# WHY THIS IS NOT YET USEFUL
#
#   Distance has no upper limit. Near TARGET it is 0; at the far corner it
#   is 18, or 40, or whatever the grid happens to be.
#
#   Nothing you want to drive works in those units. Panel scale wants 0.1
#   to 1.0. Rotation wants 0 to 90. Colour wants 0 to 1.
#
#   Converting between ranges is script 10, and it is the missing tool.
#
# TRY IT
#
#   1. Move TARGET to (0.0, 0.0, 0.0), then to a corner off the grid.
#   2. SCALE = -0.25. The cone inverts into a funnel.
#   3. Lift the target: TARGET = (15.0, 10.0, 20.0). The cone flattens,
#      because no point on the plane can now reach distance zero.
#   4. Make a hard edge instead of a gradient:
#
#          if d < 8.0:
#              z = 2.0
#          else:
#              z = 0.0
#
#      That is a filter — a conditional on a measured property. It is what
#      Assignment 2A asks for.
# =======================================================================
