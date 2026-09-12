import bpy
import bmesh
import json
import os
from mathutils.bvhtree import BVHTree

FOLDER = r'C:\Users\luigi\Documents\animaquina\class-prep\geometry101'
pyramid = bpy.data.node_groups['002-point in middle']
boolean = bpy.data.node_groups['06 - Boolean']
assert boolean.nodes['Group'].node_tree == pyramid

def inspect(name):
    scene = bpy.data.scenes[name]
    layer = scene.view_layers[0]
    obj = layer.objects.active
    with bpy.context.temp_override(scene=scene, view_layer=layer):
        obj.update_tag()
        layer.update()
        evaluated = obj.evaluated_get(layer.depsgraph)
        geo = evaluated.evaluated_geometry()
        mesh, curves, points = geo.mesh, geo.curves, geo.pointcloud
        result = {'points':len(points.points) if points else 0,
                  'curves':len(curves.curves) if curves else 0,
                  'curve_points':len(curves.points) if curves else 0,
                  'vertices':len(mesh.vertices) if mesh else 0,
                  'edges':len(mesh.edges) if mesh else 0,
                  'faces':len(mesh.polygons) if mesh else 0}
        if mesh and mesh.polygons:
            bm = bmesh.new()
            try:
                bm.from_mesh(mesh)
                bvh = BVHTree.FromBMesh(bm)
                result.update(volume=bm.calc_volume(signed=True),
                              non_manifold_edges=sum(not e.is_manifold for e in bm.edges),
                              inconsistent_edges=sum(not e.is_contiguous for e in bm.edges),
                              center_ray_clear=bvh.ray_cast((0.55,0.6,3),(0,0,-1),6)[0] is None)
            finally:
                bm.free()
        return result

checks = {}
expected = {
    '01 - Point': (1,0,0,0,0,0),
    '02 - Line': (0,1,2,0,0,0),
    '03 - Edge': (0,0,0,2,1,0),
    '04 - Face': (0,0,0,3,3,1),
    '05 - Solid': (0,0,0,5,8,5),
    '06 - Boolean': (0,0,0,16,28,12),
}
for name, counts in expected.items():
    data = inspect(name)
    assert tuple(data[k] for k in ['points','curves','curve_points','vertices','edges','faces']) == counts, (name,data)
    checks[name] = data

parameter_sets = []
for scene_name in ['05 - Solid', '06 - Boolean']:
    mod = bpy.data.scenes[scene_name].view_layers[0].objects.active.modifiers['GeometryNodes']
    sockets = [s for s in mod.node_group.interface.items_tree if s.item_type == 'SOCKET' and s.in_out == 'INPUT']
    assert [s.name for s in sockets] == ['Width','Depth','Height']
    parameter_sets.append([getattr(mod.properties.inputs, s.identifier) for s in sockets])
defaults = [[p.value for p in parameters] for parameters in parameter_sets]
variants = [('width', 0, 1.3), ('depth', 1, 1.4), ('height_0.9', 2, 0.9), ('height_1.6', 2, 1.6)]
try:
    for label, index, value in variants:
        for parameters, saved in zip(parameter_sets, defaults):
            for parameter, default in zip(parameters, saved):
                parameter.value = default
            parameters[index].value = value
        pyramid.update_tag()
        boolean.update_tag()
        solid = inspect('05 - Solid')
        cut = inspect('06 - Boolean')
        dimensions = [p.value for p in parameter_sets[0]]
        expected_volume = dimensions[0] * dimensions[1] * dimensions[2] / 3
        assert abs(solid['volume'] - expected_volume) < 1e-5, solid
        for data in (solid, cut):
            assert data['non_manifold_edges'] == 0 and data['inconsistent_edges'] == 0 and data['volume'] > 0, data
        assert cut['center_ray_clear'] and cut['volume'] < 1.5 * 1.6 * 0.45, cut
        checks[label] = {'solid':solid, 'boolean':cut}
    assert checks['height_0.9']['boolean']['volume'] > checks['06 - Boolean']['volume'] > checks['height_1.6']['boolean']['volume']
finally:
    for parameters, saved in zip(parameter_sets, defaults):
        for parameter, default in zip(parameters, saved):
            parameter.value = default
    pyramid.update_tag()
    boolean.update_tag()
    inspect('05 - Solid')
    inspect('06 - Boolean')

with open(os.path.join(FOLDER,'pyramid-sequence-verification.json'),'w',encoding='utf-8') as f:
    json.dump(checks,f,indent=2)
result = {'stages':{k:checks[k] for k in expected}, 'parameter_tests':[v[0] for v in variants], 'shared_source':True, 'exposed_inputs':['Width','Depth','Height'], 'defaults_restored':defaults}
