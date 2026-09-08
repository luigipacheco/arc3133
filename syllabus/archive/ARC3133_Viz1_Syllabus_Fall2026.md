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

The course is structured around three fundamental spatial and representational elements — **Point**, **Line**, and **Plane** — each paired with a specific computational focus:

| Module | Element | What is taught |
|---|---|---|
| 1 | Point | **Lists, arrays, and fields** — generating, storing, and differentiating collections |
| 2 | Line | **Section and sequence** — cutting continuous geometry into ordered parts |
| 3 | Plane | **Modularity and tessellation** — one component, varied across a surface |

The elements give the course its conceptual armature; the computational focus is what is taught and assessed.

Each module approaches one element through two complementary assignments:

- A **Digital Visualization Assignment**, focused on computational graphics and the production of compelling images.
- A **Physical Fabrication Assignment**, focused on translating computational logic into material processes.

Visualization remains the primary emphasis. Students explore composition, color, hierarchy, line weight, rendering, diagramming, and post-processing. Computational methods are used as tools for generating new types of images rather than as ends in themselves.

**Python is the primary tool taught in this course.** Because Python is relatively human-readable, it provides a way to break a problem into a sequence of understandable operations. Students are taught variables, data types, lists, indexing, conditionals, loops, and functions directly, and this is the material on which computational understanding is assessed.

Students are then free to apply that knowledge in any of four environments:

| Environment | Type |
|---|---|
| **Blender Python** | Scripting |
| **Grasshopper Python** | Scripting |
| **Blender Geometry Nodes** | Visual programming |
| **Grasshopper** | Visual programming |

The same computational logic underlies all four. Students may work in whichever they prefer, may change environments between modules, and are encouraged to implement at least one system twice — once as script, once as a node graph — to see that the logic, not the interface, is the transferable thing.

This is what "tool-agnostic" means here in practice: one language learned properly, then applied wherever it is useful. It does not mean sampling four platforms and mastering none.

Digital fabrication complements the visualization curriculum through three modes of computer-controlled making: **drawing**, **cutting**, and **additive manufacturing**.

Architectural examples provide context and inspiration, but the emphasis is on visual communication, computational thinking, experimentation, technical execution, and fabrication.

---

## Course Structure

| Module | Concept | Focus | Fabrication Process | Physical Output |
|---|---|---|---|---|
| 0 | Foundations | Solid modeling, transformations, CSG; graphic systems and presentation standards | Additive (introductory) | Small print |
| 1 | POINT | **Lists, arrays, and fields** — organizing and differentiating collections | Computer-controlled motion | Drawing |
| 2 | LINE | **Section and sequence** — slicing continuous geometry into ordered parts | Computer-controlled cutting | Sectional assembly |
| 3 | PLANE | **Modularity and tessellation** — one component, varied across a surface | Additive manufacturing | 3D-printed vault or façade fragment |
| Final | — | Independent procedural exploration | — | — |

The progression introduces three fundamental relationships between computation and making:

1. **Data becomes motion.**
2. **Geometry becomes parts.**
3. **Geometry becomes material.**

Module 0's print sits before this progression rather than inside it. It introduces the machine at its simplest — one solid, one orientation — so that Module 3 can address additive fabrication at the scale of an assembly.

---

## Software and Materials

### Required Software

| Purpose | Environment | Notes |
|---|---|---|
| **Primary language — taught in class** | Python 3.x | Written inside Blender or Rhino; no separate install required |
| Application environment | Blender (Python + Geometry Nodes) | Free and cross-platform. Recommended for students without a Rhino license. |
| Application environment | Rhino + Grasshopper (incl. Grasshopper Python) | Student license |
| Layout and post-processing | Adobe Illustrator, Photoshop, InDesign | Student license. Open-source equivalents accepted: Inkscape (vector), GIMP (raster), Scribus (layout) |
| Slicing | PrusaSlicer, Cura, or FabLab-specified slicer | Per FabLab standard |
| Plotter / cutting preparation | As specified by the FabLab | Introduced in Weeks 6 and 10 |

**Template-based design tools are not permitted.** Canva, Adobe Express, Figma templates, PowerPoint, Google Slides, Wix, and similar drag-and-drop or template-driven applications may not be used to produce any sheet, the Visual Identity Manual, or the Booklet.

The reason is the same one behind the Prohibited Shortcuts list: a template supplies the grid, the type hierarchy, the palette, and the spacing — which is precisely the set of decisions Assignment 0.2 asks you to make yourself, and that every sheet afterward is assessed on. A tool that makes those choices for you removes the thing being taught.

Work in a vector or raster editor where you control the coordinate space directly: Illustrator, Photoshop, and InDesign, or Inkscape, GIMP, and Scribus. Affinity Designer, Photo, and Publisher are also acceptable.

### Materials

Consumable materials for the fabrication assignments are **supplied by the School**, subject to the per-student limits below.

| Module | Supplied | Per-student allocation |
|---|---|---|
| 0 — CSG first print | Filament | One print, 200 g |
| 1 — Plotter drawing | Paper and pens | 3 sheets, 1 pen |
| 2 — Laser cutting | Sheet material — chipboard, basswood, or acrylic | 1 sheet |
| 3 — 3D printing | Filament | `[CONFIRM — FabLab supplied or student purchase]` |

Allocations are fixed. Students who exceed them are responsible for replacement material. Test cuts and failed prints count against the allocation, so plan them deliberately rather than iteratively — this constraint is itself part of the fabrication lesson.

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
| 2 | Analyze point, line, and plane as simultaneously graphic, spatial, and computational systems | All modules |
| 3 | Decompose a visual or geometric problem into an explicit sequence of procedural steps, expressed as pseudocode | Final, all modules |
| 3b | Construct and modify solid geometry through Boolean operations and transformations, maintaining a non-destructive operation history | 0.1, 3B |
| 4 | Write Python that applies fundamental programming constructs — variables, data types, lists, indices, conditionals, loops, functions — to generate and manipulate geometry | 1A, 2A, 3A, Final |
| 5 | Recognize the same computational logic across scripted and node-based environments, and reimplement a given system in a second one | 2A, 3A, Final |
| 6 | Generate and control point fields, sections, patterns, and differentiated surfaces | 1A, 2A, 3A |
| 7 | Prepare geometry correctly for computer-controlled drawing, cutting, and additive manufacturing | 1B, 2B, 3B |
| 8 | Evaluate and account for material and machine constraints — ordering, kerf, tolerance, manifold geometry, orientation | 1B, 2B, 3B |
| 9 | Assemble a fabricated system from computationally generated components | 2B, 3B |
| 9b | Plan a multi-part fabrication run against real machine, time, and material constraints, and account for the trade-off between differentiation and production cost | 3B |
| 10 | Develop and consistently apply a personal visual identity across a body of work | 0.2, Booklet |
| 11 | Communicate computational and fabrication processes through diagrams, documentation photography, and annotation | All B assignments, Booklet |
| 12 | Independently learn an unfamiliar computational workflow, extract its logic as pseudocode, and rebuild it as a reusable tool | Final |

---

## Module 0 — Foundations

The semester opens with two parallel tracks: a guided modeling tutorial that establishes the transformations Python will later express as code, and the personal graphic system used for the rest of the course.

### Assignment 0.1 — CSG Massing Sequence

A guided tutorial introducing solid modeling through Constructive Solid Geometry: form developed as an ordered sequence of geometric operations, each responding to an architectural rationale — program, orientation, circulation, views. This is where transformations are learned by hand, before Week 3 writes them as code. The workflow must remain **non-destructive**.

**Concepts:** Primitive solids · Translation · Rotation · Scale · Boolean union, difference, intersection · Non-destructive modeling · Manifold geometry · Print orientation · Supports · Layer height · Slicing · Axonometric and isometric representation · Exporting 3D geometry to 2D linework · Post-processing

**Requirements**

- 5+ Boolean operations
- 4+ distinct primitive types
- 2+ translations, 1+ rotation
- Operation history intact and demonstrable on request
- All primitives generated in-session; no imported models

**Assessed on** legibility of the operation sequence, quality of the axonometric set, and graphic execution of the final isometric.

**Deliverable:** One 17" × 11" sheet — one axonometric per operation, plus one larger final isometric with human scale, vegetation, context, shadows, and annotation. This diagram sets the documentation standard for every fabrication assignment that follows. **Due Week 3 — Sep 8 · 8%**

**First print — required.** The CSG result is 3D printed at small scale and presented at the Week 8 Midterm Review. This is the course's introduction to additive fabrication at its most basic: does the geometry survive contact with a machine, and what do you have to decide before it can.

Three things are learned here, all of which return at system scale in 3B:

- **Manifold geometry.** A Boolean that leaves an open edge or a self-intersection produces a model that looks correct on screen and fails in the slicer. Finding that out in Week 8 rather than Week 15 is the point.
- **Orientation.** The same solid prints differently depending on how it sits on the bed — surface quality, strength, and time all change.
- **Supports, by their absence.** **No supports are permitted on this print.** Where geometry overhangs, supports are what a slicer adds to hold it up, and they cost material, time, and post-processing labor. Banning them here leaves orientation as your only lever, which is the fastest way to learn what orientation actually does. Supports become available in 3B, once you know what you are buying with them.

**Additional requirements**

- An orientation diagram on the sheet showing your chosen print orientation, the overhangs it produces, and why you chose it over an alternative
- If the geometry cannot print unsupported in any orientation, revise the geometry — that is a legitimate and expected outcome

Assessed on printability and on the reasoning behind your orientation and support decisions. Craft and finish are not assessed here; those belong to 3B. **No credit is issued for 0.1 without the print.**

Printer queue is open from Week 3. Print within the scope limit below.

### Assignment 0.2 — Visual Identity Manual for Architects

A personal graphic system applied to every subsequent assignment. Drawings, diagrams, renders, captions, typography, and page layouts should work together rather than as separate decisions.

**Standards to define:** Personal logo · Color palette and color theory · Typography · Font hierarchy and sizing · Line weights · Captions · Image labels · Graphic hierarchy · Margins · Grid systems · 17" × 11" tabloid sheet template · Booklet cover

**Requirements**

- 8+ pages
- No more than 3 typefaces, with a hierarchy of 4+ levels
- 5+ color palette with stated values and written rationale
- 4+ defined line weights, each with an assigned use
- One tabloid template with the grid shown explicitly
- Built in a vector or layout editor, not a template-based tool (see *Software and Materials*). The grid, hierarchy, and palette must be your decisions

**This is a provisional system.** It is designed before you have content to test it against and is expected to change. A mandatory revision is submitted with the Final Booklet and assessed there.

**Deliverable:** Separate PDF. **Due Week 4 — Sep 15 · 8%**

---

## Module 1 — POINT
### Focus: Lists, Arrays, and Fields

The first module is about **collections**: how to generate a set of positions, how to store them, how to reach into that store and change part of it. A list is the data structure; an array is what you get when a list is laid out in space; a **field** is what you get when a value varies continuously across that space; a point is the individual item.

An attractor is the simplest field there is — every point asks how far it is from something, and that distance drives a property. That question returns in Module 2 as a signed distance field, so the idea is introduced here and extended there.

A single point represents a position. Collections of points describe fields, patterns, density, information, images, and three-dimensional form.

**Visualization concepts:** Point · Coordinate · Point cloud · Field · Distribution · Density · Gradient · Scale · Proximity · Composition

**Computational concepts:** Variables · Data types · Coordinates · Lists · Indexing · Sequences · Basic loops · Basic functions · Randomization

Arrays are introduced as systems for generating and organizing points in space, rather than simply as commands for duplicating geometry. Students explore rectangular, radial, and hexagonal arrays, distribution along curves, point clouds, list manipulation, point relationships, and single, multiple, and curve attractors.

### Assignment 1A — POINT: Arrays + Attractors

An array organizes points; an attractor differentiates them. This assignment explores what happens when the two are combined — a matrix of approaches in which different array types are driven by different attractor types, so that the same organizing structure yields very different fields depending on what varies across it.

**Requirements**

- 3+ distinct array/attractor combinations, drawing on the array types covered in Tutorial 1.1 (rectangular, radial, hexagonal, along a curve) and covering all three attractor types (single-point, multiple-point, curve)
- 3+ distinct parameters driven by attractor distance across the set — scale, rotation, density, height, color
- 1+ composition containing 1,000 or more elements; 1+ resolved spatially in 3D
- For one combination: **three views of the same system** — isometric, close-up, eye-level perspective
- Minimum 2 sheets
- Arrays and falloff authored. Array add-ons, scatter tools, and preset falloff plugins prohibited

**Assessed on** composition, density, rhythm, contrast, hierarchy, gradient, scale, depth, and color — and on whether the set reads as a systematic exploration rather than four unrelated images.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 6 — Sep 29 · 8%**

### Assignment 1B — POINT: Toolpath Drawing
**Fabrication: Computer-Controlled Motion**

Pick one system from 1A and draw it physically, using a pen plotter or robotic arm. The assignment turns on one transition: **geometry must become an ordered sequence before a machine can execute it.** Points and lists define motion, and the ordering of data directly determines the mark.

**Topics:** Lists · Indices · Point ordering · Toolpaths · Travel moves · Drawing moves · Pen up / pen down · Coordinate systems · Machine motion · Machine constraints

**Conceptual workflow:** Point → Sequence → Toolpath → Motion → Mark

**Assessed on** correctness of the toolpath logic, craft of the physical drawing, and clarity of documentation.

**Deliverable:** Drawing within the stated scope limits, plus photographic documentation and a toolpath diagram. **Due Week 8 — Oct 13, with the Midterm · 8%**

---

## Module 2 — LINE
### Focus: Section and Sequence

The second module is about **order**: taking something continuous, cutting it into discrete pieces, and keeping track of which piece goes where. Section is the operation; sequence is what makes the result legible and buildable. Where Module 1 asked how to organize a collection, Module 2 asks how to produce one from a solid — and then how to put it back together.

Continuous geometry is intersected by planes and translated into a series of discrete linear profiles, creating a direct relationship between graphic representation and fabrication.

**Visualization concepts:** Line · Direction · Profile · Section · Contour · Sequence · Flow · Intersection · Line density · Line hierarchy

**Computational concepts:** Loops · Iteration · Conditionals · Boolean logic · Filtering · Sequences · Ranges · Relationships between lists · Geometric intersections · Signed distance fields

Students describe workflows procedurally: generate geometry → generate section planes → iterate through the planes → intersect each plane with the geometry → store the resulting profiles → filter or modify results → organize the sections → visualize or fabricate the system.

### Assignment 2A — LINE: Section + Direction

A composition in which line is the primary representational element. Section is explored beyond the conventional section drawing — serial, overlapping, directional, data-driven. The result may be abstract, spatial, analytical, architectural, or representational.

**Requirements**

- 1+ system generated from 20 or more serial sections
- 2+ distinct section directions
- 3+ distinct line weights, each with a stated role in the hierarchy
- 1+ conditional filter that removes or modifies a subset of profiles based on a tested property
- Section planes and intersections generated by your own loop; automated contour and sectioning plugins prohibited

**Assessed on** line weight, rhythm, direction, density, hierarchy, overlap, contrast, and positive/negative space.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 10 — Oct 27 · 8%**

### Assignment 2B — LINE: Section-Based Fabrication
**Fabrication: Computer-Controlled Cutting**

Continuous geometry translated into a series of flat profiles, then reassembled so that the sections **generate depth by accumulation**. A surface or volume is intersected by planes; the profiles become parts; the parts, spaced and held in relation to one another, reconstruct the spatial character of the original.

**The assembly strategy is yours to determine.** Interlocking slots — the waffle — are one answer. So are sections stacked on threaded rod, spaced by sleeves or washers, bolted through aligned holes, suspended from cables, laminated face to face, or held in an external frame. Different strategies produce different relationships between part and whole, and choosing among them is part of the assignment.

What every strategy shares is **registration**: each component must know where it goes. Design that system and make it legible.

**Workflow:** Generate continuous geometry → establish section direction(s) → generate section planes → intersect → extract profiles → give profiles material thickness → design the registration and connection system → label components → nest → prepare files → cut → test fit → assemble.

**Fabrication concepts:** Computer-controlled cutting · Laser cutting · 2D machine files · Material thickness · Kerf · Tolerance · Registration · Slots and joinery · Fasteners, spacers, and tension elements · Nesting · Component labeling · Assembly sequence

**Conceptual workflow:** Continuous Geometry → Section → Profile → Part → Assembly

**Requirements**

- 12+ sections generated computationally, not drawn
- A registration system that positions every component without measurement during assembly
- Kerf and tolerance measured on your own test cut and stated on the sheet — not assumed
- All components labeled, with labels legible in the assembled object or documented in the exploded diagram
- Nesting layout submitted, with material efficiency stated
- The assembly must be self-supporting, or its support strategy explicitly designed
- One-click waffle plugins prohibited; the section series and the connection geometry must be authored

**Assessed on** fit and tolerance, craft of assembly, coherence between the chosen strategy and the geometry it serves, efficiency of nesting, and clarity of documentation.

**Deliverable:** Laser-cut sectional assembly within the stated scope limits, plus photographic documentation, an exploded assembly diagram, and the nesting layout. **Due Week 11 — Nov 3 · 8%**

---

## Module 3 — PLANE
### Focus: Modularity and Tessellation

The third module is about **the component**: design one module, then vary it across a surface. Tessellation is how the surface is divided; modularity is what makes the pieces relate to one another and to the whole. This is where the course's two-dimensional data structures arrive — a grid is a list of lists, and a panel field is that grid with a component mapped onto every cell.

A plane need not function as a solid boundary — it can selectively filter light, views, information, density, or movement. Nor need it stay flat: a vault is a plane that has acquired curvature and structure, and panelizing one raises problems a flat façade never does.

**Visualization concepts:** Plane · Surface · Curvature · Vault · Pattern · Filter · Layer · Panel · Aperture · Porosity · Transparency · Relief · Tessellation

**Computational concepts:** Nested loops · Functions · Grids · Two-dimensional data structures · UV coordinates · Data mapping · Remapping · Conditional variation · Parametric variation

**Panelization tools are permitted in this module.** Having built grids and loops by hand in Modules 1 and 2, you have earned the right to use a library.

| Environment | Tools |
|---|---|
| Blender | **Tissue** (Zomparelli) — the Tessellate operator maps a component object onto the faces of a base mesh; also Dual Mesh and weight/color exchange |
| Grasshopper — native | **Surface Box + Box Morph** — the direct structural equivalent of Tessellate, requiring no plugin. Start here. |
| Grasshopper — plugins | **Paneling Tools** (Issa, McNeel) · **Pufferfish** (Pryor) for twisted-box morphing · **LunchBox** for panel grid types · **Weaverbird** for mesh subdivision and thickening |

The tool may generate the tessellation. **The differentiation across it must be yours** — your parameters, your mapping, your remapping ranges. A field of identical panels produced by a plugin is not an answer to this assignment.

### Assignment 3A — PLANE: Surface + Filtering

A computational graphic exploring the plane as a variable surface or filter. The primary objective remains the quality of the image — rendering, lighting, shadow, materiality, and post-processing carry more weight in this module than in the previous two.

**3A and 3B describe the same system.** The graphic shows the surface whole; the print realizes a 3 × 3 fragment of it. Choose a vault or a façade here, and develop it in both.

**Requirements**

- A field of 400+ cells or panels (minimum 20 × 20)
- 2+ independent parameters driving the variation
- 1+ explicit remapping operation, with input and output ranges documented on the sheet
- **Three views of the same system:** overall, close-up detail, and eye-level or oblique
- 1+ rendered image with controlled lighting demonstrating the filtering behavior
- Panelization and tessellation tools are **permitted** — the variation driving them must be authored (see below)

**Assessed on** surface, figure/ground, pattern, repetition, variation, transparency, depth, shadow, and material appearance.

**Deliverable:** 17" × 11" sheet(s) in your visual identity. **Due Week 13 — Nov 17 · 8%**

### Assignment 3B — PLANE: Additive Fabrication
**Fabrication: 3D Printing**

The surface system built in 3A, fabricated as an architectural element. Students build **either a vaulted structure or a façade fragment** — a curved or planar surface panelized into physical components that connect to one another.

A vault introduces a condition the flat sheet never posed: panels sitting on a doubly curved surface distort, and a component that reads cleanly on a plane will not necessarily close on a curve. Resolving that is half the assignment.

The other half is **fabrication management**. This is the first assignment where you are not making an object but running a production. Nine or more parts, one shared machine, a fixed deadline, and a queue you share with everyone else in the room. How many objects, how long each takes, in what order, batched how, with what margin for a failed print — these are the questions, and they have to be answered before the first file is sliced.

There is a real trade-off buried here, and it is the point. **Differentiation costs production time.** Nine identical panels batch efficiently and teach nothing; nine wholly unique panels may not finish. Where you land between those is a design decision with fabrication consequences, and defending that position is part of what is assessed.

**Requirements**

- **Minimum 9 panels** (3 × 3 or equivalent) forming a continuous assembly
- Panel-to-panel connections designed, not improvised — the assembly must hold together
- Variation across the panel set; nine identical panels do not meet the requirement
- **A production plan, submitted in Week 13 (Nov 17) before the queue opens:** panel count, estimated print time per panel, total machine hours, batching and orientation strategy, print order, and what you will do if a print fails
- Manifold, watertight geometry with stated wall thickness
- **Supports are permitted here but must be minimized and justified.** Every support is print time, material, and post-processing labor you have chosen to spend — account for it in the production plan. Orientation remains the first tool; supports are what you use when orientation runs out.
- Within the stated print scope limits

**Fabrication concepts:** Manifold geometry · Meshes · Surface thickness · Resolution · Layer height · Print orientation · Supports · Slicing · Toolpaths · Material use · Print time · Tolerances · Panel connections · Production planning · Batching · Machine scheduling · Failure contingency

**Conceptual workflow:** Plane → Variation → Volume → Layers → Material

**Assessed on** printability of the geometry, print quality, resolution of the panel connections, realism of the production plan and how well the built result matches it, appropriateness of orientation and layer decisions, and clarity of documentation.

**Deliverable:** 3D-printed vault or façade fragment of 9+ panels within the stated scope limits, plus photographic documentation and a slicing/orientation diagram. **Due at the Final Review, Dec 10–16 · 8%**

> **Print queue:** Files must be submitted to the FabLab queue by the end of Week 13 (Nov 17). Prints submitted after that date are not guaranteed to complete before the deadline, and queue congestion is not grounds for an extension. The physical object is presented at the Week 15 final review; its photographic documentation may be added to the Booklet within 48 hours of the review.

---

## Final Assignment — Reverse-Engineer a Workflow, Build a Tool

The semester closes by turning a technique you did not know into an instrument you own. Three stages: **study** an existing workflow, **extract** its logic, **build** your own tool from it.

The distinction that matters here is between a *result* and a *tool*. A result is one image. A tool takes inputs and produces a family of outputs — it is reusable, and someone else could run it. This assignment asks for the second.

A **one-paragraph proposal** naming the workflow you intend to study and what you think you will build from it is due in Week 14 (Nov 24).

### Stage 1 — Study

Find a workflow that interests you: a tutorial, a shared definition, a published paper, an existing add-on. Grasshopper, Blender Geometry Nodes, Houdini, TouchDesigner, Processing, Three.js, or anything else procedural — environments beyond the four used this semester are deliberately permitted. Follow it until it works and you understand why.

### Stage 2 — Extract

Write the logic as **pseudocode in your own words**, independent of the original's interface. Not "plug the Populate 2D into the Voronoi" but what the procedure actually does, step by step, in language that would survive being carried to a different platform.

This is the pivot of the assignment. Separating a procedure from the software that happened to express it is the single most transferable skill in the course, and it is what the whole semester has been building toward.

### Stage 3 — Build

Implement that logic as **your own tool** — a Python script, a Grasshopper definition, a Blender node group — with named inputs a user can change. Coding assistance is permitted under the Stage 2 AI terms, with your pseudocode written first and the prompt log submitted.

Your tool must do something the original did not. It must demonstrate at least **two** substantive departures:

- A different data source or input drives the system
- The dimensionality or topology of the output is changed
- A step in the procedural logic is replaced, not merely re-parameterized
- The system is extended with logic not present in the original
- The workflow is reimplemented in a different environment than the original's

Changing colors, materials, or slider values does not count.

**Required content across the two sheets:** Screenshot and full link to the original · Your pseudocode · A diagram of the extracted logic · The original's result, reproduced · Your tool — code, definition, or node group, with inputs labeled · **At least three outputs from your tool, produced by varying its inputs** · Full AI prompt log where applicable · Written explanation of what you changed and why

The three-output requirement is how a tool proves it is a tool. One image proves nothing.

**Live demonstration.** At the final review you will run your tool with inputs you have not prepared in advance. **A student who cannot explain or operate their own tool receives no credit for Computational Understanding, regardless of whether it runs.**

**Deliverable — two 17" × 11" sheets**, plus the tool file submitted with the Booklet materials.

| Sheet | Content |
|---|---|
| **1 — Process** | The three stages made visible: the original workflow (screenshot and link), your pseudocode, the original's result reproduced, and a diagram of the logic you extracted. This sheet answers *how did you get from their thing to yours.* |
| **2 — Tool** | The tool itself — code, definition, or node group with inputs labeled — and at least three outputs produced by varying those inputs, arranged so the effect of each input is legible. This sheet answers *what does it do.* |

Both sheets use your visual identity. The process sheet is not documentation of the tool sheet; the two carry different arguments, and both are assessed.

**Due:** Final Review, Dec 10–16 · **Weight: 13%**

---

## Midterm Review — Week 8, Oct 13

At the midterm, students **print and present all work completed to date**, in its latest revised form, using their visual identity:

- 0.1 CSG Massing Sequence — sheet **and verification print**
- 0.2 Visual Identity Manual
- 1A POINT: Arrays + Attractors
- 1B POINT: Toolpath Drawing (with documentation)

The printed set is what is reviewed. Work shown on a screen is not assessed.

**The midterm does not re-grade the individual assignments.** Those grades stand. Like the Final Booklet, the midterm assesses what only an assembled body of work can show:

| Component | Share of midterm grade |
|---|---|
| Evidence of revision in response to critique received so far | 40% |
| Coherence of the visual identity across the set | 30% |
| Quality of print, layout, and documentation | 30% |

**Weight: 8%**

This is also the formal point at which students receive a standing in the course while there is still time to act on it.

---

## Prohibited Shortcuts

Several assignments name components, add-ons, or plugins that may not be used. The rule behind them is consistent: **a tool that automates the concept an assignment exists to teach may not be used in that assignment.**

| Assignment | Prohibited |
|---|---|
| All sheets, 0.2, and the Booklet | Canva, Adobe Express, template-driven layout apps, PowerPoint, Google Slides. Use a vector or raster editor — see *Software and Materials* |
| 0.1 | Imported or downloaded models; any geometry not generated in-session |
| 1A | Array add-ons, scatter and distribution tools, preset attractor falloff plugins |
| 2A / 2B | Automated contour and sectioning plugins; one-click waffle and slotting generators |
| 3A / 3B | Panelization libraries are **permitted** for generating the tessellation. Their preset gradient, attractor, and variation components are not — the differentiation must be authored |
| All Grasshopper work | The Cross Reference component may be used **once** per definition |

These tools are legitimate professional instruments and students are encouraged to learn them — after the semester, or in the Final Assignment, where the constraint is lifted. During the modules, the point is to build the logic rather than call it.

The constraint relaxes as the semester progresses. Module 3 permits panelization libraries precisely because Modules 1 and 2 required building grids and loops by hand; the restriction exists to earn the tool, not to forbid it.

Use of a prohibited tool is assessed as a failure to meet Assignment Requirements for that submission.

---

## Final Submission — Booklet + Visual Identity Manual

Two separate PDF files, due at the Final Review (Dec 10–16).

### 1. Final Booklet — **Weight: 10%**

The Final Booklet contains all course assignments in their latest revised form. Students are expected to incorporate feedback received throughout the semester rather than resubmit original work.

Contents: CSG Massing Sequence · POINT — Arrays + Attractors · POINT — Toolpath Drawing · LINE — Section + Direction · LINE — Section-Based Fabrication · PLANE — Surface + Filtering · PLANE — Additive Fabrication · Final — Reverse-Engineer a Workflow, Build a Tool (both sheets)

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

| Item | Weight |
|---|---|
| 0.1 — CSG Massing Sequence | 8% |
| 0.2 — Visual Identity Manual | 8% |
| 1A — POINT: Arrays + Attractors | 8% |
| 1B — POINT: Toolpath Drawing | 8% |
| 2A — LINE: Section + Direction | 8% |
| 2B — LINE: Section-Based Fabrication | 8% |
| 3A — PLANE: Surface + Filtering | 8% |
| 3B — PLANE: Additive Fabrication | 8% |
| **Midterm Review (Oct 13)** | 8% |
| Final — Procedural Workflow Exploration | 13% |
| Final Booklet | 10% |
| Attendance and participation | 5% |
| **Total** | **100%** |

Every assignment carries equal weight. The Midterm and the Final Booklet are the only items that assess the body of work rather than a single submission, and neither re-grades work already assessed.

### Evaluation Criteria

Each assignment is assessed against the following criteria. Percentages indicate the share of that assignment's grade.

| Criterion | Digital assignments (0.1, 0.2, 1A, 2A, 3A, Final) | Fabrication assignments (1B, 2B, 3B) |
|---|---|---|
| **Visual Quality** — composition, hierarchy, contrast, color, typography, line weight, image quality, graphic impact | 35% | 20% |
| **Computational Understanding** — assessed primarily through live modification of your own work at pin-up (see AI policy); secondarily through pseudocode and written explanation | 25% | 20% |
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

**Every tutorial is provided in two versions — Grasshopper and Blender Geometry Nodes** — implementing the same logic in both. Watch the one for your chosen environment; skim the other at least once per module to see the logic survive the change of interface.

---

## Tutorial Calendar

| # | Tutorial | Released | Covers |
|---|---|---|---|
| **0.1** | 3D Transformations — *the 10-cube challenge* | Week 1 | Translate, rotate, scale. Ten cubes, ten distinct transformation states, from one primitive |
| **0.2** | CSG Operations in Graphs | Week 2 | Boolean union, difference, intersection built as a graph — non-destructive by construction |
| **0.3** | 3D Printing Basics | Week 3 | Manifold checking, orientation, supports, layer height, slicing, sending a file to the queue |
| **1.1** | Arrays | Week 4 | Rectangular grid · radial · hexagonal · along a curve, including distribution on a divided curve |
| **1.2** | Attractors | Week 5 | Single-point, multiple-point, and curve attractors; distance, falloff, and remapping |
| **1.3** | Toolpath Logic | Week 6 | Direction, ordering, retraction, pen up/down, and running the plotter |
| **2.1** | Contour Curves from SDF Solids | Week 9 | Signed distance fields, isosurfaces, and extracting contour curves as serial sections |
| **2.2** | 2D Fabrication | Week 10 | Waffle logic, slots and registration, kerf and tolerance, nesting, labeling, alternative connection strategies |
| **3.1** | Panelization + Tessellation | Week 12 | Surface Box / Box Morph and Tissue Tessellate; UV domains, component morphing, variation across a field |
| **3.2** | Fabrication Strategies | Week 13 | Panel connections, wall thickness, print orientation for a set, batching and production planning |
| **4.1** | Tool Building with AI Assistance | Week 12 | Pseudocode to code; prompting for geometry work; verifying and correcting generated output; exposing named inputs so a script becomes a tool |

Tutorial 4.1 is released early, alongside the Final Assignment brief, so that you can begin the final while Module 3 is still running.

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

| Wk | Date | Content | Computational Focus | Due |
|---|---|---|---|---|
| | | **Weeks 1–7: AI-free. Coding assistance permitted from Week 8 onward, with disclosure.** | | |
| 1 | Aug 25 | Course introduction. Point/Line/Plane framework. **Tutorial 0.1.** **CSG I:** primitives, move / rotate / scale, Boolean operations, manifold vs. non-manifold, non-destructive workflow. Visual identity brief issued. | Operations as an ordered sequence | FabLab Safety Orientation enrollment |
| 2 | Sep 1 | **Tutorial 0.2.** **CSG II:** massing sequence logic; axonometric and isometric representation; exporting 3D geometry to 2D linework; post-processing. | Operation hierarchy; reading a model as a process | FabLab Safety Orientation **completed** |
| 3 | Sep 8 | **Tutorial 0.3.** **Python I** — writing and running scripts inside Blender and Rhino. The same CSG operations, rebuilt as code. **Printer queue opens.** | Variables, data types, transformations as function calls | **0.1 — CSG Massing Sequence** (sheet) |
| 4 | Sep 15 | **Tutorial 1.1.** **Python II.** **Module 1 — POINT** begins. Arrays as systems: rectangular, radial, hexagonal, along a curve. | Lists, indexing, loops, functions, randomization | **0.2 — Visual Identity Manual** |
| 5 | Sep 22 | **Tutorial 1.2.** Attractors: single, multiple, curve. Point clouds, image sampling. **Same system built twice** — once scripted, once in Geometry Nodes / Grasshopper. | Distance, falloff, remapping, point relationships | — |
| 6 | Sep 29 | **Tutorial 1.3.** 1A pin-up and critique. 1B briefing: toolpaths, ordering, machine constraints. Plotter demonstration. | Point ordering; travel vs. drawing moves | **1A — Arrays + Attractors** |
| 7 | Oct 6 | Plotter production session. *Midterm Studio Reviews week — no submissions due.* | Coordinate systems, machine motion | — |
| 8 | Oct 13 | **MIDTERM REVIEW** — printed set presented; **live modification begins.** **Module 2 — LINE** opens in the second half of the session. | Iteration, conditionals, Boolean logic | **1B — Toolpath Drawing** · **Midterm submission** |
| 9 | Oct 20 | **Tutorial 2.1.** Section logic: serial sections, contours, direction fields, flow lines. Line hierarchy. *Midterm grades posted; written notice of poor performance issued.* | Signed distance fields, filtering, ranges | — |
| 10 | Oct 27 | **Tutorial 2.2.** 2A pin-up and critique **with live modification.** 2B briefing: section strategies, registration, material thickness, kerf, tolerance, nesting, labeling. | Geometric intersections | **2A — Section + Direction** |
| 11 | Nov 3 | Laser production session. Assembly workshop. | Component ordering and assembly sequence | **2B — Section-Based Fabrication** |
| 12 | Nov 10 | **Tutorials 3.1 + 4.1.** **Module 3 — PLANE** begins. Grids and two-dimensional data. Panelization, apertures, relief. **Final assignment released.** | Nested loops, UV coordinates, mapping | — |
| 13 | Nov 17 | **Tutorial 3.2.** 3A pin-up and critique **with live modification.** Rendering, lighting, post-processing. 3B technical briefing: manifold geometry, thickness, orientation, slicing, production planning and batching. **Print queue closes end of week.** | Remapping, conditional and parametric variation | **3A — Surface + Filtering** · **3B production plan** |
| 14 | Nov 24 | Print production. Final desk crits. Booklet layout workshop. *Thanksgiving break follows.* | — | **Final proposal** |
| 15 | Dec 1 | Last regular session. Final desk crits, booklet review, print troubleshooting. *Final Studio Reviews week — no submissions due.* | — | — |
| — | Dec 10–16 | **FINAL REVIEW** — scheduled exam date and time `[CONFIRM against the University exam schedule]` | — | **3B print · Final: 2 sheets + tool file · Final Booklet PDF · Visual Identity Manual PDF** |

**Three constraints shaped this schedule.** Week 7 falls in Midterm Studio Reviews, so 1B moves to the Week 8 midterm rather than being due during that window — the plotter session still runs, only the deadline shifts. Week 15 falls in Final Studio Reviews, so it is a working session with nothing due, and the final submission moves to the University exam period. Midterm grades are due Oct 20, one week after the Midterm Review on Oct 13, which is workable but leaves no slack — expect to grade that set within the week. The Oct 30 "W" deadline falls after grades post, so students receive a standing before the drop decision.

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

### Stage 1 — Weeks 1 through 7: AI-free

No AI assistance of any kind in producing coursework through the Week 8 Midterm. This covers 0.1, 0.2, 1A, and 1B.

Permitted throughout, at any stage: asking an AI to explain a computational concept, clarify syntax, or interpret an error message. Not permitted: asking it to write, complete, or fix your code.

This period exists so that variables, lists, indices, loops, conditionals, and functions are installed as your own working vocabulary. Module 1's fabrication assignment in particular depends on it — the lesson of 1B is that data ordering determines what the machine draws, and that lesson is learned by getting the ordering wrong and working out why. Correct output supplied on the first attempt teaches nothing.

### Stage 2 — Week 8 onward: coding assistance permitted, with disclosure

From Module 2 forward, AI may be used to generate, debug, refactor, or explain **code**, subject to:

- **Pseudocode first.** Your own written decomposition of the problem must precede any code generation, and is submitted alongside it. AI-generated pseudocode submitted as your own procedural reasoning is a violation.
- **Full disclosure.** Tool and version, the prompts used, what was kept, and what was changed. Citation follows https://fau.edu/ai/citation.
- **Live modification** (see below).

### Not permitted at any stage

- **Generative image models** — Midjourney, Stable Diffusion, DALL·E, Firefly, or any diffusion-based tool — to produce, extend, or modify any image submitted as coursework. This includes backgrounds, textures, entourage, generative fill, and AI upscaling.
- AI generation of the visual identity system, including logo, palette, and layout.

The reason is specific rather than reflexive: in 1A, 2A, and 3A the assessed outcome *is the image*. Delegating its production removes the exact judgment the assignment exists to develop. In the computational work, the assessed outcome is procedural understanding, and an assistant does not remove that — provided you can account for what the code does.

### Live Modification

At every pin-up and review from Week 8 onward, each student will be asked to make **one unscripted change to their own work in front of the class** — reverse a section order, alter an attractor's falloff, add a conditional, change a mapping range. Roughly ninety seconds per student.

This, rather than a written explanation, is the primary assessment of Computational Understanding. It applies equally to scripted and node-based work, and equally whether or not AI was used.

A student who cannot modify their own submitted work receives no credit for Computational Understanding on that assignment, regardless of whether the work runs or how it looks. Where the work is demonstrably not the student's own, this may constitute a violation of Regulation 4.001.

### Accountability

Students are responsible for the accuracy and behavior of any AI-assisted output they submit. AI may generate geometry that is subtly wrong — non-manifold meshes, inverted normals, off-by-one indexing in a toolpath — and these reach the machines. Verification is the student's obligation, not the tool's.

### Critical Awareness

While generative AI models are not used to produce work in this class, students should be aware of their availability and capabilities in order to develop a critical perspective. The distinction between automated two-dimensional image generation and the discrete techniques used here — building three-dimensional systems, extracting information from them, and compositing images — is itself a subject of the course. Understanding when a tool is appropriate to a task is part of what a designer is expected to know.

---

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

A module-specific reference set is distributed at the start of each module and expands this list.

These references support the assignments while leaving students free to develop their own visual and computational interpretations.

---

## NAAB Student Performance & Program Criteria

The following National Architectural Accreditation Board (NAAB) criteria are satisfied in this course. Definitions can be found at NAAB.org/Conditions.

`[CONFIRM with the School whether the 2014 SPC set below or the 2020 Conditions PC/SC set should be cited for this accreditation cycle.]`

| Criterion | Description | Where Satisfied |
|---|---|---|
| **A.2 Design Thinking Skills** | Ability to raise clear and precise questions, use abstract ideas to interpret information, consider diverse points of view, reach well-reasoned conclusions, and test alternative outcomes against relevant criteria and standards. | Final Assignment; all module A assignments |
| **A.3 Investigative Skills** | Ability to gather, assess, record, and comparatively evaluate relevant information and performance in order to support conclusions related to a specific project or assignment. | Final Assignment; module briefings and reference research |
| **A.4 Architectural Design Skills** | Ability to effectively use basic formal, organizational and environmental principles and the capacity of each to inform two- and three-dimensional design. | Modules 1–3, A and B assignments |
| **A.5 Ordering Systems** | Ability to apply the fundamentals of both natural and formal ordering systems and the capacity of each to inform two- and three-dimensional design. | Module 1 (fields, distribution); Module 3 (panelization, tessellation) |
| **A.6 Use of Precedents** | Ability to examine and comprehend the fundamental principles present in relevant precedents and to make informed choices about the incorporation of such principles into architecture and urban design projects. | Conceptual references; Final Assignment, Stage 1 |
| **PC.5 Research and Innovation** | How the program prepares students to engage and participate in architectural research to test and evaluate innovations in the field. | Final Assignment; fabrication modules |

---

*Syllabus subject to revision. Any changes will be announced in class and posted to Canvas.*
