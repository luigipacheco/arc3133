# Introduction-to-Generative-Design.blend: handover

Interactive lecture for ARC 3133 Viz 1, Project 4 (generative). One scene per slide, same method as `BLENDER-INTERACTIVE-SLIDES.md` and the sister decks `Introduction-to-Procedural-Design.blend` and `Introduction-to-Parametric-Design.blend`.

- File: `files/blender/Introduction-to-Generative-Design.blend` (Blender 5.2.4)
- Built by script: `_tools/generative_slidekit.py` (registers `GK`) and `_tools/generative_build.py` (registers `GB`). Run `blender_slidekit.py`, `procedural_slidekit.py`, `generative_slidekit.py`, then `generative_build.py`. `GB['groups']()` rebuilds the shared groups (then rebuild every slide, the groups are replaced), `GB['s07']()` rebuilds one slide and resets its values. Static slides 20 to 22 are text objects only (`static_slide`); delete their `· rN` text objects before rebuilding one, or the lines are doubled.
- Test renders: `_check/GEN_00.png` to `GEN_21.png`
- Last updated: 3 November 2026

## Definitions used

- Procedural: the steps (instructions in order). Parametric: relationships (parameters). Generative: a rule that iterates on its own result and explores a solution space you have not mapped, returning answers you did not anticipate.
- Cards are plain-word rules with live values (START / RULE / REPEAT where it fits) plus where it lives in Blender and Grasshopper. No Python.

## Slides

Controls: **L** = `GeometryNodes` modifier (lesson), **U** = `UI` modifier (display only). Part 1 (01 to 18) explains generative systems; Part 2 (19 to 21) is the Project 4 exercise.

| Scene | Idea | Controls |
|---|---|---|
| 00 Title | title, 21 chips | none |
| 01 Generative | the definition (a solution space you have not mapped, answers you did not anticipate); Langton's ant: two rules, no randomness, a highway after about 10,000 steps | L: Steps, Size |
| 02 Noise | random (no memory of neighbours) vs noise (smooth); seed makes both repeatable | L: Mode, Seed, Scale |
| 03 Threshold | noise above Threshold becomes solid: floor 0 of what follows; % solid | L: Threshold, Seed, Scale |
| 04 One Rule | Wolfram's elementary cellular automata (1983): a cell and its two neighbours make one of 8 patterns, the rule number in binary answers each; live rule table | L: Rule, Width, Generations, Start, Seed |
| 05 Neighbours | the 8 neighbours of a picked cell and their alive count | L: Density, Seed, Column, Row |
| 06 Game of Life | Conway (1970): born with exactly 3, survives with 2 or 3, otherwise dies; noise start, step through generations | L: Generation, Seed, Threshold, Born, Survive Min, Survive Max |
| 07 Stack | time becomes height: each generation a layer; default Born 4 / Survive 3 to 6 tapers gently | L: Generations, Seed, Threshold, Born, Survive Min/Max, Layer Height |
| 08 Environment | the attractor limits where cells may live (Reach); move `Attractor - move me` | L: Attractor, Reach, Seed, Threshold, Generations |
| 09 Agents | walkers turn, walk, leave trails; Steer follows the noise field; Height turns time into height | L: Agents, Steps, Turn, Steer, Seed, Height |
| 10 Stigmergy | walkers deposit a trail on the ground, the ground fades and spreads, walkers steer to the strongest trail ahead (ants, slime mould) | L: Agents, Steps, Sense, Decay, Seed |
| 11 Reaction Diffusion | Gray-Scott on a 120 x 120 grid; Spots, Maze, Coral, Worms presets (about 1.5 s to evaluate) | L: Pattern, Steps, Seed |
| 12 Growth | DLA-like: a cell joins when exactly one of its 4 sides touches a grown cell, with Chance; colour = when it joined | L: Steps, Chance, Seed, Height |
| 13 Differential Growth | rebuilt on Nov 3 from Luis's working reference (`geonodes/sim/differential_growth_z.blend`): each iteration, Curve to Points then Merge by Distance (Reach) gives one point every Reach m; Geometry Proximity finds the nearest; each point steps away from it (Map Range: Repel x 0.01 at 0 m, 0 at 2 m); Blur Attribute on the step (weight 1) makes neighbours move together; flatten to XY; Resample at Spacing adds points. Stable and fast (300 it about 1.1k points, 1000 it about 7.5k points, about 1 s). Height keeps a layer every Every iterations, Layer Height apart, so the history stacks into a coral-like object; ISO camera. UI-only Solid turns every layer into a wall one layer tall | L: Iterations, Spacing, Reach, Repel, Seed, Height, Layer Height, Every; UI: Solid |
| 14 Physics | a net relaxes under gravity (Blur Attribute on position + a drop per iteration, pinned points held): hanging form, Flip makes the compression shell (Gaudi, Frei Otto, Kangaroo) | L: Gravity, Iterations, Pins (Edges default), Flip |
| 15 Noise Field | noise as a generator, from Luis's `sdfexperimetns.blend`: 4D Voronoi distance to edge x Cell Size minus Wall is a signed distance field (negative inside thin walls, the empty cells read as rooms); box SDFs for the store (8 x 6 x 3.5 m at y = 2, open to the +y face), a floor slab and the site; Combine menu: intersect = smooth max(a, b), subtract = smooth max(a, -b), union = smooth min(a, b), Blend = smoothing; always intersected with the site box so the mesh closes; Cube Grid Topology (10 x 8 x 4.5 m, Voxel) + Field to Grid + Grid to Mesh at 0. About 1 s at Voxel 0.12. UI: white smooth mass, store box as a pink ghost | L: Cell Size, Wall, Seed, Combine (Keep the store, Cut the store out, Add a floor, Field only), Blend, Voxel |
| 16 Reading | slice a layer: floor below, clearance from walls, headroom above; pink = room for a space, area in m² | L: Layer, Clearance, Headroom, Seed, Threshold |
| 17 Design Space | 5 x 5 matrix of automata: columns Threshold, rows Seed; pick one (pink) | L: Threshold From/To, Seed, Generations, Pick Column/Row |
| 18 Breed | the parent in the middle, 8 children nudged by Mutation; pick again | L: Parent Seed, Parent Threshold, Mutation, Generations, Pick |
| 19 Plan Section | the generated volume cut like a building: plan (layers above removed, snapped to a layer) and section (cells beyond Section X removed); the cut faces are painted pink | L: Plan Level, Section X, Show, Seed, Threshold |
| 20 Exercise | static: Project 4 Generative Store, the six strategies, the dates (Nov 10 approval, Dec 11 final) | none |
| 21 Three Sheets | static: the system 5%, the design space 5%, the proposal 20%; booklet 15% | none |
| 22 Rubric | static: the competition-sheet rubric (nine criteria) | none |

## Shared node groups

- `Cell Grid` (Columns, Rows, Cell): one point per cell, index = column x Rows + row; stores `column`, `row`.
- `Noise Value` (Seed, Scale): noise at each position, stretched to 0..1.
- `Neighbour` (Geometry, Columns, Rows, Name, DX, DY) and `Count Neighbours` (8 of them added).
- `Life Rule` (Columns, Rows, Born, Survive Min, Survive Max, Allowed): one generation, stores `alive`.
- `Automaton`: floor 0 from noise inside the environment (Center, Reach), then a Repeat zone that keeps each generation as a layer (`Cells` points with `alive`, `generation`) and as extruded plates (`Volume`), and applies `Life Rule`. Outputs Volume, Cells, Last.

## Notes

- Reaction-diffusion: the Laplacian is Blur Attribute minus the value (factor 1.0); 1.25 is unstable.
- Anything that inserts points each iteration must grow slowly or be capped; the first differential growth (springs) hung Blender twice on November 2. The Nov 3 rebuild grows about linearly and needs no cap.
- Loading data from a .blend on Google Drive (`bpy.data.libraries.load`) crashed Blender on Nov 3; inspect reference files with headless `bpy` (pip) in the cloud instead.
- Resample Curve has no `mode` property in 5.2: set `inputs['Mode'].default_value = 'Length'`.
- A driver on a menu input reads the item's internal value; `mirror()` subtracts the first value.
- Matrix and Breed run the Automaton inside a For Each zone (16 x 16 cells, 0.75 m) to stay fast.
- Reading: with the default rule most rooms found are terraces (floor below, open above). A "covered" filter is a possible next step.

## Lessons from Luis's reference files (G:\My Drive\Selflearn\blender\geonodes, reviewed 3 Nov 2026)

- **Merge by Distance is a neighbourhood average.** On a point cloud it merges points closer than the distance into one point at their centre (tested: points at x=0 and x=1, distance 1.5, give one point at 0.5). Both `differential_growth_z.blend` and `flock_v2_basic.blend` use it as a cheap "what is around me" before Geometry Proximity / Sample Nearest. Slide 13 now uses it.
- `sim/flock_v2_basic.blend`: Reynolds boids (separation, cohesion, alignment) with stored velocity, mixed each step; agents react to each other. Slide 09 walkers do not.
- `sim/antsim_curve.blend`: physarum-style stigmergy like slide 10, plus velocity with inertia, wrap-around edges, and Points to Volume then Volume to Mesh to turn the trails into a 3D object.
- `sim/reaction difusion.blend`: one value, short-range activation minus long-range inhibition (difference of two blurs), on any mesh, displaced along the normal: a 3D surface. Simpler to explain than Gray-Scott (slide 11).
- `sim/cellular_automata_gn.blend`, `cgol_v01.blend`: 1D, 2D and 3D automata with Keep Old States (time as height), seeding from an image, a pattern collection and an effector object that adds live cells.
- `relaxmesh.blend`: Verlet physics (velocity = position minus previous position, damped) plus relaxation and anti-shrink toward the rest shape, on any mesh. Slide 14 has no velocity and no anti-shrink.
- `sim/circlepacking.blend`, `sim/randomgrrowth1.blend`: greedy circle packing; branches that grow toward an attractor with a random turn.
- Loading these files with `bpy.data.libraries.load` from Google Drive crashed Blender. Read them headless (`pip install bpy==5.2.3` in the cloud) instead.
