# ARC 3133 — Module 1: POINT
# Script 3 of 5 — The loop, and the edge
#
# Two new ideas, and they belong together.
#
#   A loop repeats the same instruction with a different value each time.
#   An edge is a pair of INDEX NUMBERS — it does not store positions, it
#   stores which two vertices in the list to connect.
#
# From here on the object is visible in Object Mode. Edges draw; loose
# vertices do not.

import bpy
import random

NAME = "03_loop_and_edges"

# ---- PARAMETERS -------------------------------------------------------

COUNT = 20        # how many points        <- change this one first
STEP = 1.0        # distance between them along X
JITTER = 0.0      # sideways wander in Y
HEIGHT = 3.0      # vertical range

SEED = 1

# ---- LOGIC ------------------------------------------------------------

random.seed(SEED)

points = []                        # start empty
for i in range(COUNT):             # i counts 0, 1, 2, ... COUNT-1
    x = i * STEP                   # each point steps further along X
    y = random.uniform(-JITTER, JITTER)
    z = random.uniform(0.0, HEIGHT)
    points.append((x, y, z))       # add this point to the end of the list

edges = []                         # start empty
for i in range(COUNT - 1):         # one fewer edge than there are points
    edges.append((i, i + 1))       # connect point i to the next one

print("points:", len(points))
print("edges: ", len(edges))
print("first edge:", edges[0], "-> joins", points[0], "and", points[1])

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])        # vertices, edges, faces
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# WHY COUNT - 1
#
#   Five fence posts, four gaps. Twenty points, nineteen edges.
#   Write range(COUNT) instead and the last pass asks for point number 20,
#   which does not exist — the list stops at 19. See BREAK IT below.
#
# THE IDEA THAT MATTERS
#
#   points  holds WHERE things are      (0.0, 0.3, 2.1)
#   edges   holds WHAT CONNECTS         (0, 1)
#
#   An edge never stores a position. It stores two index numbers. Move a
#   point and the edge follows, because the edge only ever knew the index.
#
#   That separation — positions in one list, relationships in another — is
#   the whole of Module 2. Sections, toolpaths, and waffle joints are all
#   this same split.
#
# TRY IT
#
#   1. COUNT = 200. Run. Then COUNT = 2000. The code did not change.
#      This is what you could not do by hand in script 2.
#   2. JITTER = 2.0. Run.
#   3. Comment out the edge loop with a # on each line. Run.
#      The object goes invisible in Object Mode — the points are still
#      there, but there is nothing to draw.
#   4. Change the edge line to  edges.append((i, i + 2))  and run range
#      to COUNT - 2. What did you make?
#   5. Add one last edge after the loop:  edges.append((COUNT - 1, 0))
#      The line closes into a loop.
#
# BREAK IT  — run these. Verified in Blender; the first one is the important one.
#
#   a) Change the second loop to  for i in range(COUNT):
#
#      NO ERROR APPEARS. Nothing turns red. The script reports success.
#
#      What actually happened: the last pass asked for an edge between
#      vertex 19 and vertex 20, and vertex 20 was never made. Blender
#      built that edge anyway, pointing at nothing. The mesh is corrupt.
#
#      Add this line after mesh.update() and run again:
#
#          print("problems found:", mesh.validate())
#
#      It prints True, silently deletes the bad edge, and your edge count
#      drops from 20 to 19 — the number it should have been.
#
#      This is the most important failure in the module, because it is
#      the one that does not announce itself. Wrong geometry that runs is
#      more expensive than code that crashes: the crash costs you an
#      afternoon, the corrupt mesh costs you a print. Manifold checking in
#      Tutorial 0.3 is this same problem at fabrication scale.
#
#   b) Delete the colon at the end of  for i in range(COUNT)
#         SyntaxError: expected ':'
#         Python's most common beginner error. It names the line.
#
#   c) Remove the indent on the  x = i * STEP  line
#         IndentationError: expected an indented block
#         Indentation is not style in Python. It is the syntax.
# =======================================================================
