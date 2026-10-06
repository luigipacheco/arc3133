# -*- coding: utf-8 -*-
"""Slides whose content comes from course.yml — built once, used by every deck."""
from nb import *
import coursedata as C
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Pt

ACCENTS = [CYAN, LIME, YELLOW, PINK]


def title_slide(d, week_n, big_lines, left_tag, bg=LIME, lfill=PINK, rfill=CYAN,
                right_tag=None, foot=None):
    """Kicker, date and the due/issued footer all come from the YAML."""
    s = d.slide(bg)
    w = C.week(week_n)
    units = " + ".join(w.get("units", []))
    kicker = "CLASS %02d  /  %s%s" % (week_n, C.date_short(week_n),
                                      ("  /  " + units) if units else "")
    if right_tag is None:
        due = sorted(m["id"] for m in C.milestones_due(week_n))
        right_tag = ("%s DUE" % " + ".join(due)) if due else "NOTHING DUE"
    if foot is None:
        rel = sorted(m["id"] for m in C.milestones_released(week_n))
        foot = ("%s ISSUED TODAY" % " + ".join(rel)) if rel else w["title"].upper()
    s.title_slide(kicker, big_lines, left_tag, right_tag, foot, lfill=lfill, rfill=rfill)
    return s


def issued_slide(d, mid, blurb=None, badge="ISSUED TODAY", badgefill=YELLOW, cards=None):
    """1.x brief header, straight from the milestone record."""
    m = C.milestone(mid)
    s = d.slide(BLACK)
    s.issued(badge,
             "%s — %s" % (mid, m["title"].upper()),
             C.due_line(mid),
             blurb or m.get("project_title", ""),
             badgefill=badgefill)
    if cards:
        x = L
        wd = (W - 0.23 * (len(cards) - 1)) / len(cards)
        for i, (tag, ttl, body) in enumerate(cards):
            col = ACCENTS[i % len(ACCENTS)]
            s.chip(x, 3.95, wd, 0.45, tag, fill=col, size=11)
            s.card(x, 4.5, wd, 1.6, fill=CREAM)
            s.t(x + 0.28, 4.68, wd - 0.56, 0.35, [s.Ab(ttl, 14)])
            s.t(x + 0.28, 5.1, wd - 0.56, 0.9, [s.Cb(body, 12.5)], ls=1.25)
            x += wd + 0.23
    return s


def _requirement_type(reqs):
    """Row height and type size for a list of requirements, and whether the longest fits."""
    n = len(reqs)
    top, gap = 1.95, 0.16
    h = min(1.05, (6.55 - top - gap * (n - 1)) / n)
    # keep long requirements inside their row: ~95 characters per line at 13pt,
    # and a row fits h / 0.22 lines. Shrink the type rather than clip the text.
    longest = max((len(r) for r in reqs), default=0)
    fits = lambda sz: (longest / (95 * 13.0 / sz)) <= int(h / (0.225 * sz / 13.0))
    size = 13.0
    while size > 9.5 and not fits(size):
        size -= 0.5
    return h, size, fits(size)


def requirements_slide(d, mid, sub="Counting these earns a C. The rest is judgement.",
                       extra=None, title=None, _reqs=None, _start=0, _last=True):
    """One numbered row per requirement, wrapped. Text is verbatim from course.yml.
    When the list cannot fit on one slide even at the smallest type, it continues on a second."""
    reqs = _reqs if _reqs is not None else C.requirements(mid) + list(extra or [])
    h, size, ok = _requirement_type(reqs)
    if not ok and _reqs is None and len(reqs) > 3:
        half = (len(reqs) + 1) // 2
        base = title or ("REQUIREMENTS — %s" % mid)
        requirements_slide(d, mid, sub, title=base + "  ·  1/2", _reqs=reqs[:half], _start=0, _last=False)
        return requirements_slide(d, mid, sub, title=base + "  ·  2/2", _reqs=reqs[half:], _start=half)
    s = d.slide(CREAM)
    s.header(title or ("REQUIREMENTS — %s" % mid), sub)
    gap = 0.16
    y = 1.95
    for i, r in enumerate(reqs):
        col = ACCENTS[(i + _start) % len(ACCENTS)]
        s.chip(L, y, 0.85, h, "%02d" % (i + 1 + _start), fill=col, size=15)
        s.card(L + 1.15, y, W - 1.15, h, fill=CREAM)
        s.t(L + 1.45, y + 0.1, W - 1.75, h - 0.2, [s.Cb(r, size)], ls=1.25,
            anchor=MSO_ANCHOR.MIDDLE)
        y += h + gap
    if not _last:
        return s
    cps = C.checkpoints(mid)
    if cps:
        wk, txt = cps[0]
        s.banner(min(y + 0.06, 6.78),
                 "CHECKPOINT · %s — %s" % (C.date_long(wk), txt),
                 fill=PINK, h=0.56, size=11.5)
    return s


def now_slide(d, title, sub, rows, closer=None, bg=CYAN, closer_color=None):
    s = d.slide(bg)
    s.header(title)
    s.t(L, 1.85, 11.5, 0.4, [s.Cb(sub, 16)])
    y, h = 2.5, 0.62
    step = 0.78 if len(rows) <= 5 else 0.70
    for r in rows:
        s.checkrow(y, r, h=h)
        y += step
    if closer:
        s.card(L, min(y + 0.1, 6.5), 9.2, 0.62, fill=BLACK)
        s.t(L, min(y + 0.1, 6.5), 9.2, 0.62,
            [s.Ab(closer, 13, closer_color or bg)],
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return s


def before_next_slide(d, rows):
    s = d.slide(CREAM)
    s.header("BEFORE NEXT CLASS")
    y = 1.95
    for i, (label, body) in enumerate(rows):
        s.actionrow(y, label, body, fill=ACCENTS[i % len(ACCENTS)])
        y += 1.16
    return s


def unit_steps_slide(d, uid, title=None, sub=None, bg=BLACK, n=None):
    """The unit's own numbered steps, verbatim."""
    u = C.unit(uid)
    st = C.steps(uid)
    if n:
        st = st[n[0]:n[1]]
    s = d.slide(bg)
    s.header(title or u["title"].upper(), sub or u["goal"])
    top, gap = 2.0, 0.14
    h = min(1.0, (6.4 - top - gap * (len(st) - 1)) / len(st))
    y = top
    for i, step in enumerate(st):
        s.chip(L, y, 0.85, h, "%02d" % (i + 1), fill=ACCENTS[i % len(ACCENTS)], size=15)
        s.card(L + 1.15, y, W - 1.15, h, fill=CREAM)
        s.t(L + 1.45, y + 0.1, W - 1.75, h - 0.2, [s.Cb(step, 12.5)], ls=1.2,
            anchor=MSO_ANCHOR.MIDDLE)
        y += h + gap
    return s


def vocab_strip(s, uid, y=6.55, label="VOCABULARY"):
    """The unit's vocabulary along the bottom — the words they must be saying."""
    words = C.vocab(uid)
    s.t(L, y, 1.6, 0.3, [s.A(label, 10, MUTE if s.dark else GREY)])
    s.t(L + 1.7, y, W - 1.7, 0.3,
        [s.A(" · ".join(w for w in words), 11.5)])


def pseudocode_slide(d, uid, title="THE SAME THING, WRITTEN OUT",
                     sub="You are not asked to type this. Read it, and check that it says what "
                         "the nodes you just built say.",
                     note=None, bg=BLACK, size=12.5, note_fill=YELLOW):
    """The unit's pseudocode, verbatim from course.yml, beside what it maps onto."""
    u = C.unit(uid)
    code = u.get("pseudocode", "").rstrip("\n").split("\n")
    s = d.slide(bg)
    s.header(title, sub)
    s.card(L, 2.0, 7.5, 4.15, fill=CREAM)
    step = min(0.30, 3.75 / max(len(code), 1))
    y = 2.2
    for ln in code:
        s.t(L + 0.32, y, 7.0, step, [s.Mb(ln if ln.strip() else " ", size)])
        y += step
    s.panel(8.35, 2.0, 4.3, 4.15, "WHAT IT MAPS ONTO", headfill=CYAN, tsize=13.5)
    words = C.vocab(uid)
    if len(words) <= 8:
        s.t(8.6, 2.75, 3.8, 3.2, [s.Cb(w, 13) for w in words], ls=1.45)
    else:
        half = (len(words) + 1) // 2
        s.t(8.6, 2.75, 1.85, 3.2, [s.Cb(w, 12) for w in words[:half]], ls=1.4)
        s.t(10.55, 2.75, 1.85, 3.2, [s.Cb(w, 12) for w in words[half:]], ls=1.4)
    s.banner(6.45, note or "EVERY WORD ON THE LEFT IS A NODE YOU USED TODAY. NOTHING HERE IS NEW.",
             fill=note_fill, h=0.62, size=12, align=PP_ALIGN.CENTER)
    return s
