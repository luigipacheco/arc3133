# ATLV GH Python — Keep / Cut Audit against ARC 3133

Source: *ATLV / Education / GH Python* (Satoru Sugihara), 78 pp., **~110 examples across 8 sections**.
Target: ARC 3133 Viz 1, eleven tutorials, Blender Python track prioritized.

**Verdict: keep ~20 of ~110 examples (18%).** Everything kept needs porting — IronPython 2 → Python 3, `rhinoscriptsyntax` → `bpy`. Roughly half of what the syllabus needs has no ATLV source at all and must be written from scratch.

---

## 1. Section-by-section

| § | ATLV section | Ex. | Keep | Verdict |
|---|---|---|---|---|
| 0 | References & Resources | — | 0 | **Cut.** Rhino 5 / IronPython 5.0 links, all dead or superseded. Cite the page for attribution only. |
| 1 | GH Python Basics | 10 | **7** | **Core keep.** This is Tutorial 0.3 / Python I almost verbatim. |
| 2 | Inputs | 15 | **5** | **Selective.** Named inputs and the distance examples are gold; the 6 panelization variants and 3 data-tree examples are not. |
| 3 | Function and Recursion | 10 | **2** | **Mostly cut.** Keep the two plain functions. Recursion is not in the syllabus. |
| 4 | Baking and Object Attributes | 10 | **3** | **Condense.** Ten near-duplicates of one lesson: get geometry out of the script with color, material, and layer. |
| 5 | Object-Oriented Programming | 8 | **0** | **Cut.** No learning outcome mentions classes. Students meet their first loop in Week 3. |
| 6 | Connective Module | 7 | **0** | **Cut** from the tutorials. Park 6-1/6-2 as Final-assignment reference. |
| 7 | Custom Subdivisions | 36 | **5** | **Heavy cut.** 30+ recursive subdivision variants against a module that permits Tissue and Box Morph. |

---

## 2. What to keep, and where it lands

### Tutorial 0.3 / Python I — Week 3
The whole point of § 1 is one CSG script rebuilt as code, so these become the language primer.

| ATLV | What it teaches | Note on porting |
|---|---|---|
| 1-1 First code | script → geometry in the document | `print text` → `print(text)`. In Blender there is no `AddPoint`; decide the point strategy first (see § 4). |
| 1-2 For loop | `range`, the loop | Fine as-is. |
| 1-3 List | empty list, `append` | Fine as-is. The single most important idea in Module 1. |
| 1-4 If condition | `%`, even/odd branching | Fine as-is. |
| 1-5 If / elif / else | three-way branch | Fine as-is. |
| 1-6 Math library | `sin`/`cos` driving position — a spiral | Best example in the section. Keep. |
| 1-7 Random | `random.random()` gated by a condition | Keep. Set a seed — students need reproducible results between class and pin-up. |
| 1-8 2D nested loop | `i`/`j` grid | **Keep, but move to Tutorial 1.1** — it *is* the rectangular array. |
| 1-9 And/or in loop | 8-branch `elif` chain | **Cut.** Hardcoded regions, not a system. Teaches the wrong habit for a course assessed on live modification. |
| 1-10 Conditions + patterning | same, with `%` | **Cut** or reduce to a two-line version. |

### Tutorial 1.1 Arrays — Week 4
- **1-8** — rectangular array, the nested loop.
- **2-5** curve input, division points — this is *array along a curve*, and the inner closest-point search is a preview of 1.2. Keep the division half here, the distance half for 1.2.
- 1-6's spiral covers the radial case if you rewrite it in polar terms.
- **Missing: hexagonal.** ATLV has no hex array anywhere. Write from scratch — offset every other row by half a step.

### Tutorial 1.2 Attractors — Week 5
- **2-4** point clustering — the "measure distance to every other point, act on the result" loop. Structurally an attractor already; reframe.
- **7-3** move vertices by closest attractor — has the pattern you actually want to teach: a `attractorVector(pos)` function that finds the nearest attractor, then scales by `(threshold - dist)/threshold`. That line is falloff, and it is the only place in 110 examples where ATLV normalizes a distance to 0–1.
- **7-23** face offset with attractors — multi-attractor, drives four properties at once. Good as the "one field, several parameters" example.

> **Gap to write:** 1A requires a documented remapping. ATLV never writes a `remap()` function — it hardcodes multipliers like `i*0.05` everywhere. Write `remap(value, in_min, in_max, out_min, out_max)` as a named function and use it in every subsequent script, so students can state input and output ranges on the sheet because the code says them out loud.
>
> Also missing: curve attractors (1A requires all three types), and falloff shapes beyond linear.

### Tutorial 2.1 Contours from SDF — Week 9
- **2-6** curve intersections — the only intersection example in the source. Useful for the *idea* (test a pair, store what you find), but the syllabus wants plane × solid, not curve × curve. Port the loop skeleton, replace the operation.
- **7-30 / 7-31** dispatch faces randomly / by attractor — a conditional filter over a collection. Maps directly to 2A's "conditional filter that removes or modifies a subset based on a tested property."

> **Gap:** signed distance fields, isosurfaces, contour extraction. Nothing in ATLV. Write from scratch.

### Tutorial 3.1 Panelization — Week 12
- **2-7** surface panelization — keep **one** of the six. They differ by output geometry, not by logic; the logic is `for u: for v: evaluate surface, build component`. One example, then Tissue / Box Morph.
- **7-25** extruded face offset with attractors — variation across a panel field, closest thing in the source to 3A.

> **Gap:** UV domain remapping into a component's local space, which is what Box Morph does and what students must understand to author the variation driving it.

### Tutorial 4.1 Tool Building — Week 12
- **2-1** integer/float input and **2-2** point input. Small examples, disproportionate value: this is *exactly* "exposing named inputs so a script becomes a tool," and the difference between a result and a tool that the Final assignment turns on.
- **3-1 / 3-2** functions with one and three arguments. Same lesson at the language level.

### Sheet and render production — cuts across 1A, 2A, 3A
From § 4, keep three, drop seven:
- **4-1** color per object — 1A requires color as an attractor-driven parameter.
- **4-3 or 4-5** material assignment — 3A requires a rendered image with controlled lighting.
- **4-7** baking into layers — underrated. Objects sorted into named layers is how a script's output arrives in Illustrator as editable, separable linework, which is how 2A gets three line weights with a stated hierarchy. Blender equivalent: collections + SVG/vector export.

Cut 4-2, 4-4, 4-6, 4-8, 4-9, 4-10 — same lesson, different geometry type.

---

## 3. What to cut, and why

**All recursion (3-3 through 3-10, most of § 7).** The syllabus concept sequence goes lists → loops → conditionals → nested loops → grids as lists of lists. Recursion appears in none of the twelve learning outcomes. It is also the hardest thing in the source to debug, and Weeks 1–7 are AI-free.

**All OOP (§ 5).** Same reasoning, stronger.

**Data trees (2-13 to 2-15).** Grasshopper-specific with no Blender analogue. If you build the GH track, they belong there as a footnote; the Blender track teaches the same idea as nested lists.

**Connective modules (§ 6).** Genuinely good work — closest-point graphs, sorted links, max link counts. It answers a question this course does not ask.

**Subdivision variants (7-4 to 7-22, 7-26 to 7-36).** Twenty-plus examples of recursive mesh subdivision, including bitmap-driven depth control and tubular subdivision with tab faces. Module 3 permits Tissue and Box Morph outright. This much subdivision would displace the module's actual subject, which is authored variation across a tessellation.

**Keep as an appendix, not a tutorial:** 7-20 tubular subdivision and § 6's connective work are strong precedent images for the Final assignment brief — *here is a workflow worth reverse-engineering*. Show them; do not teach them.

---

## 4. Porting notes that affect every kept script

**IronPython 2 → Python 3.**
`print text` → `print(text)`. Integer division changed: `i/div` in 2-5 was float division under IronPython 2 with floats, but any `int/int` in the source now yields a float in Py3 where it previously truncated — check 4-7's `(num-i)/num*255` and 7-x index math. `range()` no longer returns a list.

**`rhinoscriptsyntax` → `bpy`: the points problem.**
ATLV's entire § 1 outputs `rs.AddPoint()` — points as document objects. Blender has no point object. Two choices, and it matters:
- **One mesh, N vertices** — fast, correct, and what 1A's *1,000+ elements* requirement demands.
- **N objects** — visible and easy to explain, but unusable past a few hundred.

Recommendation: teach the list-of-coordinates first (pure Python, no `bpy`), then a single `from_pydata()` call at the end that builds one mesh from the list. It keeps the loop readable, it scales to 1A's element count, and it makes "the list is the design, the mesh is the output" the structural lesson of the module.

**Every ATLV script hardcodes its numbers inline.** `i*0.1`, `0.05`, `threshold` buried mid-function. From Week 8 students modify their own work live, in front of the room. Give every ported script a `# ---- PARAMETERS ----` block at the top with named variables and a one-line comment on the visible effect of each. This is the single highest-value change to make across the whole port.

**Add the broken variant.** Per the materials brief, each script needs a deliberately broken twin for the failure-points slide. The good news: the ports generate them for free — the un-ported IronPython original *is* the broken variant for Tutorials 0.3 and 1.1. `print text` and the division change are real errors with real messages.

---

## 5. Coverage against the eleven tutorials

| # | Tutorial | ATLV source | Status |
|---|---|---|---|
| 0.1 | 3D Transformations | none | **Write from scratch** |
| 0.2 | CSG Operations | none | **Write from scratch** |
| 0.3 | 3D Printing Basics | none | **Write from scratch** |
| 0.3 | Python I (Wk 3 code half) | 1-1 … 1-7 | Port |
| 1.1 | Arrays | 1-8, 2-5, 1-6 | Port + write hex |
| 1.2 | Attractors | 2-4, 7-3, 7-23 | Port + write remap, curve attractor, falloff set |
| 1.3 | Toolpath Logic | none | **Write from scratch** |
| 2.1 | Contours from SDF | 2-6, 7-30/31 (partial) | Mostly write from scratch |
| 2.2 | 2D Fabrication | none | **Write from scratch** |
| 3.1 | Panelization | 2-7, 7-25 | Port + write UV remapping |
| 3.2 | Fabrication Strategies | none | **Write from scratch** |
| 4.1 | Tool Building | 2-1, 2-2, 3-1, 3-2 | Port |

**Five of eleven tutorials have no ATLV source at all** — and they are the five carrying the fabrication half of the course. ATLV is a strong reference for the language and the field logic in Modules 1 and 3. It contributes nothing to Module 0, nothing to toolpaths, nothing to sectioning for fabrication, and nothing to production planning.

Treat it as: a proven sequence for teaching Python-for-geometry to architecture students, worth following in structure, with roughly a fifth of its code worth carrying over.
