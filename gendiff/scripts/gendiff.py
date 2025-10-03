import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.\n",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="options::\n  -h, --help            show this help message and exit\n  -f FORMAT, --format FORMAT\n                        set format of output"
    )

    # Опции
    parser.add_argument(
        "-f", "--format",
        default="plain",
        help=argparse.SUPPRESS  
    )

    
    parser.add_argument("first_file", help="Path to the first configuration file")
    parser.add_argument("second_file", help="Path to the second configuration file")

    args = parser.parse_args()

    print(f"Comparing {args.first_file} with {args.second_file}")
    print(f"Output format: {args.format}")

if __name__ == "__main__":
    main()


















