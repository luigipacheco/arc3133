import bpy
import json
import os

FOLDER = r'C:\Users\luigi\Documents\animaquina\class-prep\geometry101'

def evaluate(scene_name):
    bpy.context.window.scene = bpy.data.scenes[scene_name]
    bpy.context.view_layer.update()
    obj = bpy.context.view_layer.objects.active
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    geo = evaluated.evaluated_geometry()
    mesh = geo.mesh
    points = geo.pointcloud
    return {
        'points': len(points.points) if points else 0,
        'point_positions': [list(p.co) for p in points.points] if points else [],
        'vertices': len(mesh.vertices) if mesh else 0,
        'edges': len(mesh.edges) if mesh else 0,
        'faces': len(mesh.polygons) if mesh else 0,
        'positions': [list(v.co) for v in mesh.vertices] if mesh else [],
        'area': sum(p.area for p in mesh.polygons) if mesh else 0,
    }

results = {}
for name, counts in [('01 - Point', (1, 0, 0, 0)), ('02 - Line', (0, 2, 1, 0)), ('03 - Face', (0, 3, 3, 1)), ('Scene', (0, 5, 8, 4))]:
    record = evaluate(name)
    assert tuple(record[k] for k in ('points', 'vertices', 'edges', 'faces')) == counts, (name, record)
    results[name] = record

g = bpy.data.node_groups['01 - Point']
value = g.nodes['Value'].outputs[0]
old = value.default_value
try:
    value.default_value = 2.0
    g.update_tag()
    record = evaluate('01 - Point')
    assert abs(record['point_positions'][0][0] - 2.0) < 1e-5, record
    results['point_parameter_test'] = record
finally:
    value.default_value = old
    g.update_tag()

g = bpy.data.node_groups['02 - Line']
x = g.nodes['Combine XYZ.001'].inputs['X']
old = x.default_value
try:
    x.default_value = 3.0
    g.update_tag()
    record = evaluate('02 - Line')
    assert record['vertices'] == 2 and record['edges'] == 1 and max(p[0] for p in record['positions']) == 3.0, record
    results['line_parameter_test'] = record
finally:
    x.default_value = old
    g.update_tag()

g = bpy.data.node_groups['03 - Face']
y = g.nodes['Combine XYZ.002'].inputs['Y']
x = g.nodes['Combine XYZ.002'].inputs['X']
old_x, old_y = x.default_value, y.default_value
try:
    y.default_value = 3.0
    g.update_tag()
    record = evaluate('03 - Face')
    assert record['faces'] == 1 and abs(record['area'] - 3) < 1e-5, record
    results['face_parameter_test'] = record
    x.default_value = 1.0
    y.default_value = 0.0
    g.update_tag()
    record = evaluate('03 - Face')
    assert record['area'] < 1e-6, record
    results['collinear_test'] = record
finally:
    x.default_value, y.default_value = old_x, old_y
    g.update_tag()

with open(os.path.join(FOLDER, 'verification.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

# Leave the line on screen for visual review.
evaluate('02 - Line')
for a in bpy.context.screen.areas:
    sp = a.spaces.active
    if a.type == 'SPREADSHEET':
        sp.geometry_component_type = 'MESH'
        sp.attribute_domain = 'POINT'
    elif a.type == 'VIEW_3D':
        sp.overlay.show_stats = False
        sp.region_3d.view_location = (0.85, 0.85, 0)
        sp.region_3d.view_distance = 10
result = {'checks': results}
