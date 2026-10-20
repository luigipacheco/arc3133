"""Evaluate the saved lesson, exercise its controls, and render sample results."""
import bpy
import bmesh
import json
import math
from hashlib import sha256
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / "files/blender/04-attractors/Attractors.blend"
OUT = ROOT / "reference/blender/attractors"
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(FILE), load_ui=False)
report = {"file": str(FILE.relative_to(ROOT)), "sha256": sha256(FILE.read_bytes()).hexdigest(),
          "blender": bpy.app.version_string, "scenes": {}}
assert not bpy.data.libraries
for group in bpy.data.node_groups:
    for node in group.nodes:
        assert node.type == "FRAME" or not node.label
        assert node.bl_idname != "NodeUndefined"
        if node.type != "FRAME":
            assert node.name == node.bl_label or node.name.startswith(node.bl_label + "."), (node.name, node.bl_label)


def mesh_of(ob):
    bpy.context.view_layer.update()
    ob.update_tag()
    bpy.context.view_layer.update()
    return ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).data


def signature(ob):
    mesh = mesh_of(ob)
    return [tuple(round(v,5) for v in x.co) for x in mesh.vertices]


def components(mesh):
    adjacency = {v.index:set() for v in mesh.vertices}
    for e in mesh.edges:
        a,b = e.vertices
        adjacency[a].add(b)
        adjacency[b].add(a)
    unseen = set(adjacency)
    result = []
    while unseen:
        todo = [unseen.pop()]
        chunk = []
        while todo:
            i = todo.pop()
            chunk.append(mesh.vertices[i].co.copy())
            for j in adjacency[i] & unseen:
                unseen.remove(j)
                todo.append(j)
        result.append(chunk)
    return result


for scene in bpy.data.scenes:
    bpy.context.window.scene = scene
    bpy.context.window.view_layer = scene.view_layers[0]
    ob = scene.view_layers[0].objects.active
    assert ob and ob.name == scene.name
    mode = ob["lesson_mode"]
    mesh = mesh_of(ob)
    assert len(mesh.vertices) > 0
    bm = bmesh.new()
    bm.from_mesh(mesh)
    assert all(e.is_manifold for e in bm.edges), scene.name
    volume = abs(bm.calc_volume())
    bm.free()
    chunks = components(mesh)
    assert len(chunks) == (1 if mode == "prefab" else 63), (scene.name,len(chunks))
    data = {"vertices":len(mesh.vertices),"faces":len(mesh.polygons),"components":len(chunks),
            "volume":volume,"closed":True,"native_node_names":True}
    if mode in ("opening","prefab"):
        widths = []
        for chunk in chunks:
            lo = Vector([min(p[k] for p in chunk) for k in range(3)])
            hi = Vector([max(p[k] for p in chunk) for k in range(3)])
            center = (hi+lo)/2
            assert abs((hi-lo).x-1)<1e-4 and abs((hi-lo).z-1)<1e-4
            assert abs((hi-lo).y-.12)<1e-4
            holes = [abs(p.x-center.x)*2 for p in chunk if 1e-4 < abs(p.x-center.x) < .499]
            assert holes, (scene.name,center)
            opening = sum(holes)/len(holes)
            widths.append(opening)
            if mode=="opening" and ob["attractor_method"]!="curve":
                points = [p.location for p in scene.objects if p.type=="EMPTY"]
                d = min((center-p).length for p in points)
                expected = .85 + (.15-.85)*min(d/4,1)
                assert abs(opening-expected)<1e-4,(scene.name,opening,expected)
        assert abs(sum((1-w*w)*.12 for w in widths)-volume)<1e-4
        data["opening_range"] = [min(widths),max(widths)]
        data["outer_size_fixed"] = [1,.12,1]
        if mode=="opening":
            assert max(widths)-min(widths)>.3
    # Exercise each control rather than only checking a default screenshot.
    if mode!="prefab":
        before = signature(ob)
        if ob["attractor_method"]=="curve":
            target = next(p for p in scene.objects if p.type=="CURVE" and not p.hide_select)
            knot = target.data.splines[0].bezier_points[1]
            original = knot.co.copy()
            knot.co.z += 1.7
            target.data.update_tag()
            assert signature(ob)!=before,scene.name
            knot.co = original
            target.data.update_tag()
        else:
            targets = [p for p in scene.objects if p.type=="EMPTY"]
            for target in targets:
                original = target.location.copy()
                target.location.x += 2.7
                target.update_tag()
                assert signature(ob)!=before,(scene.name,target.name)
                target.location = original
                target.update_tag()
                signature(ob)
        data["moving_attractors_changes_geometry"] = True
        g = ob.modifiers[0].node_group
        mr = next(n for n in g.nodes if n.bl_idname=="ShaderNodeMapRange")
        near,far = mr.inputs["To Min"].default_value,mr.inputs["To Max"].default_value
        mr.inputs["To Min"].default_value, mr.inputs["To Max"].default_value = far,near
        assert signature(ob)!=before
        mr.inputs["To Min"].default_value, mr.inputs["To Max"].default_value = near,far
        data["reverse_remap_changes_geometry"] = True
    else:
        mod = ob.modifiers[0]
        inp = next(s for s in mod.node_group.interface.items_tree if s.item_type=="SOCKET" and s.in_out=="INPUT")
        value = getattr(mod.properties.inputs,inp.identifier)
        before = signature(ob)
        original = value.value
        value.value = .8
        assert signature(ob)!=before
        value.value = original
        data["prefab_input_changes_geometry"] = True
    report["scenes"][scene.name] = data
    print("VERIFIED",scene.name,data,flush=True)
    if mode=="opening" or mode=="prefab":
        scene.render.filepath = str(OUT/(scene.name[:2]+".png"))
        bpy.ops.render.render(write_still=True)
assert sha256(FILE.read_bytes()).hexdigest()==report["sha256"]
(OUT/"verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print("VERIFIED all scenes and controls; saved source unchanged.")
