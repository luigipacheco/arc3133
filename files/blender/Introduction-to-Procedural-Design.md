# Introduction-to-Procedural-Design.blend: handover

Interactive lecture for ARC 3133 Viz 1, P2 (procedural: primitives, transformations, Boolean operations, ordered steps). One scene per slide. Same method as `BLENDER-INTERACTIVE-SLIDES.md` and the sister deck `Introduction-to-Parametric-Design.blend`.

- File: `files/blender/Introduction-to-Procedural-Design.blend` (Blender 5.2.4)
- Built by scripts, rebuildable slide by slide: `_tools/procedural_slidekit.py` (helpers, registers `PD`) and `_tools/procedural_build.py` (one function per slide, registers `PB`). Run `blender_slidekit.py`, then those two, then `PB['s05']()` rebuilds slide 05 (it resets that slide's values).
- Test renders: `_check/PROC_00.png` to `PROC_17.png` (not for students)
- Last updated: 2 November 2026

## Scope and rules for this deck

- Concept slides, KISS, tool-agnostic. **No Python on any slide**: every card is a numbered list of steps in plain words with the live values, plus one or two grey lines saying where the operation lives in Blender and Grasshopper (bare UI: transform keys, modifiers, components).
- Any procedural approach counts as long as every step stays live: the Blender modifier stack (Boolean, Solidify, Simple Deform), Geometry Nodes, or Grasshopper. No applied modifiers, no hand-edited mesh. Slide 15 makes this point.
- Goal of the unit: a BIG-style diagram of a precedent building (slides 16 and 17).
- Visual: white masses, black edges, pink only on what the step changed, grey ghosts for "before", cyan for planes. True isometric camera (54.7356, 0, 135) except 02 (top view).

## Slides

Controls: **L** = `GeometryNodes` modifier (lesson), **U** = `UI` modifier (display only).

| Scene | Idea | Controls | Card |
|---|---|---|---|
| 00 Title | title and 17 chips | none | none |
| 01 Three Ways | procedural (fixed steps, one result), parametric (steps with dials, a family of 5 towers), generative (a rule repeated on its own result: next floor = last floor turned and shrunk at random) | L: Mode, Floors, Twist, Iterations, Seed | the steps of the chosen mode |
| 02 LeWitt | the instruction is the work: place N points at random, connect each to its nearest neighbour (or to every other point). Seed plays the person who draws it | L: Count, Seed, Connect, Step | the instruction, current step in pink |
| 03 Parameter | a parameter is a named input; width, depth, height of a box, labelled on the edges | L: Width, Depth, Height | BOX width/depth/height |
| 04 Primitives | box, cylinder, cone, sphere, plane with their own parameters (cone with 4 sides = pyramid) | L: Primitive, Width, Depth, Height, Sides | primitive and its parameters |
| 05 Translate | move adds the same offset to every point; start at the origin, move from there; ghost + arrow + axes | L: Move | box, move x y z |
| 06 Rotate | axis + angle + pivot (origin); arc and axis line | L: Axis (default Z), Angle | rotate N° around axis |
| 07 Scale | factors per axis, from the pivot; ghost | L: Scale | scale x y z, resulting size |
| 08 Order | rotate then move vs move then rotate (swing around the origin); faint ghost of the other order | L: Order, Move X, Angle | the two steps in the chosen order |
| 09 Boolean | union, difference, intersection of the same A (box) and B (cylinder); Swap shows A minus B is not B minus A; "Boolean operation" vs "Boolean value" | L: Operation, Cutter Move, Cutter Radius, Swap | A, B, the operation |
| 10 Extrude | plan in, mass out: rectangle, circle, hexagon, star extruded by Height; pink footprint, arrow | L: Footprint, Width, Depth, Height | plan, extrude |
| 11 Split | a plane cuts a mass into bottom and top (two Booleans with one big box); cyan plane | L: Cut Height. U: Explode | box, split |
| 12 Shift Lift | move the top part after a split: shift (x, y) and lift (z); ghost + arrow | L: Cut Height, Shift X, Shift Y, Lift | 4 steps |
| 13 Taper | x and y scaled by height, 1 at the base, Top at the roof | L: Top | box, taper |
| 14 Twist | each floor turned by its height, 0 at the base, Twist at the roof | L: Twist, Floors | box, twist |
| 15 Keep It Live | non-destructive: box minus sphere; Applied freezes it (Apply in Blender, Bake in Grasshopper) and Radius stops working | L: Radius, Applied | live history vs "nothing left to edit" |
| 16 Procedure | a numbered list: place, split, turn, shift, carve; pink = what the current step changed. The modifier uses the shared group `Procedure` directly | L: Width, Depth, Height, Step, Cut Height, Angle, Shift, Passage | 5 steps: done black, current pink, next grey |
| 17 Diagram | the BIG diagram: the same procedure stopped at steps 1 to 5, side by side, captioned with one verb each | L: Width, Depth, Height, Cut Height, Angle, Shift, Passage | none (captions under the frames) |

## Node groups

- Shared lesson groups: `Box` (Width, Depth, Height; base-centred), `Split` (Geometry, Cut Height -> Bottom, Top), `Procedure` (Width, Depth, Height, Step, Cut Height, Angle, Shift, Passage; stores `changed`; the passage cutter is Depth + 1 deep).
- Lesson trees `01 Three Ways` ... `17 Diagram` (16 uses `Procedure` itself). Display trees `01 · UI` ... `17 · UI`.
- Shared display groups appended from the parametric deck: `UI · Paint`, `UI · Text`, `UI · Card`, `UI · Axes` (and the others, unused here). Note: `UI · Outline` returns the input mesh plus the tubes; this deck uses its own edge tubes (`UI.edges` in the kit) so masses are not drawn twice.
- Named attributes the UI reads: `top` (11, 12), `changed` (16, 17).

## Gotchas found while building

- A driver on a menu input reads the item's internal value (2, 3, 4...), not its position. `mirror()` subtracts the first value with a scripted driver (`var - 2`).
- Menu inputs on a new modifier start empty: `lesson_object()` evaluates the tree, then sets each menu to its first item.
- Extrude Mesh: link an explicit (0, 0, 1) vector to Offset; the unlinked default follows the face normal.
- Flat masses need Set Shade Smooth (off) before painting, or extruded faces shade grey.
- Compare node in INT mode has only two inputs in 5.2.

## Ideas not done

- Ghost of the removed or moved part inside the diagram frames (the CKS deck lists colour, arrow, ghost).
- A static slide on choosing a precedent: orthogonal massing, no complex curves, 5 to 10 clear moves (from Class02-CKS).
