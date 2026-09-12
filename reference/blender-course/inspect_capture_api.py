import bpy
import json
result = {}
for name,op in [('screenshot',bpy.ops.screen.screenshot),('screenshot_area',bpy.ops.screen.screenshot_area),('screen_full_area',bpy.ops.screen.screen_full_area),('view_all',bpy.ops.node.view_all)]:
    result[name] = {p.identifier:{'type':p.type,'default':str(getattr(p,'default',''))} for p in op.get_rna_type().properties}
result['space_node'] = [p.identifier for p in bpy.types.SpaceNodeEditor.bl_rna.properties]
result['space_3d'] = [p.identifier for p in bpy.types.SpaceView3D.bl_rna.properties]
print(json.dumps(result),flush=True)
