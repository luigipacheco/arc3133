"""
in count_around s d=24 n=2
in count_rings s d=8 n=2
in radius_step s d=1.0 n=2
in spiral s d=0.0 n=2
out vertex v
out edges s
"""
# Polar coordinates:
#
#     x = radius * cos(angle)
#     y = radius * sin(angle)
#
# sin and cos take RADIANS, not degrees. A full circle is 2 * pi.
# Swap the two loops and rings become spokes.

import math

FULL_TURN = math.pi * 2.0
na = int(count_around)
nr = int(count_rings)

for r in range(nr):
    for a in range(na):
        radius = (r + 1) * radius_step
        angle = (a / na) * FULL_TURN + r * spiral
        vertex.append([radius * math.cos(angle),
                       radius * math.sin(angle),
                       0.0])

for k in range(len(vertex) - 1):
    edges.append((k, k + 1))
