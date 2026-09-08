"""
in count_x s d=30 n=2
in count_y s d=20 n=2
in spacing s d=1.0 n=2
in target v
in reach s d=14.0 n=2
in height s d=5.0 n=2
in shape s d=1.0 n=2
out vertex v
out edges s
"""
# remap() converts a value from one range into another.
# Distance 0..reach becomes height 0..HEIGHT. State your ranges on the
# sheet — write remap() and the code states them for you.
#
# shape: 1 linear · 2 sharp · 0.5 soft

import math


def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))


if target:
    tgt = target[0][0]
else:
    tgt = [15.0, 10.0, 0.0]

for i in range(int(count_x)):
    for j in range(int(count_y)):
        x = i * spacing
        y = j * spacing

        d = math.dist((x, y, 0.0), tgt)

        t = remap(d, 0.0, reach, 1.0, 0.0)   # 1 at the target, 0 at reach
        t = clamp(t, 0.0, 1.0)               # nothing outside 0..1
        t = t ** shape                       # bend the curve

        vertex.append([x, y, remap(t, 0.0, 1.0, 0.0, height)])
