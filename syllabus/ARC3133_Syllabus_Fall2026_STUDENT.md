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

Architectural Visualization Methods 1 explores computational design thinking — algorithmic methods and parametric principles — for architectural representation, with an emphasis on procedural processes and the visual communication of design intentions.

The course runs in five modules. The first four are built in node graphs (Blender Geometry Nodes or Grasshopper); the last is written in Python with coding assistance.

| Module | Subject | Fabrication | Output |
|---|---|---|---|
| **0** | Foundations — parametric modeling, booleans | Additive, introductory | Small print |
| **1** | POINT — lists, arrays, and fields | Computer-controlled motion | Plotter drawing |
| **2** | LINE — section and sequence | Computer-controlled cutting | Sectional assembly |
| **3** | PLANE — modularity and tessellation | Additive manufacturing | Vault or façade fragment |
| **4** | TOOL — AI-assisted tool building | — | The tool |

Modules 1, 2, and 3 each have two assignments: a **digital visualization assignment** producing a sheet, and a **physical fabrication assignment** producing an object. Visualization is the primary emphasis — composition, color, hierarchy, line weight, rendering, and post-processing are what the sheets are assessed on.

For the first ten weeks you work in a node graph, and every operation is named twice: once by its interface label, once by its computational term. Module 4 shows you what those terms look like as code, so that the work there is reading and verifying rather than writing from scratch.

**Choose Blender or Rhino in Week 1 and stay there.** Every tutorial ships in both.

---

## Course Learning Outcomes

By the end of the course, students will be able to:

| # | Outcome | Assessed In |
|---|---|---|
| 1 | Produce architectural graphics of professional visual quality using computational methods | 1.1, 2.1, 3.1, Booklet |
| 2 | Build and modify a parametric graph — connect nodes, expose inputs, change an upstream parameter and predict the downstream result | 0.1, 2.1, 3.1 |
| 3 | Construct and modify solid geometry through Boolean operations and transformations, non-destructively | 0.1, 3.2 |
| 4 | Read, verify, and modify Python — locate the loop, the conditional, and the function in a script; recognise generated code that does not do what was asked | 4.1 |
| 5 | Name the computational operation a node performs — which operation repeats, over what collection, producing what | Every module |
| 6 | Recognise the same logic in a graph and in code, and reimplement a system from one in the other | 2.1, 4.1 |
| 7 | Generate and control point fields, sections, patterns, and differentiated surfaces | 1.1, 2.1, 3.1 |
| 8 | Decompose a geometric problem into an explicit sequence of steps, expressed as pseudocode | 4.1; all modules |
| 9 | Prepare geometry correctly for computer-controlled drawing, cutting, and additive manufacturing | 1.2, 2.2, 3.2 |
| 10 | Evaluate and account for material and machine constraints — ordering, kerf, tolerance, manifold geometry, orientation | 1.2, 2.2, 3.2 |
| 11 | Assemble a fabricated system from computationally generated components | 2.2, 3.2 |
| 12 | Plan a multi-part fabrication run against machine, time, and material constraints | 3.2 |
| 13 | Analyze point, line, and plane as simultaneously graphic, spatial, and computational systems | Modules 1–3 |
| 14 | Develop and consistently apply a personal visual identity across a body of work | VIM, Booklet |
| 15 | Communicate computational and fabrication processes through diagrams, documentation photography, and annotation | All fabrication assignments, Booklet |
| 16 | Independently learn an unfamiliar computational workflow, extract its logic, and rebuild it as a reusable tool | 4.1 |

---

## Software and Materials

| Purpose | Environment |
|---|---|
| Application environment | Blender — Geometry Nodes (Modules 0–3), Python (Module 4). Free and cross-platform |
| Application environment | Rhino + Grasshopper (Modules 0–3), Grasshopper Python (Module 4). Student license |
| Layout and post-processing | Adobe Illustrator, Photoshop, InDesign. Open-source equivalents accepted: Inkscape, GIMP, Scribus |
| Slicing | PrusaSlicer, Cura, or FabLab-specified slicer |
| Plotter / cutting preparation | As specified by the FabLab |

**Template-based design tools are not permitted.** Canva, Adobe Express, Figma templates, PowerPoint, Google Slides, Wix, and similar applications may not be used to produce any sheet, the Visual Identity Manual, or the Booklet. Work in a vector or raster editor.

### Materials

Consumable materials are supplied by the School, subject to these limits. Test cuts and failed prints count against your allocation.

| Module | Supplied | Allocation |
|---|---|---|
| 0 | Filament | One print, 200 g |
| 1 | Paper and pens | 3 sheets, 1 pen |
| 2 | Chipboard, basswood, or acrylic | 1 sheet |
| 3 | Filament | `[CONFIRM]` |

Students supply their own storage media and are responsible for their own file backups.
---

## How the Course Runs

Every class does three things, in this order:

1. **Pin-up and critique** of the assignment due today
2. **Tutorial review** — questions and troubleshooting. Bring the file, not a description of the problem
3. **Assignment briefing** for the work due in two weeks

The next tutorial is released immediately after class. Every assignment therefore has two weeks: one to watch the tutorial and try it, one to make the work after the brief. **Tutorials are watched before the class that discusses them.**

Because the course meets once per week, expect a minimum of six hours of out-of-class work per week, including tutorial time.

---

## Assignments

| # | Assignment | Briefed | Due |
|---|---|---|---|
| **VIM** | Visual Identity Manual — 8+ page PDF defining logo, palette, typography, line weights, grid, and tabloid template | Week 1 | Week 8, with the Midterm |
| **0.1** | Parametric Massing Sequence — a boolean operation graph, documented as an axonometric series and a final isometric | Week 2 | Week 4 |
| **0.2** | First Print — the 0.1 massing prepared and printed. Manifold geometry, orientation diagram, **no supports permitted** | Week 3 | Week 5 · print presented at Midterm |
| **1.1** | POINT: Tiling + Arrays — one simple tile designed from a facade precedent, laid out with three arrays of your choosing from cartesian, radial, hexagonal, along a curve; 1,000+ elements in one composition | Week 4 | Week 6 |
| **1.2** | POINT: Site Analysis Fields — attractor fields built and read in 2D, then applied to a site imported as a point cloud to diagram one measured site condition. Two studies | Week 5 | Week 8 |
| **2.1** | LINE: Section + Light — a sectioned system rendered for material, light, and filtering. 20+ serial sections | Week 9 | Week 11 |
| **2.2** | LINE: Section-Based Fabrication — laser-cut sectional assembly with a designed registration system. 12+ sections | Week 10 | Week 12 |
| **3.1** | PLANE: Surface + Filtering — a panelized vault or façade, 400+ cells, variation authored | Week 11 | Week 13 |
| **3.2** | PLANE: Additive Fabrication — 9+ printed panels forming a continuous assembly, plus a production plan | Week 12 | Final Review |
| **4.1** | TOOL: Reverse-Engineer a Workflow — study a workflow, extract its logic as pseudocode, build your own tool with named inputs | Week 12 | Final Review |

Full requirements for each assignment are issued at the briefing and posted to Canvas.

**Fabrication scope limits.** Work exceeding these will not be scheduled on the machines.

- **0.2** — maximum bounding box 60 mm; draft layer height; no supports
- **1.2** — maximum drawing size tabloid; maximum plot time 20 minutes
- **2.2** — maximum assembled bounding box 300 mm; maximum 1 sheet
- **3.2** — maximum assembled volume 300 mm; maximum print time `[TBD]`

### FabLab Access

The **FabLab Safety Orientation must be completed to gain access to any part of the FabLab.** Enroll at `https://canvas.fau.edu/enroll/JEW9J6` `[CONFIRM link]`. **Completion is due by the end of Week 2 (Sep 1).** Students who have not completed it cannot begin fabrication work and remain responsible for the deadlines.

---

## Midterm Review — Week 8, Oct 13

Students print and present all work completed to date, in its latest revised form: the Visual Identity Manual, 0.1, 0.2 (sheet and print), 1.1, and 1.2. **The printed set is what is reviewed. Work shown on a screen is not assessed.**

The midterm does not re-grade individual assignments. It assesses revision in response to critique (40%), coherence of the visual identity across the set (30%), and quality of print, layout, and documentation (30%).

---

## Final Submission

Due at the Final Review, Dec 10–16:

- **3.2** printed assembly · **4.1** two sheets and the tool file
- **Final Booklet** (PDF) — all assignments in their latest revised form, documented with photography, diagrams, and captions, at 17" × 11". Assessed on revision in response to critique (40%), quality of documentation (35%), and coherence of the visual identity (25%)
- **Visual Identity Manual** (PDF) — revised from the Week 4 version

An ungraded booklet progress check is held in Week 12.

---

## Prohibited Tools

**A tool that automates the concept an assignment exists to teach may not be used in that assignment — until you can say what it does.**

| Assignment | Prohibited |
|---|---|
| All sheets, VIM, Booklet | Canva, Adobe Express, template-driven layout apps, PowerPoint, Google Slides |
| 0.1 | Imported or downloaded models; any geometry not generated in-session |
| 1.1 / 1.2 | Array add-ons, scatter and distribution tools, preset attractor falloff plugins |
| 3.1 / 3.2 | Preset gradient, attractor, and variation components — the differentiation must be authored. Panelization libraries are permitted |
| All Grasshopper work | The Cross Reference component may be used once per definition |

**The explanation requirement.** From Module 2 onward, supplied and third-party node groups are permitted, on one condition: you must be able to state what a group does — which operation repeats, over what collection, producing what output. A student who cannot do so for a group they used receives **no credit for Computational Understanding** on that assignment. This is tested at pin-up.

Use of a prohibited tool is assessed as a failure to meet Assignment Requirements for that submission.
---

## Course Evaluation Method

| Item | Weight |
|---|---|
| VIM — Visual Identity Manual | 7% |
| 0.1 — Parametric Massing Sequence | 7% |
| 0.2 — First Print | 7% |
| 1.1 — POINT: Tiling + Arrays | 7% |
| 1.2 — POINT: Site Analysis Fields | 7% |
| 2.1 — LINE: Section + Light | 7% |
| 2.2 — LINE: Section-Based Fabrication | 7% |
| 3.1 — PLANE: Surface + Filtering | 7% |
| 3.2 — PLANE: Additive Fabrication | 7% |
| Midterm Review (Oct 13) | 8% |
| 4.1 — TOOL: Reverse-Engineer a Workflow | 13% |
| Final Booklet | 11% |
| Attendance and participation | 5% |
| **Total** | **100%** |

### Evaluation Criteria

| Criterion | Digital (VIM, 0.1, 1.1, 2.1, 3.1, 4.1) | Fabrication (0.2, 1.2, 2.2, 3.2) |
|---|---|---|
| **Visual Quality** — composition, hierarchy, contrast, color, typography, line weight, graphic impact | 35% | 20% |
| **Computational Understanding** — assessed through live modification of your own work at pin-up, and through explanation of any node group you used | 25% | 20% |
| **Technical Execution** — competent use of modeling, visualization, and computational workflows | 20% | 15% |
| **Fabrication Quality** — geometry preparation, material and machine constraints, assembly, craft | — | 30% |
| **Creativity + Experimentation** | 10% | 5% |
| **Requirements + Visual Identity** | 10% | 10% |

### Performance Levels

| Level | Range | Description |
|---|---|---|
| Exemplary | 94–100 | Meets all requirements; the work is visually distinctive and technically assured; the student can explain and defend every procedural decision; evident iteration beyond the assigned minimum |
| Proficient | 83–93 | Meets all requirements competently; procedural logic is understood and explicable; visual and technical execution is solid with minor lapses |
| Developing | 70–82 | Requirements partially met; procedural logic is applied but incompletely understood; visual or technical execution is inconsistent |
| Insufficient | Below 70 | Requirements substantially unmet; the student cannot account for the logic of their own work; execution does not meet the assignment's stated constraints |

### Grading Scale

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

## Schedule

Class meets Tuesdays, 5:00–7:50 PM.

| Date | |
|---|---|
| Aug 22 | Classes begin |
| Oct 5–9 | Midterm Studio Reviews — no due dates in this course |
| Oct 12–16 | Midterm Review falls here |
| Oct 30 | Last day to drop with a "W" |
| Nov 25–29 | Thanksgiving break |
| Dec 1–4 | Final Studio Reviews — no due dates in this course |
| Dec 10–16 | Final Review |

| Wk | Date | Due today | Briefed today |
|---|---|---|---|
| **1** | Aug 25 | — | Syllabus and course structure. **Visual Identity Manual** |
| **2** | Sep 1 | — | **0.1 Parametric Massing Sequence** |
| **3** | Sep 8 | — | **0.2 First Print.** *Printer queue opens* |
| **4** | Sep 15 | **0.1** | **1.1 Tiling + Arrays** |
| **5** | Sep 22 | **0.2** file + sheet | **1.2 Fields + Toolpath**, stage 1 |
| **6** | Sep 29 | **1.1** · 1.2 field study reviewed | 1.2 stage 2 |
| **7** | Oct 6 | — | Plotter production session. *Nothing due* |
| **8** | Oct 13 | **MIDTERM · VIM · 1.2 · 0.2 print** | Module 2 opens |
| **9** | Oct 20 | — | **2.1 Section + Light** |
| **10** | Oct 27 | — | **2.2 Section-Based Fabrication** |
| **11** | Nov 3 | **2.1** | **3.1 Surface + Filtering.** Laser production |
| **12** | Nov 10 | **2.2** | **3.2 Additive Fabrication · 4.1 TOOL.** Booklet check |
| **13** | Nov 17 | **3.1** · 3.2 production plan | *Print queue closes end of week* |
| **14** | Nov 24 | **4.1 proposal** | Print production. Final desk crits |
| **15** | Dec 1 | — | Final desk crits and booklet review. *Nothing due* |
| **—** | Dec 10–16 | **3.2 · 4.1 · Booklet · VIM** | **FINAL REVIEW** `[CONFIRM exam slot]` |

Two deadlines sit outside the two-week rhythm. **0.2**'s file and sheet are due Week 5, but the printed object is presented at the Week 8 midterm, because the queue has latency. **1.2** runs three weeks, because the second tutorial is released only after the field study has been reviewed.
---

## Required Texts / Materials

**No required textbook.** Course material is delivered through pre-recorded tutorials, in-class demonstration, and distributed files. Students should bookmark the Blender Geometry Nodes documentation or the Grasshopper primer for their chosen environment.

### Recommended Readings

- **Point and Line to Plane** — Wassily Kandinsky (Dover)
- **Elements of Parametric Design** — Robert Woodbury · Routledge, 2010 · ISBN 978-0415779876
- **AAD Algorithms-Aided Design: Parametric Strategies using Grasshopper** — Arturo Tedeschi · Le Penseur · ISBN 978-8895315300
- **Advanced 3D Printing with Grasshopper®: Clay and FDM** — Diego García Cuevas and Gianluca Pugliese · 2020 · ISBN 9798635379011
- **Drawing Architecture** — Neil Spiller (Ed.) · Wiley, 2013 · ISBN 978-1118418796
- **Drawing: The Motive Force of Architecture** — Peter Cook · Wiley, 2014 · ISBN 978-1118700648
- **Drawing Futures** — Migayrou, Sheil, Allen, Pearson (Eds.) · Riverside Architectural Press, 2016 · ISBN 978-1988366043
- **Bartlett Designs: Speculating with Architecture** — Iain Borden (Ed.) · Wiley, 2009 · ISBN 978-0470772805
- **Speculative Coolness** — Bryan Cantley · Routledge, 2023 · ISBN 978-1032318868

### Contemporary Practitioners

Working practitioners publishing continuously — treat these as a live feed rather than a fixed bibliography. A module-specific reference set is distributed at the start of each module.

| Reference | Relevant to |
|---|---|
| [@mmnksr](https://www.instagram.com/mmnksr/) | Modules 1–2 — point clouds and sections |
| [@mantissa.xyz](https://www.instagram.com/mantissa.xyz/) | Modules 1–2 — a useful read against @mmnksr |
| [@saul_kim_](https://www.instagram.com/saul_kim_/) | All modules — restraint and line weight |
| [@facadepot](https://www.instagram.com/facadepot/) | Module 3 — modular façades |
## Artificial Intelligence Preamble

FAU recognizes the value of generative AI in facilitating learning. However, output generated by artificial intelligence (AI) — written words, computations, code, artwork, images, music, and so on — is drawn from previously published materials and is not your own original work.

FAU students are not permitted to use AI for any course work unless explicitly allowed to do so by the instructor of the class for a specific assignment. [Policy 12.16 Artificial Intelligence]

Class policies related to AI use are decided by the individual faculty. Some faculty may permit the use of AI in some assignments but not others, and some faculty may prohibit the use of AI in their course entirely. In the case that an instructor permits the use of AI for some assignments, the assignment instructions will indicate when and how the use of AI is permitted in that specific assignment. It is the student's responsibility to comply with the instructor's expectations for each assignment in each course. When AI is authorized, the student is also responsible and accountable for the content of the work. AI may generate inaccurate, false, or exaggerated information. Users should approach any generated content with skepticism and review any information generated by AI before using generated content as-is.

If you are unclear about whether or not the use of AI is permitted, ask your instructor before starting the assignment.

Failure to comply with the requirements related to the use of AI may constitute a violation of the Florida Atlantic Code of Academic Integrity, Regulation 4.001.

**Proper Citation:** If the use of AI is permitted for a specific assignment, then use of the AI tool must be properly documented and cited. For more information on how to properly cite the use of AI tools, visit https://fau.edu/ai/citation


---

## AI Language Specific To This Course

**Weeks 1 through 7 — AI-free.** No AI assistance of any kind in producing coursework through the Week 8 Midterm. This covers the Visual Identity Manual, 0.1, 0.2, 1.1, and 1.2.

Permitted at any stage: asking an AI to explain a computational concept, clarify syntax, or interpret an error message. Not permitted: asking it to write, complete, or fix your work.

**Week 8 onward — coding assistance permitted, with disclosure.** In practice this matters from Module 4, which is where code appears. Subject to:

- **Pseudocode first.** Your own written decomposition of the problem must precede any code generation and is submitted alongside it. AI-generated pseudocode submitted as your own reasoning is a violation.
- **Full disclosure.** Tool and version, the prompts used, what was kept, what was changed. Citation follows https://fau.edu/ai/citation.
- **Live modification** (below).

**Not permitted at any stage:** generative image models — Midjourney, Stable Diffusion, DALL·E, Firefly, or any diffusion-based tool — to produce, extend, or modify any image submitted as coursework, including backgrounds, textures, entourage, generative fill, and AI upscaling. Also not permitted: AI generation of the visual identity system, including logo, palette, and layout.

In 1.1, 2.1, and 3.1 the assessed outcome *is the image*; delegating its production removes the judgment the assignment exists to develop.

### Live Modification

At every pin-up from Week 8 onward, each student makes **one unscripted change to their own work in front of the class** — reverse a section order, alter an attractor's falloff, add a conditional, change a mapping range. Roughly ninety seconds.

It is paired with a shorter question: **name a node or group in your definition and say what it does.** About thirty seconds.

This, rather than a written explanation, is the primary assessment of Computational Understanding. **A student who cannot modify their own submitted work, or cannot account for a component in it, receives no credit for Computational Understanding on that assignment**, regardless of whether the work runs or how it looks. Where the work is demonstrably not the student's own, this may constitute a violation of Regulation 4.001.

### Accountability

Students are responsible for the accuracy and behavior of any AI-assisted output they submit. AI may generate geometry that is subtly wrong — non-manifold meshes, inverted normals, off-by-one indexing in a toolpath — and these reach the machines. Verification is the student's obligation, not the tool's.
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
