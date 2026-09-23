"""Assignment deadline display and cumulative midterm grading from course data."""
import re


def time_label(course, assignment):
    value = assignment.get("due_time")
    if not value:
        return ""
    hour, minute = map(int, value.split(":"))
    suffix = "PM" if hour >= 12 else "AM"
    return f"{hour % 12 or 12}:{minute:02d} {suffix} {course.meta['deadline_timezone']}"


def deadline(course, assignment):
    result = course.when(assignment["due"])
    time = time_label(course, assignment)
    return result + (", " + time if time else "")


def validate(course):
    for assignment in course.assessments:
        if assignment.get("due_time"):
            assert re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", assignment["due_time"])
            assert isinstance(assignment["due"], int) and course.meta["deadline_timezone"]
    spec = course.data["midterm_grade"]
    members = spec["assessments"]
    assert members and len(members) == len(set(members))
    assert set(members) <= set(course.by_id)
    assert set(spec["due_at_midterm"]) <= set(members)
    week = course.meta["midterm_week"]
    assert week in course.weeks
    assert all(isinstance(course.by_id[aid]["due"], int) and course.by_id[aid]["due"] <= week for aid in members)
    assert all(course.by_id[aid]["due"] == week for aid in spec["due_at_midterm"]), "Midterm assignment dates must match course.midterm_week"
    assert sum(course.by_id[aid]["weight"] for aid in members) > 0


def members(course):
    return [course.by_id[aid] for aid in course.data["midterm_grade"]["assessments"]]


def note(course):
    total = sum(a["weight"] for a in members(course))
    return ("The midterm grade accumulates the Graphic Standards Manual, CSG sheet and print, "
            f"module (3.1) and arrays (3.2). These assignments account for {total}% of the final course grade. "
            f"Report the accumulated result as a percentage of those {total} possible course points. "
            "The midterm adds no separate assessment weight.")


def summary(course, web=False):
    selected = members(course)
    total = sum(a["weight"] for a in selected)
    out = "## Midterm grade\n\n"
    out += f"**Midterm deadline:** {course.when(course.meta['midterm_week'])}.\n\n" + note(course) + "\n\n"
    out += "| Included work | Due | Course weight |\n| --- | --- | --- |\n"
    for a in selected:
        name = course.label(a)
        if web:
            name = course.link(name, course.assignment_url(a))
        out += f"| {name} | {deadline(course, a)} | {a['weight']}% |\n"
    out += (f"\n**Calculation:** add each assignment's earned course points "
            f"(assignment percentage / 100 x its course weight), then divide the total by {total} "
            "and multiply by 100. Use the course's existing submission and late-work policies.\n\n")
    return out
