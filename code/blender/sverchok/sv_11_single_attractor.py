"""
in count_x s d=36 n=2
in count_y s d=24 n=2
in spacing s d=1.0 n=2
in attractor v
in reach s d=16.0 n=2
in shape s d=1.0 n=2
in height s d=5.0 n=2
in pull s d=0.0 n=2
out vertex v
out edges s
"""
# An array, a measurement, and a way to convert it — wired together.
# Two parameters driven by one distance: height, and how far each point
# slides toward the attractor.
#
# Feed `attractor` from a Vector In, or from an Objects In node so you can
# drag an empty in the viewport.

import math


def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))


if attractor:
    a = attractor[0][0]
else:
    a = [18.0, 12.0, 0.0]

for i in range(int(count_x)):
    for j in range(int(count_y)):
        x = i * spacing
        y = j * spacing

        d = math.dist((x, y, 0.0), a)

        t = clamp(remap(d, 0.0, reach, 1.0, 0.0), 0.0, 1.0) ** shape

        z = remap(t, 0.0, 1.0, 0.0, height)

        # pull toward the attractor — (a[0] - x) is the whole trip,
        # multiplying takes a fraction of it
        amount = remap(t, 0.0, 1.0, 0.0, pull)
        x = x + (a[0] - x) * amount
        y = y + (a[1] - y) * amount

        vertex.append([x, y, z])
