"""
in count s d=20 n=2
in step s d=1.0 n=2
in low s d=0.0 n=2
in high s d=2.0 n=2
out vertex v
out edges s
"""
# The conditional. The loop still runs the same number of times —
# what changes is that each pass now makes a decision.
#
#   %   the remainder after dividing.  7 % 2 is 1.  8 % 2 is 0.
#   ==  asks a question.  =  assigns a value. They are different.

n = int(count)

for i in range(n):
    if i % 2 == 0:              # is i even?
        z = low
    else:
        z = high
    vertex.append([i * step, 0.0, z])

for i in range(n - 1):
    edges.append((i, i + 1))
