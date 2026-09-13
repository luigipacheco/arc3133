"""Verify individual Blender downloads and their supporting data; no class ZIP is made."""
from hashlib import sha256
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import yaml

ROOT = Path(__file__).resolve().parents[2]
data = yaml.safe_load((ROOT/'syllabus/course.yml').read_text(encoding='utf-8'))
sessions = data['blender']['sessions']
assert len(sessions) == 12
verified = {r['file']: r for r in json.loads((ROOT/'reference/blender/sessions-verification.json').read_text())}
assets = {ROOT/'files/blender/README.md'}
for session in sessions:
    path = ROOT/session['path']
    assert sha256(path.read_bytes()).hexdigest() == verified[session['path']]['sha256'], 'Revalidate changed Blender file'
    assets.add(path)
    assets.update(p for p in path.parent.iterdir() if p.is_file() and p.suffix.lower() in ('.md','.png','.ply','.json','.stl','.svg'))

# Check the material dimensions in the saved export snapshots.
fabrication = ROOT/'files/blender/09-final-project'
stl_bounds = {}
for name, expected in [('small-print-mm.stl',(45,36,22)), ('fit-coupon-mm.stl',(24,12,3)), ('modular-parts-mm.stl',(75.5,75.5,3))]:
    payload = (fabrication/name).read_bytes()
    count = struct.unpack_from('<I', payload, 80)[0]
    assert count > 0 and len(payload) == 84+count*50
    points = []
    for index in range(count):
        values = struct.unpack_from('<12fH', payload, 84+50*index)
        points.extend([values[3:6],values[6:9],values[9:12]])
    dims = [max(p[k] for p in points)-min(p[k] for p in points) for k in range(3)]
    assert all(abs(a-b)<.002 for a,b in zip(dims,expected)), (name,dims)
    assert abs(min(p[2] for p in points))<.002
    stl_bounds[name] = dims
svg = ET.parse(fabrication/'section-parts-and-spacers-mm.svg').getroot()
assert svg.attrib['width']=='400mm' and svg.attrib['height']=='300mm'
paths = svg.findall('.//{http://www.w3.org/2000/svg}path')
assert len(paths)==80 and all(p.attrib['d'].endswith('Z') for p in paths)
labels = svg.findall('.//{http://www.w3.org/2000/svg}text')
assert [e.text for e in labels[:12]] == [f'{i:02d}' for i in range(1,13)]

report = {'downloads': [{'file':p.relative_to(ROOT).as_posix(), 'bytes':p.stat().st_size,
                         'sha256':sha256(p.read_bytes()).hexdigest()} for p in sorted(assets)],
          'blender_files':len(sessions), 'stl_dimensions_mm':stl_bounds,
          'closed_svg_cut_paths':len(paths)}
assert not list((ROOT/'files/blender').rglob('*.zip')), 'Move old bundled downloads into the archive'
(ROOT/'reference/blender/downloads-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'Verified {len(sessions)} individual Blender files and supporting data; no session ZIP created.')
