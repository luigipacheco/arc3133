---
title: Final · Build a Tool That Iterates
published: true
---

**Due at the Final Review · 15%** · Generative

The semester closes on the third paradigm. Modules 1–3 built parametric systems: change an input, get a different result. A **generative** system does something a parametric one cannot — it reads its own output and uses it to decide what happens next. Form emerges from iteration rather than being specified in advance.

The mechanism is always the same: a state, a rule applied to that state, and the result becoming the next state.

| Family | What iterates |
|---|---|
| **Growth systems** | A structure extends from its own tips — L-systems, space colonization, diffusion-limited aggregation |
| **Agents** | Individuals move and respond to neighbours or environment; the trail is the drawing |
| **Cellular automata** | A grid updates each cell from the state of its neighbours |
| **Relaxation** | A configuration adjusts repeatedly toward equilibrium — packing, physics, form-finding |

## Three stages

### 1 — Study

Find a workflow that interests you: a tutorial, a shared definition, a published paper, an existing add-on. Grasshopper, Blender Geometry Nodes, Houdini, TouchDesigner, Processing, Three.js — environments beyond the ones used this semester are deliberately permitted. Follow it until it works and you understand why.

### 2 — Extract

Write the logic as **pseudocode in your own words**, independent of the original's interface. Not "plug the Populate 2D into the Voronoi" but what the procedure actually does, step by step, in language that would survive being carried to a different platform.

This is the pivot of the assignment. Separating a procedure from the software that happened to express it is the single most transferable skill in the course.

### 3 — Build

Implement that logic as **your own tool** — a Python script, a Grasshopper definition, a Blender node group — with named inputs a user can change.

**The tool must iterate.** It must contain a loop in which the output of one step becomes the input of the next, and the number of steps must be one of its exposed inputs. A system that evaluates a formula once, however complex, is parametric rather than generative and does not meet this requirement.

Your tool must do something the original did not — but the substantive requirement is the loop, not novelty for its own sake. A working iterative system that you built, can explain and can alter is the standard.

## Deliverable — two sheets

| Sheet | Content |
|---|---|
| **1 — Process** | The original (screenshot and link), your pseudocode, a diagram of the extracted logic, the original's result reproduced. Answers *how did you get from their thing to yours* |
| **2 — Tool** | The tool itself with inputs labelled, and at least three outputs produced by varying those inputs. **One output shown as a sequence of iteration states**, so the loop is visible. Answers *what does it do* |

Plus the tool file, submitted with the Booklet materials.

The three-output requirement is how a tool proves it is a tool. One image proves nothing.

## Live demonstration

At the final review you will run your tool with inputs you have not prepared in advance. A student who cannot explain or operate their own tool receives no credit for Computational Understanding, regardless of whether it runs.

## References

Craig Reynolds, *Boids* (1986) · John Conway, *Game of Life* (1970) · Casey Reas, *Process* series · Aristid Lindenmayer, L-systems · Daniel Shiffman, [*The Nature of Code*](https://natureofcode.com/)

