"""Fit teaching annotations and validate every standalone session after reopening.

session-manifest.json is generated from syllabus/course.yml, never edited by hand.
Run in a separate Blender process. The original Geometry101 file is read-only.
"""
import bpy
import importlib.util
import json
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('lessons', HERE/'build_lessons.py')
lesson = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lesson)
manifest = json.loads((HERE/'session-manifest.json').read_text(encoding='utf-8'))
report = []
for session in manifest:
    path = lesson.ROOT/session['file']
    original = sha256(path.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=True)
    bpy.context.preferences.filepaths.save_version = 0
    assert sorted(s.name for s in bpy.data.scenes) == sorted(session['scenes']), session['id']
    if session['id'] != 'S02':
        for group in bpy.data.node_groups:
            if group.bl_idname != 'GeometryNodeTree':
                continue
            lesson.fit_teaching_frames(group)
            for node in group.nodes:
                if node.type == 'FRAME' and node.text and not node.shrink:
                    body = node.text.as_string().rstrip()
                    node.height = max(node.height, 100+40*len(body.splitlines()))
                    node.width = max(node.width, max(map(len, body.splitlines()), default=0)*15)
                    if node.label == 'NINE RELATED PARTS, ONE TESTED CONNECTION':
                        node.label = 'NINE RELATED PARTS | TEST ONE CONNECTION'
        lesson.view_setup(bpy.data.scenes[session['scenes'][0]])
        bpy.ops.wm.save_as_mainfile(filepath=str(path))
        bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=True)
        assert bpy.context.scene.name == session['scenes'][0]
    else:
        assert sha256(path.read_bytes()).hexdigest() == original
    details = {}
    assert not bpy.data.libraries, 'All lesson groups must be embedded in each session'
    for group in bpy.data.node_groups:
        if group.bl_idname == 'GeometryNodeTree':
            for node in group.nodes:
                assert node.type == 'FRAME' or not node.label, (path,group.name,node.name,node.label)
                assert node.bl_idname != 'NodeUndefined'
                if node.bl_idname == 'GeometryNodeImportPLY':
                    filename = lesson.sock(node,'Path').default_value
                    assert filename == '//teaching-courtyard.ply'
                    assert Path(bpy.path.abspath(filename)).is_file()
    for name in session['scenes']:
        scene = bpy.data.scenes[name]
        lesson.activate(scene)
        obj = scene.view_layers[0].objects.active
        assert obj is not None and any(m.type == 'NODES' for m in obj.modifiers)
        geometry = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).evaluated_geometry()
        details[name] = {
            'points': len(geometry.pointcloud.points) if geometry.pointcloud else 0,
            'curves': len(geometry.curves.curves) if geometry.curves else 0,
            'vertices': len(geometry.mesh.vertices) if geometry.mesh else 0,
            'edges': len(geometry.mesh.edges) if geometry.mesh else 0,
            'faces': len(geometry.mesh.polygons) if geometry.mesh else 0,
        }
        assert sum(details[name].values()) > 0, (session['id'],name)
        if session['id'] == 'S02' and name in ('05 - Solid','06 - Boolean'):
            modifier = next(m for m in obj.modifiers if m.type == 'NODES')
            assert [s.name for s in modifier.node_group.interface.items_tree if s.item_type=='SOCKET' and s.in_out=='INPUT'] == ['Width','Depth','Height']
        if geometry.mesh and geometry.mesh.polygons:
            stats = lesson.mesh_stats(scene)
            is_open = (session['id']=='S02' and name=='04 - Face') or (session['id']=='S05' and name=='01 - Read the field')
            if not is_open:
                assert stats['nonmanifold_edges']==0 and stats['volume']>0, (session['id'],name,stats)
            details[name]['closed'] = stats['nonmanifold_edges']==0
    report.append({'session':session['id'],'file':session['file'],'scenes':details,
                   'sha256':sha256(path.read_bytes()).hexdigest(),'fresh_open_verified':True})
    print(f"VERIFIED {session['id']}: {len(details)} scenes; native names; embedded groups; geometry evaluates",flush=True)
(HERE/'all-sessions-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
assert len(report)==12
print('ALL 12 SESSION FILES VERIFIED',flush=True)
