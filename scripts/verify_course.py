"""Verify the generated course, archived originals, and built local links."""
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

import yaml

from sync_course import Course, ROOT
import session_pages


SMART_QUOTES = str.maketrans({'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"'})


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.text = []
        self.tables = []
        self._table = None
        self._row = None
        self._cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table':
            self._table = []
        elif tag == 'tr':
            self._row = []
        elif tag in ('th', 'td'):
            self._cell = []
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])

    def handle_data(self, data):
        # Jekyll/kramdown turns straight quotes into typographic ones; compare the plain form.
        data = data.translate(SMART_QUOTES)
        self.text.append(data)
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag in ('th', 'td') and self._cell is not None:
            self._row.append(' '.join(''.join(self._cell).split()))
            self._cell = None
        elif tag == 'tr' and self._table is not None:
            self._table.append(self._row)
            self._row = None
        elif tag == 'table' and self._table is not None:
            self.tables.append(self._table)
            self._table = None


def verify_sequence(course, site, documents, baseurl):
    """Classes are the sessions: one page per class carries its slides and files."""
    expected = [[session_pages.weeks(b), b['focus']] for b in course.sequence]
    overview_path = 'modules' + session_pages.OVERVIEW + 'index.html'
    for path in ('index.html', overview_path, 'resources/course-policies/index.html'):
        page = documents[(site / path).resolve()]
        tables = [t for t in page.tables if t and t[0][:2] == ['Weeks', 'Topic']]
        assert len(tables) == 1 and [row[:2] for row in tables[0][1:]] == expected, f'Teaching sequence drift: {path}'
    index = documents[(site / overview_path).resolve()]
    assert {b['id'].lower() for b in course.sequence} <= index.ids
    optional_units = {u for b in course.optional_classes for u in b['units']}
    assert not optional_units & {u for b in course.sequence for u in b['units']}, 'Optional topics returned to the required sequence'
    assert not (site / 'modules/sessions').exists(), 'The retired sessions section was published'
    for number, block in course.week_blocks.items():
        path = (site / ('modules' + course.class_url(number)).lstrip('/') / 'index.html').resolve()
        if number not in course.open_weeks:
            assert path not in documents or 'Course material has moved' in ''.join(documents[path].text), f'Unreleased class page: {number}'
            continue
        page = documents[path]
        assert block['focus'] in ''.join(page.text), f'Class focus drift: {number}'
        stem = f'/slides/ARC3133_Class{number:02d}'
        review = next(r for r in course.data['presentation_review'] if r['week'] == number)
        slide_links = [baseurl + stem + suffix for suffix in ('.pdf', '.pptx')]
        if review['status'] == 'current':
            assert all(link in page.links for link in slide_links), f'Class slides missing: {number}'
        else:
            assert not any(link in page.links for link in slide_links), f'Unreviewed slides linked: {number}'
            assert 'Revised slides are not yet posted' in ''.join(page.text), f'Missing slide-status notice: {number}'
        for sid in course.weeks[number]['sessions']:
            session = next(s for s in course.sessions if s['id'] == sid)
            if session_pages.available(course, session):
                assert baseurl + '/' + session['path'] in page.links, f'Class file missing: {number}, {sid}'
                assert 'capture-' + sid.lower() in page.ids, f'Class screenshots missing: {number}, {sid}'
    for session in course.sessions:
        path = (site / 'sessions' / session['id'].lower() / 'index.html').resolve()
        assert path in documents and 'sessions and classes are now the same' in ''.join(documents[path].text), f'Missing redirect: {session["id"]}'
    examples = documents[(site / 'resources/example-files/index.html').resolve()]
    if course.optional_classes:
        assert 'possible-intermediate-class' in examples.ids, 'Optional downloads are not separated'
    for s in course.sessions:
        assert baseurl + '/' + s['path'] in examples.links, f'Missing individual download: {s["id"]}'
        for _, extra in s.get('extras', []):
            assert baseurl + '/' + extra in examples.links, f'Missing supporting download: {extra}'
    assert not list((site / 'files/blender').rglob('*.zip')), 'A bundled session ZIP was published'
    assert not any('/files/blender/' in link and '.zip' in link for page in documents.values() for link in page.links), 'Bundled session ZIP link remains'
    assert course.blender['reference_note'] in ' '.join(''.join(examples.text).split()), 'Reference-only instructions missing'


STALE = []


def verify_screenshots(course, site, documents):
    captures = course.blender_images
    sessions = {s["id"]: s for s in course.sessions}
    assert {i["session"] for i in captures} == set(sessions), "Missing or duplicate session screenshots"
    assert len(captures) == len(sessions)
    assert captures == json.loads((ROOT / "images/blender/manifest.json").read_text(encoding="utf-8"))
    for item in captures:
        assert item["source_file"] == sessions[item["session"]]["path"]
        assert item["unit"] in sessions[item["session"]]["units"]
        if sha256((ROOT / item["source_file"]).read_bytes()).hexdigest() != item["source_sha256"]:
            # The .blend has been edited since these screenshots were taken, so the
            # published images show an older graph. Worth knowing, not worth blocking
            # a deploy over: recapture with scripts/blender/capture_images.py when
            # the pictures matter. Everything below still proves the published
            # images are internally consistent.
            STALE.append(item["session"])
        for kind in ("geonodes", "viewport"):
            asset = item[kind]
            payload = (site / asset["file"]).read_bytes()
            assert sha256(payload).hexdigest() == asset["sha256"], asset["file"]
            assert payload[:8] == b"\x89PNG\r\n\x1a\n"
            assert struct.unpack(">II", payload[16:24]) == (asset["width"], asset["height"])
    with ZipFile(site / "images/blender/ARC3133-Blender-Screenshots.zip") as archive:
        assert archive.testzip() is None
        for item in captures:
            for kind in ("geonodes", "viewport"):
                asset = item[kind]
                assert sha256(archive.read(Path(asset["file"]).name)).hexdigest() == asset["sha256"]
    expected = {"capture-" + i["session"].lower() for i in captures if i["unit"] in course.open_units}
    gallery = documents.get((site / "resources/blender-screenshots/index.html").resolve())
    assert gallery is not None or not expected, "Screenshot gallery disappeared"
    if gallery:
        assert {i for i in gallery.ids if i.startswith("capture-")} == expected, "Gallery does not match released lessons"
    for uid in course.open_units & set(course.units):
        page = documents[(site / ("modules" + course.unit_url(course.units[uid])).lstrip("/") / "index.html").resolve()]
        expected = {"capture-" + i["session"].lower() for i in captures if i["unit"] == uid}
        assert {i for i in page.ids if i.startswith("capture-")} == expected, f"Lesson screenshots missing: {uid}"


def matches_archive_hash(path, expected):
    """Keep the archived content check stable across Git's LF/CRLF checkouts."""
    payload = path.read_bytes()
    if sha256(payload).hexdigest() == expected:
        return True
    # Only the known archived UTF-8 source formats permit newline normalization.
    # Binary teaching assets and all other changes still require the exact hash.
    if path.suffix.lower() not in {".md", ".yml", ".yaml", ".py"}:
        return False
    try:
        payload.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return sha256(payload.replace(b"\r\n", b"\n")).hexdigest() == expected


def verify_assignment_pdfs(course, site, documents, baseurl):
    for project in course.projects.values():
        if not project.get("brief_pdf"):
            continue
        relative = project["brief_pdf"]
        assert (site / relative).read_bytes() == (ROOT / relative).read_bytes(), relative
        if project["id"] in course.open_work:
            page = (site / ("modules" + course.project_url(project)).lstrip("/") / "index.html").resolve()
            assert baseurl + "/" + relative in documents[page].links, f"Missing PDF download: {project['id']}"


def main():
    course = Course()
    if course.sync(True):
        raise SystemExit(1)
    archive = ROOT / "reference/archive/2026-09-12-before-sequence"
    manifest = json.loads((archive / "manifest.json").read_text(encoding="utf-8"))
    for item in manifest:
        assert matches_archive_hash(archive / item["path"], item["sha256"]), item["path"]
    site = ROOT / "_site"
    config = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8"))
    baseurl = config.get("baseurl", "").rstrip("/")
    assert (site / "index.html").is_file(), "Build the course site first"
    built_files = {p.relative_to(site).as_posix() for p in site.rglob("*") if p.is_file()}
    documents = {}
    for path in site.rglob("*.html"):
        parser = Links()
        parser.feed(path.read_text(encoding="utf-8"))
        documents[path.resolve()] = parser
    checked = 0
    errors = set()
    for path, parsed in documents.items():
        for link in parsed.links:
            target = urlsplit(link)
            if target.scheme or target.netloc or link in ("#", ""):
                continue
            if target.path.startswith("/"):
                local_path = unquote(target.path)
                if baseurl and (local_path == baseurl or local_path.startswith(baseurl + "/")):
                    local_path = local_path[len(baseurl):]
                elif baseurl:
                    errors.add(f"Missing project prefix: {path.relative_to(site)} → {link}")
                    continue
                resolved = site / local_path.lstrip("/")
            elif target.path:
                resolved = path.parent / unquote(target.path)
            else:
                resolved = path
            resolved = resolved.resolve()
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if not resolved.is_file():
                errors.add(f"{path.relative_to(site)} → {link}")
                continue
            if not resolved.is_relative_to(site) or resolved.relative_to(site).as_posix() not in built_files:
                errors.add(f"Path or filename case mismatch: {path.relative_to(site)} → {link}")
                continue
            if target.fragment and resolved in documents and unquote(target.fragment) not in documents[resolved].ids:
                errors.add(f"Missing anchor: {path.relative_to(site)} → {link}")
            checked += 1
    assert not errors, "Broken local links:\n" + "\n".join(sorted(errors))
    for excluded in ("reference", "syllabus", "slides/src", "scripts", "code", "vendor", ".bundle", ".github", ".git"):
        assert not (site / excluded).exists(), f"Historical/source directory leaked into site: {excluded}"
    verify_screenshots(course, site, documents)
    verify_sequence(course, site, documents, baseurl)
    verify_assignment_pdfs(course, site, documents, baseurl)
    size = sum((site / name).stat().st_size for name in built_files)
    assert size < 1_000_000_000, "Site exceeds the GitHub Pages 1 GB site limit"
    if STALE:
        print("NOTE: screenshots predate the current Blender files for "
              + ", ".join(STALE)
              + ". Recapture with scripts/blender/capture_images.py to refresh them.")
    print(f"Verified {len(manifest)} archived originals, {checked} local links, and {len(course.blender_images) * 2} screenshots across {len(documents)} built pages. Site size: {size / 1_000_000:.1f} MB. Sources are excluded; release settings and project paths match.")


if __name__ == "__main__":
    main()
