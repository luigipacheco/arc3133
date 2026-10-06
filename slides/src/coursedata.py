# -*- coding: utf-8 -*-
"""Read syllabus/course.yml so the decks never drift from the site.

Every date, weight, requirement and unit step on a slide comes from here.
Only the teaching slides are hand-authored.
"""
import os, io, yaml, datetime

_CANDIDATES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "syllabus", "course.yml"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "course.yml"),
    "/mnt/user-data/uploads/arc3133/syllabus/course.yml",
]

def _load():
    for p in _CANDIDATES:
        if os.path.exists(p):
            return yaml.safe_load(io.open(p, encoding="utf-8")), os.path.abspath(p)
    raise SystemExit("course.yml not found; looked in:\n  " + "\n  ".join(_CANDIDATES))

DATA, PATH = _load()

def require_current_deck(week_number):
    review = next(r for r in DATA["presentation_review"] if r["week"] == week_number)
    if review["status"] != "current" and os.environ.get("DECK_REVIEW_DRAFT") != "1":
        raise SystemExit("This deck needs editorial revision for the current assignment sequence. Revise it first; use DECK_REVIEW_DRAFT=1 only to render a review draft.")

COURSE   = DATA["course"]
UNITS    = {u["id"]: u for u in DATA["units"]}
PROJECTS = {p["id"]: p for p in DATA["projects"]}
WEEKS    = {w["week"]: dict(w) for w in DATA["weeks"]}
# Week titles and units live on the teaching blocks, not on the dated weeks.
BLOCKS   = {}
for _b in DATA.get("teaching_sequence", []):
    for _n in _b["weeks"]:
        WEEKS[_n].setdefault("title", _b["focus"])
        WEEKS[_n].setdefault("units", list(_b["units"]))
        BLOCKS[_n] = _b

MILESTONES = {}
for _p in DATA["projects"]:
    for _m in _p["milestones"]:
        _m = dict(_m); _m["project"] = _p["id"]; _m["project_title"] = _p["title"]
        MILESTONES[_m["id"]] = _m
for _a in DATA.get("assessments", []):
    _a = dict(_a); _a.setdefault("project", None)
    MILESTONES.setdefault(_a["id"], _a)


# ── dates ──────────────────────────────────────────────────────────────
def _d(week):
    w = WEEKS.get(week)
    if not w:
        return None
    v = w["date"]
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v))

def date_short(week):
    """'SEP 15' — for the title slide kicker."""
    d = _d(week)
    return d.strftime("%b %d").upper().replace(" 0", " ") if d else ""

def date_long(week):
    """'Week 4 — Sep 15' — matches the site's phrasing."""
    d = _d(week)
    return "WEEK %d — %s" % (week, d.strftime("%b %d").replace(" 0", " ")) if d else "WEEK %d" % week


# ── lookups ────────────────────────────────────────────────────────────
def week(n):
    return WEEKS[n]

def unit(uid):
    return UNITS[uid]

def milestone(mid):
    return MILESTONES[mid]

def due_line(mid):
    """'DUE WEEK 8 — OCT 13   /   7%' for the ISSUED slide."""
    m = MILESTONES[mid]
    due = m.get("due")
    if m.get("due_date"):
        d = "DUE " + due_label(mid).upper()
    elif isinstance(due, int):
        d = "DUE " + date_long(due)
    else:
        d = "DUE " + str(due).upper()
    w = m.get("weight")
    return d + ("   /   %d%%" % w if w else "")

def due_label(mid):
    """'Sun Oct 18, 11:59 PM' when a deadline falls between classes; otherwise 'Week 9 — Oct 20'."""
    m = MILESTONES[mid]
    if m.get("due_date"):
        d = datetime.date.fromisoformat(str(m["due_date"]))
        out = "%s %s %d" % (d.strftime("%a"), d.strftime("%b"), d.day)
        if m.get("due_time"):
            h, mi = map(int, m["due_time"].split(":"))
            out += ", %d:%02d %s" % (h % 12 or 12, mi, "PM" if h >= 12 else "AM")
        return out
    return date_long(m["due"]).title() if isinstance(m.get("due"), int) else str(m.get("due"))

def requirements(mid):
    return list(MILESTONES[mid].get("requirements", []))

def checkpoints(mid):
    return [(c["week"], c["text"]) for c in MILESTONES[mid].get("checkpoints", [])]

def steps(uid):
    return list(UNITS[uid].get("steps", []))

def vocab(uid):
    return list(UNITS[uid].get("vocabulary", []))

def milestones_due(week_n):
    return [m for m in MILESTONES.values() if m.get("due") == week_n]

def milestones_released(week_n):
    return [m for m in MILESTONES.values() if m.get("release") == week_n]


def banner_for(week_n):
    """Footer strip for a title slide: what is due and what is issued today."""
    due = sorted(m["id"] for m in milestones_due(week_n))
    rel = sorted(m["id"] for m in milestones_released(week_n))
    bits = []
    if due:
        bits.append("%s DUE TODAY" % " + ".join(due))
    if rel:
        bits.append("%s ISSUED TODAY" % " + ".join(rel))
    return "  /  ".join(bits)


if __name__ == "__main__":
    print("course.yml:", PATH)
    print("revision:", DATA.get("revision"), "|", DATA.get("status"))
    for n in sorted(WEEKS):
        w = WEEKS[n]
        print("W%-2d %s  %-38s units=%s  %s" % (
            n, date_short(n), w["title"], ",".join(w["units"]), banner_for(n)))
