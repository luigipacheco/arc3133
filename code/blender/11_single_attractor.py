# ARC 3133 — Module 1: POINT
# Script 11 of 14 — One attractor, read from the scene
#
# Everything is in place: an array (6, 7, 8), a measurement (9), and a way
# to convert it (10). An attractor is those three wired together.
#
# The attractor is not typed into the code. It is an OBJECT in the scene,
# found by name. Move the empty in the viewport, run the script again, and
# the field follows it. That loop — drag, run, look — is how you will work
# for the rest of the semester.

import bpy
import math

NAME = "11_single_attractor"

# ---- THE TOOLKIT ------------------------------------------------------

def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))

# ---- PARAMETERS -------------------------------------------------------

ATTRACTOR_NAME = "Attractor"      # the object the field measures itself against

COUNT_X = 36
COUNT_Y = 24
SPACING = 1.0

REACH = 16.0
SHAPE = 1.0             # 1 linear · 2 sharp · 0.5 soft

HEIGHT = 5.0            # height at the attractor      <- change this first
SIZE_NEAR = 1.0         # stored per point, used in script 14
SIZE_FAR = 0.15

# ---- FIND THE ATTRACTOR -----------------------------------------------

if ATTRACTOR_NAME in bpy.data.objects:
    target = bpy.data.objects[ATTRACTOR_NAME]
else:
    target = bpy.data.objects.new(ATTRACTOR_NAME, None)   # None makes an Empty
    target.empty_display_size = 2.0
    target.location = (18.0, 12.0, 0.0)
    bpy.context.collection.objects.link(target)
    print("made an Empty called", ATTRACTOR_NAME, "- move it and run again")

attractor = tuple(target.location)        # three plain numbers

# ---- LOGIC ------------------------------------------------------------

points = []
sizes = []

for i in range(COUNT_X):
    for j in range(COUNT_Y):
        x = i * SPACING
        y = j * SPACING

        d = math.dist((x, y, 0.0), attractor)

        t = remap(d, 0.0, REACH, 1.0, 0.0)      # 1 at the attractor
        t = clamp(t, 0.0, 1.0)
        t = t ** SHAPE

        z = remap(t, 0.0, 1.0, 0.0, HEIGHT)
        size = remap(t, 0.0, 1.0, SIZE_FAR, SIZE_NEAR)

        points.append((x, y, z))
        sizes.append(size)

edges = []

print("attractor at:", [round(v, 2) for v in attractor])
print("points:", len(points), "· size range:",
      round(min(sizes), 3), "to", round(max(sizes), 3))

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)

# store size on every vertex so it travels with the geometry
attr = mesh.attributes.new(name="size", type="FLOAT", domain="POINT")
attr.data.foreach_set("value", sizes)
mesh.update()


# =======================================================================
# HOW TO WORK WITH THIS
#
#   Run once. An Empty called Attractor appears. Move it anywhere — G to
#   grab — and run the script again. The field rebuilds around wherever
#   you left it.
#
#   Drag, run, look. Do it ten times before you change any other number.
#
# WHY tuple()
#
#       attractor = tuple(target.location)
#
#   target.location is a Blender Vector. tuple() turns it into three plain
#   numbers, which is what math.dist expects — and it takes a COPY, so the
#   value cannot change underneath the loop.
#
#   There is a second way to ask where an object is: matrix_world.
#   location is the position relative to a parent; matrix_world is the
#   position in the scene. They are identical until you parent something.
#
#   Be careful with matrix_world on an object your script has only just
#   created: Blender does not recalculate it until its next update, so it
#   reads (0, 0, 0) for the rest of that run and is correct the second
#   time. A bug that only appears on the first run is a bad one to meet
#   under critique. location does not have this problem.
#
# WHY t RUNS BACKWARDS
#
#       t = remap(d, 0.0, REACH, 1.0, 0.0)
#
#   Read the output range: 1.0 at distance zero, 0.0 at REACH. Near the
#   attractor t is high, so everything downstream reads naturally — 1.0
#   means fully affected.
#
#   Swap it to 0.0, 1.0 and every effect inverts. Same attractor, opposite
#   field. Both are legitimate. Know which you chose.
#
# WHAT AN ATTRIBUTE IS
#
#   `sizes` is a Python list and disappears when the script ends. The
#   attribute written at the bottom is stored on the geometry — it saves
#   with the file and Geometry Nodes can read it.
#
#   Select the object, open the Spreadsheet editor, find the `size` column
#   beside the positions. That table is what your script produced, and it
#   is your Week 5 bridge: Python writes the field, Geometry Nodes reads it.
#
# TRY IT
#
#   1. Drag the attractor off the edge of the grid. A distant attractor
#      reads as a tilt, not an event.
#   2. Drag it UP, off the plane. The peak flattens, because nothing on
#      the grid can reach distance zero any more.
#   3. REACH = 6.0, then 40.0. SHAPE = 2.0, then 0.5.
#   4. Point ATTRACTOR_NAME at something else already in your scene — the
#      camera, a cube. Any object has a position.
#   5. Add the third parameter — pull the points toward the attractor:
#
#          amount = remap(t, 0.0, 1.0, 0.0, 0.45)
#          x = x + (attractor[0] - x) * amount
#          y = y + (attractor[1] - y) * amount
#
#      (attractor[0] - x) is the whole trip; multiplying takes a fraction
#      of it. Set 0.45 to 1.0 and everything inside REACH lands on the
#      attractor. Worth seeing once.
#
# BREAK IT
#
#   a) Delete the Empty in the viewport, then run.
#      No error — the script simply makes a new one at the default
#      position, and your careful placement is gone. Convenient and
#      dangerous. Decide whether a script should create what it cannot
#      find, or stop and tell you.
#
#   b) foreach_set("value", sizes[:10]).
#      RuntimeError. One value per vertex, exactly. `points` and `sizes`
#      stay in step only because they are appended on the same pass.
# =======================================================================
