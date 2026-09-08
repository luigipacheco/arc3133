# ARC 3133 — Module 1: POINT
# Script 12 of 14 — Several attractors, read from a collection
#
# Every object inside the named collection is an attractor. Duplicate an
# empty in the viewport and there are more of them; delete one and there
# are fewer. The code never changes.
#
# One attractor asks one question per point. Several ask one question per
# point PER ATTRACTOR — a third loop, inside the two that build the grid.
#
# Then a decision has to be made, and it is a design decision:
# given four answers, which number do you keep?
#
#   max   only the nearest attractor matters — sharp territories
#   sum   influences add up and reinforce where they overlap
#   avg   a smooth blend; nothing dominates, nothing accumulates

import bpy
import math

NAME = "12_multi_attractor"

# ---- THE TOOLKIT ------------------------------------------------------

def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))

# ---- PARAMETERS -------------------------------------------------------

ATTRACTOR_GROUP = "Attractors"     # every object in here is an attractor

COUNT_X = 40
COUNT_Y = 26
SPACING = 1.0

REACH = 14.0
SHAPE = 1.0
HEIGHT = 5.0

# ---- FIND THE ATTRACTORS ----------------------------------------------

if ATTRACTOR_GROUP in bpy.data.collections:
    group = bpy.data.collections[ATTRACTOR_GROUP]
else:
    group = bpy.data.collections.new(ATTRACTOR_GROUP)
    bpy.context.scene.collection.children.link(group)
    for start in [(8.0, 6.0, 0.0), (30.0, 8.0, 0.0),
                  (20.0, 20.0, 0.0), (36.0, 22.0, 0.0)]:
        e = bpy.data.objects.new("attractor", None)
        e.empty_display_size = 2.0
        e.location = start
        group.objects.link(e)
    print("made", ATTRACTOR_GROUP, "- move the empties and run again")

attractors = []
for ob in group.objects:
    attractors.append(tuple(ob.location))

# ---- LOGIC ------------------------------------------------------------

points = []
for i in range(COUNT_X):
    for j in range(COUNT_Y):
        x = i * SPACING
        y = j * SPACING

        influences = []                       # reset for every point
        for a in attractors:
            d = math.dist((x, y, 0.0), a)
            t = clamp(remap(d, 0.0, REACH, 1.0, 0.0), 0.0, 1.0)
            influences.append(t ** SHAPE)

        strength = max(influences)            # <- change this one first
        # strength = clamp(sum(influences), 0.0, 1.0)
        # strength = sum(influences) / len(influences)

        z = remap(strength, 0.0, 1.0, 0.0, HEIGHT)
        points.append((x, y, z))

edges = []

print("attractors found:", len(attractors))
print("points:", len(points),
      "· distance calculations:", len(points) * len(attractors))

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
#   Run once. Four empties appear in a collection called Attractors.
#   Select one, Shift-D to duplicate, drag it somewhere, run again — five
#   attractors. Delete two and run — three. Nothing in the script knows
#   how many there are, and that is the point.
#
#   A script that reads the scene instead of hardcoding it is a tool.
#   That distinction is what the Final Assignment is asking for.
#
# WHY max() MEANS "CLOSEST"
#
#   The influences were remapped so 1.0 is at an attractor and 0.0 is at
#   REACH. High influence means near, so the largest is the nearest.
#
#   ATLV's original writes it the long way, and it is worth writing once
#   because the pattern is everywhere:
#
#       nearest = -1
#       for a in attractors:
#           d = math.dist((x, y, 0.0), a)
#           if nearest < 0 or d < nearest:
#               nearest = d
#
#   The  nearest < 0  test handles the first pass, when there is nothing
#   to compare against yet.
#
# THE SEAMS
#
#   With max(), look at where influence changes hands. Those boundaries
#   are a Voronoi diagram, and you did not have to build one.
#
# THE COST
#
#   Read the console. 1,040 points times 4 attractors is 4,160 distance
#   calculations. Nested loops multiply. Duplicate the empties up to 20
#   and it is 20,800; go to a 100 x 100 grid as well and it is 200,000.
#   Do the multiplication before you run, not after.
#
# TRY IT
#
#   1. Uncomment each `strength` line in turn. Three fields, one system,
#      one line changed. The cheapest systematic exploration in the module
#      — document all three for 1A.
#   2. With sum, drag two empties close together. Their overlap goes
#      higher than either alone. Remove the clamp and it goes higher still.
#   3. Use the empties' scale as a weight — they are objects, so they
#      carry more than a position:
#
#          for ob in group.objects:
#              attractors.append((tuple(ob.location), ob.scale.x))
#
#      then multiply each influence by that number. Scale an empty up in
#      the viewport and it pulls harder. Make it negative and it pushes.
#   4. Point ATTRACTOR_GROUP at a collection of real objects rather than
#      empties — columns, trees, anything with a position.
#
# BREAK IT
#
#   a) Delete every object in the collection, leaving it empty, and run.
#      ValueError: max() arg is an empty sequence. An empty list is not
#      "no attractors, handled politely" — it is a question with no answer.
#
#   b) Move  influences = []  above the two grid loops.
#      No error. The list never resets, so every point inherits every
#      earlier point's influences, max() reaches 1.0 everywhere, and the
#      field goes flat at full height. Where you reset a list is what the
#      loop means.
# =======================================================================
