import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference"
    )
    # Позиционные аргументы
    parser.add_argument("first_file", help="Path to the first configuration file")
    parser.add_argument("second_file", help="Path to the second configuration file")

    # Опция для формата вывода
    parser.add_argument(
        "-f", "--format",
        default="plain",
        help="set format of output"
    )

    args = parser.parse_args()

    # Пока просто выводим переданные значения
    print(f"Comparing {args.first_file} with {args.second_file}")
    print(f"Output format: {args.format}")

if __name__ == "__main__":
    main()

