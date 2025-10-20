import argparse
from gendiff.scripts.load_file import load_file  # ваш корректный импорт

SEPARATOR = "  "
ADD = "+ "
DEL = "- "
UNCHANGED = "  "


def format_value(value, depth=0):
    """Форматирование значения с отступами, без {} для вложенных dict."""
    if isinstance(value, dict):
        lines = []
        for k in sorted(value):
            lines.append(f"{'    ' * (depth + 1)}{k}: {format_value(value[k], depth + 1)}")
        return "\n".join(lines)
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def build_diff(data1, data2):
    """Рекурсивно строит diff между двумя словарями."""
    diff_lines = []
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    for key in all_keys:
        val1 = data1.get(key)
        val2 = data2.get(key)

        if key not in data1:
            diff_lines.append({"name": key, "action": "added", "value": val2, "children": []})
        elif key not in data2:
            diff_lines.append({"name": key, "action": "deleted", "value": val1, "children": []})
        elif isinstance(val1, dict) and isinstance(val2, dict):
            diff_lines.append({
                "name": key,
                "action": "nested",
                "children": build_diff(val1, val2)
            })
        elif val1 == val2:
            diff_lines.append({"name": key, "action": "unchanged", "value": val1, "children": []})
        else:
            diff_lines.append({"name": key, "action": "deleted", "value": val1, "children": []})
            diff_lines.append({"name": key, "action": "added", "value": val2, "children": []})
    return diff_lines


def make_stylish(diff, depth=0):
    """Конвертирует diff в стильный формат с отступами."""
    lines = []
    indent = SEPARATOR * depth
    for node in diff:
        key = node["name"]
        action = node["action"]
        if action == "nested":
            lines.append(f"{indent}{UNCHANGED}{key}:")
            lines.extend(make_stylish(node["children"], depth + 1))
        elif action == "added":
            value = format_value(node["value"], depth)
            lines.append(f"{indent}{ADD}{key}: {value}")
        elif action == "deleted":
            value = format_value(node["value"], depth)
            lines.append(f"{indent}{DEL}{key}: {value}")
        else:  # unchanged
            value = format_value(node["value"], depth)
            lines.append(f"{indent}{UNCHANGED}{key}: {value}")
    return lines


def format_diff_stylish(diff):
    return "\n".join(make_stylish(diff))


def generate_diff(file_path1, file_path2, format_name="stylish"):
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)
    diff = build_diff(data1, data2)
    if format_name == "stylish":
        return format_diff_stylish(diff)
    return diff


def parser_function():
    parser = argparse.ArgumentParser(
        description="Compares two files and shows the differences in stylish format."
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    return parser.parse_args()


def main():
    args = parser_function()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == "__main__":
    main()




