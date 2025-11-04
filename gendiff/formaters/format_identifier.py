from .stylish import format_diff_stylish
from .plain import format_diff_plain

def format_identifier(diff, formatter_name='stylish'):
    if formatter_name == 'stylish':
        return format_diff_stylish(diff)
    elif formatter_name == 'plain':
        return format_diff_plain(diff)
    else:
        raise ValueError(f"Unknown formatter: {formatter_name}")
