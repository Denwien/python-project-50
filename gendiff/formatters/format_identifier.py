from gendiff.formatters import json, plain, stylish


def format_identifier(diff, formatter='stylish'):
    if formatter == 'stylish':
        return stylish.format_diff_stylish(diff)
    elif formatter == 'plain':
        return plain.format_plain(diff)
    elif formatter == 'json':
        return json.format_json(diff)
    raise ValueError(f"Unknown format: {formatter}")
