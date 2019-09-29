def parse_changes_fmt(text):
    """
    Takes Salt's state output in the `--state-output=changes` format and returns a dictionary.
    """
    parsed_entries = []
    for line in text.splitlines():
        parsed_entries.append(parse_clean_entry(line))
    return parsed_entries


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
