"""
in count_x s d=12 n=2
in count_y s d=8 n=2
in spacing s d=1.0 n=2
out vertex v
out edges s
"""
# A loop inside a loop makes a field.
# The points are connected in the order they were made, so this is also a
# path — and the order comes from which loop is on the outside.
#
# SWAP THE TWO for LINES and run again. Not one point moves. The drawing
# combs vertically instead of horizontally.

nx = int(count_x)
ny = int(count_y)

for j in range(ny):             # outer — moves slowly
    for i in range(nx):         # inner — runs all the way, every time
        vertex.append([i * spacing, j * spacing, 0.0])

for k in range(len(vertex) - 1):
    edges.append((k, k + 1))
