"""procedural_build.py: builds every slide of Introduction-to-Procedural-Design.blend.

Run blender_slidekit.py, then procedural_slidekit.py, then this file. It registers PB in
bpy.app.driver_namespace with one function per slide (PB['s05']() rebuilds slide 05).
No Python on the slides: every card is a numbered list of steps in plain words, plus where
to find the operation in Blender and Grasshopper.
"""
import bpy, math

PD = bpy.app.driver_namespace['PD']
Tree, UI = PD['Tree'], PD['UI']
ISO, TOP = PD['ISO'], PD['TOP']
RIGHT = (-0.70711, 0.70711, 0.0)        # screen right for the isometric view (z = 135)
R = math.radians


def S(n, name, out=False):
    """Socket by name, skipping unavailable ones (Random Value, Compare...)."""
    socks = n.outputs if out else n.inputs
    return next(s for s in socks if s.name == name and getattr(s, 'enabled', True))


def lnk(t, a, n, name):
    s = S(n, name)
    if isinstance(a, (int, float, bool, tuple, str)):
        s.default_value = a
    else:
        t.L(a, s)


def done(key, sc, t, u, drive, extra=None):
    ob = PD['lesson_object'](sc, t.nt if hasattr(t, 'nt') else t, u.nt, drive)
    if extra:
        extra(ob)
    bpy.context.window.scene = sc
    PD['snap'](sc, "PROC_" + key[:2])
    return ob


def tools(blender, gh):
    out = []
    for i, b in enumerate(blender if isinstance(blender, list) else [blender]):
        out.append(('g', ("Blender:  " if i == 0 else "          ") + b))
    for i, g in enumerate(gh if isinstance(gh, list) else [gh]):
        out.append(('g', ("Grasshopper:  " if i == 0 else "              ") + g))
    return out


def cint(u, sock, value, op='EQUAL'):
    c = u.n('FunctionNodeCompare', u.place(), data_type='INT', operation=op)
    ins = [s for s in c.inputs if getattr(s, 'enabled', True)]
    u.L(sock, ins[0]); ins[1].default_value = value
    return c.outputs[0]


def step_color(u, step, i):
    """0 black (done), 1 pink (this step), 2 grey (not yet)."""
    eq = cint(u, step, i, 'EQUAL'); gt = cint(u, step, i, 'GREATER_THAN')
    s1 = u.n('GeometryNodeSwitch', u.place(), input_type='INT')
    u.L(gt, s1.inputs['Switch']); s1.inputs['False'].default_value = 2; s1.inputs['True'].default_value = 0
    s2 = u.n('GeometryNodeSwitch', u.place(), input_type='INT')
    u.L(eq, s2.inputs['Switch']); u.L(s1.outputs[0], s2.inputs['False']); s2.inputs['True'].default_value = 1
    return s2.outputs[0]


def rot_z(t, deg_sock, loc):
    rad = t.math('RADIANS', deg_sock, None, loc)
    return t.euler(t.xyz(0.0, 0.0, rad, (loc[0] + 180, loc[1])), (loc[0] + 360, loc[1]))


# ================================================================ 01 Three ways
def s01():
    key = "01 Three Ways"
    sc, cam, hud = PD['make_slide'](key, 1, "THREE WAYS\nTO MAKE FORM",
        "Procedural: a fixed list of steps.\nParametric: the same steps with dials.\n"
        "Generative: a rule that repeats on its own result.",
        "Switch Mode. Parametric: change Floors and Twist. Generative: change Seed and Iterations.", scale=22)
    PD['aim'](cam, (0, 0, 2.6), ISO, shift=3.2)
    t = Tree(key)
    t.inp("Mode", "Menu", desc="Procedural, Parametric or Generative")
    t.inp("Floors", "Int", 6, 1, 14, "Parametric: floors in every tower")
    t.inp("Twist", "Float", 8.0, 0.0, 30.0, "Parametric: extra turn per floor, tower by tower (degrees)")
    t.inp("Iterations", "Int", 10, 0, 24, "Generative: how many times the rule runs")
    t.inp("Seed", "Int", 0, 0, 999, "Generative: another seed, another result")
    floor = t.box(1.6, 1.6, 0.6, (-500, 500))
    # procedural
    ml = t.n('GeometryNodeMeshLine', (-500, 300)); ml.mode = 'OFFSET'
    ml.inputs['Count'].default_value = 5; ml.inputs['Offset'].default_value = (0, 0, 0.7)
    ix = t.n('GeometryNodeInputIndex', (-700, 160))
    r1 = rot_z(t, t.math('MULTIPLY', ix.outputs[0], 10.0, (-500, 160)), (-320, 160))
    i1 = t.n('GeometryNodeInstanceOnPoints', (60, 300))
    t.L(ml.outputs[0], i1.inputs['Points']); t.L(floor.outputs[0], i1.inputs['Instance']); t.L(r1, i1.inputs['Rotation'])
    re1 = t.n('GeometryNodeRealizeInstances', (240, 300)); t.L(i1.outputs[0], re1.inputs[0])
    t.frame("01  procedural: 5 floors, each turned 10 more, numbers fixed", [ml, ix, r1.node, i1, re1])
    # parametric
    cnt = t.math('MULTIPLY', t.g("Floors"), 5, (-700, -80))
    ix2 = t.n('GeometryNodeInputIndex', (-900, -200))
    tw = t.math('FLOOR', t.math('DIVIDE', ix2.outputs[0], t.g("Floors"), (-700, -200)), None, (-520, -200))
    fl = t.math('FLOORED_MODULO', ix2.outputs[0], t.g("Floors"), (-700, -320))
    off = t.math('MULTIPLY', t.math('SUBTRACT', tw, 2.0, (-340, -200)), 2.3, (-160, -200))
    pos = t.vmath('ADD', t.vmath('SCALE', RIGHT, off, (20, -200)),
                  t.xyz(0.0, 0.0, t.math('MULTIPLY', fl, 0.7, (-340, -320)), (-160, -320)), (200, -240))
    ang = t.math('MULTIPLY', t.math('MULTIPLY', fl, tw, (-340, -440)), t.g("Twist"), (-160, -440))
    r2 = rot_z(t, ang, (20, -440))
    pts = t.n('GeometryNodePoints', (380, -120)); t.L(cnt, pts.inputs['Count']); t.L(pos, pts.inputs['Position'])
    i2 = t.n('GeometryNodeInstanceOnPoints', (560, -160))
    t.L(pts.outputs[0], i2.inputs['Points']); t.L(floor.outputs[0], i2.inputs['Instance']); t.L(r2, i2.inputs['Rotation'])
    re2 = t.n('GeometryNodeRealizeInstances', (740, -160)); t.L(i2.outputs[0], re2.inputs[0])
    t.frame("02  parametric: five towers, Floors and Twist are dials", [cnt.node, ix2, tw.node, fl.node, off.node, pos.node, ang.node, r2.node, pts, i2, re2])
    # generative
    rin = t.n('GeometryNodeRepeatInput', (-500, -760)); rout = t.n('GeometryNodeRepeatOutput', (560, -760))
    rin.pair_with_output(rout)
    rout.repeat_items.new('GEOMETRY', "All")
    t.L(t.g("Iterations"), rin.inputs['Iterations'])
    t.L(floor.outputs[0], rin.inputs['Geometry']); t.L(floor.outputs[0], rin.inputs['All'])
    rv = t.n('FunctionNodeRandomValue', (-300, -900), data_type='FLOAT')
    S(rv, 'Min').default_value = -30.0; S(rv, 'Max').default_value = 30.0
    t.L(rin.outputs['Iteration'], S(rv, 'ID')); t.L(t.g("Seed"), S(rv, 'Seed'))
    rs = t.n('FunctionNodeRandomValue', (-300, -1080), data_type='FLOAT')
    S(rs, 'Min').default_value = 0.86; S(rs, 'Max').default_value = 1.02
    t.L(rin.outputs['Iteration'], S(rs, 'ID'))
    t.L(t.math('ADD', t.g("Seed"), 7, (-480, -1100)), S(rs, 'Seed'))
    r3 = rot_z(t, S(rv, 'Value', True), (-120, -900))
    sc3 = t.xyz(S(rs, 'Value', True), S(rs, 'Value', True), 1.0, (-120, -1080))
    nxt = t.transform(rin.outputs['Geometry'], (0, 0, 0.7), r3, sc3, (260, -820))
    allj = t.joing([rin.outputs['All'], nxt], (400, -900))
    t.L(nxt, rout.inputs['Geometry']); t.L(allj, rout.inputs['All'])
    t.frame("03  generative: next floor = last floor, turned and shrunk at random", [rin, rout, rv, rs, r3.node, sc3.node, nxt.node, allj.node])
    ms = t.menu(["Procedural", "Parametric", "Generative"], 'GEOMETRY', (950, 0))
    t.L(t.g("Mode"), ms.inputs['Menu'])
    t.L(re1.outputs[0], ms.inputs['Procedural']); t.L(re2.outputs[0], ms.inputs['Parametric'])
    t.L(rout.outputs['All'], ms.inputs['Generative'])
    t.out(ms.outputs[0]); t.go.location = (1150, 0)
    t.note("01 note - three ways", "The same floor, three ways. Procedural: the numbers are written into the steps. "
           "Parametric: the steps read dials (Floors, Twist). Generative: a loop feeds each result back as the next input.",
           (-1000, 700), 640, 120)
    t.tidy()
    u = UI(key, cam)
    for n, ty, d in (("Mode", "Int", 0), ("Floors", "Int", 6), ("Twist", "Float", 8.0), ("Iterations", "Int", 10), ("Seed", "Int", 0)):
        u.inp(n, ty, d)
    u.mass(u.g("Geometry"))
    M = u.g("Mode"); tw = u.g("Twist")
    f0 = lambda k: u.fmt(u.math('MULTIPLY', tw, k, u.place()), 0)
    rows = [
        ["PROCEDURAL   fixed steps", "PARAMETRIC   steps with dials", "GENERATIVE   a rule on its own result"],
        ["1  floor: box 1.6 x 1.6 x 0.6", "1  floor: box 1.6 x 1.6 x 0.6", "1  start with one floor"],
        ["2  stack 5 floors", u.cat(["2  stack ", u.fmt(u.g("Floors"), 0), " floors"]), "2  next floor = last floor,"],
        ["3  turn each floor 10° more",
         u.cat(["3  turn per floor: 0, ", f0(1), ", ", f0(2), ", ", f0(3), ", ", f0(4), "°"]),
         "   turned and shrunk at random"],
        ["", "", u.cat(["3  repeat ", u.fmt(u.g("Iterations"), 0), " times, seed ", u.fmt(u.g("Seed"), 0)])],
        ["One list of steps, one result.", "Same steps, a family of five.", "You set the rule, then discover."],
    ]
    lines = [('p' if i == 0 else ('g' if i == 5 else 'k'), u.sswitch(M, r)) for i, r in enumerate(rows)]
    u.code(lines, y=-0.95)
    u.finish()
    return done(key, sc, t, u, [("Mode", "Mode"), ("Floors", "Floors"), ("Twist", "Twist"), ("Iterations", "Iterations"), ("Seed", "Seed")])


# ================================================================ 02 LeWitt
def s02():
    key = "02 LeWitt"
    sc, cam, hud = PD['make_slide'](key, 2, "THE INSTRUCTION\nIS THE WORK",
        "Sol LeWitt wrote his wall drawings as instructions. Other people drew them.\n\n"
        "Same instruction, another hand, another drawing. Here Seed plays the hand.",
        "Change Seed and Count. Set Step to 1, then 2. Switch Connect to All.", scale=17)
    PD['aim'](cam, (0, 0, 0), TOP, shift=3.6)
    t = Tree(key)
    t.inp("Count", "Int", 20, 2, 60, "How many points")
    t.inp("Seed", "Int", 0, 0, 999, "Who draws it: another seed, another drawing")
    t.inp("Connect", "Menu", desc="Nearest neighbour, or every other point")
    t.inp("Step", "Int", 2, 1, 2, "How much of the instruction is done")
    rv = t.n('FunctionNodeRandomValue', (-600, 300), data_type='FLOAT_VECTOR')
    S(rv, 'Min').default_value = (-3.6, -2.4, 0); S(rv, 'Max').default_value = (3.6, 2.4, 0)
    t.L(t.g("Seed"), S(rv, 'Seed'))
    pts = t.n('GeometryNodePoints', (-380, 300)); t.L(t.g("Count"), pts.inputs['Count'])
    t.L(S(rv, 'Value', True), pts.inputs['Position']); pts.inputs['Radius'].default_value = 0.05
    t.frame("01  place Count points at random on the sheet (7.2 x 4.8)", [rv, pts])
    nn = t.n('GeometryNodeIndexOfNearest', (-600, 0))

    def ends(count_sock, y):
        e = t.n('GeometryNodePoints', (260, y)); t.L(count_sock, e.inputs['Count'])
        ix = t.n('GeometryNodeInputIndex', (-600, y - 120))
        k = t.math('FLOOR', t.math('DIVIDE', ix.outputs[0], 2.0, (-420, y - 120)), None, (-260, y - 120))
        en = t.math('FLOORED_MODULO', ix.outputs[0], 2.0, (-420, y - 240))
        return e, ix, k, en

    def line_from(e, k, a, b, y, extra=()):
        sw = t.n('GeometryNodeSwitch', (-80, y - 200), input_type='INT')
        t.L(t.math('GREATER_THAN', a[1], 0.5, (-260, y - 240)), sw.inputs['Switch'])
        t.L(a[0], sw.inputs['False']); t.L(b, sw.inputs['True'])
        sp = t.n('GeometryNodeSampleIndex', (80, y - 160), data_type='FLOAT_VECTOR', domain='POINT')
        p = t.n('GeometryNodeInputPosition', (-80, y - 340))
        t.L(pts.outputs[0], sp.inputs['Geometry']); t.L(p.outputs[0], sp.inputs['Value']); t.L(sw.outputs[0], sp.inputs['Index'])
        t.L(sp.outputs[0], e.inputs['Position'])
        return [sw, sp, p, a[1].node]

    # nearest
    e1, ix1, k1, en1 = ends(t.math('MULTIPLY', t.g("Count"), 2, (80, -20)), -20)
    si = t.n('GeometryNodeSampleIndex', (-260, -100), data_type='INT', domain='POINT')
    t.L(pts.outputs[0], si.inputs['Geometry']); t.L(nn.outputs['Index'], si.inputs['Value']); t.L(k1, si.inputs['Index'])
    extra1 = line_from(e1, k1, (k1, en1), si.outputs[0], -20)
    pc1 = t.n('GeometryNodePointsToCurves', (440, -20)); t.L(e1.outputs[0], pc1.inputs['Points']); t.L(k1, pc1.inputs['Curve Group ID'])
    t.frame("02  connect each point to its nearest neighbour: one line per point", [nn, e1, ix1, k1.node, en1.node, si, pc1] + extra1)
    # all
    cc = t.math('MULTIPLY', t.math('MULTIPLY', t.g("Count"), t.g("Count"), (-80, -560)), 2, (80, -560))
    e2, ix2, k2, en2 = ends(cc, -560)
    a = t.math('FLOOR', t.math('DIVIDE', k2, t.g("Count"), (-80, -700)), None, (80, -700))
    b = t.math('FLOORED_MODULO', k2, t.g("Count"), (-80, -820))
    extra2 = line_from(e2, k2, (a, en2), b, -560)
    dl = t.n('GeometryNodeDeleteGeometry', (440, -560), domain='POINT'); t.L(e2.outputs[0], dl.inputs['Geometry'])
    t.L(t.math('GREATER_THAN', t.math('ADD', a, 0.5, (260, -700)), b, (260, -820)), dl.inputs['Selection'])
    pc2 = t.n('GeometryNodePointsToCurves', (620, -560)); t.L(dl.outputs[0], pc2.inputs['Points']); t.L(k2, pc2.inputs['Curve Group ID'])
    t.frame("02  or connect every point to every other point (each pair once)", [cc.node, e2, ix2, k2.node, en2.node, a.node, b.node, dl, pc2] + extra2)
    ms = t.menu(["Nearest", "All"], 'GEOMETRY', (820, -200)); t.L(t.g("Connect"), ms.inputs['Menu'])
    t.L(pc1.outputs[0], ms.inputs['Nearest']); t.L(pc2.outputs[0], ms.inputs['All'])
    sw = t.n('GeometryNodeSwitch', (1000, 100), input_type='GEOMETRY')
    t.L(t.math('GREATER_THAN', t.g("Step"), 1.5, (820, 160)), sw.inputs['Switch'])
    t.L(pts.outputs[0], sw.inputs['False']); t.L(t.joing([pts.outputs[0], ms.outputs[0]], (820, 40)), sw.inputs['True'])
    t.out(sw.outputs[0]); t.go.location = (1180, 100)
    t.note("02 note - instruction", "Read the frames as the two lines of the instruction. Seed changes where the points land, "
           "the instruction stays the same.", (-900, 560), 560, 100)
    t.tidy()
    u = UI(key, cam)
    for n, ty, d in (("Count", "Int", 20), ("Seed", "Int", 0), ("Connect", "Int", 0), ("Step", "Int", 2)):
        u.inp(n, ty, d)
    g = u.g("Geometry")
    sh = u.n('GeometryNodeMeshGrid', u.place()); u.set(sh, Size_X=7.9, Size_Y=5.3)
    shg = u.transform(sh.outputs[0], (0, 0, -0.02), loc=u.place())
    u.add(u.paint(shg, 'WHITE')); u.add(u.outline(shg, 0.02))
    sc_ = u.n('GeometryNodeSeparateComponents', u.place()); u.L(g, sc_.inputs[0])
    dot = u.n('GeometryNodeMeshCircle', u.place(), fill_type='NGON'); u.set(dot, Vertices=16, Radius=0.075)
    io = u.n('GeometryNodeInstanceOnPoints', u.place()); u.L(sc_.outputs['Point Cloud'], io.inputs['Points']); u.L(dot.outputs[0], io.inputs['Instance'])
    rz = u.n('GeometryNodeRealizeInstances', u.place()); u.L(io.outputs[0], rz.inputs[0])
    u.add(u.paint(rz.outputs[0], 'BLACK'))
    u.add(u.tube(sc_.outputs['Curve'], 0.012, 'BLACK', 6))
    st = u.g("Step"); cn = u.g("Connect")
    s1 = cint(u, st, 1)
    col1 = u.n('GeometryNodeSwitch', u.place(), input_type='INT'); u.L(s1, col1.inputs['Switch'])
    col1.inputs['False'].default_value = 0; col1.inputs['True'].default_value = 1
    s2 = cint(u, st, 2)
    col2 = u.n('GeometryNodeSwitch', u.place(), input_type='INT'); u.L(s2, col2.inputs['Switch'])
    col2.inputs['False'].default_value = 2; col2.inputs['True'].default_value = 1
    lines = [('k', "INSTRUCTION"),
             (col1.outputs[0], u.cat(["1  Place ", u.fmt(u.g("Count"), 0), " points at random"])),
             (col1.outputs[0], "   on the sheet."),
             (col2.outputs[0], u.sswitch(cn, ["2  Connect each point to its", "2  Connect every point to"])),
             (col2.outputs[0], u.sswitch(cn, ["   nearest neighbour.", "   every other point."])),
             ('g', "after Sol LeWitt's wall drawings")]
    u.code(lines, y=-0.8)
    u.finish()
    return done(key, sc, t, u, [("Count", "Count"), ("Seed", "Seed"), ("Connect", "Connect"), ("Step", "Step")])


# ================================================================ 03 Parameter
def s03():
    key = "03 Parameter"
    sc, cam, hud = PD['make_slide'](key, 3, "A PARAMETER",
        "A parameter is a named input of a step. Width, depth and height are the parameters of a box.\n\n"
        "The step stays the same. Change a number and the result follows.",
        "Change Width, Depth and Height. Set Height to 0: which primitive do you get?", scale=15)
    PD['aim'](cam, (0, 0, 2.0), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Width", "Float", 3.0, 0.0, 12.0, "Size along x"); t.inp("Depth", "Float", 2.0, 0.0, 12.0, "Size along y")
    t.inp("Height", "Float", 4.0, 0.0, 12.0, "Size along z")
    size = t.xyz(t.g("Width"), t.g("Depth"), t.g("Height"), (-600, 100))
    cube = t.n('GeometryNodeMeshCube', (-380, 100)); t.L(size, cube.inputs['Size'])
    half = t.math('MULTIPLY', t.g("Height"), 0.5, (-600, -120)); up = t.xyz(0.0, 0.0, half, (-380, -120))
    tr = t.n('GeometryNodeTransform', (-120, 60)); t.L(cube.outputs[0], tr.inputs['Geometry']); t.L(up, tr.inputs['Translation'])
    t.out(tr.outputs[0]); t.go.location = (140, 60)
    t.frame("01  three parameters set the size", [size.node, cube])
    t.frame("02  stand it on the ground", [half.node, up.node, tr])
    t.note("03 note - parameter", "Width, Depth and Height are exposed in the modifier panel: they are the parameters. "
           "The nodes never change, only the numbers that flow into them.", (-900, -330), 520, 110)
    t.tidy()
    u = UI(key, cam)
    for n, d in (("Width", 3.0), ("Depth", 2.0), ("Height", 4.0)):
        u.inp(n, "Float", d)
    W, D, H = u.g("Width"), u.g("Depth"), u.g("Height")
    u.mass(u.g("Geometry"))
    hw = u.math('MULTIPLY', W, 0.5, u.place()); hd = u.math('MULTIPLY', D, 0.5, u.place()); hh = u.math('MULTIPLY', H, 0.5, u.place())
    u.text(u.cat(["width ", u.fmt(W)]), u.xyz(0.0, u.math('ADD', hd, 0.55, u.place()), 0.0, u.place()), 0.26, 'PINK')
    u.text(u.cat(["depth ", u.fmt(D)]), u.xyz(u.math('ADD', hw, 0.55, u.place()), 0.0, 0.0, u.place()), 0.26, 'PINK')
    corner = u.xyz(u.math('MULTIPLY', hw, -1.0, u.place()), hd, hh, u.place())
    u.text(u.cat(["height ", u.fmt(H)]), u.vmath('ADD', corner, (-0.3, 0.3, 0.0), u.place()), 0.26, 'PINK', left=True)
    lines = [('k', "BOX"), ('p', ["width    ", u.fmt(W)]), ('p', ["depth    ", u.fmt(D)]), ('p', ["height   ", u.fmt(H)]),
             ('k', "")] + tools(["Shift A > Cube, then", "N panel > Dimensions"], "Box")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Width", "Width"), ("Depth", "Depth"), ("Height", "Height")])


# ================================================================ 04 Primitives
def s04():
    key = "04 Primitives"
    sc, cam, hud = PD['make_slide'](key, 4, "PRIMITIVES",
        "Most 3D software starts from the same few solids: box, cylinder, cone, sphere and plane.\n\n"
        "Each one has its own parameters. Complex forms are primitives plus operations.",
        "Switch Primitive. Pick Cone and set Sides to 4: a pyramid. Cylinder with 3 sides: a prism.", scale=13)
    PD['aim'](cam, (0, 0, 1.0), ISO, shift=2.7)
    t = Tree(key)
    t.inp("Primitive", "Menu", desc="Which primitive")
    t.inp("Width", "Float", 2.0, 0.1, 6.0, "Width (or diameter)"); t.inp("Depth", "Float", 2.0, 0.1, 6.0, "Depth")
    t.inp("Height", "Float", 2.0, 0.0, 6.0, "Height"); t.inp("Sides", "Int", 24, 3, 64, "Sides of round primitives")
    rad = t.math('MULTIPLY', t.g("Width"), 0.5, (-600, -100))
    up = t.xyz(0.0, 0.0, t.math('MULTIPLY', t.g("Height"), 0.5, (-600, -220)), (-420, -220))
    bx = t.box(t.g("Width"), t.g("Depth"), t.g("Height"), (-200, 400))
    cy = t.n('GeometryNodeMeshCylinder', (-200, 220)); t.L(t.g("Sides"), cy.inputs['Vertices']); t.L(rad, cy.inputs['Radius']); t.L(t.g("Height"), cy.inputs['Depth'])
    cyt = t.transform(cy.outputs[0], up, loc=(20, 220))
    co = t.n('GeometryNodeMeshCone', (-200, 20)); t.L(t.g("Sides"), co.inputs['Vertices']); t.L(rad, co.inputs['Radius Bottom']); t.L(t.g("Height"), co.inputs['Depth'])
    co.inputs['Radius Top'].default_value = 0.0
    cot = t.transform(co.outputs[0], up, loc=(20, 20))
    sp = t.n('GeometryNodeMeshUVSphere', (-200, -200)); t.L(t.g("Sides"), sp.inputs['Segments'])
    t.L(t.math('MAXIMUM', t.math('DIVIDE', t.g("Sides"), 2, (-600, -340)), 3, (-420, -340)), sp.inputs['Rings']); t.L(rad, sp.inputs['Radius'])
    spt = t.transform(sp.outputs[0], t.xyz(0.0, 0.0, rad, (-420, -460)), loc=(20, -200))
    pl = t.n('GeometryNodeMeshGrid', (-200, -420)); t.L(t.g("Width"), pl.inputs['Size X']); t.L(t.g("Depth"), pl.inputs['Size Y'])
    ms = t.menu(["Box", "Cylinder", "Cone", "Sphere", "Plane"], 'GEOMETRY', (300, 0)); t.L(t.g("Primitive"), ms.inputs['Menu'])
    for nm, s in (("Box", bx.outputs[0]), ("Cylinder", cyt), ("Cone", cot), ("Sphere", spt), ("Plane", pl.outputs[0])):
        t.L(s, ms.inputs[nm])
    t.out(ms.outputs[0]); t.go.location = (500, 0)
    t.frame("five primitives, each with its own parameters", [bx, cy, cyt.node, co, cot.node, sp, spt.node, pl])
    t.note("04 note - primitives", "Round primitives use Width as the diameter and Sides as the number of segments. "
           "A pyramid is a cone with 4 sides.", (-900, 560), 520, 100)
    t.tidy()
    u = UI(key, cam)
    for n, ty, d in (("Primitive", "Int", 0), ("Width", "Float", 2.0), ("Depth", "Float", 2.0), ("Height", "Float", 2.0), ("Sides", "Int", 24)):
        u.inp(n, ty, d)
    P_, W, D, H, N = (u.g(n) for n in ("Primitive", "Width", "Depth", "Height", "Sides"))
    u.mass(u.g("Geometry"))
    r_ = u.fmt(u.math('MULTIPLY', W, 0.5, u.place())); w_ = u.fmt(W); d_ = u.fmt(D); h_ = u.fmt(H); n_ = u.fmt(N, 0)
    c = lambda a, b: u.cat([a, b])
    rows = [[c("width    ", w_), c("radius   ", r_), c("radius   ", r_), c("radius   ", r_), c("width    ", w_)],
            [c("depth    ", d_), c("height   ", h_), c("height   ", h_), c("sides    ", n_), c("depth    ", d_)],
            [c("height   ", h_), c("sides    ", n_), c("sides    ", n_), "", ""]]
    lines = [('k', u.cat(["PRIMITIVE  ", u.sswitch(P_, ["box", "cylinder", "cone", "sphere", "plane"])]))]
    lines += [('p', u.sswitch(P_, r)) for r in rows]
    lines += [('k', "")] + tools("Shift A > Mesh", ["Box, Cylinder, Cone, Sphere,", "Plane Surface"])
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Primitive", "Primitive"), ("Width", "Width"), ("Depth", "Depth"), ("Height", "Height"), ("Sides", "Sides")])


# ================================================================ 05 Translate
def s05():
    key = "05 Translate"
    sc, cam, hud = PD['make_slide'](key, 5, "TRANSLATE",
        "Translate (move) adds the same offset to every point: x, y and z. The shape stays the same.\n\n"
        "Start every shape at the origin and move it from there: the move is the whole story.",
        "Change Move. Try a negative x, then lift the box with z.", scale=15)
    PD['aim'](cam, (1.2, 0.6, 1.6), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Move", "Vector", (3.0, 1.0, 0.0), -6.0, 6.0, "Offset along x, y and z", 'TRANSLATION')
    bx = t.box(2.0, 2.0, 3.0, (-500, 0))
    tr = t.n('GeometryNodeTransform', (-200, 0)); t.L(bx.outputs[0], tr.inputs['Geometry']); t.L(t.g("Move"), tr.inputs['Translation'])
    t.out(tr.outputs[0]); t.go.location = (40, 0)
    t.frame("01  box 2 x 2 x 3", [bx]); t.frame("02  move it", [tr])
    t.note("05 note - translate", "Translation only: Rotation and Scale stay at their defaults.", (-700, -260), 420, 90)
    t.tidy()
    u = UI(key, cam)
    u.inp("Move", "Vector", (3.0, 1.0, 0.0))
    mv = u.g("Move")
    u.axes(4)
    u.ghost(u.box(2.0, 2.0, 3.0, u.place()).outputs[0])
    u.mass(u.g("Geometry"))
    u.arrow((0, 0, 3.3), u.vmath('ADD', mv, (0, 0, 3.3), u.place()))
    x, y, z = u.sep(mv, u.place())[:3]
    lines = [('k', "1  box 2 x 2 x 3"), ('p', ["2  move  x ", u.fmt(x), "  y ", u.fmt(y), "  z ", u.fmt(z)]),
             ('k', "")] + tools("G, then X, Y or Z and a number", "Move")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Move", "Move", 3)])


# ================================================================ 06 Rotate
EUL = {"X": (90.0, 0.0, 90.0), "Y": (0.0, -90.0, -90.0), "Z": (0.0, 0.0, 0.0)}


def s06():
    key = "06 Rotate"
    sc, cam, hud = PD['make_slide'](key, 6, "ROTATE",
        "Rotate turns every point around an axis by an angle.\n\n"
        "The axis passes through a pivot, here the origin. Same angle, another axis, another result.",
        "Change Angle, then switch Axis between X, Y and Z.", scale=14)
    PD['aim'](cam, (0, 0, 1.0), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Axis", "Menu", desc="Axis of the rotation")
    t.inp("Angle", "Float", 30.0, -180.0, 180.0, "Angle in degrees")
    bx = t.box(3.0, 1.2, 2.0, (-700, 200))
    a = t.math('RADIANS', t.g("Angle"), None, (-700, -100))
    ms = t.menu(["X", "Y", "Z"], 'VECTOR', (-300, -100)); t.L(t.g("Axis"), ms.inputs['Menu'])
    for k, nm in enumerate("XYZ"):
        v = t.xyz(*[a if j == k else 0.0 for j in range(3)], loc=(-500, -40 - 140 * k))
        t.L(v, ms.inputs[nm])
    rot = t.euler(ms.outputs[0], (-100, -100))
    tr = t.n('GeometryNodeTransform', (120, 100)); t.L(bx.outputs[0], tr.inputs['Geometry']); t.L(rot, tr.inputs['Rotation'])
    t.out(tr.outputs[0]); t.go.location = (340, 100)
    t.frame("01  box 3 x 1.2 x 2", [bx]); t.frame("02  rotate it: axis and angle", [a.node, ms, rot.node, tr] + [n for n in t.nt.nodes if n.bl_idname == 'ShaderNodeCombineXYZ'])
    t.tidy()
    u = UI(key, cam)
    u.inp("Axis", "Int", 2); u.inp("Angle", "Float", 30.0)
    ax, an = u.g("Axis"), u.g("Angle")
    u.axes(3)
    u.ghost(u.box(3.0, 1.2, 2.0, u.place()).outputs[0])
    u.mass(u.g("Geometry"))
    arc = u.n('GeometryNodeCurveArc', u.place(), mode='RADIUS'); u.set(arc, Resolution=48, Radius=2.3)
    S(arc, 'Start Angle').default_value = 0.0; u.L(u.math('RADIANS', an, None, u.place()), S(arc, 'Sweep Angle'))
    eul = u.iswitch('VECTOR', 3, u.place()); u.L(ax, eul.inputs['Index'])
    for k, nm in enumerate("XYZ"):
        eul.inputs[k + 1].default_value = [math.radians(v) for v in EUL[nm]]
    tube = u.tube(arc.outputs[0], 0.035, 'PINK')
    u.add(u.transform(tube, None, u.euler(eul.outputs[0], u.place()), loc=u.place()))
    axv = u.iswitch('VECTOR', 3, u.place()); u.L(ax, axv.inputs['Index'])
    for k in range(3):
        axv.inputs[k + 1].default_value = tuple(1.0 if j == k else 0.0 for j in range(3))
    ln = u.n('GeometryNodeCurvePrimitiveLine', u.place())
    u.L(u.vmath('SCALE', axv.outputs[0], -1.5, u.place()), ln.inputs['Start']); u.L(u.vmath('SCALE', axv.outputs[0], 3.2, u.place()), ln.inputs['End'])
    u.add(u.tube(ln.outputs[0], 0.02, 'PINK'))
    name = u.sswitch(ax, ["x", "y", "z"])
    u.text(u.cat([u.fmt(an, 0), "° around ", name]), u.vmath('ADD', u.vmath('SCALE', axv.outputs[0], 3.4, u.place()), (-0.5, 0.5, 0.0), u.place()), 0.26, 'PINK', left=True)
    lines = [('k', "1  box 3 x 1.2 x 2"), ('p', ["2  rotate ", u.fmt(an, 0), "° around ", name]), ('k', "   pivot: the origin"),
             ('k', "")] + tools("R, then X, Y or Z and an angle", "Rotate Axis")
    u.code(lines)
    u.finish()

    def extra(ob):
        PD['set_in'](ob, "Axis", "Z")
    return done(key, sc, t, u, [("Axis", "Axis"), ("Angle", "Angle")], extra)


# ================================================================ 07 Scale
def s07():
    key = "07 Scale"
    sc, cam, hud = PD['make_slide'](key, 7, "SCALE",
        "Scale multiplies every size: 1 keeps it, 2 doubles it, 0.5 halves it.\n\n"
        "The same factor on x, y and z keeps the proportions. Scale works from the pivot, here the middle of the base.",
        "Set all three to 2, then only z. Try 0 on one axis: the box goes flat.", scale=15)
    PD['aim'](cam, (0, 0, 1.8), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Scale", "Vector", (1.5, 1.0, 0.5), 0.0, 4.0, "Factor along x, y and z", 'XYZ')
    bx = t.box(2.0, 2.0, 3.0, (-500, 0))
    tr = t.n('GeometryNodeTransform', (-200, 0)); t.L(bx.outputs[0], tr.inputs['Geometry']); t.L(t.g("Scale"), tr.inputs['Scale'])
    t.out(tr.outputs[0]); t.go.location = (40, 0)
    t.frame("01  box 2 x 2 x 3", [bx]); t.frame("02  scale it", [tr])
    t.tidy()
    u = UI(key, cam)
    u.inp("Scale", "Vector", (1.5, 1.0, 0.5))
    x, y, z = u.sep(u.g("Scale"), u.place())[:3]
    u.axes(3)
    u.ghost(u.box(2.0, 2.0, 3.0, u.place()).outputs[0])
    u.mass(u.g("Geometry"))
    m = lambda s, k: u.fmt(u.math('MULTIPLY', s, k, u.place()))
    lines = [('k', "1  box 2 x 2 x 3"), ('p', ["2  scale  x ", u.fmt(x), "  y ", u.fmt(y), "  z ", u.fmt(z)]),
             ('k', ["   now ", m(x, 2), " x ", m(y, 2), " x ", m(z, 3)]),
             ('k', "")] + tools("S, then X, Y or Z and a factor", "Scale, Scale NU")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Scale", "Scale", 3)])


# ================================================================ 08 Order
def s08():
    key = "08 Order"
    sc, cam, hud = PD['make_slide'](key, 8, "ORDER MATTERS",
        "A procedure is an ordered list. Rotate, then move: the box turns in place, then moves. "
        "Move, then rotate: it swings around the origin.\n\nSame steps, another order, another result.",
        "Switch Order and watch the box jump. Change Angle in both orders.", scale=17)
    PD['aim'](cam, (1.5, 0.6, 1.2), ISO, shift=3.0)
    t = Tree(key)
    t.inp("Order", "Menu", desc="Which step comes first")
    t.inp("Move X", "Float", 3.0, -6.0, 6.0, "Move along x"); t.inp("Angle", "Float", 45.0, -180.0, 180.0, "Turn around z (degrees)")
    bx = t.box(2.0, 1.0, 1.5, (-800, 0))
    mv = t.xyz(t.g("Move X"), 0.0, 0.0, (-800, -200)); rt = rot_z(t, t.g("Angle"), (-1000, -360))
    a1 = t.transform(bx.outputs[0], None, rt, loc=(-300, 200)); a2 = t.transform(a1, mv, loc=(-100, 200))
    b1 = t.transform(bx.outputs[0], mv, loc=(-300, -200)); b2 = t.transform(b1, None, rt, loc=(-100, -200))
    ms = t.menu(["Rotate, then move", "Move, then rotate"], 'GEOMETRY', (150, 0)); t.L(t.g("Order"), ms.inputs['Menu'])
    t.L(a2, ms.inputs[1]); t.L(b2, ms.inputs[2])
    t.out(ms.outputs[0]); t.go.location = (380, 0)
    t.frame("rotate, then move", [a1.node, a2.node]); t.frame("move, then rotate", [b1.node, b2.node])
    t.tidy()
    u = UI(key, cam)
    u.inp("Order", "Int", 0); u.inp("Move X", "Float", 3.0); u.inp("Angle", "Float", 45.0)
    o, mx, an = u.g("Order"), u.g("Move X"), u.g("Angle")
    u.axes(3)
    gb = u.box(2.0, 1.0, 1.5, u.place()).outputs[0]
    u.ghost(gb)
    rr = u.euler(u.xyz(0.0, 0.0, u.math('RADIANS', an, None, u.place()), u.place()), u.place())
    mvv = u.xyz(mx, 0.0, 0.0, u.place())
    oa = u.transform(u.transform(gb, None, rr, loc=u.place()), mvv, loc=u.place())
    ob_ = u.transform(u.transform(gb, mvv, loc=u.place()), None, rr, loc=u.place())
    oth = u.n('GeometryNodeSwitch', u.place(), input_type='GEOMETRY'); u.L(cint(u, o, 1), oth.inputs['Switch'])
    u.L(ob_, oth.inputs['False']); u.L(oa, oth.inputs['True'])
    u.ghost(oth.outputs[0], 'LINE', 0.01)
    u.mass(u.g("Geometry"))
    is1 = cint(u, o, 1)
    rsw = u.n('GeometryNodeSwitch', u.place(), input_type='FLOAT'); u.L(is1, rsw.inputs['Switch'])
    rsw.inputs['False'].default_value = 1.6; u.L(mx, rsw.inputs['True'])
    csw = u.n('GeometryNodeSwitch', u.place(), input_type='VECTOR'); u.L(is1, csw.inputs['Switch'])
    u.L(mvv, csw.inputs['False']); csw.inputs['True'].default_value = (0, 0, 0)
    arc = u.n('GeometryNodeCurveArc', u.place(), mode='RADIUS'); arc.inputs['Resolution'].default_value = 48
    u.L(rsw.outputs[0], S(arc, 'Radius')); u.L(u.math('RADIANS', an, None, u.place()), S(arc, 'Sweep Angle'))
    u.add(u.transform(u.tube(arc.outputs[0], 0.035, 'PINK'), u.vmath('ADD', csw.outputs[0], (0, 0, 0.03), u.place()), loc=u.place()))
    a_ = u.fmt(an, 0); m_ = u.fmt(mx)
    lines = [('p', u.sswitch(o, [u.cat(["1  rotate ", a_, "°"]), u.cat(["1  move  x ", m_])])),
             ('p', u.sswitch(o, [u.cat(["2  move  x ", m_]), u.cat(["2  rotate ", a_, "°, around the origin"])])),
             ('k', "")] + tools("drag a modifier up or down", "swap two components")
    u.code(lines, y=-0.85)
    u.finish()
    return done(key, sc, t, u, [("Order", "Order"), ("Move X", "Move X"), ("Angle", "Angle")])


# ================================================================ 09 Boolean
def s09():
    key = "09 Boolean"
    sc, cam, hud = PD['make_slide'](key, 9, "BOOLEAN OPERATIONS",
        "A Boolean operation combines two solids. Union joins them, difference cuts B out of A, "
        "intersection keeps only the overlap.\n\nNot a Boolean value (true or false): same name, another idea.",
        "Switch Operation. In Difference, turn on Swap: A minus B is not B minus A.", scale=13)
    PD['aim'](cam, (0, 0, 1.0), ISO, shift=2.7)
    t = Tree(key)
    t.inp("Operation", "Menu", desc="Difference, Union or Intersection")
    t.inp("Cutter Move", "Vector", (0.8, 0.7, 0.0), -3.0, 3.0, "Where the cylinder B stands", 'TRANSLATION')
    t.inp("Cutter Radius", "Float", 0.9, 0.1, 2.0, "Radius of the cylinder B")
    t.inp("Swap", "Bool", False, desc="Difference only: B minus A instead of A minus B")
    A = t.box(3.0, 2.0, 2.0, (-700, 200))
    cy = t.n('GeometryNodeMeshCylinder', (-900, -100)); cy.inputs['Vertices'].default_value = 40
    t.L(t.g("Cutter Radius"), cy.inputs['Radius']); cy.inputs['Depth'].default_value = 3.0
    B = t.transform(cy.outputs[0], t.vmath('ADD', t.g("Cutter Move"), (0, 0, 1.4), (-900, -300)), loc=(-700, -100))
    nodes = []
    bd = t.n('GeometryNodeMeshBoolean', (-300, 260)); bd.operation = 'DIFFERENCE'; t.L(A.outputs[0], bd.inputs['Mesh 1']); t.L(B, bd.inputs['Mesh 2'])
    bd2 = t.n('GeometryNodeMeshBoolean', (-300, 460)); bd2.operation = 'DIFFERENCE'; t.L(B, bd2.inputs['Mesh 1']); t.L(A.outputs[0], bd2.inputs['Mesh 2'])
    swd = t.n('GeometryNodeSwitch', (-100, 360), input_type='GEOMETRY'); t.L(t.g("Swap"), swd.inputs['Switch'])
    t.L(bd.outputs[0], swd.inputs['False']); t.L(bd2.outputs[0], swd.inputs['True'])
    bu = t.n('GeometryNodeMeshBoolean', (-300, 0)); bu.operation = 'UNION'; t.L(B, bu.inputs['Mesh 2']); t.L(A.outputs[0], bu.inputs['Mesh 2'])
    bi = t.n('GeometryNodeMeshBoolean', (-300, -260)); bi.operation = 'INTERSECT'; t.L(B, bi.inputs['Mesh 2']); t.L(A.outputs[0], bi.inputs['Mesh 2'])
    ms = t.menu(["Difference", "Union", "Intersection"], 'GEOMETRY', (0, 0)); t.L(t.g("Operation"), ms.inputs['Menu'])
    for nm, b in (("Difference", swd), ("Union", bu), ("Intersection", bi)):
        t.L(b.outputs[0], ms.inputs[nm])
    t.out(ms.outputs[0]); t.go.location = (220, 0)
    t.frame("A  box 3 x 2 x 2", [A]); t.frame("B  cylinder", [cy, B.node])
    t.frame("three Boolean operations on the same A and B (difference both ways)", [bd, bd2, swd, bu, bi])
    t.tidy()
    u = UI(key, cam)
    u.inp("Operation", "Int", 0); u.inp("Cutter Move", "Vector", (0.8, 0.7, 0.0)); u.inp("Cutter Radius", "Float", 0.9); u.inp("Swap", "Bool", False)
    op, cm, cr = u.g("Operation"), u.g("Cutter Move"), u.g("Cutter Radius")
    gA = u.box(3.0, 2.0, 2.0, u.place()).outputs[0]
    gc = u.n('GeometryNodeMeshCylinder', u.place()); gc.inputs['Vertices'].default_value = 40; u.L(cr, gc.inputs['Radius']); gc.inputs['Depth'].default_value = 3.0
    gB = u.transform(gc.outputs[0], u.vmath('ADD', cm, (0, 0, 1.4), u.place()), loc=u.place())
    u.mass(u.g("Geometry"))
    u.ghost(gA, 'MUTE', 0.012); u.ghost(gB, 'PINK', 0.012)
    u.text("A", (1.7, -1.3, 0.5), 0.34, 'BLACK')
    u.text("B", u.vmath('ADD', cm, (0, 0, 3.25), u.place()), 0.34, 'PINK')
    lines = [('k', "A  box 3 x 2 x 2"), ('k', ["B  cylinder, radius ", u.fmt(cr)]),
             ('p', u.sswitch(op, [u.sswitch(u.g("Swap"), ["difference: A minus B", "difference: B minus A"]), "union: A plus B", "intersection: what A and B share"])),
             ('k', "")] + tools("Boolean modifier", ["Solid Difference, Solid Union,", "Solid Intersection"])
    u.code(lines, y=-0.85)
    u.finish()
    return done(key, sc, t, u, [("Operation", "Operation"), ("Cutter Move", "Cutter Move", 3), ("Cutter Radius", "Cutter Radius"), ("Swap", "Swap")])


# ================================================================ 10 Extrude
def footprints(t, W, D, x, y):
    q = t.n('GeometryNodeCurvePrimitiveQuadrilateral', (x, y), mode='RECTANGLE'); t.L(W, q.inputs['Width']); t.L(D, q.inputs['Height'])
    r = t.math('MULTIPLY', W, 0.5, (x - 200, y - 200))
    c = t.n('GeometryNodeCurvePrimitiveCircle', (x, y - 160), mode='RADIUS'); c.inputs['Resolution'].default_value = 40; t.L(r, c.inputs['Radius'])
    h = t.n('GeometryNodeCurvePrimitiveCircle', (x, y - 320), mode='RADIUS'); h.inputs['Resolution'].default_value = 6; t.L(r, h.inputs['Radius'])
    s = t.n('GeometryNodeCurveStar', (x, y - 480)); s.inputs['Points'].default_value = 5; t.L(r, s.inputs['Outer Radius'])
    t.L(t.math('MULTIPLY', W, 0.22, (x - 200, y - 520)), s.inputs['Inner Radius'])
    return [q.outputs[0], c.outputs['Curve'], h.outputs['Curve'], s.outputs['Curve']], [q, r.node, c, h, s]


def s10():
    key = "10 Extrude"
    sc, cam, hud = PD['make_slide'](key, 10, "EXTRUDE",
        "Extrude pushes a flat shape along a direction and turns it into a volume. Plan in, mass out.\n\n"
        "A box is an extruded rectangle, a cylinder an extruded circle.",
        "Switch Footprint, then change Width, Depth and Height.", scale=14)
    PD['aim'](cam, (0, 0, 1.2), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Footprint", "Menu", desc="The plan to extrude")
    t.inp("Width", "Float", 3.0, 0.2, 6.0, "Width (or diameter)"); t.inp("Depth", "Float", 2.0, 0.2, 6.0, "Depth (rectangle)")
    t.inp("Height", "Float", 2.0, 0.0, 6.0, "How far to extrude")
    outs, nodes = footprints(t, t.g("Width"), t.g("Depth"), -500, 300)
    ms = t.menu(["Rectangle", "Circle", "Hexagon", "Star"], 'GEOMETRY', (-250, 100)); t.L(t.g("Footprint"), ms.inputs['Menu'])
    for nm, s in zip(["Rectangle", "Circle", "Hexagon", "Star"], outs):
        t.L(s, ms.inputs[nm])
    fc0 = t.n('GeometryNodeFillCurve', (-60, 100)); t.L(ms.outputs[0], fc0.inputs['Curve'])
    up = t.n('FunctionNodeInputVector', (-60, -80)); up.vector = (0, 0, 1)
    try:
        fc0.inputs['Mode'].default_value = 'N-gons'
    except Exception:
        pass
    ex = t.n('GeometryNodeExtrudeMesh', (140, 100), mode='FACES'); t.L(fc0.outputs[0], ex.inputs['Mesh'])
    t.L(up.outputs[0], ex.inputs['Offset']); t.L(t.g("Height"), ex.inputs['Offset Scale'])
    t.out(ex.outputs['Mesh']); t.go.location = (360, 100)
    t.frame("01  a plan: one of four flat shapes", nodes + [ms]); t.frame("02  fill it, then extrude it straight up by Height", [fc0, up, ex])
    t.tidy()
    u = UI(key, cam)
    for n, ty, d in (("Footprint", "Int", 0), ("Width", "Float", 3.0), ("Depth", "Float", 2.0), ("Height", "Float", 2.0)):
        u.inp(n, ty, d)
    fp, W, D, H = (u.g(n) for n in ("Footprint", "Width", "Depth", "Height"))
    outs, _ = footprints(u, W, D, -1200, -2000)
    pm = u.iswitch('GEOMETRY', 4, u.place()); u.L(fp, pm.inputs['Index'])
    for k, s in enumerate(outs):
        u.L(s, pm.inputs[k + 1])
    u.add(u.tube(u.transform(pm.outputs[0], (0, 0, 0.02), loc=u.place()), 0.035, 'PINK'))
    u.mass(u.g("Geometry"))
    p0 = u.vmath('SCALE', RIGHT, u.math('ADD', u.math('MULTIPLY', W, 0.5, u.place()), 0.8, u.place()), u.place())
    u.arrow(p0, u.vmath('ADD', p0, u.xyz(0.0, 0.0, H, u.place()), u.place()))
    u.text(u.cat(["height ", u.fmt(H)]), u.vmath('ADD', p0, u.xyz(-0.25, 0.25, u.math('MULTIPLY', H, 0.5, u.place()), u.place()), u.place()), 0.26, 'PINK', left=True)
    w_ = u.fmt(W)
    lines = [('k', u.sswitch(fp, [u.cat(["1  plan: rectangle ", w_, " x ", u.fmt(D)]), u.cat(["1  plan: circle ", w_, " across"]),
                                  u.cat(["1  plan: hexagon ", w_, " across"]), u.cat(["1  plan: star ", w_, " across"])])),
             ('p', ["2  extrude up ", u.fmt(H)]), ('k', "")] + tools(["E in edit mode,", "or the Solidify modifier"], "Extrude")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Footprint", "Footprint"), ("Width", "Width"), ("Depth", "Depth"), ("Height", "Height")])


# ================================================================ 11 Split
def paint_parts(u, geo, attr, on='PINK', off='WHITE', lift=None):
    top, rest = u.split(geo, u.named(attr))
    if lift is not None:
        top = u.transform(top, lift, loc=u.place())
    u.mass(rest, off); u.mass(top, on)
    return top


def s11():
    key = "11 Split"
    sc, cam, hud = PD['make_slide'](key, 11, "SPLIT",
        "Split cuts a mass into parts with a plane.\n\n"
        "After a split each part can take its own operation. Many diagrams start here.",
        "Move Cut Height. In the UI panel, raise Explode to pull the parts apart.", scale=14)
    PD['aim'](cam, (0, 0, 2.2), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Cut Height", "Float", 1.5, 0.0, 4.0, "Height of the cutting plane")
    bx = t.box(3.0, 2.0, 4.0, (-800, 200))
    big = t.n('GeometryNodeMeshCube', (-800, -100)); big.inputs['Size'].default_value = (1000, 1000, 1000)
    tb = t.transform(big.outputs[0], t.xyz(0.0, 0.0, t.math('SUBTRACT', t.g("Cut Height"), 500, (-800, -300)), (-620, -300)), loc=(-600, -100))
    bi = t.n('GeometryNodeMeshBoolean', (-300, 200)); bi.operation = 'INTERSECT'; t.L(tb, bi.inputs['Mesh 2']); t.L(bx.outputs[0], bi.inputs['Mesh 2'])
    bd = t.n('GeometryNodeMeshBoolean', (-300, -60)); bd.operation = 'DIFFERENCE'; t.L(bx.outputs[0], bd.inputs['Mesh 1']); t.L(tb, bd.inputs['Mesh 2'])
    s1 = t.store(bi.outputs[0], "top", False, loc=(-80, 200)); s2 = t.store(bd.outputs[0], "top", True, loc=(-80, -60))
    j = t.joing([s1, s2], (120, 80)); t.out(j); t.go.location = (300, 80)
    t.frame("01  box 3 x 2 x 4", [bx]); t.frame("02  the cutting plane: a big box below Cut Height", [big, tb.node] + [n for n in t.nt.nodes if n.bl_idname in ('ShaderNodeMath', 'ShaderNodeCombineXYZ')])
    t.frame("03  bottom = keep the overlap, top = cut it away", [bi, bd, s1.node, s2.node])
    t.note("11 note - split", "A split is two Boolean operations with the same cutter. The attribute top marks which part is which.",
           (-900, 460), 520, 90)
    t.tidy()
    u = UI(key, cam)
    u.inp("Cut Height", "Float", 1.5); u.inp("Explode", "Float", 0.4, 0.0, 2.0, "Display only: pull the parts apart")
    ch = u.g("Cut Height")
    paint_parts(u, u.g("Geometry"), "top", lift=u.xyz(0.0, 0.0, u.g("Explode"), u.place()))
    q = u.n('GeometryNodeCurvePrimitiveQuadrilateral', u.place(), mode='RECTANGLE'); u.set(q, Width=4.2, Height=3.2)
    u.add(u.tube(u.transform(q.outputs[0], u.xyz(0.0, 0.0, ch, u.place()), loc=u.place()), 0.025, 'CYAN'))
    lines = [('k', "1  box 3 x 2 x 4"), ('p', ["2  split at height ", u.fmt(ch)]), ('k', "   a bottom part and a top part"),
             ('k', "")] + tools("Boolean modifier with a big box", "Split Brep")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Cut Height", "Cut Height")])


# ================================================================ 12 Shift / Lift
def s12():
    key = "12 Shift Lift"
    sc, cam, hud = PD['make_slide'](key, 12, "SHIFT AND LIFT",
        "Shift moves one part sideways. Lift moves it up.\n\nBoth are a move, applied to one part after a split.",
        "Change Shift X, Shift Y and Lift. Then move Cut Height.", scale=15)
    PD['aim'](cam, (0.5, 0, 2.4), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Cut Height", "Float", 2.0, 0.2, 3.8, "Where the box is split")
    t.inp("Shift X", "Float", 1.0, -3.0, 3.0, "Move the top part along x"); t.inp("Shift Y", "Float", 0.0, -3.0, 3.0, "Move the top part along y")
    t.inp("Lift", "Float", 0.5, 0.0, 3.0, "Move the top part up")
    bx = t.box(3.0, 2.0, 4.0, (-800, 0))
    sp = t.n('GeometryNodeGroup', (-560, 0)); sp.node_tree = PD['G']("Split"); t.L(bx.outputs[0], sp.inputs['Geometry']); t.L(t.g("Cut Height"), sp.inputs['Cut Height'])
    mv = t.xyz(t.g("Shift X"), t.g("Shift Y"), t.g("Lift"), (-560, -240))
    tp = t.transform(sp.outputs['Top'], mv, loc=(-300, -80))
    s1 = t.store(sp.outputs['Bottom'], "top", False, loc=(-80, 120)); s2 = t.store(tp, "top", True, loc=(-80, -80))
    t.out(t.joing([s1, s2], (120, 40))); t.go.location = (300, 40)
    t.frame("01  box and split", [bx, sp]); t.frame("02  shift and lift the top part", [mv.node, tp.node, s1.node, s2.node])
    t.tidy()
    u = UI(key, cam)
    for n, d in (("Cut Height", 2.0), ("Shift X", 1.0), ("Shift Y", 0.0), ("Lift", 0.5)):
        u.inp(n, "Float", d)
    sx, sy, lf, ch = (u.g(n) for n in ("Shift X", "Shift Y", "Lift", "Cut Height"))
    mv = u.xyz(sx, sy, lf, u.place())
    top = paint_parts(u, u.g("Geometry"), "top")
    u.ghost(u.transform(top, u.vmath('SCALE', mv, -1.0, u.place()), loc=u.place()))
    u.arrow((0, 0, 4.6), u.vmath('ADD', mv, (0, 0, 4.6), u.place()))
    lines = [('k', "1  box 3 x 2 x 4"), ('k', ["2  split at height ", u.fmt(ch)]),
             ('p', ["3  shift top  x ", u.fmt(sx), "  y ", u.fmt(sy)]), ('p', ["4  lift top ", u.fmt(lf)]),
             ('k', "")] + tools("select the part, G", "Move")
    u.code(lines, y=-0.25)
    u.finish()
    return done(key, sc, t, u, [("Cut Height", "Cut Height"), ("Shift X", "Shift X"), ("Shift Y", "Shift Y"), ("Lift", "Lift")])


# ================================================================ 13 Taper
def s13():
    key = "13 Taper"
    sc, cam, hud = PD['make_slide'](key, 13, "TAPER",
        "Taper scales a mass more and more toward the top: full size at the base, Top at the roof.\n\n"
        "Below 1 it narrows, above 1 it widens.",
        "Change Top. Try 0: the box becomes a pyramid.", scale=15)
    PD['aim'](cam, (0, 0, 2.5), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Top", "Float", 0.5, 0.0, 2.0, "Size of the roof compared to the base")
    bx = t.box(3.0, 3.0, 5.0, (-800, 0))
    p = t.n('GeometryNodeInputPosition', (-800, -220))
    x, y, z = t.sep(p.outputs[0], (-620, -220))[:3]
    mr = t.n('ShaderNodeMapRange', (-420, -260)); t.L(z, mr.inputs[0]); mr.inputs[1].default_value = 0.0; mr.inputs[2].default_value = 5.0
    mr.inputs[3].default_value = 1.0; t.L(t.g("Top"), mr.inputs[4]); mr.clamp = False
    f = mr.outputs[0]
    np_ = t.xyz(t.math('MULTIPLY', x, f, (-220, -160)), t.math('MULTIPLY', y, f, (-220, -300)), z, (-40, -220))
    spn = t.n('GeometryNodeSetPosition', (160, 0)); t.L(bx.outputs[0], spn.inputs['Geometry']); t.L(np_, spn.inputs['Position'])
    t.out(spn.outputs[0]); t.go.location = (360, 0)
    t.frame("01  box 3 x 3 x 5", [bx])
    t.frame("02  scale x and y by height: 1 at the base, Top at the roof", [p, x.node, mr, f.node if hasattr(f, 'node') else mr, np_.node, spn] + [n for n in t.nt.nodes if n.bl_idname == 'ShaderNodeMath'])
    t.tidy()
    u = UI(key, cam)
    u.inp("Top", "Float", 0.5)
    tp = u.g("Top")
    u.ghost(u.box(3.0, 3.0, 5.0, u.place()).outputs[0])
    u.mass(u.g("Geometry"))
    u.text(u.cat(["top x ", u.fmt(tp)]), (-1.6, 1.6, 5.4), 0.26, 'PINK')
    lines = [('k', "1  box 3 x 3 x 5"), ('p', ["2  taper: the roof is ", u.fmt(tp), " x the base"]),
             ('k', "")] + tools("Simple Deform modifier, Taper", "Taper")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Top", "Top")])


# ================================================================ 14 Twist
def s14():
    key = "14 Twist"
    sc, cam, hud = PD['make_slide'](key, 14, "TWIST",
        "Twist turns every floor a little more than the one below: nothing at the base, the full angle at the roof.\n\n"
        "Floors sets how many cuts can turn.",
        "Change Twist. Set Floors to 1: what happens to the faces?", scale=16)
    PD['aim'](cam, (0, 0, 3.0), ISO, shift=2.6)
    t = Tree(key)
    t.inp("Twist", "Float", 90.0, -360.0, 360.0, "Turn of the roof compared to the base (degrees)")
    t.inp("Floors", "Int", 12, 1, 48, "How many cuts along the height")
    cu = t.n('GeometryNodeMeshCube', (-800, 100)); cu.inputs['Size'].default_value = (3, 3, 6)
    t.L(t.math('ADD', t.g("Floors"), 1, (-1000, 0)), cu.inputs['Vertices Z'])
    up = t.transform(cu.outputs[0], (0, 0, 3.0), loc=(-600, 100))
    p = t.n('GeometryNodeInputPosition', (-800, -200))
    z = t.sep(p.outputs[0], (-620, -260))[2]
    ang = t.math('MULTIPLY', t.math('DIVIDE', z, 6.0, (-440, -260)), t.math('RADIANS', t.g("Twist"), None, (-440, -380)), (-260, -300))
    vr = t.n('ShaderNodeVectorRotate', (-80, -200), rotation_type='Z_AXIS'); t.L(p.outputs[0], vr.inputs['Vector']); t.L(ang, vr.inputs['Angle'])
    spn = t.n('GeometryNodeSetPosition', (120, 80)); t.L(up, spn.inputs['Geometry']); t.L(vr.outputs[0], spn.inputs['Position'])
    t.out(spn.outputs[0]); t.go.location = (320, 80)
    t.frame("01  box 3 x 3 x 6, cut into Floors", [cu, up.node]); t.frame("02  turn each point by its height: 0 at the base, Twist at the roof", [p, z.node, ang.node, vr, spn] + [n for n in t.nt.nodes if n.bl_idname == 'ShaderNodeMath' and n.location.y < -150])
    t.tidy()
    u = UI(key, cam)
    u.inp("Twist", "Float", 90.0); u.inp("Floors", "Int", 12)
    u.ghost(u.box(3.0, 3.0, 6.0, u.place()).outputs[0])
    u.mass(u.g("Geometry"))
    lines = [('k', ["1  box 3 x 3 x 6, ", u.fmt(u.g("Floors"), 0), " floors"]), ('p', ["2  twist ", u.fmt(u.g("Twist"), 0), "° from base to roof"]),
             ('k', "")] + tools(["loop cuts, then", "Simple Deform modifier, Twist"], "Twist")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Twist", "Twist"), ("Floors", "Floors")])


# ================================================================ 15 Keep it live
def s15():
    key = "15 Keep It Live"
    sc, cam, hud = PD['make_slide'](key, 15, "KEEP IT LIVE",
        "Non-destructive: every step stays editable. Change a number early and everything after it updates.\n\n"
        "Applying a step freezes it into a plain mesh and throws its numbers away.",
        "Change Radius. Then turn on Applied and change Radius again: nothing happens.", scale=13)
    PD['aim'](cam, (0, 0, 1.3), ISO, shift=2.7)
    t = Tree(key)
    t.inp("Radius", "Float", 1.3, 0.2, 2.4, "Radius of the sphere")
    t.inp("Applied", "Bool", False, desc="On: the operation is applied, its history is gone")
    bx = t.box(2.4, 2.4, 2.4, (-700, 240))
    sw = t.n('GeometryNodeSwitch', (-900, -60), input_type='FLOAT'); t.L(t.g("Applied"), sw.inputs['Switch'])
    t.L(t.g("Radius"), sw.inputs['False']); sw.inputs['True'].default_value = 1.3
    sp = t.n('GeometryNodeMeshUVSphere', (-700, -60)); sp.inputs['Segments'].default_value = 48; sp.inputs['Rings'].default_value = 24
    t.L(sw.outputs[0], sp.inputs['Radius'])
    spt = t.transform(sp.outputs[0], (1.2, 1.2, 2.4), loc=(-500, -60))
    bd = t.n('GeometryNodeMeshBoolean', (-260, 120)); bd.operation = 'DIFFERENCE'
    t.L(bx.outputs[0], bd.inputs['Mesh 1']); t.L(spt, bd.inputs['Mesh 2'])
    t.out(bd.outputs[0]); t.go.location = (-40, 120)
    t.frame("01  box", [bx]); t.frame("02  sphere on the top corner: Radius stays live, unless Applied", [sw, sp, spt.node])
    t.frame("03  difference: box minus sphere", [bd])
    t.note("15 note - applied", "Applied stands in for Apply (Blender) or Bake (Grasshopper): the result is frozen at "
           "radius 1.3, so the Radius slider no longer reaches it.", (-950, 520), 560, 100)
    t.tidy()
    u = UI(key, cam)
    u.inp("Radius", "Float", 1.3); u.inp("Applied", "Bool", False)
    ap = u.g("Applied"); r_ = u.fmt(u.g("Radius"))
    u.mass(u.g("Geometry"))
    u.text(u.sswitch(ap, [u.cat(["radius ", r_]), ""]), (1.6, 1.6, 3.6), 0.26, 'PINK')
    rows = [("k", ["1  box 2.4 x 2.4 x 2.4", "1  one mesh"]),
            ("k", [u.cat(["2  sphere, radius ", r_]), "   box, sphere and radius are gone"]),
            ("k", ["3  difference: box minus sphere", ""]),
            ("p", ["history: 3 live steps", "history: nothing left to edit"])]
    lines = [(c, u.sswitch(ap, r)) for c, r in rows]
    lines += [('k', "")] + tools("keep the modifiers, do not Apply", "keep the definition, Bake at the end")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Radius", "Radius"), ("Applied", "Applied")])


# ================================================================ 15 Procedure (shared group) and 16 Diagram
STEPS = ["PLACE", "SPLIT", "TURN", "SHIFT", "CARVE"]


def procedure_group():
    t = Tree("Procedure")
    t.inp("Width", "Float", 6.0, 0.5, 12.0, "Step 1: box size along x")
    t.inp("Depth", "Float", 4.0, 0.5, 12.0, "Step 1: box size along y")
    t.inp("Height", "Float", 3.0, 0.5, 12.0, "Step 1: box size along z")
    t.inp("Step", "Int", 5, 1, 5, "How many steps are done")
    t.inp("Cut Height", "Float", 1.5, 0.3, 2.7, "Step 2: where the mass is split")
    t.inp("Angle", "Float", 15.0, -90.0, 90.0, "Step 3: turn of the top part (degrees)")
    t.inp("Shift", "Float", 1.5, -3.0, 3.0, "Step 4: shift of the top part along x")
    t.inp("Passage", "Float", 2.0, 0.0, 4.0, "Step 5: width of the passage carved through the bottom")
    bx = t.box(t.g("Width"), t.g("Depth"), t.g("Height"), (-1100, 300))
    sp = t.n('GeometryNodeGroup', (-850, 300)); sp.node_tree = PD['G']("Split"); t.L(bx.outputs[0], sp.inputs['Geometry']); t.L(t.g("Cut Height"), sp.inputs['Cut Height'])
    tr = t.transform(sp.outputs['Top'], None, rot_z(t, t.g("Angle"), (-1100, 60)), loc=(-560, 120))
    ts = t.transform(tr, t.xyz(t.g("Shift"), 0.0, 0.0, (-750, -120)), loc=(-560, -60))
    cut = t.transform(t.box(t.g("Passage"), t.math('ADD', t.g("Depth"), 1.0, (-1300, -360)), 1.1, (-1100, -320)).outputs[0], (0, 0, -0.1), loc=(-850, -320))
    bc = t.n('GeometryNodeMeshBoolean', (-560, -280)); bc.operation = 'DIFFERENCE'
    t.L(sp.outputs['Bottom'], bc.inputs['Mesh 1']); t.L(cut, bc.inputs['Mesh 2'])
    st = lambda g, v, y: t.store(g, "changed", v, loc=(-300, y))
    stages = [st(bx.outputs[0], True, 520),
              t.joing([st(sp.outputs['Bottom'], False, 360), st(sp.outputs['Top'], True, 260)], (-120, 300)),
              t.joing([st(sp.outputs['Bottom'], False, 160), st(tr, True, 60)], (-120, 100)),
              t.joing([st(sp.outputs['Bottom'], False, -40), st(ts, True, -140)], (-120, -100)),
              t.joing([st(bc.outputs[0], True, -240), st(ts, False, -340)], (-120, -300))]
    sw = t.iswitch('GEOMETRY', 5, (120, 0)); t.L(t.math('SUBTRACT', t.g("Step"), 1, (-60, 160)), sw.inputs['Index'])
    for k, s in enumerate(stages):
        t.L(s, sw.inputs[k + 1])
    t.out(sw.outputs[0]); t.go.location = (320, 0)
    t.frame("1  place a box Width x Depth x Height", [bx]); t.frame("2  split", [sp]); t.frame("3  turn the top", [tr.node])
    t.frame("4  shift the top", [ts.node]); t.frame("5  carve a passage through the bottom", [cut.node, bc])
    t.note("Procedure note", "Every step works on the result of the step before. The attribute changed marks what the "
           "current step touched: the diagrams paint it.", (-1150, 760), 600, 100)
    t.tidy(); t.nt.use_fake_user = True
    return t.nt


def proc_paint(u, geo):
    ch, rest = u.split(geo, u.named("changed"))
    u.mass(rest, 'WHITE'); u.mass(ch, 'PINK')


def s16():
    key = "16 Procedure"
    sc, cam, hud = PD['make_slide'](key, 16, "A PROCEDURE",
        "A procedure is a numbered list of operations. Each step works on the result of the one before.\n\n"
        "Pink shows what the current step changed.",
        "Set Step from 1 to 5. Then change Angle or Shift: every later step follows.", scale=22)
    PD['aim'](cam, (0.5, 0, 1.4), ISO, shift=3.2)
    nt = procedure_group()
    u = UI(key, cam)
    names = [("Width", "Float", 6.0), ("Depth", "Float", 4.0), ("Height", "Float", 3.0), ("Step", "Int", 5), ("Cut Height", "Float", 1.5), ("Angle", "Float", 15.0), ("Shift", "Float", 1.5), ("Passage", "Float", 2.0)]
    for n, ty, d in names:
        u.inp(n, ty, d)
    stp = u.g("Step")
    proc_paint(u, u.g("Geometry"))
    rows = [["1  place a box ", u.fmt(u.g("Width")), " x ", u.fmt(u.g("Depth")), " x ", u.fmt(u.g("Height"))], ["2  split it at height ", u.fmt(u.g("Cut Height"))], ["3  turn the top ", u.fmt(u.g("Angle"), 0), "°"],
            ["4  shift the top ", u.fmt(u.g("Shift"))], ["5  carve a passage ", u.fmt(u.g("Passage")), " wide"]]
    lines = [(step_color(u, stp, i + 1), r) for i, r in enumerate(rows)]
    lines += [('k', "")] + tools("one named modifier per step", "one component per step")
    u.code(lines)
    u.finish()
    return done(key, sc, nt, u, [(n, n) for n, _, _ in names])


def s17():
    key = "17 Diagram"
    sc, cam, hud = PD['make_slide'](key, 17, "THE DIAGRAM",
        "One move per frame, captioned with one verb, read left to right. Same view and scale in every frame; "
        "mark only what changed (color, arrow or ghost). It should read without words.",
        None, scale=50, col_w=12)
    sp_ = 9.0
    PD['aim'](cam, (0, 0, 1.5), ISO, shift=0.0, lift=-0.9)
    t = Tree(key)
    for n, ty, d, mn, mx, ds in (("Width", "Float", 6.0, 0.5, 12.0, "Step 1"), ("Depth", "Float", 4.0, 0.5, 12.0, "Step 1"),
                                 ("Height", "Float", 3.0, 0.5, 12.0, "Step 1"), ("Cut Height", "Float", 1.5, 0.3, 2.7, "Step 2"), ("Angle", "Float", 15.0, -90.0, 90.0, "Step 3 (degrees)"),
                                 ("Shift", "Float", 1.5, -3.0, 3.0, "Step 4"), ("Passage", "Float", 2.0, 0.0, 4.0, "Step 5")):
        t.inp(n, ty, d, mn, mx, ds)
    frames = []
    for k in range(5):
        g = t.n('GeometryNodeGroup', (-300, 400 - 220 * k)); g.node_tree = PD['G']("Procedure"); g.inputs['Step'].default_value = k + 1
        for n in ("Width", "Depth", "Height", "Cut Height", "Angle", "Shift", "Passage"):
            t.L(t.g(n), g.inputs[n])
        off = tuple(c * (k - 2) * sp_ for c in RIGHT)
        frames.append(t.transform(g.outputs[0], off, loc=(-60, 400 - 220 * k)))
    t.out(t.joing(frames, (200, 0))); t.go.location = (400, 0)
    t.frame("five frames: the same procedure stopped at step 1, 2, 3, 4 and 5, side by side", [n for n in t.nt.nodes if n.bl_idname in ('GeometryNodeGroup', 'GeometryNodeTransform')])
    t.tidy()
    u = UI(key, cam)
    proc_paint(u, u.g("Geometry"))
    down = PD['camdir'](cam, (0, -1, 0))
    for k, nm in enumerate(STEPS):
        c = [RIGHT[i] * (k - 2) * sp_ + down[i] * 4.6 for i in range(3)]
        u.text(f"{k + 1}  {nm}", tuple(c), 0.3, 'BLACK')
    u.finish()
    return done(key, sc, t, u, [])


PB = {f"s{n:02d}": globals()[f"s{n:02d}"] for n in range(1, 18)}
PB['procedure_group'] = procedure_group
bpy.app.driver_namespace['PB'] = PB
print("procedural_build ready")
