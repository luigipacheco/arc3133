# Interactive slides in Blender: the method

How we build a lecture as a Blender file where every slide is live geometry that students can change during class. Written so we (or another agent) can make the next one the same way.

Reference build: `files/blender/Introduction-to-Parametric-Design.blend` (see its handover doc, `Introduction-to-Parametric-Design.md`, next to it).
Second build: `files/blender/Introduction-to-Procedural-Design.blend` (handover `Introduction-to-Procedural-Design.md`), built entirely by script: `_tools/procedural_slidekit.py` + `_tools/procedural_build.py`.
Helper code: `files/blender/_tools/blender_slidekit.py`.

---

## 1. The idea in one paragraph

One `.blend` file, one **scene per slide**. Each scene has a fixed orthographic camera that frames a 16:9 slide: title, text, a Python code card and a TRY line on the left (the "HUD"), live geometry on the right. The geometry is a Geometry Nodes object whose inputs show in the modifier panel, so the teacher changes numbers and the slide answers immediately. The Spreadsheet shows the same data as a table, and a pseudo-Python card shows it as code. Three views of one idea: picture, table, code.

## 2. Rules that keep it teachable

0. **Concept slides, not tutorials.** Explain the computational-design idea in general terms (KISS); tool-specific depth (Blender, Grasshopper) belongs in the per-assignment tutorials.

1. **Lesson and display are separate modifiers.** Every slide object has two Geometry Nodes modifiers:
   - `GeometryNodes` = the lesson. Only the nodes students should learn. Its output is the real data (points, instances), so the Spreadsheet shows the lesson list, not the drawing.
   - `UI` = display only. Reads the lesson output (named attributes, Position, Index) and draws labels, colors, outlines, axes, code readouts. Lives in `NN · UI` node groups.
   The node editor opens on the lesson modifier. Never mix display tricks into the lesson tree.
2. **The lesson stores its answers as named attributes** (`selected`, `remainder`, `column`, `row`, `answer`, `distance`, `opening`...). The UI reads them by name. This is also what makes them appear as Spreadsheet columns, which is part of the lesson.
3. **Controls go in the modifier panel.** Lesson controls in the `GeometryNodes` modifier; display-only controls (number line ranges, Auto Fit, loop stepping, Show Lines) in the `UI` modifier. Name them the way you explain them in class ("Domain 1 Min", "Clamp Min", "Loop i").
4. **Every slide gets pseudo-Python**, live where possible (built from the actual values with Value to String and Join Strings), static otherwise. Short, Python-like, readable in 5 seconds. Exception: for an introduction to the interfaces (the procedural deck) use **instruction cards** instead: numbered steps in plain words with live values, plus one grey line each for where the operation lives in Blender and in Grasshopper. No Python.
5. **One idea per slide.** When two ideas share a slide, split it (we split Remap and Clamp; Clamp defaults to an identity remap 0 to 10 into 0 to 10 so only the clamp is visible).
6. **Defaults show the idea.** The file should open on values that make the point without touching anything.
7. **Node rules (from the geonodes-tutorial-builder skill):** never rename or relabel nodes; explain with comments; frames only to set apart a stage. Blender 5.2 has no Comment node, so a comment is a Frame with a Text datablock (`frame.text`, `shrink = False`). Frame labels can read like code lines (`for i in range(Count):`, `    if i % N == Pick:`).
8. **Writing:** no em dashes. Short sentences. Slide body under ~6 lines.

## 3. Visual system

- Palette from the deck kit `nb.py`: BLACK 000000, CREAM FFFDF7 (world/background), PAPER F4F4EE (cards, neutral items), LIME C6F035 (rule under titles, highlights), PINK FF4D8D (the answer, the selected thing, TRY text), CYAN 00D9E1 (ranges, limits), YELLOW FFE500, GREY 6B6B6B (secondary numbers), MUTE B4B4AC (lines, "before" states).
- Fonts: Arial Bold titles, Arial body, Courier New Bold for code, tags and data labels.
- EEVEE, Standard view transform, emission-only materials (flat, print-like). Black outlines from `UI · Outline` (only sharp edges, so Boolean diagonals are skipped).
- **Projection:** orthographic. Flat diagrams (lists, number lines, graphs) use a top view (rotation 0,0,0). 3D slides use **true isometric**, the one used in descriptive geometry: camera rotation X = 54.7356° (atan √2), Y = 0, Z = 135°. x reads to the lower left, y to the lower right, z up, all at true scale. Lists must read left to right: for slides where items run along x, use the same isometric from the other corner (Z = 45°) so x runs to the lower right.
- Slide frame: 1920 x 1080, ortho scale about 14 to 18. HUD built in a 16 x 9 unit box, scaled by `ortho_scale / 16`.

## 4. Anatomy of a slide (scene)

```
Scene "NN Name"
├── NN Name                    lesson object (selectable)  modifiers: GeometryNodes, UI
├── Attractor - move me        empty, if the slide has one (selectable)
└── Slide UI NN Name           collection; toggle selection here
    ├── Camera NN Name         ortho camera, scene.camera
    │   └── HUD NN Name        empty at z = -1 in camera space, scale = ortho/16
    │       ├── NN Name · tag      "ARC 3133  VIZ 1  ·  ..." (mono, grey)
    │       ├── NN Name · number   "NN / TT"
    │       ├── NN Name · title    Arial Bold 0.62, 1 or 2 lines
    │       ├── NN Name · rule     lime bar under the title
    │       ├── NN Name · body     Arial 0.27, width 5.3
    │       ├── NN Name · code / card / cardb   static code card (optional)
    │       └── NN Name · try      "TRY ..." pink, bold
    └── markers, axis titles, other display objects
```

Selection: keep every object selectable and control it on the `Slide UI` collection (Outliner arrow toggle). Child objects do not inherit "selectable" from a parent object, but they do from a collection.

## 5. Shared UI node groups (append them from the reference file)

| Group | Does |
|---|---|
| `UI · Paint` | Stores a color as `.viz_col` on points/instances, realizes, sets the `Viz` material |
| `UI · Tint` | Colors lesson geometry **without realizing** it (keeps instances in the Spreadsheet). Sets `Viz` on meshes, `Viz Instances` on instances |
| `UI · Labels` | Prints numbers on points, facing the camera. A, B, C, Pair, Triple, Decimals, Prefix, Suffix, Size, Lift, Color |
| `UI · Text` | One string as a filled mesh facing the camera (left align for code) |
| `UI · Card` | Paper card facing the camera, top-left at Position |
| `UI · Outline` | Thin black tubes on sharp edges |
| `UI · Nice Range` | Round axis range (step 1, 2, 5 x 10^n), optional Include Zero |
| `UI · Ruler` | Number line with ticks and labels from a Nice Range |
| `UI · Axes` | x, y, z axes from the origin, ticks every 1, axis letters |
| `UI · Coord Box` | For every point: the box from the origin to the point plus its projections on the axes (the descriptive-geometry construction) |

Materials: `Viz` (reads `.viz_col` as a geometry attribute) and `Viz Instances` (reads it as an instancer attribute). The leading dot hides the attribute from the Spreadsheet.

## 6. Recipes

- **List readout `>>> points`**: Repeat zone over the first N items, Sample Index for Position, Value to String, Join Strings with `, `; close with `]` or `, ...]`.
- **Stepping through a loop**: UI input `Loop i` (-1 = finished). Separate Geometry: keep `index <= i`, draw the rest as faint ghosts, ring the current item, print `# now i = 2` in the code card. Nested loop: one `Loop Step` k, show `c` and `r` sampled at index k.
- **Two lists side by side (fields)**: Repeat zone printing `[i]  points[i]  answer[i]`, then `len(points) == len(answer)`.
- **Number lines / graphs that resize**: Attribute Statistic on the data, then Nice Range, then map values to a fixed drawing length. Offer manual ranges plus an `Auto Fit` toggle in the UI modifier.
- **Camera-fixed live text**: Active Camera + Object Info Rotation/Location, Rotate Vector a camera-local offset, add. Static text belongs in the HUD as font objects instead.
- **Spreadsheet table of one value**: put the single value on a separate component (mesh vertex) so it gets its own table next to the point-cloud graph.

## 7. Workflow (what worked)

1. Agree on the slide list and the one idea per slide.
2. Build the shared materials and UI groups first (or append them from the reference file).
3. Per slide: lesson tree, then UI tree, then `make_slide` (camera, HUD, text), then `two_mods`, then set modifier values to the interface defaults (new inputs on an existing modifier start at 0, not the default).
4. Render a 50 % still per slide and look at it before moving on (`snap`). Check overlaps, text overflow, cut-off geometry.
5. Back up before big changes (`save_as_mainfile(copy=True)`), then save.
6. Renumbering slides: rename scenes, objects, data, node groups, collections, texts and `NN / TT` numbers in descending order to avoid name clashes, then fix any "slide NN" references in frame labels and comments.

## 8. Gotchas

- Blender 5.2: modifier inputs are `getattr(mod.properties.inputs, socket.identifier).value`.
- Menu sockets on a group interface only get enum items after the tree evaluates; a Menu Switch whose Menu socket is fed by a second Menu Switch breaks the enum. Use one Menu Switch per group input.
- Group input min/max only limit typed values. Linked values pass through (we teach this on the Clamp slide).
- For Each zone: the extra generation outputs (Generated panel) need a Store Named Attribute after the zone to become a named column.
- `evaluated_geometry()` data objects die after the next depsgraph update; read what you need immediately.
- Text objects parented to a camera do not inherit selectability; use a collection.
- The SK helpers live in `bpy.app.driver_namespace` while Blender is open; after a restart, run `blender_slidekit.py` again.
