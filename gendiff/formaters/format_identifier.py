from gendiff.formaters import stylish, plain, json as json_format


def format_identifier(diff, formatter='stylish'):
    if formatter == 'stylish':
        return stylish.format_diff_stylish(diff)
    elif formatter == 'plain':
        return plain.format_diff_plain(diff)
    elif formatter == 'json':
        return json_format.format_diff_json(diff)
    else:
        raise ValueError(f"Unknown formatter: {formatter}")
