# ARC 3133 — Module 1: POINT
# Script 13 of 14 — The curve attractor
#
# A curve in this course is not a mathematical object. It is a list of
# points, closely spaced.
#
# So distance to a curve is distance to the nearest point in that list —
# script 12's closest-of-many loop, with the curve's vertices standing in
# for the attractors.
#
# The curve is read from an object in the scene by name. Run script 5 and
# point this at 05_sinusoid, or script 7 and point it at a spiral, or
# model a polyline by hand. Anything with vertices will do.

import bpy
import math

NAME = "13_curve_attractor"

# ---- THE TOOLKIT ------------------------------------------------------

def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))

# ---- PARAMETERS -------------------------------------------------------

CURVE_NAME = "Attractor_Curve"     # the object the field measures against

COUNT_X = 40
COUNT_Y = 26
SPACING = 1.0

REACH = 7.0
SHAPE = 1.0
HEIGHT = 4.5

# ---- FIND THE CURVE ---------------------------------------------------

if CURVE_NAME in bpy.data.objects:
    source = bpy.data.objects[CURVE_NAME]
else:
    # no curve yet — build a sine one, exactly as script 5 did
    verts = []
    segs = []
    for s in range(120):
        t = s / 119.0
        x = t * (COUNT_X - 1) * SPACING
        verts.append((x, COUNT_Y * 0.5 + 7.0 * math.sin(x * 0.18), 0.0))
        if s > 0:
            segs.append((s - 1, s))
    cm = bpy.data.meshes.new(CURVE_NAME)
    cm.from_pydata(verts, segs, [])
    cm.update()
    source = bpy.data.objects.new(CURVE_NAME, cm)
    bpy.context.collection.objects.link(source)
    print("made", CURVE_NAME, "- edit it and run again")

# read its vertices, in world space
# (matrix_world is safe here — either the curve already existed, or this
#  script just built it at the origin, where matrix_world is the identity)
curve = []
for v in source.data.vertices:
    curve.append(tuple(source.matrix_world @ v.co))

# ---- LOGIC ------------------------------------------------------------

points = []
for i in range(COUNT_X):
    for j in range(COUNT_Y):
        x = i * SPACING
        y = j * SPACING

        nearest = -1.0                        # closest vertex on the curve
        for c in curve:
            d = math.dist((x, y, 0.0), c)
            if nearest < 0.0 or d < nearest:
                nearest = d

        t = clamp(remap(nearest, 0.0, REACH, 1.0, 0.0), 0.0, 1.0)
        z = remap(t ** SHAPE, 0.0, 1.0, 0.0, HEIGHT)

        points.append((x, y, z))

edges = []

print("curve:", CURVE_NAME, "with", len(curve), "vertices")
print("distance calculations:", len(points) * len(curve))

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# HOW TO WORK WITH THIS
#
#   Run once and a sine curve appears. Then TAB into it, drag its vertices
#   around, TAB out, and run again. The field reshapes to whatever you
#   drew. You can also move or rotate the whole object — matrix_world
#   handles that.
#
#   Or point CURVE_NAME at 05_sinusoid, or at 07_radial_array, and measure
#   the field against something you generated rather than drew.
#
# WHY matrix_world @ v.co
#
#   v.co is the vertex position in the object's OWN space — as if the
#   object sat at the origin, unrotated. Multiplying by matrix_world moves
#   it into scene space.
#
#   Skip it and the field ignores wherever you dragged the curve, which
#   looks like the script is broken when it is doing exactly what you
#   asked. The @ symbol is matrix multiplication.
#
# RESOLUTION CHANGES THE ANSWER
#
#   Make a curve with only eight vertices and run. The ridge goes lumpy —
#   it bulges at each vertex and pinches between them, because the field
#   is measuring distance to eight dots, not to a curve.
#
#   Script 5 made this point about how a curve is drawn. Here it changes
#   what gets measured, and therefore the geometry.
#
# THE COST
#
#   1,040 points against 120 vertices is 124,800 distance calculations —
#   thirty times script 12 — for one number per point. It still runs
#   instantly at this size, so take the count as arithmetic rather than a
#   warning: the total is points x vertices, and you set both. Subdivide
#   the curve to 500 and use a 100 x 100 grid and it is five million.
#
# TRY IT
#
#   1. SHAPE = 3.0, REACH = 4.0. A hard ridge instead of a swell.
#   2. Swap the first remap's output to 0.0, 1.0 — the curve becomes a
#      trench cut through a raised field.
#   3. Point CURVE_NAME at a circle: run script 7 with COUNT_RINGS = 1.
#   4. Two curves. Read a second object, measure both, and combine them
#      with script 12's max / sum / average decision.
#   5. Distribute ON the curve instead of measuring to it. `curve` is
#      already a list of positions — that is the fourth array type 1A asks
#      for.
#
# BREAK IT
#
#   a) Delete  source.matrix_world @  and leave just  v.co. Then move the
#      curve object in the viewport and run.
#      No error. The field stays where the curve used to be. Object space
#      and world space are not the same space, and nothing will remind you.
#
#   b) Set  nearest = 0.0  instead of -1.0 as the starting value.
#      No error, and the field goes flat at full height. Nothing is ever
#      closer than zero, so the test never fires and `nearest` stays 0 —
#      which reads as "on the curve" everywhere. The starting value of a
#      running minimum has to be impossible, not merely small.
# =======================================================================
