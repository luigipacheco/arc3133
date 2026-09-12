# Teaching review — 12 September 2026

The sequence has a clear purpose: describe geometry, construct it, repeat it, vary it using measurements, change its representation, then make physical parts. The strongest connection is the pyramid: students build it from faces, subtract it from a cube and reuse it in arrays and attractors.

These are instructor review notes and suggested stopping points. They do not introduce new assignments or change dates or grading. [syllabus/course.yml](../../syllabus/course.yml) remains the curriculum source.

The introduction is well scaled for a first lesson: two nodes to make a cube, four for each transformation and six for the Boolean examples. The geometry lesson has more nodes, but repeats the face construction students just learned. Later lessons introduce several new ideas together, so their complete graphs are best treated as instructor references with staged student exercises.

| Topic | Suggested stopping point | Continue after students can explain the first result |
|---|---|---|
| Introduction | Build a block and cutter; change one parameter and predict the difference. | Compare operator order, Union and Intersect; save three massing variants. |
| Geometry Fundamentals | Construct one face, then reuse that construction for a closed pyramid. Explain 5 vertices, 8 edges and 5 faces. | Replace the previous cutter with the pyramid and expose Width, Depth and Height. |
| Arrays I | Make three points in a Repeat Zone and explain iteration 0, 1 and 2. | Build a 2 × 3 nested grid before increasing counts. |
| Arrays II | Change an index range and predict exactly which elements move. | Develop the radial, staggered-row and sine studies across additional practice as needed. These are different mathematical ideas. |
| Attractors | Read the grayscale field, then use one attractor to change height. Explain distance → remapping → geometry. | Reuse the same mapping with multiple points and a curve. |
| Tessellation and lattices | Explain why a panel array covers the plane at Fill = 1, then distinguish panels from struts. | Vary the upper layer with an attractor and develop a real connection. Overlapping struts alone are not a fabrication joint. |
| Point clouds | Inspect the actual sample count, preserve the source and filter by distance. | Compare two point radii or voxel resolutions. Separate the data from the display spheres and reconstructed boundary. |
| Advanced volumes | Explain negative / zero / positive on the sphere field and identify the extracted zero surface. | Add Boolean operations and noise. Inspect the supplied sampling setup before rebuilding every support node. |
| Discretization | Make one contour, then three contours with a known interval. | Add thickness, lay out parts and compare the finite section set with the continuous source. |
| Fabrication | Make a coupon and test one connection or pair of section parts. | Produce a complete assembly after the material and machine tests. Use the final file as a reference for development, not a completed design brief. |

Arrays II is the most crowded session: staggered rows, trigonometry, range selection and sine variation all compete for attention. Keep the separate files, but allow the second array file to span more than one class. Volumes and discretization also need pauses between understanding the result and rebuilding the mechanism. These suggestions preserve the flexible pacing already stated in the syllabus.

The course also needs a visible architectural question alongside each technical operation. A simple progression would be bay spacing for arrays, shade or opening size for attractors, connected panels for tessellation, and material thickness and light for sections. The supplied abstract geometry is useful for isolating operations; the short assignments should ask students to apply them to an architectural decision.

Two curriculum details need alignment before student release. Some pseudocode describes a different example from its Blender counterpart: the point-cloud block uses neighborhood density, while the file filters by attractor distance; the volume block uses a smooth combination, while the file demonstrates difference and a separate noise field. The pyramid pseudocode also uses ±w and ±d, which makes those half-dimensions, whereas the saved pyramid exposes full Width and Depth. Treat the code as conceptual examples until those differences are resolved.

The fabrication file also has independent modifier settings for the assembled sections, cutting layout and spacer rings. Its notes correctly tell the user to match those settings, but this is fragile for a production workflow. Before treating it as a fabrication template, drive all three views from one shared parameter set so a thickness or count change cannot leave the cutting file inconsistent with the assembly. The existing exports are snapshots of the checked defaults.

Corrections made during this pass:

- Moved the new lesson header Frames above the native nodes, preserving a clear gap after fitting their text. Native node names and original Geometry Fundamentals were preserved.
- Reduced the contour-stack graph's horizontal span from 4,190 to 2,490 node-editor units by removing unused space. Its geometry and connections are unchanged.
- Clarified that the point-cloud lesson's final output is a mesh of display spheres. Added instructions for using Viewer on Mesh to Points to inspect the actual samples in the Spreadsheet. The Viewer workflow is documented in the [Blender 5.2 manual](https://docs.blender.org/manual/sv/5.2/modeling/geometry_nodes/output/viewer.html).

The files evaluate correctly, but computational checks do not establish that beginners can follow the lesson or that physical joints fit. The next useful check is to rehearse the first two lessons from an empty graph, then use the stopping points above to decide how much can be taught comfortably in one meeting.
