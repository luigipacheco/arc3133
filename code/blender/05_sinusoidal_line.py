# ARC 3133 — Module 1: POINT
# Script 5 of 5 — The sine wave: continuous variation
#
# Script 4 chose between two heights. This one calculates the height.
#
#   math.sin() takes a number and returns a value that rises and falls
#   smoothly between -1 and +1, forever.
#
# The difference is the whole reason this script exists. A conditional
# sorts into cases. A function varies continuously. A value that varies
# continuously across space has a name: a FIELD. That is Tutorial 1.2.

import bpy
import math

NAME = "05_sinusoid"

# ---- PARAMETERS -------------------------------------------------------

COUNT = 60          # how many points — this is RESOLUTION, see below
STEP = 0.2          # distance between them along X
AMPLITUDE = 2.0     # how tall the wave is       <- change this one first
FREQUENCY = 0.5     # how tight the wave is
PHASE = 0.0         # shifts the whole wave along its length

# ---- LOGIC ------------------------------------------------------------

points = []
for i in range(COUNT):
    x = i * STEP
    y = 0.0
    z = AMPLITUDE * math.sin(x * FREQUENCY + PHASE)
    points.append((x, y, z))

edges = []
for i in range(COUNT - 1):
    edges.append((i, i + 1))

print("points:", len(points))
print("length along X:", (COUNT - 1) * STEP)
print("highest point:", max(p[2] for p in points))

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])        # vertices, edges, faces
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# RESOLUTION — the architectural lesson in this script
#
#   There is no curve here. There is a polyline pretending to be one.
#   Set COUNT = 8 and run: you can see the straight segments. Set
#   COUNT = 200 and it reads as smooth. Nothing about the shape changed,
#   only how finely it was sampled.
#
#   Every curve you fabricate this semester is sampled at some resolution.
#   The plotter draws segments. The laser cuts segments. The slicer reads
#   segments. Choosing COUNT is choosing how much of the curve survives
#   contact with the machine, and it is a decision you make, not a default
#   you inherit.
#
# WHY x AND NOT i
#
#   The wave is driven by  x * FREQUENCY, not  i * FREQUENCY.
#
#   Drive it with i and the wave changes shape every time you change STEP,
#   because i counts points while x measures distance. Drive it with x and
#   the wave keeps its real-world size no matter how finely you sample it.
#
#   Sample count and geometry should be independent. Try it both ways.
#
# TRY IT
#
#   1. AMPLITUDE = 0.5, then 5.0.
#   2. FREQUENCY = 2.0, then 0.1.
#   3. PHASE = 1.57 (a quarter turn). The wave slides along.
#   4. Give y its own wave, out of phase with z:
#
#          y = AMPLITUDE * math.cos(x * FREQUENCY)
#
#      The line leaves the plane. You have made a helix.
#
#   5. Make the amplitude grow along the line:
#
#          z = (AMPLITUDE * x * 0.1) * math.sin(x * FREQUENCY)
#
#      The wave now varies twice — once along its length, once in height.
#
#   6. Combine scripts 4 and 5. Keep the sine, but only place a point when
#      i % 2 == 0. A continuous rule, sampled conditionally.
#
# WHERE THIS GOES
#
#   Assignment 1A requires an explicit remapping operation with its input
#   and output ranges stated on the sheet. This script is the first half
#   of one: sin() hands you a value from -1 to +1, and AMPLITUDE stretches
#   it to the range you want.
#
#   Write that stretch as a named function and you have remap(), which is
#   the tool the rest of the module runs on.
#
# BREAK IT  — run these to see the real errors
#
#   a) Delete the  import math  line.
#         NameError: name 'math' is not defined
#         Python does not load the maths library unless you ask.
#
#   b) Write  math.sin(x, FREQUENCY)  with a comma instead of  * .
#         TypeError: math.sin() takes exactly one argument (2 given)
#         Reading the argument count out of an error message is a skill.
#
#   c) Set  STEP = "0.2"  in quotes.
#         TypeError: can't multiply sequence by non-int of type 'float'
#         "0.2" is text that looks like a number. Data types are not
#         decoration.
# =======================================================================
