"""
in count_x s d=30 n=2
in count_y s d=20 n=2
in spacing s d=1.0 n=2
in target v
in scale s d=0.25 n=2
out vertex v
out edges s
"""
# Every attractor is this one question, asked once per point:
# how far is this point from that one?
#
# Feed `target` from a Vector In node. Sverchok hands vertex sockets over
# nested as [ [ [x,y,z], ... ] ], so take [0] to get the list of points.

import math

if target:
    tgt = target[0][0]
else:
    tgt = [15.0, 10.0, 0.0]         # fallback so the node works unlinked

for i in range(int(count_x)):
    for j in range(int(count_y)):
        x = i * spacing
        y = j * spacing
        d = math.dist((x, y, 0.0), tgt)
        vertex.append([x, y, d * scale])
