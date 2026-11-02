# Introduction-to-Generative-Design.blend: handover

Interactive lecture for ARC 3133 Viz 1, Project 4 (generative). One scene per slide, same method as `BLENDER-INTERACTIVE-SLIDES.md` and the sister decks `Introduction-to-Procedural-Design.blend` and `Introduction-to-Parametric-Design.blend`.

- File: `files/blender/Introduction-to-Generative-Design.blend` (Blender 5.2.4)
- Built by script: `_tools/generative_slidekit.py` (registers `GK`) and `_tools/generative_build.py` (registers `GB`). Run `blender_slidekit.py`, `procedural_slidekit.py`, `generative_slidekit.py`, then `generative_build.py`. `GB['groups']()` rebuilds the shared groups (then rebuild every slide, the groups are replaced), `GB['s07']()` rebuilds one slide and resets its values.
- Test renders: `_check/GEN_00.png` to `GEN_15.png`
- Last updated: 2 November 2026

## Definitions used

- Procedural: the steps (instructions in order). Parametric: relationships (parameters). Generative: a rule that iterates on its own result and explores a solution space you have not mapped, returning answers you did not anticipate.
- Cards are plain-word rules with live values (START / RULE / REPEAT where it fits) plus where it lives in Blender and Grasshopper. No Python.

## Slides

Controls: **L** = `GeometryNodes` modifier (lesson), **U** = `UI` modifier (display only).

| Scene | Idea | Controls |
|---|---|---|
| 00 Title | title, 15 chips | none |
| 01 Generative | the definition; start + rule + repeat: a square turned and scaled 30 times (start square pink) | L: Size, Turn, Shrink, Iterations |
| 02 Noise | random (no memory of neighbours) vs noise (smooth); seed makes both repeatable; bars coloured by value | L: Mode, Seed, Scale |
| 03 Threshold | noise above Threshold becomes solid: floor 0 of what follows; % solid | L: Threshold, Seed, Scale |
| 04 One Rule | Wolfram's elementary cellular automata (1983): a cell and its two neighbours make one of 8 patterns, the rule number in binary answers each; rows downward, live rule table | L: Rule, Width, Generations, Start, Seed |
| 05 Neighbours | the 8 neighbours of a picked cell and their alive count | L: Density, Seed, Column, Row |
| 06 Game of Life | Conway's Game of Life (1970): born with exactly 3, survives with 2 or 3, otherwise dies (loneliness or crowding); noise start, step through generations | L: Generation, Seed, Threshold, Born, Survive Min, Survive Max |
| 07 Stack | time becomes height: each generation a layer; default rule Born 4 / Survive 3 to 6 tapers gently (Life B3/S23 thins out fast) | L: Generations, Seed, Threshold, Born, Survive Min/Max, Layer Height |
| 08 Environment | the attractor limits where cells may live (Reach); move `Attractor - move me` | L: Attractor, Reach, Seed, Threshold, Generations |
| 09 Agents | walkers turn a little, walk, leave trails; Steer follows the noise field; Height turns time into height | L: Agents, Steps, Turn, Steer, Seed, Height |
| 10 Reaction Diffusion | Gray-Scott on a 120 x 120 grid; Spots, Maze, Coral, Worms presets (about 1.5 s to evaluate) | L: Pattern, Steps, Seed |
| 11 Growth | a cell joins when exactly one of its 4 sides touches a grown cell, with Chance; colour = when it joined | L: Steps, Chance, Seed, Height |
| 12 Reading | slice a layer: floor below, clearance from walls, headroom above; pink = room for a space, area in m² | L: Layer, Clearance, Headroom, Seed, Threshold |
| 13 Design Space | 5 x 5 matrix of automata: columns Threshold, rows Seed; pick one (pink) | L: Threshold From/To, Seed, Generations, Pick Column/Row |
| 14 Breed | the parent in the middle, 8 children nudged by Mutation (threshold, noise scale); pick again | L: Parent Seed, Parent Threshold, Mutation, Generations, Pick |
| 15 Layer Sheet | one generation = one sheet: Sheet x Scale gives layer height and sheet count | L: Height, Sheet, Scale, Seed, Threshold. U: Explode |

## Shared node groups

- `Cell Grid` (Columns, Rows, Cell): one point per cell, index = column x Rows + row; stores `column`, `row`.
- `Noise Value` (Seed, Scale): noise at each position, stretched to 0..1.
- `Neighbour` (Geometry, Columns, Rows, Name, DX, DY) and `Count Neighbours` (8 of them added).
- `Life Rule` (Columns, Rows, Born, Survive Min, Survive Max, Allowed): one generation, stores `alive`.
- `Automaton`: floor 0 from noise inside the environment (Center, Reach), then a Repeat zone that keeps each generation as a layer (`Cells` points with `alive`, `generation`) and as extruded plates (`Volume`), and applies `Life Rule`. Outputs Volume, Cells, Last.

## Notes

- Reaction-diffusion: the Laplacian is Blur Attribute minus the value (factor 1.0); 1.25 is unstable.
- Matrix and Breed run the Automaton inside a For Each zone (16 x 16 cells, 0.75 m) to stay fast.
- Reading: with the default rule most rooms found are terraces (floor below, open above). A "covered" filter is a possible next step.
