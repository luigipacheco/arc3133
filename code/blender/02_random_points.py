# ARC 3133 — Module 1: POINT
# Script 2 of 5 — Random points, written out by hand
#
# Same structure as script 1. One thing changed: the numbers are no longer
# typed in, they are asked for. random.uniform(a, b) returns a number
# somewhere between a and b.
#
# Note how tedious four points already is. That is the point of this script.
#
# To see them: run, select the object, press TAB for Edit Mode.

import bpy
import random

NAME = "02_random_points"

# ---- PARAMETERS -------------------------------------------------------

SEED = 1          # change for a different set of points
SPREAD = 5.0      # how far from the origin points may land
HEIGHT = 2.0      # vertical range

# ---- LOGIC ------------------------------------------------------------

random.seed(SEED)          # same seed -> same points, every single run

point_a = (random.uniform(-SPREAD, SPREAD),
           random.uniform(-SPREAD, SPREAD),
           random.uniform(0.0, HEIGHT))

point_b = (random.uniform(-SPREAD, SPREAD),
           random.uniform(-SPREAD, SPREAD),
           random.uniform(0.0, HEIGHT))

point_c = (random.uniform(-SPREAD, SPREAD),
           random.uniform(-SPREAD, SPREAD),
           random.uniform(0.0, HEIGHT))

point_d = (random.uniform(-SPREAD, SPREAD),
           random.uniform(-SPREAD, SPREAD),
           random.uniform(0.0, HEIGHT))

points = [point_a, point_b, point_c, point_d]
edges = []

for p in points:
    print(p)

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])        # vertices, edges, faces
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# WHY THE SEED
#
#   Delete the random.seed(SEED) line and run three times. Different points
#   every run. Now put it back and run three times. Identical every run.
#
#   From Week 8 you will modify your own work live, in front of the room.
#   Unseeded randomness means the thing on screen is not the thing you
#   showed last week. Seed everything. Write the seed on your sheet.
#
# TRY IT
#
#   1. SEED = 2, then 3, then 7. Keep the one you like.
#   2. Set HEIGHT to 0.0. What kind of distribution is that now?
#   3. Add point_e by hand. Add it to the list. Run.
#   4. Now add ninety-six more.
#
#      You won't — and that is the argument for script 3.
#
# RANDOM IS NOT DESIGN
#
#   random.uniform gives every position an equal chance. That is a
#   distribution, not a composition. Nothing here is denser anywhere,
#   nothing responds to anything. Making a field respond is Tutorial 1.2.
# =======================================================================
