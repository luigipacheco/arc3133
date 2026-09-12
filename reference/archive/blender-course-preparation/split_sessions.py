"""Export complete, ready-to-open files containing only one session's scenes."""
import bpy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('lessons', HERE/'build_lessons.py')
lesson = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lesson)

reports = []
for key, sessions in lesson.SPLIT_SESSIONS.items():
    master = lesson.source_path(key)
    for number, (filename, names) in enumerate(sessions, 1):
        bpy.ops.wm.open_mainfile(filepath=str(master), load_ui=True)
        bpy.context.preferences.filepaths.save_version = 0
        first = bpy.data.scenes[names[0]]
        lesson.activate(first)
        for scene in list(bpy.data.scenes):
            if scene.name not in names:
                bpy.data.scenes.remove(scene)
        for obj in list(bpy.data.objects):
            if not obj.users_scene:
                bpy.data.objects.remove(obj, do_unlink=True)
        for text in list(bpy.data.texts):
            if text.name.startswith('START HERE'):
                bpy.data.texts.remove(text)
        # Keep only the groups reachable from the remaining objects/materials.
        for group in bpy.data.node_groups:
            group.use_fake_user = False
        bpy.data.orphans_purge(do_recursive=True)
        notes = bpy.data.texts.new(f'START HERE — Session {number}')
        notes.use_fake_user = True
        notes.write(f'ARC 3133 — {lesson.CATALOG[key][2]} — Session {number}\n\n'
                    'This file contains only this session. Choose scenes in the order below.\n'
                    'Select the lesson object and change exposed controls in its GeometryNodes modifier.\n'
                    'Press Home over the node editor to fit the graph. Read the explanatory Frames.\n'
                    'Keep native node names and save your own working copy.\n\n' + '\n'.join(names) + '\n')
        report = {'file': str((lesson.FILES/lesson.CATALOG[key][0]/filename).relative_to(lesson.ROOT)),
                  'session': number, 'scenes': {name: lesson.mesh_stats(bpy.data.scenes[name]) for name in names}}
        for group in bpy.data.node_groups:
            if group.bl_idname == 'GeometryNodeTree':
                assert all(n.type == 'FRAME' or not n.label for n in group.nodes)
        lesson.view_setup(first)
        target = lesson.FILES/lesson.CATALOG[key][0]/filename
        bpy.ops.wm.save_as_mainfile(filepath=str(target))
        bpy.ops.wm.open_mainfile(filepath=str(target), load_ui=True)
        assert sorted(s.name for s in bpy.data.scenes) == sorted(names)
        assert bpy.context.scene.name == names[0]
        assert all(lesson.mesh_stats(bpy.data.scenes[name])['vertices'] > 0 for name in names)
        report['fresh_open_verified'] = True
        reports.append(report)
        print('SESSION_COMPLETE '+json.dumps(report), flush=True)
(HERE/'sessions-verification.json').write_text(json.dumps(reports, indent=2)+'\n', encoding='utf-8')
