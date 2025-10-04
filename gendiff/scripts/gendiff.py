import argparse
from pathlib import Path
import json


def read_file(file_path: str) -> dict:
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_diff(file1_path: str, file2_path: str) -> str:
    file1_data = read_file(file1_path)
    file2_data = read_file(file2_path)

    all_keys = sorted(file1_data.keys() | file2_data.keys())
    lines = ["{"]
    for key in all_keys:
        val1 = file1_data.get(key)
        val2 = file2_data.get(key)
        if key in file1_data and key not in file2_data:
            lines.append(f"  - {key}: {val1}")
        elif key not in file1_data and key in file2_data:
            lines.append(f"  + {key}: {val2}")
        elif val1 != val2:
            lines.append(f"  - {key}: {val1}")
            lines.append(f"  + {key}: {val2}")
        else:
            lines.append(f"    {key}: {val1}")
    lines.append("}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("first_file", help="Path to the first configuration file")
    parser.add_argument("second_file", help="Path to the second configuration file")

    args = parser.parse_args()

    diff = generate_diff(args.first_file, args.second_file)
    print(diff)


if __name__ == "__main__":
    main()

























