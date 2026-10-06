"""Classes are the sessions: every Blender example file is taught in a dated class.

There is no separate session section. Each class page carries the example files,
scene order, practice and screenshots for the files scheduled that week. Old
/sessions/ URLs are kept as redirects to the matching class.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERVIEW = '/classes/overview/'


def home_week(course, session):
    """The first class that teaches this file, or None for optional files."""
    weeks = [w['week'] for w in course.weeks.values() if session['id'] in w.get('sessions', [])]
    if not weeks:
        block = course.session_blocks[session['id']]
        weeks = list(block['weeks'])
    return weeks[0] if weeks else None


def available(course, session):
    if not (ROOT / session['path']).is_file():
        return False
    if not set(session['units']) & course.open_units:
        return False
    week = home_week(course, session)
    return week is None or week in course.open_weeks


def title(course, session):
    block = course.session_blocks[session['id']]
    return course.units[block['units'][0]]['title'] if block.get('combine_sessions') else session['title']


def url(session, course):
    week = home_week(course, session)
    return course.class_url(week) if week else '/resources/example-files/'


def weeks(block):
    values = block['weeks']
    if not values:
        return 'Optional'
    return str(values[0]) if len(values) == 1 else f'{values[0]}–{values[-1]}'


def videos(course, block):
    out = []
    for uid in block['units']:
        for label, link in course.units[uid].get('videos', []):
            out.append(f'[{label}]({link})')
    return out


def sequence(course, web=True):
    rows = ['| Weeks | Topic | Classes | Video tutorials |', '|---|---|---|---|']
    for block in course.sequence:
        classes = []
        for n in block['weeks']:
            label = f'Class {n:02d}'
            classes.append(course.link(label, course.class_url(n)) if web else label)
        vids = videos(course, block) or ['—']
        rows.append(f"| {weeks(block)} | {block['focus']} | {' · '.join(classes)} | {' · '.join(vids)} |")
    return '\n'.join(rows) + '\n'


def files_section(course, week):
    """Example files, scene order, practice and screenshots for one class."""
    w = course.weeks[week]
    planned = [s for s in course.sessions if s['id'] in w.get('sessions', [])]
    group = []
    for s in planned:
        block = course.session_blocks[s['id']]
        if block.get('combine_sessions'):
            group += [x for x in course.sessions if x['id'] in block['sessions'] and x not in group]
        elif s not in group:
            group.append(s)
    if not group:
        return ''
    ready = [s for s in group if available(course, s)]
    out = '## Example files\n\n'
    if not ready:
        return out + 'The example file is posted with this class.\n\n'
    out += course.blender['reference_note'] + ' ' + course.blender['how_to_use'] + '\n\n'
    out += f"Prepared in **{course.blender['version']}**. {course.blender['version_note']}\n\n"
    for s in ready:
        out += f"**[{s['title']}]({course.asset(s['path'], True)})** — download .blend\n\n"
        out += '\n'.join(f'{n}. {scene}' for n, scene in enumerate(s['scenes'], 1)) + '\n\n'
        if s.get('note'):
            out += s['note'].strip() + '\n\n'
        extras = [(label, path) for label, path in s.get('extras', []) if (ROOT / path).is_file()]
        if extras:
            out += 'Supporting files: ' + ', '.join(f'[{label}]({course.asset(path, True)})' for label, path in extras) + '.\n\n'
    unit = course.units[group[0]['units'][0]]
    out += '**Practice:** ' + (unit['exercise'] if len(group) > 1 else group[0]['exercise']) + '\n\n'
    shots = [s for s in ready if any(i['session'] == s['id'] for i in course.blender_images)]
    if shots:
        out += '### Screenshots from the files\n\nSelect an image to open it at full resolution.\n\n'
        for s in shots:
            out += '{% include blender_screenshots.html session="' + s['id'] + '" %}\n\n'
    return out


def build(course, front):
    """Classes overview plus redirects from every retired /sessions/ address."""
    index = front('Classes · overview', categories=['classes'])
    index += ('# Classes\n\nOne page per class, in order. Each class page has the slides, the video tutorials, '
              'the Blender example files, what to practice and what is due. Pages are posted as the semester reaches them. '
              'Everything through Arrays is due by ' + course.midterm_deadline() + '.\n\n')
    index += sequence(course)
    for block in course.sequence:
        label = 'Weeks' if len(block['weeks']) > 1 else 'Week'
        index += f'\n<a id="{block["id"].lower()}"></a>\n\n## {block["focus"]}\n\n{label} {weeks(block)}. '
        index += (block.get('delivery') or course.units[block['units'][0]]['goal']) + '\n\n'
        rows = []
        for n in block['weeks']:
            wk = course.weeks[n]
            rows.append('- ' + course.link(f'Class {n:02d}' + (' · ' + wk['label'] if wk.get('label') else ''), course.class_url(n)) + ' — ' + course.when(n) + ': ' + wk['focus'])
        index += '\n'.join(rows) + '\n'
    if course.optional_classes:
        index += '\n## Possible intermediate class\n\n'
        for block in course.optional_classes:
            index += f'<a id="{block["id"].lower()}"></a>\n\n**{block["focus"]}.** ' + block['description'] + ' '
            index += course.link('Optional example files', '/resources/example-files/') + '\n\n'
    course.emit('modules/classes/_posts/1999-12-31-overview.md', index)

    moved = 'This page has moved: sessions and classes are now the same thing. '
    page = front('Classes', 'index', permalink='/sessions/', sitemap=False)
    page += '## Classes\n\n' + moved + course.link('Open the class list', OVERVIEW) + '.\n'
    course.emit('redirects/sessions-index.md', page)
    for s in course.sessions:
        page = front('Classes', 'index', permalink='/sessions/' + s['id'].lower() + '/', sitemap=False)
        page += '## ' + s['title'] + '\n\n' + moved + course.link('Open the class that uses this file', url(s, course)) + '.\n'
        course.emit('redirects/session-' + s['id'].lower() + '.md', page)
