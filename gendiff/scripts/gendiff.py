import argparse
from pathlib import Path
import json


def read_file(file_path: str) -> dict:
    
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("first_file", help="Path to the first configuration file")
    parser.add_argument("second_file", help="Path to the second configuration file")

    args = parser.parse_args()

    
    file1_data = read_file(args.first_file)
    file2_data = read_file(args.second_file)

    print("File 1 data:", file1_data)
    print("File 2 data:", file2_data)


if __name__ == "__main__":
    main()






















