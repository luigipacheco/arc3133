# -*- coding: utf-8 -*-
"""Dot-field diagrams, drawn from primitives so they stay crisp at any size."""
import math
from nb import *
from pptx.util import Pt


def cartesian(s, x, y, cols=6, rows=5, p=0.34, d=0.11):
    for i in range(cols):
        for j in range(rows):
            s.dot(x + i * p, y + j * p, d=d)


def hexagonal(s, x, y, cols=6, rows=5, p=0.34, d=0.11):
    for j in range(rows):
        off = p / 2 if j % 2 else 0.0
        for i in range(cols if j % 2 == 0 else cols - 1):
            s.dot(x + off + i * p, y + j * p, d=d)


def radial(s, cx, cy, rings=(0.44, 0.80, 1.16), n=12, d=0.105, hub=PINK):
    for rr in rings:
        for k in range(96):
            a = 2 * math.pi * k / 96.0
            s.dot(cx + rr * math.cos(a), cy + rr * math.sin(a), d=0.022, fill=MUTE)
    for rr in rings:
        for k in range(n):
            a = 2 * math.pi * k / n - math.pi / 2
            s.dot(cx + rr * math.cos(a), cy + rr * math.sin(a), d=d)
    s.dot(cx, cy, d=0.16, fill=hub)


def on_curve(s, x, y, w=2.25, amp=0.85, n=9, d=0.12, col=YELLOW):
    f = lambda t: y + amp - amp * math.sin(t * math.pi)
    for k in range(49):
        t = k / 48.0
        s.dot(x + t * w, f(t), d=0.028, fill=MUTE)
    for k in range(n):
        t = k / (n - 1.0)
        s.dot(x + t * w, f(t), d=d, fill=col)


def sine_row(s, x, y, w=2.4, amp=0.55, n=13, d=0.12, col=YELLOW, cycles=1.0):
    f = lambda t: y - amp * math.sin(t * math.pi * 2 * cycles)
    for k in range(80):
        t = k / 79.0
        s.dot(x + t * w, f(t), d=0.025, fill=MUTE)
    for k in range(n):
        t = k / (n - 1.0)
        s.dot(x + t * w, f(t), d=d, fill=col)


def field_point(s, x, y, ax, ay, cols=9, rows=7, p=0.34, q=0.24, k=0.16, base=0.24):
    for i in range(cols):
        for j in range(rows):
            px, py = x + i * p, y + j * q
            dd = math.hypot(px - ax, (py - ay) * 1.4)
            s.dot(px, py, d=max(0.045, base - dd * k))
    s.dot(ax, ay, d=0.13, fill=PINK)


def field_multi(s, x, y, pts, cols=9, rows=7, p=0.34, q=0.24, k=0.15, base=0.22):
    for i in range(cols):
        for j in range(rows):
            px, py = x + i * p, y + j * q
            dd = min(math.hypot(px - ax, (py - ay) * 1.4) for ax, ay in pts)
            s.dot(px, py, d=max(0.045, base - dd * k))
    for ax, ay in pts:
        s.dot(ax, ay, d=0.13, fill=PINK)


def field_curve(s, x, y, cx, cw, cf, cols=9, rows=7, p=0.34, q=0.24, k=0.20, base=0.22):
    for m in range(70):
        t = m / 69.0
        s.dot(cx + t * cw, cf(t), d=0.03, fill=PINK)
    for i in range(cols):
        for j in range(rows):
            px, py = x + i * p, y + j * q
            t = min(max((px - cx) / cw, 0), 1)
            dd = abs(py - cf(t)) * 1.3
            s.dot(px, py, d=max(0.045, base - dd * k))


def falloff(s, x, y, fn, w=2.2, h=0.75, n=26, col=BLACK):
    for k in range(n):
        t = k / (n - 1.0)
        v = max(0.0, min(1.0, fn(t)))
        s.dot(x + t * w, y - v * h, d=0.055, fill=col)


GRAY_RAMP = ["FFFDF7", "E8E8E0", "CFCFC6", "B4B4AC", "969690",
             "757570", "525250", "323230", "1C1C1C"]


def gray_ramp(s, x, y, w, h=0.5, ramp=None):
    ramp = ramp or GRAY_RAMP
    step = w / len(ramp)
    for i, c in enumerate(ramp):
        s.rect(x + i * step, y, step, h, fill=c, line=BLACK, lw=Pt(1.5))
