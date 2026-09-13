# -*- coding: utf-8 -*-
"""ARC 3133 — one consistency pass for every Blender teaching file.

Run headless per file. It never deletes a graph or rewires logic; it makes the
files agree with each other and makes the graphs readable:

  1. Naming    — object, node group and world take their scene's name, so what a
                 student sees in the outliner and the modifier matches the tab.
  2. Labels    — every Math / Compare / Boolean node says what it does instead of
                 reading "Math.004". Hand-written labels are never overwritten.
  3. Look      — one course-palette material whose colour encodes what the scene
                 teaches (height, or distance from the centre), one lighting rig,
                 one camera framed on the real extent, one render engine.

Report is printed as JSON so the caller can check what changed.
"""
import bpy, json, math, sys
from mathutils import Vector

# ── the course palette, converted sRGB -> linear ──────────────────────────
def _lin(h):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(int(h[0:2], 16)), f(int(h[2:4], 16)), f(int(h[4:6], 16)), 1.0)

CYAN, LIME, YELLOW = _lin("00D9E1"), _lin("C6F035"), _lin("FFE500")
BG = (0.021, 0.021, 0.024, 1.0)

# ── 2. readable node labels ───────────────────────────────────────────────
MATH = {
    'ADD': "add", 'SUBTRACT': "subtract", 'MULTIPLY': "multiply", 'DIVIDE': "divide",
    'MULTIPLY_ADD': "multiply then add", 'POWER': "power", 'SQRT': "square root",
    'ABSOLUTE': "absolute value", 'MINIMUM': "smaller of the two",
    'MAXIMUM': "larger of the two", 'MODULO': "remainder", 'WRAP': "wrap into a range",
    'SINE': "sin( )", 'COSINE': "cos( )", 'TANGENT': "tan( )", 'ARCTAN2': "angle of (x, y)",
    'FLOOR': "round down", 'CEIL': "round up", 'ROUND': "round", 'FRACT': "fractional part",
    'SIGN': "sign", 'SNAP': "snap to steps",
}
COMPARE = {'GREATER_THAN': "is greater than", 'GREATER_EQUAL': "is greater or equal",
           'LESS_THAN': "is less than", 'LESS_EQUAL': "is less or equal",
           'EQUAL': "is equal to", 'NOT_EQUAL': "is not equal to"}
BOOL = {'AND': "AND — both true?", 'OR': "OR — either true?", 'NOT': "NOT — flip it",
        'NAND': "NAND", 'NOR': "NOR", 'XOR': "XOR — one but not both"}
PLAIN = {
    'INDEX': "i — the position in the list",
    'POSITION': "where is this point?",
    'INSTANCE_ON_POINTS': "put a component at every point",
    'REALIZE_INSTANCES': "instances -> real geometry",
    'SET_POSITION': "apply the move",
    'JOIN_GEOMETRY': "collect them together",
    'MERGE_BY_DISTANCE': "weld points that sit on top of each other",
    'SWITCH': "TRUE takes one value, FALSE the other",
    'REPEAT_INPUT': "REPEAT — once per item",
    'REPEAT_OUTPUT': "...until the count is reached",
    'MESH_PRIMITIVE_LINE': "a row of points",
    'MESH_PRIMITIVE_GRID': "a grid of points",
    'MESH_PRIMITIVE_CUBE': "THE COMPONENT",
    'POINTS': "a point",
    'SEPXYZ': "split into X, Y, Z",
    'COMBXYZ': "build a vector from X, Y, Z",
    'FILL_CURVE': "close the outline into a face",
    'POINTS_TO_CURVES': "join the points into a curve",
    'FLIP_FACES': "turn the face the other way",
    'SET_MATERIAL': "give it the course colours",
    'STORE_NAMED_ATTRIBUTE': "remember a value on each element",
    'GROUP_OUTPUT': "the result",
}

def label_nodes(ng):
    n_done = 0
    for n in ng.nodes:
        if n.type == 'FRAME' or n.label:      # never overwrite a hand-written label
            continue
        text = None
        if n.type == 'MATH':
            text = MATH.get(getattr(n, "operation", ""), None)
        elif n.type == 'COMPARE':
            text = COMPARE.get(getattr(n, "operation", ""), None)
        elif n.type == 'BOOLEAN_MATH':
            text = BOOL.get(getattr(n, "operation", ""), None)
        elif n.type == 'GROUP_INPUT':
            names = [s.name for s in n.outputs if s.name and s.enabled][:-1]
            text = " / ".join(names) if names else "the controls"
        else:
            text = PLAIN.get(n.type)
        if text:
            n.label = text
            n_done += 1
    return n_done

# ── 3. one material whose colour carries the lesson ───────────────────────
def ramp_material(name, mode, lo, hi):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial");  out.location = (620, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (330, 0)
    bsdf.inputs["Roughness"].default_value = 0.35
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.location = (40, 0)
    e = ramp.color_ramp
    e.elements[0].position, e.elements[0].color = 0.0, CYAN
    e.elements[1].position, e.elements[1].color = 1.0, YELLOW
    e.elements.new(0.5).color = LIME
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.location = (-170, 0)
    mr.inputs["From Min"].default_value = lo
    mr.inputs["From Max"].default_value = hi
    geo = nt.nodes.new("ShaderNodeNewGeometry"); geo.location = (-620, 0)
    if mode == "height":
        sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (-440, 0)
        nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
        nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    else:
        ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = 'LENGTH'; ln.location = (-440, 0)
        nt.links.new(geo.outputs["Position"], ln.inputs[0])
        nt.links.new(ln.outputs["Value"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m

def ensure_set_material(ng, mat):
    if any(n.type == 'SET_MATERIAL' for n in ng.nodes):
        for n in ng.nodes:
            if n.type == 'SET_MATERIAL':
                n.inputs["Material"].default_value = mat
        return False
    go = next((n for n in ng.nodes if n.type == 'GROUP_OUTPUT'), None)
    if not go:
        return False
    src = next((l for l in ng.links if l.to_node == go), None)
    if not src:
        return False
    sm = ng.nodes.new("GeometryNodeSetMaterial")
    sm.location = (go.location.x - 200, go.location.y - 120)
    sm.label = "give it the course colours"
    sm.inputs["Material"].default_value = mat
    fs = src.from_socket
    ng.links.remove(src)
    ng.links.new(fs, sm.inputs["Geometry"])
    ng.links.new(sm.outputs["Geometry"], go.inputs[0])
    return True

# ── real extent: instances do not grow bound_box ──────────────────────────
def _walk(dg):
    lo = Vector((1e9, 1e9, 1e9)); hi = Vector((-1e9, -1e9, -1e9)); n = 0
    for inst in dg.object_instances:
        ob = inst.object
        if ob is None or ob.type != 'MESH':
            continue
        mw = inst.matrix_world
        for c in ob.bound_box:
            p = mw @ Vector(c); n += 1
            lo.x, lo.y, lo.z = min(lo.x, p.x), min(lo.y, p.y), min(lo.z, p.z)
            hi.x, hi.y, hi.z = max(hi.x, p.x), max(hi.y, p.y), max(hi.z, p.z)
    return lo, hi, n


def real_bounds(sc):
    """Instances do not grow bound_box, so walk the evaluated depsgraph.

    Background Blender has no window, so the scene cannot be switched the usual
    way; temp_override gives the right scene's depsgraph in both modes.
    """
    lo = hi = None; n = 0
    try:
        with bpy.context.temp_override(scene=sc, view_layer=sc.view_layers[0]):
            lo, hi, n = _walk(bpy.context.evaluated_depsgraph_get())
    except Exception:
        win = getattr(bpy.context, "window", None)
        if win:
            prev = win.scene
            win.scene = sc
            lo, hi, n = _walk(bpy.context.evaluated_depsgraph_get())
            win.scene = prev
    if not n:
        return Vector((0, 0, 0)), Vector((2, 2, 2))
    return (lo + hi) / 2.0, (hi - lo)

def rig(sc, centre, size):
    sphere = max(size.length / 2.0, 0.5)
    for old in [x for x in list(sc.objects) if x.type in ('CAMERA', 'LIGHT')]:
        bpy.data.objects.remove(old, do_unlink=True)
    cd = bpy.data.cameras.new(sc.name + " cam"); cd.lens = 50
    cam = bpy.data.objects.new(sc.name + " camera", cd)
    sc.collection.objects.link(cam)
    sc.render.resolution_x, sc.render.resolution_y = 1600, 1000
    aspect = sc.render.resolution_y / sc.render.resolution_x
    hf = 2 * math.atan(cd.sensor_width / (2 * cd.lens))
    vf = 2 * math.atan((cd.sensor_width * aspect) / (2 * cd.lens))
    dist = max(sphere / math.tan(hf / 2), sphere / math.tan(vf / 2)) * 1.18
    d = Vector((0.85, -1.0, 0.55)).normalized()
    cam.location = centre + d * dist
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = cam
    for nm, dirn, mult, col in (("key", Vector((0.7, -0.9, 1.5)), 95, (1, 1, 1)),
                                ("rim", Vector((-1.1, 0.8, 0.5)), 38, (0.55, 0.85, 1.0))):
        L = bpy.data.lights.new(f"{sc.name} {nm}", 'AREA')
        L.size = sphere * 2.2
        L.energy = (sphere ** 2) * mult
        L.color = col
        o = bpy.data.objects.new(f"{sc.name} {nm}", L)
        sc.collection.objects.link(o)
        dn = dirn.normalized()
        o.location = centre + dn * (sphere * 2.6)
        o.rotation_euler = (-dn).to_track_quat('-Z', 'Y').to_euler()
    return sphere, dist


def run():
    report = {"file": bpy.data.filepath, "scenes": [], "renamed": [], "labelled": 0}
    engines = [s.render.engine for s in bpy.data.scenes]
    engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in engines else engines[0]

    for sc in bpy.data.scenes:
        sc.render.engine = engine
        meshes = [o for o in sc.objects if o.type == 'MESH']
        if not meshes:
            continue

        # 1. naming — everything answers to the scene it lives in
        for i, o in enumerate(meshes):
            want = sc.name if i == 0 else f"{sc.name} {i+1}"
            if o.name != want:
                report["renamed"].append(f"object {o.name} -> {want}")
                o.name = want
            if o.data and o.data.name != want + " source":
                o.data.name = want + " source"
            for m in o.modifiers:
                if m.type == 'NODES' and m.node_group:
                    ng = m.node_group
                    users = sum(1 for ob in bpy.data.objects
                                for mm in ob.modifiers
                                if mm.type == 'NODES' and mm.node_group == ng)
                    if users == 1 and ng.name != want:      # shared helper groups keep their names
                        report["renamed"].append(f"group {ng.name} -> {want}")
                        ng.name = want
        if sc.world and sc.world.name != sc.name:
            wusers = sum(1 for s in bpy.data.scenes if s.world == sc.world)
            if wusers == 1:
                report["renamed"].append(f"world {sc.world.name} -> {sc.name}")
                sc.world.name = sc.name
        if sc.world:
            sc.world.use_nodes = True
            bg = sc.world.node_tree.nodes.get("Background")
            if bg:
                bg.inputs[0].default_value = BG
                bg.inputs[1].default_value = 1.0

        centre, size = real_bounds(sc)
        flat = size.z < max(size.x, size.y) * 0.12          # a flat scene has no height to colour
        mode = "radius" if flat else "height"
        if mode == "height":
            lo, hi = centre.z - size.z / 2.0, centre.z + size.z / 2.0
        else:
            lo, hi = 0.0, max(size.x, size.y) / 2.0
        if hi - lo < 1e-4:
            hi = lo + 1.0
        mat = ramp_material(f"ARC - {sc.name}", mode, lo, hi)

        for o in meshes:
            o.data.materials.clear()
            o.data.materials.append(mat)
            for m in o.modifiers:
                if m.type == 'NODES' and m.node_group:
                    ensure_set_material(m.node_group, mat)

        sphere, dist = rig(sc, centre, size)
        report["scenes"].append({
            "scene": sc.name, "colour": mode,
            "size": [round(v, 2) for v in size], "camera_distance": round(dist, 1)})

    for ng in bpy.data.node_groups:
        report["labelled"] += label_nodes(ng)

    bpy.ops.wm.save_mainfile()
    report["saved"] = True
    print("ARC_REPORT " + json.dumps(report))
    return report

run()
