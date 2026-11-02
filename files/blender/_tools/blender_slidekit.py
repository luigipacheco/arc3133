"""blender_slidekit.py: helpers for interactive Blender slides (ARC 3133).

Run inside Blender (Text Editor > Run, or through the Blender MCP). It registers
a dict SK in bpy.app.driver_namespace so later scripts can do:

    SK = bpy.app.driver_namespace['SK']

Method and conventions: files/blender/BLENDER-INTERACTIVE-SLIDES.md
Shared UI node groups (UI · Paint, UI · Labels, ...) are appended from
files/blender/Introduction-to-Parametric-Design.blend when missing.
"""
import bpy, math, os, mathutils

_HERE = os.path.dirname(bpy.data.filepath or "")
REF = next((p for p in (os.path.join(d, "Introduction-to-Parametric-Design.blend")
                        for d in (_HERE, os.path.dirname(_HERE), os.path.dirname(os.path.dirname(_HERE))))
            if os.path.exists(p)), os.path.join(_HERE, "Introduction-to-Parametric-Design.blend"))
UI_GROUPS = ["UI · Paint", "UI · Tint", "UI · Labels", "UI · Text", "UI · Card",
             "UI · Outline", "UI · Nice Range", "UI · Ruler"]
FONTS = {"bold": "arialbd.ttf", "reg": "arial.ttf", "mono": "courbd.ttf"}
FONT_DIR = "C:/Windows/Fonts/"
HEX = dict(BLACK="000000", CREAM="FFFDF7", LIME="C6F035", PINK="FF4D8D", CYAN="00D9E1",
           YELLOW="FFE500", GREY="6B6B6B", MUTE="B4B4AC", PAPER="F4F4EE", LINE="E2E2DA", WHITE="FFFFFF")
ISO = (math.degrees(math.atan(math.sqrt(2))), 0.0, 135.0)   # true isometric


def lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


PAL = {k: lin(v) for k, v in HEX.items()}


# ---------- materials, world, fonts ----------
def emission_mat(name, col):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (*col, 1)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); o.location = (250, 0)
    nt.links.new(e.outputs[0], o.inputs['Surface'])
    m.diffuse_color = (*col, 1)
    return m


def append_ui_groups(path=REF):
    missing = [g for g in UI_GROUPS if g not in bpy.data.node_groups]
    if missing and os.path.exists(path):
        with bpy.data.libraries.load(path, link=False) as (src, dst):
            dst.node_groups = [g for g in src.node_groups if g in missing]
    return [g for g in UI_GROUPS if g not in bpy.data.node_groups]


# ---------- node helpers ----------
def node(nt, t, loc, **kw):
    n = nt.nodes.new(t); n.location = loc
    for k, v in kw.items():
        setattr(n, k, v)
    return n


def link(nt, a, ao, b, bi):
    return nt.links.new(a.outputs[ao], b.inputs[bi])


def sv(n, key, val):
    n.inputs[key].default_value = val


def gsock(nt, name, io, stype, default=None, mn=None, mx=None, desc="", subtype=None):
    s = nt.interface.new_socket(name=name, in_out=io, socket_type=stype)
    if default is not None: s.default_value = default
    if mn is not None: s.min_value = mn
    if mx is not None: s.max_value = mx
    if desc: s.description = desc
    if subtype: s.subtype = subtype
    return s


def new_tree(name):
    nt = bpy.data.node_groups.get(name)
    if nt:
        bpy.data.node_groups.remove(nt)
    return bpy.data.node_groups.new(name, 'GeometryNodeTree')


def comment(nt, key, body, loc, w=420, h=160, col=(0.16, 0.16, 0.10)):
    """Blender 5.2 has no Comment node: a Frame showing a Text datablock."""
    t = bpy.data.texts.get(key) or bpy.data.texts.new(key)
    t.clear(); t.write(body)
    f = nt.nodes.new('NodeFrame'); f.text = t; f.shrink = False; f.label_size = 14
    f.location = loc; f.width = w; f.height = h
    f.use_custom_color = True; f.color = col
    return f


def frame(nt, label, nodes, col=None):
    f = nt.nodes.new('NodeFrame'); f.label = label; f.label_size = 20
    if col:
        f.use_custom_color = True; f.color = col
    for n in nodes:
        a = n.location_absolute.copy(); n.parent = f; n.location_absolute = a
    return f


def grp(nt, tree, loc, **vals):
    g = node(nt, 'GeometryNodeGroup', loc); g.node_tree = tree
    for k, v in vals.items():
        g.inputs[k].default_value = v
    return g


def join(nt, delim, outs, loc):
    j = node(nt, 'GeometryNodeStringJoin', loc); j.inputs['Delimiter'].default_value = delim
    for o in reversed(outs):          # Join Strings stacks new links on top
        nt.links.new(o, j.inputs['Strings'])
    return j


def lit(nt, s, loc):
    n = node(nt, 'FunctionNodeInputString', loc); n.string = s
    return n.outputs[0]


def M(nt, op, loc, a=None, b=None, bv=None, av=None, c=None):
    m = node(nt, 'ShaderNodeMath', loc); m.operation = op
    if a is not None: nt.links.new(a, m.inputs[0])
    if av is not None: m.inputs[0].default_value = av
    if b is not None: nt.links.new(b, m.inputs[1])
    if bv is not None: m.inputs[1].default_value = bv
    if c is not None: nt.links.new(c, m.inputs[2])
    return m.outputs[0]


def hide_unused(nt):
    for n in nt.nodes:
        if n.bl_idname == 'NodeGroupInput':
            for s in n.outputs:
                if not s.is_linked:
                    s.hide = True


# ---------- slides ----------
def text_obj(name, body, font, size, loc, parent, mat, align='LEFT', width=0, coll=None):
    cu = bpy.data.curves.get(name) or bpy.data.curves.new(name, 'FONT')
    cu.body = body; cu.font = font; cu.size = size; cu.align_x = align; cu.align_y = 'TOP'
    if width:
        cu.text_boxes[0].width = width
    cu.materials.clear(); cu.materials.append(mat)
    ob = bpy.data.objects.get(name) or bpy.data.objects.new(name, cu)
    ob.data = cu
    if ob.name not in coll.objects:
        coll.objects.link(ob)
    ob.parent = parent; ob.location = (loc[0], loc[1], 0); ob.rotation_euler = (0, 0, 0)
    return ob


def make_slide(key, num, title, body, try_text, cam_loc, cam_rot=(0, 0, 0), scale=16.0, col_w=5.3,
               total=11, tag="ARC 3133  VIZ 1  ·  FROM A LIST TO A FACADE"):
    sc = bpy.data.scenes.get(key) or bpy.data.scenes.new(key)
    sc.world = SK['WORLD']; sc.render.engine = 'BLENDER_EEVEE'
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.view_settings.view_transform = 'Standard'
    coll = bpy.data.collections.get("Slide UI " + key) or bpy.data.collections.new("Slide UI " + key)
    if coll.name not in sc.collection.children:
        sc.collection.children.link(coll)
    coll.hide_select = True
    cd = bpy.data.cameras.get("Cam " + key) or bpy.data.cameras.new("Cam " + key)
    cd.type = 'ORTHO'; cd.ortho_scale = scale; cd.clip_start = 0.01; cd.clip_end = 500
    cam = bpy.data.objects.get("Camera " + key) or bpy.data.objects.new("Camera " + key, cd)
    if cam.name not in coll.objects:
        coll.objects.link(cam)
    cam.location = cam_loc; cam.rotation_euler = [math.radians(a) for a in cam_rot]; sc.camera = cam
    hud = bpy.data.objects.get("HUD " + key) or bpy.data.objects.new("HUD " + key, None)
    if hud.name not in coll.objects:
        coll.objects.link(hud)
    hud.parent = cam; hud.location = (0, 0, -1); hud.scale = (scale / 16,) * 3; hud.empty_display_size = 0.01
    F = SK['FONT']; T = lambda n: f"{key} · {n}"
    text_obj(T("tag"), tag, F['mono'], 0.2, (-7.5, 4.15), hud, SK['INKG'], coll=coll)
    if num is not None:
        text_obj(T("number"), f"{num:02d} / {total:02d}", F['mono'], 0.2, (7.5, 4.15), hud, SK['INKG'], align='RIGHT', coll=coll)
    two = "\n" in title
    text_obj(T("title"), title, F['bold'], 0.62, (-7.5, 3.55), hud, SK['INK'], width=col_w + 1.5, coll=coll)
    me = bpy.data.meshes.get(T("rule")) or bpy.data.meshes.new(T("rule"))
    if not me.vertices:
        me.from_pydata([(0, 0, 0), (1.4, 0, 0), (1.4, -0.14, 0), (0, -0.14, 0)], [], [(0, 1, 2, 3)])
        me.materials.append(SK['LIME'])
    rule = bpy.data.objects.get(T("rule")) or bpy.data.objects.new(T("rule"), me)
    if rule.name not in coll.objects:
        coll.objects.link(rule)
    rule.parent = hud; rule.location = (-7.5, 2.05 if two else 2.75, 0)
    if body:
        text_obj(T("body"), body, F['reg'], 0.27, (-7.5, 1.6 if two else 2.4), hud, SK['INK'], width=col_w, coll=coll)
    if try_text:
        t = text_obj(T("try"), "TRY\n" + try_text, F['bold'], 0.25, (-7.5, -3.4), hud, SK['INKP'], width=col_w, coll=coll)
    return sc, cam, hud


def aim(cam, target, rot_deg, scale, dist=40, shift=2.9):
    """Point an ortho camera at target; shift moves the target into the right half of the slide."""
    R = mathutils.Euler([math.radians(a) for a in rot_deg]).to_matrix()
    cam.rotation_euler = [math.radians(a) for a in rot_deg]
    cam.location = mathutils.Vector(target) + R @ mathutils.Vector((-shift * scale / 16, 0, dist))


def cam_point(sc, x, y, depth=25):
    cam = sc.camera
    return tuple(cam.matrix_world.translation + cam.matrix_world.to_3x3() @ mathutils.Vector((x, y, -depth)))


def slide_object(sc, name, tree):
    me = bpy.data.meshes.get(name) or bpy.data.meshes.new(name)
    ob = bpy.data.objects.get(name) or bpy.data.objects.new(name, me)
    if ob.name not in sc.collection.objects:
        sc.collection.objects.link(ob)
    return ob


def two_mods(sc_name, lesson, ui):
    """Lesson modifier first (node editor shows it), display modifier second."""
    sc = bpy.data.scenes[sc_name]
    ob = slide_object(sc, sc_name, lesson)
    ob.data.materials.clear(); ob.data.materials.append(SK['VIZI'])
    for m in list(ob.modifiers):
        ob.modifiers.remove(m)
    m1 = ob.modifiers.new("GeometryNodes", 'NODES'); m1.node_group = lesson
    m2 = ob.modifiers.new("UI", 'NODES'); m2.node_group = ui
    ob.modifiers.active = m1
    set_defaults(ob)
    vl = sc.view_layers[0]
    for o in sc.objects:
        o.select_set(False, view_layer=vl)
    ob.select_set(True, view_layer=vl); vl.objects.active = ob
    return ob, m1, m2


def set_defaults(ob):
    """New group inputs on an existing modifier start at 0: copy the interface defaults."""
    for m in ob.modifiers:
        if m.type != 'NODES' or not m.node_group:
            continue
        for it in m.node_group.interface.items_tree:
            if getattr(it, 'in_out', '') == 'INPUT' and it.socket_type not in ('NodeSocketGeometry', 'NodeSocketObject', 'NodeSocketMenu'):
                try:
                    getattr(m.properties.inputs, it.identifier).value = it.default_value
                except Exception:
                    pass


def set_input(ob, mod_name, name, value):
    m = ob.modifiers[mod_name]
    it = [i for i in m.node_group.interface.items_tree if getattr(i, 'name', '') == name][0]
    getattr(m.properties.inputs, it.identifier).value = value
    ob.update_tag()


def snap(sc, name, folder=None):
    """Render a quick 50 % still to check a slide."""
    folder = folder or os.path.join(os.path.dirname(os.path.dirname(bpy.data.filepath)), "_check")
    sc.render.filepath = os.path.join(folder, name + ".png")
    sc.render.resolution_percentage = 50; sc.eevee.taa_render_samples = 8
    with bpy.context.temp_override(scene=sc):
        bpy.ops.render.render(write_still=True, scene=sc.name)
    sc.render.resolution_percentage = 100
    return sc.render.filepath


# ---------- register ----------
SK = {}


def setup():
    SK.update(PAL=PAL, ISO=ISO)
    SK['FONT'] = {k: bpy.data.fonts.load(FONT_DIR + f, check_existing=True) for k, f in FONTS.items()}
    SK['INK'] = emission_mat("Ink", PAL['BLACK']); SK['INKG'] = emission_mat("Ink Grey", PAL['GREY'])
    SK['INKP'] = emission_mat("Ink Pink", PAL['PINK']); SK['LIME'] = emission_mat("Lime", PAL['LIME'])
    missing = append_ui_groups()   # brings the Viz and Viz Instances materials along
    SK['VIZ'] = bpy.data.materials.get("Viz"); SK['VIZI'] = bpy.data.materials.get("Viz Instances")
    w = bpy.data.worlds.get("Slide Paper") or bpy.data.worlds.new("Slide Paper")
    w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (*PAL['CREAM'], 1)
    SK['WORLD'] = w
    SK.update(node=node, link=link, sv=sv, gsock=gsock, new_tree=new_tree, comment=comment, frame=frame,
              grp=grp, join=join, lit=lit, M=M, hide_unused=hide_unused, text_obj=text_obj,
              make_slide=make_slide, aim=aim, cam_point=cam_point, slide_object=slide_object,
              two_mods=two_mods, set_defaults=set_defaults, set_input=set_input, snap=snap)
    bpy.app.driver_namespace['SK'] = SK
    print("blender_slidekit ready.", "Missing UI groups: " + ", ".join(missing) if missing else "")


setup()
