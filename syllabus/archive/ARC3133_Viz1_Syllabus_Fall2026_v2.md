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

The course runs in **five modules**, alternating between two ways of working:

| Module | Environment | What is taught |
|---|---|---|
| **0** | Node graph | Parametric modeling: what a parameter is, how nodes connect, transformations, booleans |
| **1** | Python | Computational geometry: the point, arrays, fields, loops, conditionals |
| **2** | Node graph | Section and sequence: bisecting geometry and rebuilding it as slices |
| **3** | Node graph | Modularity and tessellation: vault systems, panel fields |
| **4** | Python + AI | Tool building |

Module 0 puts students inside a node graph before they can read one. Module 1 explains what the graph was doing — a node that scatters points is a loop, a node that varies a value is a remapping function. Modules 2 and 3 return to node graphs with that vocabulary. Module 4 asks students to build a tool of their own.

### Point, Line, Plane

Modules 1, 2, and 3 each take one of the three fundamental spatial elements:

| Module | Element | Computational focus |
|---|---|---|
| 1 | Point | Lists, arrays, and fields |
| 2 | Line | Section and sequence |
| 3 | Plane | Modularity and tessellation |

Each of these modules has two assignments: a **Digital Visualization Assignment** producing a sheet, and a **Physical Fabrication Assignment** producing an object.

Visualization is the primary emphasis. Composition, color, hierarchy, line weight, rendering, diagramming, and post-processing are what the sheets are assessed on. Computational methods are tools for generating new types of images, not ends in themselves.

### On Python

Python is taught directly and in full — variables, data types, lists, indexing, conditionals, loops, functions — and it is the material on which computational understanding is assessed.

It is not the environment you are required to work in. Three of the five modules are node-based, because that is how this work is done in practice and because the visual feedback is immediate. Python is where you learn what those graphs do underneath.

| Environment | Type | Used in |
|---|---|---|
| Blender Geometry Nodes | Visual programming | Modules 0, 2, 3 |
| Grasshopper | Visual programming | Modules 0, 2, 3 |
| Blender Python | Scripting | Modules 1, 4 |
| Grasshopper Python | Scripting | Modules 1, 4 |

Choose Blender or Rhino in Week 1 and stay there. Every tutorial ships in both.

Digital fabrication complements the visualization curriculum through three modes of computer-controlled making: **drawing**, **cutting**, and **additive manufacturing**.

---

## Course Structure

| Module | Concept | Environment | Fabrication | Physical output |
|---|---|---|---|---|
| 0 | Foundations | Node graph | Additive (introductory) | Small print |
| 1 | POINT | Python | Computer-controlled motion | Drawing |
| 2 | LINE | Node graph | Computer-controlled cutting | Sectional assembly |
| 3 | PLANE | Node graph | Additive manufacturing | Vault or façade fragment |
| 4 | TOOL | Python + AI | — | The tool |

Each module's fabrication process matches its computational subject. A toolpath is an ordered list, so the plotter belongs to the module that teaches lists. Sections are flat parts, so the laser belongs to the module that teaches iteration. Panels are a batch, so multi-part printing belongs to the module that teaches grids.

Module 0's print sits before this progression rather than inside it — one solid, one orientation, so that Module 3 can address additive fabrication at the scale of an assembly.

---

## Software and Materials

### Required Software

| Purpose | Environment | Notes |
|---|---|---|
| Application environment | Blender (Geometry Nodes + Python) | Free and cross-platform. Recommended for students without a Rhino license. |
| Application environment | Rhino + Grasshopper (incl. Grasshopper Python) | Student license |
| Language taught and assessed | Python 3.x | Written inside Blender or Rhino; no separate install required |
| Layout and post-processing | Adobe Illustrator, Photoshop, InDesign | Student license. Open-source equivalents accepted: Inkscape, GIMP, Scribus |
| Slicing | PrusaSlicer, Cura, or FabLab-specified slicer | Per FabLab standard |
| Plotter / cutting preparation | As specified by the FabLab | Introduced in Weeks 6 and 10 |

**Template-based design tools are not permitted.** Canva, Adobe Express, Figma templates, PowerPoint, Google Slides, Wix, and similar applications may not be used to produce any sheet, the Visual Identity Manual, or the Booklet. A template supplies the grid, the type hierarchy, the palette, and the spacing — the exact set of decisions Assignment 0.2 asks you to make yourself.

Work in a vector or raster editor: Illustrator, Photoshop, InDesign, Inkscape, GIMP, Scribus, or Affinity.

### Materials

Consumable materials are **supplied by the School**, subject to the limits below.

| Module | Supplied | Per-student allocation |
|---|---|---|
| 0 — First print | Filament | One print, 200 g |
| 1 — Plotter drawing | Paper and pens | 3 sheets, 1 pen |
| 2 — Laser cutting | Chipboard, basswood, or acrylic | 1 sheet |
| 3 — 3D printing | Filament | `[CONFIRM — FabLab supplied or student purchase]` |
| 4 — Tool | — | No physical output |

Allocations are fixed. Test cuts and failed prints count against them, so plan them deliberately. Students who exceed the allocation are responsible for replacement material.

Students supply their own storage media and are responsible for their own file backups.
### Fabrication Scope Limits

To ensure the whole cohort can complete fabrication within FabLab capacity, the following limits apply and are part of each assignment's requirements:

- **Assignment 0.1 (first print):** maximum bounding box 60 mm; draft layer height; **no supports permitted** — orientation is the only lever, and the choice must be documented
- **Assignment 1B:** maximum drawing size tabloid; maximum plot time per student 20 minutes
- **Assignment 2B:** maximum assembled bounding box 300 mm; maximum sheet count 1
- **Assignment 3B:** maximum assembled volume 300 mm; maximum print time per student `[TBD]`

Work exceeding these limits will not be scheduled on the machines.

---

## FABLAB Usage Protocols

For all new FAU School of Architecture students, the **FabLab Safety Orientation must be completed to gain access to any part of the FabLab.** Enroll through:

`https://canvas.fau.edu/enroll/JEW9J6` — `[CONFIRM link is current for this term]`

**Completion is due by the end of Week 2 (Sep 1).** Students who have not completed the orientation cannot begin Assignment 1B and remain responsible for the assignment deadline.

---

## Required Texts / Materials

**No required textbook.** Course material is delivered through in-class demonstration, distributed code, and documentation. `[DECIDE — Woodbury was previously the required text; it is Grasshopper-centered and now sits below as recommended. Confirm with the bookstore if a required text must be listed.]`

Students should bookmark the official Python documentation, the Blender Python API reference, and the Rhino/Grasshopper developer documentation, which are referenced throughout the semester.

## Recommended Readings and Materials

- **Point and Line to Plane** — Wassily Kandinsky (Dover) — foundational to the course's conceptual structure
- **Elements of Parametric Design** — Robert Woodbury · Routledge, 2010 · ISBN 978-0415779876
- **AAD Algorithms-Aided Design: Parametric Strategies using Grasshopper** — Arturo Tedeschi · Le Penseur · ISBN 978-8895315300
- **Advanced 3D Printing with Grasshopper®: Clay and FDM** — Diego García Cuevas and Gianluca Pugliese · Independently published, 2020 · ISBN 9798635379011 — *primary reference for Module 3B; also relevant to Module 1B*
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
| 1 | Produce architectural graphics of professional visual quality using computational methods | 1A, 2A, 3A, Booklet |
| 2 | Build and modify a parametric graph — connect nodes, expose inputs, change an upstream parameter and predict the downstream result | 0.1, 2A, 3A |
| 3 | Construct and modify solid geometry through Boolean operations and transformations, non-destructively | 0.1, 3B |
| 4 | Write Python applying variables, data types, lists, indices, conditionals, loops, and functions to generate and manipulate geometry | 1A, 1B, Module 4 |
| 5 | Read a node graph and state what it is doing in computational terms — which operation repeats, over what collection, producing what | 2A, 3A |
| 6 | Reimplement a system built in one environment in the other | 1A → 2A handoff; Module 4 |
| 7 | Generate and control point fields, sections, patterns, and differentiated surfaces | 1A, 2A, 3A |
| 8 | Decompose a geometric problem into an explicit sequence of steps, expressed as pseudocode | Module 4; all modules |
| 9 | Prepare geometry correctly for computer-controlled drawing, cutting, and additive manufacturing | 1B, 2B, 3B |
| 10 | Evaluate and account for material and machine constraints — ordering, kerf, tolerance, manifold geometry, orientation | 1B, 2B, 3B |
| 11 | Assemble a fabricated system from computationally generated components | 2B, 3B |
| 12 | Plan a multi-part fabrication run against machine, time, and material constraints | 3B |
| 13 | Analyze point, line, and plane as simultaneously graphic, spatial, and computational systems | Modules 1–3 |
| 14 | Develop and consistently apply a personal visual identity across a body of work | 0.2, Booklet |
| 15 | Communicate computational and fabrication processes through diagrams, documentation photography, and annotation | All B assignments, Booklet |
| 16 | Independently learn an unfamiliar computational workflow, extract its logic, and rebuild it as a reusable tool | Module 4 |

Outcomes 5 and 6 are the ones the course is organized around. Outcome 6 is assessed at a specific point: in 2A, where students rebuild a Module 1 Python system as a node graph.
## Module 0 — Foundations
### Focus: Parametric Modeling

Module 0 introduces parametric, non-destructive modeling and the node interface.

**What is taught:**

- **Non-destructive modeling** — the difference between a model you have edited and a model that describes how it was made. Changing an early decision without rebuilding what follows.
- **What a parameter is** — a named value the definition depends on. Where parameters live, how to expose them, and why a number typed into a node is not the same as a number wired into it.
- **The interface** — the Geometry Nodes editor and the Grasshopper canvas. Adding a node, connecting one, reading what a wire carries.
- **Inputs and outputs** — every node takes something and returns something. Matching types. What happens when the wrong thing is plugged into the wrong socket.
- **Transformations** — translate, rotate, scale, applied as parameters rather than by hand.
- **Boolean operations** — union, difference, intersection, used to build new solids from primitives. The result stays parametric: change a primitive and the boolean updates.

Students are not expected to understand why the graph works. Module 1 covers that.

**Environment:** Blender Geometry Nodes or Grasshopper. Choose one and stay in it.

**Concepts:** Parameter · Node · Input and output · Wire · Data type · Non-destructive construction · Order of operations · Primitive solids · Translate, rotate, scale · Boolean union, difference, intersection

### Assignment 0.1 — Parametric Massing Sequence

Form developed as an ordered sequence of geometric operations, each responding to an architectural rationale — program, orientation, circulation, views — built as a graph rather than modeled by hand.

**Concepts:** Primitive solids · Translation · Rotation · Scale · Boolean union, difference, intersection · Parametric graphs · Manifold geometry · Print orientation · Supports · Layer height · Slicing · Axonometric and isometric representation · Exporting 3D geometry to 2D linework · Post-processing

**Requirements**

- 5+ Boolean operations
- 4+ distinct primitive types
- 2+ translations, 1+ rotation
- The graph is part of the submission. It must be intact, and you must be able to change any upstream parameter on request and have the result update
- All primitives generated in-session; no imported models
- An annotated screenshot of the graph on the sheet

**Assessed on** legibility of the operation sequence, quality of the axonometric set, and graphic execution of the final isometric.

**Deliverable:** One 17" × 11" sheet — one axonometric per operation, one larger final isometric with human scale, vegetation, context, shadows, and annotation, and the annotated graph. This sheet sets the documentation standard for the rest of the course. **Due Week 3 — Sep 8 · 8%**

**First print — required.** The result is 3D printed at small scale and presented at the Week 8 Midterm Review.

Three things are learned here, all of which return at system scale in 3B:

- **Manifold geometry.** A Boolean that leaves an open edge or a self-intersection looks correct on screen and fails in the slicer. Node-based Booleans produce these readily.
- **Orientation.** The same solid prints differently depending on how it sits on the bed — surface quality, strength, and time all change.
- **Supports, by their absence.** **No supports are permitted on this print.** Banning them leaves orientation as your only lever. Supports become available in 3B, once you know what you are buying with them.

**Additional requirements**

- An orientation diagram on the sheet showing your chosen orientation, the overhangs it produces, and why you chose it over an alternative
- If the geometry cannot print unsupported in any orientation, revise the geometry — that is an expected outcome

Craft and finish are not assessed here; those belong to 3B. **No credit is issued for 0.1 without the print.**

Printer queue opens Week 3. Print within the scope limit above.

### Assignment 0.2 — Visual Identity Manual for Architects

A personal graphic system applied to every subsequent assignment. Drawings, diagrams, renders, captions, typography, and page layouts should work together rather than as separate decisions.

**Standards to define:** Personal logo · Color palette · Typography · Font hierarchy and sizing · Line weights · Captions · Image labels · Graphic hierarchy · Margins · Grid systems · 17" × 11" tabloid sheet template · Booklet cover

**Requirements**

- 8+ pages
- No more than 3 typefaces, with a hierarchy of 4+ levels
- 5+ color palette with stated values and written rationale
- 4+ defined line weights, each with an assigned use
- One tabloid template with the grid shown explicitly
- Built in a vector or layout editor, not a template-based tool

**This is a provisional system.** It is designed before you have content to test it against and is expected to change. A mandatory revision is submitted with the Final Booklet and assessed there.

**Deliverable:** Separate PDF. **Due Week 4 — Sep 15 · 8%**
---

## Module 1 — POINT
### Focus: Computational Geometry

Module 1 teaches the principles of computational geometry, starting from a single point and building up. It is the module that explains what the graphs in Modules 0, 2, and 3 are doing.

**What is taught:**

- **How a point is built** — a vertex is three numbers in order. Variables, data types, coordinates.
- **Multiple points** — the list. Storing a collection, reaching into it by index, adding to it.
- **The for loop** — how a collection gets made without writing each item. Nested loops, and how loop order determines the order of everything downstream.
- **The if statement** — testing a value and acting on the result. Filtering a collection.
- **Arrays** — rectangular, radial, hexagonal, along a curve. Organizing points into structure.
- **Fields** — measuring distance, remapping a measurement into a useful range, applying falloff. Single-point, multiple-point, and curve attractors.
- **Generating geometry from points** — turning a collection of positions into vertices, edges, and instanced objects.
- **Organizing geometry** — indices, parallel lists, attributes stored on the mesh itself.

**Environment:** Blender Python or Grasshopper Python. Each tutorial script is also supplied as a Sverchok / SNLite node, so the identical logic can be watched running in a graph.

**Visualization concepts:** Point · Coordinate · Point cloud · Field · Distribution · Density · Gradient · Scale · Proximity · Composition

**Computational concepts:** Variables · Data types · Coordinates · Lists · Indexing · For loops · Nested loops · If statements · Functions · Randomization · Distance · Remapping · Falloff

Arrays are taught as systems for generating and organizing points, not as commands for duplicating geometry.

### Assignment 1A — POINT: Arrays + Attractors

An array organizes points; an attractor differentiates them. This assignment combines the two — different array types driven by different attractor types, so that the same structure yields different fields depending on what varies across it.

**Requirements**

- 3+ distinct array/attractor combinations, covering the array types from Tutorial 1.1 (rectangular, radial, hexagonal, along a curve) and all three attractor types (single-point, multiple-point, curve)
- 3+ distinct parameters driven by attractor distance across the set — scale, rotation, density, height, color
- 1+ explicit remapping operation, with its input and output ranges stated on the sheet
- 1+ composition containing 1,000 or more elements; 1+ resolved spatially in 3D
- For one combination: **three views of the same system** — isometric, close-up, eye-level perspective
- Minimum 2 sheets
- Arrays and falloff authored in Python. Array add-ons, scatter tools, and preset falloff plugins prohibited

**Assessed on** composition, density, rhythm, contrast, hierarchy, gradient, scale, depth, and color — and on whether the set reads as a systematic exploration rather than four unrelated images.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 6 — Sep 29 · 8%**

### Assignment 1B — POINT: Toolpath Drawing
**Fabrication: Computer-Controlled Motion**

Pick one system from 1A and draw it physically, using a pen plotter or robotic arm. Geometry must become an ordered sequence before a machine can execute it. Points and lists define motion, and the ordering of the data determines the mark.

**Topics:** Lists · Indices · Point ordering · Toolpaths · Travel moves · Drawing moves · Pen up / pen down · Coordinate systems · Machine motion · Machine constraints

**Conceptual workflow:** Point → Sequence → Toolpath → Motion → Mark

**Requirements**

- The drawing order is authored — swapping the loop nesting must visibly change the result, and you must be able to demonstrate that
- Travel moves identified and minimized, with the strategy stated (serpentine ordering, or an alternative you can defend)
- A toolpath diagram distinguishing draw moves from travel moves

**Assessed on** correctness of the toolpath logic, craft of the physical drawing, and clarity of documentation.

**Deliverable:** Drawing within the stated scope limits, plus photographic documentation and a toolpath diagram. **Due Week 8 — Oct 13, with the Midterm · 8%**
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

### Assignment 2A — LINE: Section + Light

A composition built from a sectioned system, in which **material, light, and filtering** are the primary graphic subject. What does a stack of slices do to light passing through it — what is revealed, what is occluded, what reads as depth.

Section is explored beyond the conventional section drawing: serial, overlapping, directional, data-driven. The result may be abstract, spatial, analytical, architectural, or representational.

**Requirements**

- 1+ system generated from 20 or more serial sections
- 2+ distinct section directions
- 1+ rendered image with controlled lighting, demonstrating what the section stack does to light
- 2+ distinct materials, with their optical behavior (transparency, translucency, reflectivity) doing visible work
- 1+ conditional filter that removes or modifies a subset of profiles based on a tested property
- **One system from Module 1, rebuilt here as a node graph** — your Python array or attractor, reimplemented, with a short side-by-side diagram of the two on the sheet
- You must be able to explain every supplied group you used

**Assessed on** material and light, depth, transparency, figure/ground, density, contrast — and on the Module 1 reimplementation, which is where Outcome 6 is assessed.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 10 — Oct 27 · 8%**

### Assignment 2B — LINE: Section-Based Fabrication
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

**Deliverable:** Laser-cut sectional assembly within the stated scope limits, plus photographic documentation, an exploded assembly diagram, and the nesting layout. **Due Week 11 — Nov 3 · 8%**

---

## Module 3 — PLANE
### Focus: Modularity and Tessellation

Module 3 builds the most complex definitions of the course: a vault or façade system, tessellated into panels, with variation authored across the field.

**What is taught:**

- **Tessellation** — dividing a surface into cells. Quad, triangular, and hexagonal subdivisions, and what each does to a curved surface.
- **Modularity** — designing one component and mapping it onto every cell. Why a component that reads cleanly on a plane will not necessarily close on a curve.
- **Grids as two-dimensional data** — a grid is a list of lists. UV coordinates, and mapping a component into a cell's local space.
- **Vault systems** — curvature, panel distortion, and the structural logic of a doubly curved assembly.
- **Variation across a field** — driving panel parameters from the attractor and remapping logic built in Module 1, now applied to a component rather than a point.

Definitions here are longer and more nested than anything in Modules 0 or 2. Where a node graph becomes unwieldy, scripting is permitted and sometimes faster.

**Environment:** Blender Geometry Nodes or Grasshopper; Python where a definition is easier written than wired.

**Visualization concepts:** Plane · Surface · Curvature · Vault · Pattern · Filter · Layer · Panel · Aperture · Porosity · Relief · Tessellation

**Computational concepts:** Nested loops · Grids · Two-dimensional data structures · UV coordinates · Data mapping · Remapping · Conditional variation

**Panelization tools are permitted in this module.**

| Environment | Tools |
|---|---|
| Blender | **Tissue** (Zomparelli) — Tessellate maps a component object onto the faces of a base mesh; also Dual Mesh and weight/color exchange |
| Grasshopper — native | **Surface Box + Box Morph** — the structural equivalent of Tessellate, no plugin required. Start here. |
| Grasshopper — plugins | **Paneling Tools** (Issa, McNeel) · **Pufferfish** (Pryor) · **LunchBox** · **Weaverbird** |

The tool may generate the tessellation. **The differentiation across it must be yours** — your parameters, your mapping, your remapping ranges. A field of identical panels produced by a plugin does not answer this assignment.

### Assignment 3A — PLANE: Surface + Filtering

A computational graphic exploring the plane as a variable surface or filter. Rendering, lighting, shadow, and materiality carry the image.

**3A and 3B describe the same system.** The graphic shows the surface whole; the print realizes a 3 × 3 fragment. Choose a vault or a façade here and develop it in both.

**Requirements**

- A field of 400+ cells or panels (minimum 20 × 20)
- 2+ independent parameters driving the variation
- 1+ explicit remapping operation, with input and output ranges documented on the sheet
- **Three views of the same system:** overall, close-up detail, and eye-level or oblique
- 1+ rendered image with controlled lighting demonstrating the filtering behavior
- Panelization and tessellation tools are permitted; the variation driving them must be authored

**Assessed on** surface, figure/ground, pattern, repetition, variation, transparency, depth, shadow, and material appearance.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 13 — Nov 17 · 8%**

### Assignment 3B — PLANE: Additive Fabrication
**Fabrication: 3D Printing**

The surface system from 3A, fabricated as an architectural element — **either a vaulted structure or a façade fragment**, panelized into physical components that connect to one another.

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

**Deliverable:** 3D-printed vault or façade fragment of 9+ panels within the stated scope limits, plus photographic documentation and a slicing/orientation diagram. **Due at the Final Review, Dec 10–16 · 8%**

> **Print queue:** Files must be submitted to the FabLab queue by the end of Week 13 (Nov 17). Prints submitted later are not guaranteed to complete before the deadline, and queue congestion is not grounds for an extension. The object is presented at the Week 15 final review; its documentation may be added to the Booklet within 48 hours of the review.
---

## Module 4 — TOOL
### Focus: AI-Assisted Tool Building

Module 4 returns to code and asks for an instrument rather than an image. Three stages: **study** an existing workflow, **extract** its logic, **build** your own tool from it.

A result is one image. A tool takes inputs and produces a family of outputs — it is reusable, and someone else could run it. This assignment asks for the second.

Coding assistance is a taught subject here. Language models write Python fluently and are unreliable in geometry APIs. The skill assessed is not writing code but reading it and catching where it is wrong.

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

> Module 1 ends in Week 8 and Module 4 begins in Week 12 — four weeks without writing code. Module 4 is AI-assisted partly for this reason: it asks you to read code critically, which fades more slowly than syntax recall. Each Module 2 and 3 tutorial opens with the Python equivalent of whatever node group it uses.

---

## Midterm Review — Week 8, Oct 13

Students **print and present all work completed to date**, in its latest revised form, using their visual identity:

- 0.1 Parametric Massing Sequence — sheet **and verification print**
- 0.2 Visual Identity Manual
- 1A POINT: Arrays + Attractors
- 1B POINT: Toolpath Drawing (with documentation)

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
| All sheets, 0.2, Booklet | Canva, Adobe Express, template-driven layout apps, PowerPoint, Google Slides | Vector or raster editors |
| 0.1 | Imported or downloaded models; any geometry not generated in-session | Any node-based boolean and transform operations |
| 1A / 1B | Array add-ons, scatter and distribution tools, preset attractor falloff plugins. Arrays, distance, falloff, and remapping must be written | Nothing that automates the loop |
| 2A / 2B | Nothing prohibited | Supplied section, SDF, and contour groups, subject to the explanation requirement |
| 3A / 3B | Preset gradient, attractor, and variation components — the differentiation must be authored | Panelization and tessellation libraries |
| Module 4 | Nothing prohibited | Everything, including coding assistance under the Stage 2 AI terms |
| All Grasshopper work | The Cross Reference component may be used **once** per definition | |

### The explanation requirement

From Module 2 onward, using a supplied or third-party group carries one condition: **you must be able to state what it does in the vocabulary taught in Module 1** — which operation repeats, over what collection, producing what output.

A student who cannot do that for a group they used receives **no credit for Computational Understanding** on that assignment, regardless of how the image looks. This is tested at pin-up alongside live modification and takes about thirty seconds.

Module 1 is where the vocabulary is installed; Modules 2 and 3 are where it buys you something.

Use of a prohibited tool is assessed as a failure to meet Assignment Requirements for that submission.
---

## Final Submission — Booklet + Visual Identity Manual

Two separate PDF files, due at the Final Review (Dec 10–16).

### 1. Final Booklet — **Weight: 10%**

The Final Booklet contains all course assignments in their latest revised form. Students are expected to incorporate feedback received throughout the semester rather than resubmit original work.

Contents: Parametric Massing Sequence · POINT — Arrays + Attractors · POINT — Toolpath Drawing · LINE — Section + Light · LINE — Section-Based Fabrication · PLANE — Surface + Filtering · PLANE — Additive Fabrication · TOOL — Reverse-Engineer a Workflow, Build a Tool (both sheets)

Physical assignments must be documented through high-quality photography, diagrams, and captions. All pages use the student's visual identity at 17" × 11" tabloid size.

**How the Booklet is graded.** The Booklet grade does **not** revise the grades already earned on individual assignments. Those stand. The Booklet's 10% assesses three things that only the Booklet can assess:

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
| 0.1 — Parametric Massing Sequence | 0 | 8% |
| 0.2 — Visual Identity Manual | 0 | 8% |
| 1A — POINT: Arrays + Attractors | 1 | 8% |
| 1B — POINT: Toolpath Drawing | 1 | 8% |
| 2A — LINE: Section + Light | 2 | 8% |
| 2B — LINE: Section-Based Fabrication | 2 | 8% |
| 3A — PLANE: Surface + Filtering | 3 | 8% |
| 3B — PLANE: Additive Fabrication | 3 | 8% |
| **Midterm Review (Oct 13)** | — | 8% |
| 4 — TOOL: Reverse-Engineer a Workflow, Build a Tool | 4 | 13% |
| Final Booklet | — | 10% |
| Attendance and participation | — | 5% |
| **Total** | | **100%** |

Every module assignment carries equal weight. The Midterm and the Final Booklet are the only items that assess the body of work rather than a single submission, and neither re-grades work already assessed.

### Evaluation Criteria

Each assignment is assessed against the following criteria. Percentages indicate the share of that assignment's grade.

| Criterion | Digital assignments (0.1, 0.2, 1A, 2A, 3A, Module 4) | Fabrication assignments (1B, 2B, 3B) |
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

Each session follows the same structure:

1. **Before class — watch the tutorial.** Every tutorial is pre-recorded and released the week before. You are expected to have worked through it before the session.
2. **Questions and troubleshooting.** The first part of class is spent on what did not work — errors, unexpected results, things that behaved differently on your machine. Bring the file, not just the description.
3. **Assignment briefing.** The current assignment is explained, with examples and the specific requirements walked through.
4. **Supervised work time and critique.**

This format only works if the tutorial is done beforehand. A session spent watching what you could have watched at home is a session not spent on your actual problem.

**Every tutorial ships in two versions.** For the node modules (0, 2, 3): Grasshopper and Blender Geometry Nodes. For the code modules (1, 4): Blender Python and Grasshopper Python, with each Module 1 script also supplied as a Sverchok / SNLite node.

Watch the version for your environment. Skim the other at least once per module.

---

## Tutorial Calendar

| # | Tutorial | Released | Environment | Covers |
|---|---|---|---|---|
| **0.1** | Parametric Modeling — interface and parameters | Week 1 | Nodes | The node editor. Adding and connecting nodes, inputs and outputs, data types. What a parameter is. Translate, rotate, scale as parameters |
| **0.2** | Booleans in the Graph | Week 2 | Nodes | Union, difference, intersection used to build new solids from primitives, non-destructively |
| **0.3** | 3D Printing Basics | Week 3 | — | Manifold checking, orientation, supports, layer height, slicing, sending a file to the queue |
| **1.0** | Python I — the point | Week 3 | Python | How a point is built: three numbers. Lists, indexing, the for loop, the if statement |
| **1.1** | Arrays | Week 4 | Python | Rectangular · radial · hexagonal · along a curve. Nested loops, and how loop order becomes drawing order |
| **1.2** | Fields and Attractors | Week 5 | Python | Measuring distance, `remap()`, falloff; single-point, multiple-point, and curve attractors |
| **1.3** | Generating and Ordering Geometry | Week 6 | Python | Turning a point field into vertices, edges, and instanced objects. Ordering, serpentine paths, travel vs. drawing moves, running the plotter |
| **2.1** | Sectioning and Sequence | Week 9 | Nodes | Bisecting geometry with section planes; ordering the slices; the supplied SDF and contour groups, and what they do |
| **2.2** | 2D Fabrication | Week 10 | Nodes | Slots and registration, kerf and tolerance, nesting, labeling, alternative connection strategies |
| **3.1** | Tessellation + Modularity | Week 12 | Nodes | Surface Box / Box Morph and Tissue Tessellate; UV domains, component morphing, panel distortion on a curved surface |
| **3.2** | Fabrication Strategies | Week 13 | Nodes | Panel connections, wall thickness, print orientation for a set, batching and production planning |
| **4.1** | Tool Building with AI Assistance | Week 12 | Python | Pseudocode to code; prompting for geometry work; verifying and correcting generated output; exposing named inputs so a script becomes a tool |

Tutorial 4.1 is released early, alongside the Module 4 brief, so that you can begin it while Module 3 is still running.

---

## Course Topical Outline — 15-Week Schedule

Class meets Tuesdays, 5:00–7:50 PM. Dates below follow the School of Architecture calendar; three School-wide windows constrain this schedule and are marked in the table.

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

| Wk | Date | Module | Content | Due |
|---|---|---|---|---|
| | | | **Weeks 1–7: AI-free. Coding assistance permitted from Week 8 onward, with disclosure.** | |
| 1 | Aug 25 | **0** | Course introduction. Point/Line/Plane framework. **Tutorial 0.1.** The node interface, inputs and outputs, what a parameter is, transformations as parameters. Visual identity brief issued. | FabLab Safety Orientation enrollment |
| 2 | Sep 1 | **0** | **Tutorial 0.2.** Booleans in the graph; new solids from primitives; massing sequence logic; axonometric and isometric representation; exporting 3D geometry to 2D linework; post-processing. | FabLab Safety Orientation **completed** |
| 3 | Sep 8 | **0 → 1** | **Tutorials 0.3 + 1.0.** **Module 1 opens.** Python I — how a point is built; lists, indexing, the for loop, the if statement. **Printer queue opens.** | **0.1 — Parametric Massing Sequence** (sheet) |
| 4 | Sep 15 | **1** | **Tutorial 1.1.** Arrays: rectangular, radial, hexagonal, along a curve. Nested loops; loop order as drawing order. | **0.2 — Visual Identity Manual** |
| 5 | Sep 22 | **1** | **Tutorial 1.2.** Fields: distance, `remap()`, falloff. Single, multiple, and curve attractors. **Same system built twice** — once scripted, once as a node graph. | — |
| 6 | Sep 29 | **1** | **Tutorial 1.3.** 1A pin-up and critique. 1B briefing: toolpaths, ordering, machine constraints. Plotter demonstration. | **1A — Arrays + Attractors** |
| 7 | Oct 6 | **1** | Plotter production session. *Midterm Studio Reviews week — no submissions due.* | — |
| 8 | Oct 13 | **1 → 2** | **MIDTERM REVIEW** — printed set presented; **live modification begins.** **Module 2 opens** in the second half. Supplied groups distributed. | **1B — Toolpath Drawing** · **Midterm submission** |
| 9 | Oct 20 | **2** | **Tutorial 2.1.** Sectioning and sequence: serial sections, contours, slice ordering. Materials and light through a section stack. Reading the supplied groups. *Midterm grades posted.* | — |
| 10 | Oct 27 | **2** | **Tutorial 2.2.** 2A pin-up and critique **with live modification and group explanation.** 2B briefing: section strategies, registration, material thickness, kerf, tolerance, nesting, labeling. | **2A — Section + Light** |
| 11 | Nov 3 | **2** | Laser production session. Assembly workshop. | **2B — Section-Based Fabrication** |
| 12 | Nov 10 | **3 + 4** | **Tutorials 3.1 + 4.1.** **Module 3 opens.** Grids as two-dimensional data. Tessellation, modularity, vault systems. **Module 4 released.** Booklet progress check (ungraded). | — |
| 13 | Nov 17 | **3** | **Tutorial 3.2.** 3A pin-up and critique **with live modification.** Rendering, lighting, post-processing. 3B technical briefing: manifold geometry, thickness, orientation, slicing, production planning and batching. **Print queue closes end of week.** | **3A — Surface + Filtering** · **3B production plan** |
| 14 | Nov 24 | **3 + 4** | Print production. Final desk crits. Booklet layout workshop. *Thanksgiving break follows.* | **Module 4 proposal** |
| 15 | Dec 1 | **3 + 4** | Last regular session. Final desk crits, booklet review, print troubleshooting. *Final Studio Reviews week — no submissions due.* | — |
| — | Dec 10–16 | — | **FINAL REVIEW** — scheduled exam date and time `[CONFIRM against the University exam schedule]` | **3B print · Module 4: 2 sheets + tool file · Final Booklet PDF · Visual Identity Manual PDF** |

**Four constraints shaped this schedule.** Week 7 falls in Midterm Studio Reviews, so 1B moves to the Week 8 midterm rather than being due during that window — the plotter session still runs, only the deadline shifts. Week 15 falls in Final Studio Reviews, so it is a working session with nothing due, and the final submission moves to the University exam period. Midterm grades are due Oct 20, one week after the Midterm Review on Oct 13, which is workable but leaves no slack. The Oct 30 "W" deadline falls after grades post, so students receive a standing before the drop decision.

**Module 1 is compressed into Weeks 3–8** and everything else depends on it. If the cohort is behind in Week 5, borrow time from Module 2 — it has supplied groups to fall back on and Module 1 does not.
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

Module 4 asks you to build a tool with an assistant. That is only meaningful if you can audit what the assistant hands you, and Module 1 is where that ability is built.

### Stage 1 — Weeks 1 through 7: AI-free

No AI assistance of any kind in producing coursework through the Week 8 Midterm. This covers **all of Module 0 and all of Module 1** — 0.1, 0.2, 1A, and 1B.

Permitted throughout, at any stage: asking an AI to explain a computational concept, clarify syntax, or interpret an error message. Not permitted: asking it to write, complete, or fix your code.

This period exists so that variables, lists, indices, loops, conditionals, and functions are installed as your own working vocabulary. 1B depends on it: the lesson is that data ordering determines what the machine draws, and it is learned by getting the ordering wrong and working out why.

### Stage 2 — Week 8 onward: coding assistance permitted, with disclosure

From Module 2 forward, AI may be used to generate, debug, refactor, or explain **code**, subject to:

- **Pseudocode first.** Your own written decomposition of the problem must precede any code generation, and is submitted alongside it. AI-generated pseudocode submitted as your own procedural reasoning is a violation.
- **Full disclosure.** Tool and version, the prompts used, what was kept, and what was changed. Citation follows https://fau.edu/ai/citation.
- **Live modification and group explanation** (see below).

### Not permitted at any stage

- **Generative image models** — Midjourney, Stable Diffusion, DALL·E, Firefly, or any diffusion-based tool — to produce, extend, or modify any image submitted as coursework. This includes backgrounds, textures, entourage, generative fill, and AI upscaling.
- AI generation of the visual identity system, including logo, palette, and layout.

The reason is specific rather than reflexive: in 1A, 2A, and 3A the assessed outcome *is the image*. Delegating its production removes the exact judgment the assignment exists to develop. In the computational work, the assessed outcome is procedural understanding, and an assistant does not remove that — provided you can account for what the code does.

### Live Modification

At every pin-up and review from Week 8 onward, each student will be asked to make **one unscripted change to their own work in front of the class** — reverse a section order, alter an attractor's falloff, add a conditional, change a mapping range. Roughly ninety seconds per student.

This, rather than a written explanation, is the primary assessment of Computational Understanding. It applies equally to scripted and node-based work, and equally whether or not AI was used.

From Module 2 onward it is paired with a second, shorter question: **name a group in your definition and say what it does** — which operation repeats, over what collection, producing what. About thirty seconds. Supplied groups are fair game, and so is anything you downloaded.

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
