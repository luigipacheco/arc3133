# Introduction-to-Parametric-Design.blend: handover

Interactive lecture for ARC 3133 Viz 1, Unit 5 (attractors), taught as a Blender file. One scene per slide. Built with the method in `files/blender/BLENDER-INTERACTIVE-SLIDES.md`.

- File: `files/blender/Introduction-to-Parametric-Design.blend` (Blender 5.2.4). Title: "Introduction to Parametric Design" (was "From a list to a facade", `Lists-to-Facade-Slides.blend` in `04-attractors`). It sits above the unit folders because it introduces the ideas used from Arrays through Attractors and the facade
- Backups: `files/blender/_check/Lists-to-Facade-Slides_v1.blend` (before the lesson/UI split), `_v2.blend` (before adding the point slide), `_v3.blend` (before adding edge and face), `_v4.blend` (before adding the panel slide), `_v5.blend` (before moving Pattern after List of Lists), `_v6.blend` (before the List, List of Lists, Array, Pattern, Volume order), `_v7.blend` (before splitting the attractors into three slides and adding Falloff), `_v8_old-name.blend` (last copy under the old name and folder)
- Test renders: `files/blender/_check/SLIDE_00.png` to `SLIDE_19.png` (not for students; safe to delete)
- Helper code: `files/blender/_tools/blender_slidekit.py`
- Last updated: 2 November 2026

## Scope

These slides explain the concepts only, tool-agnostic and kept simple. Each assignment has its own tutorial that goes deeper in Blender and Grasshopper; do not turn the slides into tutorials.

## Teaching arc

A point is three numbers. An edge is a pair of point indices, a face a loop of them. With those we build a parametric panel. A list is points in order, built by a loop. An array places an object on every item. A conditional picks per item. A loop inside a loop gives a 2D array, one more gives 3D. A field is a second list of the same length (one value per point). An attractor makes a distance field. Remap moves numbers from one domain to another; clamp keeps them in range. All of it drives a facade.

## Slides

Controls: **L** = `GeometryNodes` modifier (lesson), **U** = `UI` modifier (display only).

| Scene | Idea | Controls | Python card |
|---|---|---|---|
| 00 Title | Title and 19 chips | none | none |
| 01 Point | p = (x, y, z); isometric axes, coordinate box to the point | L: X, Y, Z | live: `p[0]`, `p[1]`, `p[2]` |
| 02 Edge | two points, the edge is an index pair (0, 1); coordinate box for each point | L: Point 0, Point 1 | live: `points = [...]`, `edge = (points[0], points[1])`, `dist(edge[0], edge[1])` (note: Blender stores it as indices (0, 1)) |
| 03 Face | three points and the face between them, built like the edge (Mesh Circle 3 N-Gon for the topology, Set Position + Index Switch puts corner i at points[i]); corner order gives the normal: front green, back red (`Face Sides` material, shader Backfacing), black normal arrow at the centre, Flip Faces toggle | L: Point 0, Point 1, Point 2, Flip | live: `points = [...]`, `face = (points[0], points[1], points[2])`, indices `edges`, `faces = [(0, 1, 2)]` or `[(0, 2, 1)]  # flipped` |
| 04 Panel | a parametric object built from scratch: Quadrilateral outline (4 points in a loop), the same loop scaled by Opening (clamped 0.05 to 0.95) as the hole, Fill Curve between the loops, Extrude Mesh + flipped copy + Merge by Distance for thickness. The lesson tree is the reusable group `Panel` | L: Width, Height, Opening, Thickness, Build menu (Outline, Hole, Face, Thickness). U: copies of the four values, driven from L | live: `def panel(width, height, opening, thickness): ...` and `>>> panel(2.00, 2.00, 0.55, 0.15)` |
| 05 List | list in brackets across the middle, index above, (x, y, z) below; the loop that builds it in a compact code card top right | L: Count, Step, Read Index. U: Loop i (-1 = finished) | live: `points = []`, `for i in range(n):  # now i = 2`, `>>> points`, `len`, `points[i]`, `points[i][0]` |
| 06 List of Lists | 2D array, nested loop, flat index `i = c x Rows + r` | L: Columns, Rows, Column Step, Row Step, Pick Column, Pick Row. U: Loop Step (-1 = finished) | live: nested `for c` / `for r` with current c and r, `len(grid)`, `grid[c][r]`, `c * Rows + r` |
| 07 Array | the two meanings of "array"; a box on every list item | L: Count, Step, Box Size | static |
| 08 Pattern | a 2D pattern: every grid item asks the same yes/no question with its address, `(rule) % N == Pick`, rule = c, r, c + r or c - r (stripes, checkerboard, diagonals); the answer is a Boolean value | L: Columns, Rows, Spacing, Rule menu, Every N, Pick | live: nested `for c` / `for r` with the counts and `if (c + r) % N == pick: tall else: short` |
| 09 Volume | "All together": one more loop makes a 3D array `volume[f][c][r]`, then the array (a box on every item) and the pattern (`(rule) % N == Pick`, rule = c + r + f, f, c + r or c) combine; Show Floor/Column/Row highlights one item (yellow) with its address and flat index i | L: Columns, Rows, Floors, Spacing, Floor Height, Show Floor, Show Column, Show Row, Rule, Every N, Pick | live: three nested loops + the if, `>>> volume[f][c][r]`, flat index |
| 10 Fields | a field is a second list, same length, item i belongs to point i | L: Field menu (Index, X, Y, Random, Wave), Columns, Rows, Seed, Wave Size | live: `[i]  points[i]  answer[i]` rows and `len(points) == len(answer)` |
| 11 Attractor | one point: distance from every item to the attractor is a distance field | L: Attractor (object), Columns, Rows, Spacing. U: Reach, Show Lines | static `dist(p, a)` |
| 12 Attractors | several points: measure to A, B and C, compare, keep the smallest, `min(dA, dB, dC)`; each item listens to its nearest | L: Attractor A, B, C, Columns, Rows, Spacing. U: Attractor A, B, C (markers), Reach, Show Lines, Inspect | live: `dA`, `dB`, `dC`, `distance = min(...)` and `>>> min(3.4, 2.5, 5.1)` for the inspected item |
| 13 Curve Attractor | a curve: find the closest point on the curve, then measure to it (Curve to Mesh + Geometry Proximity on edges) | L: Curve, Columns, Rows, Spacing. U: Curve, Reach, Show Lines, Inspect | live: `closest = closest_point(curve, p)`, `distance = dist(p, closest)`, values for the inspected item |
| 14 Remap | two number lines (domains); each sample projected from Domain 1 to Domain 2 | L: Samples, Domain 1 Min/Max, Domain 2 Min/Max. U: Auto Fit, Line 1 Min/Max, Line 2 Min/Max | static `remap()` |
| 15 Falloff | the shape of the drop from 1 (near) to 0 (at the reach): t = distance / reach (clamped); Linear, Smooth, Sharp, Soft, Step, or Drawn (a Float Curve shaped by hand; the tutorial also uses a Color Ramp). Fixed distance axis 0 to Range in metres, so moving Reach visibly moves where the curve hits 0; row of openings scaled by the influence | L: Falloff menu, Reach, Samples, Range | live: `def falloff(d, reach): t = clamp(d / reach, 0, 1); return ...` with the chosen formula or `curve(t)` |
| 16 Clamp | value in, value out; clamp independent of remap (default remap 0..10 into 0..10, clamp 2 to 8) | L: Value, From/To Min/Max, Clamp on/off, Clamp Min/Max, Graph Min/Max. U: Auto Fit, X Min/Max, Y Min/Max | static `clamp()` with three cases; live readout `in > remap > clamp > out` |
| 17 Facade | grid of panels, distance, remap, clamp, For Each panel with its own opening | L: Attractor, Facade Width/Height, Columns, Rows, Gap, Reach, Near, Far. U: Show Numbers | static loop |
| 18 Facade Points | the same facade driven by three point attractors: each panel keeps the smallest distance (as on slide 12) | L: Attractor (FA), Attractor B (FB), Attractor C (FC), Facade Width/Height, Columns, Rows, Gap, Reach (2.6), Near, Far. U: Show Numbers | static loop with `min(dA, dB, dC)` |
| 19 Facade Curve | the same facade driven by a curve: distance to the closest point on the curve (as on slide 13); edit the curve object `Attractor curve facade - edit me` | L: Curve, Facade Width/Height, Columns, Rows, Gap, Reach (2.2), Near, Far. U: Show Numbers, Curve | static loop with `closest_point(curve, p)` |

Projection: 01, 02, 03, 04, 09, 10 are true isometric with x to the lower left (54.7356°, 0, 135°); slide 04 stands the panel up in the UI (lesson output stays in XY, like the facade expects). 06 and 07 are true isometric from the other corner (54.7356°, 0, 45°) so lists read left to right. 05, 08, 11 to 16 are top views. 17, 18, 19 are a near-front axonometric of the facade.

## Data contract (named attributes the UI reads)

- 01 to 03: plain mesh data (Position, edges, faces); the UI reads them directly
- 04: plain mesh (the panel); Build shows curves for Outline and Hole
- 05: `selected` (bool)
- 06: `column`, `row` (int), `in_column`, `selected` (bool)
- 08: `column`, `row`, `rule`, `remainder` (int), `is_pick` (bool), on instances
- 09: `floor`, `column`, `row`, `rule`, `remainder` (int), `in_floor`, `in_column`, `selected`, `is_pick` (bool); output is instances (boxes)
- 10: `answer` (float), on instances
- 11, 12, 13: `distance` (float), `nearest` (vector, the closest attractor point); 12 also `dA`, `dB`, `dC` (float), `which` (int)
- 14: `value`, `remapped` (float)
- 15: `distance`, `influence`, `linear`, `reach` (float), `falloff` (int)
- 16: `remapped`, `value_out` (float); your one Value is a mesh vertex, the graph is a point cloud
- 17, 18, 19: `opening` (float), on instances (one per panel)

## Node groups

- Lesson: `01 Point` ... `19 Facade Curve`, except slide 04, whose lesson tree is the reusable group `Panel` (Width, Height, Opening, Thickness, Build). `17 Facade`, `18 Facade Points` and `19 Facade Curve` use this same `Panel` group inside its For Each zone (Build = Thickness), so the object built on slide 04 is the one on the facade. Each has numbered frames (`01  ...`) and comment frames with Text datablocks (`NN note - ...`).
- Display: `01 · UI` ... `19 · UI`.
- Shared display: `UI · Paint`, `UI · Tint`, `UI · Labels`, `UI · Text`, `UI · Card`, `UI · Outline`, `UI · Nice Range`, `UI · Ruler`, `UI · Axes` (x, y, z axes with ticks), `UI · Coord Box` (isometric coordinate box and axis projections for every point).
- `Face Sides` material (slide 03): green front, red back, from the shader's Backfacing output.
- `ARCH / Prototype measurement grid / Controls.001` and scene `Scene`: leftovers from the startup file, unused.

## Collections and selection

Each scene has a `Slide UI NN Name` collection (camera, HUD, text, cards, axis titles, attractor marker balls). Every object is selectable by default; the switch lives on the collection: click the arrow on the `Slide UI` row in the Outliner to lock or unlock everything in it. When locked the arrow is faint, which makes it easy to miss. The lesson object and the attractor empty (the thin sphere outline, click it and press G) sit outside the collection.

## Known issues / ideas not done

- Static code cards (07, 11, 14, 17, 18, 19) do not follow the controls.
- The workspace layout (Spreadsheet, node editor, modifier panel) is shared by all scenes; the Spreadsheet keeps the last chosen component (Point Cloud or Instances), switch it per slide.
- Some old comment Text datablocks from earlier versions are unused (e.g. `10 note - why`, `09 note - examples`); harmless.

## How to continue (for an agent)

1. Open the file in Blender 5.2 with the Blender MCP, run `files/blender/_tools/blender_slidekit.py` to load the helpers (`SK = bpy.app.driver_namespace['SK']`).
2. Read the slide's lesson tree and UI tree before editing. Keep lesson and UI separate. Never rename nodes.
3. After editing, render with `SK['snap'](scene, "SLIDE_NN")`, stage the PNG and look at it.
4. Save a backup copy before large changes, then `bpy.ops.wm.save_mainfile()`.
5. Ask Luis before deleting anything.
