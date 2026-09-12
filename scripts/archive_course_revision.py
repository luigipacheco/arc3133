"""One-time, verified snapshot before the September 2026 curriculum revision."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "reference/archive/2026-09-12-before-sequence"

def main():
    if (ARCHIVE / "manifest.json").exists():
        raise SystemExit("Snapshot already exists; it will not be overwritten.")
    files = [ROOT / "README.md", ROOT / "index.md", ROOT / "_config.yml"]
    files += list((ROOT / "syllabus").glob("*.md"))
    files += list((ROOT / "reference").glob("*.md"))
    files += list((ROOT / "modules").rglob("*.md"))
    files += [p for p in (ROOT / "slides").rglob("*") if p.is_file()]
    records = []
    for src in files:
        src = src.resolve()
        if not src.is_relative_to(ROOT) or src.is_relative_to(ARCHIVE):
            raise ValueError(src)
        relative = src.relative_to(ROOT)
        dst = (ARCHIVE / relative).resolve()
        if not dst.is_relative_to(ARCHIVE):
            raise ValueError(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        if hashlib.sha256(dst.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Snapshot verification failed: {src}")
        records.append({"path": relative.as_posix(), "sha256": digest})
    (ARCHIVE / "manifest.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    (ARCHIVE / "ARCHIVE_README.md").write_text(
        "# Historical course snapshot — September 12, 2026\n\n"
        "These files preserve the course before the revised learning sequence. "
        "They are not current assignment instructions. The snapshot includes conflicting older plans.\n\n"
        "Current curriculum: [course.yml](../../../syllabus/course.yml). "
        "The manifest records the original paths and SHA-256 hashes. "
        "Archived links may describe paths in the earlier repository.\n",
        encoding="utf-8")
    original = (ROOT / "syllabus/ARC3133_Syllabus_Fall2026.md").read_text(encoding="utf-8")
    preamble = original.split("## Artificial Intelligence Preamble", 1)[1].split("## AI Language Specific To This Course", 1)[0].strip()
    policy = original.split("## Attendance Policy Statement", 1)[1].split("## Teaching Methodologies", 1)[0].strip()
    (ROOT / "syllabus/policies.md").write_text(
        "<!-- Policy text retained from the previous syllabus. Edit policy wording here; generated copies are not authoritative. -->\n\n"
        "## Artificial Intelligence Preamble\n\n" + preamble + "\n\n"
        "## Attendance Policy Statement\n\n" + policy + "\n",
        encoding="utf-8")
    print(f"Verified snapshot of {len(records)} files; retained policy text separately.")

if __name__ == "__main__":
    main()
