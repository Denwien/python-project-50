import argparse
import yaml


def format_value(value):
    """Приводим булевы значения к lower-case, остальные оставляем как есть."""
    if isinstance(value, bool):
        return str(value).lower()
    return value


def generate_diff(file_path1, file_path2):
    with open(file_path1) as f1, open(file_path2) as f2:
        data1 = yaml.safe_load(f1) or {}
        data2 = yaml.safe_load(f2) or {}

    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff_lines = []
    unchanged_block = []

    for key in all_keys:
        val1 = data1.get(key)
        val2 = data2.get(key)

        if val1 == val2:
            unchanged_block.append(f"{key}: {format_value(val1)}")
        else:
            # добавляем предыдущий блок неизменных ключей, если есть
            if unchanged_block:
                diff_lines.append("- " + unchanged_block[0])
                for line in unchanged_block[1:]:
                    diff_lines.append("  " + line)
                unchanged_block = []

            if key in data1 and key not in data2:
                diff_lines.append(f"- {key}: {format_value(val1)}")
            elif key not in data1 and key in data2:
                diff_lines.append(f"+ {key}: {format_value(val2)}")
            else:  # ключ есть в обоих, но значения разные
                diff_lines.append(f"- {key}: {format_value(val1)}")
                diff_lines.append(f"+ {key}: {format_value(val2)}")

    # добавляем оставшийся блок неизменных ключей
    if unchanged_block:
        diff_lines.append("- " + unchanged_block[0])
        for line in unchanged_block[1:]:
            diff_lines.append("  " + line)

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






