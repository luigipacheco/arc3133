# ARC 3133 — Module 1: POINT
# Script 10 of 14 — remap(): the function the rest of the course runs on
#
# Script 9 left you with a distance — a number between 0 and 18 that means
# nothing to a panel size. Remapping converts a value from one range into
# another:
#
#       distance 0 to 18   ->   height 5.0 to 0.0
#       distance 0 to 18   ->   scale 1.0 to 0.1
#
# Same measurement, different result, because the output range changed.
# Assignment 1A asks you to state your ranges on the sheet. Write remap()
# and the code states them for you.
#
# This is also where you write your first function.

import bpy
import math

NAME = "10_remap"

# ---- THE TOOLKIT — copy these into every script from here on ----------

def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)      # where value sits, 0 to 1
    return out_min + t * (out_max - out_min)      # same position, new range


def clamp(value, low, high):
    return max(low, min(high, value))

# ---- PARAMETERS -------------------------------------------------------

COUNT_X = 30
COUNT_Y = 20
SPACING = 1.0

TARGET = (15.0, 10.0, 0.0)
REACH = 14.0            # distance at which the effect has faded to nothing

HEIGHT = 5.0            # height at the target        <- change this one first
SHAPE = 1.0             # 1 linear · 2 sharp · 0.5 soft

# ---- LOGIC ------------------------------------------------------------

points = []
for i in range(COUNT_X):
    for j in range(COUNT_Y):
        x = i * SPACING
        y = j * SPACING

        d = math.dist((x, y, 0.0), TARGET)

        t = remap(d, 0.0, REACH, 1.0, 0.0)    # 1 at the target, 0 at REACH
        t = clamp(t, 0.0, 1.0)                # nothing outside 0..1
        t = t ** SHAPE                        # bend the curve

        z = remap(t, 0.0, 1.0, 0.0, HEIGHT)   # 0..1 -> the range you want

        points.append((x, y, z))

edges = []

print("input range: 0.0 to", REACH, " ->  output range: 0.0 to", HEIGHT)
print("check — remap(0.5, 0, 1, 10, 20) should be 15.0 ->",
      remap(0.5, 0.0, 1.0, 10.0, 20.0))

# ---- OUTPUT — identical in every script in this module -----------------

if NAME in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects[NAME], do_unlink=True)

mesh = bpy.data.meshes.new(NAME)
mesh.from_pydata(points, edges, [])
mesh.update()

obj = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(obj)


# =======================================================================
# READING  def
#
#       def remap(value, in_min, in_max, out_min, out_max):
#           ...
#           return out_min + t * (out_max - out_min)
#
#   def       here is a new instruction I am defining
#   remap     the name you will call it by
#   (...)     the inputs it expects, in order
#   return    the answer it hands back
#
#   Defining a function does nothing. It runs when you call it. The `t`
#   inside remap has nothing to do with any `t` outside it.
#
#   This is the difference between a result and a tool, which is what the
#   Final Assignment is asking for.
#
# THE THREE-LINE PATTERN
#
#       t = remap(measurement, in_min, in_max, 1.0, 0.0)
#       t = clamp(t, 0.0, 1.0)
#       result = remap(t, 0.0, 1.0, out_min, out_max)
#
#   Measure, normalise to 0..1, stretch to the range you want. Passing
#   through 0..1 in the middle is what lets you change the output range
#   without touching anything else.
#
# TRY IT
#
#   1. SHAPE = 1.0, then 2.0, then 0.5, then 4.0. The geometry is
#      identical every time — only the curve between measurement and
#      result changed. Four images, one system. That is 1A's "systematic
#      exploration", for the price of one number.
#   2. REACH = 5.0, then 50.0. Local incident versus overall tilt.
#   3. Swap the last remap to  (t, 0.0, 1.0, HEIGHT, 0.0). A crater.
#   4. Drive something else. Replace z with a spacing:
#          x = i * remap(t, 0.0, 1.0, 1.0, 0.3)
#      Density instead of form, from the same measurement.
#
# BREAK IT
#
#   a) Delete the clamp line and set REACH = 6.0.
#      No error. Points beyond REACH get a negative t, and with SHAPE = 0.5
#      Python then tries the square root of a negative number. Sometimes
#      you get sunken geometry; sometimes a complex number arrives three
#      lines later. Unclamped remapping is the most common quiet bug in
#      attractor code.
#
#   b) Set REACH = 0.0.
#      ZeroDivisionError, from inside remap. The function trusts you. Add
#      a guard as its first line and it becomes a tool other people can
#      run:
#
#          if in_max == in_min:
#              return out_min
#
#   c) Call  remap(d, 0.0, REACH)  with three arguments.
#      TypeError: remap() missing 2 required positional arguments
# =======================================================================
