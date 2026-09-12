import bpy
import json
import os
from mathutils import Quaternion

FOLDER = r'C:\Users\luigi\Documents\animaquina\class-prep\geometry101'
original = bpy.data.node_groups['002-point in middle']
original.use_fake_user = True
original_face = bpy.data.node_groups['MAKEFACE']
original_face.use_fake_user = True

def snapshot(group):
    return {
        'nodes': {n.name: {'type': n.bl_idname, 'label': n.label} for n in group.nodes if n.type != 'FRAME'},
        'links': sorted([l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier] for l in group.links),
        'values': {n.name: n.outputs[0].default_value for n in group.nodes if n.bl_idname == 'ShaderNodeValue'},
    }

baseline = {g.name: snapshot(g) for g in (original, original_face)}
with open(os.path.join(FOLDER, 'original-node-record.json'), 'w', encoding='utf-8') as f:
    json.dump(baseline, f, indent=2)

def text_block(name, body):
    text = bpy.data.texts.new(name)
    text.write(body)
    return text

def frame(group, title, x, y, width=400, height=170, body=None, color=(0.12, 0.17, 0.22)):
    n = group.nodes.new('NodeFrame')
    n.label = title
    n.label_size = 20
    n.use_custom_color = True
    n.color = color
    n.shrink = False
    n.location = (x, y)
    n.width = width
    n.height = height
    if body:
        n.text = text_block(group.name + ' | ' + title, body)
    return n

def node(group, kind, x, y, width=165, parent=None):
    n = group.nodes.new(kind)
    n.width = width
    if parent:
        n.parent = parent
    n.location = (x, y)
    return n

def connect(group, source, output, dest, input_):
    group.links.new(source.outputs[output], dest.inputs[input_])

def new_lesson(name):
    assert name not in bpy.data.scenes, 'Lesson scene already exists: ' + name
    scene = bpy.data.scenes.new(name)
    scene.unit_settings.system = 'NONE'
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    obj.select_set(True, view_layer=scene.view_layers[0])
    scene.view_layers[0].objects.active = obj
    group = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    group.is_modifier = True
    group.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    modifier = obj.modifiers.new('GeometryNodes', 'NODES')
    modifier.node_group = group
    return scene, obj, group

# 01: one editable number, one vector, one point. No custom node titles.
s1, o1, g1 = new_lesson('01 - Point')
frame(g1, '01 | POINT', 0, 290, 1050, 205,
      'PARAMETER: a value we can change. Try Value = 0, 1, then 2.\n'
      'VECTOR: (X, Y, Z) describes direction and size.\n'
      'Here it is a position: an offset from the object origin.\n'
      'POINT: a location. Points creates a point cloud, not a mesh.\n'
      'The dot has display radius; a mathematical point has no size.')
f = frame(g1, 'PARAMETER', 0, 25, 210, 190)
v = node(g1, 'ShaderNodeValue', 22, -45, parent=f)
v.outputs[0].default_value = 1.0
f = frame(g1, 'VECTOR', 265, 25, 210, 235)
xyz = node(g1, 'ShaderNodeCombineXYZ', 22, -45, parent=f)
f = frame(g1, 'POINT', 530, 25, 210, 245)
p = node(g1, 'GeometryNodePoints', 22, -45, parent=f)
p.inputs['Count'].default_value = 1
p.inputs['Radius'].default_value = 0.06
out = node(g1, 'NodeGroupOutput', 845, -20)
connect(g1, v, 0, xyz, 'X')
connect(g1, xyz, 'Vector', p, 'Position')
connect(g1, p, 'Points', out, 'Geometry')

def point_pair(group, title, coord, y):
    f = frame(group, title, 0, y, 390, 210)
    xyz = node(group, 'ShaderNodeCombineXYZ', 20, -43, parent=f)
    for socket, value in zip(('X', 'Y', 'Z'), coord):
        xyz.inputs[socket].default_value = value
    pts = node(group, 'GeometryNodePoints', 215, -43, parent=f)
    pts.inputs['Count'].default_value = 1
    pts.inputs['Radius'].default_value = 0.06
    connect(group, xyz, 'Vector', pts, 'Position')
    return xyz, pts

# 02: the same points, connected into a curve, then converted to a mesh edge.
s2, o2, g2 = new_lesson('02 - Line')
frame(g2, '02 | LINE / EDGE', 0, 280, 1260, 195,
      'VERTEX (plural: vertices): one point in a mesh.\n'
      'EDGE: a connection between two mesh vertices.\n'
      'Join Geometry collects points; Points to Curves connects them.\n'
      'Curve to Mesh, with no profile, makes vertices and edges.\n'
      'TRY: change X on the second Combine XYZ. Watch the line length.')
xa, pa = point_pair(g2, 'A | (0, 0, 0)', (0, 0, 0), 30)
xb, pb = point_pair(g2, 'B | change X', (2, 0, 0), -210)
j = node(g2, 'GeometryNodeJoinGeometry', 445, -65)
c = node(g2, 'GeometryNodePointsToCurves', 655, -65)
m = node(g2, 'GeometryNodeCurveToMesh', 865, -65)
out = node(g2, 'NodeGroupOutput', 1080, -65)
for point in (pa, pb):
    connect(g2, point, 'Points', j, 'Geometry')
connect(g2, j, 'Geometry', c, 'Points')
connect(g2, c, 'Curves', m, 'Curve')
connect(g2, m, 'Mesh', out, 'Geometry')
frame(g2, 'RESULT | 2 vertices / 1 edge / 0 faces', 440, -290, 825, 110,
      'Read the counts in the Spreadsheet.\nA straight line segment has no surface area.')

# 03: add a third point and fill the boundary. Keep Z=0 for Fill Curve.
s3, o3, g3 = new_lesson('03 - Face')
frame(g3, '03 | FACE', 0, 265, 1260, 185,
      'FACE: a filled surface bounded by edges.\n'
      'Three points not on one straight line can make a triangle.\n'
      'Fill Curve closes and fills the boundary in the XY plane.\n'
      'Keep Z = 0 here. TRY: change X on B or Y on C.')
xa, pa = point_pair(g3, 'A | (0, 0, 0)', (0, 0, 0), 30)
xb, pb = point_pair(g3, 'B | change X', (2, 0, 0), -200)
xc, pc = point_pair(g3, 'C | change Y', (0, 2, 0), -430)
j = node(g3, 'GeometryNodeJoinGeometry', 445, -140)
c = node(g3, 'GeometryNodePointsToCurves', 655, -140)
f = node(g3, 'GeometryNodeFillCurve', 865, -140)
out = node(g3, 'NodeGroupOutput', 1080, -140)
for point in (pa, pb, pc):
    connect(g3, point, 'Points', j, 'Geometry')
connect(g3, j, 'Geometry', c, 'Points')
connect(g3, c, 'Curves', f, 'Curve')
connect(g3, f, 'Mesh', out, 'Geometry')
frame(g3, 'RESULT | 3 vertices / 3 edges / 1 face', 440, -385, 825, 125,
      'A triangle is the simplest mesh face.\nMake C lie on AB: the area becomes zero.\nUndo to bring the face back.')

# Keep the existing extension's node names, values, and wiring.
# Give the overlapping Divide nodes enough space, and explain the controls.
for name, title, pos in [
    ('Value', 'PARAMETER | X size', (-950, 60)),
    ('Value.001', 'PARAMETER | Y size', (-950, -130)),
    ('Value.002', 'PARAMETER | middle Z', (-950, -320)),
]:
    f = frame(original, title, *pos, width=235, height=145)
    n = original.nodes[name]
    n.parent = f
    n.location = (30, -45)
    n.width = 175
original.nodes['Math'].location = (-620, -130)
original.nodes['Math.001'].location = (-420, -130)
original.nodes['Group Input'].location = (-620, 120)
frame(original, 'NEXT | FOUR FACES + A MIDDLE POINT', -950, 670, 1640, 235,
      'Start with scenes 01 - Point, 02 - Line, and 03 - Face.\n'
      'Here, four corners share X and Y parameters.\n'
      'Divide by 2 finds the middle X and middle Y. The third Value sets its Z.\n'
      'Each MAKEFACE uses two corners and the middle point to make one triangle.\n'
      'Join Geometry collects the faces. Merge by Distance welds shared vertices.\n'
      'Expected result: 5 vertices / 8 edges / 4 faces.')
frame(original_face, 'MAKEFACE | YOUR EXISTING TRIANGLE GROUP', -440, 485, 1080, 220,
      'Used by the original middle-point example.\n'
      'Points to Curves connects the points. Fill Curve makes a flat face.\n'
      'Position + Index + Sample Index read the original point positions.\n'
      'Set Position restores their 3D coordinates, including the middle Z.\n'
      'This is a later exercise; use scene 03 for the first face lesson.')

notes = '''GEOMETRY 101 - TEACHING NOTES

Use the Scene selector at the top right: 01 - Point, 02 - Line, 03 - Face.
Scene is the original four-face example. All original node names and links remain.
If the graph is off screen, place the mouse in the node editor and press Home.
The explanatory titles belong to Frames. The actual nodes keep Blender names.

WORDS TO INTRODUCE
Parameter: a value we can change to control a result.
Vector: an (X, Y, Z) quantity with direction and magnitude (size).
Here a position vector locates a point relative to the object's origin.
Point: a location. A mathematical point has no size.
Vertex: a point belonging to a mesh. Plural: vertices.
Edge: a connection between two mesh vertices.
Face: a filled surface bounded by edges.

01 - POINT
Follow Value -> Combine XYZ -> Points -> Group Output.
Ask students to predict what changes when Value goes from 1 to 2.
Change it, observe, and return to 1. Then try Y and Z on Combine XYZ.
Count stays 1. Radius makes the dot visible; it does not add mesh faces.
Points outputs a point cloud. In the Spreadsheet choose Point Cloud > Point.
A point cloud point is not yet a mesh vertex. Points to Vertices is the native
conversion node if you want an optional extra exercise later.

02 - LINE
Read A=(0,0,0), B=(2,0,0). Both points are in the same object coordinates.
Join Geometry collects their data; it does not create an edge on its own.
Points to Curves connects the points. Curve to Mesh has no Profile Curve.
The result is 2 vertices, 1 edge, 0 faces. Choose Mesh > Vertex in Spreadsheet.
Change B's X from 2 to 3. Predict, observe, and restore it to 2.
The Combine XYZ inputs are parameters too; a Value node is not required.

03 - FACE
Add C=(0,2,0). Fill Curve closes and fills the three-point boundary.
The result is 3 vertices, 3 edges, 1 face. Inspect each Spreadsheet domain.
Keep Z=0 because Fill Curve fills in the XY plane.
Change C's Y to 3. Then make C=(1,0,0): the points are collinear, area is zero.
Undo to restore the triangle. Three points need not always produce a face.

NEXT - ORIGINAL SCENE
Choose Scene for the original 002-point in middle graph.
X and Y define the rectangle. Divide by 2 finds the middle. Z raises it.
Four MAKEFACE groups build four triangles. Merge by Distance welds them.
Original parameters: X=1.1, Y=1.2, middle Z=0.2.
Expected topology: 5 vertices, 8 edges, 4 faces.
MAKEFACE contains a later topic: restoring 3D positions after Fill Curve.

SIMPLE CLASS ROUTINE
For each example: predict -> change one parameter -> observe -> explain.
Finish by asking students to identify one parameter, vector, vertex, edge, face.

REFERENCE
Blender Manual: Curve to Mesh (unconnected profile gives mesh edges)
https://docs.blender.org/manual/en/4.4/modeling/geometry_nodes/curve/operations/curve_to_mesh.html
Blender source: Fill Curve (curves treated as cyclic and projected to XY)
https://github.com/blender/blender/blob/main/source/blender/nodes/geometry/nodes/node_geo_curve_fill.cc
'''
text_block('START HERE - Geometry 101', notes)
with open(os.path.join(FOLDER, 'Geometry101-teaching-notes.txt'), 'w', encoding='utf-8') as f:
    f.write(notes)

for g in (g1, g2, g3):
    for n in g.nodes:
        n.select = False

bpy.context.window.scene = s1
for area in bpy.context.screen.areas:
    space = area.spaces.active
    if area.type == 'NODE_EDITOR':
        space.pin = False
        space.show_region_ui = False
        space.show_region_toolbar = False
    elif area.type == 'VIEW_3D':
        space.shading.type = 'SOLID'
        space.overlay.show_cursor = False
        space.overlay.show_stats = True
        space.region_3d.view_perspective = 'ORTHO'
        space.region_3d.view_rotation = Quaternion((1, 0, 0, 0))
        space.region_3d.view_location = (1, 0.65, 0)
        space.region_3d.view_distance = 7
    elif area.type == 'SPREADSHEET':
        space.object_eval_state = 'EVALUATED'
        space.geometry_component_type = 'POINTCLOUD'
        space.attribute_domain = 'POINT'

result = {'created_scenes': [s1.name, s2.name, s3.name],
          'original_preserved': {g.name: snapshot(g) == baseline[g.name] for g in (original, original_face)},
          'notes': 'START HERE - Geometry 101'}
