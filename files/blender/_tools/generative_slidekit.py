"""generative_slidekit.py: helpers for Introduction-to-Generative-Design.blend (ARC 3133).
A copy of procedural_slidekit.py with its own tag, slide count and registry key (GK).

Run blender_slidekit.py first (it registers SK), then this file. It registers PD in
bpy.app.driver_namespace:

    PD = bpy.app.driver_namespace['PD']

Same method as files/blender/BLENDER-INTERACTIVE-SLIDES.md: one scene per slide, a lesson
modifier (GeometryNodes) and a display modifier (UI), code card drawn by the UI tree.
"""
import bpy, math, os, mathutils

SK = bpy.app.driver_namespace['SK']
node, gsock, new_tree, comment = SK['node'], SK['gsock'], SK['new_tree'], SK['comment']
lit, join, text_obj = SK['lit'], SK['join'], SK['text_obj']
P = SK['PAL']
TAG = "ARC 3133  VIZ 1  ·  INTRODUCTION TO GENERATIVE DESIGN"
TOTAL = 15
ISO = (math.degrees(math.atan(math.sqrt(2))), 0.0, 135.0)
TOP = (0.0, 0.0, 0.0)


def C(name, a=1.0):
    return (*P[name], a)


def G(name):
    return bpy.data.node_groups[name]


def folder():
    return os.path.join(os.path.dirname(bpy.data.filepath), "_check")


# ---------------------------------------------------------------- slide shell
def make_slide(key, num, title, body, try_text, scale=16.0, col_w=5.3, body_y=None):
    sc = bpy.data.scenes.get(key) or bpy.data.scenes.new(key)
    sc.world = SK['WORLD']; sc.render.engine = 'BLENDER_EEVEE'
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.view_settings.view_transform = 'Standard'
    coll = bpy.data.collections.get("Slide UI " + key) or bpy.data.collections.new("Slide UI " + key)
    if coll.name not in sc.collection.children:
        sc.collection.children.link(coll)
    coll.hide_select = False          # everything selectable; lock it on the collection
    cd = bpy.data.cameras.get("Cam " + key) or bpy.data.cameras.new("Cam " + key)
    cd.type = 'ORTHO'; cd.ortho_scale = scale; cd.clip_start = 0.01; cd.clip_end = 500
    cam = bpy.data.objects.get("Camera " + key) or bpy.data.objects.new("Camera " + key, cd)
    if cam.name not in coll.objects:
        coll.objects.link(cam)
    sc.camera = cam
    hud = bpy.data.objects.get("HUD " + key) or bpy.data.objects.new("HUD " + key, None)
    if hud.name not in coll.objects:
        coll.objects.link(hud)
    hud.parent = cam; hud.location = (0, 0, -1); hud.scale = (scale / 16,) * 3; hud.empty_display_size = 0.01
    F = SK['FONT']; T = lambda n: f"{key} · {n}"
    text_obj(T("tag"), TAG, F['mono'], 0.2, (-7.5, 4.15), hud, SK['INKG'], coll=coll)
    if num is not None:
        text_obj(T("number"), f"{num:02d} / {TOTAL:02d}", F['mono'], 0.2, (7.5, 4.15), hud, SK['INKG'],
                 align='RIGHT', coll=coll)
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
        by = body_y if body_y is not None else (1.6 if two else 2.4)
        text_obj(T("body"), body, F['reg'], 0.27, (-7.5, by), hud, SK['INK'], width=col_w, coll=coll)
    if try_text:
        text_obj(T("try"), "TRY\n" + try_text, F['bold'], 0.25, (-7.5, -3.45), hud, SK['INKP'], width=col_w, coll=coll)
    return sc, cam, hud


def aim(cam, target, rot=ISO, shift=2.9, lift=0.0, dist=40):
    """Ortho camera looking at target; shift puts the target in the right half of the slide."""
    s = cam.data.ortho_scale / 16
    R = mathutils.Euler([math.radians(a) for a in rot]).to_matrix()
    cam.rotation_euler = [math.radians(a) for a in rot]
    cam.location = mathutils.Vector(target) + R @ mathutils.Vector((-shift * s, -lift * s, dist))


def camp(cam, x, y, depth=20.0):
    """World point at HUD coordinates (x, y), `depth` in front of the camera."""
    s = cam.data.ortho_scale / 16
    R = mathutils.Euler(cam.rotation_euler).to_matrix()
    return tuple(mathutils.Vector(cam.location) + R @ mathutils.Vector((x * s, y * s, -depth)))


def camdir(cam, v):
    R = mathutils.Euler(cam.rotation_euler).to_matrix()
    return tuple(R @ mathutils.Vector(v))


# ---------------------------------------------------------------- tree builder
class Tree:
    """Thin wrapper over a geometry node tree with its own Group Input / Output."""

    def __init__(self, name, geo_in=False, geo_out=True):
        self.nt = new_tree(name)
        if geo_out:
            gsock(self.nt, "Geometry", 'OUTPUT', 'NodeSocketGeometry')
        if geo_in:
            gsock(self.nt, "Geometry", 'INPUT', 'NodeSocketGeometry')
        self.gi = node(self.nt, 'NodeGroupInput', (-900, 0))
        self.go = node(self.nt, 'NodeGroupOutput', (1200, 0))

    # interface
    def inp(self, name, stype, default=None, mn=None, mx=None, desc="", subtype=None):
        s = gsock(self.nt, name, 'INPUT', 'NodeSocket' + stype, default, mn, mx, desc, subtype)
        return s

    def outp(self, name, stype='Geometry'):
        return gsock(self.nt, name, 'OUTPUT', 'NodeSocket' + stype)

    def g(self, name):
        return self.gi.outputs[name]

    # nodes
    def n(self, t, loc=(0, 0), label=None, **props):
        nd = node(self.nt, t, loc)
        for k, v in props.items():
            setattr(nd, k, v)
        return nd

    def L(self, a, b):
        self.nt.links.new(a, b)

    def set(self, nd, **vals):
        for k, v in vals.items():
            nd.inputs[k.replace('_', ' ')].default_value = v
        return nd

    def math(self, op, a, b=None, loc=(0, 0)):
        m = self.n('ShaderNodeMath', loc, operation=op)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                m.inputs[i].default_value = v
            else:
                self.L(v, m.inputs[i])
        return m.outputs[0]

    def vmath(self, op, a, b=None, loc=(0, 0), out=0):
        m = self.n('ShaderNodeVectorMath', loc, operation=op)
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                m.inputs[3 if op == 'SCALE' and i == 1 else i].default_value = v
            elif isinstance(v, tuple):
                m.inputs[i].default_value = v
            else:
                self.L(v, m.inputs[3 if op == 'SCALE' and i == 1 else i])
        return m.outputs[out]

    def xyz(self, x=0.0, y=0.0, z=0.0, loc=(0, 0)):
        c = self.n('ShaderNodeCombineXYZ', loc)
        for k, v in zip("XYZ", (x, y, z)):
            if isinstance(v, (int, float)):
                c.inputs[k].default_value = v
            else:
                self.L(v, c.inputs[k])
        return c.outputs[0]

    def sep(self, v, loc=(0, 0)):
        s = self.n('ShaderNodeSeparateXYZ', loc)
        self.L(v, s.inputs[0])
        return s.outputs

    def box(self, w, d, h, loc=(0, 0)):
        """The shared Box group (base-centred)."""
        b = self.n('GeometryNodeGroup', loc); b.node_tree = G("Box")
        for k, v in zip(("Width", "Depth", "Height"), (w, d, h)):
            if isinstance(v, (int, float)):
                b.inputs[k].default_value = v
            else:
                self.L(v, b.inputs[k])
        return b

    def transform(self, geo, t=None, r=None, s=None, loc=(0, 0)):
        tr = self.n('GeometryNodeTransform', loc)
        self.L(geo, tr.inputs['Geometry'])
        if t is not None:
            if isinstance(t, tuple): tr.inputs['Translation'].default_value = t
            else: self.L(t, tr.inputs['Translation'])
        if r is not None:
            if isinstance(r, tuple):
                tr.inputs['Rotation'].default_value = [math.radians(a) for a in r]
            else:
                self.L(r, tr.inputs['Rotation'])
        if s is not None:
            if isinstance(s, tuple): tr.inputs['Scale'].default_value = s
            else: self.L(s, tr.inputs['Scale'])
        return tr.outputs[0]

    def euler(self, v, loc=(0, 0)):
        e = self.n('FunctionNodeEulerToRotation', loc)
        self.L(v, e.inputs[0])
        return e.outputs[0]

    def joing(self, socks, loc=(0, 0)):
        j = self.n('GeometryNodeJoinGeometry', loc)
        for s in reversed(socks):
            self.L(s, j.inputs[0])
        return j.outputs[0]

    def menu(self, items, dtype, loc=(0, 0)):
        m = self.n('GeometryNodeMenuSwitch', loc)
        m.data_type = dtype
        m.enum_items.clear()
        for it in items:
            m.enum_items.new(it)
        return m

    def iswitch(self, dtype, n, loc=(0, 0)):
        s = self.n('GeometryNodeIndexSwitch', loc); s.data_type = dtype
        while len(s.index_switch_items) < n:
            s.index_switch_items.new()
        return s

    def store(self, geo, name, value, dtype='BOOLEAN', domain='POINT', loc=(0, 0)):
        st = self.n('GeometryNodeStoreNamedAttribute', loc, data_type=dtype, domain=domain)
        self.L(geo, st.inputs['Geometry']); st.inputs['Name'].default_value = name
        if isinstance(value, (int, float, bool, tuple)):
            st.inputs['Value'].default_value = value
        else:
            self.L(value, st.inputs['Value'])
        return st.outputs[0]

    def frame(self, label, nodes, col=None):
        return SK['frame'](self.nt, label, nodes, col)

    def note(self, key, body, loc, w=420, h=150):
        return comment(self.nt, key, body, loc, w, h)

    def out(self, geo):
        self.L(geo, self.go.inputs[0])

    def tidy(self):
        SK['hide_unused'](self.nt)


# ---------------------------------------------------------------- UI tree
class UI(Tree):
    """Display tree: reads the lesson geometry, adds paint, outlines, ghosts, arrows, code."""

    def __init__(self, key, cam):
        super().__init__(f"{key[:2]} · UI", geo_in=True)
        self.cam = cam; self.s = cam.data.ortho_scale / 16
        self.parts = []
        self.y = -400

    def place(self):
        self.y -= 160
        return (0, self.y)

    def add(self, sock):
        self.parts.append(sock)

    def finish(self):
        self.out(self.joing(self.parts, (1000, 0)))
        self.tidy()

    def paint(self, geo, color):
        p = self.n('GeometryNodeGroup', self.place()); p.node_tree = G("UI · Paint")
        self.L(geo, p.inputs['Geometry']); p.inputs['Color'].default_value = C(color) if isinstance(color, str) else color
        return p.outputs[0]

    def outline(self, geo, t=0.022, color=None):
        o = self.n('GeometryNodeGroup', self.place()); o.node_tree = G("UI · Outline")
        self.L(geo, o.inputs['Geometry']); o.inputs['Thickness'].default_value = t
        out = o.outputs[0]
        return self.paint(out, color) if color else out

    def mass(self, geo, color='WHITE', t=0.022):
        flat = self.n('GeometryNodeSetShadeSmooth', self.place())      # flat faces read like a drawing
        self.L(geo, flat.inputs['Geometry'])
        sm = [s for s in flat.inputs if s.name == 'Shade Smooth'][0]; sm.default_value = False
        self.add(self.paint(flat.outputs[0], color)); self.add(self.edges(geo, t, 'BLACK', 25.0))

    def edges(self, geo, t=0.012, color='MUTE', angle=20.0):
        """Tubes on the sharp and open edges only (UI · Outline also returns the mesh)."""
        ea = self.n('GeometryNodeInputMeshEdgeAngle', self.place())
        sharp = self.math('GREATER_THAN', ea.outputs['Unsigned Angle'], math.radians(angle), self.place())
        nb = self.n('GeometryNodeInputMeshEdgeNeighbors', self.place())
        open_ = self.math('LESS_THAN', nb.outputs['Face Count'], 1.5, self.place())
        sel = self.math('MAXIMUM', sharp, open_, self.place())
        mc = self.n('GeometryNodeMeshToCurve', self.place())
        self.L(geo, mc.inputs['Mesh']); self.L(sel, mc.inputs['Selection'])
        return self.tube(mc.outputs[0], t, color, 6)

    def ghost(self, geo, color='MUTE', t=0.014):
        self.add(self.edges(geo, t, color))

    def tube(self, curve, r=0.03, color='PINK', res=8):
        c = self.n('GeometryNodeCurvePrimitiveCircle', self.place()); c.inputs['Radius'].default_value = r
        c.inputs['Resolution'].default_value = res
        cm = self.n('GeometryNodeCurveToMesh', self.place())
        self.L(curve, cm.inputs['Curve']); self.L(c.outputs[0], cm.inputs['Profile Curve'])
        cm.inputs['Fill Caps'].default_value = True
        return self.paint(cm.outputs[0], color)

    def vec(self, v):
        if isinstance(v, tuple):
            n = self.n('FunctionNodeInputVector', self.place()); n.vector = v
            return n.outputs[0]
        return v

    def arrow(self, a, b, color='PINK', r=0.035):
        a, b = self.vec(a), self.vec(b)
        d = self.vmath('SUBTRACT', b, a, self.place())
        dn = self.vmath('NORMALIZE', d, None, self.place())
        tip = self.vmath('SCALE', dn, r * 4, self.place())
        end = self.vmath('SUBTRACT', b, tip, self.place())
        ln = self.n('GeometryNodeCurvePrimitiveLine', self.place())
        self.L(a, ln.inputs['Start']); self.L(end, ln.inputs['End'])
        self.add(self.tube(ln.outputs[0], r, color))
        cone = self.n('GeometryNodeMeshCone', self.place())
        self.set(cone, Vertices=16, Radius_Top=0.0, Radius_Bottom=r * 3.2, Depth=r * 8)
        al = self.n('FunctionNodeAlignRotationToVector', self.place(), axis='Z')
        self.L(dn, al.inputs['Vector'])
        self.add(self.paint(self.transform(cone.outputs[0], end, al.outputs[0], loc=self.place()), color))

    def text(self, string, pos, size=0.26, color='BLACK', left=False):
        """Camera-facing text. string: str or socket. pos: world tuple or socket. size in HUD units."""
        t = self.n('GeometryNodeGroup', self.place()); t.node_tree = G("UI · Text")
        if isinstance(string, str): t.inputs['String'].default_value = string
        else: self.L(string, t.inputs['String'])
        if isinstance(pos, tuple): t.inputs['Position'].default_value = pos
        else: self.L(pos, t.inputs['Position'])
        t.inputs['Size'].default_value = size * self.s
        t.inputs['Left Align'].default_value = left; t.inputs['Mono'].default_value = True
        t.inputs['Color'].default_value = C(color)
        self.add(t.outputs[0])

    def fmt(self, sock, dec=1):
        v = self.n('FunctionNodeValueToString', self.place())
        if dec == 0:
            v.data_type = 'INT'
        self.L(sock, v.inputs['Value'])
        if dec:
            v.inputs['Decimals'].default_value = dec
        return v.outputs[0]

    def vfmt(self, vsock, dec=1):
        """'(x, y, z)' from a vector socket."""
        x, y, z = self.sep(vsock, self.place())[:3]
        return self.cat(["(", self.fmt(x, dec), ", ", self.fmt(y, dec), ", ", self.fmt(z, dec), ")"])

    def cat(self, parts, delim=""):
        socks = [lit(self.nt, p, self.place()) if isinstance(p, str) else p for p in parts]
        return join(self.nt, delim, socks, self.place()).outputs[0]

    def sswitch(self, idx, strings):
        """Pick one string by an int socket."""
        s = self.iswitch('STRING', len(strings), self.place())
        self.L(idx, s.inputs['Index'])
        for i, st in enumerate(strings):
            if isinstance(st, str): s.inputs[i + 1].default_value = st
            else: self.L(st, s.inputs[i + 1])
        return s.outputs[0]

    def code(self, lines, x=-7.5, y=-0.55, size=0.29, w=6.6, h=None):
        """Code card. lines: list of (color, parts). color: 'k' black, 'p' pink, 'g' grey, or an
        int socket (0 black, 1 pink, 2 grey). parts: str, socket, or list of both."""
        pad = 0.22; lh = size * 1.02
        rows = []
        for c, parts in lines:
            if isinstance(parts, str): ls = lit(self.nt, parts, self.place())
            elif isinstance(parts, list): ls = self.cat(parts)
            else: ls = parts
            rows.append((c, ls))
        for ci, (cname, colr) in enumerate((('k', 'BLACK'), ('p', 'PINK'), ('g', 'GREY'))):
            outs = []; used = False
            for c, ls in rows:
                if isinstance(c, str):
                    if c == cname: outs.append(ls); used = True
                    else: outs.append(lit(self.nt, "", self.place()))
                else:
                    cmp = self.n('FunctionNodeCompare', self.place(), data_type='INT', operation='EQUAL')
                    ins = [s for s in cmp.inputs if getattr(s, 'enabled', True)]
                    self.L(c, ins[0]); ins[1].default_value = ci
                    sw = self.n('GeometryNodeSwitch', self.place(), input_type='STRING')
                    self.L(cmp.outputs[0], sw.inputs['Switch']); self.L(ls, sw.inputs['True'])
                    outs.append(sw.outputs[0]); used = True
            if used:
                self.text(join(self.nt, "\n", outs, self.place()).outputs[0],
                          camp(self.cam, x + pad, y - pad), size, colr, left=True)
        hh = h if h is not None else pad * 2 + len(lines) * lh + 0.05
        cd = self.n('GeometryNodeGroup', self.place()); cd.node_tree = G("UI · Card")
        m = 0.25 / self.s           # UI · Card adds a 0.25 margin around Position
        cd.inputs['Position'].default_value = camp(self.cam, x + m, y - m, 20.3)
        cd.inputs['Width'].default_value = w * self.s; cd.inputs['Height'].default_value = hh * self.s
        self.add(cd.outputs[0])

    def axes(self, length=4):
        a = self.n('GeometryNodeGroup', self.place()); a.node_tree = G("UI · Axes")
        a.inputs['Length'].default_value = length
        self.add(a.outputs[0])

    def named(self, name, dtype='BOOLEAN'):
        n = self.n('GeometryNodeInputNamedAttribute', self.place(), data_type=dtype)
        n.inputs['Name'].default_value = name
        return n.outputs['Attribute']

    def split(self, geo, sel):
        sp = self.n('GeometryNodeSeparateGeometry', self.place())
        self.L(geo, sp.inputs['Geometry']); self.L(sel, sp.inputs['Selection'])
        return sp.outputs['Selection'], sp.outputs['Inverted']


# ---------------------------------------------------------------- object, drivers, render
def lesson_object(sc, lesson, ui, drive=()):
    """Object named after the scene with GeometryNodes (lesson) + UI modifiers.
    drive: (lesson input name, ui input name[, n components]) pairs copied by drivers."""
    name = sc.name
    me = bpy.data.meshes.get(name) or bpy.data.meshes.new(name)
    ob = bpy.data.objects.get(name) or bpy.data.objects.new(name, me)
    if ob.name not in sc.collection.objects:
        sc.collection.objects.link(ob)
    for m in list(ob.modifiers):
        ob.modifiers.remove(m)
    if ob.animation_data:
        ob.animation_data_clear()
    m1 = ob.modifiers.new("GeometryNodes", 'NODES'); m1.node_group = lesson
    m2 = ob.modifiers.new("UI", 'NODES'); m2.node_group = ui
    ob.modifiers.active = m1
    SK['set_mod_defaults'](ob) if 'set_mod_defaults' in SK else SK['set_defaults'](ob)
    bpy.context.window.scene = sc
    sc.view_layers[0].update()          # menu items exist only after the tree evaluates
    for it in lesson.interface.items_tree:
        if getattr(it, 'in_out', '') == 'INPUT' and it.socket_type == 'NodeSocketMenu':
            sub = getattr(m1.properties.inputs, it.identifier)
            try:
                sub.value = sub.bl_rna.properties['value'].enum_items[0].identifier
            except Exception:
                pass
    for d in drive:
        mirror(ob, *d)
    vl = sc.view_layers[0]
    for o in sc.objects:
        o.select_set(False, view_layer=vl)
    ob.select_set(True, view_layer=vl); vl.objects.active = ob
    return ob


def ident(ob, mod, name):
    m = ob.modifiers[mod]
    return [i for i in m.node_group.interface.items_tree if getattr(i, 'name', '') == name
            and getattr(i, 'in_out', '') == 'INPUT'][0].identifier


def menu_offset(ob, src):
    """A driver on a menu input reads the item's internal value, not its position."""
    m = ob.modifiers["GeometryNodes"]
    it = [i for i in m.node_group.interface.items_tree if getattr(i, 'name', '') == src and getattr(i, 'in_out', '') == 'INPUT'][0]
    if it.socket_type != 'NodeSocketMenu':
        return None
    sub = getattr(m.properties.inputs, it.identifier)
    vals = [e.value for e in sub.bl_rna.properties['value'].enum_items]
    return min(vals) if vals else None


def mirror(ob, src, dst, n=1):
    a, b = ident(ob, "GeometryNodes", src), ident(ob, "UI", dst)
    off = menu_offset(ob, src)
    for k in range(n):
        idx = -1 if n == 1 else k
        fc = ob.driver_add(f'modifiers["UI"].properties.inputs.{b}.value', idx) if n > 1 else \
            ob.driver_add(f'modifiers["UI"].properties.inputs.{b}.value')
        d = fc.driver
        if off:
            d.type = 'SCRIPTED'; d.expression = f"var - {off}"
        else:
            d.type = 'AVERAGE'
        for v in list(d.variables):
            d.variables.remove(v)
        v = d.variables.new(); v.type = 'SINGLE_PROP'
        v.targets[0].id = ob
        v.targets[0].data_path = f'modifiers["GeometryNodes"].properties.inputs.{a}.value' + (f'[{k}]' if n > 1 else '')


def set_in(ob, name, value, mod="GeometryNodes"):
    getattr(ob.modifiers[mod].properties.inputs, ident(ob, mod, name)).value = value
    ob.update_tag()


def snap(sc, name):
    bpy.context.view_layer.update()
    for vl in sc.view_layers:
        vl.update()
    sc.render.filepath = os.path.join(folder(), name + ".png")
    sc.render.resolution_percentage = 50; sc.eevee.taa_render_samples = 8
    with bpy.context.temp_override(scene=sc):
        bpy.ops.render.render(write_still=True, scene=sc.name)
    sc.render.resolution_percentage = 100
    return sc.render.filepath


PD = dict(C=C, G=G, make_slide=make_slide, aim=aim, camp=camp, camdir=camdir, Tree=Tree, UI=UI,
          lesson_object=lesson_object, mirror=mirror, set_in=set_in, snap=snap, ISO=ISO, TOP=TOP,
          TAG=TAG, TOTAL=TOTAL, folder=folder)
bpy.app.driver_namespace['GK'] = PD
print("generative_slidekit ready")
