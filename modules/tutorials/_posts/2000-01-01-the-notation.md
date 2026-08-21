---
title: 01 · The Notation
published: true
---

The pseudocode notation used from Class 2 onward.

```
PRIMITIVES          TRANSFORMS               BOOLEANS
box(x, y, z)        move(s, x, y, z)         union(a, b)
cylinder(r, h)      rotate(s, axis, deg)     subtract(a, b)
sphere(r)           scale(s, factor)         intersect(a, b)
cone(r, h)
```

## Three rules

**Every shape is created centred on the origin (0, 0, 0).** Position is expressed as a move from there. This removes the question "where is it?" — every position is stated relative to a known place.

**Units are abstract.** `3` units, not 3 metres. The procedure is scale-independent, and works at any size.

**Every step assigns a name.** `subtract(mass, void)` can only mean one thing. `"subtract the cylinder"` never could.

## Example

```
base   = box(6, 4, 3)
tower  = box(2, 2, 6)
tower  = move(tower, 2, 0, 3)
void   = cylinder(r=1, h=5)
void   = move(void, -1.5, 0, 0)

mass   = union(base, tower)
result = subtract(mass, void)
```

## Why formal notation

LeWitt's instructions were ambiguous on purpose — different executors, different drawings, and that variance was the work.

Yours must produce **one** result. Named assignment fixes the order of operations; origin-centred creation fixes position. What ambiguity remains is precise and fixable, which is what the Class 5 exchange exposes.

[OpenSCAD](https://openscad.org/) is a working language built on exactly these operations, if you want to try the real thing.

