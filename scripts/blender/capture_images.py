"""Capture authentic Blender editors in a separate, unsaved UI process.

Run without --background. Source .blend files are opened read-only and never saved.
Uses Blender's native screenshot_area operator, without image reconstruction.
"""
import argparse
import bpy
import json
import math
import struct
import sys
import traceback
from hashlib import sha256
from mathutils import Vector, Euler
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'images/blender'
OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument('--only',default='')
parser.add_argument('--live',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
sessions=json.loads((ROOT/'reference/blender-course/session-manifest.json').read_text(encoding='utf-8'))
choices={'S01':('07 - Difference','difference'),
         'S02':('05 - Solid','parametric-pyramid'),
         'S03':('02 - Nested grid','nested-grid'),
         'S04':('05 - If and range','index-range'),
         'S05':('04 - Curve attractor','curve-attractor'),
         'S06':('03 - Attractor lattice','attractor-lattice'),
         'S07':('03 - Points to volume','points-to-volume'),
         'S08':('03 - SDF Boolean','sdf-boolean'),
         'S09':('04 - Noise field','noise-field'),
         'S10':('02 - Contour stack','contour-stack'),
         'S11':('04 - Laid out parts','section-parts-layout'),
         'S12':('04 - Registered sections','registered-sections')}
jobs=[s for s in sessions if not args.only or s['id'] in args.only.split(',')]
state={'index':0,'stage':'load','results':[],'area':None,'original_hash':None}
STATUS=ROOT/'reference/blender-course/capture-status.json'

def write_status(error=None,complete=False):
    STATUS.write_text(json.dumps({'stage':state['stage'],'index':state['index'],'total':len(jobs),
                                 'results':state['results'],'complete':complete,'error':error},indent=2)+'\n',encoding='utf-8')

def active_context():
    window=bpy.context.window_manager.windows[0]
    area=max(window.screen.areas,key=lambda a:a.width*a.height)
    region=next(r for r in area.regions if r.type=='WINDOW')
    return window,area,region

def finish():
    if 'show_tooltips' in state:
        bpy.context.preferences.view.show_tooltips=state['show_tooltips']
    if args.live:
        bpy.ops.wm.open_mainfile(filepath=str(ROOT/sessions[0]['file']),load_ui=True)
        if state.get('restore_window'):
            state['restore_window']()
    else:
        bpy.ops.wm.quit_blender()

def screenshot(kind):
    job=jobs[state['index']]
    filename=f"{job['id'].lower()}-{choices[job['id']][1]}-{kind}.png"
    window,area,region=active_context()
    with bpy.context.temp_override(window=window,area=area,region=region):
        bpy.ops.screen.screenshot_area(filepath=str(OUT/filename),check_existing=False)
    content=(OUT/filename).read_bytes()
    assert content[:8]==b'\x89PNG\r\n\x1a\n'
    width,height=struct.unpack('>II',content[16:24])
    assert width>=1400 and height>=750,(width,height)
    entry=state['entry']
    entry[kind]={'file':'images/blender/'+filename,'width':width,'height':height,'sha256':sha256(content).hexdigest()}
    print('CAPTURED '+filename+f' {width}x{height}',flush=True)

def tick():
    try:
        if state['index']>=len(jobs):
            write_status(complete=True)
            finish()
            return None
        job=jobs[state['index']]
        scene_name,slug=choices[job['id']]
        if state['stage']=='load':
            path=ROOT/job['file']
            state['original_hash']=sha256(path.read_bytes()).hexdigest()
            bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
            window=bpy.context.window_manager.windows[0]
            scene=bpy.data.scenes[scene_name]
            window.scene=scene
            obj=scene.view_layers[0].objects.active
            assert obj is not None
            for other in scene.objects:
                other.select_set(other==obj,view_layer=scene.view_layers[0])
            obj.hide_set(False,view_layer=scene.view_layers[0])
            scene.view_layers[0].update()
            group=next(m.node_group for m in obj.modifiers if m.type=='NODES')
            state['entry']={'session':job['id'],'unit':job['unit'],'title':job['title'],'source_file':job['file'],
                            'source_sha256':state['original_hash'],'scene':scene_name,'node_group':group.name,
                            'object':obj.name,'capture':'Blender native editor screenshots','blender_version':bpy.app.version_string}
            window,area,region=active_context()
            if len(window.screen.areas)>1:
                with bpy.context.temp_override(window=window,area=area,region=region):
                    bpy.ops.screen.screen_full_area(use_hide_panels=True)
            state['stage']='nodes'
            write_status()
            return 1.5
        if state['stage']=='nodes':
            window,area,region=active_context()
            area.type='NODE_EDITOR'
            space=area.spaces.active
            space.tree_type='GeometryNodeTree'
            space.pin=False
            space.show_region_toolbar=False
            space.show_region_ui=False
            space.show_region_header=True
            group=next(m.node_group for m in window.scene.view_layers[0].objects.active.modifiers if m.type=='NODES')
            if state.get('resize_window'):
                span=max(n.location.x+n.width for n in group.nodes)-min(n.location.x for n in group.nodes)
                state['resize_window'](min(3840,max(1920,int(span+180))))
            for node in group.nodes:
                node.select=False
            area.tag_redraw()
            state['stage']='fit_nodes'
            return 1.5
        if state['stage']=='fit_nodes':
            window,area,region=active_context()
            with bpy.context.temp_override(window=window,area=area,region=region):
                bpy.ops.node.view_all()
            state['stage']='capture_nodes'
            return 2.0
        if state['stage']=='capture_nodes':
            screenshot('geonodes')
            if state.get('resize_window'):
                state['resize_window'](1920)
            window,area,region=active_context()
            area.type='VIEW_3D'
            space=area.spaces.active
            space.show_region_toolbar=False
            space.show_region_ui=False
            space.show_region_header=False
            space.show_region_tool_header=False
            space.show_gizmo=False
            overlay=space.overlay
            overlay.show_overlays=True
            for prop in ('show_floor','show_axis_x','show_axis_y','show_axis_z','show_cursor','show_text','show_extras','show_relationship_lines','show_outline_selected','show_stats'):
                if hasattr(overlay,prop):setattr(overlay,prop,False)
            space.shading.type='SOLID'
            space.shading.color_type='OBJECT'
            space.shading.light='STUDIO'
            space.shading.show_cavity=True
            space.shading.cavity_type='BOTH'
            space.shading.background_type='WORLD'
            space.clip_end=10000
            space.clip_start=.001
            points=[]
            scene=window.scene
            scene.view_layers[0].update()
            deps=scene.view_layers[0].depsgraph
            for obj in scene.objects:
                if obj.hide_get(view_layer=scene.view_layers[0]) or obj.type in ('CAMERA','LIGHT'):continue
                ev=obj.evaluated_get(deps)
                if obj.type in ('MESH','CURVE','SURFACE'):
                    mesh=ev.to_mesh()
                    if mesh:points.extend(ev.matrix_world@v.co for v in mesh.vertices)
                    ev.to_mesh_clear()
            assert points,'No visible evaluated geometry'
            state['view_points']=points
            state['framing_pass']=0
            lo=Vector([min(p[k] for p in points) for k in range(3)])
            hi=Vector([max(p[k] for p in points) for k in range(3)])
            space.region_3d.view_perspective='ORTHO'
            space.region_3d.view_location=(lo+hi)/2
            space.region_3d.view_rotation=Euler((math.radians(65),0,math.radians(30)),'XYZ').to_quaternion()
            space.region_3d.view_distance=max((hi-lo).length,1)*.9
            if job['id']=='S11':
                space.region_3d.view_rotation=Euler((0,0,0),'XYZ').to_quaternion()
                space.region_3d.view_distance=max((hi-lo).length,1)*.8
            area.tag_redraw()
            state['stage']='fit_viewport'
            return 1.5
        if state['stage']=='fit_viewport':
            window,area,region=active_context()
            with bpy.context.temp_override(window=window,area=area,region=region):
                bpy.ops.view3d.view_selected(use_all_regions=False)
            area.spaces.active.region_3d.view_distance*=1.1
            state['stage']='check_framing'
            return 2.0
        if state['stage']=='check_framing':
            from bpy_extras.view3d_utils import location_3d_to_region_2d,region_2d_to_location_3d
            window,area,region=active_context()
            rv=area.spaces.active.region_3d
            positions=[location_3d_to_region_2d(region,rv,p) for p in state['view_points']]
            xmin=min(p.x for p in positions);xmax=max(p.x for p in positions)
            ymin=min(p.y for p in positions);ymax=max(p.y for p in positions)
            width,height=region.width,region.height
            if xmin>=width*.08 and xmax<=width*.92 and ymin>=height*.08 and ymax<=height*.92:
                state['stage']='capture_viewport'
                return .5
            assert state['framing_pass']<4,'Could not fit the full visible geometry in the viewport'
            center=region_2d_to_location_3d(region,rv,((xmin+xmax)/2,(ymin+ymax)/2),rv.view_location)
            factor=max((xmax-xmin)/(width*.76),(ymax-ymin)/(height*.76))
            rv.view_location=center
            rv.view_distance*=factor
            state['framing_pass']+=1
            area.tag_redraw()
            return 1.0
        if state['stage']=='capture_viewport':
            screenshot('viewport')
            assert sha256((ROOT/job['file']).read_bytes()).hexdigest()==state['original_hash'],'Source file changed'
            state['results'].append(state['entry'])
            state['index']+=1
            state['stage']='load'
            write_status()
            return .5
    except Exception:
        error=traceback.format_exc()
        print(error,flush=True)
        write_status(error=error)
        finish()
        return None

if args.live:
    state['show_tooltips']=bpy.context.preferences.view.show_tooltips
    bpy.context.preferences.view.show_tooltips=False
    # Resize only this Blender process's window; retain its original placement.
    import ctypes
    from ctypes import wintypes
    import os
    user32=ctypes.windll.user32
    class POINT(ctypes.Structure):
        _fields_=[('x',wintypes.LONG),('y',wintypes.LONG)]
    class RECT(ctypes.Structure):
        _fields_=[('left',wintypes.LONG),('top',wintypes.LONG),('right',wintypes.LONG),('bottom',wintypes.LONG)]
    class WINDOWPLACEMENT(ctypes.Structure):
        _fields_=[('length',wintypes.UINT),('flags',wintypes.UINT),('showCmd',wintypes.UINT),('ptMinPosition',POINT),('ptMaxPosition',POINT),('rcNormalPosition',RECT)]
    found=[]
    CALLBACK=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
    def collect(hwnd,lparam):
        pid=wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))
        if pid.value==os.getpid() and user32.IsWindowVisible(hwnd):found.append(hwnd)
        return True
    callback=CALLBACK(collect)
    user32.EnumWindows(callback,0)
    if len(found)==1:
        hwnd=found[0]
        placement=WINDOWPLACEMENT();placement.length=ctypes.sizeof(placement)
        user32.GetWindowPlacement(hwnd,ctypes.byref(placement))
        user32.ShowWindow(hwnd,9)
        def resize_window(width):
            user32.SetWindowPos(hwnd,None,0,0,width,1080,0x14)
        resize_window(1920)
        state['resize_window']=resize_window
        def restore_window():
            user32.SetWindowPlacement(hwnd,ctypes.byref(placement))
        state['restore_window']=restore_window
write_status()
bpy.app.timers.register(tick,first_interval=2,persistent=True)
