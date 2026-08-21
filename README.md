# ARC 3133 — Architectural Visualization Methods 1

Course site for ARC 3133 at Florida Atlantic University, School of Architecture.

Built with [Course in a Box](https://howto.p2pu.org/) by P2PU — a Jekyll template for open online courses.

## Structure

```
_data/course.yml          site title + module list (drives the nav)
index.md                  landing page
modules/classes/_posts/   one page per class session
modules/assignments/_posts/
modules/tutorials/_posts/
modules/resources/_posts/
slides/                   class decks (pptx + pdf)
```

Every page in `modules/` is a post. File names are `YYYY-MM-DD-name.md`; the date
controls the order within the module, not the publication date.

## Running locally

```bash
bundle install
bundle exec jekyll serve
```

## Licence

Course content CC BY-SA 4.0 unless noted. Template © P2PU.
