# ARC 3133 — Architectural Visualization Methods 1

Course site and material archive for ARC 3133 at Florida Atlantic University,
School of Architecture. Fall 2026. Instructor: Luis Pacheco Alcalá.

Built with [Course in a Box](https://howto.p2pu.org/) by P2PU — a Jekyll template
for open online courses.

## What is in here

```
syllabus/                 the syllabus, source of truth — full and student cuts
  archive/                superseded versions
reference/                module structure rationale, vocabulary spine, audits
slides/                   class decks, pptx and pdf
  src/                    python-pptx generators — nb.py is the shared style kit
code/blender/             tested Blender Python teaching scripts
  sverchok/               SNLite versions of the same
files/                    Blender and Grasshopper working files
modules/                  the site itself — one page per class, assignment,
                          tutorial and resource
_data/course.yml          site title + module list, drives the nav
index.md                  landing page
```

Everything under `modules/` is a Jekyll post. File names are `YYYY-MM-DD-name.md`;
the date controls the order within the module, not the publication date.
`syllabus/`, `reference/`, `code/` and `slides/src/` are excluded from the built
site — they live here so the course has one backup, not because they are pages.

## Course structure

Five modules, alternating environment, each with a fabrication mode that matches
its computational subject.

| M | Subject | Fabrication |
|---|---|---|
| 1 | Transformations and CSG | small print |
| 2 | Lists, mesh construction, arrays | — |
| 3 | Fields and attractors | plotter |
| 4 | Tessellation and panelization | multi-part print |
| 5 | SDF, volume, section and light | laser cutting |
| — | Translating a graph to Python | extra credit |

## Rebuilding a deck

```bash
cd slides/src
python3 class04.py            # writes ../ARC3133_Class04.pptx
python3 class03_patch.py      # appends to base/ARC3133_Class03_base.pptx
```

`nb.py` holds the palette, card geometry and compound blocks the decks are built
from. `class03_patch.py` must always read from `base/` — never from its own
output, which would append the added slides twice.

## Running the site locally

```bash
bundle install
bundle exec jekyll serve
```

## Licence

Course content CC BY-SA 4.0 unless noted. Template © P2PU.
