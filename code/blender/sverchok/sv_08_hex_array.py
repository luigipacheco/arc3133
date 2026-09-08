"""
in count_x s d=16 n=2
in count_y s d=12 n=2
in spacing s d=1.0 n=2
out vertex v
out edges s
"""
# A rectangular grid with two changes:
#   1. every other row shifts sideways by half a step
#   2. the rows sit closer together, by sqrt(3)/2
#
# The second one is the part people skip. Replace ROW_SPACING with plain
# spacing and the neighbour distances stop matching — 1.0 and 1.118.
# A 13% error your eye will not catch, and panels that do not fit.

import math

ROW_SPACING = spacing * math.sqrt(3.0) / 2.0
nx = int(count_x)
ny = int(count_y)

for j in range(ny):

    if j % 2 == 0:
        offset = 0.0                    # even rows start at zero
    else:
        offset = spacing * 0.5          # odd rows start half a step over

    for i in range(nx):
        vertex.append([i * spacing + offset, j * ROW_SPACING, 0.0])

for k in range(len(vertex) - 1):
    edges.append((k, k + 1))
