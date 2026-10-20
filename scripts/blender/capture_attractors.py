"""Capture real node editors in a disposable Blender UI process; never save."""
import bpy
import json
import traceback
from pathlib import Path
from hashlib import sha256

ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT/"files/blender/04-attractors/Attractors.blend"
OUT = ROOT/"images/blender/attractors"
OUT.mkdir(parents=True,exist_ok=True)
STATUS = ROOT/"reference/blender/attractors/capture.json"
original = sha256(FILE.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(FILE),load_ui=False)
jobs = ["02 - One point","03 - Multiple points","04 - Curve attractor",
        "05 - Panel prefab","06 - One point opening","07 - Multiple point openings","08 - Curve openings"]
state = {"index":0,"stage":"select","captures":[]}


def tick():
    try:
        window = bpy.context.window_manager.windows[0]
        area = max(window.screen.areas,key=lambda a:a.width*a.height)
        if state["index"]==len(jobs):
            assert sha256(FILE.read_bytes()).hexdigest()==original
            STATUS.write_text(json.dumps({"complete":True,"sha256":original,**state},indent=2)+"\n")
            bpy.ops.wm.quit_blender()
            return None
        title = jobs[state["index"]]
        if state["stage"]=="select":
            scene = bpy.data.scenes[title]
            window.scene = scene
            for ob in scene.objects:
                ob.select_set(ob==scene.view_layers[0].objects.active)
            if len(window.screen.areas)>1:
                with bpy.context.temp_override(window=window,area=area):
                    bpy.ops.screen.screen_full_area(use_hide_panels=True)
                area = max(window.screen.areas,key=lambda a:a.width*a.height)
            area.type = "NODE_EDITOR"
            space = area.spaces.active
            space.tree_type = "GeometryNodeTree"
            space.pin = False
            space.show_region_ui = False
            space.show_region_toolbar = False
            state["stage"]="fit"
            return 1
        region = next(r for r in area.regions if r.type=="WINDOW")
        if state["stage"]=="fit":
            with bpy.context.temp_override(window=window,area=area,region=region):
                bpy.ops.node.view_all()
            state["stage"]="capture"
            return 1
        path = OUT/(title[:2]+"-nodes.png")
        with bpy.context.temp_override(window=window,area=area,region=region):
            bpy.ops.screen.screenshot_area(filepath=str(path),check_existing=False)
        state["captures"].append({"scene":title,"file":str(path.relative_to(ROOT)),
                                  "sha256":sha256(path.read_bytes()).hexdigest()})
        state["index"]+=1
        state["stage"]="select"
        STATUS.write_text(json.dumps({"complete":False,"sha256":original,**state},indent=2)+"\n")
        return .5
    except Exception:
        STATUS.write_text(json.dumps({"complete":False,"error":traceback.format_exc(),**state},indent=2)+"\n")
        bpy.ops.wm.quit_blender()
        return None


bpy.app.timers.register(tick,first_interval=2)
