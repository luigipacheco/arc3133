# ARC 3133 — Course Materials Development Brief

Context for developing per-class presentations and example code. Pair this with the syllabus (`ARC3133_Viz1_Syllabus_Fall2026.md`) as project knowledge.

---

## What is being built

For each of eleven tutorials: a **pre-recorded video**, its **example code**, and a **class presentation**.

Class format is flipped — students watch the tutorial before the session. Class time is: questions and troubleshooting → assignment briefing → supervised work and critique. **The deck supports the live session, not the video.** It does not re-teach the tutorial.

## Two tracks per tutorial

Every tutorial ships in two versions implementing the same logic:

- **Blender track** — Blender Python (`bpy`), plus Geometry Nodes where the tutorial calls for it
- **Grasshopper track** — Grasshopper Python and native components

Currently prioritizing the **Blender Python track**.

## Existing material

A prior YouTube series, *Introduction to Computational Design with Blender*, was built on **Sverchok Scripted Node**. Sverchok is not one of the four environments in the syllabus. The decision: **that series' Python is the source material for the Blender Python track** — same language, different host. Port the logic into `bpy` scripts run from Blender's text editor. Geometry Nodes versions are recorded fresh.

Historical reference for the Grasshopper track: ATLV / Satoru Sugihara, http://atlv.org/education/ghpython/ — well-structured, but IronPython 2 from the Rhino 5 era. Does not run as written (`print` without parens; integer-division behavior changed). Cite for attribution; port before use.

---

## Tutorial list

| # | Tutorial | Released | Covers |
|---|---|---|---|
| 0.1 | 3D Transformations — 10-cube challenge | Wk 1 | Translate, rotate, scale |
| 0.2 | CSG Operations in Graphs | Wk 2 | Boolean union / difference / intersection, non-destructive |
| 0.3 | 3D Printing Basics | Wk 3 | Manifold checking, orientation, supports, layer height, slicing |
| 1.1 | Arrays | Wk 4 | Rectangular · radial · hexagonal · along a curve |
| 1.2 | Attractors | Wk 5 | Single-point, multi-point, curve; distance, falloff, remapping |
| 1.3 | Toolpath Logic | Wk 6 | Direction, ordering, retraction, pen up/down, running the plotter |
| 2.1 | Contour Curves from SDF Solids | Wk 9 | Signed distance fields, isosurfaces, contour extraction |
| 2.2 | 2D Fabrication | Wk 10 | Waffle logic, registration, kerf, tolerance, nesting, labeling |
| 3.1 | Panelization + Tessellation | Wk 12 | Tissue Tessellate / Box Morph; UV domains, variation |
| 3.2 | Fabrication Strategies | Wk 13 | Panel connections, thickness, orientation, batching, production planning |
| 4.1 | Tool Building with AI Assistance | Wk 12 | Pseudocode → code; verifying output; named inputs |

---

## Constraints that shape the code

**Python is the primary tool taught.** Concepts are introduced as code first, then shown to transfer to node graphs. Example code should be readable over clever — students met their first loop in Week 3.

**Concept sequence by module:**
- Module 1 — lists, arrays, fields. Variables, data types, lists, indexing, loops, functions, randomization, distance and falloff
- Module 2 — section and sequence. Iteration, conditionals, Boolean logic, filtering, ranges, geometric intersection, SDFs
- Module 3 — modularity and tessellation. Nested loops, grids as lists of lists, UV coordinates, mapping and remapping

**Prohibited in student work** (so tutorials must build these by hand):
- 1A — array add-ons, scatter tools, preset attractor falloff
- 2A/2B — automated contour and sectioning, one-click waffle generators
- 3A/3B — panelization libraries permitted for the tessellation; their preset gradient/attractor components are not
- All sheets — Canva and template-driven layout tools

**Weeks 1–7 are AI-free for students.** Tutorials in that window should be followable without an assistant.

**Assessment is live modification.** From Week 8, students change their own work unscripted in front of the class. Example code must be structured so that a single parameter change produces a visible, explicable result — write for modifiability, not just for the final image.

---

## Deck structure

Roughly 8–12 slides per session:

1. Title — tutorial number and what it covered
2. Recap — the logic in three or four steps, no syntax
3. Common failure points — errors expected from the tutorial, and what causes them
4. The assignment — requirements as stated in the syllabus, verbatim
5. Examples — precedent or prior student work
6. Live demo placeholder — what gets shown on screen
7. Work time and pin-up order

Visual identity: students each build their own; the course deck should have its own consistent one.

---

## Working method

- The **Blender connector** can execute `bpy` in a live session and capture viewport screenshots. Write code, run it, verify the geometry, then use the render for slide imagery.
- One chat per tutorial. Produce: tested script, commented teaching version, deck, and any starter file students receive.
- Every script needs a deliberately broken variant — the failure-points slide should show real errors, not invented ones.
