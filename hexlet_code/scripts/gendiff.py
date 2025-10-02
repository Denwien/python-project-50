import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference"
    )

    # Опции
    parser.add_argument(
        "-f", "--format",
        default="plain",
        help="set format of output"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="gendiff 0.1.0",
        help="show program's version number and exit"
    )

    # Позиционные аргументы (необязательные, чтобы -h и --version работали)
    parser.add_argument(
        "first_file",
        nargs="?",
        help="Path to the first configuration file"
    )
    parser.add_argument(
        "second_file",
        nargs="?",
        help="Path to the second configuration file"
    )

    args = parser.parse_args()

    # Если файлы не указаны и не вызвана версия, показать help
    if not args.first_file or not args.second_file:
        parser.print_help()
        return

    # Заглушка: пока просто выводим переданные значения
    print(f"Comparing {args.first_file} with {args.second_file}")
    print(f"Output format: {args.format}")

if __name__ == "__main__":
    main()









