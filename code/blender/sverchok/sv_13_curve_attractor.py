"""
in count_x s d=40 n=2
in count_y s d=26 n=2
in spacing s d=1.0 n=2
in curve v
in reach s d=7.0 n=2
in shape s d=1.0 n=2
in height s d=4.5 n=2
out vertex v
out edges s
"""
# A curve is a list of points, closely spaced.
# So distance to a curve is distance to the nearest point in that list —
# the closest-of-many loop, with the curve's vertices standing in for the
# attractors.
#
# Feed `curve` the vertex output of any node — the sinusoid, a circle,
# a Bezier, an Objects In. Resolution matters: a curve of eight points
# makes a lumpy ridge, because you are measuring to eight dots.

import math


def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))


if curve:
    samples = curve[0]
else:
    samples = []
    for s in range(120):                     # a sine curve, as a fallback
        x = (s / 119.0) * (int(count_x) - 1) * spacing
        samples.append([x, int(count_y) * 0.5 + 7.0 * math.sin(x * 0.18), 0.0])

for i in range(int(count_x)):
    for j in range(int(count_y)):
        x = i * spacing
        y = j * spacing

        nearest = -1.0                       # must start impossible, not small
        for c in samples:
            d = math.dist((x, y, 0.0), c)
            if nearest < 0.0 or d < nearest:
                nearest = d

        t = clamp(remap(nearest, 0.0, reach, 1.0, 0.0), 0.0, 1.0)
        vertex.append([x, y, remap(t ** shape, 0.0, 1.0, 0.0, height)])
