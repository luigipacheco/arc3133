# Course maintenance

`syllabus/course.yml` is the source for session paths, teaching content and release settings. Generated course pages, the session index and `reference/blender/session-manifest.json` follow that source.

Edit `teaching_sequence` for the approved ten blocks, their target weeks and session placement. The dated `weeks` entries add dates and class notes, and `blender.sessions` adds the file, scene order and exercise. A teaching block with `combine_sessions: true` groups its example files on one session page; arrays uses this with one planned video. Do not duplicate topic titles or session membership in those lists.

| Tool | Use |
|---|---|
| `sync_course.py` | Regenerate the site pages and course indexes |
| `verify_course.py` | Check the built site, links, releases, screenshots and downloads |
| `blender/annotate_csg.py` | Annotate the instructor's open CSG graph through Blender MCP |
| `blender/add_array_3d.py` | Add the XYZ cube-array exercise before hexagonal arrays through Blender MCP |
| `blender/capture_images.py` | Capture authentic node-editor and viewport images through Blender MCP |
| `blender/verify_sessions.py` | Open and evaluate every current session in background Blender, without saving |
| `blender/package_images.py` | Merge the latest capture with the image catalog and rebuild the image ZIP |
| `blender/verify_downloads.py` | Check individual class files and their supporting data |

## Updating a class file

1. Save its current teaching copy in the corresponding numbered folder under `files/blender`. Archive superseded source files under `reference/archive`.
2. Update the session in `syllabus/course.yml`, then run `python scripts/sync_course.py`.
3. Run Blender with `--background --factory-startup --python scripts/blender/verify_sessions.py`. This checks the saved files and writes results and hashes to `reference/blender/sessions-verification.json`.
4. Through Blender MCP, execute `blender/capture_images.py` with `--live --only S01` (substitute the session ID). Inspect both PNGs. Update the script's scene choice when a lesson scene changes.
5. Run `python scripts/blender/package_images.py`, `python scripts/sync_course.py`, and `python scripts/blender/verify_downloads.py`.
6. Build with `bundle exec jekyll build`, then run `python scripts/verify_course.py`.

Capturing changes the editor view without saving over the class files. Image metadata and the screenshot ZIP are generated outputs; refresh them with the tools instead of maintaining separate manual indexes. Review captions in `blender/package_images.py` when the example changes.

Earlier build experiments and one-time preparation scripts are archived under `reference/archive/blender-course-preparation`. They are historical records and should not be used to overwrite the current lessons.

Blender example files are downloaded individually from Resources. Do not recreate a bundle of all sessions; the earlier ZIP and packaging script are preserved in the archive.

Possible intermediate classes belong under `optional_classes`, outside the required `teaching_sequence`. Their example files remain available individually and are identified as optional.
