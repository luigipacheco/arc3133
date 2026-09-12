# ARC 3133 — The Vocabulary Spine

Structure v3: **Modules 0–3 are node-based. Python vocabulary is taught through the graphs. Module 4 translates that vocabulary into code.**

This document is the mechanism that makes v3 work. Without it, "teach the terms in Python terms" is an intention. With it, it is a table you can put on a slide in Week 1 and cash in during Week 12.

---

## The rule

Every node group, every operation, every component introduced in Modules 0–3 is **named twice**: once by its interface label, once by its computational term. The computational term is the one used in critique, in briefs, and in assessment.

Students will not write code until Module 4. They will be *saying* `loop`, `list`, `index`, `conditional`, and `remap` from Week 1.

---

## The table

Introduce in Module 0. Reprint at the head of every tutorial. It is the Module 4 Rosetta stone.

| Term | Geometry Nodes | Grasshopper | The code (Module 4) |
|---|---|---|---|
| **variable** | a named Group Input socket | a slider or param | `x = 0.0` |
| **list** | a geometry with N elements | a list in a param | `points = []` |
| **index** | `Index` | `List Item` | `points[3]` |
| **length** | `Domain Size` | `List Length` | `len(points)` |
| **for loop** | *implicit* — any node acting on all elements | *implicit* — any component acting on a list | `for i in range(n):` |
| **nested loop** | `Grid`, or two-axis construction | `Cross Reference`, or two ranges | `for i: for j:` |
| **range** | `Index`, `Repeat Zone` | `Series`, `Range` | `range(n)` |
| **append** | `Join Geometry` | `Merge` | `points.append(p)` |
| **if statement** | `Switch` + `Compare` | `Stream Filter`, `Dispatch` | `if condition:` |
| **filter** | `Delete Geometry`, `Separate Geometry` | `Cull Pattern`, `Dispatch` | `if test: keep` |
| **and / or** | `Boolean Math` | `Gate And`, `Gate Or` | `and`, `or` |
| **function** | a **Node Group** | a **Cluster** | `def f(x):` |
| **remap** | `Map Range` | `Remap Numbers` | `remap(v, a, b, c, d)` |
| **clamp** | `Clamp` | `Minimum` + `Maximum` | `clamp(v, lo, hi)` |
| **distance** | `Geometry Proximity`, `Vector Math → Distance` | `Distance`, `Closest Point` | `math.dist(a, b)` |
| **random** | `Random Value` (+ Seed) | `Random`, `Jitter` (+ Seed) | `random.uniform()` |
| **sort** | `Sort Elements` | `Sort List` | `sorted(items)` |
| **list of lists** | nested instances / multi-level | **Data Tree** branches | `[[...], [...]]` |
| **attribute** | `Store Named Attribute` | a list carried alongside | a value stored per item |

---

## The one thing that can break this

**Grasshopper hides the loop, and Geometry Nodes hides it too.**

This is the central risk of v3 and it is not obvious. In both environments, a component applied to a list of 500 items simply operates on all 500. There is no visible repetition. Students see one node do one thing and get 500 results.

Under the old structure that did not matter, because Module 1 made them write `for i in range(500)` by hand and the repetition was unmissable. Under v3, **nothing in the interface will ever show a student a loop.** If it is not named out loud, deliberately, every single week, they will reach Module 4 having never encountered the concept — and the whole plan collapses at exactly the point it is supposed to pay off.

Three practical defences:

1. **Say the sentence.** Every time a node is introduced: *"this is a loop — it runs once per point, and there are four hundred points."* Say it until it is boring, then keep saying it.
2. **Show the count.** Wherever possible, display the element count next to the operation. Blender's Spreadsheet editor is the best teaching surface in the course for this — the table *is* the list, and every row is one pass of the loop.
3. **Break it once per module.** Feed a component a list of 3 and a list of 500 and let students predict the output count before running it. That is the loop, made visible, in thirty seconds.

Grasshopper's Data Trees are the sharper version of the same problem: students learn to graft and flatten by superstition without ever knowing what the branches are. Name them as **lists of lists** from the first time they appear, and the Module 3 grid work becomes legible instead of magic.

---

## What Module 4 becomes

Module 4 is now the only Python in the course, and it is doing three jobs at once. It needs the room.

**4.0 — Translation.** The table above, gone through line by line. For each row: here is the node you have used for twelve weeks, here is the code that does the same thing. Students are not learning concepts here — they already have them — they are learning what the concepts look like typed out. This is the tutorial the fourteen `module1_point/` scripts already exist to serve.

**4.1 — Reading and modifying.** Given a working script, change a parameter and predict the result. Find the loop. Find the conditional. Break it deliberately and read the error. The `BREAK IT` sections in the existing scripts are built for this, and the silent failures — an out-of-range edge index, an `if` with no `else`, an unclamped remap — are the most valuable ones, because they are the failures an assistant will hand a student without warning.

**4.2 — Specifying and generating.** Pseudocode first, then generate with an assistant, then read and verify. The student's job is not to write the code; it is to know whether what came back does what they asked. That judgment is exactly what twelve weeks of naming has been building.

### Give it more time

Under v2, Module 4 was released Week 12 and due at the final review — three working weeks, when Python was already familiar from Module 1. Under v3 it is the students' first contact with code.

Recommendation: **release 4.0 in Week 10**, alongside Module 3's opening rather than after it. It is a short tutorial and it is not tied to a fabrication deadline, so it can run in the background for five weeks instead of three. Module 3's work does not compete with it — one is a node assignment, the other is reading practice.

---

## What changes in the syllabus

| Section | Change |
|---|---|
| Course Description | Five modules, four in nodes, one in code. The alternation argument is replaced by "vocabulary first, syntax last." |
| Module 1 | Same subject — point, list, field — rebuilt as a node module. Python terms are the naming convention, not the environment |
| Learning Outcome on Python | From *write Python* to **read, verify, and modify Python**, assessed in Module 4 |
| New Learning Outcome | Name the computational operation a node performs, in the terms in the table above — assessed in every module |
| Tutorial calendar | 1.0–1.3 become node tutorials; a new 4.0 Translation tutorial is added at Week 10 |
| Prohibited Shortcuts | Simplifies considerably. There is no longer a "must be written by hand" row, since nothing is written until Module 4. The constraint becomes purely the explanation requirement |
| AI policy | Weeks 1–7 AI-free still holds, but its justification changes: it protects the acquisition of the vocabulary, not of syntax |
| Materials | The fourteen Blender Python scripts move from Module 1 material to Module 4 material |

---

## Honest assessment

**This is a better fit for the course you are actually running.** One environment for twelve weeks, no syntax errors competing with fabrication deadlines, and Python arriving at the moment it becomes useful rather than four weeks before it is needed again.

It also makes the AI module coherent for the first time. "Vibe coding" only works if you can audit the output, and auditing requires vocabulary, not syntax. A student who has spent twelve weeks saying *this node is a loop over four hundred points* can read a generated `for` statement and tell whether it is doing the right thing. A student who spent those weeks memorising `bpy` calls often cannot.

**The cost is that everything now rests on naming discipline.** Under the old structure, Module 1 forced the vocabulary in whether or not anyone named it well — you cannot write a loop without meeting a loop. Under v3 the interface will happily let a student go the whole semester without ever noticing one. The table above has to be live in every session, or Module 4 arrives and there is nothing to translate.
