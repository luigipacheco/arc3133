import bpy
import os

FOLDER = r'C:\Users\luigi\Documents\animaquina\class-prep\geometry101'
assert bpy.data.filepath == os.path.join(FOLDER, 'GEOMETRY101-class-ready.blend')
assert '03 - Edge' not in bpy.data.scenes

def rewrite_frame(n, title, body, height=None):
    n.label = title
    if n.text:
        # Copied graphs must not share editable teaching captions.
        n.text = n.text.copy()
    else:
        n.text = bpy.data.texts.new(title)
    n.text.clear()
    n.text.write(body.rstrip() + '\n')
    if height is not None:
        n.height = height

def new_frame(g, title, x, y, width, height, body=None):
    n = g.nodes.new('NodeFrame')
    n.label = title
    n.label_size = 20
    n.location = (x, y)
    n.width, n.height = width, height
    n.shrink = False
    n.use_custom_color = True
    n.color = (0.12, 0.17, 0.22)
    if body:
        n.text = bpy.data.texts.new(g.name + ' | ' + title)
        n.text.write(body.rstrip() + '\n')
    return n

def new_node(g, kind, x, y, width=175, parent=None):
    n = g.nodes.new(kind)
    n.width = width
    if parent:
        n.parent = parent
    n.location = (x, y)
    return n

def link(g, a, a_socket, b, b_socket):
    g.links.new(a.outputs[a_socket], b.inputs[b_socket])

# Keep the existing mesh-edge example, and introduce the curve one step earlier.
line = bpy.data.node_groups['02 - Line']
edge = line.copy()
edge.name = '03 - Edge'
scene = bpy.data.scenes.new('03 - Edge')
obj = bpy.data.objects.new('03 - Edge', bpy.data.meshes.new('03 - Edge'))
scene.collection.objects.link(obj)
scene.view_layers[0].objects.active = obj
obj.select_set(True, view_layer=scene.view_layers[0])
mod = obj.modifiers.new('GeometryNodes', 'NODES')
mod.node_group = edge
rewrite_frame(edge.nodes['Frame'], '03 | EDGE',
    'VERTEX: a point belonging to a mesh. Plural: vertices.\n'
    'EDGE: a connection between two mesh vertices.\n'
    'Curve to Mesh converts the line to an edge; leave Profile Curve empty.\n'
    'Same line shape, now mesh data. TRY: change X on B.', 205)

line.nodes.remove(line.nodes['Curve to Mesh'])
link(line, line.nodes['Points to Curves'], 'Curves', line.nodes['Group Output'], 'Geometry')
line.nodes['Group Output'].location = (900, -65)
rewrite_frame(line.nodes['Frame'], '02 | LINE',
    'LINE: here, a straight segment connecting A and B.\n'
    'Join Geometry collects the points; Points to Curves connects them.\n'
    'Blender represents this line as a curve with two control points.\n'
    'TRY: change X on B. There are no mesh vertices or edges yet.', 205)
rewrite_frame(line.nodes['Frame.003'], 'RESULT | 1 curve / 2 control points',
    'In the Spreadsheet, choose Curve > Control Point.', 110)

# Face remains the same triangle; only its position in the sequence changes.
bpy.data.scenes['03 - Face'].name = '04 - Face'
face = bpy.data.node_groups['03 - Face']
face.name = '04 - Face'
bpy.data.objects['03 - Face'].name = '04 - Face'
face.nodes['Frame'].label = '04 | FACE'

# Complete the user's own four-corner + apex mesh with its missing base.
bpy.data.scenes['04 - Mesh'].name = '05 - Solid'
pyramid = bpy.data.node_groups['002-point in middle']
pyramid.nodes['Value.002'].outputs[0].default_value = 1.2
pyramid.nodes['Frame.005'].label = 'PARAMETER | width X'
pyramid.nodes['Frame.006'].label = 'PARAMETER | depth Y'
pyramid.nodes['Frame.007'].label = 'PARAMETER | height Z'
pyramid.nodes['Frame.002'].label = 'APEX | (X/2, Y/2, Z)'
rewrite_frame(pyramid.nodes['Frame.008'], '05 | SOLID - A PYRAMID MADE FROM A MESH',
    'Three Value parameters: width X, depth Y, height Z.\n'
    'Four corners stay on Z = 0. The apex is (X/2, Y/2, Z).\n'
    'Your four triangles make the sides. Add the bottom face to close the mesh.\n'
    'A closed mesh encloses a volume: 5 vertices / 8 edges / 5 faces.\n'
    'TRY: change height Z. The next exercise uses this same pyramid.', 250)

base_frame = new_frame(pyramid, 'BOTTOM FACE | close the mesh', -80, -915, 900, 255)
join = new_node(pyramid, 'GeometryNodeJoinGeometry', 25, -55, parent=base_frame)
curve = new_node(pyramid, 'GeometryNodePointsToCurves', 245, -55, parent=base_frame)
fill = new_node(pyramid, 'GeometryNodeFillCurve', 465, -55, parent=base_frame)
fill.inputs['Mode'].default_value = 'N-gons'
flip = new_node(pyramid, 'GeometryNodeFlipFaces', 685, -55, parent=base_frame)
for name in ['Points', 'Points.001', 'Points.003', 'Points.004']:
    link(pyramid, pyramid.nodes[name], 'Points', join, 'Geometry')
link(pyramid, join, 'Geometry', curve, 'Points')
link(pyramid, curve, 'Curves', fill, 'Curve')
link(pyramid, fill, 'Mesh', flip, 'Mesh')
link(pyramid, flip, 'Mesh', pyramid.nodes['Join Geometry.004'], 'Geometry')
new_frame(pyramid, 'WHY A BOTTOM FACE?', 875, -910, 590, 230,
    'Four sides alone leave an open mesh.\n'
    'Fill Curve makes the base at Z = 0.\n'
    'Flip Faces points its normal downward.\n'
    'Merge by Distance joins shared corners.')

# Replace the sphere lesson with the user's shared pyramid as the cutter.
bpy.data.scenes['05 - Boolean Module'].name = '06 - Boolean'
boolean_obj = bpy.data.objects['05 - Boolean Module']
boolean_obj.name = '06 - Boolean'
boolean = bpy.data.node_groups.new('06 - Boolean', 'GeometryNodeTree')
boolean.is_modifier = True
boolean.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
boolean.description = 'Subtract the pyramid built from points in 05 - Solid from a cube. The pyramid group is shared.'
boolean_obj.modifiers['GeometryNodes'].node_group = boolean
new_frame(boolean, '06 | BOOLEAN - CUBE MINUS OUR PYRAMID', 0, 300, 1230, 205,
    'Start with two closed solids: a cube and the pyramid from 05.\n'
    'DIFFERENCE = A minus B. Remove the overlapping pyramid volume.\n'
    'Transform Geometry places the cube across the pyramid.\n'
    'Change the three Value nodes in 05; this cut updates too.')

frame = new_frame(boolean, 'A | CUBE', 0, 30, 495, 370)
cube = new_node(boolean, 'GeometryNodeMeshCube', 25, -50, 190, frame)
cube.inputs['Size'].default_value = (1.5, 1.6, 0.45)
transform = new_node(boolean, 'GeometryNodeTransform', 270, -50, 200, frame)
transform.inputs['Translation'].default_value = (0.55, 0.6, 0.4)
link(boolean, cube, 'Mesh', transform, 'Geometry')
frame = new_frame(boolean, 'B | OUR PYRAMID FROM 05', 0, -395, 495, 190)
pyramid_node = new_node(boolean, 'GeometryNodeGroup', 25, -50, 300, frame)
pyramid_node.node_tree = pyramid
pyramid_node.inputs['Geometry'].hide = True
operation = new_node(boolean, 'GeometryNodeMeshBoolean', 635, -60, 210)
operation.operation = 'DIFFERENCE'
operation.solver = 'EXACT'
output = new_node(boolean, 'NodeGroupOutput', 975, -60, 195)
link(boolean, transform, 'Geometry', operation, 'Mesh 1')
link(boolean, pyramid_node, 'Geometry', operation, 'Mesh 2')
link(boolean, operation, 'Mesh', output, 'Geometry')
new_frame(boolean, 'ONE PYRAMID - SHARED PARAMETERS', 595, -360, 635, 205,
    'Select the pyramid group and press Tab to inspect it.\n'
    'Its original node-group name is kept.\n'
    'Later: array this block and vary pyramid height\n'
    'with attractor distance to change the openings.')

# The old sphere graph is no longer part of the teaching file; the backup retains it.
old = bpy.data.node_groups.get('05 - Boolean Module')
if old and old.users == 0:
    bpy.data.node_groups.remove(old)
for g in (line, edge, face, pyramid, boolean):
    for n in g.nodes:
        n.select = False

notes = '''GEOMETRY 101 - FROM A POINT TO A BOOLEAN

Use the Scene selector at the top right:
01 - Point -> 02 - Line -> 03 - Edge -> 04 - Face -> 05 - Solid -> 06 - Boolean.
The captions are Frames. Actual nodes keep their original Blender names.
Home fits the node graph. Use the wheel to zoom. Ctrl+Space maximizes an editor.

WORDS
Parameter: a value we can change to control a result.
Vector: an (X, Y, Z) quantity with direction and magnitude (size).
Here a position vector locates a point relative to the object's origin.
Point: a location. A mathematical point has no size.
Line: a geometric idea; here a straight segment represented as a Blender curve.
Vertex: a point belonging to a mesh. Plural: vertices.
Edge: a connection between two mesh vertices.
Face: a surface bounded by edges.
Solid: a shape enclosing a volume; here represented by a closed mesh surface.
Boolean Difference: remove the overlapping volume of solid B from solid A.

01 - POINT
Value -> Combine XYZ -> Points -> Group Output.
Try Value = 1, then 2. One point moves along X. Radius makes it visible.
The output is a point cloud, not yet a mesh. Spreadsheet: Point Cloud > Point.

02 - LINE
Two points: A=(0,0,0), B=(2,0,0).
Join Geometry collects them. Points to Curves connects them into one curve.
Try B's X=3. Spreadsheet: Curve > Control Point, 2 points; Curve > Spline, 1.
A straight Blender curve represents the line. This output has no mesh edges.

03 - EDGE
Add Curve to Mesh after Points to Curves. Leave Profile Curve empty.
The shape looks the same, but the data is now a mesh: 2 vertices, 1 edge, 0 faces.
Spreadsheet: Mesh > Vertex, Edge, Face. A vertex is a mesh point.

04 - FACE
Add C=(0,2,0). Fill Curve closes and fills a triangle in the XY plane.
Keep Z=0. Result: 3 vertices, 3 edges, 1 face. It has no enclosed volume.
Try changing C's Y. If C lies on AB, the triangle has zero area.

05 - SOLID / A PYRAMID FROM SCRATCH
Use the original 002-point in middle group.
The three Value nodes control width X, depth Y, and height Z.
Defaults: X=1.1, Y=1.2, Z=1.2.
The four corners are (0,0,0), (0,Y,0), (X,Y,0), and (X,0,0).
Divide by 2 puts the apex at (X/2,Y/2,Z).
The existing four MAKEFACE groups each form a triangular side.
The new bottom branch joins the four corners, makes a curve, and fills its face.
Flip Faces points the bottom outward, downward. Merge by Distance welds corners.
Four side faces plus one bottom face close the mesh and enclose volume.
Result: 5 vertices, 8 edges, 5 faces. Volume = X * Y * Z / 3.
Try height Z=0.9, 1.2, then 1.6. Restore 1.2 for the saved starting example.
This is the same pyramid used in the Boolean exercise, not a separate copy.

06 - BOOLEAN / CUBE MINUS PYRAMID
A: Cube -> Transform Geometry. B: the shared 002-point in middle group.
Mesh Boolean uses Difference: Mesh 1 minus Mesh 2.
Cube Size=(1.5,1.6,0.45); Translation=(0.55,0.6,0.4).
The cube crosses the pyramid, leaving a tapered square through-opening.
Select the pyramid group and press Tab to inspect its point/face construction.
Change its three Value parameters, or change them in 05 - Solid; both update.
Keep positive pyramid dimensions. For the starting cube, try pyramid heights
0.9 to 1.6 to compare the opening sizes. The cube remains a fixed reference.

LATER - ARRAYS AND ATTRACTORS
Repeat the cut block in a grid. Vary pyramid height to vary the opening size.
Attractor distance can determine that height for each generated module.
Identical instances share geometry: different cuts require generating variants
or generating each module with its own height. Scaling an instance scales the
whole block and is not the same as changing only its pyramid cutter.
This file prepares the single module; arrays and attractors are the next lesson.

CLASS ROUTINE
Predict -> change one parameter -> observe -> explain -> restore.
Ask: What changed between line and edge? When does a mesh become a solid?
Why does the pyramid need a bottom face before it is used as a Boolean solid?
'''
text = bpy.data.texts['START HERE - Geometry 101']
text.clear()
text.write(notes)
with open(os.path.join(FOLDER, 'Geometry101-teaching-notes.txt'), 'w', encoding='utf-8') as f:
    f.write(notes)

bpy.context.window.scene = bpy.data.scenes['05 - Solid']
result = {'scenes': [s.name for s in bpy.data.scenes], 'shared_pyramid': pyramid_node.node_tree.name,
          'boolean_nodes': [n.name for n in boolean.nodes if n.type != 'FRAME'],
          'pyramid_parameters': {n.name:n.outputs[0].default_value for n in pyramid.nodes if n.bl_idname=='ShaderNodeValue'}}
