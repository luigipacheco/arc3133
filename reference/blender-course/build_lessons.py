"""Build the ARC 3133 teaching files in a separate Blender process.

The live project is never reset by this script. Use --lesson ID after Blender's
-- separator. Existing outputs are backed up before an explicitly requested
rebuild. Native node names and labels are left untouched; explanations are Frames.
"""
import argparse
import bpy
import bmesh
import json
import math
from mathutils import Vector, Euler
from pathlib import Path
import shutil
import struct

ROOT = Path(__file__).resolve().parents[2]
FILES = ROOT / 'files/blender'
REFERENCE = ROOT / 'reference/blender-course'
TEMPLATE = REFERENCE / 'preparation-archive/before-new-lessons.blend'
CATALOG = {
    'intro': ('01-intro-geometry-nodes', 'Intro-Geometry-Nodes.blend', '01 · Intro to Geometry Nodes'),
    'arrays': ('03-arrays-lists', 'Arrays-and-Lists.blend', '03 · Arrays and Lists'),
    'attractors': ('04-attractors', 'Attractors.blend', '04 · Attractors'),
    'tessellation': ('05-tessellation-lattices', 'Tessellation-and-Lattices.blend', '05 · Tessellation and Lattices'),
    'clouds': ('06-point-clouds-volumes', 'Point-Clouds-and-Volumes.blend', '06 · Point Clouds and Volumes'),
    'volumes': ('07-advanced-volumes', 'Advanced-Volumes.blend', '07 · Advanced Volumes'),
    'discretization': ('08-discretizing-geometry', 'Discretizing-Geometry.blend', '08 · Discretizing Geometry'),
    'fabrication': ('09-final-project', 'Final-Project-Fabrication.blend', '09 · Final Project — Fabrication'),
}
SCENES = []
NOTES = []
CURRENT = None
SPLIT_SESSIONS = {
    'arrays': [('Arrays-Lists-Session-1.blend',['01 - Linear loop','02 - Nested grid']),
               ('Arrays-Lists-Session-2.blend',['03 - Hexagonal array','04 - Radial array','05 - If and range','06 - Sine curve'])],
    'volumes': [('Advanced-Volumes-Session-1.blend',['01 - Mesh to SDF','02 - Signed distance','03 - SDF Boolean']),
                ('Advanced-Volumes-Session-2.blend',['04 - Noise field'])],
    'discretization': [('Discretizing-Geometry-Session-1.blend',['01 - One contour','02 - Contour stack']),
                      ('Discretizing-Geometry-Session-2.blend',['03 - Section parts','04 - Laid out parts'])],
}
PALETTE = [(0.49, 0.64, 0.76, 1), (0.87, 0.49, 0.23, 1), (0.57, 0.68, 0.42, 1)]


def source_path(lesson):
    folder,name,_=CATALOG[lesson]
    return REFERENCE/'lesson-masters'/name if lesson in SPLIT_SESSIONS else FILES/folder/name


def native(g, kind, x=0, y=0, width=180):
    n = g.nodes.new(kind)
    n.location = (x, y)
    n.width = width
    return n


def sock(n, key, output=False):
    sockets = n.outputs if output else n.inputs
    if isinstance(key, int):
        return sockets[key]
    matches = [s for s in sockets if s.name == key and s.enabled]
    return matches[0] if matches else sockets[key]


def link(g, a, ak, b, bk):
    g.links.new(sock(a, ak, True), sock(b, bk))


def value(n, key, v):
    sock(n, key).default_value = v


def frame(g, title, body, x=-300, y=350, width=1150, height=150):
    f = native(g, 'NodeFrame', x, y, width)
    f.label, f.label_size = title, 24
    f.shrink = False
    f.height = max(height, 100 + 40 * len(body.rstrip().splitlines()))
    f.width = max(width, max((len(line) for line in body.splitlines()), default=0) * 15)
    f.use_custom_color = True
    f.color = (0.12, 0.17, 0.22)
    if body:
        f.text = bpy.data.texts.new(g.name + ' | ' + title)
        f.text.write(body.rstrip() + '\n')
    return f


def interface(g, name, typ='NodeSocketFloat', default=None, low=None, high=None, description=''):
    s = g.interface.new_socket(name=name, in_out='INPUT', socket_type=typ)
    if default is not None:
        s.default_value = default
    if low is not None and hasattr(s, 'min_value'):
        s.min_value = low
    if high is not None and hasattr(s, 'max_value'):
        s.max_value = high
    s.description = description
    # In 5.2 the modifier receives a socket before its interface default is set.
    # Seed the matching modifier control after assigning the teaching default.
    if default is not None:
        for obj in bpy.data.objects:
            for m in obj.modifiers:
                if m.type == 'NODES' and m.node_group == g:
                    getattr(m.properties.inputs, s.identifier).value = default
    return s


def group(name):
    g = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    g.is_modifier = True
    g.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    return g


def output(g, n, socket='Geometry', x=1000, y=0):
    out = native(g, 'NodeGroupOutput', x, y)
    link(g, n, socket, out, 'Geometry')
    return out


def math_node(g, operation, x, y, a=None, b=None):
    n = native(g, 'ShaderNodeMath', x, y, 150)
    n.operation = operation
    if a is not None:
        value(n, 0, a)
    if b is not None:
        value(n, 1, b)
    return n


def object_for(scene, g, name=None, color=0):
    obj = bpy.data.objects.new(name or g.name, bpy.data.meshes.new(name or g.name))
    scene.collection.objects.link(obj)
    m = obj.modifiers.new('GeometryNodes', 'NODES')
    m.node_group = g
    obj.color = PALETTE[color]
    scene.view_layers[0].objects.active = obj
    obj.select_set(True, view_layer=scene.view_layers[0])
    return obj


def lesson_scene(name, title, explanation, width=1150):
    s = bpy.data.scenes.new(name)
    s.unit_settings.system = 'NONE'
    s.render.engine = 'BLENDER_WORKBENCH'
    s.display.shading.light = 'STUDIO'
    s.display.shading.color_type = 'OBJECT'
    s.display.shading.show_shadows = True
    s.display.shading.show_cavity = True
    s.display.shading.cavity_type = 'BOTH'
    s.display.shading.background_type = 'WORLD'
    s.world = bpy.data.worlds.new(name)
    s.world.color = (0.11, 0.12, 0.14)
    s.render.resolution_x, s.render.resolution_y = 1280, 900
    s.render.resolution_percentage = 100
    s.render.image_settings.file_format = 'PNG'
    g = group(name)
    obj = object_for(s, g)
    frame(g, title, explanation, width=width)
    SCENES.append(s)
    NOTES.append((name, title, explanation))
    return s, obj, g


def cube(g, x=0, y=0, size=(1, 1, 1)):
    n = native(g, 'GeometryNodeMeshCube', x, y)
    value(n, 'Size', size)
    for k in ('Vertices X', 'Vertices Y', 'Vertices Z'):
        value(n, k, 2)
    return n


def cylinder(g, x=0, y=0, radius=0.75, depth=2.6, resolution=48):
    n = native(g, 'GeometryNodeMeshCylinder', x, y)
    n.fill_type = 'NGON'
    value(n, 'Vertices', resolution)
    value(n, 'Radius', radius)
    value(n, 'Depth', depth)
    return n


def transform(g, src, socket='Mesh', x=250, y=0, translation=None, rotation=None, scale=None):
    n = native(g, 'GeometryNodeTransform', x, y, 200)
    link(g, src, socket, n, 'Geometry')
    for k, v in [('Translation', translation), ('Rotation', rotation), ('Scale', scale)]:
        if v is not None:
            value(n, k, v)
    return n


def load_group(path, name):
    if name not in bpy.data.node_groups:
        with bpy.data.libraries.load(str(path), link=False) as (src, dst):
            assert name in src.node_groups, (name, src.node_groups)
            dst.node_groups = [name]
    return bpy.data.node_groups[name]


def component(g, x, y):
    ng = load_group(FILES / 'geometry101/GEOMETRY101-class-ready.blend', '002-point in middle')
    n = native(g, 'GeometryNodeGroup', x, y)
    n.node_tree = ng
    for k, v in [('Width', .28), ('Depth', .28), ('Height', .7)]:
        value(n, k, v)
    return n


def instances(g, points, p_socket, x, y=0, scales=None):
    shape = component(g, x, y-230)
    n = native(g, 'GeometryNodeInstanceOnPoints', x+250, y)
    link(g, points, p_socket, n, 'Points')
    link(g, shape, 'Geometry', n, 'Instance')
    if scales:
        link(g, scales[0], scales[1], n, 'Scale')
    real = native(g, 'GeometryNodeRealizeInstances', x+500, y)
    link(g, n, 'Instances', real, 'Geometry')
    return real


def modifier_value(obj, key, v=None):
    m = next(m for m in obj.modifiers if m.type == 'NODES')
    item = next(s for s in m.node_group.interface.items_tree if s.item_type == 'SOCKET' and s.in_out == 'INPUT' and s.name == key)
    wrap = getattr(m.properties.inputs, item.identifier)
    if v is None:
        q = wrap.value
        return tuple(q) if hasattr(q, '__len__') and not isinstance(q, str) else q
    wrap.value = v
    obj.update_tag()
    bpy.context.view_layer.update()


def begin(lesson):
    global CURRENT
    CURRENT = lesson
    bpy.ops.wm.open_mainfile(filepath=str(TEMPLATE), load_ui=True)
    temporary = bpy.data.scenes.new('Preparing course file')
    if bpy.context.window:
        bpy.context.window.scene = temporary
    for s in list(bpy.data.scenes):
        if s != temporary:
            bpy.data.scenes.remove(s)
    for collection in (bpy.data.objects, bpy.data.node_groups, bpy.data.texts, bpy.data.materials, bpy.data.worlds):
        for item in list(collection):
            collection.remove(item)
    bpy.data.orphans_purge(do_recursive=True)
    bpy.context.preferences.filepaths.save_version = 0


def activate(scene):
    if bpy.context.window:
        bpy.context.window.scene = scene
    active = scene.view_layers[0].objects.active
    for obj in scene.objects:
        obj.select_set(obj == active, view_layer=scene.view_layers[0])
    if active:
        active.hide_set(False, view_layer=scene.view_layers[0])
    bpy.context.view_layer.update()


def mesh_stats(scene, obj=None):
    activate(scene)
    obj = obj or scene.view_layers[0].objects.active
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = ev.to_mesh()
    coords = [obj.matrix_world @ v.co for v in mesh.vertices]
    bm = bmesh.new()
    bm.from_mesh(mesh)
    stats = {'vertices':len(mesh.vertices), 'edges':len(mesh.edges), 'faces':len(mesh.polygons),
             'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),
             'volume':bm.calc_volume(signed=True) if bm.faces else 0.0,
             'bounds':[[min(c[k] for c in coords),max(c[k] for c in coords)] for k in range(3)] if coords else None}
    bm.free()
    ev.to_mesh_clear()
    return stats


def view_setup(scene):
    activate(scene)
    meshes = [o for o in scene.objects if o.type == 'MESH' and not o.hide_get()]
    points = []
    for o in meshes:
        ev = o.evaluated_get(bpy.context.evaluated_depsgraph_get())
        me = ev.to_mesh()
        points.extend(ev.matrix_world @ v.co for v in me.vertices)
        ev.to_mesh_clear()
    center = Vector((0, 0, 0))
    extent = 4.0
    if points:
        lo = Vector([min(p[k] for p in points) for k in range(3)])
        hi = Vector([max(p[k] for p in points) for k in range(3)])
        center, extent = (lo+hi)/2, max((hi-lo).length, 2)
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                sp = area.spaces.active
                sp.shading.type, sp.shading.color_type = 'SOLID', 'OBJECT'
                if scene.get('show_field_material'):
                    sp.shading.type = 'MATERIAL'
                sp.shading.light = 'STUDIO'
                sp.shading.show_cavity = True
                sp.shading.cavity_type = 'BOTH'
                sp.overlay.show_extras = False
                sp.region_3d.view_distance = extent*1.25
                sp.region_3d.view_location = center
                sp.region_3d.view_rotation = Euler((math.radians(65),0,math.radians(30)), 'XYZ').to_quaternion()
                sp.region_3d.view_perspective = 'ORTHO'
                sp.clip_end = 10000
            elif area.type == 'NODE_EDITOR':
                sp = area.spaces.active
                sp.tree_type = 'GeometryNodeTree'
                sp.pin = False
                sp.show_region_ui = False
                sp.show_region_toolbar = False
                try:
                    region = next(r for r in area.regions if r.type=='WINDOW')
                    with bpy.context.temp_override(window=bpy.context.window, area=area, region=region):
                        bpy.ops.node.view_all()
                except (RuntimeError, TypeError, StopIteration):
                    pass
            elif area.type == 'PROPERTIES':
                try:
                    area.spaces.active.context = 'MODIFIER'
                except TypeError:
                    pass
    return center, extent


def fit_teaching_frames(g):
    """Leave a clear gap between header annotations and native nodes."""
    nodes = [n for n in g.nodes if n.type != 'FRAME' and not n.parent]
    if not nodes:
        return
    for f in g.nodes:
        if f.type != 'FRAME' or not f.text or f.shrink:
            continue
        if any(abs(a-b)>.001 for a,b in zip(f.color,(.12,.17,.22))):
            continue
        body = f.text.as_string().rstrip()
        f.height = max(f.height,100+40*len(body.splitlines()))
        f.width = max(f.width,max(map(len,body.splitlines()),default=0)*15)
        f.location.y = max(f.location.y,max(n.location.y for n in nodes)+f.height+80)


def save_lesson(hero=None):
    folder_name, filename, title = CATALOG[CURRENT]
    folder = FILES/folder_name
    folder.mkdir(parents=True, exist_ok=True)
    target = source_path(CURRENT)
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        backup = REFERENCE/'preparation-archive'/CURRENT
        backup.mkdir(parents=True, exist_ok=True)
        i = 1
        while (backup/f'{i:02d}-{filename}').exists():
            i += 1
        shutil.copy2(target, backup/f'{i:02d}-{filename}')
    if 'Preparing course file' in bpy.data.scenes:
        bpy.data.scenes.remove(bpy.data.scenes['Preparing course file'])
    readme = bpy.data.texts.new('START HERE — '+title)
    body = f'{title}\nARC 3133 — Architectural Visualization Methods 1\n\n'
    body += 'Choose scenes in numbered order using the Scene selector.\n'
    body += 'Select the lesson object. Change exposed controls in the GeometryNodes modifier.\n'
    body += 'Home over the node editor fits the graph; Ctrl+Space maximizes an editor.\n'
    body += 'Keep native node names. Explanations are Frames. Save your own working copy.\n\n'
    for name, heading, note in NOTES:
        body += name+'\n'+heading+'\n'+note+'\n\n'
    readme.write(body)
    readme.use_fake_user = True
    report = {'lesson':CURRENT, 'file':str(target), 'blender':bpy.app.version_string, 'scenes':{}}
    for s in SCENES:
        st = mesh_stats(s)
        assert st['vertices'] > 0 and st['faces'] > 0, (s.name, st)
        report['scenes'][s.name] = st
    for g in bpy.data.node_groups:
        if g.bl_idname == 'GeometryNodeTree':
            fit_teaching_frames(g)
            for n in g.nodes:
                assert n.type == 'FRAME' or n.label == '', (g.name,n.name,n.label)
    if hero is not None:
        scene = SCENES[hero]
        center, extent = view_setup(scene)
        cam_data = bpy.data.cameras.new('Preview camera')
        cam = bpy.data.objects.new('Preview camera', cam_data)
        scene.collection.objects.link(cam)
        cam_data.type = 'ORTHO'
        cam_data.ortho_scale = extent*1.05
        cam.location = center + Vector((1,-1.7,1.2)).normalized()*extent*2
        cam.rotation_euler = (center-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.camera = cam
        scene.render.filepath = str(folder/'preview.png')
        bpy.ops.render.render(write_still=True)
        cam.hide_set(True)
    activate(SCENES[0])
    view_setup(SCENES[0])
    bpy.ops.wm.save_as_mainfile(filepath=str(target))
    imports=[n for ng in bpy.data.node_groups if ng.bl_idname=='GeometryNodeTree' for n in ng.nodes if n.bl_idname=='GeometryNodeImportPLY']
    if imports:
        for n in imports:
            source=Path(bpy.path.abspath(sock(n,'Path').default_value))
            assert source.is_file()
            value(n,'Path','//'+source.name)
        bpy.ops.wm.save_as_mainfile(filepath=str(target))
        assert mesh_stats(SCENES[0])['vertices']>0
    report['complete'] = True
    (REFERENCE/(CURRENT+'-verification.json')).write_text(json.dumps(report,indent=2)+'\n', encoding='utf-8')
    md = f'# {title}\n\n'
    if CURRENT in SPLIT_SESSIONS:
        md += 'Each teaching session has its own Blender file:\n\n'
        for fname,scenes in SPLIT_SESSIONS[CURRENT]:
            md += f'- [{fname}]({fname}) — '+', '.join(n[5:] for n in scenes)+'.\n'
        md += '\n'
    else:
        md += f'Open [{filename}]({filename}) in Blender 5.2.1 LTS or a compatible newer version.\n\n'
    md += 'Use the Scene selector in numbered order. Select the lesson object to see its Geometry Nodes. Change the exposed parameters in the modifier; press Home over the node editor to fit the graph.\n\n'
    md += '| Scene | Exercise |\n|---|---|\n'
    for name, heading, note in NOTES:
        safe_heading = heading.replace('|', r'\|')
        md += f'| {name} | {safe_heading} |\n'
    md += '\nNative node names are retained. Short explanations and things to try are in Frames. Save your own working copy.\n\n'
    if imports:
        md += '**Keep `teaching-courtyard.ply` beside this Blender file.** The Import PLY node uses a relative path. This is a synthetic teaching dataset, not a surveyed site. [Dataset and provenance](teaching-courtyard.json).\n\n'
    if CURRENT == 'fabrication':
        md += '[Fabrication notes and dimensions](FABRICATION-NOTES.md) · [Small print STL](small-print-mm.stl) · [Fit coupon STL](fit-coupon-mm.stl) · [Modular parts STL](modular-parts-mm.stl) · [Section parts and spacers SVG](section-parts-and-spacers-mm.svg). These are default-parameter snapshots in millimeters. Regenerate after edits and test fit on the actual material and machine.\n\n'
    md += '[Course file index](../README.md) · [Current syllabus](../../../syllabus/ARC3133_Syllabus_Fall2026_STUDENT.md)\n'
    (folder/'README.md').write_text(md,encoding='utf-8')
    print('ARC3133_COMPLETE '+json.dumps(report), flush=True)


def build_intro():
    s,o,g = lesson_scene('01 - Start','A NODE GRAPH MAKES GEOMETRY',
        'Cube creates geometry. The wire carries it to Group Output.\nChange Size on Cube: one input changes the result.\nA parameter is an input we can change. The empty host mesh is not the result.')
    c=cube(g,0,0,(1.2,.8,1.8))
    output(g,c,'Mesh',x=350)
    for number,name,socket,typ,default,note in [
        (2,'Translation','Translation','NodeSocketVector',(2,0,0), 'Translation is a displacement vector: X, Y, Z.\nTry X = 0, 1, 2. The shape stays the same; its position changes.\nChange Translation in the modifier. The object origin stays at zero.'),
        (3,'Rotation','Rotation','NodeSocketRotation',(0,0,math.radians(35)), 'Rotation changes orientation around the object-space origin.\nTry Z = 0, 45, 90 degrees. The block has different side lengths.\nThe modifier shows angles in degrees; the graph keeps the relationship.'),
        (4,'Scale','Scale','NodeSocketVector',(1.6,1,.6), 'Scale multiplies size along X, Y and Z.\n1 keeps the size, 2 doubles it, 0.5 halves it.\nTry changing only Z. Avoid zero scale in a solid Boolean.')]:
        s,o,g=lesson_scene(f'{number:02d} - {name}',name.upper(),note)
        interface(g,socket,typ,default,description=note.split('\n')[0])
        gi=native(g,'NodeGroupInput',-280,0)
        c=cube(g,0,0,(1.2,.8,1.8))
        t=transform(g,c,x=280)
        link(g,gi,socket,t,socket)
        output(g,t,x=600)
    s,o,g=lesson_scene('05 - Order','ORDER CHANGES THE RESULT',
        'Blue: move, then rotate. Orange: rotate, then move.\nBoth start with the same block and use the same values.\nSelect either object in the viewport or Outliner to read its four-node graph.')
    c=cube(g,0,0,(.8,.5,1.3))
    t=transform(g,c,x=250,translation=(3,0,0))
    r=transform(g,t,'Geometry',x=500,rotation=(0,0,math.pi/3))
    output(g,r,x=780)
    o.name='Move then rotate'
    gb=group('05 - Rotate then move')
    frame(gb,'ROTATE, THEN MOVE','Rotate around the origin first. Then move along X.\nCompare its position with the blue block.',width=1150)
    c=cube(gb,0,0,(.8,.5,1.3))
    r=transform(gb,c,x=250,rotation=(0,0,math.pi/3))
    t=transform(gb,r,'Geometry',x=500,translation=(3,0,0))
    output(gb,t,x=780)
    object_for(s,gb,'Rotate then move',1)
    s.view_layers[0].objects.active=o
    for i,operation,heading,note in [
        (6,'UNION','UNION | A OR B','Keep all the volume occupied by either solid.\nBoth branches feed the multi-input Mesh 2 socket in Union mode.\nThe next two scenes use the same cube and cylinder.'),
        (7,'DIFFERENCE','DIFFERENCE | A MINUS B','Mesh 1 is the block. Mesh 2 is the cutter.\nOnly the block outside the cylinder remains.\nMove the cutter with Cylinder Position and predict the opening.'),
        (8,'INTERSECT','INTERSECTION | A AND B','Keep only the shared volume.\nBoth solids feed the multi-input Mesh 2 socket in Intersect mode.\nTry moving the cylinder away: no overlap means no result.')]:
        s,o,g=lesson_scene(f'{i:02d} - {operation.title()}',heading,note,1400)
        interface(g,'Block Size','NodeSocketVector',(2.5,2,1.6),.1,5)
        interface(g,'Cylinder Radius','NodeSocketFloat',.75,.1,2)
        interface(g,'Cylinder Depth','NodeSocketFloat',2.6,.1,5)
        interface(g,'Cylinder Position','NodeSocketVector',(.8,0,0),-5,5)
        gi=native(g,'NodeGroupInput',-300,0)
        a=cube(g,0,100)
        b=cylinder(g,0,-200)
        link(g,gi,'Block Size',a,'Size')
        link(g,gi,'Cylinder Radius',b,'Radius')
        link(g,gi,'Cylinder Depth',b,'Depth')
        t=transform(g,b,x=280,y=-160)
        link(g,gi,'Cylinder Position',t,'Translation')
        boolean=native(g,'GeometryNodeMeshBoolean',580,60,200)
        boolean.operation, boolean.solver=operation,'EXACT'
        link(g,a,'Mesh',boolean,'Mesh 1' if operation=='DIFFERENCE' else 'Mesh 2')
        link(g,t,'Geometry',boolean,'Mesh 2')
        output(g,boolean,'Mesh',x=880,y=60)
    s,o,g=lesson_scene('09 - Massing exercise','ONE PARAMETRIC MASSING STUDY',
        'Make a block, transform a second cube, subtract it.\nChange one control at a time. Save three variations and diagram the steps.\nNEXT CLASS: replace the cutter with your pyramid built from points and faces.',1500)
    for name,typ,default in [('Block Size','NodeSocketVector',(3,1.1,2.4)),('Opening Scale','NodeSocketVector',(1.2,1.8,1.8)),('Opening Rotation','NodeSocketRotation',(0,.18,0)),('Opening Position','NodeSocketVector',(.2,0,-.5))]:
        interface(g,name,typ,default)
    gi=native(g,'NodeGroupInput',-300,0)
    a=cube(g,0,100)
    b=cube(g,0,-200)
    link(g,gi,'Block Size',a,'Size')
    t=transform(g,b,x=280,y=-200)
    for src,dst in [('Opening Scale','Scale'),('Opening Rotation','Rotation'),('Opening Position','Translation')]:
        link(g,gi,src,t,dst)
    bo=native(g,'GeometryNodeMeshBoolean',600,40,200)
    bo.operation,bo.solver='DIFFERENCE','EXACT'
    link(g,a,'Mesh',bo,'Mesh 1')
    link(g,t,'Geometry',bo,'Mesh 2')
    output(g,bo,'Mesh',x=920,y=40)
    # Analytic transform checks and Boolean set identities catch incorrect wiring.
    stats=[mesh_stats(scene) for scene in SCENES]
    assert abs(stats[1]['bounds'][0][0]-1.4)<1e-5, stats[1]
    assert abs(stats[3]['volume']-stats[0]['volume']*1.6*.6)<1e-5
    a_vol=2.5*2*1.6
    b_vol=48*.5*.75**2*math.sin(2*math.pi/48)*2.6
    union,diff,inter=[stats[k]['volume'] for k in (5,6,7)]
    assert abs(union+inter-a_vol-b_vol)<1e-4, (union,inter,a_vol,b_vol)
    assert abs(diff+inter-a_vol)<1e-4
    assert all(st['nonmanifold_edges']==0 and st['volume']>0 for st in stats)
    modifier_value(o,'Opening Position',(.45,0,-.35))
    changed=mesh_stats(s)
    assert changed['nonmanifold_edges']==0 and abs(changed['volume']-stats[-1]['volume'])>1e-3
    modifier_value(o,'Opening Position',(.2,0,-.5))
    save_lesson(hero=8)


def repeat_pair(g, x1, y1, x2, y2):
    end=native(g,'GeometryNodeRepeatOutput',x2,y2,180)
    start=native(g,'GeometryNodeRepeatInput',x1,y1,180)
    start.pair_with_output(end)
    return start,end


def linear_positions(g, gi):
    ri,ro=repeat_pair(g,0,100,1020,100)
    link(g,gi,'Count',ri,'Iterations')
    multiply=math_node(g,'MULTIPLY',240,0)
    link(g,ri,'Iteration',multiply,0)
    link(g,gi,'Spacing',multiply,1)
    xyz=native(g,'ShaderNodeCombineXYZ',440,0)
    link(g,multiply,0,xyz,'X')
    p=native(g,'GeometryNodePoints',650,0)
    value(p,'Count',1)
    value(p,'Radius',.05)
    link(g,xyz,'Vector',p,'Position')
    join=native(g,'GeometryNodeJoinGeometry',850,0)
    link(g,ri,'Geometry',join,'Geometry')
    link(g,p,'Points',join,'Geometry')
    link(g,join,'Geometry',ro,'Geometry')
    return ro


def nested_grid(hexagonal=False):
    name='Hexagonal Grid' if hexagonal else 'Nested Grid'
    g=group(name)
    for k in ('Rows','Columns'):
        interface(g,k,'NodeSocketInt',5,1,20)
    interface(g,'Spacing','NodeSocketFloat',.8,.3,2)
    gi=native(g,'NodeGroupInput',-550,200)
    outer,end=repeat_pair(g,-300,200,1780,200)
    inner,inner_end=repeat_pair(g,-60,0,1340,0)
    link(g,gi,'Rows',outer,'Iterations')
    link(g,gi,'Columns',inner,'Iterations')
    x=math_node(g,'MULTIPLY',200,-20)
    y=math_node(g,'MULTIPLY',200,-210)
    link(g,inner,'Iteration',x,0)
    link(g,outer,'Iteration',y,0)
    link(g,gi,'Spacing',x,1)
    link(g,gi,'Spacing',y,1)
    x_src,y_src=x,y
    if hexagonal:
        parity=math_node(g,'MODULO',180,-420,b=2)
        link(g,outer,'Iteration',parity,0)
        half=math_node(g,'MULTIPLY',390,-430,b=.5)
        link(g,gi,'Spacing',half,0)
        shift=math_node(g,'MULTIPLY',580,-430)
        link(g,parity,0,shift,0)
        link(g,half,0,shift,1)
        x_src=math_node(g,'ADD',760,-20)
        link(g,x,0,x_src,0)
        link(g,shift,0,x_src,1)
        y_src=math_node(g,'MULTIPLY',760,-210,b=math.sqrt(3)/2)
        link(g,y,0,y_src,0)
    xyz=native(g,'ShaderNodeCombineXYZ',960,-60)
    link(g,x_src,0,xyz,'X')
    link(g,y_src,0,xyz,'Y')
    p=native(g,'GeometryNodePoints',1140,-190)
    value(p,'Count',1)
    link(g,xyz,'Vector',p,'Position')
    join=native(g,'GeometryNodeJoinGeometry',1140,40)
    link(g,inner,'Geometry',join,'Geometry')
    link(g,p,'Points',join,'Geometry')
    link(g,join,'Geometry',inner_end,'Geometry')
    rows=native(g,'GeometryNodeJoinGeometry',1550,80)
    link(g,outer,'Geometry',rows,'Geometry')
    link(g,inner_end,'Geometry',rows,'Geometry')
    link(g,rows,'Geometry',end,'Geometry')
    output(g,end,x=2020,y=200)
    frame(g,name.upper(),'Outer loop: one row at a time. Inner loop: every column in that row.\nJoin Geometry carries the points into the next iteration. Total = Rows x Columns.\n'+('Odd rows move half a spacing; row distance = spacing x sqrt(3)/2.' if hexagonal else 'X = column x spacing. Y = row x spacing.'),x=-550,y=630,width=2750,height=170)
    return g


def grid_node(g,x=0,y=0,count=11,size=8):
    n=native(g,'GeometryNodeMeshGrid',x,y)
    value(n,'Size X',size)
    value(n,'Size Y',size)
    value(n,'Vertices X',count)
    value(n,'Vertices Y',count)
    return n


def compare(g,op,x,y,a=None,b=None):
    n=native(g,'FunctionNodeCompare',x,y,160)
    n.data_type='INT'
    n.operation=op
    if a is not None:value(n,'A',a)
    if b is not None:value(n,'B',b)
    return n


def build_arrays():
    s,o,g=lesson_scene('01 - Linear loop','COUNT, INDEX, REPEAT',
        'A list has an order. Iteration starts at 0 and increases by 1.\nEach pass adds one point at X = iteration x spacing.\nInstance on Points reuses the pyramid; Realize Instances makes mesh copies.',2200)
    interface(g,'Count','NodeSocketInt',8,1,30)
    interface(g,'Spacing','NodeSocketFloat',.8,.3,2)
    gi=native(g,'NodeGroupInput',-300,0)
    positions=linear_positions(g,gi)
    real=instances(g,positions,'Geometry',1240)
    output(g,real,x=1960)
    for number,hexagonal in [(2,False),(3,True)]:
        ng=nested_grid(hexagonal)
        name='Hexagonal array' if hexagonal else 'Nested grid'
        s,o,g=lesson_scene(f'{number:02d} - {name}',name.upper(),
            'Rows x Columns gives the number of points. Change either count.\nSelect the '+ng.name+' group and press Tab to see both Repeat Zones.\n'+('Compare odd and even rows: the offset creates a hexagonal arrangement.' if hexagonal else 'The inner loop makes a row; the outer loop collects the rows.'),1500)
        for key in ('Rows','Columns'):
            interface(g,key,'NodeSocketInt',5,1,20)
        interface(g,'Spacing','NodeSocketFloat',.8,.3,2)
        gi=native(g,'NodeGroupInput',-300,0)
        n=native(g,'GeometryNodeGroup',0,0)
        n.node_tree=ng
        for key in ('Rows','Columns','Spacing'):link(g,gi,key,n,key)
        real=instances(g,n,'Geometry',270)
        output(g,real,x=1040)
    s,o,g=lesson_scene('04 - Radial array','REPEAT AROUND A CIRCLE',
        'Angle step = 2 pi / Count. Angle = iteration x angle step.\nX = radius x cos(angle). Y = radius x sin(angle).\nChange Count and Radius independently; the same pyramid is reused.',2550)
    interface(g,'Count','NodeSocketInt',16,3,48)
    interface(g,'Radius','NodeSocketFloat',3,1,8)
    gi=native(g,'NodeGroupInput',-300,0)
    ri,ro=repeat_pair(g,0,100,1530,100)
    link(g,gi,'Count',ri,'Iterations')
    step=math_node(g,'DIVIDE',220,0,a=2*math.pi)
    link(g,gi,'Count',step,1)
    angle=math_node(g,'MULTIPLY',420,0)
    link(g,ri,'Iteration',angle,0)
    link(g,step,0,angle,1)
    co=math_node(g,'COSINE',620,50)
    si=math_node(g,'SINE',620,-130)
    for n in (co,si):link(g,angle,0,n,0)
    cx=math_node(g,'MULTIPLY',810,50)
    sy=math_node(g,'MULTIPLY',810,-130)
    link(g,co,0,cx,0);link(g,si,0,sy,0)
    for n in (cx,sy):link(g,gi,'Radius',n,1)
    xyz=native(g,'ShaderNodeCombineXYZ',1000,0)
    link(g,cx,0,xyz,'X');link(g,sy,0,xyz,'Y')
    p=native(g,'GeometryNodePoints',1180,-100)
    value(p,'Count',1);link(g,xyz,'Vector',p,'Position')
    join=native(g,'GeometryNodeJoinGeometry',1320,80)
    link(g,ri,'Geometry',join,'Geometry');link(g,p,'Points',join,'Geometry')
    link(g,join,'Geometry',ro,'Geometry')
    real=instances(g,ro,'Geometry',1750)
    output(g,real,x=2480)
    s,o,g=lesson_scene('05 - If and range','IF THE INDEX IS IN THIS RANGE, MOVE IT',
        'Compare tests Index >= Start and Index < End. Boolean Math combines both tests.\nSwitch chooses the height: True moves up; False keeps zero.\nGrid is the compact point arrangement; inspect Index on its point domain.',2400)
    interface(g,'Start','NodeSocketInt',22,0,120)
    interface(g,'End','NodeSocketInt',66,1,121)
    interface(g,'Height','NodeSocketFloat',1.5,-2,3)
    gi=native(g,'NodeGroupInput',-300,-150)
    grid=grid_node(g,0,180)
    index=native(g,'GeometryNodeInputIndex',0,-160)
    a=compare(g,'GREATER_EQUAL',230,-110)
    b=compare(g,'LESS_THAN',230,-330)
    link(g,index,'Index',a,'A');link(g,index,'Index',b,'A')
    link(g,gi,'Start',a,'B');link(g,gi,'End',b,'B')
    both=native(g,'FunctionNodeBooleanMath',450,-130)
    both.operation='AND'
    link(g,a,'Result',both,0);link(g,b,'Result',both,1)
    switch=native(g,'GeometryNodeSwitch',660,-100)
    switch.input_type='FLOAT'
    link(g,both,0,switch,'Switch');link(g,gi,'Height',switch,'True')
    xyz=native(g,'ShaderNodeCombineXYZ',870,-100)
    link(g,switch,'Output',xyz,'Z')
    setpos=native(g,'GeometryNodeSetPosition',1100,100)
    link(g,grid,'Mesh',setpos,'Geometry');link(g,xyz,'Vector',setpos,'Offset')
    real=instances(g,setpos,'Geometry',1360)
    output(g,real,x=2080)
    s,o,g=lesson_scene('06 - Sine curve','A FUNCTION CONTROLS THE CURVE',
        'Z = Amplitude x sin(X x Frequency + Phase). Change one parameter at a time.\nFrequency is radians per model unit; Phase is an angle.\nMesh to Curve uses the ordered line edges. A small circle gives the curve visible thickness.',2100)
    interface(g,'Count','NodeSocketInt',80,4,200)
    interface(g,'Amplitude','NodeSocketFloat',1,.05,3)
    interface(g,'Frequency','NodeSocketFloat',1.6,.1,5)
    interface(g,'Phase','NodeSocketFloat',0,-math.pi*2,math.pi*2)
    gi=native(g,'NodeGroupInput',-300,-100)
    line=native(g,'GeometryNodeMeshLine',0,180)
    value(line,'Offset',(.1,0,0));link(g,gi,'Count',line,'Count')
    pos=native(g,'GeometryNodeInputPosition',0,-160)
    separate=native(g,'ShaderNodeSeparateXYZ',220,-160)
    link(g,pos,'Position',separate,'Vector')
    freq=math_node(g,'MULTIPLY',420,-140)
    link(g,separate,'X',freq,0);link(g,gi,'Frequency',freq,1)
    phase=math_node(g,'ADD',620,-140)
    link(g,freq,0,phase,0);link(g,gi,'Phase',phase,1)
    sine=math_node(g,'SINE',820,-140)
    link(g,phase,0,sine,0)
    amplitude=math_node(g,'MULTIPLY',1020,-140)
    link(g,sine,0,amplitude,0);link(g,gi,'Amplitude',amplitude,1)
    xyz=native(g,'ShaderNodeCombineXYZ',1220,-140)
    link(g,amplitude,0,xyz,'Z')
    setpos=native(g,'GeometryNodeSetPosition',1440,120)
    link(g,line,'Mesh',setpos,'Geometry');link(g,xyz,'Vector',setpos,'Offset')
    curve=native(g,'GeometryNodeMeshToCurve',1690,120)
    link(g,setpos,'Geometry',curve,'Mesh')
    circle=native(g,'GeometryNodeCurvePrimitiveCircle',1690,-140)
    value(circle,'Radius',.035);value(circle,'Resolution',8)
    tube=native(g,'GeometryNodeCurveToMesh',1950,120)
    value(tube,'Fill Caps',True)
    link(g,curve,'Curve',tube,'Curve');link(g,circle,'Curve',tube,'Profile Curve')
    output(g,tube,'Mesh',x=2200,y=120)
    expected=[8*5,25*5,25*5,16*5,121*5]
    for scene,count in zip(SCENES,expected):
        st=mesh_stats(scene)
        assert st['vertices']==count,(scene.name,st,count)
    activate(SCENES[0]);a=SCENES[0].view_layers[0].objects.active
    modifier_value(a,'Count',3)
    assert mesh_stats(SCENES[0])['vertices']==15
    modifier_value(a,'Count',8)
    activate(SCENES[1]);a=SCENES[1].view_layers[0].objects.active
    modifier_value(a,'Rows',3);modifier_value(a,'Columns',4)
    assert mesh_stats(SCENES[1])['vertices']==60
    modifier_value(a,'Rows',5);modifier_value(a,'Columns',5)
    save_lesson(hero=4)


def target_object(scene, kind):
    if kind=='curve':
        data=bpy.data.curves.new('Attractor curve','CURVE')
        data.dimensions='3D'
        spline=data.splines.new('POLY')
        spline.points.add(32)
        for i,p in enumerate(spline.points):
            x=-4+i*.25
            p.co=(x,1.4*math.sin(x*.8),0,1)
        ob=bpy.data.objects.new('Attractor curve - edit or move me',data)
    else:
        data=bpy.data.meshes.new('Attractor positions')
        if kind=='single':
            bm=bmesh.new();bmesh.ops.create_uvsphere(bm,u_segments=16,v_segments=8,radius=.15)
            bm.to_mesh(data);bm.free()
        else:
            data.from_pydata([(-2,-1,0),(2,1,0),(-.5,3,0)],[],[])
        ob=bpy.data.objects.new('Attractor - move me' if kind=='single' else 'Attractors - edit the three vertices',data)
        if kind=='single':ob.location=(1,1,.05)
    scene.collection.objects.link(ob)
    ob.color=PALETTE[1]
    ob.show_in_front=True
    if kind=='multiple':
        g=group('Display the attractor points')
        g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry')
        gi=native(g,'NodeGroupInput',0,0)
        pts=native(g,'GeometryNodeMeshToPoints',240,0)
        pts.mode='VERTICES';value(pts,'Radius',.16)
        link(g,gi,'Geometry',pts,'Mesh');output(g,pts,'Points',x=480)
        m=ob.modifiers.new('GeometryNodes','NODES');m.node_group=g
    return ob


def distance_field(g, gi, kind, x=0,y=-250):
    info=native(g,'GeometryNodeObjectInfo',x,y)
    info.transform_space='RELATIVE'
    link(g,gi,'Attractor',info,'Object')
    if kind=='single':
        position=native(g,'GeometryNodeInputPosition',x,y-280)
        distance=native(g,'ShaderNodeVectorMath',x+260,y)
        distance.operation='DISTANCE'
        link(g,position,'Position',distance,0)
        link(g,info,'Location',distance,1)
        return distance,'Value'
    prox=native(g,'GeometryNodeProximity',x+500,y)
    prox.target_element='EDGES' if kind=='curve' else 'POINTS'
    if kind=='curve':
        wire=native(g,'GeometryNodeCurveToMesh',x+250,y)
        link(g,info,'Geometry',wire,'Curve')
        link(g,wire,'Mesh',prox,'Geometry')
    else:
        link(g,info,'Geometry',prox,'Geometry')
    return prox,'Distance'


def remap(g,gi,distance,ds,x,y,near='Near Scale',far='Far Scale'):
    n=native(g,'ShaderNodeMapRange',x,y,190)
    n.clamp=True
    link(g,distance,ds,n,'Value')
    value(n,'From Min',0)
    link(g,gi,'Distance Limit',n,'From Max')
    if near:link(g,gi,near,n,'To Min')
    else:value(n,'To Min',1)
    if far:link(g,gi,far,n,'To Max')
    else:value(n,'To Max',0)
    return n


def attribute_material(name, attribute):
    mat=bpy.data.materials.new(name)
    mat.use_nodes=True
    mat.node_tree.nodes.clear()
    a=native(mat.node_tree,'ShaderNodeAttribute',0,0)
    a.attribute_name=attribute
    emission=native(mat.node_tree,'ShaderNodeEmission',250,0)
    link(mat.node_tree,a,'Fac',emission,'Color')
    out=native(mat.node_tree,'ShaderNodeOutputMaterial',500,0)
    link(mat.node_tree,emission,'Emission',out,'Surface')
    return mat


def build_attractors():
    for i,kind in [(1,'single'),(2,'single'),(3,'multiple'),(4,'curve')]:
        field_view=i==1
        title='Read the field' if field_view else {'single':'One point','multiple':'Multiple points','curve':'Curve attractor'}[kind]
        note=('White is near; black is far. Read the measured field before changing geometry.\n' if field_view else 'Distance drives Z scale. Near and far values are explicit.\n')
        note+=('Move the orange point, then select the lesson surface again.' if kind=='single' else 'Edit the three source vertices; the nearest point wins.' if kind=='multiple' else 'Move or edit the source curve; distance is measured to its nearest edge.')
        note+='\nTRY: change Distance Limit and predict the affected area.'
        s,o,g=lesson_scene(f'{i:02d} - {title}',title.upper(),note,2300)
        target=target_object(s,kind)
        interface(g,'Attractor','NodeSocketObject',target)
        interface(g,'Distance Limit','NodeSocketFloat',4,.1,12)
        if not field_view:
            interface(g,'Near Scale','NodeSocketFloat',3,.1,5)
            interface(g,'Far Scale','NodeSocketFloat',.3,.1,5)
        gi=native(g,'NodeGroupInput',-300,-80)
        grid=grid_node(g,0,220,count=41 if field_view else 17,size=8)
        distance,ds=distance_field(g,gi,kind)
        mapping=remap(g,gi,distance,ds,780,-150,None if field_view else 'Near Scale',None if field_view else 'Far Scale')
        if field_view:
            store=native(g,'GeometryNodeStoreNamedAttribute',1050,160)
            store.data_type='FLOAT';store.domain='POINT'
            value(store,'Name','influence')
            link(g,grid,'Mesh',store,'Geometry');link(g,mapping,'Result',store,'Value')
            mat=attribute_material('Distance field - grayscale','influence')
            sm=native(g,'GeometryNodeSetMaterial',1310,160)
            value(sm,'Material',mat);link(g,store,'Geometry',sm,'Geometry')
            output(g,sm,x=1570,y=160)
            s.render.engine='CYCLES';s.cycles.samples=16
            s['show_field_material']=True
        else:
            xyz=native(g,'ShaderNodeCombineXYZ',1040,-100)
            value(xyz,'X',1);value(xyz,'Y',1)
            link(g,mapping,'Result',xyz,'Z')
            real=instances(g,grid,'Mesh',1300,100,(xyz,'Vector'))
            output(g,real,x=2040,y=100)
        s.view_layers[0].objects.active=o
    for scene in SCENES[1:]:
        st=mesh_stats(scene)
        assert st['vertices']==17*17*5,(scene.name,st)
        assert st['bounds'][2][1]>.7,(scene.name,st)
    s=SCENES[1];o=s.view_layers[0].objects.active;activate(s)
    target=modifier_value(o,'Attractor')
    before=mesh_stats(s)['volume']
    target.location.x=12;target.update_tag()
    after=mesh_stats(s)['volume']
    assert after<before*.5,(before,after)
    target.location.x=1;target.update_tag()
    save_lesson(hero=3)


def tube_mesh(g, geometry, socket, x, y, radius=.045, gi=None, radius_name='Strut Radius'):
    curve=native(g,'GeometryNodeMeshToCurve',x,y)
    link(g,geometry,socket,curve,'Mesh')
    circle=native(g,'GeometryNodeCurvePrimitiveCircle',x,y-240)
    value(circle,'Resolution',8);value(circle,'Radius',radius)
    if gi:link(g,gi,radius_name,circle,'Radius')
    tube=native(g,'GeometryNodeCurveToMesh',x+250,y)
    value(tube,'Fill Caps',True)
    link(g,curve,'Curve',tube,'Curve');link(g,circle,'Curve',tube,'Profile Curve')
    return tube


def build_tessellation():
    s,o,g=lesson_scene('01 - Tessellation','A CELL COVERS A SURFACE',
        'Repeated square cells meet edge to edge when Fill = 1.\nReduce Fill to introduce panel gaps; then it is no longer complete coverage.\nChange Count, Cell Size and Thickness. Start with a small system.',1700)
    interface(g,'Count','NodeSocketInt',6,2,12)
    interface(g,'Cell Size','NodeSocketFloat',.8,.3,2)
    interface(g,'Fill','NodeSocketFloat',1,.5,1)
    interface(g,'Thickness','NodeSocketFloat',.12,.03,.5)
    gi=native(g,'NodeGroupInput',-300,0)
    count=math_node(g,'SUBTRACT',0,100,b=1);link(g,gi,'Count',count,0)
    extent=math_node(g,'MULTIPLY',220,100)
    link(g,count,0,extent,0);link(g,gi,'Cell Size',extent,1)
    grid=grid_node(g,450,120,count=6,size=4)
    for k in ('Vertices X','Vertices Y'):link(g,gi,'Count',grid,k)
    for k in ('Size X','Size Y'):link(g,extent,0,grid,k)
    width=math_node(g,'MULTIPLY',0,-200)
    link(g,gi,'Cell Size',width,0);link(g,gi,'Fill',width,1)
    xyz=native(g,'ShaderNodeCombineXYZ',230,-200)
    for k in ('X','Y'):link(g,width,0,xyz,k)
    link(g,gi,'Thickness',xyz,'Z')
    cell=cube(g,450,-200);link(g,xyz,'Vector',cell,'Size')
    inst=native(g,'GeometryNodeInstanceOnPoints',720,100)
    link(g,grid,'Mesh',inst,'Points');link(g,cell,'Mesh',inst,'Instance')
    real=native(g,'GeometryNodeRealizeInstances',960,100)
    link(g,inst,'Instances',real,'Geometry');output(g,real,x=1200,y=100)
    for i,vary in [(2,False),(3,True)]:
        name='Lattice' if not vary else 'Attractor lattice'
        s,o,g=lesson_scene(f'{i:02d} - {name}',name.upper(),
            'Two point grids are connected by vertical members. Edges become struts.\n'+('The upper layer height responds to the external attractor.' if vary else 'Change Layer Height and Strut Radius independently.')+'\nStruts overlap at joints; fuse and test the joints before fabrication.',2550)
        if not vary:interface(g,'Layer Height','NodeSocketFloat',1.4,.3,3)
        interface(g,'Strut Radius','NodeSocketFloat',.045,.025,.12)
        gi=native(g,'NodeGroupInput',-300,0)
        grid=grid_node(g,0,200,count=5,size=4)
        height=None
        if vary:
            target=target_object(s,'single')
            interface(g,'Attractor','NodeSocketObject',target)
            interface(g,'Distance Limit','NodeSocketFloat',4,.5,8)
            interface(g,'Near Scale','NodeSocketFloat',2.4,.3,4)
            interface(g,'Far Scale','NodeSocketFloat',.45,.3,4)
            distance,ds=distance_field(g,gi,'single',0,-200)
            height=remap(g,gi,distance,ds,570,-150)
        xyz=native(g,'ShaderNodeCombineXYZ',840,-50)
        if height:link(g,height,'Result',xyz,'Z')
        else:link(g,gi,'Layer Height',xyz,'Z')
        top=native(g,'GeometryNodeSetPosition',1090,200)
        link(g,grid,'Mesh',top,'Geometry');link(g,xyz,'Vector',top,'Offset')
        line=native(g,'GeometryNodeMeshLine',840,-310)
        value(line,'Count',2);value(line,'Offset',(0,0,1))
        scales=native(g,'ShaderNodeCombineXYZ',1090,-140)
        value(scales,'X',1);value(scales,'Y',1)
        if height:link(g,height,'Result',scales,'Z')
        else:link(g,gi,'Layer Height',scales,'Z')
        inst=native(g,'GeometryNodeInstanceOnPoints',1320,-100)
        link(g,grid,'Mesh',inst,'Points');link(g,line,'Mesh',inst,'Instance')
        link(g,scales,'Vector',inst,'Scale')
        real=native(g,'GeometryNodeRealizeInstances',1560,-100)
        link(g,inst,'Instances',real,'Geometry')
        join=native(g,'GeometryNodeJoinGeometry',1780,200)
        for n,key in [(grid,'Mesh'),(top,'Geometry'),(real,'Geometry')]:link(g,n,key,join,'Geometry')
        merge=native(g,'GeometryNodeMergeByDistance',2010,200)
        value(merge,'Distance',.001);link(g,join,'Geometry',merge,'Geometry')
        tube=tube_mesh(g,merge,'Geometry',2250,200,gi=gi)
        output(g,tube,'Mesh',x=2750,y=200)
        s.view_layers[0].objects.active=o
    assert mesh_stats(SCENES[0])['vertices']==36*8
    flat=mesh_stats(SCENES[1]);varied=mesh_stats(SCENES[2])
    assert varied['bounds'][2][1]>flat['bounds'][2][1]+.4
    save_lesson(hero=2)


def teaching_cloud(folder):
    folder.mkdir(parents=True,exist_ok=True)
    pts=set()
    boxes=[((-2,-.8,0),(1.2,1.6,2.4)),((.5,-1.5,0),(1.8,1.2,1.3)),((-.5,1.1,0),(2.3,.9,1.8))]
    for origin,size in boxes:
        for fixed in range(3):
            other=[k for k in range(3) if k!=fixed]
            for side in (0,1):
                for i in range(11):
                    for j in range(11):
                        p=list(origin);p[fixed]+=side*size[fixed]
                        p[other[0]]+=i/10*size[other[0]]
                        p[other[1]]+=j/10*size[other[1]]
                        pts.add(tuple(round(x,5) for x in p))
    pts=sorted(pts)
    path=folder/'teaching-courtyard.ply'
    text='ply\nformat ascii 1.0\ncomment Synthetic ARC 3133 teaching data; not a survey\nelement vertex '+str(len(pts))+'\nproperty float x\nproperty float y\nproperty float z\nend_header\n'
    text+='\n'.join(' '.join(str(x) for x in p) for p in pts)+'\n'
    path.write_text(text,encoding='ascii')
    meta={'name':'Synthetic teaching courtyard','source':'Generated from three sampled box surfaces for ARC 3133. Not measured site data.','license':'CC BY-SA 4.0, matching the course materials','units':'model units; treated as meters for this exercise','origin':[0,0,0],'point_count':len(pts),'edges':0,'faces':0,'decimation':'none; 11 by 11 samples per box face, duplicate coordinates removed','purpose':'Practice import, sample analysis and volume conversion without an external service.'}
    (folder/'teaching-courtyard.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    return path,len(pts)


def imported_points(g,path,x=0,y=100):
    n=native(g,'GeometryNodeImportPLY',x,y,240)
    value(n,'Path',str(path))
    pts=native(g,'GeometryNodeMeshToPoints',x+300,y)
    pts.mode='VERTICES';value(pts,'Radius',.035)
    link(g,n,'Mesh',pts,'Mesh')
    return pts


def point_glyphs(g,src,socket,x,y,gi=None):
    ico=native(g,'GeometryNodeMeshIcoSphere',x,y-200)
    value(ico,'Radius',.025);value(ico,'Subdivisions',1)
    if gi:link(g,gi,'Display Radius',ico,'Radius')
    inst=native(g,'GeometryNodeInstanceOnPoints',x+240,y)
    link(g,src,socket,inst,'Points');link(g,ico,'Mesh',inst,'Instance')
    real=native(g,'GeometryNodeRealizeInstances',x+480,y)
    link(g,inst,'Instances',real,'Geometry')
    return real


def build_clouds():
    folder=FILES/CATALOG['clouds'][0]
    path,count=teaching_cloud(folder)
    s,o,g=lesson_scene('01 - Import points','IMPORT SAMPLES, NOT FACES',
        f'Import PLY reads {count} samples with zero edges and zero faces.\nThe small spheres are display geometry; the final output is a mesh.\nCtrl+Shift+click Mesh to Points to inspect the samples with Viewer.\nIn the Spreadsheet, choose Viewer Node, then Point Cloud / Point.\nSynthetic data, origin (0,0,0), meters, no decimation. Keep the PLY beside this file.',1800)
    interface(g,'Display Radius','NodeSocketFloat',.025,.01,.1)
    gi=native(g,'NodeGroupInput',-300,-150)
    pts=imported_points(g,path)
    glyph=point_glyphs(g,pts,'Points',630,100,gi)
    output(g,glyph,x=1360,y=100)
    s,o,g=lesson_scene('02 - Analyze points','USE AN EXTERNAL CONDITION TO FILTER THE CLOUD',
        'Distance is measured at each imported point, using the same attractor logic as before.\nKeep the points inside Distance Limit; Delete Geometry removes the rest from this branch.\nMove the orange attractor and compare with the unchanged source in Scene 01.',2000)
    target=target_object(s,'single');target.location=(.4,0,1)
    interface(g,'Attractor','NodeSocketObject',target)
    interface(g,'Distance Limit','NodeSocketFloat',2,.2,6)
    interface(g,'Display Radius','NodeSocketFloat',.03,.01,.1)
    gi=native(g,'NodeGroupInput',-300,-150)
    pts=imported_points(g,path,0,170)
    distance,ds=distance_field(g,gi,'single',0,-200)
    outside=math_node(g,'GREATER_THAN',620,-100)
    link(g,distance,ds,outside,0);link(g,gi,'Distance Limit',outside,1)
    delete=native(g,'GeometryNodeDeleteGeometry',850,120)
    delete.domain='POINT'
    link(g,pts,'Points',delete,'Geometry');link(g,outside,0,delete,'Selection')
    glyph=point_glyphs(g,delete,'Geometry',1110,100,gi)
    output(g,glyph,x=1840,y=100)
    s.view_layers[0].objects.active=o
    s,o,g=lesson_scene('03 - Points to volume','SAMPLES BECOME A SAMPLED DENSITY VOLUME',
        'Radius gives each point an area of influence. Voxel Amount controls resolution.\nVolume to Mesh extracts the chosen density threshold so the boundary is visible.\nThis is a reconstruction choice, not recovered survey detail or an exact signed distance field.',1800)
    interface(g,'Influence Radius','NodeSocketFloat',.19,.08,.5)
    interface(g,'Voxel Amount','NodeSocketInt',64,32,128)
    interface(g,'Surface Threshold','NodeSocketFloat',.2,.05,.8)
    gi=native(g,'NodeGroupInput',-300,-150)
    pts=imported_points(g,path)
    volume=native(g,'GeometryNodePointsToVolume',640,100,210)
    link(g,pts,'Points',volume,'Points')
    link(g,gi,'Influence Radius',volume,'Radius');link(g,gi,'Voxel Amount',volume,'Voxel Amount')
    mesh=native(g,'GeometryNodeVolumeToMesh',920,100,210)
    link(g,volume,'Volume',mesh,'Volume');link(g,gi,'Surface Threshold',mesh,'Threshold')
    output(g,mesh,'Mesh',x=1220,y=100)
    original=mesh_stats(SCENES[0]);filtered=mesh_stats(SCENES[1]);converted=mesh_stats(SCENES[2])
    assert original['vertices']==count*12,(count,original)
    assert 0<filtered['vertices']<original['vertices']
    assert converted['volume']>0 and converted['nonmanifold_edges']==0,converted
    before=converted['volume'];modifier_value(o,'Influence Radius',.26)
    assert mesh_stats(s)['volume']>before
    modifier_value(o,'Influence Radius',.19)
    save_lesson(hero=2)


def field_grid(g,gi,field,field_socket,x,y,bounds=1.8):
    topology=native(g,'GeometryNodeCubeGridTopology',x,y-280,200)
    value(topology,'Bounds Min',(-bounds,)*3);value(topology,'Bounds Max',(bounds,)*3)
    for k in ('Resolution X','Resolution Y','Resolution Z'):link(g,gi,'Resolution',topology,k)
    sample=native(g,'GeometryNodeFieldToGrid',x+270,y,210)
    sample.grid_items.new('FLOAT','Value')
    link(g,topology,'Topology',sample,'Topology');link(g,field,field_socket,sample,'Value')
    mesh=native(g,'GeometryNodeGridToMesh',x+550,y,190)
    value(mesh,'Threshold',0)
    link(g,sample,'Value',mesh,'Grid')
    return mesh


def build_volumes():
    s,o,g=lesson_scene('01 - Mesh to SDF','FROM A MESH BOUNDARY TO SIGNED DISTANCE',
        'Mesh to SDF Grid samples distance to the closed cube boundary.\nGrid to Mesh extracts its zero level. Voxel Size sets the sampling scale.\nCompare with density: a density value is not a distance.',1450)
    interface(g,'Size','NodeSocketVector',(2.4,1.8,1.8),.5,3)
    interface(g,'Voxel Size','NodeSocketFloat',.12,.04,.3)
    gi=native(g,'NodeGroupInput',-300,0)
    c=cube(g,0,0);link(g,gi,'Size',c,'Size')
    sdf=native(g,'GeometryNodeMeshToSDFGrid',270,0)
    link(g,c,'Mesh',sdf,'Mesh');link(g,gi,'Voxel Size',sdf,'Voxel Size')
    mesh=native(g,'GeometryNodeGridToMesh',540,0)
    value(mesh,'Threshold',0);link(g,sdf,'SDF Grid',mesh,'Grid')
    output(g,mesh,'Mesh',x=820)
    for i,noise in [(2,False),(4,True)]:
        title='Signed distance' if not noise else 'Noise field'
        s,o,g=lesson_scene(f'{i:02d} - {title}',title.upper(),
            ('Sphere distance = length(Position) - Radius.\nNegative is inside, zero is the surface, positive is outside.\n' if not noise else 'Start with sphere distance; add a centered Noise Texture value.\nThe distorted field defines a surface but is no longer an exact distance.\n')+
            'The topology defines the sampled region. Increase Resolution only after the small test works.',2300)
        interface(g,'Radius','NodeSocketFloat',1.2,.5,1.45)
        interface(g,'Resolution','NodeSocketInt',48,24,80)
        if noise:
            interface(g,'Noise Strength','NodeSocketFloat',.3,0,.6)
            interface(g,'Noise Scale','NodeSocketFloat',2.2,.5,6)
        gi=native(g,'NodeGroupInput',-300,-150)
        pos=native(g,'GeometryNodeInputPosition',0,100)
        length=native(g,'ShaderNodeVectorMath',230,100)
        length.operation='LENGTH';link(g,pos,'Position',length,0)
        distance=math_node(g,'SUBTRACT',460,100)
        link(g,length,'Value',distance,0);link(g,gi,'Radius',distance,1)
        f=distance
        if noise:
            tex=native(g,'ShaderNodeTexNoise',0,-250,200)
            value(tex,'Detail',2)
            link(g,pos,'Position',tex,'Vector');link(g,gi,'Noise Scale',tex,'Scale')
            centered=math_node(g,'SUBTRACT',260,-230,b=.5)
            link(g,tex,'Fac',centered,0)
            strength=math_node(g,'MULTIPLY',470,-230)
            link(g,centered,0,strength,0);link(g,gi,'Noise Strength',strength,1)
            f=math_node(g,'ADD',700,100)
            link(g,distance,0,f,0);link(g,strength,0,f,1)
        mesh=field_grid(g,gi,f,0,980,100)
        output(g,mesh,'Mesh',x=1810,y=100)
    # Place the Boolean scene before the noise study in the saved scene list.
    s,o,g=lesson_scene('03 - SDF Boolean','BOOLEAN OPERATIONS ON DISTANCE GRIDS',
        'Both meshes become signed distance grids at the same voxel size.\nSDF Grid Boolean is set to Difference: block minus sphere.\nCompare Union and Intersect in the same node, then return to Difference.',2100)
    interface(g,'Voxel Size','NodeSocketFloat',.08,.04,.2)
    interface(g,'Cutter Radius','NodeSocketFloat',1.05,.3,1.5)
    interface(g,'Cutter Position','NodeSocketVector',(.8,0,0),-3,3)
    gi=native(g,'NodeGroupInput',-300,-150)
    a=cube(g,0,160,(2.6,1.8,1.8))
    sphere=native(g,'GeometryNodeMeshIcoSphere',0,-130)
    value(sphere,'Subdivisions',3);link(g,gi,'Cutter Radius',sphere,'Radius')
    t=transform(g,sphere,x=250,y=-130)
    link(g,gi,'Cutter Position',t,'Translation')
    sa=native(g,'GeometryNodeMeshToSDFGrid',530,160)
    sb=native(g,'GeometryNodeMeshToSDFGrid',530,-120)
    link(g,a,'Mesh',sa,'Mesh');link(g,t,'Geometry',sb,'Mesh')
    for n in (sa,sb):link(g,gi,'Voxel Size',n,'Voxel Size')
    bo=native(g,'GeometryNodeSDFGridBoolean',810,140)
    bo.operation='DIFFERENCE'
    link(g,sa,'SDF Grid',bo,'Grid 1');link(g,sb,'SDF Grid',bo,'Grid 2')
    mesh=native(g,'GeometryNodeGridToMesh',1070,140)
    value(mesh,'Threshold',0);link(g,bo,'Grid',mesh,'Grid')
    output(g,mesh,'Mesh',x=1330,y=140)
    SCENES.sort(key=lambda s:s.name);NOTES.sort(key=lambda n:n[0])
    for scene in SCENES:
        st=mesh_stats(scene)
        if st['volume']<0:
            graph=scene.view_layers[0].objects.active.modifiers[0].node_group
            out=next(n for n in graph.nodes if n.type=='GROUP_OUTPUT')
            old=out.inputs['Geometry'].links[0]
            source,source_socket=old.from_node,old.from_socket
            graph.links.remove(old)
            flip=native(graph,'GeometryNodeFlipFaces',out.location.x,out.location.y)
            graph.links.new(source_socket,flip.inputs['Mesh'])
            link(graph,flip,'Mesh',out,'Geometry')
            out.location.x+=250
            next(n for n in graph.nodes if n.type=='FRAME').text.write('Flip Faces gives outward normals for the negative-inside field.\n')
    sphere_stats=mesh_stats(SCENES[1])
    assert abs(sphere_stats['volume']-4/3*math.pi*1.2**3)<.12,sphere_stats
    for scene in SCENES:
        st=mesh_stats(scene)
        assert st['nonmanifold_edges']==0 and st['volume']>0,(scene.name,st)
    s=SCENES[3];o=s.view_layers[0].objects.active;activate(s)
    original=mesh_stats(s)['volume']
    modifier_value(o,'Radius',1)
    assert mesh_stats(s)['volume']<original*.8
    modifier_value(o,'Radius',1.2)
    save_lesson(hero=3)


def noise_volume(g,x=0,y=0):
    path=source_path('volumes')
    ng=load_group(path,'04 - Noise field')
    n=native(g,'GeometryNodeGroup',x,y,210);n.node_tree=ng
    value(n,'Resolution',32)
    return n


def contour_group():
    if 'Contour at Height' in bpy.data.node_groups:return bpy.data.node_groups['Contour at Height']
    g=group('Contour at Height')
    interface(g,'Geometry','NodeSocketGeometry')
    interface(g,'Height','NodeSocketFloat',0)
    interface(g,'Cut Extent','NodeSocketFloat',10,1,1000)
    gi=native(g,'NodeGroupInput',-300,0)
    xyz=native(g,'ShaderNodeCombineXYZ',0,-200)
    for k in ('X','Y','Z'):link(g,gi,'Cut Extent',xyz,k)
    c=cube(g,240,-200);link(g,xyz,'Vector',c,'Size')
    half=math_node(g,'MULTIPLY',0,160,b=.5);link(g,gi,'Cut Extent',half,0)
    z=math_node(g,'ADD',230,160)
    link(g,half,0,z,0);link(g,gi,'Height',z,1)
    loc=native(g,'ShaderNodeCombineXYZ',450,160);link(g,z,0,loc,'Z')
    t=transform(g,c,x=700,y=-100);link(g,loc,'Vector',t,'Translation')
    bo=native(g,'GeometryNodeMeshBoolean',950,160)
    bo.operation,bo.solver='DIFFERENCE','EXACT'
    link(g,gi,'Geometry',bo,'Mesh 1');link(g,t,'Geometry',bo,'Mesh 2')
    curve=native(g,'GeometryNodeMeshToCurve',1200,160)
    link(g,bo,'Mesh',curve,'Mesh');link(g,bo,'Intersecting Edges',curve,'Selection')
    output(g,curve,'Curve',x=1470,y=160)
    frame(g,'EXTRACT A TRUE CONTOUR','A large closed cutter removes everything above Height.\nOnly Intersecting Edges become curves: the cut boundary lies in one plane.\nCut Extent must be larger than the source object.',x=-300,y=520,width=1950,height=160)
    return g


def solid_profile_group():
    if 'Profile to Solid' in bpy.data.node_groups:return bpy.data.node_groups['Profile to Solid']
    g=group('Profile to Solid')
    interface(g,'Curve','NodeSocketGeometry')
    interface(g,'Thickness','NodeSocketFloat',.06,.001,10)
    gi=native(g,'NodeGroupInput',-300,0)
    fill=native(g,'GeometryNodeFillCurve',0,100)
    link(g,gi,'Curve',fill,'Curve')
    xyz=native(g,'ShaderNodeCombineXYZ',0,-200)
    link(g,gi,'Thickness',xyz,'Z')
    extrude=native(g,'GeometryNodeExtrudeMesh',260,100)
    extrude.mode='FACES';value(extrude,'Individual',False)
    link(g,fill,'Mesh',extrude,'Mesh');link(g,xyz,'Vector',extrude,'Offset')
    value(extrude,'Offset Scale',1)
    base=native(g,'GeometryNodeFlipFaces',260,-200)
    link(g,fill,'Mesh',base,'Mesh')
    join=native(g,'GeometryNodeJoinGeometry',520,100)
    link(g,extrude,'Mesh',join,'Geometry');link(g,base,'Mesh',join,'Geometry')
    merge=native(g,'GeometryNodeMergeByDistance',760,100)
    value(merge,'Distance',.00001);link(g,join,'Geometry',merge,'Geometry')
    output(g,merge,x=1010,y=100)
    frame(g,'CLOSE THE PHYSICAL PART','The profile must lie on XY before Fill Curve.\nExtrude Mesh removes the back face, so Flip Faces supplies the bottom cap.\nJoin and merge the boundaries to make a closed solid.',x=-300,y=480,width=1500,height=160)
    return g


def contour_instance(g,source,source_socket,height,height_socket,x,y,extent=10):
    n=native(g,'GeometryNodeGroup',x,y,200);n.node_tree=contour_group()
    link(g,source,source_socket,n,'Geometry');link(g,height,height_socket,n,'Height')
    value(n,'Cut Extent',extent)
    return n


def curve_tube(g,src,src_socket,x,y,radius=.012):
    circle=native(g,'GeometryNodeCurvePrimitiveCircle',x,y-210)
    value(circle,'Resolution',8);value(circle,'Radius',radius)
    tube=native(g,'GeometryNodeCurveToMesh',x+250,y)
    value(tube,'Fill Caps',True)
    link(g,src,src_socket,tube,'Curve');link(g,circle,'Curve',tube,'Profile Curve')
    return tube


def section_positions(g,gi,ri,x=250,y=100):
    offset=math_node(g,'MULTIPLY',x,y)
    link(g,ri,'Iteration',offset,0);link(g,gi,'Spacing',offset,1)
    height=math_node(g,'ADD',x+200,y)
    link(g,offset,0,height,0);link(g,gi,'Start Height',height,1)
    return height


def flatten_profile(g,contour,height,x,y):
    negative=math_node(g,'MULTIPLY',x,y-220,b=-1)
    link(g,height,0,negative,0)
    xyz=native(g,'ShaderNodeCombineXYZ',x+190,y-220)
    link(g,negative,0,xyz,'Z')
    flat=transform(g,contour,'Geometry',x=x+420,y=y)
    link(g,xyz,'Vector',flat,'Translation')
    return flat


def layout_vector(g,gi,ri,x,y):
    col=math_node(g,'MODULO',x,y);link(g,ri,'Iteration',col,0);link(g,gi,'Columns',col,1)
    div=math_node(g,'DIVIDE',x,y-220);link(g,ri,'Iteration',div,0);link(g,gi,'Columns',div,1)
    row=math_node(g,'FLOOR',x+190,y-220);link(g,div,0,row,0)
    cx=math_node(g,'MULTIPLY',x+400,y);link(g,col,0,cx,0);link(g,gi,'Pitch',cx,1)
    cy=math_node(g,'MULTIPLY',x+400,y-220);link(g,row,0,cy,0);link(g,gi,'Pitch',cy,1)
    xyz=native(g,'ShaderNodeCombineXYZ',x+600,y);link(g,cx,0,xyz,'X');link(g,cy,0,xyz,'Y')
    return xyz


def build_discretization():
    s,o,g=lesson_scene('01 - One contour','A VOLUME MEETS ONE PLANE',
        'The source is the noise-driven volume from the preceding class.\nHeight chooses the plane. Contour at Height extracts its boundary as a curve.\nTab into the group to see the Boolean and Intersecting Edges selection.',1700)
    interface(g,'Height','NodeSocketFloat',0,-1,1)
    gi=native(g,'NodeGroupInput',-300,0)
    source=noise_volume(g,0,100)
    contour=contour_instance(g,source,'Geometry',gi,'Height',300,100)
    tube=curve_tube(g,contour,'Geometry',570,100)
    output(g,tube,'Mesh',x=1110,y=100)
    for i,solid,layout in [(2,False,False),(3,True,False),(4,True,True)]:
        name='Contour stack' if not solid else 'Section parts' if not layout else 'Laid out parts'
        s,o,g=lesson_scene(f'{i:02d} - {name}',name.upper(),
            'Height = Start Height + iteration x Spacing. Count controls the finite set.\n'+('Contours become closed parts with material thickness.' if solid else 'A small circular profile makes the contour curves visible.')+'\n'+('Modulo and division arrange the parts on a sheet. Check gaps before export.' if layout else 'Compare the discrete result with the continuous source volume.'),3000)
        interface(g,'Count','NodeSocketInt',9,2,12)
        interface(g,'Start Height','NodeSocketFloat',-.88,-1.1,0)
        interface(g,'Spacing','NodeSocketFloat',.22,.08,.3)
        if solid:interface(g,'Thickness','NodeSocketFloat',.06,.01,.15)
        if layout:
            interface(g,'Columns','NodeSocketInt',3,1,6)
            interface(g,'Pitch','NodeSocketFloat',2.8,2.5,4)
        gi=native(g,'NodeGroupInput',-300,0)
        source=noise_volume(g,0,-280)
        ri,ro=repeat_pair(g,0,180,2920,180)
        link(g,gi,'Count',ri,'Iterations')
        height=section_positions(g,gi,ri)
        contour=contour_instance(g,source,'Geometry',height,0,700,100)
        result_node=contour
        if solid:
            flat=flatten_profile(g,contour,height,960,100)
            part=native(g,'GeometryNodeGroup',1640,100);part.node_tree=solid_profile_group()
            link(g,flat,'Geometry',part,'Curve');link(g,gi,'Thickness',part,'Thickness')
            if layout:
                position=layout_vector(g,gi,ri,1700,-250)
            else:
                position=native(g,'ShaderNodeCombineXYZ',1910,-180)
                link(g,height,0,position,'Z')
            result_node=transform(g,part,'Geometry',x=2430,y=100)
            link(g,position,'Vector',result_node,'Translation')
        join=native(g,'GeometryNodeJoinGeometry',2690,180)
        link(g,ri,'Geometry',join,'Geometry');link(g,result_node,'Geometry',join,'Geometry')
        link(g,join,'Geometry',ro,'Geometry')
        if solid:output(g,ro,x=3180,y=180)
        else:
            tube=curve_tube(g,ro,'Geometry',3180,180)
            output(g,tube,'Mesh',x=3710,y=180)
            for node in g.nodes:
                if node.type != 'FRAME' and node.location.x>=2690:
                    node.location.x-=1700
            next(n for n in g.nodes if n.type=='FRAME').width=2490
    for s in SCENES:
        st=mesh_stats(s)
        assert st['vertices']>0 and st['nonmanifold_edges']==0 and st['volume']>0,(s.name,st)
    stack=mesh_stats(SCENES[2]);layout=mesh_stats(SCENES[3])
    assert abs(stack['volume']-layout['volume'])<1e-3,(stack,layout)
    assert abs(layout['bounds'][2][0])<1e-4 and abs(layout['bounds'][2][1]-.06)<1e-4,layout
    save_lesson(hero=2)


def boolean(g,a,ak,cutters,x,y,operation='DIFFERENCE'):
    n=native(g,'GeometryNodeMeshBoolean',x,y,200)
    n.operation,n.solver=operation,'EXACT'
    link(g,a,ak,n,'Mesh 1' if operation=='DIFFERENCE' else 'Mesh 2')
    for b,bk in cutters:link(g,b,bk,n,'Mesh 2')
    return n


def registered_profile_group():
    g=group('Registered Profile to Solid')
    interface(g,'Curve','NodeSocketGeometry')
    interface(g,'Thickness','NodeSocketFloat',3,.5,3)
    interface(g,'Hole Radius','NodeSocketFloat',1.65,1.5,2)
    gi=native(g,'NodeGroupInput',-300,0)
    part=native(g,'GeometryNodeGroup',0,140);part.node_tree=solid_profile_group()
    link(g,gi,'Curve',part,'Curve');link(g,gi,'Thickness',part,'Thickness')
    hole=cylinder(g,0,-140,radius=1.65,depth=12,resolution=32)
    link(g,gi,'Hole Radius',hole,'Radius')
    a=transform(g,hole,x=280,y=-140,translation=(-7,0,0))
    b=transform(g,hole,x=280,y=-500,translation=(7,0,0))
    bo=boolean(g,part,'Geometry',[(a,'Geometry'),(b,'Geometry')],570,140)
    output(g,bo,'Mesh',x=850,y=140)
    frame(g,'TWO HOLES KEEP THE SECTIONS REGISTERED','The two holes share fixed centers at X = -7 and +7 mm.\nHole Radius includes the trial fit allowance. Cut a coupon before production.\nUse matching rods and spacer rings to preserve the section interval.',x=-300,y=530,width=1420,height=160)
    return g


def add_part_index(g,src,key,ri,x,y):
    store=native(g,'GeometryNodeStoreNamedAttribute',x,y)
    store.domain='POINT';store.data_type='INT';value(store,'Name','part_index')
    link(g,src,key,store,'Geometry');link(g,ri,'Iteration',store,'Value')
    return store


def final_sections(layout):
    name='05 - Cutting layout' if layout else '04 - Registered sections'
    s,o,g=lesson_scene(name,'CUTTING LAYOUT' if layout else 'REGISTERED SECTION ASSEMBLY',
        'Coordinates are millimeters. Twelve section parts come from the earlier volume.\nTwo 3 mm rods register the parts. Spacer rings maintain the gaps.\n'+('The 400 x 300 mm SVG is a default-settings snapshot. Verify actual stock and cut a fit test.' if layout else 'Sheet Thickness controls both the part thickness and the spacer thickness.'),4100)
    s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001;s.unit_settings.length_unit='MILLIMETERS'
    interface(g,'Count','NodeSocketInt',12,4,12)
    interface(g,'Sheet Thickness','NodeSocketFloat',3,1,3)
    interface(g,'Hole Radius','NodeSocketFloat',1.65,1.5,2)
    if layout:
        interface(g,'Columns','NodeSocketInt',4,1,4)
        interface(g,'Pitch','NodeSocketFloat',80,75,85)
    gi=native(g,'NodeGroupInput',-300,0)
    src=noise_volume(g,0,-400)
    value(src,'Noise Strength',.12)
    body=transform(g,src,'Geometry',x=270,y=-400,scale=(30,30,30))
    ri,ro=repeat_pair(g,0,180,3490,180)
    link(g,gi,'Count',ri,'Iterations')
    # Symmetric section heights. The interval is two sheet thicknesses.
    interval=math_node(g,'MULTIPLY',220,-130,b=2)
    link(g,gi,'Sheet Thickness',interval,0)
    last=math_node(g,'SUBTRACT',220,130,b=1);link(g,gi,'Count',last,0)
    half=math_node(g,'MULTIPLY',410,130,b=-.5);link(g,last,0,half,0)
    centered=math_node(g,'ADD',600,130);link(g,ri,'Iteration',centered,0);link(g,half,0,centered,1)
    height=math_node(g,'MULTIPLY',800,130);link(g,centered,0,height,0);link(g,interval,0,height,1)
    contour=contour_instance(g,body,'Geometry',height,0,1020,130,extent=200)
    flat=flatten_profile(g,contour,height,1250,130)
    registered=bpy.data.node_groups.get('Registered Profile to Solid') or registered_profile_group()
    part=native(g,'GeometryNodeGroup',1910,130);part.node_tree=registered
    link(g,flat,'Geometry',part,'Curve');link(g,gi,'Sheet Thickness',part,'Thickness');link(g,gi,'Hole Radius',part,'Hole Radius')
    store=add_part_index(g,part,'Geometry',ri,2150,130)
    if layout:
        position=layout_vector(g,gi,ri,2150,-240)
        shift=native(g,'ShaderNodeVectorMath',2970,-80);shift.operation='ADD'
        link(g,position,'Vector',shift,0);value(shift,1,(40,40,0))
        placed=transform(g,store,'Geometry',x=3010,y=170)
        link(g,shift,'Vector',placed,'Translation')
    else:
        z=math_node(g,'MULTIPLY',2410,-140)
        link(g,ri,'Iteration',z,0);link(g,interval,0,z,1)
        position=native(g,'ShaderNodeCombineXYZ',2620,-140);link(g,z,0,position,'Z')
        placed=transform(g,store,'Geometry',x=3010,y=170);link(g,position,'Vector',placed,'Translation')
    join=native(g,'GeometryNodeJoinGeometry',3260,180)
    link(g,ri,'Geometry',join,'Geometry');link(g,placed,'Geometry',join,'Geometry')
    link(g,join,'Geometry',ro,'Geometry');output(g,ro,x=3770,y=180)
    return s,o,g


def modular_cell():
    g=group('Modular Cell')
    interface(g,'Thickness','NodeSocketFloat',3,2,5)
    interface(g,'Aperture Radius','NodeSocketFloat',4,2,5.5)
    interface(g,'Fit Clearance','NodeSocketFloat',.15,.05,.4)
    gi=native(g,'NodeGroupInput',-300,0)
    shapes=[]
    for i,(size,translation) in enumerate([((20,20,3),(0,0,0)),((4,6,3),(11.5,0,0)),((6,4,3),(0,11.5,0))]):
        xyz=native(g,'ShaderNodeCombineXYZ',0,160-i*300)
        value(xyz,'X',size[0]);value(xyz,'Y',size[1]);link(g,gi,'Thickness',xyz,'Z')
        c=cube(g,230,160-i*300);link(g,xyz,'Vector',c,'Size')
        t=transform(g,c,x=470,y=160-i*300,translation=translation)
        shapes.append((t,'Geometry'))
    union=boolean(g,shapes[0][0],'Geometry',shapes[1:],740,160,'UNION')
    hole=cylinder(g,740,-160,radius=4,depth=12,resolution=32)
    link(g,gi,'Aperture Radius',hole,'Radius')
    double=math_node(g,'MULTIPLY',980,-170,b=2);link(g,gi,'Fit Clearance',double,0)
    four=math_node(g,'ADD',1190,-170,b=4);link(g,double,0,four,0)
    six=math_node(g,'ADD',1190,-370,b=6);link(g,double,0,six,0)
    cuts=[(hole,'Mesh')]
    for i,loc in enumerate([(-8.5,0,0),(0,-8.5,0)]):
        xyz=native(g,'ShaderNodeCombineXYZ',1420,-140-i*320)
        link(g,four if i==0 else six,0,xyz,'X');link(g,six if i==0 else four,0,xyz,'Y');value(xyz,'Z',12)
        c=cube(g,1650,-140-i*320);link(g,xyz,'Vector',c,'Size')
        t=transform(g,c,x=1890,y=-140-i*320,translation=loc)
        cuts.append((t,'Geometry'))
    bo=boolean(g,union,'Mesh',cuts,2150,160)
    output(g,bo,'Mesh',x=2400,y=160)
    frame(g,'A SMALL CELL WITH TWO TABS AND TWO RECEIVING SLOTS','The nominal cell is 20 x 20 mm. Two tabs locate the next cells.\nFit Clearance enlarges the receiving slots; it must be tested on the printer.\nThe joints align the cells. Develop the fastening or backing strategy in your project.',x=-300,y=540,width=2900,height=170)
    return g


def final_modular():
    s,o,g=lesson_scene('03 - Modular print','NINE RELATED PARTS | TEST ONE CONNECTION',
        'Iteration varies Aperture Radius through three sizes. The cell is the same group.\nPitch = 26 mm separates parts for printing. Pitch = 20 mm shows the assembly.\nPrint a connection test before all nine. This example uses millimeter coordinates.',3300)
    s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001;s.unit_settings.length_unit='MILLIMETERS'
    interface(g,'Thickness','NodeSocketFloat',3,2,5)
    interface(g,'Base Aperture','NodeSocketFloat',3,2,3.5)
    interface(g,'Fit Clearance','NodeSocketFloat',.15,.05,.4)
    interface(g,'Pitch','NodeSocketFloat',26,20,30)
    gi=native(g,'NodeGroupInput',-300,0)
    ri,ro=repeat_pair(g,0,180,2700,180);value(ri,'Iterations',9)
    mod=math_node(g,'MODULO',220,100,b=3);link(g,ri,'Iteration',mod,0)
    radius=math_node(g,'ADD',430,100);link(g,mod,0,radius,0);link(g,gi,'Base Aperture',radius,1)
    cell=native(g,'GeometryNodeGroup',660,100);cell.node_tree=modular_cell()
    link(g,radius,0,cell,'Aperture Radius')
    for key in ('Thickness','Fit Clearance'):link(g,gi,key,cell,key)
    col=math_node(g,'MULTIPLY',940,100);link(g,mod,0,col,0);link(g,gi,'Pitch',col,1)
    div=math_node(g,'DIVIDE',940,-160,b=3);link(g,ri,'Iteration',div,0)
    row=math_node(g,'FLOOR',1140,-160);link(g,div,0,row,0)
    y=math_node(g,'MULTIPLY',1340,-160);link(g,row,0,y,0);link(g,gi,'Pitch',y,1)
    z=math_node(g,'MULTIPLY',1340,-360,b=.5);link(g,gi,'Thickness',z,0)
    xyz=native(g,'ShaderNodeCombineXYZ',1560,100);link(g,col,0,xyz,'X');link(g,y,0,xyz,'Y');link(g,z,0,xyz,'Z')
    part=add_part_index(g,cell,'Geometry',ri,1800,100)
    t=transform(g,part,'Geometry',x=2040,y=100);link(g,xyz,'Vector',t,'Translation')
    join=native(g,'GeometryNodeJoinGeometry',2450,180)
    link(g,ri,'Geometry',join,'Geometry');link(g,t,'Geometry',join,'Geometry')
    link(g,join,'Geometry',ro,'Geometry');output(g,ro,x=2960,y=180)
    return s,o,g


def build_fabrication():
    s,o,g=lesson_scene('01 - Print orientation','ORIENT THE MASSING STUDY FOR A SMALL PRINT',
        'All coordinates are millimeters. The block fits within 60 mm on every axis.\nRotate the portal onto its broad face; place the bottom at Z = 0.\nInspect layers in a slicer. This orientation turns the opening into a vertical void.',1800)
    s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001;s.unit_settings.length_unit='MILLIMETERS'
    interface(g,'Opening Width','NodeSocketFloat',18,10,24)
    gi=native(g,'NodeGroupInput',-300,-150)
    block=cube(g,0,120,(45,22,36))
    xyz=native(g,'ShaderNodeCombineXYZ',0,-180);value(xyz,'Y',26);value(xyz,'Z',26)
    link(g,gi,'Opening Width',xyz,'X')
    cutter=cube(g,250,-180);link(g,xyz,'Vector',cutter,'Size')
    cut=transform(g,cutter,x=520,y=-180,translation=(0,0,-8))
    bo=boolean(g,block,'Mesh',[(cut,'Geometry')],800,120)
    oriented=transform(g,bo,'Mesh',x=1060,y=120,rotation=(math.pi/2,0,0),translation=(0,0,11))
    output(g,oriented,x=1330,y=120)
    s,o,g=lesson_scene('02 - Fit coupon','TEST THE FIT BEFORE THE BATCH',
        'Three trial holes for a nominal 3 mm rod: 3.1, 3.3 and 3.5 mm diameters.\nChange Radial Allowance after a real material and machine test.\nThe coupon is 3 mm thick. The section parts and spacers use the same stock.',2200)
    s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001;s.unit_settings.length_unit='MILLIMETERS'
    interface(g,'Radial Allowance','NodeSocketFloat',.05,0,.3)
    gi=native(g,'NodeGroupInput',-300,0)
    block=cube(g,0,150,(24,12,3))
    cuts=[]
    for i in range(3):
        radius=math_node(g,'ADD',0,-160-i*260,b=1.5+i*.1)
        link(g,gi,'Radial Allowance',radius,0)
        c=cylinder(g,250,-160-i*300,depth=10,resolution=32)
        link(g,radius,0,c,'Radius')
        t=transform(g,c,x=520,y=-160-i*330,translation=(-7+i*7,0,0))
        cuts.append((t,'Geometry'))
    bo=boolean(g,block,'Mesh',cuts,830,150)
    t=transform(g,bo,'Mesh',x=1090,y=150,translation=(0,0,1.5))
    output(g,t,x=1360,y=150)
    final_modular()
    final_sections(False);final_sections(True)
    s,o,g=lesson_scene('06 - Spacer rings','SPACERS PRESERVE THE SECTION INTERVAL',
        'Two rings between each pair of sections: 22 rings for 12 sections.\nThey use the same stock thickness and hole radius as the section parts.\nMatch Count, thickness and Hole Radius across the assembly, layout and spacers.',2000)
    s.unit_settings.system='METRIC';s.unit_settings.scale_length=.001;s.unit_settings.length_unit='MILLIMETERS'
    interface(g,'Section Count','NodeSocketInt',12,4,12)
    interface(g,'Sheet Thickness','NodeSocketFloat',3,1,3)
    interface(g,'Hole Radius','NodeSocketFloat',1.65,1.5,2)
    gi=native(g,'NodeGroupInput',-300,0)
    outer=cylinder(g,0,130,radius=3,depth=3,resolution=32)
    link(g,gi,'Sheet Thickness',outer,'Depth')
    inner=cylinder(g,0,-180,radius=1.65,depth=10,resolution=32)
    link(g,gi,'Hole Radius',inner,'Radius')
    bo=boolean(g,outer,'Mesh',[(inner,'Mesh')],280,130)
    half=math_node(g,'MULTIPLY',280,-200,b=.5);link(g,gi,'Sheet Thickness',half,0)
    loc=native(g,'ShaderNodeCombineXYZ',490,-200);link(g,half,0,loc,'Z')
    ring=transform(g,bo,'Mesh',x=520,y=130);link(g,loc,'Vector',ring,'Translation')
    cols=math_node(g,'SUBTRACT',0,-490,b=1);link(g,gi,'Section Count',cols,0)
    spaces=math_node(g,'SUBTRACT',220,-490,b=1);link(g,cols,0,spaces,0)
    width=math_node(g,'MULTIPLY',420,-490,b=10);link(g,spaces,0,width,0)
    grid=grid_node(g,780,-150,count=2,size=10)
    value(grid,'Vertices Y',2);value(grid,'Size Y',10)
    link(g,cols,0,grid,'Vertices X');link(g,width,0,grid,'Size X')
    inst=native(g,'GeometryNodeInstanceOnPoints',1050,130)
    link(g,grid,'Mesh',inst,'Points');link(g,ring,'Geometry',inst,'Instance')
    real=native(g,'GeometryNodeRealizeInstances',1300,130);link(g,inst,'Instances',real,'Geometry')
    t=transform(g,real,'Geometry',x=1550,y=130,translation=(65,270,0))
    output(g,t,x=1820,y=130)
    for scene in SCENES:
        st=mesh_stats(scene)
        assert st['volume']>0 and st['nonmanifold_edges']==0,(scene.name,st)
        assert st['bounds'][2][0]>-.0001,(scene.name,st)
    first=mesh_stats(SCENES[0])
    assert max(b-a for a,b in first['bounds'])<=60
    assembled=mesh_stats(SCENES[3]);laid=mesh_stats(SCENES[4])
    assert abs(assembled['volume']-laid['volume'])<.2,(assembled,laid)
    assert 0<laid['bounds'][0][0]<laid['bounds'][0][1]<400 and 0<laid['bounds'][1][0]<laid['bounds'][1][1]<250,laid
    save_lesson(hero=3)
    export_fabrication()


def export_stl(scene,path):
    activate(scene);obj=scene.view_layers[0].objects.active
    ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();mesh.calc_loop_triangles()
    with path.open('wb') as f:
        f.write(b'ARC3133 default-parameter snapshot; coordinates in millimeters'.ljust(80,b' '))
        f.write(struct.pack('<I',len(mesh.loop_triangles)))
        for tri in mesh.loop_triangles:
            coords=[obj.matrix_world@mesh.vertices[k].co for k in tri.vertices]
            normal=(coords[1]-coords[0]).cross(coords[2]-coords[0]).normalized()
            f.write(struct.pack('<12fH',*normal,*coords[0],*coords[1],*coords[2],0))
    ev.to_mesh_clear()


def bottom_loops(scene):
    activate(scene);obj=scene.view_layers[0].objects.active
    ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
    verts=[obj.matrix_world@v.co for v in mesh.vertices]
    edge_count={}
    for p in mesh.polygons:
        if all(abs(verts[v].z)<.0001 for v in p.vertices):
            for edge in p.edge_keys:
                key=tuple(sorted(edge));edge_count[key]=edge_count.get(key,0)+1
    boundary={e for e,count in edge_count.items() if count==1}
    adj={}
    for a,b in boundary:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
    assert all(len(v)==2 for v in adj.values()), 'Cutting boundaries must be closed loops'
    loops=[]
    while boundary:
        a,b=next(iter(boundary));boundary.remove(tuple(sorted((a,b))))
        ids=[a,b]
        while ids[-1]!=ids[0]:
            last,prev=ids[-1],ids[-2]
            nxt=next(v for v in adj[last] if v!=prev)
            boundary.remove(tuple(sorted((last,nxt))))
            ids.append(nxt)
        loops.append([(verts[k].x,verts[k].y) for k in ids[:-1]])
    ev.to_mesh_clear()
    return loops


def export_fabrication():
    folder=FILES/CATALOG['fabrication'][0]
    for index,name in [(0,'small-print-mm.stl'),(1,'fit-coupon-mm.stl'),(2,'modular-parts-mm.stl')]:
        export_stl(SCENES[index],folder/name)
    sections=bottom_loops(SCENES[4]);rings=bottom_loops(SCENES[5])
    assert len(sections)==36, ('Expected 12 outlines and 24 registration holes',len(sections))
    assert len(rings)==44, ('Expected 22 ring outlines and 22 ring holes',len(rings))
    loops=sections+rings
    assert all(0<=x<=400 and 0<=y<=300 for line in loops for x,y in line)
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="400mm" height="300mm" viewBox="0 0 400 300">',
         '<title>ARC 3133 section parts and spacers — default parameter snapshot</title>',
         '<desc>Millimeters. 12 sections, 24 registration holes, 22 spacers. Confirm stock, kerf and fit before cutting. No kerf compensation has been applied.</desc>',
         '<g id="cut" fill="none" stroke="black" stroke-width="0.1">']
    for line in loops:
        svg.append('<path d="M '+' L '.join(f'{x:.5f},{300-y:.5f}' for x,y in line)+' Z"/>')
    svg+=['</g>','<g id="labels-optional-engraving" fill="blue" font-family="sans-serif" font-size="3">']
    for i in range(12):
        x=40+(i%4)*80;y=40+(i//4)*80
        svg.append(f'<text x="{x}" y="{300-y-10}" text-anchor="middle">{i+1:02d}</text>')
    svg+=['<text x="140" y="30">22 spacers — same stock</text>','</g>','</svg>']
    (folder/'section-parts-and-spacers-mm.svg').write_text('\n'.join(svg)+'\n',encoding='utf-8')
    (folder/'FABRICATION-NOTES.md').write_text('''# Fabrication examples

These are teaching prototypes and snapshots of the saved default parameters. Regenerate exports after changing the Blender graphs. Physical fit and printer settings have not been tested on a machine.

- **Small print:** 45 × 36 × 22 mm, with its broad face on Z = 0. Inspect the layer preview before printing.
- **Modular parts:** nine separate parts in a spaced print layout, with three aperture sizes. Pitch 20 mm shows how the cells assemble; Pitch 26 mm separates them for printing. Test a joint and develop a fastening/backing strategy.
- **Fit coupon:** nominal 3 mm stock, with trial hole diameters 3.1, 3.3 and 3.5 mm. Test the actual material, machine and rod.
- **Sections:** 12 numbered parts, two holes per part and 22 spacer rings. Use two nominal 3 mm rods approximately 72 mm long; determine end retention through the prototype. The part and spacer thickness is 3 mm, giving a 6 mm section interval and a 69 mm stack.
- **Cutting layout:** an example 400 × 300 mm sheet; confirm the available stock. SVG coordinates are millimeters. Black paths are closed cutting boundaries. Blue labels are a separate optional engraving group. Kerf compensation has not been applied.

Match Count, Sheet Thickness and Hole Radius in the registered-section, cutting-layout and spacer scenes before producing a new cutting file. The scenes are separate examples with independent modifier values. The geometry within each scene remains parametric.

The original curved volume extends beyond the first and last sampled planes. The section model is a finite, cropped interpretation of that volume. Compare it with the source rather than claiming an exact reconstruction.

The print and cutting examples are starting points for the final project. Follow the assignment brief for design development, physical testing, documentation and the final booklet.
''',encoding='utf-8')
    print('FABRICATION_EXPORTS '+json.dumps({'section_cut_loops':len(sections),'spacer_cut_loops':len(rings),'sheet_mm':[400,300],'stl_units':'mm'}),flush=True)


BUILDERS={'intro':build_intro,'arrays':build_arrays,'attractors':build_attractors,'tessellation':build_tessellation,'clouds':build_clouds,'volumes':build_volumes,'discretization':build_discretization,'fabrication':build_fabrication}

if __name__ == '__main__':
    import sys
    p=argparse.ArgumentParser()
    p.add_argument('--lesson',required=True,choices=CATALOG)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    begin(args.lesson)
    BUILDERS[args.lesson]()
