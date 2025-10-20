import argparse
from gendiff.scripts.load_file import load_file  # корректный импорт


def format_value(value):
    """Приводим булевы значения к lower-case, остальные оставляем как есть."""
    if isinstance(value, bool):
        return str(value).lower()
    return value


def build_diff(data1, data2):
    """Рекурсивно строит список изменений между двумя словарями."""
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff_lines = []

    for key in all_keys:
        val1 = data1.get(key)
        val2 = data2.get(key)

        if key in data1 and key not in data2:
            diff_lines.append({
                "name": key,
                "action": "deleted",
                "value": val1
            })
        elif key not in data1 and key in data2:
            diff_lines.append({
                "name": key,
                "action": "added",
                "value": val2
            })
        elif isinstance(val1, dict) and isinstance(val2, dict):
            diff_lines.append({
                "name": key,
                "action": "nested",
                "children": build_diff(
                    val1,
                    val2
                )
            })
        elif val1 == val2:
            diff_lines.append({
                "name": key,
                "action": "unchanged",
                "value": val1
            })
        else:
            diff_lines.append({
                "name": key,
                "action": "deleted",
                "value": val1
            })
            diff_lines.append({
                "name": key,
                "action": "added",
                "value": val2
            })

    return diff_lines


def generate_diff(file_path1, file_path2, format_name='stylish'):
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)
    diff_lines = build_diff(data1, data2)

    return "\n" + "\n".join(
        f"{line['action'][:1].rjust(3)} {line['name']}: {format_value(line['value'])}"
        if 'value' in line else
        f"{line['action'][:1].rjust(3)} {line['name']}: {{...}}"
        for line in diff_lines
    ) + "\n"


def parser_function():
    parser = argparse.ArgumentParser(
        description='Compares two YAML files and shows the differences.'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    return parser.parse_args()


def main():
    args = parser_function()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == "__main__":
    main()




