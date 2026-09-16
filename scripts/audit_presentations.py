"""Inventory and read the existing decks without editing them."""
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from pypdf import PdfReader
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reference/course-audit'
OUT.mkdir(parents=True, exist_ok=True)
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
inventory = []
text = ['# Existing presentation contents\n']
for path in sorted((ROOT / 'slides').glob('*.pptx')):
    with ZipFile(path) as archive:
        bad = archive.testzip()
        names = sorted((n for n in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)),
                       key=lambda n: int(re.search(r'slide(\d+)', n).group(1)))
        slides = []
        for number, name in enumerate(names, 1):
            root = ET.fromstring(archive.read(name))
            lines = [''.join(p.itertext()) for p in root.findall('.//a:t', NS)]
            slides.append({'slide': number, 'text': '\n'.join(lines)})
        item = {'file': path.relative_to(ROOT).as_posix(), 'zip_error': bad, 'slides': slides}
    pdf = path.with_suffix('.pdf')
    item['pdf_exists'] = pdf.is_file()
    if pdf.is_file():
        reader = PdfReader(pdf)
        item['pdf_pages'] = len(reader.pages)
        item['pdf_text'] = [p.extract_text() for p in reader.pages]
        item['page_count_matches'] = len(reader.pages) == len(slides)
        render_dir = OUT / path.stem
        render_dir.mkdir(exist_ok=True)
        subprocess.run(['pdftoppm', '-scale-to', '650', '-png', str(pdf), str(render_dir / 'slide')], check=True,
                       capture_output=True)
        images = sorted(render_dir.glob('slide-*.png'))
        # Contact sheets contain rendered source pages, never fabricated slide art.
        for group in range(0, len(images), 6):
            subset = images[group:group+6]
            sheet = Image.new('RGB', (1320, 1190), 'white')
            draw = ImageDraw.Draw(sheet)
            for n, image_path in enumerate(subset):
                image = Image.open(image_path).convert('RGB')
                x, y = (n % 2) * 660, (n // 2) * 395
                draw.text((x + 5, y + 3), f'{path.stem} / page {group+n+1}', fill='black')
                sheet.paste(image, (x + 5, y + 23))
            sheet.save(OUT / f'{path.stem}-contact-{group//6+1}.jpg')
    inventory.append(item)
    text.append('\n## ' + path.name + '\n')
    for slide in slides:
        text.extend(['\n### Slide ' + str(slide['slide']) + '\n', slide['text'] + '\n'])
(OUT / 'presentation-inventory.json').write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding='utf-8')
(OUT / 'presentation-text.md').write_text('\n'.join(text), encoding='utf-8')
for item in inventory:
    print(item['file'], len(item['slides']), 'slides;', item.get('pdf_pages', 'no'), 'PDF pages')
