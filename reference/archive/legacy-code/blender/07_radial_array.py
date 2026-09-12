# ARC 3133 — Module 1: POINT
# Script 7 of 14 — The radial array
#
# A rectangular array asks how far along X and how far along Y.
# A radial array asks how far out, and at what angle.
#
#     x = radius * cos(angle)
#     y = radius * sin(angle)
#
# Two lines. Every circle, spiral, and rotation this semester is them.

import bpy
import math

NAME = "07_radial_array"

# ---- PARAMETERS -------------------------------------------------------

COUNT_AROUND = 24         # points per ring
COUNT_RINGS = 8
RADIUS_STEP = 1.0

# ---- LOGIC ------------------------------------------------------------

FULL_TURN = math.pi * 2.0            # a whole circle in radians, about 6.283

points = []
for r in range(COUNT_RINGS):                 # outer — one ring at a time
    for a in range(COUNT_AROUND):            # inner — around the ring
        radius = (r + 1) * RADIUS_STEP
        angle = (a / COUNT_AROUND) * FULL_TURN
        points.append((radius * math.cos(angle),
                       radius * math.sin(angle),
                       0.0))

edges = []
for k in range(len(points) - 1):
    edges.append((k, k + 1))

print("points:", len(points))
print("angle step:", round(360.0 / COUNT_AROUND, 2), "degrees")

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# RADIANS
#
#   sin and cos take radians, not degrees. A full circle is 2 x pi.
#   (a / COUNT_AROUND) * FULL_TURN divides the circle into equal steps.
#   The loop stops one short of a full turn, so no point lands twice.
#
#   To think in degrees:  angle = math.radians(45)
#
# SWAP THE LOOPS
#
#   Put  a  on the outside and  r  on the inside. Same points — but the
#   path now runs out along a spoke, back, out along the next. Rings
#   become a starburst.
#
#   Then make the return sweep useful: draw odd spokes inward instead of
#   outward and the pen never lifts.
#
# THE DENSITY YOU DID NOT ASK FOR
#
#   Every ring has the same number of points, but outer rings are longer —
#   so their points are further apart. There is a density gradient in this
#   field and nothing in the code says so.
#
#   To even it out, let the count follow the radius:
#
#       count = COUNT_AROUND * (r + 1)
#
#   and use count in place of COUNT_AROUND in both the range and the angle.
#
#   Neither version is correct. They are two different fields. 1A is
#   assessed on density and gradient — know which one you made.
#
# TRY IT
#
#   1. Offset each ring to make a spiral: add  + r * 0.3  to the angle.
#   2. COUNT_RINGS = 1, COUNT_AROUND = 300, and multiply the angle by 5
#      with  z = a * 0.05. A helix.
#   3. Lift into a cone: use  r * 0.5  as the z value.
#
# BREAK IT
#
#   Use  math.cos(a)  instead of  math.cos(angle).
#   No error — a ragged arc instead of a ring, because `a` counts points
#   and radians do not care how many you wanted. Wrong units, plausible
#   result.
# =======================================================================
