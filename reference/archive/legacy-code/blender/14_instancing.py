# ARC 3133 — Module 1: POINT
# Script 14 of 14 — From points to geometry
#
# Thirteen scripts have made vertices. Vertices do not render, do not cast
# shadows, and do not photograph. Assignment 1A needs images.
#
# This puts a real object at every point and varies it — scale, rotation,
# and colour, all driven by the same distance.
#
# The move that matters: every element shares ONE mesh. There is a single
# cube's worth of geometry in the file no matter how many you place. Each
# object is a name, a position, and a transform pointing at that mesh.
#
# This is instancing, written by hand. It is what the scatter add-ons
# prohibited by 1A are doing underneath.

import bpy
import math

NAME = "14_instanced_field"

# ---- THE TOOLKIT ------------------------------------------------------

def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))

# ---- PARAMETERS -------------------------------------------------------

ATTRACTOR_NAME = "Attractor"     # the same empty script 11 uses

COUNT_X = 24
COUNT_Y = 16
SPACING = 1.0

REACH = 12.0
SHAPE = 1.0

SCALE_NEAR = 0.85        # the three driven parameters   <- change these
SCALE_FAR = 0.12
TWIST = 90.0             # degrees of rotation at the attractor
HEIGHT = 3.0

# ---- FIND THE ATTRACTOR -----------------------------------------------

if ATTRACTOR_NAME in bpy.data.objects:
    target = bpy.data.objects[ATTRACTOR_NAME]
else:
    target = bpy.data.objects.new(ATTRACTOR_NAME, None)
    target.empty_display_size = 2.0
    target.location = (12.0, 8.0, 0.0)
    bpy.context.collection.objects.link(target)

attractor = tuple(target.location)

# ---- SETUP: one mesh, one collection ----------------------------------

if NAME in bpy.data.collections:
    old = bpy.data.collections[NAME]
    for o in list(old.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.collections.remove(old)

group = bpy.data.collections.new(NAME)
bpy.context.scene.collection.children.link(group)

# the single piece of geometry every element points at
unit_name = NAME + "_unit"
if unit_name in bpy.data.meshes:
    bpy.data.meshes.remove(bpy.data.meshes[unit_name])

h = 0.5
unit = bpy.data.meshes.new(unit_name)
unit.from_pydata(
    [(-h, -h, -h), (h, -h, -h), (h, h, -h), (-h, h, -h),
     (-h, -h, h), (h, -h, h), (h, h, h), (-h, h, h)],
    [],
    [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
     (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)])
unit.update()

# ---- LOGIC ------------------------------------------------------------

for i in range(COUNT_X):
    for j in range(COUNT_Y):
        x = i * SPACING
        y = j * SPACING

        d = math.dist((x, y, 0.0), attractor)
        t = clamp(remap(d, 0.0, REACH, 1.0, 0.0), 0.0, 1.0) ** SHAPE

        scale = remap(t, 0.0, 1.0, SCALE_FAR, SCALE_NEAR)
        twist = remap(t, 0.0, 1.0, 0.0, TWIST)
        z = remap(t, 0.0, 1.0, 0.0, HEIGHT)

        o = bpy.data.objects.new("el_%03d_%03d" % (i, j), unit)
        o.location = (x, y, z)
        o.scale = (scale, scale, scale)
        o.rotation_euler = (0.0, 0.0, math.radians(twist))
        o.color = (t, 0.35, 1.0 - t, 1.0)          # colour, driven too
        group.objects.link(o)

print("attractor at:", [round(v, 2) for v in attractor])
print("elements:", COUNT_X * COUNT_Y, "· mesh datablocks used: 1")

# =======================================================================
# TO SEE THE COLOUR
#
#   Viewport shading dropdown, top right of the 3D view:
#   Solid -> Color -> Object.
#
# WHY THERE IS NO OUTPUT BLOCK
#
#   Every other script ended with the same six lines that built one mesh.
#   This one builds objects instead. The geometry was made once, at the
#   top, and every element refers to it.
#
#   Check it in the Outliner, Blender File view. One mesh, however many
#   objects. Change that mesh and every element changes at once.
#
# ON COUNTS
#
#   384 elements is comfortable. COUNT_X = 40 and COUNT_Y = 25 gives 1A's
#   thousand and stays usable. Past about 5,000 Blender begins to labour —
#   because of the object count, not the geometry.
#
#   Beyond that, stop making objects and make one mesh: transform the
#   cube's eight vertices in Python, append them all into one vertex list,
#   offsetting the face indices as you go. Everything you need for that is
#   in scripts 1, 6, and 11.
#
# THE ARGUMENT THIS SCRIPT MAKES
#
#   1A prohibits array add-ons, scatter tools, and preset falloff. Read
#   this and you can see what such a tool does: place, measure, remap,
#   transform. Four steps, none of them mysterious.
#
#   The prohibition is not there to make the work harder. It is there so
#   that when you reach for Tissue in Module 3, you know what it is doing
#   and can argue with it.
#
# TRY IT
#
#   1. Turn parameters off one at a time — SCALE_FAR = SCALE_NEAR, or
#      TWIST = 0.0. Which single parameter carries the image? That is what
#      1A is assessing.
#   2. COUNT_X = 40, COUNT_Y = 25 for the thousand-element requirement.
#   3. Use a mesh already in your file instead of the cube:
#
#          unit = bpy.data.objects["YourObject"].data
#
#      and delete the block that builds it. That is Module 3's
#      component-on-a-grid, reached from the other direction.
#   4. Rotate about X instead of Z. On a dense grid a small rotation reads
#      as shimmer rather than turning.
#   5. Swap the placement loop for script 7's radial or script 8's hex.
#      Three arrays times three attractor types is the matrix 1A asks for.
#
# BREAK IT
#
#   a) Delete the block that clears the previous run, then run three
#      times. No error — three overlapping fields, 1,152 objects, and only
#      the newest respond to your changes. A script that creates objects
#      must clean up after itself, or live modification in Week 8 becomes
#      archaeology.
#
#   b) Move the mesh-building lines inside the loop. No error, looks
#      identical — but every element now owns a copy of the geometry.
#      Check the Outliner: 384 meshes instead of 1. Then try a thousand
#      and watch the file size. Sharing data is not a detail.
# =======================================================================
