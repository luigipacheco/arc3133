"""
in count_x s d=40 n=2
in count_y s d=26 n=2
in spacing s d=1.0 n=2
in attractors v
in reach s d=14.0 n=2
in shape s d=1.0 n=2
in height s d=5.0 n=2
in mode s d=0 n=2
out vertex v
out edges s
"""
# Several attractors: a loop inside a loop inside a loop.
# Given four answers, which number do you keep? That is a design decision.
#
#   mode 0  max  — only the nearest matters, sharp territories (Voronoi)
#   mode 1  sum  — influences add and reinforce where they overlap
#   mode 2  avg  — a smooth blend, nothing dominates
#
# Feed `attractors` a Vector In with several vectors, or an Objects In.
# Add or remove points upstream and the code never changes.

import math


def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))


if attractors:
    pts = attractors[0]
else:
    pts = [[8.0, 6.0, 0.0], [30.0, 8.0, 0.0],
           [20.0, 20.0, 0.0], [36.0, 22.0, 0.0]]

m = int(mode)

for i in range(int(count_x)):
    for j in range(int(count_y)):
        x = i * spacing
        y = j * spacing

        influences = []                      # reset for every point
        for a in pts:
            d = math.dist((x, y, 0.0), a)
            t = clamp(remap(d, 0.0, reach, 1.0, 0.0), 0.0, 1.0)
            influences.append(t ** shape)

        if m == 0:
            strength = max(influences)
        elif m == 1:
            strength = clamp(sum(influences), 0.0, 1.0)
        else:
            strength = sum(influences) / len(influences)

        vertex.append([x, y, remap(strength, 0.0, 1.0, 0.0, height)])
