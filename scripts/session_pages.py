"""Generate session pages underneath the approved teaching sequence."""
from pathlib import Path


def available(course, session):
    return bool(set(session['units']) & course.open_units) and (Path(__file__).resolve().parents[1] / session['path']).is_file()


def primary(course, session):
    block = course.session_blocks[session['id']]
    if block.get('combine_sessions'):
        return next(s for s in course.sessions if s['id'] == block['sessions'][0])
    return session


def members(course, session):
    block = course.session_blocks[session['id']]
    return [s for s in course.sessions if s['id'] in block['sessions']] if block.get('combine_sessions') else [session]


def title(course, session):
    block = course.session_blocks[session['id']]
    return course.units[block['units'][0]]['title'] if block.get('combine_sessions') else session['title']


def url(session, course=None):
    if course is not None:
        session = primary(course, session)
    return '/sessions/' + session['id'].lower() + '/'


def weeks(block):
    values = block['weeks']
    if not values:
        return 'Optional'
    return str(values[0]) if len(values) == 1 else f'{values[0]}–{values[-1]}'


def sequence(course, web=True):
    rows = ['| Target weeks | Focus | Practical sessions |', '|---|---|---|']
    sessions = {s['id']: s for s in course.sessions}
    for block in course.sequence:
        labels = []
        for sid in block['sessions']:
            s = sessions[sid]
            if primary(course, s)['id'] != sid:
                continue
            label = 'One arrays session' if block.get('combine_sessions') else sid
            labels.append(course.link(label, url(s, course)) if web and available(course, s) else label)
        if not labels:
            activity = block.get('activity', 'Manual and sample sheet')
            labels = [course.link(activity, course.unit_url(course.units[block['units'][0]])) if web else activity]
        rows.append(f"| {weeks(block)} | {block['focus']} | {', '.join(labels)} |")
    return '\n'.join(rows) + '\n'


def build(course, front):
    introduction = ('These ten blocks set the teaching order. Target weeks are a guide: a topic may take longer. '
                    'Start with short assignments, then combine and revise them into the four projects. '
                    'Download example files individually; the arrays session uses two files.\n\n')
    index = front('Teaching sequence · sessions', categories=['sessions'], permalink='/sessions/')
    index += '# Teaching sequence\n\n' + introduction
    index += sequence(course)
    index += '\nSession pages bring together the file, scene order, short exercise and matching screenshots. Pages are posted with their lesson; later sessions remain listed here.\n\n'
    sessions = {s['id']: s for s in course.sessions}
    for block in course.sequence:
        index += f'<a id="{block["id"].lower()}"></a>\n\n## {block["focus"]}\n\nTarget weeks: {weeks(block)}.\n\n'
        if not block['sessions']:
            for uid in block['units']:
                unit = course.units[uid]
                index += course.link(unit['title'], course.unit_url(unit)) + '\n\n' + unit['exercise'] + '\n\n'
            continue
        for sid in block['sessions']:
            s = sessions[sid]
            if primary(course, s)['id'] != sid:
                continue
            name = title(course, s)
            index += (course.link(name, url(s, course)) if available(course, s) else name + ' — *not yet released*') + '\n\n'
            index += (block.get('delivery') or s['focus']) + '\n\n'
    if course.optional_classes:
        index += '## Possible intermediate class\n\n'
        for block in course.optional_classes:
            index += f'<a id="{block["id"].lower()}"></a>\n\n### {block["focus"]}\n\n' + block['description'] + '\n\n'
            for sid in block['sessions']:
                s = sessions[sid]
                index += (course.link(s['title'], url(s, course)) if available(course, s) else s['title'] + ' — *optional lesson not yet posted*') + '\n\n'
    course.emit('modules/sessions/_posts/1999-12-31-session-sequence.md', index)
    for i, s in enumerate(course.sessions, 1):
        if not available(course, s):
            continue
        block = course.session_blocks[s['id']]
        if primary(course, s)['id'] != s['id']:
            redirect = front('Arrays is one session', layout='index', permalink=url(s), sitemap=False)
            redirect += 'Both arrays files are now covered in one session and one tutorial video. ' + course.link('Open the complete arrays lesson', url(s, course)) + '.\n'
            course.emit('redirects/session-' + s['id'].lower() + '.md', redirect)
            continue
        group = members(course, s)
        unit = course.units[s['units'][0]]
        name = title(course, s)
        page = front(name, categories=['sessions'], permalink=url(s), session_id=s['id'], teaching_block=block['id'])
        page += '# ' + name + '\n\n'
        timing = 'Optional intermediate class' if block.get('optional') else 'Target weeks ' + weeks(block)
        page += course.link(block['focus'], '/sessions/#' + block['id'].lower()) + ' · ' + timing + '\n\n' + (unit['goal'] if len(group) > 1 else s['focus']) + '\n\n'
        if block.get('delivery'):
            page += '**Session and tutorial video:** ' + block['delivery'] + '\n\n'
        page += course.blender['reference_note'] + '\n\n'
        page += course.blender['how_to_use'] + '\n\n'
        page += '## Example files and steps\n\n'
        for example in group:
            page += '**[' + example['title'] + '](' + course.asset(example['path'], True) + ')**\n\n'
            page += '\n'.join(f'{n}. {scene}' for n, scene in enumerate(example['scenes'], 1)) + '\n\n'
            if example.get('note'):
                page += example['note'] + '\n\n'
        page += ('## Optional exploration\n\n' if block.get('optional') else '## Short assignment\n\n') + (unit['exercise'] if len(group) > 1 else s['exercise']) + '\n\n'
        page += '## Lesson notes and project connection\n\n'
        for uid in s['units']:
            u = course.units[uid]
            page += course.link(u['title'], course.unit_url(u)) + ' — ' + u['connection'] + '\n\n'
        projects = [p for p in course.projects.values() if set(s['units']) & set(p['units'])]
        if projects:
            page += 'Develop this exercise in ' + ', '.join(course.link(p['id'] + ' — ' + p['title'], course.project_url(p)) for p in projects) + '.\n\n'
        if s.get('extras'):
            page += '## Supporting files\n\n' + '\n'.join('- [' + name + '](' + course.asset(path, True) + ')' for name, path in s['extras']) + '\n\n'
        page += '## Examples from the files\n\n'
        for example in group:
            page += '{% include blender_screenshots.html session="' + example['id'] + '" %}\n\n'
        page += course.link('Return to the complete teaching sequence', '/sessions/') + '\n'
        course.emit(f'modules/sessions/_posts/2000-01-{i:02d}-{s["id"].lower()}.md', page)
