"""Read current teaching files without saving; record failures per file."""
import bpy
import bmesh
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reference/course-audit'
OUT.mkdir(parents=True, exist_ok=True)
sessions = json.loads((ROOT / 'reference/blender/session-manifest.json').read_text(encoding='utf-8'))
report = {'blender_version': bpy.app.version_string, 'files': []}
for session in sessions:
    path = ROOT / session['file']
    item = {'session': session['id'], 'file': session['file'], 'sha256': sha256(path.read_bytes()).hexdigest(),
            'scenes': [], 'errors': [], 'dependencies': [], 'undefined_nodes': []}
    try:
        bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
        item['external_libraries'] = [lib.filepath for lib in bpy.data.libraries]
        for group in bpy.data.node_groups:
            for node in group.nodes:
                if node.bl_idname == 'NodeUndefined':
                    item['undefined_nodes'].append([group.name, node.name])
                if node.bl_idname == 'GeometryNodeImportPLY':
                    raw = next(s.default_value for s in node.inputs if s.name == 'Path')
                    resolved = Path(bpy.path.abspath(raw))
                    item['dependencies'].append({'path': raw, 'exists': resolved.is_file()})
        for scene in bpy.data.scenes:
            record = {'name': scene.name, 'objects': [obj.name for obj in scene.objects]}
            try:
                bpy.context.window.scene = scene
                layer = scene.view_layers[0]
                bpy.context.window.view_layer = layer
                obj = layer.objects.active
                if obj is None:
                    obj = next((o for o in scene.objects if any(m.type == 'NODES' for m in o.modifiers)), None)
                record['active_object'] = obj.name if obj else None
                if obj:
                    layer.update()
                    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
                    geo = evaluated.evaluated_geometry()
                    instances = geo.instances_pointcloud()
                    record['geometry'] = {
                        'points': len(geo.pointcloud.points) if geo.pointcloud else 0,
                        'instances': len(instances.points) if instances else 0,
                        'curves': len(geo.curves.curves) if geo.curves else 0,
                        'vertices': len(geo.mesh.vertices) if geo.mesh else 0,
                        'faces': len(geo.mesh.polygons) if geo.mesh else 0,
                    }
                    if geo.mesh and geo.mesh.polygons:
                        mesh = bmesh.new()
                        mesh.from_mesh(geo.mesh)
                        record['nonmanifold_edges'] = sum(not edge.is_manifold for edge in mesh.edges)
                        record['mesh_volume'] = mesh.calc_volume()
                        mesh.free()
                    record['node_groups'] = [m.node_group.name for m in obj.modifiers if m.type == 'NODES' and m.node_group]
                    record['exposed_inputs'] = {m.name: [socket.name for socket in m.node_group.interface.items_tree
                                                        if socket.item_type == 'SOCKET' and socket.in_out == 'INPUT']
                                                for m in obj.modifiers if m.type == 'NODES' and m.node_group}
            except Exception as exc:
                record['error'] = repr(exc)
                item['errors'].append(scene.name + ': ' + repr(exc))
            item['scenes'].append(record)
    except Exception as exc:
        item['errors'].append(repr(exc))
    item['source_unchanged'] = sha256(path.read_bytes()).hexdigest() == item['sha256']
    report['files'].append(item)
    (OUT / 'blender-readonly.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(session['id'], len(item['scenes']), 'scenes;', len(item['errors']), 'evaluation errors;',
          len(item['undefined_nodes']), 'undefined nodes; unchanged:', item['source_unchanged'], flush=True)
