import argparse
import yaml


def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    return value


def generate_diff(file_path1, file_path2):
    with open(file_path1) as f1, open(file_path2) as f2:
        data1 = yaml.safe_load(f1) or {}
        data2 = yaml.safe_load(f2) or {}

    diff_lines = []
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    # Формируем блоки
    unchanged_block = []
    for key in all_keys:
        if key in data1 and key in data2 and data1[key] == data2[key]:
            unchanged_block.append(f"{key}: {format_value(data1[key])}")
        else:
            # Если есть накопленный блок неизменных ключей — добавляем в diff_lines
            if unchanged_block:
                first = "- " + unchanged_block[0]
                rest = ["  " + line for line in unchanged_block[1:]]
                diff_lines.append(first)
                diff_lines.extend(rest)
                unchanged_block = []

            # Добавляем изменения
            if key in data1 and key not in data2:
                diff_lines.append(f"- {key}: {format_value(data1[key])}")
            elif key not in data1 and key in data2:
                diff_lines.append(f"+ {key}: {format_value(data2[key])}")
            elif key in data1 and key in data2 and data1[key] != data2[key]:
                diff_lines.append(f"- {key}: {format_value(data1[key])}")
                diff_lines.append(f"+ {key}: {format_value(data2[key])}")

    # Если остались неизменные ключи в конце
    if unchanged_block:
        first = "- " + unchanged_block[0]
        rest = ["  " + line for line in unchanged_block[1:]]
        diff_lines.append(first)
        diff_lines.extend(rest)

    return "{\n  " + "\n  ".join(diff_lines) + "\n}"


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

