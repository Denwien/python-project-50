from gendiff.formaters import stylish, plain, json as json_formatter

def format_identifier(diff, formatter='stylish'):
    if formatter == 'stylish':
        return stylish.format_stylish(diff)
    elif formatter == 'plain':
        return plain.format_plain(diff)
    elif formatter == 'json':
        return json_formatter.format_json(diff)
    else:
        raise ValueError(f"Unknown formatter: {formatter}")
