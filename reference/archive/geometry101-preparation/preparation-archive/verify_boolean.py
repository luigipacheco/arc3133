import bpy
import bmesh
import json
import os
from mathutils.bvhtree import BVHTree

FOLDER = r'C:\Users\luigi\Documents\animaquina\class-prep\geometry101'
obj = bpy.data.objects['05 - Boolean Module']
group = bpy.data.node_groups['05 - Boolean Module']
modifier = obj.modifiers['GeometryNodes']
assert modifier.node_group == group

def inspect():
    obj.update_tag()
    bpy.context.view_layer.update()
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        bvh = BVHTree.FromBMesh(bm)
        return {
            'vertices': len(bm.verts), 'edges': len(bm.edges), 'faces': len(bm.faces),
            'non_manifold_edges': sum(not e.is_manifold for e in bm.edges),
            'volume': bm.calc_volume(signed=True),
            'euler': len(bm.verts) - len(bm.edges) + len(bm.faces),
            'center_ray_clear': bvh.ray_cast((0, 0, 3), (0, 0, -1), 6)[0] is None,
            'rim_ray_hit': bvh.ray_cast((1.15, 0, 3), (0, 0, -1), 6)[0] is not None,
            'thickness': max(v.co.z for v in bm.verts) - min(v.co.z for v in bm.verts),
        }
    finally:
        bm.free()
        evaluated.to_mesh_clear()

def param(name):
    socket = next(s for s in group.interface.items_tree if s.item_type == 'SOCKET' and s.in_out == 'INPUT' and s.name == name)
    return getattr(modifier.properties.inputs, socket.identifier)

radius = param('Opening Radius')
thickness = param('Thickness')
boolean = group.nodes['Mesh Boolean']
old_radius, old_thickness, old_operation = radius.value, thickness.value, boolean.operation
checks = {}
try:
    for value in [0.4, 0.65, 0.95, 1.05, 1.1]:
        radius.value = value
        data = inspect()
        assert data['faces'] > 6 and data['non_manifold_edges'] == 0, data
        assert data['center_ray_clear'] and data['rim_ray_hit'], data
        assert data['euler'] == 0 and 0 < data['volume'] < 2.4 * 2.4 * 0.6, data
        checks['radius_' + str(value)] = data
    assert checks['radius_0.65']['volume'] > checks['radius_0.95']['volume'] > checks['radius_1.05']['volume']
    radius.value = 0.95
    thickness.value = 0.3
    data = inspect()
    assert abs(data['thickness'] - 0.3) < 1e-5 and data['non_manifold_edges'] == 0 and data['center_ray_clear'], data
    checks['thickness_0.3'] = data
    thickness.value = old_thickness
finally:
    radius.value = old_radius
    thickness.value = old_thickness
    boolean.operation = old_operation
    obj.update_tag()
    bpy.context.view_layer.update()

checks['final'] = inspect()
# Preserve original node identities, labels, links and parameter values.
with open(os.path.join(FOLDER, 'original-node-record.json'), encoding='utf-8') as f:
    baseline = json.load(f)
for name, old in baseline.items():
    g = bpy.data.node_groups[name]
    current = {
        'nodes': {n.name: {'type':n.bl_idname, 'label':n.label} for n in g.nodes if n.type != 'FRAME'},
        'links': sorted([l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier] for l in g.links),
        'values': {n.name:n.outputs[0].default_value for n in g.nodes if n.bl_idname == 'ShaderNodeValue'},
    }
    assert current == old, name
checks['original_graphs_preserved'] = True

with open(os.path.join(FOLDER, 'boolean-verification.json'), 'w', encoding='utf-8') as f:
    json.dump(checks, f, indent=2)
result = checks
