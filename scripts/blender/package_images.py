"""Validate native screenshots and build their downloadable image index."""
from hashlib import sha256
import json
from pathlib import Path
import struct
from zipfile import ZipFile,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'images/blender'
records={}
for name in ('capture-all-status.json','capture-status.json'):
    status=json.loads((ROOT/'reference/blender-course'/name).read_text(encoding='utf-8'))
    assert status['complete'] and not status['error'],f'Capture incomplete: {name}'
    for item in status['results']:records[item['session']]=item
assert len(records)==12
descriptions={
    'S01':('Subtracting a cylinder from a block creates a parametric opening.','a block with a cylindrical cutout','Cube, Cylinder, Transform Geometry and Mesh Boolean set to Difference.'),
    'S02':('Five vertices and five faces form the pyramid. Width, Depth and Height remain exposed.','a closed pyramid with a rectangular base','the original 002-point in middle group constructs and joins the pyramid faces.'),
    'S03':('A nested grid places the same pyramid in rows and columns.','twenty-five pyramids arranged in a regular grid','the Nested Grid group feeds Instance on Points and Realize Instances.'),
    'S04':('Two comparisons select an index range; Switch controls its vertical displacement.','a grid of pyramids with a raised band','Index, Compare, Boolean Math, Switch and Set Position control the selected range.'),
    'S05':('Distance to an external curve is remapped into pyramid height.','pyramid heights forming a ridge along the attractor curve','Geometry Proximity measures distance to the curve and Map Range controls Z scale.'),
    'S06':('An attractor changes the height of the upper lattice. The struts overlap at their joints.','a two-layer lattice with varying upper heights and an external attractor','distance remapping moves the upper layer and controls the vertical members.'),
    'S07':('The imported sample points become a density volume, then a visible mesh boundary.','three rounded building-like masses reconstructed from synthetic samples','Import PLY, Mesh to Points, Points to Volume and Volume to Mesh.'),
    'S08':('A sphere is subtracted from a block using sampled signed distance grids.','a block with a rounded spherical subtraction','Mesh to SDF Grid feeds SDF Grid Boolean and Grid to Mesh.'),
    'S09':('Noise modifies a sphere field before its zero surface is extracted.','a sphere-like surface varied by noise','Position and Vector Math define sphere distance, modified by Noise Texture and sampled with Field to Grid.'),
    'S10':('A Repeat Zone extracts a stack of contours at controlled heights.','nine contour curves describing the sampled volume','the source volume and Contour at Height group feed a Repeat Zone.'),
    'S11':('The section profiles become solid parts and are laid out in a grid.','nine flat section parts arranged in three rows','Fill and extrusion are supplied by Profile to Solid; index-based positions arrange the parts.'),
    'S12':('Twelve section parts include two registration holes for the fabrication prototype.','a stack of twelve section parts with paired registration holes','the contour and registered-profile groups construct and position the section parts.'),
}
images=[]
for key,item in sorted(records.items()):
    assert sha256((ROOT/item['source_file']).read_bytes()).hexdigest()==item['source_sha256'],f'Source changed: {key}'
    caption,viewport_alt,nodes_alt=descriptions[key]
    item.update(example=item['scene'][5:],caption=caption,viewport_alt=viewport_alt,nodes_alt=nodes_alt)
    for kind in ('geonodes','viewport'):
        asset=item[kind]
        payload=(ROOT/asset['file']).read_bytes()
        assert sha256(payload).hexdigest()==asset['sha256'],asset['file']
        assert struct.unpack('>II',payload[16:24])==(asset['width'],asset['height'])
    images.append(item)
manifest=json.dumps(images,indent=2,ensure_ascii=False)+'\n'
(OUT/'manifest.json').write_text(manifest,encoding='utf-8')
(ROOT/'_data/blender_images.json').write_text(manifest,encoding='utf-8')
readme='# Blender screenshots — ARC 3133\n\n'
readme+='24 original PNG screenshots: one Geometry Nodes setup and one matching 3D viewport from each of the 12 session files. Captured through Blender MCP in Blender 5.2.1 LTS. Source files and native node names were not changed.\n\n'
readme+='Names follow `sXX-example-geonodes.png` and `sXX-example-viewport.png`. Use the original PNGs in slides. The manifest records the source file, scene, node group, dimensions and checksums.\n\n'
readme+='| Session | Example | Geometry Nodes | 3D viewport |\n|---|---|---|---|\n'
for item in images:
    readme+=f"| {item['session']} | {item['example']} | [{Path(item['geonodes']['file']).name}]({Path(item['geonodes']['file']).name}) | [{Path(item['viewport']['file']).name}]({Path(item['viewport']['file']).name}) |\n"
readme+='\nThe website shows screenshots for released lessons. All 24 originals remain available here for slide preparation.\n'
(OUT/'README.md').write_text(readme,encoding='utf-8')
with ZipFile(OUT/'ARC3133-Blender-Screenshots.zip','w',ZIP_DEFLATED,compresslevel=6) as archive:
    for item in images:
        for kind in ('geonodes','viewport'):
            path=ROOT/item[kind]['file'];archive.write(path,path.name)
    archive.write(OUT/'README.md','README.md')
    archive.write(OUT/'manifest.json','manifest.json')
with ZipFile(OUT/'ARC3133-Blender-Screenshots.zip') as archive:
    assert archive.testzip() is None
    assert len([n for n in archive.namelist() if n.endswith('.png')])==24
print(f'Validated {len(images)} pairs; source files unchanged; manifest, index and screenshot ZIP written.')
