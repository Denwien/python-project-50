import argparse
import json
from gendiff.scripts.parser import load_file
from gendiff.scripts.builder import build_diff
from gendiff.formatters.stylish import format_diff_stylish


def generate_diff(file_path1, file_path2, format_name="stylish"):
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)
    diff = build_diff(data1, data2)

    if format_name == "stylish":
        return format_diff_stylish(diff)
    if format_name == "json":
        return json.dumps(diff, indent=4)
    return diff


def main():
    parser = argparse.ArgumentParser(
        description="Compares two files and shows the difference."
    )
    parser.add_argument("first_file", help="Path to the first file")
    parser.add_argument("second_file", help="Path to the second file")
    parser.add_argument(
        "-f", "--format",
        default="stylish",
        help="Set format of output (default: stylish)"
    )

    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == "__main__":
    main()
