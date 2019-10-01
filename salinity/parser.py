from collections import deque


def parse(highstate_output):
    highstate_lines = highstate_output.splitlines()
    changes_lines = extract_changes(highstate_lines)
    return {"changes": parse_changes_fmt(changes_lines)}


def extract_changes(highstate_lines):
    index_of_summary = highstate_lines.index("--------------")
    return highstate_lines[1 : index_of_summary - 1]


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
    entry_lines = changed_entry.splitlines()

    def get_value(line_number):
        return entry_lines[line_number].split(": ")[1].strip()

    return {
        "name": get_value(1),
        "function": get_value(2),
        "result": get_value(3),
        "duration_ms": float(get_value(6).split(" ")[0]),
    }
