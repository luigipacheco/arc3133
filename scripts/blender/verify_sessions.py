"""Read and evaluate current saved class files in a background Blender process."""
import bpy
import bmesh
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sessions = json.loads((ROOT / 'reference/blender/session-manifest.json').read_text(encoding='utf-8'))
report = []
for session in sessions:
    path = ROOT / session['file']
    original = sha256(path.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    assert not bpy.data.libraries, 'Class files must contain their node groups'
    for group in bpy.data.node_groups:
        if group.bl_idname != 'GeometryNodeTree':
            continue
        for node in group.nodes:
            assert node.bl_idname != 'NodeUndefined'
            assert node.type == 'FRAME' or not node.label, (path, group.name, node.name)
            if node.bl_idname == 'GeometryNodeImportPLY':
                filename = next(s.default_value for s in node.inputs if s.name == 'Path')
                assert filename == '//teaching-courtyard.ply'
                assert Path(bpy.path.abspath(filename)).is_file()
    details = {}
    for scene in bpy.data.scenes:
        bpy.context.window.scene = scene
        layer = scene.view_layers[0]
        bpy.context.window.view_layer = layer
        obj = layer.objects.active
        assert obj and any(m.type == 'NODES' for m in obj.modifiers), (path, scene.name)
        layer.update()
        geometry = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).evaluated_geometry()
        instances = geometry.instances_pointcloud()
        counts = {'points': len(geometry.pointcloud.points) if geometry.pointcloud else 0,
                  'instances': len(instances.points) if instances else 0,
                  'curves': len(geometry.curves.curves) if geometry.curves else 0,
                  'vertices': len(geometry.mesh.vertices) if geometry.mesh else 0,
                  'edges': len(geometry.mesh.edges) if geometry.mesh else 0,
                  'faces': len(geometry.mesh.polygons) if geometry.mesh else 0}
        assert sum(counts.values()) > 0, (path, scene.name)
        if geometry.mesh and geometry.mesh.polygons:
            mesh = bmesh.new()
            mesh.from_mesh(geometry.mesh)
            counts['nonmanifold_edges'] = sum(not edge.is_manifold for edge in mesh.edges)
            counts['closed'] = counts['nonmanifold_edges'] == 0
            counts['volume'] = abs(mesh.calc_volume())
            mesh.free()
        if session['id'] == 'S02' and scene.name in ('05 - Solid', '06 - Boolean'):
            modifier = next(m for m in obj.modifiers if m.type == 'NODES')
            assert [s.name for s in modifier.node_group.interface.items_tree if s.item_type == 'SOCKET' and s.in_out == 'INPUT'] == ['Width', 'Depth', 'Height']
        details[scene.name] = counts
    assert sha256(path.read_bytes()).hexdigest() == original
    report.append({'session': session['id'], 'file': session['file'], 'scenes': details,
                   'sha256': original, 'fresh_open_verified': True})
    print('VERIFIED ' + session['id'] + ': ' + str(len(details)) + ' scenes', flush=True)
(ROOT / 'reference/blender/sessions-verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('Verified all current sessions without modifying any class files.', flush=True)
