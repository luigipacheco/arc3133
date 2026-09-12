---
title: Tutorial 2.2 — Building a Mesh from Lists
published: true
---

# Tutorial 2.2 — Building a Mesh from Lists

| | |
|---|---|
| **Module** | 2 |
| **Released after** | Week 4 |
| **Reviewed** | Week 5 |
| **Feeds** | 2.1 Panel from Lists |

Geometry described rather than drawn. This is the slowest idea in the course to land and the one everything else rests on.

## What it covers

- `v = [x, y, z]` → `e = [v1, v2]` → `f = [v1, v2, v3]` → `mesh = [f1, f2, f3 …]`
- Winding order and normals — why the same three vertices can face either way
- Reading a panel off a precedent and rebuilding it vertex by vertex
- Where booleans are allowed to finish the job, and where they are a shortcut past the lesson

## Scripts

Tested Blender Python scripts for this tutorial live in [`code/blender/`](https://github.com/luigipacheco/arc3133/tree/main/code/blender). Each has a `PARAMETERS` block at the top and `TRY IT` / `BREAK IT` sections at the bottom.

- `03_for_loop_and_edges.py`
- `04_zigzag_if_statement.py`
- `05_sinusoidal_line.py`

Sverchok SNLite versions of most of these are in `code/blender/sverchok/`.

---

*Recording pending.*
