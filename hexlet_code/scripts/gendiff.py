#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference"
    )
    parser.add_argument("first_file", help="Path to the first configuration file")
    parser.add_argument("second_file", help="Path to the second configuration file")
    args = parser.parse_args()

    # Пока заглушка
    print(f"Comparing {args.first_file} with {args.second_file}")

if __name__ == "__main__":
    main()
