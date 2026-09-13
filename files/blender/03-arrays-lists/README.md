# 03 · Arrays and Lists

One teaching session and one tutorial video cover both files, in this order. Download them individually. Weeks 4–5 remain a flexible guide, with extra time for practice when needed. The video has not yet been posted.

- [Arrays-Lists-Session-1.blend](Arrays-Lists-Session-1.blend) — Linear loop, Nested grid.
- [Arrays-Lists-Session-2.blend](Arrays-Lists-Session-2.blend) — 3D array, Hexagonal array, Radial array, If and range, Sine curve.

Use the Scene selector in numbered order. Select the lesson object to see its Geometry Nodes. Change the exposed parameters in the modifier; press Home over the node editor to fit the graph.

| Scene | Exercise |
|---|---|
| 01 - Linear loop | COUNT, INDEX, REPEAT |
| 02 - Nested grid | NESTED GRID |
| 03 - 3D array | ROW → GRID → LAYERS |
| 04 - Hexagonal array | HEXAGONAL ARRAY |
| 05 - Radial array | REPEAT AROUND A CIRCLE |
| 06 - If and range | IF THE INDEX IS IN THIS RANGE, MOVE IT |
| 07 - Sine curve | MATH SHAPES A VOLUME |

The last exercise is the updated 3D curve array. Sine shapes the first row along X; repetition in Z and Y builds the spatial arrangement, and a second sine relationship varies the height across Y. Its purpose is to show how math can shape a volume. The output stays as cube instances, preparing for later volume fields.

After the nested grid, build a 3D cube array before moving to hexagonal arrays. Count = 4 gives 4 × 4 × 4 = 64 cubes. Change Count, Spacing and Cube Size independently. The cubes are discrete instances; later volume lessons use locations across XYZ space to sample density or distance.

Native node names are retained. Short explanations and things to try are in Frames. Use these files only as references when you are stuck. Build your own file and follow the steps one by one.

[Course file index](../README.md) · [Current syllabus](../../../syllabus/ARC3133_Syllabus_Fall2026_STUDENT.md)
