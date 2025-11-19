import argparse
import json

from gendiff.formatters.stylish import format_diff_stylish
from gendiff.scripts.builder import build_diff
from gendiff.scripts.parser import parse_data_from_file as load_file


def generate_diff(file_path1, file_path2, format_name="stylish"):
    """Generate diff between two files in specified format."""
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)
    diff = build_diff(data1, data2)

    if format_name == "stylish":
        return format_diff_stylish(diff)
    if format_name == "json":
        return json.dumps(diff, indent=4)
    raise ValueError(f"Unknown format: {format_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Compares two files and shows the difference."
    )
    parser.add_argument("first_file", help="Path to the first file")
    parser.add_argument("second_file", help="Path to the second file")
    parser.add_argument(
        "-f",
        "--format",
        default="stylish",
        help="Set format of output (default: stylish)",
    )

    args = parser.parse_args()
    output = generate_diff(args.first_file, args.second_file, args.format)
    print(output)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
