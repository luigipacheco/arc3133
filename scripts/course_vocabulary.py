"""Assignment glossary, authored in syllabus/vocabulary.yml."""
from urllib.parse import urlsplit
from html import escape
import ast
import struct

import yaml

URL = "/tutorials/the-notation/"
MARKER = "<!-- Generated from syllabus/vocabulary.yml by scripts/sync_course.py. Edit the source, not this copy. -->"


def load(root, assignments):
    data = yaml.safe_load((root / "syllabus/vocabulary.yml").read_text(encoding="utf-8"))
    sections = data["sections"]
    examples = data.get("node_examples", {})
    assert set(examples) <= {t[0] for s in sections for t in s['terms']}, 'Node example without a vocabulary term'
    assert len({s["id"] for s in sections}) == len(sections), "Duplicate vocabulary section"
    assert {s["assignment"] for s in sections} == set(assignments) - {"PART"}, "Vocabulary must cover every assignment"
    for section in sections:
        section['node_examples'] = {t[0]: examples[t[0]] for t in section['terms'] if t[0] in examples}
        assert section["title"] and section["focus"] and section["terms"]
        for term in section["terms"]:
            assert len(term) == 4 and all(isinstance(v, str) and v.strip() for v in term), term
            url = urlsplit(term[3])
            assert url.scheme == "https" and url.netloc, term
        for example in section.get('programming', []):
            assert all(isinstance(example.get(k), str) and example[k].strip()
                       for k in ('title', 'code', 'output', 'nodes', 'try'))
            ast.parse(example['code'])
        if 'debugging' in section:
            assert section['debugging'] and all(isinstance(s, str) and s.strip() for s in section['debugging'])
    for example in examples.values():
        assert all(example.get(k) for k in ('software', 'node', 'note'))
        if 'image' not in example:
            continue
        assert all(example.get(k) for k in ('caption', 'credit', 'source'))
        path = (root / example['image']).resolve()
        assert path.is_relative_to(root) and path.is_file(), path
        content = path.read_bytes()
        assert content[:8] == b'\x89PNG\r\n\x1a\n', path
        example['width'], example['height'] = struct.unpack('>II', content[16:24])
        if 'focus' in example:
            x, y, w, h = example['focus']
            assert min(x, y) >= 0 and min(w, h) > 0
            assert x+w <= example['width'] and y+h <= example['height']
        if not example['source'].startswith('https://'):
            assert (root / example['source']).is_file(), example['source']
    return sections


def assignment_links(course, assignment):
    return " · ".join(course.link(s["title"].split(" · ")[0], URL + "#" + s["id"])
                      for s in course.glossary if s["assignment"] == assignment)


def node_example(course, item, web):
    out = f"**Find it in {item['software']}:** {item['node']}. {item['note']}\n\n"
    if 'image' not in item:
        return out
    source = item['source']
    source_url = source if source.startswith('https://') else ('{{ site.baseurl }}/' if web else '../') + source
    src = ('{{ site.baseurl }}/' if web else '../') + item['image']
    if not web:
        return out + f"[![{item['software']}: {item['caption']}]({src})]({src})\n\n{item['caption']} [Source: {item['credit']}](<{source_url}>)\n\n"
    img = (f'<img src="{src}" alt="{escape(item["software"] + ": " + item["caption"], quote=True)}" '
           f'width="{item["width"]}" height="{item["height"]}" loading="lazy" decoding="async"')
    if 'focus' in item:
        x, y, w, h = item['focus']
        img += (f' style="width:{100*item["width"]/w:.4f}%;left:{-100*x/w:.4f}%;top:{-100*y/h:.4f}%;">')
        img = f'<span class="vocab-node-focus" style="width:{w*2}px;aspect-ratio:{w}/{h};">{img}</span>'
    else:
        img += '>'
    out += (f'<figure class="vocab-node">\n<a href="{src}" aria-label="Open complete screenshot: {escape(item["node"], quote=True)}">{img}</a>\n'
            f'<figcaption><strong>{escape(item["software"])}</strong> · {escape(item["caption"])} '
            f'<a href="{src}">Open full image</a>.<br>Source: <a href="{escape(source_url, quote=True)}">{escape(item["credit"])}</a>.</figcaption>\n</figure>\n\n')
    return out


def render(course, web=True):
    out = "# Vocabulary by assignment\n\n"
    out += ("Use this page while working on an assignment: each entry explains **what it is**, "
            "**how we use it** and where to read a fuller explanation. The examples use ordinary language; "
            "you do not need to memorize formal definitions or reproduce equations.\n\n"
            "The references are optional reading from Wikipedia, Python and software documentation, and a university library. "
            "They explain the underlying concepts; the assignment briefs define what to submit. "
            "Some tool names differ between Blender Geometry Nodes and Grasshopper.\n\n"
            "**Node examples:** GN means Geometry Nodes; GH means Grasshopper. Selected entries include actual course captures or attributed documentation screenshots. Click an image to inspect the full screenshot. Graft and Flatten describe GH data-tree operations, not changes to a shape's geometry.\n\n"
            '<a id="assignments"></a>\n\n## Find your assignment\n\n')
    out += "\n".join(f"- [{s['title']}](#{s['id']})" for s in course.glossary) + "\n\n"
    out += ("## Programming essentials\n\n"
            "The aim is to read a small program, predict what changing an input will do, modify one rule and inspect the result when it fails. "
            "Use the short examples as a bridge between Python and the node work. Each example runs independently in ordinary Python and prints numbers or lists; geometry creation happens in the modeling software.\n\n")
    out += '\n'.join(f"- [{s['title'].split(' · ')[0]}: {s['programming'][0]['title']}](#python-{s['id']})"
                     for s in course.glossary if s.get('programming')) + '\n'
    out += '- [Debugging checklist: find the first unexpected result](#debugging)\n\n'
    for section in course.glossary:
        out += f"<a id=\"{section['id']}\"></a>\n\n## {section['title']}\n\n{section['focus']}\n\n"
        if web:
            out += course.link("Open the assignment", course.assignment_url(course.by_id[section["assignment"]])) + "\n\n"
        for name, meaning, use, url in section["terms"]:
            host = urlsplit(url).netloc
            provider = ("Wikipedia" if host.endswith("wikipedia.org") else
                        "Blender documentation" if host.endswith("blender.org") else
                        "McNeel Grasshopper guide" if host == "developer.rhino3d.com" else
                        "Python documentation" if host == "docs.python.org" else
                        "Prusa documentation" if host == "help.prusa3d.com" else "University library guide")
            # Angle brackets preserve parentheses in Wikipedia URLs across Markdown renderers.
            out += (f"### {name}\n\n**What it is:** {meaning}\n\n"
                    f"**How we use it:** {use}\n\n"
                    f"[Read more: {name} — {provider}](<{url}>)\n\n")
            if name in section['node_examples']:
                out += node_example(course, section['node_examples'][name], web)
        if section.get('debugging'):
            out += '<a id="debugging"></a>\n\n### Debugging checklist — use with any assignment\n\n'
            out += '\n'.join(f'{i}. {step}' for i, step in enumerate(section['debugging'], 1)) + '\n\n'
        if section.get('programming'):
            out += f'<a id="python-{section["id"]}"></a>\n\n### Read, predict, change, inspect\n\n'
            for example in section['programming']:
                out += (f'#### {example["title"]}\n\n```python\n{example["code"].rstrip()}\n```\n\n'
                        f'**Expected output:**\n\n```text\n{example["output"].rstrip()}\n```\n\n'
                        f'**Connection to node work:** {example["nodes"]}\n\n'
                        f'**Try it:** {example["try"]}\n\n')
                if example.get('reference'):
                    out += f'[Further explanation](<{example["reference"]}>)\n\n'
        out += "[Back to assignments](#assignments)\n\n"
    return out
