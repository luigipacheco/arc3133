"""Shared assignment text and reproducible PDF downloads for the first three projects."""
from __future__ import annotations

from hashlib import sha256
import html
import json
from pathlib import Path
import re

SECTIONS = [
    ("Description", "description"),
    ("Rules & Constraints", "requirements"),
    ("Parameters", "parameters"),
    ("Required Studies", "studies"),
    ("Workflow", "workflow"),
    ("Deliverables", "deliverables"),
    ("Evaluation", "evaluation"),
    ("Before You Submit", "checklist"),
]
MANIFEST = "files/assignments/manifest.json"


def validate(course):
    for project in course.projects.values():
        if not project.get("brief_pdf"):
            continue
        path = Path(project["brief_pdf"])
        assert path.parts[:2] == ("files", "assignments") and ".." not in path.parts
        assert path.suffix == ".pdf"
        ids = project["brief_milestones"]
        assert ids and len(ids) == len(set(ids))
        assert set(ids) <= {a["id"] for a in project["milestones"]}
        for aid in ids:
            brief = course.by_id[aid]["brief"]
            assert set(brief) == {key for _, key in SECTIONS if key != "requirements"}, aid
            assert isinstance(brief["description"], str) and brief["description"].strip(), aid
            for _, key in SECTIONS[2:]:
                assert isinstance(brief[key], list) and brief[key], (aid, key)
                assert all(isinstance(x, str) and x.strip() for x in brief[key]), (aid, key)


def body(assignment, heading="###"):
    """The same Markdown body feeds the site and downloadable handout."""
    brief = assignment["brief"]
    parts = []
    for label, key in SECTIONS:
        parts.append(f"{heading} {label}\n\n")
        value = assignment["requirements"] if key == "requirements" else brief[key]
        if key == "description":
            parts.append(value + "\n\n")
        elif key == "workflow":
            parts.append("\n".join(f"{i}. {text}" for i, text in enumerate(value, 1)) + "\n\n")
        elif key == "checklist":
            parts.append("\n".join(f"- [ ] {text}" for text in value) + "\n\n")
        else:
            parts.append("\n".join(f"- {text}" for text in value) + "\n\n")
    return "".join(parts)


def project_markdown(course, project):
    title = project.get("brief_title", project["title"])
    out = f"# {project['id']} - {title}\n\n"
    out += f"{course.meta['code']} / {course.meta['title']} / {course.meta['term']}\n\n"
    out += f"Revision: {course.data['revision']}. Dates and weights follow the course schedule.\n\n"
    if project["id"] == "P3":
        out += "Current scope: descriptive geometry and 1D, 2D and 3D arrays. Attractors and other array families are reserved for later work.\n\n"
    for aid in project["brief_milestones"]:
        a = course.by_id[aid]
        out += f"## {aid} - {a['title']}\n\n"
        out += f"**Introduced:** {course.when(a['release'])} / **Due:** {course.when(a['due'])} / **Weight:** {a['weight']}%\n\n"
        if a.get("checkpoints"):
            out += "**Preparation checks:** " + "; ".join(
                course.when(c["week"]) + ": " + c["text"] for c in a["checkpoints"]
            ) + "\n\n"
        out += body(a)
    out += "**Shared standards:** Course software, fabrication, attribution and AI policies apply. Submit through the channel announced in class/Canvas. Test the packaged source from a clean folder. Percentages are existing course weights. This handout uses US Letter; student sheets are 17 x 11 inches.\n"
    return out


def plain(text):
    return text.translate(str.maketrans({"—": "-", "–": "-", "→": "to", "×": "x",
        "’": "'", "‘": "'", "“": '"', "”": '"', "≥": ">=", "≤": "<=", "·": "/"}))


def inline(text):
    text = html.escape(plain(text), quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`([^`]+)`", r'<font name="Courier" size="8.5">\1</font>', text)


def render_pdf(path, markdown, course, project):
    # Lazy imports let a read-only sync check run without loading the PDF renderer.
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, KeepTogether

    base = dict(fontName="Helvetica", fontSize=10, leading=12.5, spaceAfter=4,
                textColor=colors.HexColor("#171717"))
    styles = {
        "body": ParagraphStyle("body", **base),
        "list": ParagraphStyle("list", **{**base, "leftIndent": 11, "firstLineIndent": -9}),
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=24,
                                 leading=28, spaceAfter=15, keepWithNext=True),
        "milestone": ParagraphStyle("milestone", fontName="Helvetica-Bold", fontSize=17,
                                     leading=21, spaceBefore=8, spaceAfter=10, keepWithNext=True),
        "heading": ParagraphStyle("heading", fontName="Helvetica-Bold", fontSize=12,
                                   leading=15, spaceBefore=10, spaceAfter=6, keepWithNext=True),
        "note": ParagraphStyle("note", fontName="Helvetica", fontSize=8.5,
                                leading=11, spaceBefore=10, spaceAfter=0),
    }
    story = []
    milestones = 0
    active_aid = None
    # Paragraph blocks preserve numbered steps and list items as individual flowables.
    for block in markdown.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("# "):
            story.append(Paragraph(inline(block[2:]), styles["title"]))
        elif block.startswith("## "):
            if block.startswith("## Shared"):
                story.append(Paragraph(inline(block[3:]), styles["heading"]))
            else:
                if milestones:
                    story.append(PageBreak())
                milestones += 1
                active_aid = block[3:].split(" - ", 1)[0]
                story.append(Paragraph(inline(block[3:]), styles["milestone"]))
        elif block.startswith("### "):
            if (active_aid, block[4:]) in {("P2b", "Deliverables"), ("P3b", "Workflow")}:
                story.append(PageBreak())
            story.append(Paragraph(inline(block[4:]), styles["heading"]))
        elif block.startswith("- "):
            items = [Paragraph(inline(line), styles["list"]) for line in block.splitlines()]
            if block.startswith("- [ ]"):
                # Keep each final checklist together with its heading.
                heading = story.pop()
                story.append(KeepTogether([heading, *items]))
            else:
                story.extend(KeepTogether([item]) for item in items)
        elif re.match(r"^\d+\. ", block):
            story.extend(Paragraph(inline(line), styles["body"]) for line in block.splitlines())
        elif block.startswith("**Shared standards:"):
            story.append(Paragraph(inline(block), styles["note"]))
        else:
            story.append(Paragraph(inline(block.replace("\n", " ")), styles["body"]))

    def page_frame(canvas, doc):
        canvas.saveState()
        w, h = letter
        canvas.setFillColor(colors.HexColor("#c6f035"))
        canvas.rect(42, h - 35, w - 84, 4, fill=1, stroke=0)
        canvas.setFillColor(colors.black)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(42, h - 24, "ARC 3133 / FALL 2026 / ASSIGNMENT BRIEF")
        canvas.drawRightString(w - 42, h - 24, project["id"])
        canvas.setFont("Helvetica", 8)
        canvas.drawString(42, 24, f"Revision {course.data['revision']} / {project['id']}")
        canvas.drawRightString(w - 42, 24, f"Page {doc.page}")
        canvas.restoreState()

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=42, rightMargin=42,
                           topMargin=48, bottomMargin=46, invariant=1,
                           title=plain(project.get("brief_title", project["title"])),
                           author="ARC 3133 / Florida Atlantic University")
    doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)


def sync_pdfs(course, root, check):
    """Check source/PDF hashes or regenerate only the changed handouts."""
    validate(course)
    manifest_path = root / MANIFEST
    try:
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        previous = {}
    expected = {}
    issues = []
    renderer = Path(__file__).read_text(encoding="utf-8").encode("utf-8")
    for project in course.projects.values():
        if not project.get("brief_pdf"):
            continue
        markdown = project_markdown(course, project)
        digest = sha256(renderer + markdown.encode("utf-8")).hexdigest()
        relative = project["brief_pdf"]
        path = root / relative
        old = previous.get(project["id"], {})
        payload = path.read_bytes() if path.exists() else b""
        valid = (old.get("source_sha256") == digest and old.get("file") == relative
                 and payload.startswith(b"%PDF-")
                 and old.get("pdf_sha256") == sha256(payload).hexdigest())
        if not valid:
            issues.append(relative)
            if not check:
                render_pdf(path, markdown, course, project)
                payload = path.read_bytes()
        expected[project["id"]] = {"file": relative, "source_sha256": digest,
                                    "pdf_sha256": sha256(payload).hexdigest()}
    if previous != expected:
        issues.append(MANIFEST)
        if not check:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
    return issues
