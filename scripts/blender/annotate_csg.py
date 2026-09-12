"""Annotate the instructor's live CSG example, preserving its evaluated geometry."""
import bpy
from hashlib import sha256
import json
from pathlib import Path
import shutil
from mathutils import Euler
import math

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / 'reference/archive/2026-09-12-csg-replacement'
REPORTS = ROOT / 'reference/blender'
REPORTS.mkdir(parents=True, exist_ok=True)
target = ROOT / 'files/blender/01-intro-geometry-nodes/Intro-Geometry-Nodes.blend'
assert Path(bpy.data.filepath).name in ('csgblender.blend', target.name)
obj = bpy.context.view_layer.objects.active
group = next(m.node_group for m in obj.modifiers if m.type == 'NODES')
assert group.name == 'Geometry Nodes'

def geometry():
    obj.update_tag()
    bpy.context.view_layer.update()
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    data = {'vertices': [list(v.co) for v in mesh.vertices],
            'faces': [list(p.vertices) for p in mesh.polygons]}
    counts = {'vertices': len(mesh.vertices), 'edges': len(mesh.edges), 'faces': len(mesh.polygons)}
    evaluated.to_mesh_clear()
    return sha256(json.dumps(data, sort_keys=True).encode()).hexdigest(), counts

before_hash, counts = geometry()
before_links = sorted((l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier) for l in group.links)
native = {n.name: (n.bl_idname, n.label) for n in group.nodes if n.type != 'FRAME'}
if target.exists() and not (ARCHIVE / 'previous-intro.blend').exists():
    shutil.copy2(target, ARCHIVE / 'previous-intro.blend')
for name in ('Group Input', 'UV Sphere'):
    node = group.nodes.get(name)
    if node:
        assert not any(s.is_linked for s in list(node.inputs) + list(node.outputs))
        group.nodes.remove(node)
for node in list(group.nodes):
    if node.type == 'FRAME' and node.get('arc3133_note'):
        group.nodes.remove(node)

positions = {
    'UV Sphere.001': (0, 180), 'Cube': (220, 180), 'Mesh Boolean.001': (480, 180),
    'Cylinder': (0, -370), 'Transform Geometry': (220, -370),
    'Transform Geometry.001': (460, -370), 'Mesh Boolean': (740, -370),
    'Mesh Boolean.002': (1010, 180), 'Group Output': (1260, 180),
    'Join Geometry': (1140, -430),
}
for name, location in positions.items():
    node = group.nodes[name]
    node.parent = None
    node.location = location
    node.width = 180 if node.type != 'GROUP_OUTPUT' else 160
    node.select = False

def note(title, body, location, width, height, color):
    frame = group.nodes.new('NodeFrame')
    frame.label = title
    frame['arc3133_note'] = True
    frame.label_size = 22
    frame.shrink = False
    frame.location = location
    frame.width = width
    frame.height = height
    frame.use_custom_color = True
    frame.color = color
    text = bpy.data.texts.get('S01 - ' + title) or bpy.data.texts.new('S01 - ' + title)
    text.clear()
    text.write(body)
    frame.text = text
    return frame

note('1 | INTERSECTION', 'Keep only the volume shared by the cube and sphere.\nThe sphere clips the corners of the cube.',
     (-25, 390), 760, 120, (.17, .25, .31))
note('2 | ROTATION + UNION', 'The original cylinder points along Z. Rotate copies 90 degrees\naround X and Y, then merge all three with Union.',
     (-25, -165), 970, 130, (.20, .27, .19))
note('3 | DIFFERENCE', 'Mesh 1 = the solid. Mesh 2 = the cutters.\nSubtract the cylinders to make three openings.',
     (975, 390), 650, 120, (.29, .20, .15))
note('OPTIONAL | JOIN GEOMETRY', 'Join Geometry collects both meshes.\nIt does not calculate a solid union.\nConnect it to Group Output to compare.',
     (1000, -180), 610, 155, (.22, .22, .22))
note('PARAMETERS + VECTORS', 'Parameter = a value you can change, such as Radius.\nVector = three components: X, Y and Z.\nTransform Geometry can move, rotate and scale.\nTry changing Cylinder Radius, then undo and change Cube Size.',
     (-25, -835), 1635, 175, (.16, .20, .27))

after_hash, after_counts = geometry()
assert after_hash == before_hash and after_counts == counts, 'Annotation changed the geometry'
assert before_links == sorted((l.from_node.name, l.from_socket.identifier, l.to_node.name, l.to_socket.identifier) for l in group.links)
assert all((n.bl_idname, n.label) == native[n.name] for n in group.nodes if n.type != 'FRAME')
bpy.context.scene.name = '01 - CSG example'
obj.color = (.43, .58, .67, 1)
for area in bpy.context.screen.areas:
    region = next((r for r in area.regions if r.type == 'WINDOW'), None)
    if area.type == 'NODE_EDITOR':
        area.spaces.active.pin = False
        area.spaces.active.show_region_ui = False
        with bpy.context.temp_override(area=area, region=region):
            bpy.ops.node.view_all()
    elif area.type == 'VIEW_3D':
        space = area.spaces.active
        space.show_region_ui = False
        space.region_3d.view_perspective = 'ORTHO'
        space.region_3d.view_rotation = Euler((math.radians(65), 0, math.radians(30)), 'XYZ').to_quaternion()
        space.shading.type = 'SOLID'
        space.shading.color_type = 'OBJECT'
        with bpy.context.temp_override(area=area, region=region):
            bpy.ops.view3d.view_selected(use_all_regions=False)
        space.region_3d.view_distance *= 1.25

previous_versions = bpy.context.preferences.filepaths.save_version
try:
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(target))
finally:
    bpy.context.preferences.filepaths.save_version = previous_versions
result = {'session': 'S01', 'file': target.relative_to(ROOT).as_posix(),
          'scene': bpy.context.scene.name, 'group': group.name,
          'geometry_unchanged': before_hash == after_hash, 'geometry_sha256': after_hash,
          'counts': counts, 'native_names_preserved': True, 'frames': 5,
          'removed_disconnected_nodes': ['Group Input', 'UV Sphere'],
          'sha256': sha256(target.read_bytes()).hexdigest()}
(REPORTS / 'csg-annotation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
