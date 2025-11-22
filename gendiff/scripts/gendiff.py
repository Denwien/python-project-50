# gendiff/scripts/gendiff.py
import argparse

from gendiff import generate_diff   # БЕРЁМ рабочую функцию из __init__.py


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file", help="Path to the first file")
    parser.add_argument("second_file", help="Path to the second file")
    parser.add_argument(
        "-f",
        "--format",
        default="stylish",
        help="Set format of output (stylish, plain, json). Default: stylish",
    )

    args = parser.parse_args()
    result = generate_diff(args.first_file, args.second_file, args.format)
    print(result)


if __name__ == "__main__":
    main()
