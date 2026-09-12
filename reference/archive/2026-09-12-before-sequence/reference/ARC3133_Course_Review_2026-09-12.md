# ARC 3133 — course and lesson review

September 12, 2026. Observations for the instructor's next strategy discussion.

The Geometry 101 materials now belong to this course repository. The working file is [here](../files/blender/geometry101/GEOMETRY101-class-ready.blend); [instructor notes and preparation history](geometry101/README.md) are separate. No syllabus, assignment, calendar, grading, or teaching-strategy changes were made as part of this review.

## What the course is trying to teach

The syllabus's opening and module descriptions put **architectural visualization first**, with computational methods serving representation, composition, material, light, and fabrication. They describe a progression from node graphs to reading and modifying code: students must change a parameter, predict the result, and explain what an operation does. The point/line/plane framework connects geometry to lists and fields, sections and sequence, and modular surfaces. [Full syllabus: description, outcomes, and modules](../syllabus/ARC3133_Syllabus_Fall2026.md).

The current Blender exercise supports that intention. It makes geometry inspectable, gives parameters a visible consequence, and keeps the interface names that students need to find the nodes themselves. Explanation Frames satisfy the vocabulary document's request to name both the interface operation and its computational meaning without replacing the native node title. [Vocabulary spine](ARC3133_Vocabulary_Spine.md).

The strongest continuity is **one understandable component carried forward**, rather than a fresh unrelated object for each topic. The pyramid and its Boolean cut provide such a component. That does not yet determine when its shape should vary across an array.

## The documents contain competing course models

This is an internal consistency problem, including within the full syllabus itself. The README calls `syllabus/` the source of truth, but that does not resolve contradictions between its sections.

| Where | Model present in the text |
|---|---|
| Full syllabus opening and detailed assignments; student syllabus overview | Modules **0–4**: foundations, POINT, LINE, PLANE, TOOL. Graphs first; a required tool project later. |
| Full syllabus evaluation table, tutorial calendar, assignment summary, and 15-week schedule; repository landing page | Modules **1–5**: massing, lists/mesh/arrays, fields/site, panels, volume/section. Python translation is optional extra credit. |
| Published-source class and assignment pages | A separate scheme: 0.1 Procedure, 0.2 Visual Identity Manual, combined Arrays + Attractors, earlier section deadlines, and a required generative final. |
| Development brief and structure-v2 reference | Python-first or alternating graph/code teaching, whereas the vocabulary spine and syllabus opening describe graph-first teaching. |

Sources: [full syllabus](../syllabus/ARC3133_Syllabus_Fall2026.md), [student syllabus](../syllabus/ARC3133_Syllabus_Fall2026_STUDENT.md), [landing page](../index.md), [assignment overview](../modules/assignments/_posts/1999-12-31-overview.md), [development brief](ARC3133_Course_Materials_Brief.md), [structure v2](ARC3133_Module_Structure_v2.md).

### Specific discrepancies to resolve later

| Issue | Observed difference | Why it matters |
|---|---|---|
| Grading | The full syllabus's evaluation table lists ten module assignments at 7%, a 7% midterm, and no required tool project. Its detailed body specifies eight assignments at 7%, TOOL at 13%, and a midterm at 8%; the student evaluation table follows that latter scheme. Both totals reach 100%. | The arithmetic is not the problem; the assessed work and its weights differ. |
| Visual Identity Manual | Syllabus body/student version: 8+ pages, due Oct 13, 7%. Site assignment page: due Sep 15, 5%. The full syllabus's final-submission section also refers to a “Week 4 version.” | Students can receive different deliverables and deadlines from apparently current sources. |
| September 15 and 22 | Full 15-week calendar: points/lists, then mesh construction. Class 04 site page: arrays. Class 05 site page: a procedure exchange plus attractors. Current Class 05 generator source: attractors plus site analysis. | The intended place of this geometry lesson cannot be inferred from a single class number. |
| Arrays versus varying the component | Detailed Assignment 1.1 requires the **same tile** in every copy; field-level rotation, spacing, culling, and index-driven properties may vary. The legacy class/assignment pages combine arrays with attractors. Component differentiation is explicit in the later panel module. | Changing the pyramid's internal shape across copies is a different learning step from repeating one tile. |
| Site analysis versus plotting | Detailed 1.2 is now a site-analysis field assignment; the full course-structure table says plotting is unplaced. The student overview/materials and its Week 5/7 schedule still promise toolpaths and plotter production. The full 15-week calendar instead gives plotting its own later assignment. | Output, preparation, materials, and machine time remain unresolved. |
| Required code versus optional code | The full body specifies TOOL at 13%, calls it the only code module, but also permits a node-group/Grasshopper tool. Later tables make Python optional extra credit. The legacy final requires a generative iterative tool at 15%. | These are different outcomes and assessment requirements, not interchangeable descriptions of one final. |
| Live modification | The full opening says it is assessed from Week 1; the 15-week schedule says live modification and naming begin at Week 8. | A central assessment practice has two starting points. |
| Print production timing | The detailed print assignment places its production plan in Week 13; the full calendar puts the plan in Week 14, after the queue closes at the end of Week 13. The assignment also calls the presentation a Week 15 final review while the schedule uses Dec 10–16. | The sequence cannot be used as a reliable production calendar as written. |
| Track parity | Students are told to choose Blender or Rhino and that tutorials come in both. Site import instructions specifically prescribe Blender, with its importer still marked for confirmation. | The equivalent Rhino route is not established by those instructions. |
| Prerequisite tool use | The full body permits supplied section/SDF/contour groups with an explanation requirement. The legacy site assignment overview prohibits automated contour/section tools. | A student could follow one source and violate the other. |

Primary locators: full syllabus **Course Evaluation Method** (line 694), **Tutorial Calendar** (780), **Assignments** (805), **15-Week Schedule** (826), detailed **1.1** (323), **1.2** (362), **TOOL** (559). Student evaluation begins at line 196; its schedule at 249. See also [Class 04 page](../modules/classes/_posts/2000-01-04-class-04.md), [Class 05 page](../modules/classes/_posts/2000-01-05-class-05.md), [Class 05 generator](../slides/src/class05.py), and [VIM page](../modules/assignments/_posts/2000-01-02-0-2-visual-identity-manual.md).

The remaining room, lab importer, material-allocation, print-time, and final-slot placeholders are still open items. This review records them rather than deciding them.

## What the Blender lesson currently establishes

| Stage | Verified output | Teaching purpose |
|---|---|---|
| Point | One point-cloud point | Parameter, XYZ vector, position. |
| Line | One curve, two control points | Connect locations into a straight segment. |
| Edge | Two mesh vertices, one edge | The same visible line can be represented as mesh data. |
| Face | Three vertices, three edges, one triangle | Boundary, surface, and the need for non-collinear corners. |
| Solid | Five vertices, eight edges, five faces | Four triangular sides plus a base enclose the pyramid's volume. |
| Boolean | Sixteen vertices, twenty-eight edges, twelve faces | Subtract the constructed pyramid from a cube; preserve editable inputs. |

Width, Depth, and Height are exposed in the Solid and Boolean exercises. Both use the same pyramid definition; each use has independent input values. The geometry was checked for closed, consistently oriented surfaces at the tested solid/Boolean settings. [Verification record](geometry101/preparation-archive/pyramid-sequence-verification.json).

**Line → Edge is a change of representation**, not an extra spatial dimension. The Spreadsheet is essential here because the two outputs look alike. Likewise, a solid is not simply “more faces”: closing the base is what makes this mesh enclose a volume.

This is a foundations demonstration, not a completed massing submission. Detailed Assignment 0.1 asks for five or more Boolean operations, four primitive types, transformations, and architectural/graphic documentation. The single cut teaches the mechanism that students will need to extend. [Massing assignment](../syllabus/ARC3133_Syllabus_Fall2026.md#assignment-01--parametric-massing-sequence).

## Boundaries of the present example

- **Lists and indices still need explicit treatment.** The file shows points, connections, and generated topology, but it does not yet teach a full vertex/edge/face index-list workflow, ordering changes, culling, or nested repetition. Those are called for in the mesh and array material. The existing `MAKEFACE` helper also contains `Sample Index` and position restoration, which is a substantial conceptual jump if opened before those ideas are introduced. [Mesh tutorial](../modules/tutorials/_posts/2026-09-15-t2-2-building-a-mesh-from-lists.md).
- **The single tile and the varying tile are separate steps.** A class using the detailed 1.1 brief would first repeat one student-designed, precedent-based tile. A pyramid-height attractor that changes each cut belongs to a later differentiation exercise or to a deliberate revision of that brief. Reusing the instructor's demo is not the same as satisfying its precedent/design requirement.
- **An instance does not acquire independent internal geometry merely by receiving a different scalar.** Identical instances share their source geometry. Different Boolean openings need generated variants or per-element geometry generation. This affects the eventual array/attractor implementation; it is not built in this file yet.
- **Scale and anchor are not yet fabrication settings.** The saved Boolean scene uses meters with scale length 1. The block is 1.5 × 1.6 × 0.45 meters; the introductory print brief limits the bounding box to 60 mm. The object is at the origin, but its local mesh is offset, with X bounds −0.2 to 1.3 and Y bounds −0.2 to 1.4. A future array/print workflow needs an explicit anchor, spacing, and unit conversion. No scaling change was made during relocation.
- **A valid solid is not a verified unsupported print.** Closed geometry was tested. Slicing, orientation, overhang behavior, and compliance with the no-support first-print brief were not established by those mesh tests.
- **The reusable parameter range is a design choice.** The tested pyramid heights include 0.9, 1.2, and 1.6. The fixed cube occupies Z = 0.175 to 0.625; reducing the apex below its top changes whether the opening goes through. The much wider exposed input limits are not a promise of the same visual effect everywhere.
- **The working file still contains auxiliary session data.** GeoSlicer test objects remain in the Boolean scene. No linked libraries or external images were found; unused Sverchok font data also remain. The lesson graphs themselves use native Blender nodes. Relocation preserved that data rather than silently deleting it; distribution cleanup is a separate item to settle.

## Decisions to bring to the strategy discussion

1. Which module/assignment structure and calendar should govern the course, and which tables/pages are superseded.
2. Whether this six-step lesson precedes the first Boolean exercise or serves as the geometry-construction bridge immediately before arrays.
3. Where constant-tile repetition ends and attractor-driven changes to the tile begin, with explicit links to the chosen assignment requirements.
4. The status of plotting, the equivalent site-data workflow for both software tracks, and the required versus optional role of code.
5. What counts as a student-ready starter: geometry only, parameter presets, unit/anchor conventions, and the amount of helper-group logic students must explain.

Reviewed evidence: the full and student syllabi's curricular, assessment, and calendar sections; repository README and landing page; reference brief, structure v2, and vocabulary spine; class 04/05 pages and generator source; relevant assignment/tutorial pages; and the live Geometry 101 file. The review compares the local materials; it does not treat an unverified historical page or generator as the final teaching decision.
