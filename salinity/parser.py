from collections import deque


def parse_changes_fmt(text):
    """
    Takes Salt's state output in the `--state-output=changes` format and returns a dictionary.
    """
    raw_lines = deque(text.splitlines())
    parsed_entries = []
    current_entry = None
    current_entry_is_clean = True

    while raw_lines:
        line = raw_lines.popleft()
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
