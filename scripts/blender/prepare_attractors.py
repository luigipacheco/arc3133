"""Build the attractor lesson in a separate factory-startup Blender process.

Never run in a student's live file. Native nodes keep their names and labels.
The previous teaching file is preserved before the first replacement.
"""
import bpy
import json
import math
from pathlib import Path
from mathutils import Vector, Quaternion

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "files/blender/04-attractors"
FILE = DEST / "Attractors.blend"
BACKUP = ROOT / "reference/archive/2026-10-20-attractors/Attractors-before-opening-lesson.blend"
assert bpy.app.background, "Use a separate background Blender process."
assert not bpy.data.filepath, "Start with --factory-startup; do not replace a working file."
if FILE.exists() and not BACKUP.exists():
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(FILE.read_bytes())
bpy.ops.wm.read_factory_settings(use_empty=True)


def enum(obj, prop, value):
    choices = [x.identifier for x in obj.bl_rna.properties[prop].enum_items]
    assert value in choices, (prop, value, choices)
    setattr(obj, prop, value)


def node(g, kind, x, y, frame=None):
    n = g.nodes.new(kind)
    n.parent = frame
    n.location = (x, y)
    n.width = 175
    return n


def frame(g, title, x, y):
    n = g.nodes.new("NodeFrame")
    n.label = title
    n.location = (x, y)
    n.label_size = 24
    return n


def wire(g, a, out, b, inp):
    g.links.new(a.outputs[out], b.inputs[inp])


def socket(g, name, kind, direction="INPUT", default=None, lo=None, hi=None):
    s = g.interface.new_socket(name=name, in_out=direction, socket_type=kind)
    if default is not None:
        s.default_value = default
    if lo is not None:
        s.min_value = lo
    if hi is not None:
        s.max_value = hi
    return s


def group(name):
    g = bpy.data.node_groups.new(name, "GeometryNodeTree")
    socket(g, "Geometry", "NodeSocketGeometry", "OUTPUT")
    return g


def material(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = .65
    m.diffuse_color = color
    return m


WHITE = material("Panel - warm white", (.72, .78, .8, 1))
ORANGE = material("Attractor - orange", (1, .16, .025, 1))
BLUE = material("Field samples - blue", (.035, .36, .62, 1))


def attach(scene, name, g):
    ob = bpy.data.objects.new(name, bpy.data.meshes.new(name))
    scene.collection.objects.link(ob)
    mod = ob.modifiers.new("GeometryNodes", "NODES")
    g.is_modifier = True
    mod.node_group = g
    scene.view_layers[0].objects.active = ob
    ob.select_set(True)
    ob.color = (.72, .78, .8, 1)
    return ob


def point(scene, name, location):
    ob = bpy.data.objects.new(name, None)
    scene.collection.objects.link(ob)
    ob.location = location
    ob.empty_display_size = .35
    enum(ob, "empty_display_type", "SPHERE")
    ob.show_in_front = True
    # Renderable marker follows the same movable empty.
    mesh = bpy.data.meshes.new(name + " marker")
    r = .14
    mesh.from_pydata([(r,0,0),(-r,0,0),(0,r,0),(0,-r,0),(0,0,r),(0,0,-r)], [],
                     [(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)])
    marker = bpy.data.objects.new(name + " marker", mesh)
    scene.collection.objects.link(marker)
    marker.parent = ob
    marker.location = (0,-.25,0)
    marker.data.materials.append(ORANGE)
    marker.hide_select = True
    marker.color = (1,.16,.025,1)
    return ob


def curve(scene):
    data = bpy.data.curves.new("Attractor curve", "CURVE")
    enum(data, "dimensions", "3D")
    data.resolution_u = 16
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(3)
    for p, co in zip(spline.bezier_points, [(-4,0,1.2),(-1.5,0,4.9),(1.5,0,2),(4,0,5)]):
        p.co = co
        enum(p,"handle_left_type","AUTO")
        enum(p,"handle_right_type","AUTO")
    ob = bpy.data.objects.new("Attractor curve - edit its control points", data)
    scene.collection.objects.link(ob)
    ob.show_in_front = True
    # A linked display copy gives the target a visible stroke without making
    # Geometry Proximity measure a tube's surface instead of the centerline.
    display = bpy.data.objects.new("Curve marker - follows curve", data)
    scene.collection.objects.link(display)
    display.parent = ob
    display.location = (0,-.22,0)
    display.hide_select = True
    display.color = (1,.16,.025,1)
    g = group("Curve marker")
    socket(g, "Geometry", "NodeSocketGeometry")
    i = node(g,"NodeGroupInput",0,0)
    c = node(g,"GeometryNodeCurvePrimitiveCircle",0,-200)
    c.inputs["Resolution"].default_value = 8
    c.inputs["Radius"].default_value = .035
    t = node(g,"GeometryNodeCurveToMesh",220,0)
    wire(g,i,"Geometry",t,"Curve")
    wire(g,c,"Curve",t,"Profile Curve")
    m = node(g,"GeometryNodeSetMaterial",440,0)
    m.inputs["Material"].default_value = ORANGE
    wire(g,t,"Mesh",m,"Geometry")
    o = node(g,"NodeGroupOutput",660,0)
    wire(g,m,"Geometry",o,"Geometry")
    display.modifiers.new("GeometryNodes","NODES").node_group = g
    return ob


def info(g, obj, x, y, f):
    n = node(g,"GeometryNodeObjectInfo",x,y,f)
    enum(n,"transform_space","RELATIVE")
    n.inputs["Object"].default_value = obj
    n.inputs["As Instance"].default_value = False
    return n


def field(g, scene, kind, near, far):
    f = frame(g,"02  Measure distance",0,-500)
    pos = node(g,"GeometryNodeInputPosition",0,0,f)
    if kind == "curve":
        ob = curve(scene)
        oi = info(g,ob,0,-120,f)
        cm = node(g,"GeometryNodeCurveToMesh",220,-120,f)
        wire(g,oi,"Geometry",cm,"Curve")
        prox = node(g,"GeometryNodeProximity",440,0,f)
        enum(prox,"target_element","EDGES")
        wire(g,cm,"Mesh",prox,"Geometry")
        wire(g,pos,"Position",prox,"Sample Position")
        source, output = prox, "Distance"
    else:
        ob = point(scene,"Point A - move me",(-2,0,3.3))
        oi = info(g,ob,0,-140,f)
        a = node(g,"ShaderNodeVectorMath",220,0,f)
        enum(a,"operation","DISTANCE")
        wire(g,pos,"Position",a,0)
        wire(g,oi,"Location",a,1)
        source, output = a, "Value"
        if kind == "multi":
            ob2 = point(scene,"Point B - move me",(2.4,0,2.2))
            oi2 = info(g,ob2,0,-390,f)
            b = node(g,"ShaderNodeVectorMath",220,-310,f)
            enum(b,"operation","DISTANCE")
            wire(g,pos,"Position",b,0)
            wire(g,oi2,"Location",b,1)
            minimum = node(g,"ShaderNodeMath",440,0,f)
            enum(minimum,"operation","MINIMUM")
            wire(g,a,"Value",minimum,0)
            wire(g,b,"Value",minimum,1)
            source, output = minimum, "Value"
            f.label = "02  Nearest of two points"
    f = frame(g,"03  Near to far",720,-500)
    mr = node(g,"ShaderNodeMapRange",0,0,f)
    enum(mr,"interpolation_type","LINEAR")
    mr.clamp = True
    mr.inputs["From Min"].default_value = 0
    mr.inputs["From Max"].default_value = 4
    mr.inputs["To Min"].default_value = near
    mr.inputs["To Max"].default_value = far
    wire(g,source,output,mr,"Value")
    return pos, mr


# A real parametric prefab: fixed outer dimensions, variable through-opening.
PANEL = group("Panel - Opening")
socket(PANEL,"Opening","NodeSocketFloat",default=.55,lo=.1,hi=.9)
socket(PANEL,"Thickness","NodeSocketFloat",default=.12,lo=.05,hi=.3)
f = frame(PANEL,"01  Fixed outside, variable cutter",0,0)
i = node(PANEL,"NodeGroupInput",0,0,f)
outer = node(PANEL,"ShaderNodeCombineXYZ",220,100,f)
outer.inputs["X"].default_value = outer.inputs["Y"].default_value = 1
wire(PANEL,i,"Thickness",outer,"Z")
inner = node(PANEL,"ShaderNodeCombineXYZ",220,-140,f)
wire(PANEL,i,"Opening",inner,"X")
wire(PANEL,i,"Opening",inner,"Y")
inner.inputs["Z"].default_value = 1
c1 = node(PANEL,"GeometryNodeMeshCube",440,100,f)
c2 = node(PANEL,"GeometryNodeMeshCube",440,-240,f)
wire(PANEL,outer,"Vector",c1,"Size")
wire(PANEL,inner,"Vector",c2,"Size")
f2 = frame(PANEL,"02  Subtract the opening",700,0)
boolean = node(PANEL,"GeometryNodeMeshBoolean",0,0,f2)
enum(boolean,"operation","DIFFERENCE")
enum(boolean,"solver","EXACT")
wire(PANEL,c1,"Mesh",boolean,"Mesh 1")
wire(PANEL,c2,"Mesh",boolean,"Mesh 2")
o = node(PANEL,"NodeGroupOutput",940,0)
wire(PANEL,boolean,"Mesh",o,"Geometry")
PANEL.use_fake_user = True


def finish(g, geom, outsocket, x):
    f = frame(g,"05  DISPLAY",x,0)
    mat = node(g,"GeometryNodeSetMaterial",0,0,f)
    mat.inputs["Material"].default_value = WHITE
    wire(g,geom,outsocket,mat,"Geometry")
    out = node(g,"NodeGroupOutput",220,0,f)
    wire(g,mat,"Geometry",out,"Geometry")


SCENES = [
    ("01 - Read the field","point","field"),
    ("02 - One point","point","scale"),
    ("03 - Multiple points","multi","scale"),
    ("04 - Curve attractor","curve","scale"),
    ("05 - Panel prefab","point","prefab"),
    ("06 - One point opening","point","opening"),
    ("07 - Multiple point openings","multi","opening"),
    ("08 - Curve openings","curve","opening"),
]
for title, kind, mode in SCENES:
    scene = bpy.data.scenes.new(title)
    bpy.context.window.scene = scene
    scene.world = bpy.data.worlds.new(title)
    scene.world.color = (.06,.06,.06)
    g = group(title)
    ob = attach(scene,title,g)
    ob["lesson_mode"] = mode
    ob["attractor_method"] = kind
    if mode == "prefab":
        socket(g,"Opening","NodeSocketFloat",default=.55,lo=.1,hi=.9)
        f = frame(g,"01  Test the Opening input",0,0)
        i = node(g,"NodeGroupInput",0,0,f)
        panel = node(g,"GeometryNodeGroup",220,0,f)
        panel.node_tree = PANEL
        wire(g,i,"Opening",panel,"Opening")
        transform = node(g,"GeometryNodeTransform",440,0,f)
        transform.inputs["Rotation"].default_value = (math.pi/2,0,0)
        transform.inputs["Translation"].default_value = (0,0,3.3)
        wire(g,panel,"Geometry",transform,"Geometry")
        finish(g,transform,"Geometry",720)
    else:
        f = frame(g,"01  Panel locations: 9 x 7",0,100)
        grid = node(g,"GeometryNodeMeshGrid",0,0,f)
        grid.inputs["Size X"].default_value = 8.8
        grid.inputs["Size Y"].default_value = 6.6
        grid.inputs["Vertices X"].default_value = 9
        grid.inputs["Vertices Y"].default_value = 7
        place = node(g,"GeometryNodeTransform",220,0,f)
        place.inputs["Rotation"].default_value = (math.pi/2,0,0)
        place.inputs["Translation"].default_value = (0,0,3.3)
        wire(g,grid,"Mesh",place,"Geometry")
        near, far = (.85,.15) if mode=="opening" else (1,.25)
        pos, mr = field(g,scene,kind,near,far)
        if mode=="opening":
            f = frame(g,"04  Build one panel per location",1000,100)
            start = node(g,"GeometryNodeForeachGeometryElementInput",0,0,f)
            end = node(g,"GeometryNodeForeachGeometryElementOutput",690,0,f)
            start.pair_with_output(end)
            enum(end,"domain","POINT")
            end.input_items.new("VECTOR","Panel position")
            end.input_items.new("FLOAT","Opening")
            wire(g,place,"Geometry",start,"Geometry")
            wire(g,pos,"Position",start,"Panel position")
            wire(g,mr,"Result",start,"Opening")
            panel = node(g,"GeometryNodeGroup",230,0,f)
            panel.node_tree = PANEL
            wire(g,start,"Opening",panel,"Opening")
            transform = node(g,"GeometryNodeTransform",460,0,f)
            transform.inputs["Rotation"].default_value = (math.pi/2,0,0)
            wire(g,panel,"Geometry",transform,"Geometry")
            wire(g,start,"Panel position",transform,"Translation")
            wire(g,transform,"Geometry",end,"Generation_0")
            finish(g,end,"Generation_0",1970)
        else:
            f = frame(g,"04  Scale each copy",1000,100)
            cube = node(g,"GeometryNodeMeshCube",0,-230,f)
            cube.inputs["Size"].default_value = (.9,.18,.9)
            instance = node(g,"GeometryNodeInstanceOnPoints",230,0,f)
            wire(g,place,"Geometry",instance,"Points")
            wire(g,cube,"Mesh",instance,"Instance")
            wire(g,mr,"Result",instance,"Scale")
            if mode=="field":
                f.label = "04  Values become bar heights"
                cube.inputs["Size"].default_value = (.55,.12,1)
                xyz = node(g,"ShaderNodeCombineXYZ",0,-500,f)
                xyz.inputs["X"].default_value = xyz.inputs["Y"].default_value = 1
                wire(g,mr,"Result",xyz,"Z")
                wire(g,xyz,"Vector",instance,"Scale")
            real = node(g,"GeometryNodeRealizeInstances",460,0,f)
            wire(g,instance,"Instances",real,"Geometry")
            finish(g,real,"Geometry",1710)
        # Viewer exposes the actual values on the original 63 sample locations.
        # It is deliberately a side branch: the result does not depend on it.
        if mode=="field":
            f = frame(g,"Inspect values (optional)",720,-950)
            viewer = node(g,"GeometryNodeViewer",0,0,f)
            viewer.viewer_items.new("GEOMETRY","Geometry")
            viewer.viewer_items.new("FLOAT","Value")
            enum(viewer,"domain","POINT")
            wire(g,place,"Geometry",viewer,"Geometry")
            wire(g,mr,"Result",viewer,"Value")
    # An orthographic architectural view, also usable for quick renders.
    camera_data = bpy.data.cameras.new(title)
    camera = bpy.data.objects.new("Camera",camera_data)
    scene.collection.objects.link(camera)
    camera.location = (10,-22,13)
    camera.rotation_euler = (Vector((0,0,3.3))-camera.location).to_track_quat("-Z","Y").to_euler()
    enum(camera_data,"type","ORTHO")
    camera_data.ortho_scale = 13.5 if mode!="prefab" else 2.6
    scene.camera = camera
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    try:
        scene.render.engine = "BLENDER_WORKBENCH"
    except TypeError as exc:
        raise RuntimeError(str(exc))
    shading = scene.display.shading
    enum(shading,"light","STUDIO")
    enum(shading,"color_type","MATERIAL")
    enum(shading,"background_type","WORLD")
    shading.show_shadows = True
    shading.show_cavity = True
    enum(shading,"cavity_type","BOTH")
    scene.view_layers[0].objects.active = ob
    for item in g.interface.items_tree:
        if item.item_type=="SOCKET" and item.in_out=="INPUT" and hasattr(item,"default_value"):
            getattr(ob.modifiers[0].properties.inputs,item.identifier).value = item.default_value
    for other in scene.objects:
        other.select_set(other==ob)
    for n in g.nodes:
        n.select = False

empty = bpy.data.scenes.get("Scene")
if empty:
    bpy.data.scenes.remove(empty)
bpy.context.window.scene = bpy.data.scenes[SCENES[0][0]]
# Open to the Geometry Nodes workspace with the teaching object selected.
workspace = bpy.data.workspaces.get("Geometry Nodes")
if workspace:
    bpy.context.window.workspace = workspace
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=="VIEW_3D":
            space = area.spaces.active
            space.region_3d.view_rotation = Quaternion((1,0,0),math.pi/2)
            space.region_3d.view_location = (0,0,3.3)
            space.region_3d.view_distance = 13
            enum(space.region_3d,"view_perspective","ORTHO")
            enum(space.shading,"color_type","MATERIAL")
            space.overlay.show_floor = False
        elif area.type=="NODE_EDITOR":
            area.spaces.active.tree_type = "GeometryNodeTree"
            area.spaces.active.pin = False
            area.spaces.active.show_region_ui = False
            for region in area.regions:
                if region.type=="WINDOW":
                    try:
                        with bpy.context.temp_override(area=area,region=region):
                            bpy.ops.node.view_all()
                    except (RuntimeError, TypeError):
                        pass
for g in bpy.data.node_groups:
    for n in g.nodes:
        assert n.type=="FRAME" or not n.label
notes = bpy.data.texts.new("START HERE - Attractors")
notes.write((DEST/"README.md").read_text(encoding="utf-8"))
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(FILE))
print("SAVED",FILE,flush=True)
