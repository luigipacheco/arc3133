import bpy
import os
import json
from math import radians
from mathutils import Euler

FOLDER = r'C:\Users\luigi\Documents\animaquina\class-prep\geometry101'
assert bpy.data.filepath == os.path.join(FOLDER, 'GEOMETRY101-class-ready.blend')
assert '05 - Boolean Module' not in bpy.data.node_groups

# Promote the existing exercise into the numbered lesson sequence.
scene4 = bpy.data.scenes['Scene']
scene4.name = '04 - Mesh'
original = bpy.data.node_groups['002-point in middle']
intro = next(n for n in original.nodes if n.type == 'FRAME' and n.label.startswith('NEXT'))
intro.label = '04 | MESH - MULTIPLE FACES'
intro.text.clear()
intro.text.write(
    'Four corner points + one middle point make four triangular faces.\n'
    'The first two Value nodes control X size and Y size.\n'
    'Divide by 2 finds the middle X and Y. The third Value sets its Z.\n'
    'Each MAKEFACE uses two corners and the middle to make one triangle.\n'
    'Join Geometry collects the faces. Merge by Distance welds their vertices.\n'
    'TRY: change middle Z. Result: 5 vertices / 8 edges / 4 faces.\n'
)
intro.height = 285

scene = bpy.data.scenes.new('05 - Boolean Module')
mesh = bpy.data.meshes.new('05 - Boolean Module')
obj = bpy.data.objects.new('05 - Boolean Module', mesh)
scene.collection.objects.link(obj)
scene.view_layers[0].objects.active = obj
obj.select_set(True, view_layer=scene.view_layers[0])

group = bpy.data.node_groups.new('05 - Boolean Module', 'GeometryNodeTree')
group.is_modifier = True
group.description = 'A square facade panel minus a sphere. Repeat the module later; vary Opening Radius with an attractor.'
group.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
parameters = [
    ('Width', 2.4, 2.4, 5.0, 'Panel size along X.'),
    ('Height', 2.4, 2.4, 5.0, 'Panel size along Y.'),
    ('Thickness', 0.6, 0.2, 0.6, 'Panel size along Z.'),
    ('Opening Radius', 0.95, 0.4, 1.1, 'Radius of the sphere removed from the panel. Change this first; later drive it from attractor distance.'),
]
for name, value, low, high, description in parameters:
    s = group.interface.new_socket(name=name, in_out='INPUT', socket_type='NodeSocketFloat')
    s.default_value = value
    s.min_value = low
    s.max_value = high
    s.description = description

modifier = obj.modifiers.new('GeometryNodes', 'NODES')
modifier.node_group = group

def node(kind, x, y, width=185):
    n = group.nodes.new(kind)
    n.location = (x, y)
    n.width = width
    return n

def link(source, output, target, input_):
    group.links.new(source.outputs[output], target.inputs[input_])

def frame(title, x, y, width, height, body=None):
    n = node('NodeFrame', x, y, width)
    n.label = title
    n.label_size = 20
    n.height = height
    n.shrink = False
    n.use_custom_color = True
    n.color = (0.12, 0.17, 0.22)
    if body:
        text = bpy.data.texts.new(group.name + ' | ' + title)
        text.write(body)
        n.text = text
    return n

frame('05 | BOOLEAN - A PANEL WITH AN OPENING', 0, 290, 1280, 205,
      'BOOLEAN: combine or cut intersecting solid meshes.\n'
      'DIFFERENCE: A minus B. Remove a sphere from a block.\n'
      'The sphere cuts a round opening with a curved inner surface.\n'
      'TRY: change Opening Radius in the GeometryNodes modifier.\n')

inputs = node('NodeGroupInput', 0, 0, 195)
xyz = node('ShaderNodeCombineXYZ', 245, 0)
cube = node('GeometryNodeMeshCube', 500, 0)
sphere = node('GeometryNodeMeshUVSphere', 245, -245)
sphere.inputs['Segments'].default_value = 48
sphere.inputs['Rings'].default_value = 24
smooth = node('GeometryNodeSetShadeSmooth', 500, -245)
smooth.domain = 'FACE'
boolean = node('GeometryNodeMeshBoolean', 810, -50, 205)
boolean.operation = 'DIFFERENCE'
boolean.solver = 'EXACT'
output = node('NodeGroupOutput', 1080, -50)

for name, axis in [('Width', 'X'), ('Height', 'Y'), ('Thickness', 'Z')]:
    link(inputs, name, xyz, axis)
link(xyz, 'Vector', cube, 'Size')
link(inputs, 'Opening Radius', sphere, 'Radius')
link(sphere, 'Mesh', smooth, 'Mesh')
link(cube, 'Mesh', boolean, 'Mesh 1')
link(smooth, 'Mesh', boolean, 'Mesh 2')
link(boolean, 'Mesh', output, 'Geometry')

# Explanatory text lives in frames, never as replacement node titles.
f = frame('A | BLOCK', 475, 45, 235, 250)
cube.parent = f
cube.location = (25, -45)
f = frame('B | SPHERE TO REMOVE', 220, -200, 510, 265)
sphere.parent = f
sphere.location = (25, -45)
smooth.parent = f
smooth.location = (280, -45)
frame('NEXT CLASS | ARRAYS + ATTRACTORS', 780, -275, 510, 220,
      '1. Repeat this panel in a grid.\n'
      '2. Give each panel an opening radius.\n'
      '3. Use attractor distance to vary it.\n'
      'One module, many opening sizes.\n')

for n in group.nodes:
    n.select = False

notes = bpy.data.texts['START HERE - Geometry 101']
body = notes.as_string()
body = body.replace(
    'Use the Scene selector at the top right: 01 - Point, 02 - Line, 03 - Face.\nScene is the original four-face example. All original node names and links remain.',
    'Use the Scene selector at the top right:\n01 - Point -> 02 - Line -> 03 - Face -> 04 - Mesh -> 05 - Boolean Module.\n04 - Mesh is the original four-face example. Original node names and links remain.'
)
body = body.replace('NEXT - ORIGINAL SCENE\nChoose Scene for the original 002-point in middle graph.',
                    '04 - MESH / MULTIPLE FACES\nChoose 04 - Mesh for the original 002-point in middle graph.')
addition = '''05 - BOOLEAN MODULE / PERFORATED FACADE PANEL
Two solids: a Cube and a UV Sphere, centered at the same origin.
Mesh Boolean is set to Difference: Mesh 1 minus Mesh 2, or block minus sphere.
This makes a round through-opening with a curved inner surface.
Set Shade Smooth only changes the sphere surface's shading, not its shape.

The actual node names remain visible. All teaching captions are in Frames.
Open the Modifiers tab (wrench) to change Width, Height, Thickness, Opening Radius.
Group Input passes those parameters to Combine XYZ and UV Sphere.
The allowed controls keep a rim and a through-opening for this simple exercise.
Start with Opening Radius = 0.95. Try 0.65, then 1.05; compare the opening sizes.
Restore 0.95. Try Thickness = 0.3, then restore 0.6.
Width and Height start at 2.4. The tile lies in XY; its thickness is along Z.

Ask students: What is A? What is B? What does A minus B keep?
Keep the operation on Difference for this exercise.

NEXT CLASS - ARRAYS AND ATTRACTORS
First repeat the module on a grid with spacing slightly larger than its width/height.
Then use distance from each grid point to an attractor to choose an opening radius.
For example, nearby panels can have larger openings; distant panels smaller ones.
Identical instances share their geometry. To get different opening sizes, generate
the module for each radius (for example with a For Each Geometry Element zone),
or start with a small library of radius variants. Scaling an instance also scales
its outer panel; it is not the same as changing only the opening radius.
The arrays and attractor setup are intentionally a later exercise.

'''
body = body.replace('SIMPLE CLASS ROUTINE\n', addition + 'SIMPLE CLASS ROUTINE\n')
notes.clear()
notes.write(body)
with open(os.path.join(FOLDER, 'Geometry101-teaching-notes.txt'), 'w', encoding='utf-8') as f:
    f.write(body)

bpy.context.window.scene = scene
for area in bpy.context.screen.areas:
    space = area.spaces.active
    if area.type == 'VIEW_3D':
        space.region_3d.view_rotation = Euler((radians(22), radians(-25), radians(12)), 'XYZ').to_quaternion()
        space.region_3d.view_perspective = 'ORTHO'
        space.region_3d.view_location = (0, 0, 0)
        space.region_3d.view_distance = 10.5
        space.shading.type = 'SOLID'
        space.overlay.show_cursor = False
    elif area.type == 'SPREADSHEET':
        space.geometry_component_type = 'MESH'
        space.attribute_domain = 'POINT'
    elif area.type == 'NODE_EDITOR':
        space.pin = False
        space.show_region_ui = False

result = {'scene4': scene4.name, 'new_group': group.name, 'nodes': [n.name for n in group.nodes if n.type != 'FRAME'],
          'parameters': [{'name':s.name, 'identifier':s.identifier, 'value':getattr(modifier.properties.inputs, s.identifier).value} for s in group.interface.items_tree if s.item_type=='SOCKET' and s.in_out=='INPUT']}
