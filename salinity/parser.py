from collections import deque
import re


def parse(highstate_output):
    highstate_lines = highstate_output.splitlines()
    changes_lines = extract_changes(highstate_lines)
    return {"changes": parse_changes_fmt(changes_lines)}


def extract_changes(highstate_lines):
    index_of_summary = highstate_lines.index("Summary for local")
    return highstate_lines[1:index_of_summary]


def parse_changes_fmt(change_raw_lines):
    """
    Takes Salt's state output in the `--state-output=changes` format and returns a dictionary.
    """
    raw_lines_deque = deque(change_raw_lines)
    parsed_entries = []
    current_entry = None
    current_entry_is_clean = True

    while raw_lines_deque:
        line = raw_lines_deque.popleft()
        starts_with_name = line.startswith("  Name: ")
        starts_with_dashes = line.startswith("----------")
        if starts_with_name or starts_with_dashes:
            if current_entry is not None:
                parsed_entries.append(
                    parse_entry(current_entry, current_entry_is_clean)
                )
            current_entry_is_clean = starts_with_name
            current_entry = line
        else:
            current_entry += "\n" + line

    if current_entry is not None:
        parsed_entries.append(parse_entry(current_entry, current_entry_is_clean))

    return parsed_entries


def parse_entry(entry, is_clean):
    if is_clean:
        return parse_clean_entry(entry)
    return parse_changed_entry(entry)


def parse_clean_entry(clean_entry):
    name, function, result, duration = clean_entry.split(" - ")
    return {
        "name": name.split(": ")[1].strip(),
        "function": function.split(": ")[1],
        "result": result.split(": ")[1].split(" ")[0],
        "duration_ms": float(duration.split(" ")[-2]),
    }


def parse_changed_entry(changed_entry):
    changed_entry_regex = re.compile(
        r"ID: (?P<id>.*)|"
        r"Function:(?P<function>.*)|"
        r"Name:(?P<name>.*)|"
        r"Result: (?P<result>.*)|"
        r"Duration: (?P<duration>.*)"
    )

    parsed_entry = dict(
        next(
            (key, value.strip())
            for key, value in needle.groupdict().items()
            if value is not None
        )
        for needle in changed_entry_regex.finditer(changed_entry)
    )

    return {
        "id": parsed_entry.get("id", parsed_entry.get("name")),
        "name": parsed_entry.get("name", parsed_entry.get("id")),
        "function": parsed_entry.get("function"),
        "result": parsed_entry.get("result"),
        "duration_ms": float(parsed_entry.get("duration").split(" ")[0]),
    }
