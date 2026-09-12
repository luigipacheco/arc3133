"""Verify the generated course, archived originals, and built local links."""
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

from sync_course import Course, ROOT


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])


def main():
    if Course().sync(True):
        raise SystemExit(1)
    archive = ROOT / "reference/archive/2026-09-12-before-sequence"
    manifest = json.loads((archive / "manifest.json").read_text(encoding="utf-8"))
    for item in manifest:
        assert sha256((archive / item["path"]).read_bytes()).hexdigest() == item["sha256"], item["path"]
    site = ROOT / "_site"
    assert (site / "index.html").is_file(), "Build the course site first"
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
                resolved = site / unquote(target.path).lstrip("/")
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
            if target.fragment and resolved in documents and unquote(target.fragment) not in documents[resolved].ids:
                errors.add(f"Missing anchor: {path.relative_to(site)} → {link}")
            checked += 1
    assert not errors, "Broken local links:\n" + "\n".join(sorted(errors))
    for excluded in ("reference", "syllabus", "slides", "scripts", "code"):
        assert not (site / excluded).exists(), f"Historical/source directory leaked into site: {excluded}"
    print(f"Verified {len(manifest)} archived originals and {checked} local links across {len(documents)} built pages. Historical and source directories are excluded.")


if __name__ == "__main__":
    main()
