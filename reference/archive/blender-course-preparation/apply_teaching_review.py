"""Small presentation corrections to saved files; keep all native node names."""
import bpy
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
sessions = json.loads((ROOT/'reference/blender-course/session-manifest.json').read_text(encoding='utf-8'))
archive = ROOT/'reference/blender-course/preparation-archive/before-teaching-review'
archive.mkdir(parents=True,exist_ok=True)
for session in sessions:
    if session['id']=='S02':
        continue
    path = ROOT/session['file']
    backup = archive/path.name
    if not backup.exists():
        shutil.copy2(path,backup)
    # The general annotation-spacing correction is handled by finalize_sessions.
    if session['id'] not in ('S07','S10'):
        continue
    bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=True)
    bpy.context.preferences.filepaths.save_version=0
    if session['id']=='S07':
        group = bpy.data.node_groups['01 - Import points']
        frame = next(n for n in group.nodes if n.type=='FRAME')
        frame.text.clear()
        frame.text.write('Import PLY reads 1806 samples with zero edges and zero faces.\n'
                         'The small spheres are display geometry; the final output is a mesh.\n'
                         'Ctrl+Shift+click Mesh to Points to inspect the samples with Viewer.\n'
                         'In the Spreadsheet, choose Viewer Node, then Point Cloud / Point.\n'
                         'Synthetic data, origin (0,0,0), meters, no decimation. Keep the PLY beside this file.\n')
        for text in bpy.data.texts:
            if text.name.startswith('START HERE'):
                text.write('\nPOINT DATA: use Viewer on Mesh to Points to inspect the source samples.\n'
                           'The final mesh consists of display spheres and has a different vertex count.\n')
    else:
        group = bpy.data.node_groups['02 - Contour stack']
        for node in group.nodes:
            if node.type!='FRAME' and node.location.x>=2690:
                node.location.x-=1700
        next(n for n in group.nodes if n.type=='FRAME').width=2490
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
print('Teaching review corrections applied; run finalize_sessions.py to fit headers and validate.')
