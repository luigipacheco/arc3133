"""Read-only teaching audit of the saved session files."""
import bpy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT/'reference/blender-course/session-manifest.json').read_text(encoding='utf-8'))
report = []
for session in manifest:
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/session['file']),load_ui=True)
    graphs = []
    for scene in bpy.data.scenes:
        obj = scene.view_layers[0].objects.active
        group = next(m.node_group for m in obj.modifiers if m.type=='NODES')
        nodes = [n for n in group.nodes if n.type!='FRAME']
        frames = [n for n in group.nodes if n.type=='FRAME' and n.text and not any(c.parent==n for c in group.nodes)]
        crowding = [n.label for n in frames if n.location.y-n.height < max(c.location.y for c in nodes)+50]
        groups = [n.node_tree.name for n in nodes if n.type=='GROUP' and n.node_tree]
        graphs.append({'scene':scene.name,'nodes':len(nodes),'span':round(max(n.location.x+n.width for n in nodes)-min(n.location.x for n in nodes)),
                       'groups_to_enter':groups,'annotation_crowding':crowding})
    report.append({'session':session['id'],'graphs':graphs})
    print(json.dumps(report[-1]),flush=True)
(ROOT/'reference/blender-course/teaching-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
