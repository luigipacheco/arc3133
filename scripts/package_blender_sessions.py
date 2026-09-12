"""Package the canonical session list and its dependencies for classroom use."""
from hashlib import sha256
import json
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
import yaml

ROOT = Path(__file__).resolve().parents[1]
data = yaml.safe_load((ROOT/'syllabus/course.yml').read_text(encoding='utf-8'))
sessions = data['blender_sessions']
assert len(sessions) == 12
verified = {r['file']: r for r in json.loads((ROOT/'reference/blender-course/all-sessions-verification.json').read_text())}
assets = {ROOT/'files/blender/README.md'}
for session in sessions:
    path = ROOT/session['file']
    assert sha256(path.read_bytes()).hexdigest() == verified[session['file']]['sha256'], 'Revalidate changed Blender file'
    assets.add(path)
    assets.update(p for p in path.parent.iterdir() if p.is_file() and p.suffix.lower() in ('.md','.png','.ply','.json','.stl','.svg'))
assets.update((ROOT/'syllabus').glob('*.md'))
assets.add(ROOT/'syllabus/course.yml')

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

target = ROOT/'files/blender/ARC3133-Blender-Sessions.zip'
contents = {}
for path in sorted(assets):
    name = path.relative_to(ROOT).as_posix()
    contents[name] = path.read_bytes()
contents['START-HERE.md'] = b'# ARC 3133 Blender sessions\n\nOpen [the session index](files/blender/README.md), then choose the file for this class. Extract the complete folder first and keep the point-cloud data beside its Blender file.\n\nPrepared in Blender 5.2.1 LTS. Native node names are retained. Save a separate working copy.\n'
index = contents['files/blender/README.md'].decode('utf-8')
index = re.sub(r'\[Download all 12 sessions and supporting files\]\(ARC3133-Blender-Sessions.zip\)\. Extract the ZIP before opening a lesson\.', 'This extracted folder contains all 12 session files and their supporting data.', index)
contents['files/blender/README.md'] = index.encode('utf-8')
hashes = {name:sha256(payload).hexdigest() for name,payload in contents.items()}
contents['CONTENTS-SHA256.json'] = (json.dumps(hashes,indent=2)+'\n').encode('utf-8')
with ZipFile(target,'w',ZIP_DEFLATED,compresslevel=6) as archive:
    for name,payload in contents.items():
        archive.writestr('ARC3133/'+name,payload)
with ZipFile(target) as archive:
    assert archive.testzip() is None
    assert sum(name.endswith('.blend') for name in archive.namelist())==12
    for name,expected_hash in hashes.items():
        assert sha256(archive.read('ARC3133/'+name)).hexdigest()==expected_hash
report = {'archive':target.relative_to(ROOT).as_posix(),'session_count':12,'files':len(contents),
          'bytes':target.stat().st_size,'sha256':sha256(target.read_bytes()).hexdigest(),
          'stl_dimensions_mm':stl_bounds,'closed_svg_cut_paths':len(paths)}
(ROOT/'reference/blender-course/package-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
