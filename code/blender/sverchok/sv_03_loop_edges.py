"""
in count s d=20 n=2
in step s d=1.0 n=2
in jitter s d=0.0 n=2
in height s d=3.0 n=2
in seed s d=1 n=2
out vertex v
out edges s
"""
# The loop, and the edge.
# An edge stores two INDEX NUMBERS, not positions. Move a point and the
# edge follows, because the edge only ever knew the index.

import random

random.seed(int(seed))
n = int(count)

for i in range(n):
    x = i * step
    y = random.uniform(-jitter, jitter)
    z = random.uniform(0.0, height)
    vertex.append([x, y, z])

for i in range(n - 1):          # one fewer edge than there are points
    edges.append((i, i + 1))
