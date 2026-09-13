"""Append the XYZ array exercise before hexagonal arrays to the open arrays example through MCP."""
import bpy
from pathlib import Path
from hashlib import sha256
import json
import math
from mathutils import Euler, Vector

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / 'files/blender/03-arrays-lists/Arrays-Lists-Session-2.blend'
assert Path(bpy.data.filepath) == PATH
assert '03 - 3D array' not in bpy.data.scenes, 'The example already exists; inspect it before changing it'
if bpy.data.is_dirty:
    live_backup = ROOT / 'reference/archive/2026-09-12-arrays-and-individual-downloads/arrays-2-live-before-3d.blend'
    assert not live_backup.exists(), 'Inspect the existing live backup before retrying'
    bpy.ops.wm.save_as_mainfile(filepath=str(live_backup), copy=True)
backup = ROOT / 'reference/archive/2026-09-12-arrays-and-individual-downloads/arrays-2-before-3d.blend'
if not backup.exists():
    backup.write_bytes(PATH.read_bytes())
assert backup.read_bytes() == PATH.read_bytes()

for old, new in [('03 - Hexagonal array', '04 - Hexagonal array'), ('04 - Radial array', '05 - Radial array'), ('05 - If and range', '06 - If and range'), ('06 - Sine curve', '07 - Sine curve')]:
    bpy.data.scenes[old].name = new
scene = bpy.data.scenes.new('03 - 3D array')
scene.world = bpy.data.worlds.new('3D array world')
scene.world.color = (0.08, 0.08, 0.08)
mesh = bpy.data.meshes.new('3D array source')
obj = bpy.data.objects.new('03 - 3D array', mesh)
obj.color = (0.08, 0.45, 0.65, 1)
scene.collection.objects.link(obj)
bpy.context.window.scene = scene
scene.view_layers[0].objects.active = obj
obj.select_set(True)
group = bpy.data.node_groups.new('03 - 3D array', 'GeometryNodeTree')
group.is_modifier = True
group.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
controls = {}
for name, kind, default, low, high in (
    ('Count', 'NodeSocketInt', 4, 1, 20),
    ('Spacing', 'NodeSocketFloat', 1.25, 0.1, 10),
    ('Cube Size', 'NodeSocketFloat', 0.75, 0.05, 5),
):
    socket = group.interface.new_socket(name=name, in_out='INPUT', socket_type=kind)
    socket.default_value = default
    socket.min_value = low
    socket.max_value = high
    controls[name] = socket.identifier
modifier = obj.modifiers.new('GeometryNodes', 'NODES')
modifier.node_group = group

def node(kind, x, y, width=170):
    n = group.nodes.new(kind)
    n.location = (x, y)
    n.width = width
    return n

def connect(a, output, b, input):
    group.links.new(a.outputs[output], b.inputs[input])

def note(label, text, x, y, width):
    frame = node('NodeFrame', x, y, width)
    frame.label = label
    frame.shrink = False
    frame.height = 260
    frame.use_custom_color = True
    frame.color = (0.10, 0.18, 0.24)
    frame.text = bpy.data.texts.new('3D array - ' + label)
    frame.text.write(text + '\n')
    return frame

inputs = node('NodeGroupInput', -900, 500)
size = node('ShaderNodeCombineXYZ', -900, 180)
cube = node('GeometryNodeMeshCube', -680, 180)
for axis in 'XYZ':
    connect(inputs, 'Cube Size', size, axis)
connect(size, 'Vector', cube, 'Size')
previous = cube
previous_socket = 'Mesh'
for axis, x, heading, instruction in (
    ('X', -420, '1D - ROW', 'Make Count positions along X.\nInstance on Points places one cube at each position.\nCount = 4 gives 4 cubes.'),
    ('Y', 320, '2D - GRID', 'Make Count positions along Y.\nRepeat the whole row at each position.\nCount = 4 gives 4 x 4 = 16 cubes.'),
    ('Z', 1060, '3D - LAYERS', 'Make Count positions along Z.\nRepeat the whole grid at each position.\nCount = 4 gives 4 x 4 x 4 = 64 cubes.'),
):
    offset = node('ShaderNodeCombineXYZ', x, 500)
    line = node('GeometryNodeMeshLine', x + 210, 500)
    line.mode = 'OFFSET'
    instance = node('GeometryNodeInstanceOnPoints', x + 430, 180)
    connect(inputs, 'Spacing', offset, axis)
    connect(offset, 'Vector', line, 'Offset')
    connect(inputs, 'Count', line, 'Count')
    connect(line, 'Mesh', instance, 'Points')
    connect(previous, previous_socket, instance, 'Instance')
    note(heading, instruction, x, -160, 650)
    previous, previous_socket = instance, 'Instances'
output = node('NodeGroupOutput', 1740, 180)
connect(previous, previous_socket, output, 'Geometry')
note('PARAMETERS', 'Count is the number on every axis.\nSpacing is the distance between cube centers.\nCube Size controls each individual cube.\nTry Count = 3, 4 and 5.', -930, -220, 450)
note('LATER - VOLUMES', 'This is an array of separate cube instances.\nA volume stores values sampled across 3D space.\nLater, use XYZ samples to describe density or distance.', 650, -570, 1000)
for n in group.nodes:
    n.select = False

# Verify the actual number of visible leaf instances, not just the outer layers.
tests = []
for count in (3, 4, 5):
    getattr(modifier.properties.inputs, controls['Count']).value = count
    obj.update_tag()
    scene.view_layers[0].update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    actual = sum(1 for instance in depsgraph.object_instances if instance.is_instance)
    assert actual == count ** 3, (count, actual)
    tests.append({'count_per_axis': count, 'cubes': actual})
getattr(modifier.properties.inputs, controls['Count']).value = 4
obj.update_tag()
scene.view_layers[0].update()
assert all(not n.label for n in group.nodes if n.type != 'FRAME')

# Save an approachable teaching view without changing the earlier scenes.
for area in bpy.context.window.screen.areas:
    if area.type == 'VIEW_3D':
        space = area.spaces.active
        space.shading.color_type = 'OBJECT'
        space.region_3d.view_perspective = 'ORTHO'
        space.region_3d.view_location = Vector((1.875, 1.875, 1.875))
        space.region_3d.view_rotation = Euler((math.radians(65), 0, math.radians(35)), 'XYZ').to_quaternion()
        space.region_3d.view_distance = 11
    elif area.type == 'NODE_EDITOR':
        area.spaces.active.pin = False
        area.spaces.active.tree_type = 'GeometryNodeTree'
        region = next(r for r in area.regions if r.type == 'WINDOW')
        with bpy.context.temp_override(area=area, region=region):
            bpy.ops.node.view_all()
versions = bpy.context.preferences.filepaths.save_version
try:
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(PATH))
finally:
    bpy.context.preferences.filepaths.save_version = versions
result = {'file': str(PATH), 'scene': scene.name, 'tests': tests,
          'controls': list(controls), 'source_sha256': sha256(PATH.read_bytes()).hexdigest()}
(ROOT / 'reference/blender/array-3d-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
