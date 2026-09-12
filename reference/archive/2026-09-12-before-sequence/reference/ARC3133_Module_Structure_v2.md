# ARC 3133 — Revised Module Structure

Five modules, alternating environment. Supersedes the four-module structure in `ARC3133_Viz1_Syllabus_Fall2026.md`.

---

## The shape

| M | Environment | Subject | Fabrication | Output |
|---|---|---|---|---|
| **0** | **Nodes** — GN or GH | Parametric modeling: the operation tree, booleans, non-destructive history | Additive, introductory | One small print |
| **1** | **Python** | Computational geometry: point, list, index, loop — how geometry is built | Computer-controlled motion | Drawing |
| **2** | **Nodes** | Advanced node work; instructor-supplied preset groups permitted | Computer-controlled cutting | Sectional assembly |
| **3** | **Nodes** | Panelization, tessellation, modularity | Additive manufacturing | Vault or façade fragment |
| **4** | **Python + AI** | Build a tool | — | The tool itself |

**node → code → node → node → code**

That alternation is the argument, and it is worth stating in the syllabus in one line: *Module 0 shows students a graph before they can read it; Module 1 explains what a node actually is; Modules 2 and 3 return to nodes with that knowledge; Module 4 has them author one.*

You cannot explain a loop to someone who has never wanted one. Module 0 creates the want. Module 1 answers it. Under the old structure Python arrived in Week 3 as an assertion; now it arrives as a reply.

---

## The strongest justification: fabrication now matches computation

This falls out of the new arrangement rather than being imposed on it, and it is the cleanest thing to put in front of a curriculum committee.

| Module | Computational subject | Fabrication process | Why they match |
|---|---|---|---|
| 0 | One ordered sequence of operations | One print | A solid is a single thing. One tree, one object, one machine job. |
| 1 | **Lists, indices, order** | **Pen plotter** | A toolpath *is* an ordered list. The one process where sequence is physically visible is assigned to the module that teaches sequence. |
| 2 | Iteration, filtering, intersection | Laser cutting | Sections *are* flat parts. Iteration produces a series; the laser consumes a series. |
| 3 | Nested loops, grids, modularity | Multi-part 3D printing | Panels *are* a batch. A grid of components is a production run. |
| 4 | Abstraction — inputs and outputs | none | The deliverable is the instrument, not an object. |

Module 1 is the load-bearing case. Python's output is a list of ordered coordinates; a plotter's input is a list of ordered coordinates. There is no translation layer, and the assignment cannot be faked with a node group.

---

## What each module now is

### Module 0 — Parametric modeling
Instructor's choice of Geometry Nodes or Grasshopper. Students build a **boolean operation tree**, not a modeling history. Primitives in, union / difference / intersection, ordered, editable at any point.

The existing 0.1 requirements survive intact — 5+ booleans, 4+ primitives, 2+ translations, 1+ rotation, no imported geometry — but the phrase "operation history intact and demonstrable" becomes "the graph is the submission."

The no-supports print requirement gets *sharper* here, not weaker. Node-based booleans produce non-manifold results more readily than direct modeling does, so the manifold lesson lands harder and earlier.

0.2 Visual Identity Manual is unaffected.

### Module 1 — Computational geometry
Python, in Blender or Rhino. The fourteen scripts in `module1_point/` are this module. Point → list → index → loop → conditional → function → field.

Its job has changed and the syllabus should say so. Module 1 is no longer *the way you will build everything for the rest of the semester*. It is **the module that explains what the nodes in Modules 0, 2, and 3 are doing.** A Sverchok or SNLite pairing (`module1_point/sverchok/`) makes that explicit: same logic, both environments, side by side.

Fabrication: plotter drawing, ordered by the student's own loop.

### Module 2 — Advanced nodes, graphics and section
Back to GN or GH. **Instructor-supplied preset node groups are permitted and expected.** The `Mesh To SDF` group already in the working file is exactly this — a hard piece of machinery handed over so the student can spend their time on the image.

Two deliverables that decouple cleanly:

- **2A — the graphic.** Image-led, against the practitioner references (@mmnksr, @mantissa.xyz, @saul_kim_). Preset groups make an ambitious image reachable in three weeks, which it was not when every section plane had to be hand-looped.
- **2B — the sectional model.** Laser-cut assembly, registration, kerf, tolerance, nesting, labeling. **Unaffected by the environment change** — this is craft and machine work, not node work. The prohibitions that matter here are about measurement and fit, not about which software generated the profiles.

### Module 3 — Panelization, tessellation, modularity
Nodes. Tissue Tessellate, Surface Box / Box Morph, Paneling Tools. Already node-permissive in the current syllabus, so this module changes least.

The existing rule holds and is now consistent with the rest of the course: **the tool may generate the tessellation; the differentiation across it must be authored.** Module 1 is what makes that demand fair — students have written a remap and a falloff by hand, so "author your variation" is a request they can meet.

### Module 4 — AI-assisted tool building
Promoted from "Final Assignment" to a full module. Content is unchanged: study a workflow, extract it as pseudocode, build a tool with named inputs, demonstrate it live with unprepared values.

No fabrication output. State that explicitly in the syllabus or it reads as an omission.

---

## What this breaks in the current syllabus

Seven items, in order of how badly they need fixing.

### 1. Prohibited Shortcuts, row 2A/2B — **direct contradiction**
> *2A / 2B — Automated contour and sectioning plugins; one-click waffle and slotting generators*

Module 2 now supplies preset node groups. This row must be rewritten or removed.

The governing principle still works, but its object has moved. It was *build the logic rather than call it*. It becomes: **you may call the logic once you can say what it does.** Module 1 is where that is demonstrated; Module 2 is where the tool is released. That is the same "earn the tool" argument the syllabus already makes for Module 3 — it now simply applies one module earlier.

Suggested replacement row: *2A / 2B — Preset section and waffle groups are permitted. The section logic must be explicable on demand: a student who cannot describe what the group does receives no credit for Computational Understanding.*

### 2. Learning Outcome 4 — wrong assessment sites
> *Write Python that applies variables, data types, lists, indices, conditionals, loops, functions — **Assessed in 1A, 2A, 3A, Final***

Python is now assessed in Module 1 and Module 4 only. Re-scope to **1A, 1B, Module 4**.

### 3. Learning Outcome 5 — promote it
> *Recognize the same computational logic across scripted and node-based environments, and reimplement a given system in a second one*

Under the old structure this was one of twelve outcomes. Under the new one it is the spine of the entire course, and the Module 1 → Module 2 handoff is where it is assessed. Say so.

### 4. Module 0's own text describes the wrong thing
0.1 currently reads *"a guided modeling tutorial"* and *"operation history intact and demonstrable on request"* — that is non-destructive direct modeling, not a graph. Tutorial 0.2 is already titled *CSG Operations in Graphs*, so the intent existed; the assignment text never caught up. Rewrite 0.1 around the tree.

### 5. The Python gap — name it rather than hide it
Module 1 ends around Week 8. Module 4 begins Week 12. That is four to six weeks with no code, and students will lose fluency.

Two honest responses:

- **Module 4 is AI-assisted by design.** It does not require retained syntax fluency; it requires the ability to read code and catch where it is wrong. That is a much slower skill to lose. The gap is survivable *because* of how Module 4 is built — and that is worth saying out loud rather than leaving as a happy accident.
- **Open each Module 2 and 3 tutorial with sixty seconds of the Python equivalent** of whatever the node group does. Not a lesson. A reminder that the group is not magic.

### 6. Module 4's weight and naming
Currently "Final Assignment · 13%" with a Week 14 proposal. As a module it needs a module's identity: its own reference set, its own brief, and consistent naming across the weights table, the calendar, and the tutorial list. Tutorial 4.1 already exists and is released Week 12 — that timing still works.

### 7. Tutorial 2.1 needs re-scoping
*Contour Curves from SDF Solids* was written as a Python tutorial. It now becomes a node tutorial built on the `Mesh To SDF` group. The concept — signed distance, isosurface, contour extraction — is unchanged; the environment is not.

---

## Unchanged and still correct

- 0.2 Visual Identity Manual, the Booklet, and the sheet standards
- All fabrication requirements: manifold geometry, kerf and tolerance measured not assumed, registration, nesting, production planning, batching
- The Week 1–7 AI-free window — it now covers Modules 0 and 1, which is exactly where it belongs
- Live modification from Week 8, and the rule that a student who cannot operate their own work receives no credit for Computational Understanding
- The practitioner reference set, which was already organized by module
- NAAB mapping: A.5 cites Modules 1 and 3, A.4 cites Modules 1–3 — both still hold
