"""
in count_x s d=24 n=2
in count_y s d=16 n=2
in spacing s d=1.0 n=2
in attractor v
in reach s d=12.0 n=2
in shape s d=1.0 n=2
in size_near s d=0.85 n=2
in size_far s d=0.12 n=2
in twist s d=90.0 n=2
in height s d=3.0 n=2
out vertex v
out edges s
"""
# From points to geometry, without leaving Python.
#
# A box is built at every point, scaled, rotated and lifted by the same
# distance. Everything is merged into ONE vertex list, so each box's edge
# indices have to be shifted by however many vertices came before it.
#
# That offset is the whole lesson. It is also how every Sverchok node that
# joins meshes works underneath.

import math


def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(value, low, high):
    return max(low, min(high, value))


if attractor:
    a = attractor[0][0]
else:
    a = [12.0, 8.0, 0.0]

h = 0.5
UNIT = [(-h, -h, -h), (h, -h, -h), (h, h, -h), (-h, h, -h),
        (-h, -h, h), (h, -h, h), (h, h, h), (-h, h, h)]
WIRE = [(0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)]

for i in range(int(count_x)):
    for j in range(int(count_y)):
        x = i * spacing
        y = j * spacing

        d = math.dist((x, y, 0.0), a)
        t = clamp(remap(d, 0.0, reach, 1.0, 0.0), 0.0, 1.0) ** shape

        s = remap(t, 0.0, 1.0, size_far, size_near)
        angle = math.radians(remap(t, 0.0, 1.0, 0.0, twist))
        z = remap(t, 0.0, 1.0, 0.0, height)

        offset = len(vertex)                 # how many verts came before

        for vx, vy, vz in UNIT:
            sx, sy = vx * s, vy * s          # scale
            rx = sx * math.cos(angle) - sy * math.sin(angle)   # rotate
            ry = sx * math.sin(angle) + sy * math.cos(angle)
            vertex.append([x + rx, y + ry, z + vz * s])        # move

        for e0, e1 in WIRE:
            edges.append((e0 + offset, e1 + offset))
