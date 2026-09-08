# FLORIDA ATLANTIC UNIVERSITY
## ARC 3133-001 — Architectural Visualization Methods 1
### Computational Visualization + Digital Fabrication

**Term:** Fall 2026 — Full Term
**Meeting:** Tuesday, 5:00 PM – 7:50 PM
**Location:** FAU/BC Higher Ed Complex FTL — `[room TBD]`
**Credits:** 3

---

## Instructor Information

**Instructor:** Luis Pacheco Alcala
**Email:** lpachecoalcala@fau.edu
**Office:** 712
**Office Hours:** By appointment

**TA:** None assigned

---

## Prerequisites

All of the following, with a minimum grade of C:

- ARC 1301
- ARC 1302
- ARC 2303
- ARC 2304

---

## Instructional Method

**In-Person.** Traditional in-person delivery. Attendance requirements are set by the instructor and described below.

This course requires physical fabrication and scheduled use of the School of Architecture FabLab. It cannot be completed remotely.

---

## Course Description

Architectural Visualization Methods 1 explores computational design thinking — algorithmic methods and parametric principles — for architectural representation. Analog and digital methods are examined with an emphasis on logical underpinnings, procedural processes, and the visual communication of design intentions.

The course runs in **five modules**. The first four are built in node graphs; the last is written in code.

| Module | Environment | What is taught |
|---|---|---|
| **0** | Node graph | Parametric modeling: what a parameter is, how nodes connect, transformations, booleans |
| **1** | Node graph | Computational geometry: the point, the list, loops, conditionals, arrays, fields |
| **2** | Node graph | Section and sequence: bisecting geometry and rebuilding it as slices |
| **3** | Node graph | Modularity and tessellation: vault systems, panel fields |
| **4** | Python + AI | Tool building |

**Vocabulary first, syntax last.** For ten weeks you work in a node graph, and every operation you use is named twice — once by its interface label, once by its computational term. A node applied to every element of a collection is a **loop**. A node group is a **function**. `Map Range` is a **remap**. You will be saying these words from Week 1 without writing a line of code.

Module 4 then shows you what each of them looks like typed out. Nothing new is being taught there — the concepts are already yours — so the work is reading code, verifying it, and modifying it, which is what building a tool with an assistant actually requires.

### Point, Line, Plane

Modules 1, 2, and 3 each take one of the three fundamental spatial elements:

| Module | Element | Computational focus |
|---|---|---|
| 1 | Point | Lists, arrays, and fields |
| 2 | Line | Section and sequence |
| 3 | Plane | Modularity and tessellation |

Each of these modules has two assignments: a **Digital Visualization Assignment** producing a sheet, and a **Physical Fabrication Assignment** producing an object.

Visualization is the primary emphasis. Composition, color, hierarchy, line weight, rendering, diagramming, and post-processing are what the sheets are assessed on. Computational methods are tools for generating new types of images, not ends in themselves.

### Environments

| Environment | Type | Used in |
|---|---|---|
| Blender Geometry Nodes | Visual programming | Modules 0–3 |
| Grasshopper | Visual programming | Modules 0–3 |
| Blender Python | Scripting | Module 4 |
| Grasshopper Python | Scripting | Module 4 |

Choose Blender or Rhino in Week 1 and stay there. Every tutorial ships in both.

**Computational understanding is assessed from Week 1**, in the node modules, through two questions asked at every pin-up: change something in your definition, live; and name an operation in it and say what it does. Neither requires code. Both require knowing what the graph is doing.

Digital fabrication complements the visualization curriculum through three modes of computer-controlled making: **drawing**, **cutting**, and **additive manufacturing**.

---

## Course Structure

| Module | Concept | Environment | Fabrication | Physical output |
|---|---|---|---|---|
| 0 | Foundations | Node graph | Additive (introductory) | Small print |
| 1 | POINT | Node graph | `[TBD — the pen plotter is no longer attached to 1.2; Module 1's fabrication mode is unplaced]` | — |
| 2 | LINE | Node graph | Computer-controlled cutting | Sectional assembly |
| 3 | PLANE | Node graph | Additive manufacturing | Vault or façade fragment |
| 4 | TOOL | Python + AI | — | The tool |

Each module's fabrication process matches its computational subject. Sections are flat parts, so the laser belongs to the module that teaches iteration. Panels are a batch, so multi-part printing belongs to the module that teaches grids. `[TBD — the pen plotter is no longer attached to 1.2; Module 1's fabrication mode is unplaced]` — a toolpath is an ordered list, which is why the plotter sat here originally; if it returns, this is the argument for it.

Module 0's print sits before this progression rather than inside it — one solid, one orientation, so that Module 3 can address additive fabrication at the scale of an assembly.

---

## Software and Materials

### Required Software

| Purpose | Environment | Notes |
|---|---|---|
| Application environment | Blender — Geometry Nodes (Modules 0–3), Python (Module 4) | Free and cross-platform. Recommended for students without a Rhino license. |
| Application environment | Rhino + Grasshopper (Modules 0–3), Grasshopper Python (Module 4) | Student license |
| Language read and modified | Python 3.x | Module 4 only. Written inside Blender or Rhino; no separate install required |
| Layout and post-processing | Adobe Illustrator, Photoshop, InDesign | Student license. Open-source equivalents accepted: Inkscape, GIMP, Scribus |
| Slicing | PrusaSlicer, Cura, or FabLab-specified slicer | Per FabLab standard |
| Cutting preparation | As specified by the FabLab | Introduced in Week 10 |
| Site capture | Google Photorealistic 3D Tiles, imported to Blender | Assignment 1.2 only. Free tier; an API key is provided in class. Blosm or the Google 3D Tiles importer add-on `[CONFIRM which add-on is installed on the lab machines]` |

**Template-based design tools are not permitted.** Canva, Adobe Express, Figma templates, PowerPoint, Google Slides, Wix, and similar applications may not be used to produce any sheet, the Visual Identity Manual, or the Booklet. A template supplies the grid, the type hierarchy, the palette, and the spacing — the exact set of decisions the Visual Identity Manual asks you to make yourself.

Work in a vector or raster editor: Illustrator, Photoshop, InDesign, Inkscape, GIMP, Scribus, or Affinity.

### Materials

Consumable materials are **supplied by the School**, subject to the limits below.

| Module | Supplied | Per-student allocation |
|---|---|---|
| 0 — First print | Filament | One print, 200 g |
| 1 — `[TBD — the pen plotter is no longer attached to 1.2; Module 1's fabrication mode is unplaced]` | — | — |
| 2 — Laser cutting | Chipboard, basswood, or acrylic | 1 sheet |
| 3 — 3D printing | Filament | `[CONFIRM — FabLab supplied or student purchase]` |
| 4 — Tool | — | No physical output |

Allocations are fixed. Test cuts and failed prints count against them, so plan them deliberately. Students who exceed the allocation are responsible for replacement material.

Students supply their own storage media and are responsible for their own file backups.
### Fabrication Scope Limits

To ensure the whole cohort can complete fabrication within FabLab capacity, the following limits apply and are part of each assignment's requirements:

- **Assignment 0.2 (first print):** maximum bounding box 60 mm; draft layer height; **no supports permitted** — orientation is the only lever, and the choice must be documented
- **Assignment 2.2:** maximum assembled bounding box 300 mm; maximum sheet count 1
- **Assignment 3.2:** maximum assembled volume 300 mm; maximum print time per student `[TBD]`

Work exceeding these limits will not be scheduled on the machines.

---

## FABLAB Usage Protocols

For all new FAU School of Architecture students, the **FabLab Safety Orientation must be completed to gain access to any part of the FabLab.** Enroll through:

`https://canvas.fau.edu/enroll/JEW9J6` — `[CONFIRM link is current for this term]`

**Completion is due by the end of Week 2 (Sep 1).** Students who have not completed the orientation cannot begin Assignment 1.2 and remain responsible for the assignment deadline.

---

## Required Texts / Materials

**No required textbook.** Course material is delivered through in-class demonstration, distributed code, and documentation. `[DECIDE — Woodbury was previously the required text; it is Grasshopper-centered and now sits below as recommended. Confirm with the bookstore if a required text must be listed.]`

Students should bookmark the Blender Geometry Nodes documentation or the Grasshopper primer for their chosen environment. The Blender Python API reference and the official Python documentation become relevant in Module 4.

## Recommended Readings and Materials

- **Point and Line to Plane** — Wassily Kandinsky (Dover) — foundational to the course's conceptual structure
- **Elements of Parametric Design** — Robert Woodbury · Routledge, 2010 · ISBN 978-0415779876
- **AAD Algorithms-Aided Design: Parametric Strategies using Grasshopper** — Arturo Tedeschi · Le Penseur · ISBN 978-8895315300
- **Advanced 3D Printing with Grasshopper®: Clay and FDM** — Diego García Cuevas and Gianluca Pugliese · Independently published, 2020 · ISBN 9798635379011 — *primary reference for Assignment 3.2; also relevant to 1.2*
- **Drawing Architecture** — Neil Spiller (Ed.) · John Wiley & Sons, 2013 · ISBN 978-1118418796
- **Drawing: The Motive Force of Architecture** — Peter Cook · John Wiley & Sons, 2014 · ISBN 978-1118700648
- **Drawing Futures: Speculations in Contemporary Drawing for Art and Architecture** — Migayrou, Sheil, Allen, Pearson (Eds.) · Riverside Architectural Press, 2016 · ISBN 978-1988366043
- **Bartlett Designs: Speculating with Architecture** — Iain Borden (Ed.) · John Wiley & Sons, 2009 · ISBN 978-0470772805
- **Speculative Coolness: Architecture, Media, the Real, and the Virtual** — Bryan Cantley · Routledge, 2023 · ISBN 978-1032318868

---

## Course Learning Outcomes

By the end of the course, students will be able to:

| # | Outcome | Assessed In |
|---|---|---|
| 1 | Produce architectural graphics of professional visual quality using computational methods | 1.1, 2.1, 3.1, Booklet |
| 2 | Build and modify a parametric graph — connect nodes, expose inputs, change an upstream parameter and predict the downstream result | 0.1, 2.1, 3.1 |
| 3 | Construct and modify solid geometry through Boolean operations and transformations, non-destructively | 0.1, 3.2 |
| 4 | **Read, verify, and modify Python** — locate the loop, the conditional, and the function in a script; change a parameter and predict the result; recognise generated code that does not do what was asked | 4.1 |
| 5 | **Name the computational operation a node performs** — which operation repeats, over what collection, producing what — in terms that transfer to code | Every module |
| 6 | Recognise the same logic in a graph and in code, and reimplement a system from one in the other | 2.1; 4.1 |
| 7 | Generate and control point fields, sections, patterns, and differentiated surfaces | 1.1, 2.1, 3.1 |
| 8 | Decompose a geometric problem into an explicit sequence of steps, expressed as pseudocode | 4.1; all modules |
| 9 | Prepare geometry correctly for computer-controlled cutting and additive manufacturing | 2.2, 3.2 |
| 10 | Evaluate and account for material and machine constraints — ordering, kerf, tolerance, manifold geometry, orientation | 1.2, 2.2, 3.2 |
| 11 | Assemble a fabricated system from computationally generated components | 2.2, 3.2 |
| 12 | Plan a multi-part fabrication run against machine, time, and material constraints | 3.2 |
| 13 | Analyze point, line, and plane as simultaneously graphic, spatial, and computational systems | Modules 1–3 |
| 14 | Develop and consistently apply a personal visual identity across a body of work | VIM, Booklet |
| 15 | Communicate computational and fabrication processes through diagrams, documentation photography, and annotation | All fabrication assignments, Booklet |
| 16 | Independently learn an unfamiliar computational workflow, extract its logic, and rebuild it as a reusable tool | 4.1 |

**Outcome 5 is the one the course is organized around.** Modules 0 through 3 name every operation in computational terms; Module 4 is where those names become code. Outcome 4 depends entirely on Outcome 5 having been met.
## Module 0 — Foundations
### Focus: Parametric Modeling

Module 0 introduces parametric, non-destructive modeling and the node interface.

**What is taught:**

- **Non-destructive modeling** — the difference between a model you have edited and a model that describes how it was made. Changing an early decision without rebuilding what follows.
- **What a parameter is** — a named value the definition depends on. Where parameters live, how to expose them, and why a number typed into a node is not the same as a number wired into it.
- **The interface** — the Geometry Nodes editor and the Grasshopper canvas. Adding a node, connecting one, reading what a wire carries.
- **Inputs and outputs** — every node takes something and returns something. Matching types, and what happens when the wrong thing is plugged into the wrong socket.
- **Transformations** — translate, rotate, scale, applied as parameters rather than by hand.
- **Boolean operations** — union, difference, intersection, building new solids from primitives. The result stays parametric: change a primitive and the boolean updates.

**Environment:** Blender Geometry Nodes or Grasshopper. Choose one and stay in it.

**Concepts:** Parameter · Node · Input and output · Wire · Data type · Non-destructive construction · Order of operations · Primitive solids · Translate, rotate, scale · Boolean union, difference, intersection

### Visual Identity Manual — briefed Week 1

A personal graphic system applied to every subsequent assignment. Drawings, diagrams, renders, captions, typography, and page layouts should work together rather than as separate decisions.

Briefed in the first class, with examples, and built in the background for seven weeks. It is the one piece of work that is not tied to a tutorial.

**Standards to define:** Personal logo · Color palette · Typography · Font hierarchy and sizing · Line weights · Captions · Image labels · Graphic hierarchy · Margins · Grid systems · 17" × 11" tabloid sheet template · Booklet cover

**Requirements**

- 8+ pages
- No more than 3 typefaces, with a hierarchy of 4+ levels
- 5+ color palette with stated values and written rationale
- 4+ defined line weights, each with an assigned use
- One tabloid template with the grid shown explicitly
- Built in a vector or layout editor, not a template-based tool

**This is a provisional system.** It is designed before you have content to test it against and is expected to change. A mandatory revision is submitted with the Final Booklet and assessed there.

**Deliverable:** Separate PDF. **Due Week 8 — Oct 13, with the Midterm · 7%**

### Assignment 0.1 — Parametric Massing Sequence

Form developed as an ordered sequence of geometric operations, each responding to an architectural rationale — program, orientation, circulation, views — built as a graph rather than modeled by hand.

The sheet is a **process diagram**: the sequence made visible, one operation at a time, resolving into a single finished image.

**Concepts:** Primitive solids · Translation · Rotation · Scale · Boolean union, difference, intersection · Parametric graphs · Axonometric and isometric representation · Exporting 3D geometry to 2D linework · Post-processing

**Requirements**

- 5+ Boolean operations
- 4+ distinct primitive types
- 2+ translations, 1+ rotation
- The graph is part of the submission. It must be intact, and you must be able to change any upstream parameter on request and have the result update
- All primitives generated in-session; no imported models
- An annotated screenshot of the graph on the sheet

**Assessed on** legibility of the operation sequence, quality of the axonometric set, and graphic execution of the final isometric.

**Deliverable:** One 17" × 11" sheet — one axonometric per operation, one larger final isometric with human scale, vegetation, context, shadows, and annotation, and the annotated graph. This sheet sets the documentation standard for the rest of the course. **Due Week 4 — Sep 15 · 7%**

### Assignment 0.2 — First Print

The massing from 0.1, prepared and printed. The course's introduction to additive fabrication at its simplest: does the geometry survive contact with a machine, and what has to be decided before it can.

**Concepts:** Manifold geometry · Watertight meshes · Print orientation · Overhangs · Supports · Layer height · Slicing · Print time · Machine queue

Three things are learned here, all of which return at system scale in 3.2:

- **Manifold geometry.** A Boolean that leaves an open edge or a self-intersection looks correct on screen and fails in the slicer. Node-based Booleans produce these readily.
- **Orientation.** The same solid prints differently depending on how it sits on the bed — surface quality, strength, and time all change.
- **Supports, by their absence.** **No supports are permitted on this print.** Banning them leaves orientation as your only lever, which is the fastest way to learn what orientation does. Supports become available in 3.2, once you know what you are buying with them.

**Requirements**

- Manifold, watertight geometry, verified in the slicer before submission
- An orientation diagram showing your chosen orientation, the overhangs it produces, and why you chose it over an alternative
- Estimated print time and material use, stated
- If the geometry cannot print unsupported in any orientation, revise the geometry — that is an expected outcome
- Within the stated print scope limit

**Assessed on** printability and on the reasoning behind your orientation decision. Craft and finish are not assessed here; those belong to 3.2.

**Deliverable:** Sliced file submitted to the queue plus a 17" × 11" sheet with the orientation diagram, **due Week 5 — Sep 22**. The **printed object is presented at the Week 8 Midterm Review**. No credit is issued for 0.2 without the print. **· 7%**

> The two-week cycle does not fit a shared printer. The file and sheet are due on rhythm; the object arrives when the queue delivers it. Plan for that — it is the first of three times this semester that a machine, not a deadline, sets your pace.
---

## Module 1 — POINT
### Focus: Computational Geometry

Module 1 teaches the principles of computational geometry, starting from a single point and building up. It is where the vocabulary is installed — every operation is named twice, once by its interface label and once by its computational term, and the second name is the one that carries through the rest of the course and into Module 4.

**What is taught:**

- **How a point is built** — a point is three numbers in order. Coordinates and data types.
- **Multiple points — the list.** Storing a collection, reading it by **index**, reading its **length**. The Spreadsheet editor is the list made visible: one row per element.
- **The loop.** One node operating on every element of a collection *is* a loop. It runs once per point, and there are four hundred points. A grid is a **nested loop**.
- **The conditional.** Testing a value and acting on the result — `Switch` and `Compare`, or `Dispatch` and `Stream Filter`. Filtering a collection.
- **Tiling and the tile** — reading a built façade as one repeated part: a panel, a brick, a shingle, a block. Designing that **tile** from a precedent, modeling it once, and stating the rule that fills the plane with it. Square, brick-bond, triangular and hexagonal tilings; Escher as the limit case, where identical tiles fill the plane with nothing left over.

  > **Tiling here, tessellation in Module 3.** Module 1 tiles a *flat* plane with one *identical* unit — the tile never changes, only where it is placed and what the field does to it. Module 3 tessellates a *curved* surface, where every cell is a different shape and the component has to morph to fit. Same instinct, very different problem, and the second one is unreadable without the first.
- **Arrays** — cartesian, radial, hexagonal, along a curve. Organizing points into structure, and how element order determines the order of everything downstream.
- **Fields** — measuring **distance**, **remapping** a measurement into a useful range, applying falloff. Single-point, multiple-point, and curve attractors. The field is generated and read **in 2D first** — as an image of distance across the plane — and only then attached to a module.
- **Imported points** — bringing a real site in as photorealistic 3D tiles, sampling it as a **point cloud**, and recognizing that cloud as the same list every other operation in this module has been working on. Decimation, point count, origin, and scale.
- **Generating geometry from points** — turning a collection of positions into vertices, edges, and instanced components.
- **Organizing geometry** — indices, attributes stored on the geometry itself, and sorting a list so that order carries meaning.

**Environment:** Blender Geometry Nodes or Grasshopper.

You will not write code in this module. You will be *saying* list, loop, index, conditional, and remap from the first week, and in Module 4 you will find out what each of them looks like typed out.

> **Where the loop hides.** Neither environment shows you repetition. A node applied to five hundred points simply operates on all five hundred — one node, one wire, five hundred results. That is a loop, and nothing on screen will tell you so. Every tutorial names it explicitly, and every pin-up asks you to. Watch the element count, not the picture.

**Visualization concepts:** Point · Coordinate · Point cloud · Field · Distribution · Density · Gradient · Scale · Proximity · Composition · Tile · Module · Tiling · Bond · Seam · Site

**Computational concepts:** List · Index · Length · Loop · Nested loop · Conditional · Function · Distance · Remapping · Falloff · Randomization and seed · Sampling · Decimation · Instancing

### Assignment 1.1 — POINT: Tiling + Arrays

An array is a system for organizing points in space, not a command for duplicating geometry. This assignment gives that system something real to organize: one tile, designed from a façade, and three ways of laying it out. **No attractors** — differentiation here comes from the index, not from distance. That is 1.2.

**Stage 1 — the precedent.** Briefed in Week 3 and brought to Week 4, so the modeling can start in the room. Find a façade built from one repeated part — a panel, a brick, a shingle, a cast block, a perforated plate. You are not analysing the whole building. You are looking at what it is made of, the way you would look at a brick wall and see the brick.

Bring a flat-on elevation photograph or drawing, the repeated part outlined on it, and its width, height and depth in millimetres. A curtain wall of plain glass or a one-off sculptural surface does not qualify: if you cannot point at the part and say *this, again and again*, it is the wrong building.

**Stage 2 — the tile.** Design your own tile, driven by the precedent — not traced from it. It is a panel or a brick: one object, built at the origin, at a stated real dimension, manifold and closed, and **deliberately simple**. Three to five primitives is plenty. It is about to be copied a thousand times, so every face you add is paid for a thousand times over.

Every copy is the **same tile**. Nothing about the tile itself changes across the field — that is what makes this a tiling rather than a panel system, and it is the difference between this assignment and Module 3.

**Stage 3 — the arrays.** Tile the plane with it, using **three** position systems of your choosing, drawn from the four below and each authored from base components:

| Array | The rule | Reads as |
|---|---|---|
| **Cartesian** | two counters, `i` and `j` — a nested loop | a square or stack bond |
| **Radial** | position from angle and radius, `i` driving the angle | a fan, a rose, a drum |
| **Hexagonal** | odd rows offset by half the spacing | a hex tiling, or a running brick bond |
| **Along a curve** | a curve you drew yourself, sampled at `t = i / n` | a course following an edge |

**Requirements**

- 1 precedent analysis — the building, the repeated part, and the rule that places it, in 3–4 sentences with a measured drawing of the part
- 1 tile designed from that precedent — manifold, built at the origin, dimensioned, 3–5 primitives
- **3 of the four array types** built with that tile and developed into finished compositions — your choice of which three
- 1+ composition containing 1,000 or more elements
- 1+ conditional that removes or alters a subset of the field based on a tested property — position, index, or a measured value
- 1+ array in which **changing the element order visibly changes the result**, demonstrated in a paired before/after image
- 1+ resolved spatially in 3D
- Minimum 2 sheets
- Arrays built from base components. Array add-ons, scatter and distribution tools prohibited

**On variation.** The tile is constant; the *field* is not. Rotation, spacing, culling and index-driven properties are all fair game, and the assignment requires the set to read as a system rather than as wallpaper. What you may not do is model a second tile.

**Assessed on** composition, density, rhythm, contrast, hierarchy, scale, and depth — on whether the set reads as a systematic exploration of one logic rather than three unrelated images — and on whether the tile is legibly descended from the precedent. A tile that could have come from anywhere is a weaker answer than one that clearly came from that building.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 6 — Sep 29 · 7%**

### Assignment 1.2 — POINT: Site Analysis Fields

An attractor turns distance into a value you can draw with. This assignment builds that instrument on a flat plane where its behaviour is legible, then points it at a real site and uses it to diagram something found there.

**Study A — the instrument.** Reviewed in Week 6. Take an array from 1.1 and drive it with attractors. Build the field before you attach anything to it: distance from an attractor is a value at every point on the plane, and that value can be looked at directly as a grayscale image. Read the image, adjust the falloff until the field itself is a good drawing, and only then let it drive your 1.1 module — scale, rotation, height, density, colour.

**Study B — the site.** Import a site of your choosing as a point field — photorealistic 3D tiles brought into Blender and sampled as a **point cloud** — and use attractors to diagram something about it. The difference from Study A is that the geometry is no longer yours: you did not place these points, you received them, and your job is to measure something across them.

A render shows what is on a site. A diagram argues something about it, and can therefore be disagreed with. Choose one condition and go deep rather than layering four shallow ones. The subject is yours; defending it is not optional.

| Category | Examples |
|---|---|
| **Access and movement** | entrances, desire lines, stops, crossings, parking |
| **Environment** | sun and shade, wind, noise, canopy, water, elevation, flood line |
| **Program and use** | what each mass does, density, frontage, vacancy, where people stop rather than pass |
| **Edge and boundary** | property lines, setbacks, thresholds, the seam where one condition becomes another |

**Requirements**

- All three attractor types across the set: single-point, multiple-point, curve
- 1 field shown **on its own as a 2D image**, before it drives geometry, with the falloff named
- 3+ distinct parameters driven by distance — scale, rotation, density, height, colour
- 1+ explicit remapping operation, with its input and output ranges stated on the sheet
- Falloff built, not called from a preset
- 1 site imported and reduced to a point field, with the **point count stated before and after** decimation, and the scale and origin declared
- 1 site condition measured and named, from the categories above
- 1+ attractor whose position is **argued from that condition in one written sentence** on the sheet, not chosen for the picture
- Your sheet states three things plainly: what you measured, where the attractor sits and why, and what varies over what range

**Topics:** List order · Index · Sorting · Point cloud · Sampling · Decimation · Georeferencing · Origin and scale · Field · Falloff · Remapping · Diagram versus render

**Conceptual workflow:** Point → Field → Site → Measurement → Claim → Diagram

**On the imported site.** The tile is data, not your design, and it is graded that way. Nothing rewards the model you downloaded; everything rewards what you measured against it and what you chose to show. State the source and the coordinates on the sheet, the way you would cite a survey.

**Assessed on** control of the field, the strength of the argument for where the attractors sit, whether the drawing reads as a diagram rather than an image of a place, and clarity of documentation.

**Deliverable:** Sheets covering both studies, in your visual identity. **Due Week 8 — Oct 13, with the Midterm · 7%**

---

## Module 2 — LINE
### Focus: Section and Sequence

Module 2 returns to the node graph. The subject is bisecting continuous geometry and building it back as a set of slices.

**What is taught:**

- **Sectioning** — intersecting a solid or surface with a series of planes to produce profiles.
- **Sequence** — keeping track of which slice came from where. Ordering the set so it can be read, drawn, and assembled.
- **Rebuilding as slices** — turning profiles into parts with material thickness, spaced so that the accumulation reconstructs the original volume.
- **Registration** — how each component knows where it goes without being measured during assembly.
- **Assembly strategies** — interlocking slots, threaded rod and spacers, bolted alignment, cable suspension, lamination, external frames. What each one does to the relationship between part and whole.
- **Materials, light, and filtering** — what a stack of slices does to light passing through it, and how that is rendered.

**Environment:** Blender Geometry Nodes or Grasshopper.

**Preset node groups are supplied.** Signed-distance-field conversion, contour extraction, and profile ordering are handed to you as working groups. Building them is not what this module assesses.

Using a supplied group carries one condition: you must be able to say what it does in the terms taught in Module 1 — which operation repeats, over what collection, producing what. See *Prohibited Shortcuts*.

**Visualization concepts:** Line · Direction · Profile · Section · Contour · Sequence · Material · Light · Filter · Transparency · Depth

**Computational concepts:** Iteration over a collection · Conditional filtering · Boolean logic · Ranges · Relationships between lists · Geometric intersections · Signed distance fields

Workflow, stated procedurally: generate geometry → generate section planes → iterate through the planes → intersect each with the geometry → store the profiles → filter or modify → order the set → visualize or fabricate.

### Assignment 2.1 — LINE: Section + Light

A composition built from a sectioned system, in which **material, light, and filtering** are the primary graphic subject. What does a stack of slices do to light passing through it — what is revealed, what is occluded, what reads as depth.

Section is explored beyond the conventional section drawing: serial, overlapping, directional, data-driven. The result may be abstract, spatial, analytical, architectural, or representational.

**Requirements**

- 1+ system generated from 20 or more serial sections
- 2+ distinct section directions
- 1+ rendered image with controlled lighting, demonstrating what the section stack does to light
- 2+ distinct materials, with their optical behavior (transparency, translucency, reflectivity) doing visible work
- 1+ conditional filter that removes or modifies a subset of profiles based on a tested property
- **One system carried forward from Module 1**, developed rather than repeated, with a short diagram showing what changed
- You must be able to explain every supplied group you used

**Assessed on** material and light, depth, transparency, figure/ground, density, and contrast.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 11 — Nov 3 · 7%**

### Assignment 2.2 — LINE: Section-Based Fabrication
**Fabrication: Computer-Controlled Cutting**

The sectioned system, cut and assembled so that the slices generate depth by accumulation.

**The assembly strategy is yours to determine.** Interlocking slots — the waffle — are one answer. So are sections stacked on threaded rod, spaced by sleeves or washers, bolted through aligned holes, suspended from cables, laminated face to face, or held in an external frame.

What every strategy shares is **registration**: each component must know where it goes. Design that system and make it legible.

**Workflow:** Generate geometry → establish section direction(s) → generate section planes → intersect → extract profiles → give profiles material thickness → design the registration and connection system → label components → nest → prepare files → cut → test fit → assemble.

**Fabrication concepts:** Computer-controlled cutting · Laser cutting · 2D machine files · Material thickness · Kerf · Tolerance · Registration · Slots and joinery · Fasteners, spacers, and tension elements · Nesting · Component labeling · Assembly sequence

**Requirements**

- 12+ sections generated computationally, not drawn
- A registration system that positions every component without measurement during assembly
- Kerf and tolerance measured on your own test cut and stated on the sheet — not assumed
- All components labeled, with labels legible in the assembled object or documented in the exploded diagram
- Nesting layout submitted, with material efficiency stated
- The assembly must be self-supporting, or its support strategy explicitly designed

**Assessed on** fit and tolerance, craft of assembly, coherence between the chosen strategy and the geometry it serves, efficiency of nesting, and clarity of documentation.

**Deliverable:** Laser-cut sectional assembly within the stated scope limits, plus photographic documentation, an exploded assembly diagram, and the nesting layout. **Due Week 12 — Nov 10 · 7%**

---

## Module 3 — PLANE
### Focus: Modularity and Tessellation

Module 3 builds the most complex definitions of the course: a vault or façade system, tessellated into panels, with variation authored across the field.

This is where **tessellation** enters properly. Module 1 tiled a flat plane with one identical tile; here the surface is curved, every cell is a different shape, and the component has to morph to fit it. The word was withheld until now on purpose.

**What is taught:**

- **Tessellation** — dividing a *curved* surface into cells, as opposed to the flat tiling of Module 1. Quad, triangular, and hexagonal subdivisions, and what each does to curvature.
- **Modularity** — designing one component and mapping it onto every cell. Why a component that reads cleanly on a plane will not necessarily close on a curve.
- **Grids as two-dimensional data** — a grid is a list of lists. UV coordinates, and mapping a component into a cell's local space.
- **Vault systems** — curvature, panel distortion, and the structural logic of a doubly curved assembly.
- **Variation across a field** — driving panel parameters from the attractor and remapping logic built in Module 1, now applied to a component rather than a point.

Definitions here are longer and more nested than anything in Modules 0 or 2, and they are the last node work before Module 4 shows you the same logic in code.

**Environment:** Blender Geometry Nodes or Grasshopper.

**Visualization concepts:** Plane · Surface · Curvature · Vault · Pattern · Filter · Layer · Panel · Aperture · Porosity · Relief · Tessellation

**Computational concepts:** Nested loops · Grids · Two-dimensional data structures · UV coordinates · Data mapping · Remapping · Conditional variation

**Panelization tools are permitted in this module.**

| Environment | Tools |
|---|---|
| Blender | **Tissue** (Zomparelli) — Tessellate maps a component object onto the faces of a base mesh; also Dual Mesh and weight/color exchange |
| Grasshopper — native | **Surface Box + Box Morph** — the structural equivalent of Tessellate, no plugin required. Start here. |
| Grasshopper — plugins | **Paneling Tools** (Issa, McNeel) · **Pufferfish** (Pryor) · **LunchBox** · **Weaverbird** |

The tool may generate the tessellation. **The differentiation across it must be yours** — your parameters, your mapping, your remapping ranges. A field of identical panels produced by a plugin does not answer this assignment.

### Assignment 3.1 — PLANE: Surface + Filtering

A computational graphic exploring the plane as a variable surface or filter. Rendering, lighting, shadow, and materiality carry the image.

**3.1 and 3.2 describe the same system.** The graphic shows the surface whole; the print realizes a 3 × 3 fragment. Choose a vault or a façade here and develop it in both.

**Requirements**

- A field of 400+ cells or panels (minimum 20 × 20)
- 2+ independent parameters driving the variation
- 1+ explicit remapping operation, with input and output ranges documented on the sheet
- **Three views of the same system:** overall, close-up detail, and eye-level or oblique
- 1+ rendered image with controlled lighting demonstrating the filtering behavior
- Panelization and tessellation tools are permitted; the variation driving them must be authored

**Assessed on** surface, figure/ground, pattern, repetition, variation, transparency, depth, shadow, and material appearance.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 13 — Nov 17 · 7%**

### Assignment 3.2 — PLANE: Additive Fabrication
**Fabrication: 3D Printing**

The surface system from 3.1, fabricated as an architectural element — **either a vaulted structure or a façade fragment**, panelized into physical components that connect to one another.

A vault introduces a condition the flat sheet does not: panels on a doubly curved surface distort, and a component that reads cleanly on a plane will not necessarily close on a curve. Resolving that is half the assignment.

The other half is **fabrication management**. Nine or more parts, one shared machine, a fixed deadline, and a queue shared with the rest of the cohort. How many objects, how long each takes, in what order, batched how, with what margin for a failed print — answered before the first file is sliced.

**Differentiation costs production time.** Nine identical panels batch efficiently and teach nothing; nine wholly unique panels may not finish. Where you land between those is a design decision with fabrication consequences, and defending that position is assessed.

**Requirements**

- **Minimum 9 panels** (3 × 3 or equivalent) forming a continuous assembly
- Panel-to-panel connections designed, not improvised — the assembly must hold together
- Variation across the panel set; nine identical panels do not meet the requirement
- **A production plan, submitted Week 13 (Nov 17) before the queue opens:** panel count, estimated print time per panel, total machine hours, batching and orientation strategy, print order, and the contingency for a failed print
- Manifold, watertight geometry with stated wall thickness
- **Supports are permitted but must be minimized and justified.** Orientation remains the first tool
- Within the stated print scope limits

**Fabrication concepts:** Manifold geometry · Meshes · Surface thickness · Resolution · Layer height · Print orientation · Supports · Slicing · Toolpaths · Material use · Print time · Tolerances · Panel connections · Production planning · Batching · Machine scheduling · Failure contingency

**Assessed on** printability, print quality, resolution of the panel connections, realism of the production plan and how well the built result matches it, appropriateness of orientation and layer decisions, and clarity of documentation.

**Deliverable:** 3D-printed vault or façade fragment of 9+ panels within the stated scope limits, plus photographic documentation and a slicing/orientation diagram. **Due at the Final Review, Dec 10–16 · 7%**

> **Print queue:** Files must be submitted to the FabLab queue by the end of Week 13 (Nov 17). Prints submitted later are not guaranteed to complete before the deadline, and queue congestion is not grounds for an extension. The object is presented at the Week 15 final review; its documentation may be added to the Booklet within 48 hours of the review.
---

## Module 4 — TOOL
### Focus: AI-Assisted Tool Building

Module 4 is the only code in the course, and it asks for an instrument rather than an image. Three stages: **study** an existing workflow, **extract** its logic, **build** your own tool from it.

A result is one image. A tool takes inputs and produces a family of outputs — it is reusable, and someone else could run it. This assignment asks for the second.

Coding assistance is a taught subject here. Language models write Python fluently and are unreliable in geometry APIs. **The skill assessed is not writing code but reading it and catching where it is wrong** — which is exactly what ten weeks of naming operations has prepared you for.

**Environment:** Python, a node group, or a Grasshopper definition. Environments beyond the four used this semester are permitted.

**No fabrication output.**

A **one-paragraph proposal** naming the workflow you intend to study and what you expect to build from it is due Week 14 (Nov 24).

### Stage 1 — Study

Find a workflow that interests you: a tutorial, a shared definition, a published paper, an existing add-on. Grasshopper, Blender Geometry Nodes, Houdini, TouchDesigner, Processing, Three.js, or anything else procedural. Follow it until it works and you understand why.

### Stage 2 — Extract

Write the logic as **pseudocode in your own words**, independent of the original's interface. Not "plug the Populate 2D into the Voronoi" but what the procedure does, step by step, in language that would survive being carried to another platform.

Separating a procedure from the software that expressed it is the most transferable skill in the course.

### Stage 3 — Build

Implement that logic as **your own tool**, with named inputs a user can change. Coding assistance is permitted under the Stage 2 AI terms, with your pseudocode written first and the prompt log submitted.

Your tool must demonstrate at least **two** substantive departures from the original:

- A different data source or input drives the system
- The dimensionality or topology of the output is changed
- A step in the procedural logic is replaced, not merely re-parameterized
- The system is extended with logic not present in the original
- The workflow is reimplemented in a different environment

Changing colors, materials, or slider values does not count.

**Required content across the two sheets:** Screenshot and full link to the original · Your pseudocode · A diagram of the extracted logic · The original's result, reproduced · Your tool, with inputs labeled · **At least three outputs produced by varying its inputs** · Full AI prompt log where applicable · Written explanation of what you changed and why

**Live demonstration.** At the final review you will run your tool with inputs you have not prepared in advance. **A student who cannot explain or operate their own tool receives no credit for Computational Understanding, regardless of whether it runs.**

**Deliverable — two 17" × 11" sheets**, plus the tool file submitted with the Booklet materials.

| Sheet | Content |
|---|---|
| **1 — Process** | The original workflow, your pseudocode, the original's result reproduced, and a diagram of the extracted logic. Answers *how did you get from their thing to yours.* |
| **2 — Tool** | The tool with inputs labeled, and three outputs produced by varying those inputs, arranged so the effect of each input is legible. Answers *what does it do.* |

**Due:** Final Review, Dec 10–16 · **Weight: 13%**

> This is your first contact with code. Everything you have named for ten weeks — loop, list, index, conditional, function, remap — already exists in your head; Module 4 shows you what it looks like typed out. Its three tutorials run from Week 9 in parallel with Modules 2 and 3, so the reading has five weeks to settle before the tool is due.

---

## Midterm Review — Week 8, Oct 13

Students **print and present all work completed to date**, in its latest revised form, using their visual identity:

- Visual Identity Manual
- 0.1 Parametric Massing Sequence — sheet
- 0.2 First Print — sheet **and the print itself**
- 1.1 POINT: Tiling + Arrays
- 1.2 POINT: Site Analysis Fields

The printed set is what is reviewed. Work shown on a screen is not assessed.

**The midterm does not re-grade individual assignments.** Those grades stand. It assesses what only an assembled body of work can show:

| Component | Share of midterm grade |
|---|---|
| Evidence of revision in response to critique received so far | 40% |
| Coherence of the visual identity across the set | 30% |
| Quality of print, layout, and documentation | 30% |

**Weight: 8%**

This is also the formal point at which students receive a standing in the course while there is still time to act on it.

---

## Prohibited Shortcuts

Several assignments name tools that may not be used. The rule: **a tool that automates the concept an assignment exists to teach may not be used in that assignment — until you can say what it does.**

| Assignment | Prohibited | Permitted |
|---|---|---|
| All sheets, VIM, Booklet | Canva, Adobe Express, template-driven layout apps, PowerPoint, Google Slides | Vector or raster editors |
| 0.1 | Imported or downloaded models; any geometry not generated in-session | Any node-based boolean and transform operations |
| 1.1 / 1.2 | Array add-ons, scatter and distribution tools, preset attractor falloff plugins. The array, the distance measurement, and the remapping must be built from base components. **Downloaded models may not stand in for the 1.1 tile** — it is designed and modeled by you, from your precedent | Everything else in the node editor. In **1.2 only**, an imported site and its point cloud are permitted and expected — the tile is the thing you measure, never the thing you submit |
| 2.1 / 2.2 | Nothing prohibited | Supplied section, SDF, and contour groups, subject to the explanation requirement |
| 3.1 / 3.2 | Preset gradient, attractor, and variation components — the differentiation must be authored | Panelization and tessellation libraries |
| 4.1 | Nothing prohibited | Everything, including coding assistance under the Stage 2 AI terms |
| All Grasshopper work | The Cross Reference component may be used **once** per definition | |

### The explanation requirement

From Module 2 onward, using a supplied or third-party group carries one condition: **you must be able to state what it does in the vocabulary taught in Module 1** — which operation repeats, over what collection, producing what output.

A student who cannot do that for a group they used receives **no credit for Computational Understanding** on that assignment, regardless of how the image looks. This is tested at pin-up alongside live modification and takes about thirty seconds.

Module 1 is where the vocabulary is installed; Modules 2 and 3 are where it buys you something.

Use of a prohibited tool is assessed as a failure to meet Assignment Requirements for that submission.
---

## Final Submission — Booklet + Visual Identity Manual

Two separate PDF files, due at the Final Review (Dec 10–16).

### 1. Final Booklet — **Weight: 11%**

The Final Booklet contains all course assignments in their latest revised form. Students are expected to incorporate feedback received throughout the semester rather than resubmit original work.

Contents: 0.1 Parametric Massing Sequence · 0.2 First Print · 1.1 Tiling + Arrays · 1.2 Site Analysis Fields · 2.1 Section + Light · 2.2 Section-Based Fabrication · 3.1 Surface + Filtering · 3.2 Additive Fabrication · 4.1 TOOL (both sheets)

Physical assignments must be documented through high-quality photography, diagrams, and captions. All pages use the student's visual identity at 17" × 11" tabloid size.

**How the Booklet is graded.** The Booklet grade does **not** revise the grades already earned on individual assignments. Those stand. The Booklet's 11% assesses three things that only the Booklet can assess:

| Component | Share of Booklet grade |
|---|---|
| Evidence of substantive revision in response to critique | 40% |
| Quality of documentation — photography, diagrams, captions | 35% |
| Coherence of the visual identity across the full body of work | 25% |

Ungraded booklet progress check is held in Week 12 (Nov 10). The Week 8 Midterm Review serves the same function for the first half of the semester.

### 2. Visual Identity Manual

Submitted as a separate PDF, documenting the graphic standards as revised over the semester. The revision from the Week 4 version is assessed as part of the Booklet's revision component.

---

## Course Evaluation Method

| Item | Module | Weight |
|---|---|---|
| VIM — Visual Identity Manual | — | 7% |
| 1.1 — Massing Sequence | 1 | 7% |
| 1.2 — First Print | 1 | 7% |
| 2.1 — Panel from Lists | 2 | 7% |
| 2.2 — Arrays | 2 | 7% |
| 3.1 — Field + Plotter Drawing | 3 | 7% |
| 3.2 — Site Analysis Field | 3 | 7% |
| 4.1 — Panelized Surface | 4 | 7% |
| 4.2 — Multi-part Print | 4 | 7% |
| 5.1 — Volume, Section and Light | 5 | 7% |
| 5.2 — Section-Based Fabrication | 5 | 7% |
| **Midterm Review (Oct 13)** | — | 7% |
| Final Booklet | — | 11% |
| Attendance and participation | — | 5% |
| **Total** | | **100%** |

The nine module assignments carry equal weight. The Midterm and the Final Booklet are the only items that assess the body of work rather than a single submission, and neither re-grades work already assessed.

### Evaluation Criteria

Each assignment is assessed against the following criteria. Percentages indicate the share of that assignment's grade.

| Criterion | Digital assignments (VIM, 0.1, 1.1, 2.1, 3.1, 4.1) | Fabrication assignments (0.2, 1.2, 2.2, 3.2) |
|---|---|---|
| **Visual Quality** — composition, hierarchy, contrast, color, typography, line weight, image quality, graphic impact | 35% | 20% |
| **Computational Understanding** — assessed primarily through live modification of your own work at pin-up, and from Module 2 onward through explanation of any supplied group you used (see *Prohibited Shortcuts*); secondarily through pseudocode and written explanation | 25% | 20% |
| **Technical Execution** — competent use of modeling, visualization, and computational workflows | 20% | 15% |
| **Fabrication Quality** — geometry preparation, material and machine constraints, assembly, craft, quality of the physical artifact | — | 30% |
| **Creativity + Experimentation** — willingness to explore, iterate, modify techniques, and produce distinctive results | 10% | 5% |
| **Requirements + Visual Identity** — satisfaction of stated deliverables and constraints; consistency of graphic language | 10% | 10% |
### Performance Levels

| Level | Range | Description |
|---|---|---|
| Exemplary | 94–100 | Meets all requirements; the work is visually distinctive and technically assured; the student can explain and defend every procedural decision; evident iteration beyond the assigned minimum |
| Proficient | 83–93 | Meets all requirements competently; procedural logic is understood and explicable; visual and technical execution is solid with minor lapses |
| Developing | 70–82 | Requirements partially met; procedural logic is applied but incompletely understood; visual or technical execution is inconsistent |
| Insufficient | Below 70 | Requirements substantially unmet; the student cannot account for the logic of their own work; execution does not meet the assignment's stated constraints |

---

## Course Grading Scale

| Letter | Percentage | | Letter | Percentage |
|---|---|---|---|---|
| A | 100 – 94% | | C+ | < 80 – 77% |
| A- | < 94 – 90% | | C | < 77 – 73% |
| B+ | < 90 – 87% | | C- | < 73 – 70% |
| B | < 87 – 83% | | D+ | < 70 – 67% |
| B- | < 83 – 80% | | D | < 67 – 63% |
| | | | D- | < 63 – 60% |
| | | | F | < 60 – 0% |


---

## Class Format

Every class does three things, in this order:

1. **Pin-up and critique** of the assignment due today.
2. **Tutorial review** — questions, troubleshooting, examples of what the tutorial makes possible. Bring the file, not just a description of the problem.
3. **Assignment briefing** for the work due in two weeks.

The next tutorial is released immediately after class.

### The two-week cycle

| | |
|---|---|
| **After class** | Tutorial released |
| **Next class** | Tutorial reviewed · assignment briefed |
| **Class after** | Assignment due, pinned up and critiqued |

Every assignment therefore has two weeks: one to watch the tutorial and try it, one to make the work after the brief. The tutorial is always watched **before** the class that discusses it. A session spent watching what you could have watched at home is a session not spent on your own problem.

**Every tutorial ships in two versions** — Grasshopper and Blender Geometry Nodes — implementing the same logic. Watch the version for your environment; skim the other at least once per module.

**Every tutorial names its operations twice**: once by the interface label, once by the computational term. The second name is the one used in critique and assessment, and it is the one that carries into Module 4.

---

## Tutorial Calendar

Tutorials are released after class and reviewed at the start of the next one. Each covers one idea; the modules that consume it are named in **Feeds**.

| # | Tutorial | Released after | Reviewed | Feeds | Covers |
|---|---|---|---|---|---|
| **1.1** | Parametric Modeling and Booleans | Week 1 | Week 2 | **1.1** | The node editor: adding and connecting nodes, inputs and outputs, data types. What a **parameter** is. Translate, rotate and scale as parameters. Union, difference and intersection building new solids from primitives, non-destructively |
| **1.2** | 3D Printing Basics | Week 2 | Week 3 | **1.2** | Manifold checking, orientation, supports, layer height, slicing, sending a file to the queue |
| **2.1** | Points, Lists and Data Structures | Week 3 | Week 4 | **2.1** | A point is three numbers in order. Many points are a **list**: `Index`, `Domain Size`, **append**, **pop**, selecting an item, mixing two lists. **Graft** and **flatten** — changing list structure without touching contents. The Spreadsheet editor as the list made visible |
| **2.2** | Building a Mesh from Lists | Week 4 | Week 5 | **2.1** | `v = [x, y, z]` → `e = [v1, v2]` → `f = [v1, v2, v3]` → `mesh = [f1, f2, f3 …]`. Constructing geometry by describing it rather than drawing it. Winding order and normals. Reverse-engineering a panel from a precedent, vertex by vertex |
| **2.3** | Arrays | Week 5 | Week 6 | **2.2** | One node over every element **is a loop**; a grid is a **nested loop**. `Switch` and `Compare` as the **if statement**. Cartesian · radial · hexagonal · along a curve, and how element order determines everything downstream |
| **3.1** | Fields and Attractors | Week 6 | Week 7 | **3.1** | Measuring **distance**. Generating and reading the field **as a 2D image** before it drives anything. `Map Range` as **remap**, with input and output ranges stated. Falloff. Single-point, multiple-point and curve attractors |
| **3.2** | Ordering Geometry for the Machine | Week 8 | Week 9 | **3.1** | Sorting and reversing a list, serpentine ordering. Travel moves versus drawing moves, pen up and pen down. Running the plotter |
| **3.3** | Point Clouds and Site Data | Week 8 | Week 10 | **3.2** | Importing photorealistic 3D tiles into Blender. Sampling a surface as a **point cloud**, decimating it, and declaring origin and scale. Attracting against points you did not place |
| **4.1** | Tessellation, Modularity and Variation | Week 10 | Week 11 | **4.1** | Surface Box / Box Morph and Tissue Tessellate. UV domains, component morphing, panel distortion on a curved surface. A grid is a **list of lists**. Driving panel parameters from the Module 3 attractor logic |
| **4.2** | Additive Fabrication Strategies | Week 11 | Week 12 | **4.2** | Panel connections, wall thickness, print orientation for a set, batching and production planning |
| **5.1** | SDF and Volumetric Modeling | Week 12 | Week 13 | **5.1** | Signed distance fields: a shape described as a function rather than a surface. Booleans on fields, smooth minimum, offsetting and shelling. Meshing a field for output |
| **5.2** | Sectioning, Sequence and Light | Week 13 | Week 14 | **5.1** | Bisecting a volume with section planes; ordering the slices. Rendering a section stack: transparency, translucency, shadow |
| **5.3** | Laser Cutting | Week 14 | Week 15 | **5.2** | 2D machine files from a section stack. Kerf and tolerance, slots and registration, nesting, labeling, assembly sequence |
| **X** | *Translation — the graph, written out* | Week 15 | — | *extra credit* | The vocabulary table line by line. For every node used all semester, the code that does the same thing: `for`, `if`, `def`, lists, indices, `remap()`. Optional, and the only tutorial with no assignment attached to it |

**Two tutorials cover what used to be one.** Points and lists (2.1) is separated from arrays (2.3), with mesh construction (2.2) between them, because building geometry from a list is the idea Module 2 exists to install and it cannot be taught in the same breath as the thing that repeats it.

---

## Assignments

| # | Assignment | Briefed | Due | Weight |
|---|---|---|---|---|
| **VIM** | Visual Identity Manual | Week 1 | Week 8 — with the Midterm | 7% |
| **1.1** | Massing Sequence — sheet | Week 2 | Week 4 | 7% |
| **1.2** | First Print — file, orientation sheet, and print | Week 3 | Week 5 · print at Midterm | 7% |
| **2.1** | Panel from Lists — geometry described, not drawn | Week 4 | Week 6 | 7% |
| **2.2** | Arrays — the panel, three ways | Week 6 | Week 8 | 7% |
| **3.1** | Field + Plotter Drawing | Week 8 | Week 10 | 7% |
| **3.2** | Site Analysis Field | Week 10 | Week 12 | 7% |
| **4.1** | Panelized Surface — sheet | Week 11 | Week 13 | 7% |
| **4.2** | Multi-part Print | Week 12 | Final Review | 7% |
| **5.1** | Volume, Section and Light — sheet | Week 13 | Final Review | 7% |
| **5.2** | Section-Based Fabrication — laser | Week 14 | Final Review | 7% |
| **XC** | *Translation to Python — a working tool* | Week 15 | Final Review | *up to +5% extra credit* |

**Extra credit is genuinely optional.** The last class of the semester shows how the graph you have been building all term looks written out as code. Students who want to carry one of their own definitions across and expose it as a tool may do so for up to five points on top of the final grade. Students who do not are not penalised, and nothing else in the course depends on it.

---

## Course Topical Outline — 15-Week Schedule

Class meets Tuesdays, 5:00–7:50 PM. Three School-wide windows constrain this schedule and are marked below.

**Key dates**

| Date | |
|---|---|
| Aug 22 (Sat) | Classes begin |
| Sep 7 (Mon) | Labor Day — University closed (no effect on this section) |
| Oct 5–9 | **Midterm Studio Reviews** — non-studio courses may not set due dates |
| Oct 12–16 | **Non-studio midterm assignments** — this course's Midterm Review falls here |
| Oct 20 (Tue) | Midterm grades due in Canvas |
| Oct 30 (Fri) | Last day to drop with a grade of "W" |
| Nov 11 (Wed) | Veterans Day — University closed (no effect on this section) |
| Nov 25–29 | Thanksgiving break — University closed |
| Dec 1–4 | **Final Studio Reviews** — non-studio courses may not set due dates |
| Dec 7 (Mon) | Last day of classes |
| Dec 10–16 | **Non-studio final assignments** — this course's Final Review falls here |
| Dec 21 (Mon) | Final grades due |

| Wk | Date | Due today | Tutorial reviewed | Briefed today | Released after class |
|---|---|---|---|---|---|
| | | **Weeks 1–7: AI-free. Coding assistance permitted from Week 8 onward, with disclosure.** | | | |
| **1** | Aug 25 | — | — | Syllabus, rules, course structure. **Visual Identity Manual**, with examples | **T1.1** |
| **2** | Sep 1 | — | T1.1 — parametric modeling, booleans | **1.1 Massing Sequence** | **T1.2** |
| **3** | Sep 8 | — | T1.2 — 3D printing | **1.2 First Print.** *Printer queue opens.* Panel precedent set — bring it Week 4 | **T2.1** |
| **4** | Sep 15 | **1.1** — pin-up · precedent brought | T2.1 — points, lists, data structures | **2.1 Panel from Lists** | **T2.2** |
| **5** | Sep 22 | **1.2** — file + orientation sheet | T2.2 — building a mesh from lists | Working session on 2.1 | **T2.3** |
| **6** | Sep 29 | **2.1** — pin-up | T2.3 — arrays | **2.2 Arrays** | **T3.1** |
| **7** | Oct 6 | — | T3.1 — fields and attractors | Working session on 2.2. *Midterm Studio Reviews week — nothing due* | **T3.2 + T3.3** |
| **8** | Oct 13 | **MIDTERM** · **VIM** · **2.2** · 1.2 print presented | — | **3.1 Field + Plotter Drawing.** **Live modification and naming begin** | — |
| **9** | Oct 20 | — | T3.2 — ordering for the machine | Plotter demonstration and production session. *Midterm grades posted* | — |
| **10** | Oct 27 | **3.1** — drawing + toolpath diagram | T3.3 — point clouds and site data | **3.2 Site Analysis Field** | **T4.1** |
| **11** | Nov 3 | — | T4.1 — tessellation, modularity, variation | **4.1 Panelized Surface** | **T4.2** |
| **12** | Nov 10 | **3.2** — pin-up | T4.2 — additive fabrication strategies | **4.2 Multi-part Print.** Booklet progress check | **T5.1** |
| **13** | Nov 17 | **4.1** — pin-up | T5.1 — SDF and volumetric modeling | **5.1 Volume, Section and Light.** *Print queue closes end of week* | **T5.2** |
| **14** | Nov 24 | **4.2 production plan** | T5.2 — sectioning, sequence, light | **5.2 Section-Based Fabrication.** Print production. *Thanksgiving follows* | **T5.3** |
| **15** | Dec 1 | — | T5.3 — laser cutting | Laser production session. Final desk crits. Booklet layout workshop. **Translation to Python — extra credit shown.** *Final Studio Reviews week — nothing due* | **TX** |
| **—** | Dec 10–16 | **4.2 print · 5.1 sheets · 5.2 laser assembly · Final Booklet · Visual Identity Manual** *(+ optional Python tool)* | | **FINAL REVIEW** `[CONFIRM exam slot]` | |

**Four constraints shaped this schedule.** Week 7 falls in Midterm Studio Reviews, so nothing is due — it is a working session, and 2.2 lands at the Week 8 Midterm instead. Week 15 falls in Final Studio Reviews, so it is a production and crit session and the final submission moves to the University exam period. Midterm grades are due Oct 20, one week after the Midterm Review, which leaves no slack. The Oct 30 "W" deadline falls after grades post, so students have a standing before the drop decision.

**Where the machines sit.** Three fabrication processes run in the second half: the plotter in Week 9, the printer from Week 12 to the queue close in Week 13, and the laser in Weeks 14–15. They are deliberately staggered so no two share a production week, but the back half is dense and the print queue closing before Thanksgiving is the tightest link in the chain. `[TBD — Module 5 has three weeks for two assignments and both land at the Final. If that proves too heavy, the levers are merging 5.1 and 5.2 into one 14% assignment, or moving the section-and-light sheet to a Week 15 pin-up.]`

**Two places the rhythm bends.** Assignment 1.2's print is submitted as a file in Week 5 but presented at the Week 8 Midterm, because the queue has latency the two-week cycle does not. Module 2 runs three weeks rather than two, because building geometry from lists is the slowest idea in the course to land and the arrays that follow are worthless without it.

---

## Artificial Intelligence Preamble

FAU recognizes the value of generative AI in facilitating learning. However, output generated by artificial intelligence (AI) — written words, computations, code, artwork, images, music, and so on — is drawn from previously published materials and is not your own original work.

FAU students are not permitted to use AI for any course work unless explicitly allowed to do so by the instructor of the class for a specific assignment. [Policy 12.16 Artificial Intelligence]

Class policies related to AI use are decided by the individual faculty. Some faculty may permit the use of AI in some assignments but not others, and some faculty may prohibit the use of AI in their course entirely. In the case that an instructor permits the use of AI for some assignments, the assignment instructions will indicate when and how the use of AI is permitted in that specific assignment. It is the student's responsibility to comply with the instructor's expectations for each assignment in each course. When AI is authorized, the student is also responsible and accountable for the content of the work. AI may generate inaccurate, false, or exaggerated information. Users should approach any generated content with skepticism and review any information generated by AI before using generated content as-is.

If you are unclear about whether or not the use of AI is permitted, ask your instructor before starting the assignment.

Failure to comply with the requirements related to the use of AI may constitute a violation of the Florida Atlantic Code of Academic Integrity, Regulation 4.001.

**Proper Citation:** If the use of AI is permitted for a specific assignment, then use of the AI tool must be properly documented and cited. For more information on how to properly cite the use of AI tools, visit https://fau.edu/ai/citation


---

## AI Language Specific To This Course

This course draws two lines. The first separates AI as an aid to *understanding procedure* from AI as a substitute for *visual judgment*. The second is a line in time: coding assistance is unavailable until the vocabulary needed to evaluate it has been taught.

### Why the timing matters

Reading generated code feels like understanding it. Students consistently overestimate how much they have grasped from a script they can follow line by line, and the gap only appears when something breaks. Large language models are also markedly less reliable in geometry APIs — `bpy`, RhinoScriptSyntax, Grasshopper Python — than in more common domains, because there is less training data and the interfaces change often. Confidently wrong code is the normal case, not the exception.

That makes generated code an excellent teaching instrument for a student who can detect the error, and a quiet dead end for one who cannot. So the vocabulary comes first.

Modules 0 through 3 give you that vocabulary without a line of code. By the time Module 4 asks you to build a tool with an assistant, you know what a loop, a conditional, and a remap are — you simply have not seen them typed. Auditing generated code is then a reading problem, not a writing one.

### Stage 1 — Weeks 1 through 7: AI-free

No AI assistance of any kind in producing coursework through the Week 8 Midterm. This covers **all of Module 0 and all of Module 1** — the Visual Identity Manual, 0.1, 0.2, 1.1, and 1.2.

Permitted throughout, at any stage: asking an AI to explain a computational concept, clarify syntax, or interpret an error message. Not permitted: asking it to write, complete, or fix your code.

This period exists so that list, index, loop, conditional, and remap are installed as your own working vocabulary. 1.2 depends on it: the lesson is that data ordering determines what the machine draws, and it is learned by getting the ordering wrong and working out why.

### Stage 2 — Week 8 onward: coding assistance permitted, with disclosure

From Week 8, AI may be used to generate, debug, refactor, or explain **code**. In practice this matters from Module 4, which is where code appears. It is subject to:

- **Pseudocode first.** Your own written decomposition of the problem must precede any code generation, and is submitted alongside it. AI-generated pseudocode submitted as your own procedural reasoning is a violation.
- **Full disclosure.** Tool and version, the prompts used, what was kept, and what was changed. Citation follows https://fau.edu/ai/citation.
- **Live modification and group explanation** (see below).

### Not permitted at any stage

- **Generative image models** — Midjourney, Stable Diffusion, DALL·E, Firefly, or any diffusion-based tool — to produce, extend, or modify any image submitted as coursework. This includes backgrounds, textures, entourage, generative fill, and AI upscaling.
- AI generation of the visual identity system, including logo, palette, and layout.

The reason is specific rather than reflexive: in 1.1, 2.1, and 3.1 the assessed outcome *is the image*. Delegating its production removes the exact judgment the assignment exists to develop. In the computational work, the assessed outcome is procedural understanding, and an assistant does not remove that — provided you can account for what the code does.

### Live Modification

At every pin-up and review from Week 8 onward, each student will be asked to make **one unscripted change to their own work in front of the class** — reverse a section order, alter an attractor's falloff, add a conditional, change a mapping range. Roughly ninety seconds per student.

This, rather than a written explanation, is the primary assessment of Computational Understanding. It applies equally to scripted and node-based work, and equally whether or not AI was used.

It is paired with a second, shorter question: **name a node or group in your definition and say what it does** — which operation repeats, over what collection, producing what. About thirty seconds. Supplied groups are fair game, and so is anything you downloaded.

A student who cannot modify their own submitted work, or cannot account for a component in it, receives no credit for Computational Understanding on that assignment, regardless of whether the work runs or how it looks. Where the work is demonstrably not the student's own, this may constitute a violation of Regulation 4.001.

### Accountability

Students are responsible for the accuracy and behavior of any AI-assisted output they submit. AI may generate geometry that is subtly wrong — non-manifold meshes, inverted normals, off-by-one indexing in a toolpath — and these reach the machines. Verification is the student's obligation, not the tool's.

### Critical Awareness

While generative AI models are not used to produce work in this class, students should be aware of their availability and capabilities in order to develop a critical perspective. The distinction between automated two-dimensional image generation and the discrete techniques used here — building three-dimensional systems, extracting information from them, and compositing images — is itself a subject of the course. Understanding when a tool is appropriate to a task is part of what a designer is expected to know.
## Attendance Policy Statement

Students are expected to attend all their scheduled University classes and to satisfy all academic objectives as outlined by the instructor. The effect of absences upon grades is determined by the instructor, and the University reserves the right to deal at any time with individual cases of non-attendance. Students are responsible for arranging to make up work missed because of legitimate class absence, such as illness, family emergencies, military obligation, court-imposed legal obligations, or participation in University-approved activities. Examples of University-approved reasons for absences include participating on an athletic or scholastic team, musical and theatrical performances, and debate activities. It is the student's responsibility to give the instructor notice prior to any anticipated absences and within a reasonable amount of time after an unanticipated absence, ordinarily by the next scheduled class meeting. Instructors must allow each student who is absent for a University-approved reason the opportunity to make up work missed without any reduction in the student's final course grade as a direct result of such absence.

### Course-Specific Attendance Terms

This course meets **once per week**. A single absence is roughly seven percent of the semester's contact time, and each session contains material that is not repeated.

- Attendance and participation constitute **5% of the final grade.** Each unexcused absence reduces this component by one third; each unexcused late arrival (more than 15 minutes after the start of class) reduces it by one sixth.
- Students absent more than **three** classes without serious documented reason, given in writing in advance where possible, may — at the instructor's judgment — fail the course.
- Students absent from a required pin-up, review, or submission receive an F for that assignment.
- Absence does not extend a deadline. It is the student's responsibility to obtain material covered and to submit work due.

Attendance is recorded through a sign-in link provided at the start of each session. `[CONFIRM whether Google Form or Canvas attendance is used this term]`

### Classroom Etiquette

Personal communication devices should not be used for non-course purposes during class. Devices are permitted for documentation, reference, and coursework. Students not participating in class may be considered absent at the discretion of the instructor.

---

## Policy on Make-up Tests, Late Work, and Incompletes

Absence does not absolve the student from homework, assignments, or work progress due on the day of absence, or work due the following class. In case of absence, it is the student's responsibility to obtain information on material covered and assignments.

**Late work is not accepted.** Missed projects or class activities resulting from an unexcused absence receive a zero.

**Revision.** This course is built on iteration, and revision is handled through a defined mechanism rather than through late submission. Assignment grades are issued at the original deadline and stand. All work may be revised for inclusion in the Final Booklet, where the quality of that revision is assessed as 40% of the Booklet grade. Students who submit nothing at the original deadline have nothing to revise.

Incompletes are granted only under University policy and only where the majority of coursework has been completed.

---

## Project Documentation of Student Work

The School of Architecture reserves the right to retain all student work for the purpose of record, exhibition, and instruction. All students are encouraged to reproduce all work for their own records prior to submission of originals to the instructor. In the event of publication, the author of the work will be recognized and receive full attribution. Upon completion of the final review, all students are required to submit any requested revisions and all digital material from the whole semester through a shared Google Drive, Microsoft Teams, or other online platform specified by the instructor. **Final grades will be withheld until this material is turned in.**

---

## Code of Academic Integrity

Students at Florida Atlantic University are expected to maintain the highest ethical standards. Academic dishonesty is considered a serious breach of these ethical standards, because it interferes with the university mission to provide a high quality education in which no student enjoys an unfair advantage over any other. Academic dishonesty is also destructive of the university community, which is grounded in a system of mutual trust and places high value on personal integrity and individual responsibility. Harsh penalties are associated with academic dishonesty. For more information, see University Regulation 4.001.

---

## Faculty Rights and Responsibilities

Florida Atlantic University respects the rights of instructors to teach and students to learn. Maintenance of these rights requires classroom conditions that do not impede their exercise. To ensure these rights, faculty members have the prerogative to:

- Establish and implement academic standards.
- Establish and enforce reasonable behavior standards in each class.
- Recommend disciplinary action for students whose behavior may be judged as disruptive under the Student Code of Conduct, University Regulation 4.007.

---

## Disability Policy

In compliance with the Americans with Disabilities Act Amendments Act (ADAAA), students who require reasonable accommodations due to a disability to properly execute coursework must register with Student Accessibility Services (SAS) and follow all SAS procedures. SAS has offices across three of FAU's campuses — Boca Raton, Davie and Jupiter — however disability services are available for students on all campuses. For more information, please visit the SAS website at www.fau.edu/sas/.

---

## Religious Accommodation Policy Statement

In accordance with the rules of the Florida Board of Education and Florida law, students have the right to reasonable accommodations from the University in order to observe religious practices and beliefs regarding admissions, registration, class attendance, and the scheduling of examinations and work assignments. University Regulation 2.007, Religious Observances, sets forth this policy for FAU and may be accessed on the FAU website at www.fau.edu/regulations.

Any student who feels aggrieved regarding religious accommodations may present a grievance to the executive director of The Office of Civil Rights and Title IX. Any such grievances will follow Florida Atlantic University's established grievance procedure regarding alleged discrimination.

---

## Time Commitment Per Credit Hour

For traditionally delivered courses, not less than one (1) hour of classroom or direct faculty instruction each week for fifteen (15) weeks per Fall or Spring semester, and a minimum of two (2) hours of out-of-class student work for each credit hour. Equivalent time and effort are required for Summer Semesters, which usually have a shortened timeframe. Fully Online courses, hybrid, shortened, intensive format courses, and other non-traditional modes of delivery will demonstrate equivalent time and effort.

---

## Grade Appeal Process

You may request a review of the final course grade when you believe that one of the following conditions apply:

- There was a computational or recording error in the grading.
- The grading process used non-academic criteria.
- There was a gross violation of the instructor's own grading system.

University Regulation 4.002 contains information on the grade appeals process.

---

## Policy on the Recording of Lectures

Students enrolled in this course may record video or audio of class lectures for their own personal educational use. A class lecture is defined as a formal or methodical oral presentation as part of a university course intended to present information or teach students about a particular subject. Recording class activities other than class lectures, including but not limited to student presentations (whether individually or as part of a group), class discussion (except when incidental to and incorporated within a class lecture), labs, clinical presentations such as patient history, academic exercises involving student participation, test or examination administrations, field trips, and private conversations between students in the class or between a student and the lecturer, is prohibited. Recordings may not be used as a substitute for class participation or class attendance and may not be published or shared without the written consent of the faculty member. Failure to adhere to these requirements may constitute a violation of the University's Student Code of Conduct and/or the Code of Academic Integrity.

---

## Outside Employment

While the University is sensitive to the financial and professional needs of our students, outside employment is not considered an extenuating circumstance in cases of poor performance, excessive absences, or failure to submit assigned work on schedule.

---

## Counseling and Psychological Services (CAPS) Center

Life as a university student can be challenging physically, mentally and emotionally. Students who find stress negatively affecting their ability to achieve academic or personal goals may wish to consider utilizing FAU's Counseling and Psychological Services (CAPS) Center. CAPS provides FAU students a range of services — individual counseling, support meetings, and psychiatric services, to name a few — offered to help improve and maintain emotional well-being. For more information, go to http://www.fau.edu/counseling/

---

## Title IX Statement

In any case involving allegations of sexual misconduct, you are encouraged to report the matter to the University Title IX Coordinator in the Office of Civil Rights and Title IX (OCR9). If University faculty become aware of an allegation of sexual misconduct, they are expected to report it to OCR9. If a report is made, someone from OCR9 and/or Campus Victim Services will contact you to make you aware of available resources including support services, supportive measures, and the University's grievance procedures. More information, including contact information for OCR9, is available at https://www.fau.edu/ocr9/title-ix/. You may also contact Victim Services at victimservices@fau.edu or 561-297-0500 (ask to speak to an Advocate) or schedule an appointment with a counselor at Counseling and Psychological Services (CAPS) by calling 561-297-CAPS.

---

## Student Support Services and Online Resources

- Center for Learning and Student Success (CLASS)
- Counseling and Psychological Services (CAPS)
- FAU Libraries
- Office of Information Technology Helpdesk
- Center for Global Engagement
- Office of Undergraduate Research and Inquiry (OURI)
- Student Accessibility Services
- Student Athlete Success Center (SASC)
- Testing and Certification
- Test Preparation
- University Academic Advising Services

**The Center for Teaching and Learning (CTL)** has a variety of FREE TUTORING and other academic support services to help you succeed in your courses. You are encouraged to build your academic support team early in the term and meet with your team regularly. At the CTL, you can practice difficult course content, develop skills, and learn academic success strategies — in person and online. Learn more at www.fau.edu/ctl.


---

## Teaching Methodologies

Course material is delivered in the sequence of graphic production: **conceptualize → compute → represent → fabricate**. By investigating different methods of design delineation, students address clarity of spatial communication and design intentionality. Students research and analyze graphic representation case studies in order to identify techniques useful for generating design presentations, then apply them in assignments that challenge the tools and workflows currently used to make design decisions.

The primary objective is to use these tools and techniques not only to highlight the qualities of a project, but to explore its conceptual grounds further through the process of drawing, modeling, and making. In light of visualization tools using artificial intelligence and natural language processing, questions of skill-building and craftsmanship remain central: students are expected to develop a sensibility about the advantages and limitations of the various methods available to them.

Tutorials are pre-recorded and watched before class, so that session time goes to troubleshooting, briefing, and critique rather than to demonstration. Because the course meets once per week, students should expect a minimum of six hours of out-of-class work per week, including tutorial time.

---

## Conceptual References

Point, line, and plane are explored through examples from architecture, art, graphic design, computation, and fabrication. Rather than following a single theoretical position, students examine how different designers have used fundamental geometric elements to investigate aggregation, fields, direction, section, surface, material, pattern, filtering, and atmosphere.

### Contemporary Practitioners

A starting set, organized by where each is most useful. These are working practitioners publishing continuously, so treat them as a live feed rather than a fixed bibliography — the point is to see what a high standard looks like right now, not to imitate a specific image.

| Reference | Relevant to | Why |
|---|---|---|
| [@mmnksr](https://www.instagram.com/mmnksr/) | Modules 1–2 | Point clouds and sections — density and depth built from discrete elements |
| [@mantissa.xyz](https://www.instagram.com/mantissa.xyz/) | Modules 1–2 | Point clouds and sections; a different resolution of the same territory, useful read against @mmnksr |
| [@saul_kim_](https://www.instagram.com/saul_kim_/) | All modules | Minimalist visualization — restraint, line weight, and how much can be removed before an image stops reading |
| [@facadepot](https://www.instagram.com/facadepot/) | Module 3 | Modular façades — component logic and variation across a surface |

Two of these cover the same subject deliberately. Comparing how @mmnksr and @mantissa.xyz each resolve a point cloud is more instructive than studying either alone: the technique is shared, the graphic decisions are not, and the difference between them is exactly what this course assesses.

**Module 2 sets these as its standard.** The supplied node groups exist so that this level of image is reachable within the module.

A module-specific reference set is distributed at the start of each module and expands this list.

These references support the assignments while leaving students free to develop their own visual and computational interpretations.

---

## NAAB Student Performance & Program Criteria

The following National Architectural Accreditation Board (NAAB) criteria are satisfied in this course. Definitions can be found at NAAB.org/Conditions.

`[CONFIRM with the School whether the 2014 SPC set below or the 2020 Conditions PC/SC set should be cited for this accreditation cycle.]`

| Criterion | Description | Where Satisfied |
|---|---|---|
| **A.2 Design Thinking Skills** | Ability to raise clear and precise questions, use abstract ideas to interpret information, consider diverse points of view, reach well-reasoned conclusions, and test alternative outcomes against relevant criteria and standards. | Module 4; all module A assignments |
| **A.3 Investigative Skills** | Ability to gather, assess, record, and comparatively evaluate relevant information and performance in order to support conclusions related to a specific project or assignment. | Module 4; module briefings and reference research |
| **A.4 Architectural Design Skills** | Ability to effectively use basic formal, organizational and environmental principles and the capacity of each to inform two- and three-dimensional design. | Modules 1–3, A and B assignments |
| **A.5 Ordering Systems** | Ability to apply the fundamentals of both natural and formal ordering systems and the capacity of each to inform two- and three-dimensional design. | Module 0 (operation sequence); Module 1 (fields, distribution); Module 3 (tessellation, modularity) |
| **A.6 Use of Precedents** | Ability to examine and comprehend the fundamental principles present in relevant precedents and to make informed choices about the incorporation of such principles into architecture and urban design projects. | Conceptual references; Module 4, Stage 1 |
| **PC.5 Research and Innovation** | How the program prepares students to engage and participate in architectural research to test and evaluate innovations in the field. | Module 4; fabrication modules |

---

*Syllabus subject to revision. Any changes will be announced in class and posted to Canvas.*
