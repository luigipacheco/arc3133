"""
in count s d=20 n=2
in seed s d=1 n=2
in spread s d=5.0 n=2
in height s d=2.0 n=2
out vertex v
out edges s
"""
# Random points. Same seed -> same points, every run.
# Unseeded randomness means the thing on screen is not the thing you
# showed last week.

import random

random.seed(int(seed))

for i in range(int(count)):
    x = random.uniform(-spread, spread)
    y = random.uniform(-spread, spread)
    z = random.uniform(0.0, height)
    vertex.append([x, y, z])
