"""generative_build.py: builds Introduction-to-Generative-Design.blend (ARC 3133, Project 4).

Run blender_slidekit.py, procedural_slidekit.py and generative_slidekit.py first (they register SK, PD
and GK), then this file. It registers GB: GB['groups']() builds the shared node groups, GB['s05']()
rebuilds slide 05 (and resets its values). Cards are plain-word rules, no Python.
"""
import bpy, math

GK = bpy.app.driver_namespace['GK']
Tree, UI, G = GK['Tree'], GK['UI'], GK['G']
ISO, TOP = GK['ISO'], GK['TOP']
RIGHT = (-0.70711, 0.70711, 0.0)      # screen right in the isometric view
DOWN = (0.70711, 0.70711, 0.0)        # toward the viewer: reads as down on screen
RAD = math.radians


# ---------------------------------------------------------------- small helpers
def S(n, name, out=False):
    socks = n.outputs if out else n.inputs
    return next(s for s in socks if s.name == name and getattr(s, 'enabled', True))


def setv(t, sock, v):
    if isinstance(v, (bool, int, float, tuple, str)):
        sock.default_value = v
    else:
        t.L(v, sock)


def grp(t, name, loc, vals=None):
    g = t.n('GeometryNodeGroup', loc); g.node_tree = G(name)
    for k, v in (vals or {}).items():
        setv(t, g.inputs[k], v)
    return g


def cmp(t, op, a, b, loc, dtype='FLOAT'):
    c = t.n('FunctionNodeCompare', loc, data_type=dtype, operation=op)
    ins = [s for s in c.inputs if getattr(s, 'enabled', True)]
    setv(t, ins[0], a); setv(t, ins[1], b)
    return c.outputs[0]


def bmath(t, op, a, b=None, loc=(0, 0)):
    n = t.n('FunctionNodeBooleanMath', loc, operation=op)
    setv(t, n.inputs[0], a)
    if b is not None:
        setv(t, n.inputs[1], b)
    return n.outputs[0]


def named(t, name, dtype='FLOAT', loc=(0, 0)):
    n = t.n('GeometryNodeInputNamedAttribute', loc, data_type=dtype)
    if isinstance(name, str):
        n.inputs['Name'].default_value = name
    else:
        t.L(name, n.inputs['Name'])
    return n.outputs['Attribute']


def index(t, loc):
    return t.n('GeometryNodeInputIndex', loc).outputs[0]


def position(t, loc):
    return t.n('GeometryNodeInputPosition', loc).outputs[0]


def sample(t, geo, value, idx, dtype='FLOAT', loc=(0, 0)):
    s = t.n('GeometryNodeSampleIndex', loc, data_type=dtype, domain='POINT')
    t.L(geo, s.inputs['Geometry']); t.L(value, s.inputs['Value']); setv(t, s.inputs['Index'], idx)
    return s.outputs[0]


def rand(t, dtype, mn, mx, seed, loc, ident=None, prob=None):
    r = t.n('FunctionNodeRandomValue', loc, data_type=dtype)
    if dtype == 'BOOLEAN':
        setv(t, S(r, 'Probability'), prob)
    else:
        setv(t, S(r, 'Min'), mn); setv(t, S(r, 'Max'), mx)
    setv(t, S(r, 'Seed'), seed)
    if ident is not None:
        setv(t, S(r, 'ID'), ident)
    return S(r, 'Value', True)


def repeat(t, iterations, start, loc, extra=()):
    rin = t.n('GeometryNodeRepeatInput', loc); rout = t.n('GeometryNodeRepeatOutput', (loc[0] + 1400, loc[1]))
    rin.pair_with_output(rout)
    for name in extra:
        rout.repeat_items.new('GEOMETRY', name)
    setv(t, rin.inputs['Iterations'], iterations)
    t.L(start, rin.inputs['Geometry'])
    return rin, rout


def rot_z(t, deg, loc):
    rad = t.math('RADIANS', deg, None, loc) if not isinstance(deg, (int, float)) else math.radians(deg)
    return t.euler(t.xyz(0.0, 0.0, rad, (loc[0] + 180, loc[1])), (loc[0] + 360, loc[1]))


def plates(t, cells, attr, C, R, cell, height, loc):
    """Cells (points) to a face grid; keep the faces whose cell has attr; extrude them as one region."""
    x, y = loc
    gx = t.math('MULTIPLY', C, cell, (x, y)); gy = t.math('MULTIPLY', R, cell, (x, y - 120))
    gr = t.n('GeometryNodeMeshGrid', (x + 180, y))
    t.L(gx, gr.inputs['Size X']); t.L(gy, gr.inputs['Size Y'])
    t.L(t.math('ADD', C, 1, (x, y - 240)), gr.inputs['Vertices X']); t.L(t.math('ADD', R, 1, (x, y - 360)), gr.inputs['Vertices Y'])
    sn = t.n('GeometryNodeSampleNearest', (x + 180, y - 200)); t.L(cells, sn.inputs['Geometry'])
    on = sample(t, cells, named(t, attr, 'BOOLEAN', (x + 180, y - 360)), sn.outputs[0], 'BOOLEAN', (x + 360, y - 200))
    dl = t.n('GeometryNodeDeleteGeometry', (x + 540, y), domain='FACE')
    t.L(gr.outputs[0], dl.inputs['Geometry']); t.L(bmath(t, 'NOT', on, None, (x + 540, y - 200)), dl.inputs['Selection'])
    up = t.n('FunctionNodeInputVector', (x + 540, y - 320)); up.vector = (0, 0, 1)
    ex = t.n('GeometryNodeExtrudeMesh', (x + 720, y), mode='FACES')
    t.L(dl.outputs[0], ex.inputs['Mesh']); t.L(up.outputs[0], ex.inputs['Offset']); setv(t, ex.inputs['Offset Scale'], height)
    ex.inputs['Individual'].default_value = False
    return ex.outputs['Mesh']


def done(key, sc, t, u, drive, extra=None):
    ob = GK['lesson_object'](sc, t.nt if hasattr(t, 'nt') else t, u.nt, drive)
    if extra:
        extra(ob)
    bpy.context.window.scene = sc
    GK['snap'](sc, "GEN_" + key[:2])
    return ob


def tools(blender, gh):
    out = []
    for i, b in enumerate(blender if isinstance(blender, list) else [blender]):
        out.append(('g', ("Blender:  " if i == 0 else "          ") + b))
    for i, g in enumerate(gh if isinstance(gh, list) else [gh]):
        out.append(('g', ("Grasshopper:  " if i == 0 else "              ") + g))
    return out


# ---------------------------------------------------------------- UI helpers
def squares(u, pts, size, color, outline=False, z=0.0):
    pl = u.n('GeometryNodeMeshGrid', u.place()); u.set(pl, Size_X=size, Size_Y=size, Vertices_X=2, Vertices_Y=2)
    io = u.n('GeometryNodeInstanceOnPoints', u.place()); u.L(pts, io.inputs['Points']); u.L(pl.outputs[0], io.inputs['Instance'])
    rz = u.n('GeometryNodeRealizeInstances', u.place()); u.L(io.outputs[0], rz.inputs[0])
    geo = u.transform(rz.outputs[0], (0, 0, z), loc=u.place()) if z else rz.outputs[0]
    if color is None:
        return geo
    u.add(u.paint(geo, color))
    if outline:
        u.add(u.edges(geo, 0.008, 'MUTE'))
    return geo


def value_paint(u, geo, attr, c0, c1, gain=1.0):
    na = named(u, attr, 'FLOAT', u.place())
    if isinstance(gain, (int, float)):
        fac = u.n('ShaderNodeMath', u.place(), operation='MULTIPLY', use_clamp=True)
        u.L(na, fac.inputs[0]); fac.inputs[1].default_value = gain
    else:
        fac = u.n('ShaderNodeMath', u.place(), operation='MULTIPLY', use_clamp=True)
        u.L(na, fac.inputs[0]); u.L(gain, fac.inputs[1])
    mx = u.n('ShaderNodeMix', u.place(), data_type='RGBA')
    u.L(fac.outputs[0], S(mx, 'Factor'))
    S(mx, 'A').default_value = GK['C'](c0); S(mx, 'B').default_value = GK['C'](c1)
    st = u.n('GeometryNodeStoreNamedAttribute', u.place(), data_type='FLOAT_COLOR', domain='POINT')
    u.L(geo, st.inputs['Geometry']); st.inputs['Name'].default_value = ".viz_col"; u.L(S(mx, 'Result', True), st.inputs['Value'])
    sm = u.n('GeometryNodeSetMaterial', u.place()); u.L(st.outputs[0], sm.inputs['Geometry'])
    sm.inputs['Material'].default_value = bpy.data.materials["Viz"]
    u.add(sm.outputs[0])


def sel_(u, geo, attr, dtype='BOOLEAN'):
    return u.split(geo, named(u, attr, dtype, u.place()))


# ================================================================ shared groups
def g_cellgrid():
    t = Tree("Cell Grid")
    t.inp("Columns", "Int", 24, 1, 400, "Cells along x"); t.inp("Rows", "Int", 24, 1, 400, "Cells along y")
    t.inp("Cell", "Float", 0.5, 0.01, 10.0, "Size of one cell")
    C, Rw, cell = t.g("Columns"), t.g("Rows"), t.g("Cell")
    ix = index(t, (-900, -200))
    c = t.math('FLOOR', t.math('DIVIDE', ix, Rw, (-720, -160)), None, (-560, -160))
    r = t.math('FLOORED_MODULO', ix, Rw, (-720, -320))
    hc = t.math('MULTIPLY', t.math('SUBTRACT', C, 1.0, (-720, 0)), 0.5, (-560, 0))
    hr = t.math('MULTIPLY', t.math('SUBTRACT', Rw, 1.0, (-720, -460)), 0.5, (-560, -460))
    x = t.math('MULTIPLY', t.math('SUBTRACT', c, hc, (-400, -100)), cell, (-240, -100))
    y = t.math('MULTIPLY', t.math('SUBTRACT', r, hr, (-400, -320)), cell, (-240, -320))
    pts = t.n('GeometryNodePoints', (0, 0)); t.L(t.math('MULTIPLY', C, Rw, (-240, 120)), pts.inputs['Count'])
    t.L(t.xyz(x, y, 0.0, (-80, -200)), pts.inputs['Position']); t.L(t.math('MULTIPLY', cell, 0.4, (-240, -460)), pts.inputs['Radius'])
    s = t.store(t.store(pts.outputs[0], "column", c, 'INT', loc=(200, 0)), "row", r, 'INT', loc=(380, 0))
    t.out(s); t.go.location = (560, 0)
    t.note("Cell Grid note", "One point per cell, centred on the origin. Numbered column by column: "
           "index = column x Rows + row.", (-900, 260), 520, 90)
    t.tidy(); t.nt.use_fake_user = True


def g_noise():
    t = Tree("Noise Value", geo_out=False)
    t.outp("Value", "Float")
    t.inp("Seed", "Int", 0, 0, 9999, "Another seed, another field")
    t.inp("Scale", "Float", 0.25, 0.0, 10.0, "Features per metre: small = big blobs")
    nz = t.n('ShaderNodeTexNoise', (-300, 0)); nz.noise_dimensions = '4D'
    t.L(position(t, (-500, 60)), nz.inputs['Vector']); t.L(t.math('MULTIPLY', t.g("Seed"), 1.37, (-500, -80)), nz.inputs['W'])
    t.L(t.g("Scale"), nz.inputs['Scale']); nz.inputs['Detail'].default_value = 2.0
    mr = t.n('ShaderNodeMapRange', (-80, 0)); mr.clamp = True
    t.L(nz.outputs['Factor'], mr.inputs[0]); mr.inputs[1].default_value = 0.3; mr.inputs[2].default_value = 0.7
    mr.inputs[3].default_value = 0.0; mr.inputs[4].default_value = 1.0
    t.L(mr.outputs[0], t.go.inputs['Value']); t.go.location = (140, 0)
    t.note("Noise Value note", "Noise at each position, stretched to 0 (low) .. 1 (high). Same Seed, same field.", (-500, 220), 460, 80)
    t.tidy(); t.nt.use_fake_user = True


def g_neighbour():
    t = Tree("Neighbour", geo_out=False)
    t.outp("Value", "Float")
    t.inp("Geometry", "Geometry"); t.inp("Columns", "Int", 24); t.inp("Rows", "Int", 24)
    t.inp("Name", "String", "alive"); t.inp("DX", "Int", 0, -1, 1); t.inp("DY", "Int", 0, -1, 1)
    C, Rw = t.g("Columns"), t.g("Rows")
    ix = index(t, (-900, 0))
    c = t.math('ADD', t.math('FLOOR', t.math('DIVIDE', ix, Rw, (-720, 60)), None, (-560, 60)), t.g("DX"), (-400, 60))
    r = t.math('ADD', t.math('FLOORED_MODULO', ix, Rw, (-720, -80)), t.g("DY"), (-400, -80))
    v1 = t.math('GREATER_THAN', c, -0.5, (-240, 200)); v2 = t.math('LESS_THAN', c, t.math('SUBTRACT', C, 0.5, (-400, 200)), (-240, 100))
    v3 = t.math('GREATER_THAN', r, -0.5, (-240, -200)); v4 = t.math('LESS_THAN', r, t.math('SUBTRACT', Rw, 0.5, (-400, -300)), (-240, -300))
    ok = t.math('MULTIPLY', t.math('MULTIPLY', v1, v2, (-80, 150)), t.math('MULTIPLY', v3, v4, (-80, -250)), (80, 0))
    idx = t.math('ADD', t.math('MULTIPLY', c, Rw, (-240, 0)), r, (-80, 0))
    v = sample(t, t.g("Geometry"), named(t, t.g("Name"), 'FLOAT', (-80, -420)), idx, 'FLOAT', (80, -200))
    t.L(t.math('MULTIPLY', v, ok, (260, -100)), t.go.inputs['Value']); t.go.location = (440, -100)
    t.note("Neighbour note", "Reads the value of the cell DX columns and DY rows away. Outside the grid counts as 0.", (-900, 360), 480, 80)
    t.tidy(); t.nt.use_fake_user = True


def g_count():
    t = Tree("Count Neighbours", geo_out=False)
    t.outp("Count", "Float")
    t.inp("Geometry", "Geometry"); t.inp("Columns", "Int", 24); t.inp("Rows", "Int", 24); t.inp("Name", "String", "alive")
    acc = None; k = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            n = grp(t, "Neighbour", (-300, 400 - 120 * k), {"Geometry": t.g("Geometry"), "Columns": t.g("Columns"), "Rows": t.g("Rows"),
                                                         "Name": t.g("Name"), "DX": dx, "DY": dy})
            acc = n.outputs[0] if acc is None else t.math('ADD', acc, n.outputs[0], (-80 + 20 * k, 400 - 120 * k))
            k += 1
    t.L(acc, t.go.inputs['Count']); t.go.location = (300, 0)
    t.frame("the 8 neighbours, added up", [n for n in t.nt.nodes if n.bl_idname in ('GeometryNodeGroup', 'ShaderNodeMath')])
    t.tidy(); t.nt.use_fake_user = True


def g_life():
    t = Tree("Life Rule", geo_in=True)
    t.inp("Columns", "Int", 24); t.inp("Rows", "Int", 24)
    t.inp("Born", "Int", 3, 0, 8, "An empty cell with this many alive neighbours is born")
    t.inp("Survive Min", "Int", 2, 0, 8, "An alive cell survives with at least this many")
    t.inp("Survive Max", "Int", 3, 0, 8, "... and at most this many")
    t.inp("Allowed", "Bool", True, desc="Where a cell may live at all (the environment)")
    alive = named(t, "alive", 'BOOLEAN', (-700, 200))
    n = grp(t, "Count Neighbours", (-700, -60), {"Geometry": t.g("Geometry"), "Columns": t.g("Columns"), "Rows": t.g("Rows"), "Name": "alive"}).outputs[0]
    born = cmp(t, 'EQUAL', n, t.g("Born"), (-460, -20))
    smin = cmp(t, 'GREATER_THAN', n, t.math('SUBTRACT', t.g("Survive Min"), 0.5, (-700, -260)), (-460, -160))
    smax = cmp(t, 'LESS_THAN', n, t.math('ADD', t.g("Survive Max"), 0.5, (-700, -380)), (-460, -300))
    surv = bmath(t, 'AND', alive, bmath(t, 'AND', smin, smax, (-280, -220)), (-100, 120))
    newb = bmath(t, 'AND', bmath(t, 'NOT', alive, None, (-280, 200)), born, (-100, 0))
    nxt = bmath(t, 'AND', bmath(t, 'OR', surv, newb, (80, 60)), t.g("Allowed"), (260, 60))
    t.out(t.store(t.g("Geometry"), "alive", nxt, 'BOOLEAN', loc=(440, 60))); t.go.location = (640, 60)
    t.frame("count the alive neighbours", [n.node]); t.frame("born, survives or dies", [born.node, smin.node, smax.node, surv.node, newb.node, nxt.node])
    t.tidy(); t.nt.use_fake_user = True


def g_automaton():
    t = Tree("Automaton", geo_out=False)
    t.outp("Volume"); t.outp("Cells"); t.outp("Last")
    for n, ty, d, mn, mx, ds in (("Columns", "Int", 24, 2, 200, "Cells along x"), ("Rows", "Int", 24, 2, 200, "Cells along y"),
                                 ("Cell", "Float", 0.5, 0.05, 5.0, "Cell size (m)"), ("Seed", "Int", 0, 0, 9999, "Noise seed for floor 0"),
                                 ("Scale", "Float", 0.25, 0.01, 4.0, "Noise scale for floor 0"), ("Threshold", "Float", 0.5, 0.0, 1.0, "Floor 0: noise above this is alive"),
                                 ("Born", "Int", 4, 0, 8, "Born with this many alive neighbours"), ("Survive Min", "Int", 3, 0, 8, "Survives with at least"),
                                 ("Survive Max", "Int", 6, 0, 8, "... and at most"), ("Generations", "Int", 16, 0, 120, "How many floors"),
                                 ("Layer Height", "Float", 0.5, 0.01, 5.0, "Height of one generation (m)")):
        t.inp(n, ty, d, mn, mx, ds)
    t.inp("Center", "Vector", (0.0, 0.0, 0.0), desc="Environment: centre of the area where cells may live")
    t.inp("Reach", "Float", 0.0, 0.0, 50.0, "Environment: radius of that area (0 = no limit)")
    g = lambda n: t.g(n)
    grid = grp(t, "Cell Grid", (-1500, 300), {"Columns": g("Columns"), "Rows": g("Rows"), "Cell": g("Cell")})
    d = t.vmath('LENGTH', t.vmath('MULTIPLY', t.vmath('SUBTRACT', position(t, (-1700, -300)), g("Center"), (-1500, -300)), (1.0, 1.0, 0.0), (-1340, -300)), None, (-1180, -300), out=1)
    allowed = bmath(t, 'OR', cmp(t, 'LESS_THAN', d, g("Reach"), (-1020, -260)), cmp(t, 'LESS_THAN', g("Reach"), 0.001, (-1020, -400)), (-860, -300))
    nv = grp(t, "Noise Value", (-1500, 60), {"Seed": g("Seed"), "Scale": g("Scale")}).outputs[0]
    start = bmath(t, 'AND', cmp(t, 'GREATER_THAN', nv, g("Threshold"), (-1300, 60)), allowed, (-1120, 60))
    s0 = t.store(grid.outputs[0], "alive", start, 'BOOLEAN', loc=(-940, 200))
    rin, rout = repeat(t, g("Generations"), s0, (-700, 200), ("Cells", "Volume"))
    k = rin.outputs['Iteration']
    zv = t.xyz(0.0, 0.0, t.math('MULTIPLY', k, g("Layer Height"), (-520, -40)), (-360, -40))
    lay = t.transform(t.store(rin.outputs['Geometry'], "generation", k, 'INT', loc=(-360, 120)), zv, loc=(-180, 120))
    t.L(t.joing([rin.outputs['Cells'], lay], (0, 160)), rout.inputs['Cells'])
    pl = plates(t, rin.outputs['Geometry'], "alive", g("Columns"), g("Rows"), g("Cell"), g("Layer Height"), (-520, -260))
    plz = t.store(t.transform(pl, zv, loc=(400, -260)), "generation", k, 'INT', loc=(560, -260))
    t.L(t.joing([rin.outputs['Volume'], plz], (720, -200)), rout.inputs['Volume'])
    nxt = grp(t, "Life Rule", (400, 360), {"Geometry": rin.outputs['Geometry'], "Columns": g("Columns"), "Rows": g("Rows"), "Born": g("Born"),
                                          "Survive Min": g("Survive Min"), "Survive Max": g("Survive Max"), "Allowed": allowed})
    t.L(nxt.outputs[0], rout.inputs['Geometry'])
    t.L(rout.outputs['Volume'], t.go.inputs['Volume']); t.L(rout.outputs['Cells'], t.go.inputs['Cells']); t.L(rout.outputs['Geometry'], t.go.inputs['Last'])
    t.go.location = (1000, 0)
    t.frame("floor 0: noise above Threshold, inside the environment", [grid, nv.node, start.node, s0.node])
    t.frame("each generation: keep a copy as a layer, then apply the rule", [rin, rout, lay.node, zv.node, plz.node, nxt])
    t.tidy(); t.nt.use_fake_user = True


def groups():
    g_cellgrid(); g_noise(); g_neighbour(); g_count(); g_life(); g_automaton()


# ================================================================ 01 Generative
def s01():
    key = "01 Generative"
    sc, cam, hud = GK['make_slide'](key, 1, "GENERATIVE",
        "A generative engine explores a solution space you have not mapped, returning answers you did not anticipate.\n\n"
        "Procedural is about steps, parametric about relationships. Generative iterates: a rule works on its own result.",
        "Set Steps to 500, 3000, 10000, then 12000. The highway starts near step 10,000. Nobody wrote it.", scale=16)
    GK['aim'](cam, (0, 0, 0), TOP, shift=2.9)
    t = Tree(key)
    t.inp("Steps", "Int", 11000, 0, 20000, "How many times the rule runs"); t.inp("Size", "Int", 90, 10, 200, "Cells per side")
    N = t.g("Size")
    grid = grp(t, "Cell Grid", (-1100, 200), {"Columns": N, "Rows": N, "Cell": 0.1})
    s0 = t.store(grid.outputs[0], "black", False, 'BOOLEAN', loc=(-900, 200))
    rin, rout = repeat(t, t.g("Steps"), s0, (-700, 200))
    for nm in ("X", "Y", "H"):
        rout.repeat_items.new('INT', nm)
    half = t.math('FLOOR', t.math('DIVIDE', N, 2, (-900, -40)), None, (-900, -140))
    t.L(half, rin.inputs['X']); t.L(half, rin.inputs['Y']); rin.inputs['H'].default_value = 0
    st, X, Y, H = rin.outputs['Geometry'], rin.outputs['X'], rin.outputs['Y'], rin.outputs['H']
    idx = t.math('ADD', t.math('MULTIPLY', X, N, (-500, 0)), Y, (-350, 0))
    blk = named(t, "black", 'BOOLEAN', (-500, -200))
    cur = sample(t, st, blk, idx, 'BOOLEAN', (-200, -200))
    turn = t.n('GeometryNodeSwitch', (0, -200), input_type='INT'); t.L(cur, turn.inputs['Switch'])
    turn.inputs['False'].default_value = 1; turn.inputs['True'].default_value = -1
    nh = t.math('FLOORED_MODULO', t.math('ADD', H, turn.outputs[0], (200, -200)), 4, (350, -200))
    sel = cmp(t, 'EQUAL', index(t, (-200, 420)), idx, (0, 420), 'INT')
    flip = bmath(t, 'NOT', blk, None, (0, 280))
    stn = t.n('GeometryNodeStoreNamedAttribute', (200, 420), data_type='BOOLEAN', domain='POINT')
    t.L(st, stn.inputs['Geometry']); t.L(sel, stn.inputs['Selection']); stn.inputs['Name'].default_value = "black"; t.L(flip, stn.inputs['Value'])
    t.L(stn.outputs[0], rout.inputs['Geometry'])
    dx = t.iswitch('INT', 4, (350, -400)); dy = t.iswitch('INT', 4, (350, -560))
    for sw, vals in ((dx, (0, 1, 0, -1)), (dy, (1, 0, -1, 0))):
        t.L(nh, sw.inputs['Index'])
        for k, v in enumerate(vals):
            sw.inputs[k + 1].default_value = v
    t.L(t.math('FLOORED_MODULO', t.math('ADD', X, dx.outputs[0], (550, -400)), N, (700, -400)), rout.inputs['X'])
    t.L(t.math('FLOORED_MODULO', t.math('ADD', Y, dy.outputs[0], (550, -560)), N, (700, -560)), rout.inputs['Y'])
    t.L(nh, rout.inputs['H'])
    ant = cmp(t, 'EQUAL', index(t, (900, 0)), t.math('ADD', t.math('MULTIPLY', rout.outputs['X'], N, (900, -120)), rout.outputs['Y'], (1050, -120)), (1200, 0), 'INT')
    t.out(t.store(rout.outputs['Geometry'], "ant", ant, 'BOOLEAN', loc=(1400, 200))); t.go.location = (1600, 200)
    t.frame("START  a white grid and one ant in the middle, facing up", [grid, s0.node, half.node])
    t.frame("RULE  on a white cell turn right, on a black cell turn left; flip the cell; step forward.  REPEAT",
            [rin, rout, idx.node, blk.node, cur.node, turn, nh.node, sel.node, flip.node, stn, dx, dy])
    t.note("01 note - langton", "Langton's ant (1986). Two rules, no randomness. About 10,000 steps of apparent chaos, "
           "then a diagonal highway that repeats forever. Nobody put the highway in the rule.", (-1100, 560), 620, 100)
    t.tidy()
    u = UI(key, cam)
    u.inp("Steps", "Int", 11000)
    g = u.g("Geometry")
    antp, rest = sel_(u, g, "ant")
    black, white = sel_(u, rest, "black")
    squares(u, black, 0.096, 'BLACK'); squares(u, antp, 0.14, 'PINK', z=0.02)
    bd = u.n('GeometryNodeMeshGrid', u.place()); u.set(bd, Size_X=9.0, Size_Y=9.0)
    u.add(u.edges(u.transform(bd.outputs[0], (0, 0, -0.01), loc=u.place()), 0.012, 'MUTE'))
    lines = [('p', "START   a white grid, one ant"),
             ('k', "RULE    on white: turn right, paint it black, step"),
             ('k', "        on black: turn left, paint it white, step"),
             ('k', ["REPEAT  ", u.fmt(u.g("Steps"), 0), " times"]),
             ('g', "Two rules, no randomness, a highway nobody wrote.")] + tools("Repeat zone", "a loop (Anemone)")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Steps", "Steps")])


# ================================================================ 02 Noise
def s02():
    key = "02 Noise"
    sc, cam, hud = GK['make_slide'](key, 2, "RANDOM AND NOISE",
        "Random: every value is new and has nothing in common with its neighbours.\n\n"
        "Noise: values change smoothly from place to place, like terrain or clouds. A seed makes both repeatable.",
        "Switch Mode. Change Seed, then Scale.", scale=26)
    GK['aim'](cam, (0, 0, 1.0), ISO, shift=3.3)
    t = Tree(key)
    t.inp("Mode", "Menu", desc="Random or Noise"); t.inp("Seed", "Int", 0, 0, 999, "Same seed, same values")
    t.inp("Scale", "Float", 0.25, 0.02, 2.0, "Noise: features per metre")
    grid = grp(t, "Cell Grid", (-700, 200), {"Columns": 24, "Rows": 24, "Cell": 0.5})
    rv = rand(t, 'FLOAT', 0.0, 1.0, t.g("Seed"), (-700, -60))
    nv = grp(t, "Noise Value", (-700, -260), {"Seed": t.g("Seed"), "Scale": t.g("Scale")}).outputs[0]
    ms = t.menu(["Random", "Noise"], 'FLOAT', (-450, -120)); t.L(t.g("Mode"), ms.inputs['Menu'])
    t.L(rv, ms.inputs['Random']); t.L(nv, ms.inputs['Noise'])
    t.out(t.store(grid.outputs[0], "value", ms.outputs[0], 'FLOAT', loc=(-200, 100))); t.go.location = (0, 100)
    t.frame("one value per cell: random, or noise", [rv.node, nv.node, ms])
    t.tidy()
    u = UI(key, cam)
    u.inp("Mode", "Int", 0); u.inp("Seed", "Int", 0)
    cu = u.n('GeometryNodeMeshCube', u.place()); cu.inputs['Size'].default_value = (0.46, 0.46, 1.0)
    cub = u.transform(cu.outputs[0], (0, 0, 0.5), loc=u.place())
    io = u.n('GeometryNodeInstanceOnPoints', u.place()); u.L(u.g("Geometry"), io.inputs['Points']); u.L(cub, io.inputs['Instance'])
    u.L(u.xyz(1.0, 1.0, u.math('ADD', u.math('MULTIPLY', named(u, "value", 'FLOAT', u.place()), 2.0, u.place()), 0.05, u.place()), u.place()), io.inputs['Scale'])
    rz = u.n('GeometryNodeRealizeInstances', u.place()); u.L(io.outputs[0], rz.inputs[0])
    value_paint(u, rz.outputs[0], "value", 'WHITE', 'GREY')
    u.add(u.edges(rz.outputs[0], 0.006, 'BLACK', 25.0))
    M = u.g("Mode")
    lines = [('p', u.sswitch(M, ["RANDOM  every cell rolls its own dice", "NOISE   nearby cells, nearby values"])),
             ('k', u.sswitch(M, ["neighbours have nothing in common", "smooth hills and valleys"])),
             ('k', ["seed ", u.fmt(u.g("Seed"), 0), ": same seed, same result"])] + tools("Random Value, Noise Texture", "Random; noise needs a plugin")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Mode", "Mode"), ("Seed", "Seed")])


# ================================================================ 03 Threshold
def s03():
    key = "03 Threshold"
    sc, cam, hud = GK['make_slide'](key, 3, "THRESHOLD",
        "A threshold turns a field of numbers into solid and void: above it solid, below it empty.\n\n"
        "This is floor 0 of what comes next: the starting state of a rule.",
        "Move Threshold slowly. Change Scale: bigger blobs or smaller ones?", scale=30)
    GK['aim'](cam, (0, 0, 0.5), ISO, shift=3.2)
    t = Tree(key)
    t.inp("Threshold", "Float", 0.5, 0.0, 1.0, "Above this: solid"); t.inp("Seed", "Int", 0, 0, 999, "Noise seed")
    t.inp("Scale", "Float", 0.25, 0.02, 2.0, "Noise: features per metre")
    grid = grp(t, "Cell Grid", (-700, 200), {"Columns": 24, "Rows": 24, "Cell": 0.5})
    nv = grp(t, "Noise Value", (-700, -60), {"Seed": t.g("Seed"), "Scale": t.g("Scale")}).outputs[0]
    s1 = t.store(grid.outputs[0], "value", nv, 'FLOAT', loc=(-460, 160))
    t.out(t.store(s1, "solid", cmp(t, 'GREATER_THAN', nv, t.g("Threshold"), (-460, -60)), 'BOOLEAN', loc=(-260, 120))); t.go.location = (-60, 120)
    t.frame("01  noise value of every cell", [nv.node, s1.node]); t.frame("02  above Threshold: solid", [n for n in t.nt.nodes if n.bl_idname == 'FunctionNodeCompare'])
    t.tidy()
    u = UI(key, cam)
    u.inp("Threshold", "Float", 0.5)
    g = u.g("Geometry")
    u.mass(plates(u, g, "solid", 24, 24, 0.5, 0.8, (-2000, -3000)), 'WHITE')
    solid, empty = sel_(u, g, "solid")
    value_paint(u, squares(u, empty, 0.46, None), "value", 'WHITE', 'GREY')
    st = u.n('GeometryNodeAttributeStatistic', u.place()); u.L(g, st.inputs['Geometry'])
    u.L(named(u, "solid", 'FLOAT', u.place()), st.inputs['Attribute'])
    pct = u.math('MULTIPLY', st.outputs['Mean'], 100.0, u.place())
    lines = [('k', "1  read the noise value of every cell"), ('p', ["2  above ", u.fmt(u.g("Threshold"), 2), ": solid"]),
             ('k', "   below: empty"), ('k', ["solid: ", u.fmt(pct, 0), "% of the cells"])] + tools("Compare (Greater Than)", "Larger Than")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Threshold", "Threshold")])


# ================================================================ 04 One rule, one row
def s04():
    key = "04 One Rule"
    sc, cam, hud = GK['make_slide'](key, 4, "ONE RULE,\nONE ROW",
        "Stephen Wolfram's cellular automata (1983): a row of cells, each on or off. A cell and its two neighbours "
        "make one of 8 patterns; the rule number, written in binary, gives the answer for each one.",
        "Try Rule 30 (chaos), 90 (a fractal), 110 and 184. Switch Start to Random.", scale=22)
    GK['aim'](cam, (0, -2.2, 0), TOP, shift=2.9)
    t = Tree(key)
    t.inp("Rule", "Int", 30, 0, 255, "Which of the 256 rules"); t.inp("Width", "Int", 41, 5, 121, "Cells in a row")
    t.inp("Generations", "Int", 24, 1, 100, "Rows"); t.inp("Start", "Menu", desc="One cell in the middle, or random")
    t.inp("Seed", "Int", 0, 0, 999, "Random start: seed")
    W = t.g("Width")
    ix = index(t, (-1300, 0))
    pts = t.n('GeometryNodePoints', (-900, 200)); t.L(W, pts.inputs['Count'])
    t.L(t.xyz(t.math('MULTIPLY', t.math('SUBTRACT', ix, t.math('MULTIPLY', t.math('SUBTRACT', W, 1, (-1300, 160)), 0.5, (-1140, 160)), (-1100, 0)), 0.25, (-1100, -100)), 0.0, 0.0, (-1080, 60)), pts.inputs['Position'])
    one = cmp(t, 'EQUAL', ix, t.math('FLOOR', t.math('MULTIPLY', t.math('SUBTRACT', W, 1, (-1300, -260)), 0.5, (-1140, -260)), None, (-980, -260)), (-820, -220))
    rnd = rand(t, 'BOOLEAN', None, None, t.g("Seed"), (-820, -380), prob=0.5)
    ms = t.menu(["One Cell", "Random"], 'BOOLEAN', (-640, -260)); t.L(t.g("Start"), ms.inputs['Menu'])
    t.L(one, ms.inputs['One Cell']); t.L(rnd, ms.inputs['Random'])
    s0 = t.store(pts.outputs[0], "alive", ms.outputs[0], 'BOOLEAN', loc=(-640, 200))
    rin, rout = repeat(t, t.g("Generations"), s0, (-400, 200), ("Rows",))
    k = rin.outputs['Iteration']; st = rin.outputs['Geometry']
    row = t.transform(t.store(st, "generation", k, 'INT', loc=(-200, 360)), t.xyz(0.0, t.math('MULTIPLY', k, -0.25, (-200, 240)), 0.0, (-40, 240)), loc=(0, 360))
    t.L(t.joing([rin.outputs['Rows'], row], (200, 380)), rout.inputs['Rows'])
    i2 = index(t, (-200, -40)); al = named(t, "alive", 'FLOAT', (-200, -160))
    left = sample(t, st, al, t.math('SUBTRACT', i2, 1, (-40, -40)), 'FLOAT', (120, -40))
    right = sample(t, st, al, t.math('ADD', i2, 1, (-40, -260)), 'FLOAT', (120, -260))
    p = t.math('ADD', t.math('ADD', t.math('MULTIPLY', left, 4, (280, -40)), t.math('MULTIPLY', al, 2, (280, -160)), (440, -100)), right, (600, -160))
    bit = t.math('FLOORED_MODULO', t.math('FLOOR', t.math('DIVIDE', t.g("Rule"), t.math('POWER', 2.0, p, (760, -260)), (920, -200)), None, (1080, -200)), 2.0, (1240, -200))
    nxt = t.store(st, "alive", cmp(t, 'GREATER_THAN', bit, 0.5, (1400, -200)), 'BOOLEAN', loc=(1560, 0))
    t.L(nxt, rout.inputs['Geometry'])
    t.out(rout.outputs['Rows']); t.go.location = (1800, 200)
    t.frame("START  one row of cells", [pts, one.node, rnd.node, ms, s0.node])
    t.frame("RULE  left x 4 + self x 2 + right = a pattern 0..7; its bit in Rule is the answer", [i2.node, al.node, left.node, right.node, p.node, bit.node, nxt.node] + [n for n in t.nt.nodes if n.bl_idname == 'ShaderNodeMath' and n.location.x > 200])
    t.tidy()
    u = UI(key, cam)
    u.inp("Rule", "Int", 30)
    al_, dead = sel_(u, u.g("Geometry"), "alive")
    squares(u, al_, 0.23, 'BLACK'); squares(u, dead, 0.23, 'LINE')
    # rule table: 8 patterns, three cells each, the answer below
    ip = index(u, u.place())
    g8 = u.math('FLOOR', u.math('DIVIDE', ip, 4, u.place()), None, u.place()); slot = u.math('FLOORED_MODULO', ip, 4, u.place())
    pat = u.math('SUBTRACT', 7, g8, u.place()); isres = u.math('GREATER_THAN', slot, 2.5, u.place())
    btop = u.math('FLOORED_MODULO', u.math('FLOOR', u.math('DIVIDE', pat, u.math('POWER', 2.0, u.math('SUBTRACT', 2, slot, u.place()), u.place()), u.place()), None, u.place()), 2, u.place())
    bres = u.math('FLOORED_MODULO', u.math('FLOOR', u.math('DIVIDE', u.g("Rule"), u.math('POWER', 2.0, pat, u.place()), u.place()), None, u.place()), 2, u.place())
    bit_ = u.n('GeometryNodeSwitch', u.place(), input_type='FLOAT'); u.L(cmp(u, 'GREATER_THAN', isres, 0.5, u.place()), bit_.inputs['Switch'])
    u.L(btop, bit_.inputs['False']); u.L(bres, bit_.inputs['True'])
    xo = u.math('MULTIPLY', u.math('SUBTRACT', 1.0, isres, u.place()), u.math('MULTIPLY', u.math('SUBTRACT', slot, 1, u.place()), 0.3, u.place()), u.place())
    x = u.math('ADD', u.math('MULTIPLY', u.math('SUBTRACT', g8, 3.5, u.place()), 1.3, u.place()), xo, u.place())
    y = u.math('SUBTRACT', 1.7, u.math('MULTIPLY', isres, 0.36, u.place()), u.place())
    tp = u.n('GeometryNodePoints', u.place()); tp.inputs['Count'].default_value = 32; u.L(u.xyz(x, y, 0.0, u.place()), tp.inputs['Position'])
    tps = u.store(tp.outputs[0], "bit", cmp(u, 'GREATER_THAN', bit_.outputs[0], 0.5, u.place()), 'BOOLEAN', loc=u.place())
    on, off = sel_(u, tps, "bit")
    squares(u, on, 0.26, 'BLACK'); squares(u, off, 0.26, 'WHITE', outline=True)
    lines = [('p', ["RULE ", u.fmt(u.g("Rule"), 0)]), ('k', "1  read a cell and its two neighbours"),
             ('k', "2  find that pattern in the rule table"), ('k', "3  write the answer one row down")] + tools("Repeat zone, Sample Index", "a loop (Anemone)")
    u.code(lines, y=-0.9)
    u.finish()
    return done(key, sc, t, u, [("Rule", "Rule")])


# ================================================================ 05 Neighbours
def s05():
    key = "05 Neighbours"
    sc, cam, hud = GK['make_slide'](key, 5, "NEIGHBOURS",
        "A cell's neighbours are the 8 cells around it.\n\nMost 2D rules ask one question: how many of them are alive?",
        "Move Column and Row. Change Density and Seed.", scale=20)
    GK['aim'](cam, (0, 0, 0), TOP, shift=2.9)
    t = Tree(key)
    t.inp("Density", "Float", 0.35, 0.0, 1.0, "Share of alive cells"); t.inp("Seed", "Int", 0, 0, 999, "Which cells")
    t.inp("Column", "Int", 6, 0, 12, "Picked cell"); t.inp("Row", "Int", 6, 0, 12, "Picked cell")
    grid = grp(t, "Cell Grid", (-900, 200), {"Columns": 13, "Rows": 13, "Cell": 0.6})
    s1 = t.store(grid.outputs[0], "alive", rand(t, 'BOOLEAN', None, None, t.g("Seed"), (-900, -40), prob=t.g("Density")), 'BOOLEAN', loc=(-660, 200))
    cn = grp(t, "Count Neighbours", (-660, -60), {"Geometry": s1, "Columns": 13, "Rows": 13, "Name": "alive"}).outputs[0]
    s2 = t.store(s1, "neighbours", cn, 'FLOAT', loc=(-420, 200))
    pk = bmath(t, 'AND', cmp(t, 'EQUAL', named(t, "column", 'INT', (-660, -300)), t.g("Column"), (-420, -260), 'INT'),
               cmp(t, 'EQUAL', named(t, "row", 'INT', (-660, -420)), t.g("Row"), (-420, -400), 'INT'), (-240, -300))
    t.out(t.store(s2, "picked", pk, 'BOOLEAN', loc=(-180, 200))); t.go.location = (20, 200)
    t.frame("01  random alive cells", [s1.node]); t.frame("02  every cell counts its alive neighbours", [cn.node, s2.node])
    t.tidy()
    u = UI(key, cam)
    u.inp("Column", "Int", 6); u.inp("Row", "Int", 6)
    g = u.g("Geometry")
    a, d = sel_(u, g, "alive")
    squares(u, a, 0.54, 'BLACK'); squares(u, d, 0.54, 'LINE')
    ii = u.math('ADD', u.math('MULTIPLY', u.g("Column"), 13, u.place()), u.g("Row"), u.place())
    pos = sample(u, g, position(u, u.place()), ii, 'FLOAT_VECTOR', u.place())
    nb = sample(u, g, named(u, "neighbours", 'FLOAT', u.place()), ii, 'FLOAT', u.place())
    for size, color, r in ((0.6, 'PINK', 0.035), (1.8, 'CYAN', 0.03)):
        q = u.n('GeometryNodeCurvePrimitiveQuadrilateral', u.place(), mode='RECTANGLE'); u.set(q, Width=size, Height=size)
        u.add(u.transform(u.tube(q.outputs[0], r, color), u.vmath('ADD', pos, (0, 0, 0.02), u.place()), loc=u.place()))
    u.text(u.cat([u.fmt(nb, 0), " alive"]), u.vmath('ADD', pos, (0.0, 1.3, 0.05), u.place()), 0.3, 'PINK')
    lines = [('k', ["1  pick a cell: column ", u.fmt(u.g("Column"), 0), ", row ", u.fmt(u.g("Row"), 0)]),
             ('k', "2  look at the 8 cells around it"), ('p', ["3  count the alive ones: ", u.fmt(nb, 0)]),
             ('g', "Every rule from here on starts with this count.")] + tools("Sample Index, eight times", "Rabbit (cellular automata)")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Column", "Column"), ("Row", "Row")])


# ================================================================ 06 A 2D rule
def s06():
    key = "06 Game of Life"
    sc, cam, hud = GK['make_slide'](key, 6, "A 2D RULE",
        "John Conway's Game of Life (1970): every cell counts its 8 neighbours. An empty cell with exactly 3 alive "
        "neighbours is born; an alive cell with 2 or 3 survives; every other cell dies, of loneliness or crowding.\n\n"
        "Three numbers, endless behaviour.",
        "Step Generation up from 0. Change Born and Survive: does it grow, freeze or die out?", scale=22)
    GK['aim'](cam, (0, 0, 0), TOP, shift=2.9)
    t = Tree(key)
    t.inp("Generation", "Int", 12, 0, 150, "How many times the rule has run"); t.inp("Seed", "Int", 0, 0, 999, "Noise seed")
    t.inp("Threshold", "Float", 0.5, 0.0, 1.0, "Start: noise above this is alive")
    t.inp("Born", "Int", 3, 0, 8, "Born with this many"); t.inp("Survive Min", "Int", 2, 0, 8, "Survives with at least")
    t.inp("Survive Max", "Int", 3, 0, 8, "... and at most")
    grid = grp(t, "Cell Grid", (-1000, 200), {"Columns": 32, "Rows": 32, "Cell": 0.3})
    nv = grp(t, "Noise Value", (-1000, -60), {"Seed": t.g("Seed"), "Scale": 0.6}).outputs[0]
    s0 = t.store(grid.outputs[0], "alive", cmp(t, 'GREATER_THAN', nv, t.g("Threshold"), (-800, -60)), 'BOOLEAN', loc=(-620, 200))
    rin, rout = repeat(t, t.g("Generation"), s0, (-400, 200))
    lr = grp(t, "Life Rule", (-100, 200), {"Geometry": rin.outputs['Geometry'], "Columns": 32, "Rows": 32, "Born": t.g("Born"),
                                          "Survive Min": t.g("Survive Min"), "Survive Max": t.g("Survive Max")})
    t.L(lr.outputs[0], rout.inputs['Geometry'])
    t.out(rout.outputs['Geometry']); t.go.location = (1200, 200)
    t.frame("START  noise above Threshold is alive", [grid, nv.node, s0.node]); t.frame("RULE, then REPEAT", [rin, rout, lr])
    t.tidy()
    u = UI(key, cam)
    for n, d in (("Generation", 12), ("Born", 3), ("Survive Min", 2), ("Survive Max", 3)):
        u.inp(n, "Int", d)
    u.inp("Threshold", "Float", 0.5)
    g = u.g("Geometry")
    a, d = sel_(u, g, "alive")
    squares(u, a, 0.28, 'BLACK'); squares(u, d, 0.28, 'LINE')
    st = u.n('GeometryNodeAttributeStatistic', u.place()); u.L(g, st.inputs['Geometry']); u.L(named(u, "alive", 'FLOAT', u.place()), st.inputs['Attribute'])
    f = lambda n: u.fmt(u.g(n), 0)
    lines = [('k', ["START  noise above ", u.fmt(u.g("Threshold"), 2), " is alive"]),
             ('k', ["RULE   an empty cell with ", f("Born"), " alive"]), ('k', "       neighbours is born;"),
             ('k', ["       an alive cell with ", f("Survive Min"), " to ", f("Survive Max")]), ('k', "       survives; all others die."),
             ('p', ["REPEAT generation ", f("Generation"), ": ", u.fmt(st.outputs['Sum'], 0), " alive"])] + tools("Repeat zone", "Rabbit (cellular automata)")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [(n, n) for n in ("Generation", "Born", "Survive Min", "Survive Max", "Threshold")])


# ================================================================ 07 Stack
def s07():
    key = "07 Stack"
    sc, cam, hud = GK['make_slide'](key, 7, "TIME BECOMES\nHEIGHT",
        "Stack the generations: each floor is the rule applied to the floor below. A new cell is only born above "
        "4 alive cells, so the stack carries itself.",
        "Change Seed and Threshold. Try Born 3, Survive 2 to 3 (Life): the volume thins out.", scale=32)
    GK['aim'](cam, (0, 0, 4.5), ISO, shift=3.0)
    t = Tree(key)
    for n, ty, d, mn, mx, ds in (("Generations", "Int", 16, 1, 40, "Floors"), ("Seed", "Int", 3, 0, 999, "Floor 0 noise seed"),
                                 ("Threshold", "Float", 0.5, 0.0, 1.0, "Floor 0: noise above this"), ("Born", "Int", 4, 0, 8, "Born with"),
                                 ("Survive Min", "Int", 3, 0, 8, "Survives with at least"), ("Survive Max", "Int", 6, 0, 8, "... and at most"),
                                 ("Layer Height", "Float", 0.5, 0.1, 2.0, "Height of one generation")):
        t.inp(n, ty, d, mn, mx, ds)
    au = grp(t, "Automaton", (-300, 0), {n: t.g(n) for n in ("Generations", "Seed", "Threshold", "Born", "Survive Min", "Survive Max", "Layer Height")})
    t.out(au.outputs['Volume']); t.go.location = (0, 0)
    t.note("07 note - automaton", "Tab into Automaton: floor 0 from noise, then a Repeat zone that keeps each generation as a layer and applies the Life Rule.", (-700, 300), 520, 100)
    t.tidy()
    u = UI(key, cam)
    u.inp("Generations", "Int", 16); u.inp("Layer Height", "Float", 0.5)
    u.mass(u.g("Geometry"))
    G_, LH = u.g("Generations"), u.g("Layer Height")
    lines = [('k', "1  floor 0: noise above the threshold"), ('k', "2  every next floor: the rule, applied"),
             ('k', "   to the floor below"),
             ('p', ["3  ", u.fmt(G_, 0), " generations x ", u.fmt(LH, 2), " m = ", u.fmt(u.math('MULTIPLY', G_, LH, u.place()), 1), " m"])] + tools("Repeat zone, Extrude Mesh", "Rabbit, then Extrude")
    u.code(lines, y=-0.8)
    u.finish()
    return done(key, sc, t, u, [("Generations", "Generations"), ("Layer Height", "Layer Height")])


# ================================================================ 08 Environment
def s08():
    key = "08 Environment"
    sc, cam, hud = GK['make_slide'](key, 8, "THE ENVIRONMENT",
        "Generative systems respond to their surroundings. Here the attractor from Project 3 decides where cells may live.\n\n"
        "Site, sun or views could play the same role.",
        "Select the attractor (the thin sphere) and press G. Change Reach.", scale=32)
    GK['aim'](cam, (0, 0, 3.0), ISO, shift=3.0)
    at = bpy.data.objects.get("Attractor - move me")
    if not at:
        at = bpy.data.objects.new("Attractor - move me", None); at.empty_display_type = 'SPHERE'; at.empty_display_size = 0.6
    if at.name not in sc.collection.objects:
        sc.collection.objects.link(at)
    at.location = (2.0, 1.0, 0.0)
    t = Tree(key)
    t.inp("Attractor", "Object", desc="Cells may only live near it")
    t.inp("Reach", "Float", 4.0, 0.5, 12.0, "How far from the attractor cells may live")
    t.inp("Seed", "Int", 3, 0, 999, "Floor 0 noise seed"); t.inp("Threshold", "Float", 0.45, 0.0, 1.0, "Floor 0 threshold")
    t.inp("Generations", "Int", 16, 1, 40, "Floors")
    oi = t.n('GeometryNodeObjectInfo', (-600, -100), transform_space='ORIGINAL'); t.L(t.g("Attractor"), oi.inputs['Object'])
    au = grp(t, "Automaton", (-300, 0), {"Seed": t.g("Seed"), "Threshold": t.g("Threshold"), "Generations": t.g("Generations"),
                                        "Center": oi.outputs['Location'], "Reach": t.g("Reach")})
    t.out(au.outputs['Volume']); t.go.location = (0, 0)
    t.frame("the environment: the attractor's position and Reach", [oi])
    t.tidy()
    u = UI(key, cam)
    u.inp("Attractor", "Object"); u.inp("Reach", "Float", 4.0)
    u.mass(u.g("Geometry"))
    oi2 = u.n('GeometryNodeObjectInfo', u.place(), transform_space='ORIGINAL'); u.L(u.g("Attractor"), oi2.inputs['Object'])
    sp = u.n('GeometryNodeMeshUVSphere', u.place()); u.set(sp, Radius=0.3)
    u.add(u.paint(u.transform(sp.outputs[0], oi2.outputs['Location'], loc=u.place()), 'PINK'))
    ci = u.n('GeometryNodeCurvePrimitiveCircle', u.place(), mode='RADIUS'); ci.inputs['Resolution'].default_value = 64; u.L(u.g("Reach"), S(ci, 'Radius'))
    u.add(u.transform(u.tube(ci.outputs['Curve'], 0.04, 'CYAN'), u.vmath('MULTIPLY', oi2.outputs['Location'], (1.0, 1.0, 0.0), u.place()), loc=u.place()))
    lines = [('k', "1  the same rule as before"), ('p', ["2  only within ", u.fmt(u.g("Reach")), " m of the attractor"]),
             ('p', "   can a cell live"), ('k', "Move the attractor: the volume grows"), ('k', "where the environment allows.")] + tools("Object Info, then a distance test", "Distance, then Smaller Than")
    u.code(lines)
    u.finish()

    def extra(ob):
        GK['set_in'](ob, "Attractor", at); GK['set_in'](ob, "Attractor", at, "UI")
    return done(key, sc, t, u, [("Reach", "Reach")], extra)


# ================================================================ 09 Agents
def s09():
    key = "09 Agents"
    sc, cam, hud = GK['make_slide'](key, 9, "AGENTS",
        "Agents are simple walkers with local rules: turn a little, walk, leave a trail. Together they draw paths nobody planned.\n\n"
        "Turn on Height and time becomes height again.",
        "Raise Steer to follow the noise field. Turn on Height.", scale=19)
    GK['aim'](cam, (0, 0, 1.5), ISO, shift=2.8)
    t = Tree(key)
    t.inp("Agents", "Int", 40, 1, 300, "How many walkers"); t.inp("Steps", "Int", 120, 1, 400, "How many steps")
    t.inp("Turn", "Float", 25.0, 0.0, 120.0, "Largest random turn per step (degrees)")
    t.inp("Steer", "Float", 0.0, 0.0, 1.0, "How much they follow the noise field"); t.inp("Seed", "Int", 0, 0, 999, "Randomness")
    t.inp("Height", "Bool", False, desc="Time becomes height")
    rv = rand(t, 'FLOAT_VECTOR', (-4.0, -4.0, 0.0), (4.0, 4.0, 0.0), t.g("Seed"), (-1600, 200))
    pts = t.n('GeometryNodePoints', (-1400, 200)); t.L(t.g("Agents"), pts.inputs['Count']); t.L(rv, pts.inputs['Position'])
    s0 = t.store(t.store(pts.outputs[0], "id", index(t, (-1400, 0)), 'INT', loc=(-1200, 200)), "heading",
                 rand(t, 'FLOAT', 0.0, 2 * math.pi, t.math('ADD', t.g("Seed"), 1, (-1400, -120)), (-1200, -40)), 'FLOAT', loc=(-1020, 200))
    rin, rout = repeat(t, t.g("Steps"), s0, (-800, 200), ("Trail",))
    k = rin.outputs['Iteration']; st = rin.outputs['Geometry']
    rise = t.n('GeometryNodeSwitch', (-700, 440), input_type='FLOAT'); t.L(t.g("Height"), rise.inputs['Switch']); rise.inputs['True'].default_value = 0.05
    tr = t.n('GeometryNodeSetPosition', (-400, 480)); t.L(t.store(st, "step", k, 'INT', loc=(-560, 480)), tr.inputs['Geometry'])
    t.L(t.xyz(0.0, 0.0, t.math('MULTIPLY', rise.outputs[0], k, (-560, 360)), (-480, 360)), tr.inputs['Offset'])
    t.L(t.joing([rin.outputs['Trail'], tr.outputs[0]], (-200, 480)), rout.inputs['Trail'])
    tmax = t.math('RADIANS', t.g("Turn"), None, (-700, 0))
    turn = rand(t, 'FLOAT', t.math('MULTIPLY', tmax, -1, (-560, 0)), tmax, t.math('ADD', t.g("Seed"), 2, (-700, -120)), (-400, 0),
                ident=t.math('ADD', t.math('MULTIPLY', named(t, "id", 'FLOAT', (-700, -240)), 7919, (-560, -240)), k, (-400, -240)))
    nang = t.math('MULTIPLY', grp(t, "Noise Value", (-700, -400), {"Seed": t.g("Seed"), "Scale": 0.2}).outputs[0], 4 * math.pi, (-560, -400))
    h1 = t.math('ADD', named(t, "heading", 'FLOAT', (-400, -120)), turn, (-240, -60))
    hs = t.math('ADD', h1, t.math('MULTIPLY', t.g("Steer"), t.math('SUBTRACT', nang, h1, (-240, -320)), (-80, -320)), (80, -120))
    pp = t.sep(position(t, (-400, -560)), (-240, -560))
    out_ = t.math('GREATER_THAN', t.vmath('LENGTH', t.vmath('MULTIPLY', position(t, (-400, -700)), (1.0, 1.0, 0.0), (-240, -700)), None, (-80, -700), out=1), 4.5, (80, -700))
    home = t.math('ADD', t.math('ARCTAN2', t.math('MULTIPLY', pp[1], -1, (-80, -520)), t.math('MULTIPLY', pp[0], -1, (-80, -600)), (80, -560)), turn, (240, -560))
    hsw = t.n('GeometryNodeSwitch', (240, -200), input_type='FLOAT'); t.L(cmp(t, 'GREATER_THAN', out_, 0.5, (240, -700)), hsw.inputs['Switch'])
    t.L(hs, hsw.inputs['False']); t.L(home, hsw.inputs['True'])
    s1 = t.store(st, "heading", hsw.outputs[0], 'FLOAT', loc=(420, 200))
    hn = named(t, "heading", 'FLOAT', (420, -60))
    mv = t.n('GeometryNodeSetPosition', (620, 200)); t.L(s1, mv.inputs['Geometry'])
    t.L(t.xyz(t.math('MULTIPLY', t.math('COSINE', hn, None, (420, -180)), 0.12, (560, -180)), t.math('MULTIPLY', t.math('SINE', hn, None, (420, -300)), 0.12, (560, -300)), 0.0, (700, -240)), mv.inputs['Offset'])
    t.L(mv.outputs[0], rout.inputs['Geometry'])
    pc = t.n('GeometryNodePointsToCurves', (800, 400)); t.L(rout.outputs['Trail'], pc.inputs['Points'])
    t.L(named(t, "id", 'INT', (600, 560)), pc.inputs['Curve Group ID']); t.L(named(t, "step", 'FLOAT', (600, 660)), pc.inputs['Weight'])
    heads = t.n('GeometryNodeSetPosition', (800, 200)); t.L(rout.outputs['Geometry'], heads.inputs['Geometry'])
    t.L(t.xyz(0.0, 0.0, t.math('MULTIPLY', rise.outputs[0], t.g("Steps"), (640, 100)), (720, 100)), heads.inputs['Offset'])
    t.out(t.joing([pc.outputs[0], heads.outputs[0]], (1000, 300))); t.go.location = (1200, 300)
    t.frame("START  walkers at random, each with a heading", [rv.node, pts, s0.node])
    t.frame("each step: leave a trail point, turn a little (and follow the field), walk; turn home at the edge", [rin, rout, rise, tr, turn.node, nang.node, h1.node, hs.node, hsw, s1.node, mv])
    t.frame("trails: connect each walker's points in order", [pc, heads])
    t.tidy()
    u = UI(key, cam)
    for n, ty, d in (("Agents", "Int", 40), ("Steps", "Int", 120), ("Turn", "Float", 25.0), ("Steer", "Float", 0.0)):
        u.inp(n, ty, d)
    scp = u.n('GeometryNodeSeparateComponents', u.place()); u.L(u.g("Geometry"), scp.inputs[0])
    u.add(u.tube(scp.outputs['Curve'], 0.014, 'BLACK', 5))
    dot = u.n('GeometryNodeMeshUVSphere', u.place()); u.set(dot, Segments=12, Rings=6, Radius=0.07)
    io = u.n('GeometryNodeInstanceOnPoints', u.place()); u.L(scp.outputs['Point Cloud'], io.inputs['Points']); u.L(dot.outputs[0], io.inputs['Instance'])
    rz = u.n('GeometryNodeRealizeInstances', u.place()); u.L(io.outputs[0], rz.inputs[0]); u.add(u.paint(rz.outputs[0], 'PINK'))
    ci = u.n('GeometryNodeCurvePrimitiveCircle', u.place(), mode='RADIUS'); ci.inputs['Resolution'].default_value = 64; S(ci, 'Radius').default_value = 4.5
    u.add(u.tube(ci.outputs['Curve'], 0.015, 'MUTE'))
    lines = [('k', ["1  start ", u.fmt(u.g("Agents"), 0), " walkers at random"]), ('k', ["2  each step: turn up to ", u.fmt(u.g("Turn"), 0), "°,"]),
             ('k', ["   follow the field ", u.fmt(u.math('MULTIPLY', u.g("Steer"), 100, u.place()), 0), "%, walk"]),
             ('k', "3  leave a trail"), ('p', ["4  repeat ", u.fmt(u.g("Steps"), 0), " steps"])] + tools("Repeat zone", "Culebra (agents)")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [(n, n) for n in ("Agents", "Steps", "Turn", "Steer")])


# ================================================================ 10 Reaction-diffusion
FEED = (0.04, 0.029, 0.0545, 0.03)
KILL = (0.065, 0.057, 0.062, 0.06)
PATTERNS = ["Spots", "Maze", "Coral", "Worms"]


def s11():
    key = "11 Reaction Diffusion"
    sc, cam, hud = GK['make_slide'](key, 10, "REACTION AND\nDIFFUSION",
        "Two substances spread and react (Alan Turing, 1952). Small changes in feed and removal give spots, stripes or mazes.",
        "Switch Pattern. Lower Steps to watch the pattern form.", scale=17)
    GK['aim'](cam, (0, 0, 0), TOP, shift=2.9)
    t = Tree(key)
    t.inp("Pattern", "Menu", desc="Feed and removal rates"); t.inp("Steps", "Int", 2000, 0, 6000, "How many times the rule runs")
    t.inp("Seed", "Int", 0, 0, 999, "Where B starts")
    gr = t.n('GeometryNodeMeshGrid', (-1400, 300)); t.set(gr, Size_X=9.0, Size_Y=9.0, Vertices_X=120, Vertices_Y=120)
    pm = t.menu(PATTERNS, 'INT', (-1400, 0)); t.L(t.g("Pattern"), pm.inputs['Menu'])
    for i, nm in enumerate(PATTERNS):
        pm.inputs[nm].default_value = i
    fsw = t.iswitch('FLOAT', 4, (-1200, 0)); ksw = t.iswitch('FLOAT', 4, (-1200, -200))
    for sw, vals in ((fsw, FEED), (ksw, KILL)):
        t.L(pm.outputs[0], sw.inputs['Index'])
        for i, v in enumerate(vals):
            sw.inputs[i + 1].default_value = v
    f, k = fsw.outputs[0], ksw.outputs[0]
    nv = grp(t, "Noise Value", (-1400, -400), {"Seed": t.g("Seed"), "Scale": 1.2}).outputs[0]
    b0 = t.n('GeometryNodeSwitch', (-1200, -400), input_type='FLOAT'); t.L(cmp(t, 'GREATER_THAN', nv, 0.72, (-1200, -560)), b0.inputs['Switch'])
    b0.inputs['True'].default_value = 1.0
    s0 = t.store(t.store(gr.outputs[0], "A", 1.0, 'FLOAT', loc=(-1000, 300)), "B", b0.outputs[0], 'FLOAT', loc=(-820, 300))
    rin, rout = repeat(t, t.g("Steps"), s0, (-600, 300))
    st = rin.outputs['Geometry']
    A = named(t, "A", 'FLOAT', (-500, 100)); B = named(t, "B", 'FLOAT', (-500, -100))

    def lap(v, y):
        bl = t.n('GeometryNodeBlurAttribute', (-340, y), data_type='FLOAT'); t.L(v, bl.inputs['Value'])
        bl.inputs['Iterations'].default_value = 1; bl.inputs['Weight'].default_value = 1.0
        return t.math('MULTIPLY', t.math('SUBTRACT', bl.outputs[0], v, (-180, y)), 1.0, (-20, y))
    la, lb = lap(A, 100), lap(B, -100)
    r = t.math('MULTIPLY', t.math('MULTIPLY', A, B, (-340, -300)), B, (-180, -300))
    an = t.math('ADD', A, t.math('ADD', t.math('SUBTRACT', la, r, (140, 60)), t.math('MULTIPLY', f, t.math('SUBTRACT', 1.0, A, (-20, 220)), (140, 220)), (300, 120)), (460, 120))
    bn = t.math('ADD', B, t.math('SUBTRACT', t.math('ADD', t.math('MULTIPLY', lb, 0.5, (140, -100)), r, (300, -160)),
                                 t.math('MULTIPLY', t.math('ADD', k, f, (140, -420)), B, (300, -380)), (460, -260)), (620, -200))
    for s_ in (an, bn):
        s_.node.use_clamp = True
    s1 = t.store(st, "A next", an, 'FLOAT', loc=(800, 300)); s2 = t.store(s1, "B", bn, 'FLOAT', loc=(980, 300))
    s3 = t.store(s2, "A", named(t, "A next", 'FLOAT', (980, 140)), 'FLOAT', loc=(1160, 300))
    t.L(s3, rout.inputs['Geometry'])
    t.out(rout.outputs['Geometry']); t.go.location = (1300, 300)
    t.frame("START  A everywhere, B in a few noise spots", [gr, nv.node, b0, s0.node])
    t.frame("feed and removal rates", [pm, fsw, ksw])
    t.frame("RULE  both spread (blur), B grows where it meets A, A is fed, B is removed.  REPEAT", [rin, rout, s1.node, s2.node, s3.node, r.node, an.node, bn.node, la.node, lb.node] + [n for n in t.nt.nodes if n.bl_idname == 'GeometryNodeBlurAttribute'])
    t.note("11 note - gray scott", "Gray-Scott model: A' = A + spread(A) - A x B x B + feed x (1 - A);  B' = B + spread(B)/2 + A x B x B - (removal + feed) x B.", (-1400, 700), 640, 100)
    t.tidy()
    u = UI(key, cam)
    u.inp("Pattern", "Int", 0); u.inp("Steps", "Int", 2000)
    value_paint(u, u.g("Geometry"), "B", 'WHITE', 'BLACK', 4.0)
    fs = u.iswitch('FLOAT', 4, u.place()); ks = u.iswitch('FLOAT', 4, u.place())
    for sw, vals in ((fs, FEED), (ks, KILL)):
        u.L(u.g("Pattern"), sw.inputs['Index'])
        for i, v in enumerate(vals):
            sw.inputs[i + 1].default_value = v
    lines = [('k', "A feeds the grid, B eats A"), ('k', "1  both spread to their neighbours"), ('k', "2  where they meet, B grows"),
             ('k', ["   feed ", u.fmt(fs.outputs[0], 4), ", removal ", u.fmt(ks.outputs[0], 4)]),
             ('p', ["3  repeat ", u.fmt(u.g("Steps"), 0), " steps"])] + tools("Repeat zone, Blur Attribute", "a loop (Anemone)")
    u.code(lines, y=-0.75)
    u.finish()
    return done(key, sc, t, u, [("Pattern", "Pattern"), ("Steps", "Steps")])


# ================================================================ 11 Growth
def s12():
    key = "12 Growth"
    sc, cam, hud = GK['make_slide'](key, 11, "GROWTH",
        "Growth rules add material at the edge of what already exists. A cell joins only when exactly one of its four "
        "sides touches a grown cell, so the tips keep growing: branches, like coral or frost.",
        "Change Chance and Seed. Turn on Height: time becomes height again.", scale=26)
    GK['aim'](cam, (0, 0, 1.0), ISO, shift=3.1)
    t = Tree(key)
    t.inp("Steps", "Int", 70, 0, 250, "How many times the rule runs"); t.inp("Chance", "Float", 0.3, 0.0, 1.0, "How likely a touching cell joins")
    t.inp("Seed", "Int", 0, 0, 999, "Luck"); t.inp("Height", "Bool", False, desc="Time becomes height")
    grid = grp(t, "Cell Grid", (-1200, 200), {"Columns": 61, "Rows": 61, "Cell": 0.16})
    s0 = t.store(t.store(grid.outputs[0], "grown", cmp(t, 'EQUAL', index(t, (-1200, -40)), 1860, (-1040, -40), 'INT'), 'BOOLEAN', loc=(-1000, 200)),
                 "born", 0, 'INT', loc=(-820, 200))
    rin, rout = repeat(t, t.g("Steps"), s0, (-600, 200))
    st = rin.outputs['Geometry']; k = rin.outputs['Iteration']
    n = None
    for q, (dx, dy) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
        nb = grp(t, "Neighbour", (-560, 120 - 110 * q), {"Geometry": st, "Columns": 61, "Rows": 61, "Name": "grown", "DX": dx, "DY": dy}).outputs[0]
        n = nb if n is None else t.math('ADD', n, nb, (-400, 120 - 110 * q))
    gw = named(t, "grown", 'BOOLEAN', (-400, -200))
    luck = cmp(t, 'LESS_THAN', rand(t, 'FLOAT', 0.0, 1.0, t.g("Seed"), (-400, -360),
                                    ident=t.math('ADD', index(t, (-560, -400)), t.math('MULTIPLY', k, 10007, (-560, -480)), (-400, -480))), t.g("Chance"), (-200, -360))
    join_ = bmath(t, 'AND', bmath(t, 'AND', bmath(t, 'NOT', gw, None, (-200, -200)), cmp(t, 'EQUAL', n, 1.0, (-200, -60)), (-20, -120)), luck, (160, -200))
    bsw = t.n('GeometryNodeSwitch', (160, 0), input_type='INT'); t.L(join_, bsw.inputs['Switch'])
    t.L(named(t, "born", 'INT', (0, 60)), bsw.inputs['False']); t.L(t.math('ADD', k, 1, (0, -20)), bsw.inputs['True'])
    s1 = t.store(st, "born", bsw.outputs[0], 'INT', loc=(340, 200)); s2 = t.store(s1, "grown", bmath(t, 'OR', gw, join_, (340, -60)), 'BOOLEAN', loc=(520, 200))
    t.L(s2, rout.inputs['Geometry'])
    dl = t.n('GeometryNodeDeleteGeometry', (900, 200), domain='POINT'); t.L(rout.outputs['Geometry'], dl.inputs['Geometry'])
    t.L(bmath(t, 'NOT', named(t, "grown", 'BOOLEAN', (720, 60)), None, (900, 60)), dl.inputs['Selection'])
    hz = t.n('GeometryNodeSwitch', (900, -100), input_type='FLOAT'); t.L(t.g("Height"), hz.inputs['Switch']); hz.inputs['True'].default_value = 0.05
    sp = t.n('GeometryNodeSetPosition', (1080, 200)); t.L(dl.outputs[0], sp.inputs['Geometry'])
    t.L(t.xyz(0.0, 0.0, t.math('MULTIPLY', named(t, "born", 'FLOAT', (900, -240)), hz.outputs[0], (1080, -200)), (1080, -60)), sp.inputs['Offset'])
    t.out(sp.outputs[0]); t.go.location = (1280, 200)
    t.frame("START  one grown cell in the middle", [grid, s0.node])
    t.frame("RULE  an empty cell touching a grown cell on exactly one side joins, with some luck.  REPEAT", [rin, rout, n.node, join_.node, bsw, s1.node, s2.node, luck.node])
    t.frame("keep the grown cells; Height lifts each by when it joined", [dl, hz, sp])
    t.tidy()
    u = UI(key, cam)
    u.inp("Steps", "Int", 70); u.inp("Chance", "Float", 0.3)
    cu = u.n('GeometryNodeMeshCube', u.place()); cu.inputs['Size'].default_value = (0.15, 0.15, 0.06)
    io = u.n('GeometryNodeInstanceOnPoints', u.place()); u.L(u.g("Geometry"), io.inputs['Points']); u.L(cu.outputs[0], io.inputs['Instance'])
    rz = u.n('GeometryNodeRealizeInstances', u.place()); u.L(io.outputs[0], rz.inputs[0])
    value_paint(u, rz.outputs[0], "born", 'BLACK', 'PINK', u.math('DIVIDE', 1.0, u.math('MAXIMUM', u.g("Steps"), 1, u.place()), u.place()))
    gp = u.n('GeometryNodeMeshGrid', u.place()); u.set(gp, Size_X=9.8, Size_Y=9.8)
    u.add(u.edges(u.transform(gp.outputs[0], (0, 0, -0.04), loc=u.place()), 0.015, 'MUTE'))
    lines = [('k', "1  start with one grown cell"), ('k', "2  an empty cell joins when it touches"),
             ('k', ["   on exactly one side, ", u.fmt(u.math('MULTIPLY', u.g("Chance"), 100, u.place()), 0), "% of the time"]),
             ('p', ["3  repeat ", u.fmt(u.g("Steps"), 0), " steps"]), ('g', "Older cells black, newer cells pink.")] + tools("Repeat zone", "a loop (Anemone)")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [("Steps", "Steps"), ("Chance", "Chance")])


# ================================================================ 12 Reading a layer
def s15():
    key = "15 Reading"
    sc, cam, hud = GK['make_slide'](key, 12, "READING\nA LAYER",
        "Generative results have to be read. Slice a layer and ask architectural questions: is there a floor to stand on, "
        "room to move, room above your head?",
        "Move Layer up and down. Change Clearance and Headroom.", scale=32)
    GK['aim'](cam, (0, 0, 3.5), ISO, shift=3.0)
    t = Tree(key)
    t.inp("Layer", "Int", 1, 0, 15, "Which generation to read"); t.inp("Clearance", "Float", 1.0, 0.25, 5.0, "Distance to the nearest wall (m)")
    t.inp("Headroom", "Float", 2.0, 0.5, 6.0, "Empty height needed above (m)"); t.inp("Seed", "Int", 3, 0, 999, "Floor 0 noise seed")
    t.inp("Threshold", "Float", 0.5, 0.0, 1.0, "Floor 0 threshold")
    au = grp(t, "Automaton", (-1400, 200), {"Seed": t.g("Seed"), "Threshold": t.g("Threshold"), "Generations": 16})
    cells = au.outputs['Cells']
    dl = t.n('GeometryNodeDeleteGeometry', (-1100, 200), domain='POINT'); t.L(cells, dl.inputs['Geometry'])
    t.L(cmp(t, 'NOT_EQUAL', named(t, "generation", 'INT', (-1300, -40)), t.g("Layer"), (-1100, -40), 'INT'), dl.inputs['Selection'])
    plan = dl.outputs[0]
    walls, _ = t.n('GeometryNodeSeparateGeometry', (-900, 0)), None
    t.L(plan, walls.inputs['Geometry']); t.L(named(t, "alive", 'BOOLEAN', (-1100, -160)), walls.inputs['Selection'])
    px = t.n('GeometryNodeProximity', (-700, 0)); px.target_element = 'POINTS'; t.L(walls.outputs['Selection'], px.inputs['Target'])
    s1 = t.store(plan, "clearance", px.outputs['Distance'], 'FLOAT', loc=(-500, 200))
    hl = t.math('CEIL', t.math('DIVIDE', t.g("Headroom"), 0.5, (-700, -300)), None, (-540, -300))
    s1b = t.store(s1, "blocked", 0.0, 'FLOAT', loc=(-340, 200))
    rin, rout = repeat(t, hl, s1b, (-200, 200))
    j = rin.outputs['Iteration']
    up = t.math('ADD', t.math('MULTIPLY', t.math('ADD', t.math('ADD', t.g("Layer"), j, (0, -60)), 1, (160, -60)), 576, (320, -60)), index(t, (160, -180)), (480, -100))
    a_up = sample(t, cells, named(t, "alive", 'FLOAT', (320, -300)), up, 'FLOAT', (640, -100))
    t.L(t.store(rin.outputs['Geometry'], "blocked", t.math('ADD', named(t, "blocked", 'FLOAT', (640, 60)), a_up, (800, 0)), 'FLOAT', loc=(960, 200)), rout.inputs['Geometry'])
    flo = sample(t, cells, named(t, "alive", 'FLOAT', (1100, -500)), t.math('ADD', t.math('MULTIPLY', t.math('SUBTRACT', t.g("Layer"), 1, (940, -560)), 576, (1100, -620)), index(t, (940, -680)), (1260, -600)), 'FLOAT', (1300, -500))
    floor_ok = bmath(t, 'OR', cmp(t, 'GREATER_THAN', flo, 0.5, (1460, -500)), cmp(t, 'EQUAL', t.g("Layer"), 0, (1460, -620), 'INT'), (1620, -560))
    room0 = bmath(t, 'AND', bmath(t, 'AND', bmath(t, 'NOT', named(t, "alive", 'BOOLEAN', (1300, -40)), None, (1460, -40)),
                                 cmp(t, 'GREATER_EQUAL', named(t, "clearance", 'FLOAT', (1300, -160)), t.g("Clearance"), (1460, -160)), (1620, -100)),
                 cmp(t, 'LESS_THAN', named(t, "blocked", 'FLOAT', (1300, -300)), 0.5, (1460, -300)), (1780, -160))
    room = bmath(t, 'AND', room0, floor_ok, (1880, -300))
    s3 = t.store(rout.outputs['Geometry'], "room", room, 'BOOLEAN', loc=(1940, 200))
    t.out(t.joing([au.outputs['Volume'], s3], (2120, 100))); t.go.location = (2300, 100)
    t.frame("01  the automaton and one layer of its cells", [au, dl])
    t.frame("02  clearance: distance from each cell to the nearest wall", [walls, px, s1.node])
    t.frame("03  headroom: count the alive cells in the layers above", [hl.node, s1b.node, rin, rout, up.node, a_up.node])
    t.frame("04  a room fits: empty, a floor below, far enough from walls, open above", [room0.node, room.node, s3.node, flo.node, floor_ok.node])
    t.tidy()
    u = UI(key, cam)
    u.inp("Layer", "Int", 1); u.inp("Clearance", "Float", 1.0); u.inp("Headroom", "Float", 2.0)
    scp = u.n('GeometryNodeSeparateComponents', u.place()); u.L(u.g("Geometry"), scp.inputs[0])
    vol = scp.outputs['Mesh']; pl = scp.outputs['Point Cloud']
    below, above = u.split(vol, cmp(u, 'LESS_THAN', named(u, "generation", 'INT', u.place()), u.g("Layer"), u.place(), 'INT'))
    u.mass(below); u.ghost(above, 'MUTE', 0.01)
    rm, rest = sel_(u, pl, "room")
    al, emp = sel_(u, rest, "alive")
    squares(u, rm, 0.48, 'PINK', z=0.03); squares(u, al, 0.48, 'BLACK', z=0.03); squares(u, emp, 0.48, 'LINE', z=0.03)
    stt = u.n('GeometryNodeAttributeStatistic', u.place()); u.L(pl, stt.inputs['Geometry']); u.L(named(u, "room", 'FLOAT', u.place()), stt.inputs['Attribute'])
    area = u.math('MULTIPLY', stt.outputs['Sum'], 0.25, u.place())
    L_ = u.g("Layer")
    lines = [('p', ["LAYER ", u.fmt(L_, 0), " at ", u.fmt(u.math('MULTIPLY', L_, 0.5, u.place()), 1), " m"]),
             ('k', "floor: solid cells right below"),
             ('k', ["clearance: walls at least ", u.fmt(u.g("Clearance"), 1), " m away"]),
             ('k', ["headroom: ", u.fmt(u.g("Headroom"), 1), " m empty above"]),
             ('p', ["pink: room for a space, ", u.fmt(area, 0), " m²"])] + tools("Geometry Proximity, Sample Index", "Mesh Closest Point")
    u.code(lines, y=-0.8)
    u.finish()
    return done(key, sc, t, u, [("Layer", "Layer"), ("Clearance", "Clearance"), ("Headroom", "Headroom")])


# ================================================================ 13 Design space / 14 Breed
def foreach_automata(t, pts, items, loc, gens, extra_store=()):
    """For Each point: run the Automaton with the point's values, move the volume to the point."""
    fi = t.n('GeometryNodeForeachGeometryElementInput', loc); fo = t.n('GeometryNodeForeachGeometryElementOutput', (loc[0] + 900, loc[1]))
    fi.pair_with_output(fo)
    for name, dtype in items:
        fo.input_items.new(dtype, name)
    t.L(pts, fi.inputs['Geometry'])
    for name, dtype in items:
        t.L(named(t, name.lower(), {'FLOAT': 'FLOAT', 'INT': 'INT', 'BOOLEAN': 'BOOLEAN', 'VECTOR': 'FLOAT_VECTOR'}[dtype], (loc[0] - 200, loc[1] - 120 * items.index((name, dtype)))) if name != "Position" else position(t, (loc[0] - 200, loc[1] - 600)),
            fi.inputs[name])
    v = {"Seed": fi.outputs['Seed'], "Threshold": fi.outputs['Threshold'], "Generations": gens, "Columns": 16, "Rows": 16, "Cell": 0.75, "Layer Height": 0.75}
    if any(n == "Scale" for n, _ in items):
        v["Scale"] = fi.outputs['Scale']
    au = grp(t, "Automaton", (loc[0] + 200, loc[1]), v)
    g = au.outputs['Volume']
    for name in extra_store:
        g = t.store(g, name.lower(), fi.outputs[name], 'BOOLEAN', loc=(loc[0] + 450, loc[1]))
    g = t.transform(g, fi.outputs['Position'], loc=(loc[0] + 650, loc[1]))
    t.L(g, fo.inputs[1])
    return fo.outputs[2], [fi, fo, au]


TOWARD = (0.57735 * 40, 0.57735 * 40, 0.57735 * 40)   # pulls labels toward the camera so volumes never hide them


def s16():
    key = "16 Design Space"
    S_ = 18.0; SR = 28.0
    sc, cam, hud = GK['make_slide'](key, 13, "DESIGN SPACE",
        "One run is one answer. A matrix runs the rule 25 times while two inputs change, so you can compare and choose.\n\n"
        "It maps part of a space you have not mapped.",
        "Change the threshold range and Seed. Pick a column and a row.", scale=175)
    GK['aim'](cam, (0, 0, 4.0), ISO, shift=3.5, lift=-0.3, dist=200)
    t = Tree(key)
    t.inp("Threshold From", "Float", 0.40, 0.0, 1.0, "Column 1"); t.inp("Threshold To", "Float", 0.60, 0.0, 1.0, "Column 5")
    t.inp("Seed", "Int", 0, 0, 999, "Row 1; rows 2 to 5 add 1 each"); t.inp("Generations", "Int", 12, 1, 30, "Floors")
    t.inp("Pick Column", "Int", 2, 0, 4, "Your choice"); t.inp("Pick Row", "Int", 2, 0, 4, "Your choice")
    ix = index(t, (-1600, 0))
    c = t.math('FLOOR', t.math('DIVIDE', ix, 5, (-1440, 60)), None, (-1280, 60)); r = t.math('FLOORED_MODULO', ix, 5, (-1440, -80))
    pos = t.vmath('ADD', t.vmath('SCALE', RIGHT, t.math('MULTIPLY', t.math('SUBTRACT', c, 2, (-1280, 200)), S_, (-1120, 200)), (-960, 200)),
                  t.vmath('SCALE', DOWN, t.math('MULTIPLY', t.math('SUBTRACT', r, 2, (-1280, -200)), SR, (-1120, -200)), (-960, -200)), (-800, 0))
    pts = t.n('GeometryNodePoints', (-640, 300)); pts.inputs['Count'].default_value = 25; t.L(pos, pts.inputs['Position'])
    thr = t.n('ShaderNodeMapRange', (-800, -400)); t.L(c, thr.inputs[0]); thr.inputs[1].default_value = 0; thr.inputs[2].default_value = 4
    t.L(t.g("Threshold From"), thr.inputs[3]); t.L(t.g("Threshold To"), thr.inputs[4])
    pk = bmath(t, 'AND', cmp(t, 'EQUAL', c, t.g("Pick Column"), (-800, -600)), cmp(t, 'EQUAL', r, t.g("Pick Row"), (-800, -720)), (-640, -660))
    s = t.store(t.store(t.store(pts.outputs[0], "threshold", thr.outputs[0], 'FLOAT', loc=(-480, 300)), "seed",
                        t.math('ADD', t.g("Seed"), r, (-640, -520)), 'INT', loc=(-320, 300)), "picked", pk, 'BOOLEAN', loc=(-160, 300))
    out, nodes = foreach_automata(t, s, [("Threshold", 'FLOAT'), ("Seed", 'INT'), ("Picked", 'BOOLEAN'), ("Position", 'VECTOR')], (200, 300), t.g("Generations"), ("Picked",))
    t.out(out); t.go.location = (1400, 300)
    t.frame("25 runs: columns change Threshold, rows change Seed", [pts, thr, s.node, pk.node])
    t.frame("for each run: the automaton with that run's values", nodes)
    t.tidy()
    u = UI(key, cam)
    for n, ty, d in (("Threshold From", "Float", 0.4), ("Threshold To", "Float", 0.6), ("Seed", "Int", 0), ("Pick Column", "Int", 2), ("Pick Row", "Int", 2)):
        u.inp(n, ty, d)
    pkd, rest = sel_(u, u.g("Geometry"), "picked")
    u.mass(rest, 'WHITE', 0.05); u.mass(pkd, 'PINK', 0.05)
    tf, tt = u.g("Threshold From"), u.g("Threshold To")
    for i in range(5):
        th = u.math('ADD', tf, u.math('MULTIPLY', u.math('SUBTRACT', tt, tf, u.place()), i / 4, u.place()), u.place())
        p = tuple(RIGHT[a] * (i - 2) * S_ + DOWN[a] * (-2.6) * SR + TOWARD[a] for a in range(3))
        u.text(u.cat(["threshold ", u.fmt(th, 2)]), p, 0.22, 'GREY')
        q = tuple(RIGHT[a] * (-2.75) * S_ + DOWN[a] * (i - 2) * SR + TOWARD[a] for a in range(3))
        u.text(u.cat(["seed ", u.fmt(u.math('ADD', u.g("Seed"), i, u.place()), 0)]), q, 0.22, 'GREY')
    lines = [('k', ["columns: threshold ", u.fmt(tf, 2), " to ", u.fmt(tt, 2)]),
             ('k', ["rows: seed ", u.fmt(u.g("Seed"), 0), " to ", u.fmt(u.math('ADD', u.g("Seed"), 4, u.place()), 0)]),
             ('k', "same rule, 25 runs:"), ('k', "answers you did not anticipate"),
             ('p', ["picked: column ", u.fmt(u.math('ADD', u.g("Pick Column"), 1, u.place()), 0), ", row ", u.fmt(u.math('ADD', u.g("Pick Row"), 1, u.place()), 0)])] + tools("For Each zone", "a series of values, one per run")
    u.code(lines)
    u.finish()
    return done(key, sc, t, u, [(n, n) for n in ("Threshold From", "Threshold To", "Seed", "Pick Column", "Pick Row")])


def s17():
    key = "17 Breed"
    S_ = 18.0; SR = 28.0
    sc, cam, hud = GK['make_slide'](key, 14, "SELECT\nAND BREED",
        "Selection makes it evolve: keep the best result, make small variations of it, choose again. The rule proposes, "
        "you select (John Frazer, An Evolutionary Architecture, 1995).",
        "Copy your picked seed and threshold into Parent. Change Mutation, then Pick a child.", scale=115)
    GK['aim'](cam, (0, 0, 4.0), ISO, shift=3.4, lift=-0.3, dist=200)
    t = Tree(key)
    t.inp("Parent Seed", "Int", 2, 0, 999, "From the matrix"); t.inp("Parent Threshold", "Float", 0.5, 0.0, 1.0, "From the matrix")
    t.inp("Mutation", "Float", 0.03, 0.0, 0.2, "How big the changes are"); t.inp("Generations", "Int", 12, 1, 30, "Floors")
    t.inp("Pick", "Int", 4, 0, 8, "Your choice (4 = the parent)")
    ix = index(t, (-1600, 0))
    c = t.math('SUBTRACT', t.math('FLOOR', t.math('DIVIDE', ix, 3, (-1440, 60)), None, (-1280, 60)), 1, (-1120, 60))
    r = t.math('SUBTRACT', t.math('FLOORED_MODULO', ix, 3, (-1440, -80)), 1, (-1280, -80))
    pos = t.vmath('ADD', t.vmath('SCALE', RIGHT, t.math('MULTIPLY', c, S_, (-1120, 200)), (-960, 200)),
                  t.vmath('SCALE', DOWN, t.math('MULTIPLY', r, SR, (-1120, -200)), (-960, -200)), (-800, 0))
    pts = t.n('GeometryNodePoints', (-640, 300)); pts.inputs['Count'].default_value = 9; t.L(pos, pts.inputs['Position'])
    thr = t.math('ADD', t.g("Parent Threshold"), t.math('MULTIPLY', c, t.g("Mutation"), (-800, -300)), (-640, -300))
    scl = t.math('MULTIPLY', 0.25, t.math('ADD', 1.0, t.math('MULTIPLY', r, t.math('MULTIPLY', t.g("Mutation"), 5, (-960, -460)), (-800, -460)), (-640, -460)), (-480, -460))
    pk = cmp(t, 'EQUAL', ix, t.g("Pick"), (-640, -600), 'INT')
    s = t.store(t.store(t.store(t.store(pts.outputs[0], "threshold", thr, 'FLOAT', loc=(-480, 300)), "scale", scl, 'FLOAT', loc=(-320, 300)),
                        "seed", t.g("Parent Seed"), 'INT', loc=(-160, 300)), "picked", pk, 'BOOLEAN', loc=(0, 300))
    out, nodes = foreach_automata(t, s, [("Threshold", 'FLOAT'), ("Scale", 'FLOAT'), ("Seed", 'INT'), ("Picked", 'BOOLEAN'), ("Position", 'VECTOR')],
                                  (300, 300), t.g("Generations"), ("Picked",))
    t.out(out); t.go.location = (1500, 300)
    t.frame("the parent in the middle, 8 children around it: threshold and noise scale nudged by Mutation", [pts, thr.node, scl.node, s.node, pk.node])
    t.frame("for each child: the automaton with its values", nodes)
    t.tidy()
    u = UI(key, cam)
    for n, ty, d in (("Parent Seed", "Int", 2), ("Parent Threshold", "Float", 0.5), ("Mutation", "Float", 0.03), ("Pick", "Int", 4)):
        u.inp(n, ty, d)
    pkd, rest = sel_(u, u.g("Geometry"), "picked")
    u.mass(rest, 'WHITE', 0.04); u.mass(pkd, 'PINK', 0.04)
    u.text("parent", tuple(DOWN[a] * 0.42 * SR + TOWARD[a] for a in range(3)), 0.24, 'GREY')
    mu = u.g("Mutation")
    lines = [('k', ["1  parent: seed ", u.fmt(u.g("Parent Seed"), 0), ", threshold ", u.fmt(u.g("Parent Threshold"), 2)]),
             ('k', "2  eight children, each a small change:"),
             ('k', ["   threshold ± ", u.fmt(mu, 2), ", scale ± ", u.fmt(u.math('MULTIPLY', mu, 500, u.place()), 0), "%"]),
             ('p', ["3  pick again: child ", u.fmt(u.math('ADD', u.g("Pick"), 1, u.place()), 0)]),
             ('g', "generation 2 of the design")] + tools("For Each zone", "Galapagos (evolutionary solver)")
    u.code(lines, y=-0.8)
    u.finish()
    return done(key, sc, t, u, [(n, n) for n in ("Parent Seed", "Parent Threshold", "Mutation", "Pick")])


# ================================================================ 10 Stigmergy
def s10():
    key = "10 Stigmergy"
    sc, cam, hud = GK['make_slide'](key, 10, "STIGMERGY",
        "Agents that read each other's trails. Every walker deposits on the ground; the ground spreads and fades; "
        "every walker steers toward the strongest trail ahead. Ants and slime moulds find paths this way.",
        "Raise Decay to keep trails longer. Lower Sense: the paths get thinner. Set Agents to 300.", scale=17)
    GK['aim'](cam, (0, 0, 0), TOP, shift=3.3)
    t = Tree(key)
    t.inp("Agents", "Int", 150, 1, 600, "How many walkers"); t.inp("Steps", "Int", 250, 0, 800, "How many steps")
    t.inp("Sense", "Float", 0.5, 0.1, 2.0, "How far ahead a walker smells the trail (m)")
    t.inp("Decay", "Float", 0.96, 0.5, 0.999, "How much trail is left each step"); t.inp("Seed", "Int", 0, 0, 999, "Randomness")
    C = 60; CELL = 0.15; W = C * CELL
    grid = grp(t, "Cell Grid", (-1500, 300), {"Columns": C, "Rows": C, "Cell": CELL})
    g0 = t.store(grid.outputs[0], "trail", 0.0, 'FLOAT', loc=(-1300, 300))
    rv = rand(t, 'FLOAT_VECTOR', (-3.5, -3.5, 0.0), (3.5, 3.5, 0.0), t.g("Seed"), (-1500, 0))
    pts = t.n('GeometryNodePoints', (-1300, 0)); t.L(t.g("Agents"), pts.inputs['Count']); t.L(rv, pts.inputs['Position'])
    a0 = t.store(pts.outputs[0], "heading", rand(t, 'FLOAT', 0.0, 2 * math.pi, t.math('ADD', t.g("Seed"), 1, (-1300, -200)), (-1120, -160)), 'FLOAT', loc=(-1000, 0))
    rin, rout = repeat(t, t.g("Steps"), g0, (-800, 300), ("Agents",))
    t.L(a0, rin.inputs['Agents'])
    gr, ag = rin.outputs['Geometry'], rin.outputs['Agents']
    # ground: deposit where a walker stands, then fade and spread
    px = t.n('GeometryNodeProximity', (-600, 500)); px.target_element = 'POINTS'; t.L(ag, px.inputs['Target'])
    near = cmp(t, 'LESS_THAN', px.outputs['Distance'], CELL * 0.75, (-400, 500))
    dep = t.math('ADD', t.math('MULTIPLY', named(t, "trail", 'FLOAT', (-600, 350)), t.g("Decay"), (-400, 350)), near, (-200, 420))
    g1 = t.store(gr, "trail", dep, 'FLOAT', loc=(0, 500))
    bl = t.n('GeometryNodeBlurAttribute', (200, 350), data_type='FLOAT'); t.L(named(t, "trail", 'FLOAT', (0, 300)), bl.inputs['Value'])
    bl.inputs['Iterations'].default_value = 1; bl.inputs['Weight'].default_value = 0.35
    g2 = t.store(g1, "trail", bl.outputs[0], 'FLOAT', loc=(400, 500))
    t.L(g2, rout.inputs['Geometry'])
    # walkers: smell left, ahead, right; turn toward the strongest; step
    hd = named(t, "heading", 'FLOAT', (-600, -100)); pp = position(t, (-600, -220))
    half = W / 2

    def smell(angle_off, y):
        a = t.math('ADD', hd, angle_off, (-400, y))
        sp = t.vmath('ADD', pp, t.vmath('SCALE', t.xyz(t.math('COSINE', a, None, (-250, y)), t.math('SINE', a, None, (-250, y - 60)), 0.0, (-100, y)), t.g("Sense"), (50, y)), (200, y))
        sx, sy, _ = t.sep(sp, (350, y))[:3]
        c = t.math('FLOOR', t.math('DIVIDE', t.math('ADD', sx, half, (500, y)), CELL, (620, y)), None, (740, y))
        r = t.math('FLOOR', t.math('DIVIDE', t.math('ADD', sy, half, (500, y - 60)), CELL, (620, y - 60)), None, (740, y - 60))
        cc = t.math('MINIMUM', t.math('MAXIMUM', c, 0.0, (860, y)), C - 1, (980, y)); rr = t.math('MINIMUM', t.math('MAXIMUM', r, 0.0, (860, y - 60)), C - 1, (980, y - 60))
        idx = t.math('ADD', t.math('MULTIPLY', cc, C, (1100, y)), rr, (1220, y))
        return sample(t, g2, named(t, "trail", 'FLOAT', (1100, y - 120)), idx, 'FLOAT', (1340, y))
    L_ = smell(0.6, -100); Cc = smell(0.0, -400); R_ = smell(-0.6, -700)
    side = t.math('GREATER_THAN', t.math('MAXIMUM', L_, R_, (1500, -400)), Cc, (1650, -400))
    turn = t.math('MULTIPLY', t.math('MULTIPLY', t.math('SIGN', t.math('SUBTRACT', L_, R_, (1500, -250)), None, (1650, -250)), side, (1800, -300)), 0.6, (1950, -300))
    jitter = rand(t, 'FLOAT', -0.25, 0.25, t.math('ADD', t.g("Seed"), 2, (1800, -500)), (1950, -500),
                  ident=t.math('ADD', index(t, (1650, -600)), t.math('MULTIPLY', rin.outputs['Iteration'], 7919, (1650, -700)), (1800, -650)))
    h1 = t.math('ADD', t.math('ADD', hd, turn, (2100, -300)), jitter, (2250, -300))
    out_ = cmp(t, 'GREATER_THAN', t.vmath('LENGTH', pp, None, (1500, -850), out=1), half - 0.3, (1650, -850))
    px_, py_, _ = t.sep(pp, (1500, -1000))[:3]
    home = t.math('ARCTAN2', t.math('MULTIPLY', py_, -1.0, (1650, -1000)), t.math('MULTIPLY', px_, -1.0, (1650, -1100)), (1800, -1050))
    hsw = t.n('GeometryNodeSwitch', (2400, -400), input_type='FLOAT'); t.L(out_, hsw.inputs['Switch']); t.L(h1, hsw.inputs['False']); t.L(home, hsw.inputs['True'])
    a1 = t.store(ag, "heading", hsw.outputs[0], 'FLOAT', loc=(2600, 0))
    hn = named(t, "heading", 'FLOAT', (2600, -200))
    mv = t.n('GeometryNodeSetPosition', (2800, 0)); t.L(a1, mv.inputs['Geometry'])
    t.L(t.xyz(t.math('MULTIPLY', t.math('COSINE', hn, None, (2600, -320)), 0.1, (2700, -320)), t.math('MULTIPLY', t.math('SINE', hn, None, (2600, -440)), 0.1, (2700, -440)), 0.0, (2800, -380)), mv.inputs['Offset'])
    t.L(mv.outputs[0], rout.inputs['Agents'])
    walkers = t.store(rout.outputs['Agents'], "agent", True, 'BOOLEAN', loc=(3100, 0))
    t.out(t.joing([rout.outputs['Geometry'], walkers], (3300, 200))); t.go.location = (3500, 200)
    t.frame("START  a clean ground and walkers at random", [grid, g0.node, pts, a0.node, rv.node])
    t.frame("GROUND  deposit under every walker, fade by Decay, spread a little", [px, near.node, dep.node, g1.node, bl, g2.node])
    t.frame("WALKER  smell left, ahead and right at Sense; turn toward the strongest; step 0.1", [hd.node, pp.node, side.node, turn.node, jitter.node, h1.node, hsw, a1.node, mv, out_.node, home.node])
    t.tidy()
    u = UI(key, cam)
    u.inp("Agents", "Int", 150); u.inp("Steps", "Int", 250); u.inp("Sense", "Float", 0.5); u.inp("Decay", "Float", 0.96)
    scp = u.n('GeometryNodeSeparateComponents', u.place()); u.L(u.g("Geometry"), scp.inputs[0])
    # the trail: cells painted by strength (needs a mesh: squares)
    cells = scp.outputs['Point Cloud']
    agents_, ground = sel_(u, cells, "agent")
    sq = squares(u, ground, CELL * 0.98, None)
    value_paint(u, sq, "trail", 'WHITE', 'BLACK', 0.6)
    dot = u.n('GeometryNodeMeshCircle', u.place(), fill_type='NGON'); u.set(dot, Vertices=12, Radius=0.07)
    io = u.n('GeometryNodeInstanceOnPoints', u.place()); u.L(agents_, io.inputs['Points']); u.L(dot.outputs[0], io.inputs['Instance'])
    rz = u.n('GeometryNodeRealizeInstances', u.place()); u.L(io.outputs[0], rz.inputs[0]); u.add(u.paint(u.transform(rz.outputs[0], (0, 0, 0.02), loc=u.place()), 'PINK'))
    bd = u.n('GeometryNodeMeshGrid', u.place()); u.set(bd, Size_X=W, Size_Y=W)
    u.add(u.edges(u.transform(bd.outputs[0], (0, 0, -0.01), loc=u.place()), 0.012, 'MUTE'))
    lines = [('k', ["1  ", u.fmt(u.g("Agents"), 0), " walkers on a clean ground"]),
             ('k', "2  each step every walker deposits a trail,"),
             ('k', ["   smells ", u.fmt(u.g("Sense"), 1), " m ahead and turns to the strongest"]),
             ('k', ["3  the ground keeps ", u.fmt(u.math('MULTIPLY', u.g("Decay"), 100, u.place()), 0), "% of its trail, and spreads"]),
             ('p', ["4  repeat ", u.fmt(u.g("Steps"), 0), " steps"]),
             ('g', "The paths are the memory of the group.")] + tools("Repeat zone, Blur Attribute", "Culebra (agents + trails)")
    u.code(lines, y=-0.8)
    u.finish()
    return done(key, sc, t, u, [(n, n) for n in ("Agents", "Steps", "Sense", "Decay")])


# ================================================================ 13 Differential growth
def s13():
    key = "13 Differential Growth"
    sc, cam, hud = GK['make_slide'](key, 13, "DIFFERENTIAL\nGROWTH",
        "A closed line that keeps growing in the space it has. Every point steps away from the parts of the line "
        "near it and moves together with its neighbours. New points are added where the line stretches, so it "
        "gets longer and folds like coral, a brain or a leaf edge.",
        "Raise Iterations. Change Reach, Repel and Spacing. Turn on Height, then Layer Height and Every.", scale=12)
    GK['aim'](cam, (0, 0, 1.2), ISO, shift=3.3)
    t = Tree(key)
    t.inp("Iterations", "Int", 300, 0, 1000, "How many times the rule runs")
    t.inp("Spacing", "Float", 0.05, 0.02, 0.3, "Distance between points (m); new points are added at this spacing")
    t.inp("Reach", "Float", 0.3, 0.05, 1.0, "How far a point looks: points closer than Reach are merged into their centre")
    t.inp("Repel", "Float", 1.0, 0.0, 3.0, "How hard points step away")
    t.inp("Seed", "Int", 0, 0, 999, "A small wobble in the start circle")
    t.inp("Height", "Bool", False, desc="Time becomes height: one layer every few iterations")
    t.inp("Layer Height", "Float", 0.05, 0.01, 1.0, "Distance between layers (m)"); t.inp("Every", "Int", 10, 1, 100, "Iterations between two layers")
    # start: a small circle, resampled at Spacing, with a little wobble
    ci = t.n('GeometryNodeCurvePrimitiveCircle', (-1300, 200), mode='RADIUS'); ci.inputs['Resolution'].default_value = 64; S(ci, 'Radius').default_value = 0.7
    rs0 = t.n('GeometryNodeResampleCurve', (-1100, 200)); t.L(ci.outputs['Curve'], rs0.inputs['Curve']); t.L(t.g("Spacing"), rs0.inputs['Length'])
    rs0.inputs['Mode'].default_value = 'Length'
    wob = rand(t, 'FLOAT_VECTOR', (-0.02, -0.02, 0.0), (0.02, 0.02, 0.0), t.g("Seed"), (-1100, 0))
    sp0 = t.n('GeometryNodeSetPosition', (-950, 200)); t.L(rs0.outputs[0], sp0.inputs['Geometry']); t.L(wob, sp0.inputs['Offset'])
    rin, rout = repeat(t, t.g("Iterations"), sp0.outputs[0], (-800, 200), ("Layers",))
    k = rin.outputs['Iteration']; st = rin.outputs['Geometry']
    # look: merge the points within Reach into their centre (Merge by Distance averages them), find the nearest centre
    ctp = t.n('GeometryNodeCurveToPoints', (-600, -100), mode='EVALUATED'); t.L(st, ctp.inputs['Curve'])
    md = t.n('GeometryNodeMergeByDistance', (-450, -100)); t.L(ctp.outputs['Points'], md.inputs['Geometry']); t.L(t.g("Reach"), md.inputs['Distance'])
    pr = t.n('GeometryNodeProximity', (-300, -100), target_element='POINTS'); t.L(md.outputs[0], pr.inputs['Geometry'])
    pp = position(t, (-450, -300))
    # step away: the closer it is, the bigger the step (0 at 2 m)
    away = t.vmath('NORMALIZE', t.vmath('SUBTRACT', pp, pr.outputs['Position'], (-150, -250)), None, (0, -250))
    mr = t.n('ShaderNodeMapRange', (-150, -450)); t.L(pr.outputs['Distance'], mr.inputs['Value']); mr.inputs['From Max'].default_value = 2.0
    t.L(t.math('MULTIPLY', t.g("Repel"), 0.01, (-300, -500)), mr.inputs['To Min']); mr.inputs['To Max'].default_value = 0.0
    step = t.vmath('SCALE', away, mr.outputs[0], (150, -300))
    # move together: every step becomes the average of its neighbours' steps; stay flat
    bl = t.n('GeometryNodeBlurAttribute', (300, -300), data_type='FLOAT_VECTOR'); t.L(step, bl.inputs['Value'])
    bl.inputs['Iterations'].default_value = 1; bl.inputs['Weight'].default_value = 1.0
    flat = t.vmath('MULTIPLY', bl.outputs[0], (1.0, 1.0, 0.0), (450, -300))
    sp = t.n('GeometryNodeSetPosition', (600, 100)); t.L(st, sp.inputs['Geometry']); t.L(flat, sp.inputs['Offset'])
    # grow: resample at Spacing, new points where the line stretched
    rs = t.n('GeometryNodeResampleCurve', (800, 100)); t.L(sp.outputs[0], rs.inputs['Curve']); t.L(t.g("Spacing"), rs.inputs['Length'])
    rs.inputs['Mode'].default_value = 'Length'
    t.L(rs.outputs[0], rout.inputs['Geometry'])
    # a layer every Every iterations, Layer Height apart (rise per iteration = Layer Height / Every)
    every = cmp(t, 'EQUAL', t.math('FLOORED_MODULO', k, t.g("Every"), (650, 400)), 0.0, (850, 400))
    rise = t.math('DIVIDE', t.g("Layer Height"), t.g("Every"), (450, 600))
    lift = t.n('GeometryNodeSwitch', (650, 550), input_type='FLOAT'); t.L(t.g("Height"), lift.inputs['Switch']); t.L(rise, lift.inputs['True'])
    lay = t.transform(rs.outputs[0], t.xyz(0.0, 0.0, t.math('MULTIPLY', lift.outputs[0], k, (850, 550)), (1000, 550)), loc=(1050, 400))
    keep = t.n('GeometryNodeSwitch', (1250, 400), input_type='GEOMETRY'); t.L(every, keep.inputs['Switch']); t.L(lay, keep.inputs['True'])
    t.L(t.joing([rin.outputs['Layers'], keep.outputs[0]], (1450, 450)), rout.inputs['Layers'])
    fin = t.n('GeometryNodeSwitch', (1700, 200), input_type='GEOMETRY'); t.L(t.g("Height"), fin.inputs['Switch'])
    t.L(rout.outputs['Geometry'], fin.inputs['False']); t.L(t.joing([rout.outputs['Layers'], t.transform(rout.outputs['Geometry'], t.xyz(0.0, 0.0, t.math('MULTIPLY', lift.outputs[0], t.g("Iterations"), (1450, 100)), (1550, 100)), loc=(1600, 0))], (1750, 0)), fin.inputs['True'])
    t.out(fin.outputs[0]); t.go.location = (1950, 200)
    t.frame("START  a small circle, resampled at Spacing, with a little wobble (Seed)", [ci, rs0, wob.node, sp0])
    t.frame("LOOK  points closer than Reach merge into their centre; find the nearest centre", [ctp, md, pr])
    t.frame("STEP AWAY  the closer it is, the bigger the step (Repel)", [pp.node, away.node, mr, step.node])
    t.frame("MOVE TOGETHER  each step becomes the average of its neighbours' steps", [bl, flat.node, sp])
    t.frame("GROW  resample at Spacing: new points where the line stretched", [rs])
    t.frame("layers (Height on): one every Every iterations, Layer Height apart", [every.node, rise.node, lift, lay.node, keep, fin])
    t.tidy()
    u = UI(key, cam)
    u.inp("Iterations", "Int", 300); u.inp("Spacing", "Float", 0.05); u.inp("Reach", "Float", 0.3); u.inp("Repel", "Float", 1.0)
    u.inp("Height", "Bool", False); u.inp("Layer Height", "Float", 0.05)
    u.inp("Solid", "Bool", False, desc="Display only: every layer becomes a wall one layer tall")
    tb = u.tube(u.g("Geometry"), 0.03, 'PINK', 8); u.add(tb)
    # tube radius: thinner than half a layer so the layers read; thin edges only when Solid is on
    lr = u.math('MINIMUM', 0.03, u.math('MULTIPLY', u.g("Layer Height"), 0.35, u.place()), u.place())
    hr = u.n('GeometryNodeSwitch', u.place(), input_type='FLOAT'); u.L(u.g("Height"), hr.inputs['Switch']); hr.inputs['False'].default_value = 0.03; u.L(lr, hr.inputs['True'])
    tr = u.n('GeometryNodeSwitch', u.place(), input_type='FLOAT'); u.L(u.g("Solid"), tr.inputs['Switch']); u.L(hr.outputs[0], tr.inputs['False']); tr.inputs['True'].default_value = 0.008
    cm_ = tb.node.inputs[0].links[0].from_node
    while cm_.bl_idname != 'GeometryNodeCurveToMesh': cm_ = cm_.inputs[0].links[0].from_node
    u.L(tr.outputs[0], cm_.inputs['Profile Curve'].links[0].from_node.inputs['Radius'])
    # Solid: every layer becomes a wall one layer tall (curve to edges, extrude the edges up)
    fc = u.n('GeometryNodeCurveToMesh', u.place()); u.L(u.g("Geometry"), fc.inputs['Curve'])
    ex = u.n('GeometryNodeExtrudeMesh', u.place(), mode='EDGES'); u.L(fc.outputs[0], ex.inputs['Mesh'])
    u.L(u.xyz(0.0, 0.0, u.g("Layer Height"), u.place()), ex.inputs['Offset'])
    sl = u.n('GeometryNodeSwitch', u.place(), input_type='GEOMETRY'); u.L(u.g("Solid"), sl.inputs['Switch'])
    u.L(u.paint(ex.outputs['Mesh'], 'WHITE'), sl.inputs['True']); u.add(sl.outputs[0])
    sc_ = u.n('GeometryNodeCurvePrimitiveCircle', u.place(), mode='RADIUS'); S(sc_, 'Radius').default_value = 0.7
    u.add(u.tube(sc_.outputs['Curve'], 0.012, 'MUTE', 6))
    lines = [('p', ["1  start: a small circle, then ", u.fmt(u.g("Iterations"), 0), " times:"]),
             ('k', ["2  look: merge points within ", u.fmt(u.g("Reach"), 2), " m, find the nearest centre"]),
             ('k', ["3  step away from it, more when closer (", u.fmt(u.math('MULTIPLY', u.g("Repel"), 100, u.place()), 0), "%)"]),
             ('k', "4  move together: average the steps along the line"),
             ('k', ["5  resample at ", u.fmt(u.g("Spacing"), 2), " m: new points where it stretched"])] + tools("Repeat zone, Geometry Proximity, Blur Attribute, Resample", "a loop (Anemone) or Kangaroo")
    u.code(lines, y=-0.8)
    u.finish()
    return done(key, sc, t, u, [(n, n) for n in ("Iterations", "Spacing", "Reach", "Repel", "Height", "Layer Height")])


# ================================================================ 14 Physics solver
def s14():
    key = "14 Physics"
    sc, cam, hud = GK['make_slide'](key, 14, "A PHYSICS\nSOLVER",
        "Let forces find the form. A net hangs under gravity until it settles; turn it upside down and every part is "
        "in compression (Gaudi, Frei Otto). Kangaroo and FEA optimisers work the same way: a rule applied until nothing moves.",
        "Change Gravity and Pins. Turn on Flip: the hanging net becomes a shell.", scale=20)
    GK['aim'](cam, (0, 0, 1.0), ISO, shift=3.0)
    t = Tree(key)
    t.inp("Gravity", "Float", 0.01, 0.0, 0.1, "Pull per iteration"); t.inp("Iterations", "Int", 200, 0, 1000, "Until nothing moves")
    t.inp("Pins", "Menu", desc="Which points are held"); t.inp("Flip", "Bool", False, desc="Turn the settled net upside down")
    gr = t.n('GeometryNodeMeshGrid', (-1300, 200)); t.set(gr, Size_X=8.0, Size_Y=8.0, Vertices_X=25, Vertices_Y=25)
    pp = position(t, (-1300, -100)); x, y, _ = t.sep(pp, (-1150, -100))[:3]
    ax = t.math('ABSOLUTE', x, None, (-1000, -60)); ay = t.math('ABSOLUTE', y, None, (-1000, -180))
    edge = t.math('GREATER_THAN', t.math('MAXIMUM', ax, ay, (-850, -120)), 3.9, (-700, -120))
    corner = t.math('GREATER_THAN', t.math('MINIMUM', ax, ay, (-850, -300)), 3.9, (-700, -300))
    mids = t.math('MULTIPLY', edge, t.math('LESS_THAN', t.math('MINIMUM', ax, ay, (-850, -460)), 0.2, (-700, -460)), (-550, -400))
    pm = t.menu(["Edges", "Corners", "Corners and midpoints"], 'FLOAT', (-400, -200)); t.L(t.g("Pins"), pm.inputs['Menu'])
    t.L(corner, pm.inputs['Corners']); t.L(edge, pm.inputs['Edges']); t.L(t.math('MAXIMUM', corner, mids, (-550, -520)), pm.inputs['Corners and midpoints'])
    pinned = cmp(t, 'GREATER_THAN', pm.outputs[0], 0.5, (-200, -200))
    g0 = t.store(gr.outputs[0], "pinned", pinned, 'BOOLEAN', loc=(-1000, 200))
    rin, rout = repeat(t, t.g("Iterations"), g0, (-800, 200))
    st = rin.outputs['Geometry']
    bl = t.n('GeometryNodeBlurAttribute', (-500, 100), data_type='FLOAT_VECTOR'); t.L(position(t, (-650, 60)), bl.inputs['Value'])
    bl.inputs['Iterations'].default_value = 1; bl.inputs['Weight'].default_value = 1.0
    relaxed = t.vmath('SUBTRACT', bl.outputs[0], t.xyz(0.0, 0.0, t.g("Gravity"), (-500, -100)), (-300, 50))
    sp = t.n('GeometryNodeSetPosition', (-100, 200)); t.L(st, sp.inputs['Geometry'])
    t.L(bmath(t, 'NOT', named(t, "pinned", 'BOOLEAN', (-500, 300)), None, (-300, 300)), sp.inputs['Selection']); t.L(relaxed, sp.inputs['Position'])
    t.L(sp.outputs[0], rout.inputs['Geometry'])
    flip = t.n('GeometryNodeSwitch', (800, 100), input_type='VECTOR'); t.L(t.g("Flip"), flip.inputs['Switch'])
    flip.inputs['False'].default_value = (1, 1, 1); flip.inputs['True'].default_value = (1, 1, -1)
    t.out(t.transform(rout.outputs['Geometry'], None, None, flip.outputs[0], loc=(1000, 200))); t.go.location = (1200, 200)
    t.frame("START  a flat net; the pinned points are held", [gr, g0.node, pm, pinned.node] + [n for n in t.nt.nodes if n.bl_idname == 'ShaderNodeMath' and n.location.x < -500])
    t.frame("RULE  every free point moves to the average of its neighbours, then drops by Gravity.  REPEAT until it settles", [rin, rout, bl, relaxed.node, sp])
    t.frame("flip: hanging in tension becomes standing in compression", [flip])
    t.tidy()
    u = UI(key, cam)
    u.inp("Gravity", "Float", 0.01); u.inp("Iterations", "Int", 200); u.inp("Flip", "Bool", False)
    g = u.g("Geometry")
    u.add(u.paint(g, 'WHITE'))
    mc = u.n('GeometryNodeMeshToCurve', u.place()); u.L(g, mc.inputs['Mesh']); u.add(u.tube(mc.outputs[0], 0.012, 'BLACK', 5))
    pins, free = sel_(u, g, "pinned")
    sph = u.n('GeometryNodeMeshUVSphere', u.place()); u.set(sph, Segments=12, Rings=6, Radius=0.12)
    io = u.n('GeometryNodeInstanceOnPoints', u.place()); u.L(pins, io.inputs['Points']); u.L(sph.outputs[0], io.inputs['Instance'])
    rz = u.n('GeometryNodeRealizeInstances', u.place()); u.L(io.outputs[0], rz.inputs[0]); u.add(u.paint(rz.outputs[0], 'PINK'))
    st_ = u.n('GeometryNodeAttributeStatistic', u.place(), data_type='FLOAT_VECTOR'); u.L(g, st_.inputs['Geometry']); u.L(position(u, u.place()), st_.inputs['Attribute'])
    sag = u.vmath('SUBTRACT', st_.outputs['Max'], st_.outputs['Min'], u.place())
    lines = [('k', "1  a net, 8 x 8 m, pinned at the pink points"),
             ('k', ["2  every free point: move to the middle of its"]), ('k', ["   neighbours, then drop ", u.fmt(u.g("Gravity"), 2), " m"]),
             ('p', ["3  repeat ", u.fmt(u.g("Iterations"), 0), " times: sag ", u.fmt(u.sep(sag, u.place())[2], 1), " m"]),
             ('k', u.sswitch(cint_(u, u.g("Flip")), ["4  (turn on Flip)", "4  flipped: a compression shell"]))] + tools(["Cloth simulation, or a Repeat zone", "with Blur Attribute"], "Kangaroo (physics solver)")
    u.code(lines, y=-0.8)
    u.finish()
    return done(key, sc, t, u, [("Gravity", "Gravity"), ("Iterations", "Iterations"), ("Flip", "Flip")])


def cint_(u, boolsock):
    s = u.n('GeometryNodeSwitch', u.place(), input_type='INT'); u.L(boolsock, s.inputs['Switch'])
    s.inputs['False'].default_value = 0; s.inputs['True'].default_value = 1
    return s.outputs[0]


# ================================================================ 18 Plan and section
def s18():
    key = "18 Plan Section"
    sc, cam, hud = GK['make_slide'](key, 18, "PLAN AND\nSECTION",
        "A generated volume is drawn like any building. A horizontal cut at eye height is the plan; a vertical cut is "
        "the section. Cut where the drawing explains the most.",
        "Move Plan Level and Section X. Switch Show to Plan, Section or Both.", scale=24)
    GK['aim'](cam, (0, 0, 3.5), ISO, shift=3.0)
    t = Tree(key)
    t.inp("Plan Level", "Float", 1.6, 0.0, 10.0, "Height of the plan cut (m)"); t.inp("Section X", "Float", 0.0, -6.0, 6.0, "Where the section cuts (m)")
    t.inp("Show", "Menu", desc="Plan, Section or Both"); t.inp("Seed", "Int", 3, 0, 999, "Floor 0 noise seed"); t.inp("Threshold", "Float", 0.5, 0.0, 1.0, "Floor 0 threshold")
    au = grp(t, "Automaton", (-1300, 200), {"Seed": t.g("Seed"), "Threshold": t.g("Threshold"), "Generations": 16})
    vol = au.outputs['Volume']
    # cells are 0.5 m: snap the plan to the top of a layer and the section to a cell boundary
    K = t.math('FLOOR', t.math('DIVIDE', t.g("Plan Level"), 0.5, (-1300, -200)), None, (-1150, -200))
    ztop = t.math('MULTIPLY', t.math('ADD', K, 1.0, (-1000, -200)), 0.5, (-850, -200))
    sx = t.math('MULTIPLY', t.math('ROUND', t.math('DIVIDE', t.g("Section X"), 0.5, (-1300, -400)), None, (-1150, -400)), 0.5, (-1000, -400))
    gen = named(t, "generation", 'INT', (-1000, 100)); px = t.sep(position(t, (-1000, -40)), (-850, -40))[0]
    above = cmp(t, 'GREATER_THAN', gen, K, (-700, 100))
    beyond = cmp(t, 'GREATER_THAN', px, t.math('ADD', sx, 0.01, (-850, -100)), (-700, -40))
    ms = t.menu(["Plan", "Section", "Both"], 'BOOLEAN', (-500, 0)); t.L(t.g("Show"), ms.inputs['Menu'])
    t.L(above, ms.inputs['Plan']); t.L(beyond, ms.inputs['Section']); t.L(bmath(t, 'OR', above, beyond, (-700, -200)), ms.inputs['Both'])
    dl = t.n('GeometryNodeDeleteGeometry', (-300, 200), domain='POINT'); t.L(vol, dl.inputs['Geometry']); t.L(ms.outputs[0], dl.inputs['Selection'])
    s1 = t.store(t.store(dl.outputs[0], "ztop", ztop, 'FLOAT', loc=(-100, 200)), "sx", sx, 'FLOAT', loc=(100, 200))
    t.out(s1); t.go.location = (300, 200)
    t.frame("the volume", [au]); t.frame("plan: remove every layer above Plan Level", [K.node, ztop.node, gen.node, above.node])
    t.frame("section: remove every cell beyond Section X", [sx.node, px.node, beyond.node])
    t.frame("show plan, section or both", [ms, dl, s1.node])
    t.tidy()
    u = UI(key, cam)
    u.inp("Plan Level", "Float", 1.6); u.inp("Section X", "Float", 0.0); u.inp("Show", "Int", 0)
    g = u.g("Geometry")
    # cut faces: flat faces exactly at the plan level or the section x
    fpos = u.n('GeometryNodeInputPosition', u.place())
    nrm = u.n('GeometryNodeInputNormal', u.place())
    nx_, ny_, nz_ = u.sep(nrm.outputs[0], u.place())[:3]
    px_, py_, pz_ = u.sep(fpos.outputs[0], u.place())[:3]
    ztop_ = named(u, "ztop", 'FLOAT', u.place()); sx_ = named(u, "sx", 'FLOAT', u.place())
    atplan = bmath(u, 'AND', cmp(u, 'GREATER_THAN', nz_, 0.99, u.place()), cmp(u, 'LESS_THAN', u.math('ABSOLUTE', u.math('SUBTRACT', pz_, ztop_, u.place()), None, u.place()), 0.01, u.place()), u.place())
    atsect = bmath(u, 'AND', cmp(u, 'GREATER_THAN', nx_, 0.99, u.place()), cmp(u, 'LESS_THAN', u.math('ABSOLUTE', u.math('SUBTRACT', px_, sx_, u.place()), None, u.place()), 0.01, u.place()), u.place())
    cutsel = bmath(u, 'OR', atplan, atsect, u.place())
    sg = u.n('GeometryNodeSeparateGeometry', u.place(), domain='FACE'); u.L(g, sg.inputs['Geometry']); u.L(cutsel, sg.inputs['Selection'])
    u.mass(sg.outputs['Inverted'], 'WHITE'); u.add(u.paint(sg.outputs['Selection'], 'PINK'))
    sh = u.g("Show")
    lines = [('k', u.sswitch(sh, [u.cat(["PLAN     cut at ", u.fmt(u.g("Plan Level"), 1), " m, look down"]), u.cat(["SECTION  cut at x = ", u.fmt(u.g("Section X"), 1), ", look in"]), "PLAN AND SECTION  both cuts"])),
             ('p', "pink: the cut faces (poche)"), ('k', "draw the cut heavy, what is beyond light"),
             ('k', "plus one elevation, one isometric, one perspective")] + tools("Boolean modifier with a big box", "Split Brep, Make2D")
    u.code(lines, y=-0.8)
    u.finish()
    return done(key, sc, t, u, [("Plan Level", "Plan Level"), ("Section X", "Section X"), ("Show", "Show")])


# ================================================================ 19 to 21: the exercise (static slides)
def static_slide(key, num, title, body, right, scale=16.0):
    sc, cam, hud = GK['make_slide'](key, num, title, body, None, scale=scale)
    cam.location = (0, 0, 40); cam.rotation_euler = (0, 0, 0)
    F = bpy.app.driver_namespace['SK']['FONT']; SK = bpy.app.driver_namespace['SK']
    coll = bpy.data.collections["Slide UI " + key]
    y = 3.55
    for color, text, size, gap in right:
        mat = {'k': SK['INK'], 'p': SK['INKP'], 'g': SK['INKG']}[color]
        font = F['bold'] if size >= 0.4 else F['mono']
        name = f"{key} · r{len([o for o in coll.objects if o.name.startswith(key + ' · r')])}"
        SK['text_obj'](name, text, font, size, (-0.4, y), hud, mat, width=7.9, coll=coll)
        y -= gap
    bpy.context.window.scene = sc
    GK['snap'](sc, "GEN_" + key[:2])
    return sc


def s19():
    return static_slide("19 Exercise", 19, "PROJECT 4\nGENERATIVE STORE",
        "Design a system, not an output.\n\nPick one generative strategy and one brand. Build a system that produces "
        "stores of 40 to 64 m2 for that brand. Map its design space, select one result and present it as a competition entry.\n\n"
        "Strategy and brand are approved in class on November 10. The three sheets are presented at the final review on December 11 "
        "with the booklet and the GSM.",
        [('k', "THE STRATEGIES", 0.42, 0.75),
         ('k', "cellular automata      a cell reads its neighbours", 0.27, 0.42),
         ('k', "agents, stigmergy      walkers read the field and leave trails", 0.27, 0.42),
         ('k', "reaction-diffusion     two values spread and react", 0.27, 0.42),
         ('k', "growth                 material joins at the edge", 0.27, 0.42),
         ('k', "physics solver         forces settle into a form", 0.27, 0.65),
         ('p', "one strategy  +  one brand  +  one environment", 0.3, 0.75),
         ('k', "THE DATES", 0.42, 0.7),
         ('k', "Nov 10   strategy and brand approved in class", 0.27, 0.42),
         ('k', "Nov 17   sheet 1, the system, reviewed", 0.27, 0.42),
         ('k', "Nov 24   sheet 2, the design space, reviewed", 0.27, 0.42),
         ('k', "Dec 1    sheet 3, the proposal, reviewed", 0.27, 0.42),
         ('p', "Dec 11   final review: three sheets, booklet (15%), GSM", 0.27, 0.42)])


def s20():
    return static_slide("20 Three Sheets", 20, "THREE SHEETS",
        "Each sheet is 17 x 11 inches, in your Graphic Standards Manual.\n\n"
        "Sheet 1 explains the algorithm so someone else could run it. Sheet 2 shows how you explored and chose. "
        "Sheet 3 is the proposal, drawn and post-processed like a competition entry.\n\n"
        "The last sheet carries four times the weight of each of the other two. The booklet is 15%.",
        [('k', "1  THE SYSTEM   5%", 0.42, 0.6),
         ('k', "start, rule, environment, repetitions, each named and drawn", 0.26, 0.4),
         ('k', "one frame per step, BIG-diagram style, captions in plain words", 0.26, 0.4),
         ('k', "two or three generations of the same run, side by side", 0.26, 0.7),
         ('k', "2  THE DESIGN SPACE   5%", 0.42, 0.6),
         ('k', "a matrix: two parameters, same view and scale in every cell", 0.26, 0.4),
         ('k', "readings: floor, room to move, headroom, entrance, front, light", 0.26, 0.4),
         ('k', "select, breed small variations, select again, say why", 0.26, 0.7),
         ('p', "3  THE PROPOSAL   20%", 0.42, 0.6),
         ('k', "a store of 40 to 64 m2 for your brand, from the selected result", 0.26, 0.4),
         ('k', "elevation, section, isometric, perspective (at minimum)", 0.26, 0.4),
         ('k', "post-processed: person, dimensions, brand, annotations, one story", 0.26, 0.4),
         ('g', "see Museum of Emotions, Last Nuclear Bomb Memorial (Buildner)", 0.26, 0.4)])


def s21():
    return static_slide("21 Rubric", 21, "HOW IT IS\nJUDGED",
        "Sheet 3 and the final booklet are read like a competition jury reads an entry.\n\n"
        "Sheets 1 and 2 keep the course rubric: understanding 30%, communication 30%, technical execution 25%, exploration 15%.\n\n"
        "Credit every supplied group and plugin. Keep the system editable.",
        [('k', "THE COMPETITION RUBRIC", 0.42, 0.75),
         ('k', "1  linework", 0.3, 0.46), ('k', "2  quality of drawings", 0.3, 0.46), ('k', "3  balance of color", 0.3, 0.46),
         ('k', "4  layout", 0.3, 0.46), ('k', "5  hierarchy", 0.3, 0.46), ('k', "6  annotation", 0.3, 0.46),
         ('k', "7  clarity of story", 0.3, 0.46), ('k', "8  clarity of diagrams", 0.3, 0.46),
         ('k', "9  quality of overall presentation", 0.3, 0.75),
         ('p', "also for sheet 3: fidelity to the generated result,", 0.27, 0.42),
         ('p', "a convincing store at 40 to 64 m2", 0.27, 0.42)])



GB = {f"s{n:02d}": globals()[f"s{n:02d}"] for n in range(1, 22)}
GB['groups'] = groups
bpy.app.driver_namespace['GB'] = GB
print("generative_build ready")
