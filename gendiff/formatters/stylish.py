INDENT = 4
SIGN_INDENT = 2


def format_value(value, depth):
    """Форматирование значения с учётом вложенности."""
    if isinstance(value, dict):
        lines = []
        indent = " " * ((depth + 1) * INDENT)
        for key, val in value.items():
            lines.append(f"{indent}{key}: {format_value(val, depth + 1)}")
        closing_indent = " " * (depth * INDENT)
        return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"

    if value is None:
        # None должен печататься как "null"
        return "null"

    if isinstance(value, bool):
        # true / false в нижнем регистре
        return str(value).lower()

    # строки, числа и прочие типы — через str()
    return str(value)


def format_diff_stylish(diff, depth=0):
    """Форматирование списка изменений в формате 'stylish'."""
    lines = []
    indent = " " * (depth * INDENT)

    for item in diff:
        action = item["action"]
        name = item["name"]

        if action == "nested":
            # Узел с дочерними элементами
            lines.append(f"{indent}{' ' * INDENT}{name}: {{")
            lines.append(format_diff_stylish(item["children"], depth + 1))
            lines.append(f"{indent}{' ' * INDENT}}}")
        elif action == "added":
            # Добавленное значение
            lines.append(
                f"{indent}{' ' * (INDENT - SIGN_INDENT)}+ {name}: "
                f"{format_value(item['value'], depth + 1)}",
            )
        elif action in ("removed", "deleted"):
            # Удалённое значение
            lines.append(
                f"{indent}{' ' * (INDENT - SIGN_INDENT)}- {name}: "
                f"{format_value(item.get('old_value'), depth + 1)}",
            )
        elif action in ("changed", "modified"):
            # Изменённое значение — две строки: старая и новая
            lines.append(
                f"{indent}{' ' * (INDENT - SIGN_INDENT)}- {name}: "
                f"{format_value(item['old_value'], depth + 1)}",
            )
            lines.append(
                f"{indent}{' ' * (INDENT - SIGN_INDENT)}+ {name}: "
                f"{format_value(item['new_value'], depth + 1)}",
            )
        elif action == "unchanged":
            # Неизменённое значение
            lines.append(
                f"{indent}{' ' * INDENT}{name}: "
                f"{format_value(item['value'], depth + 1)}",
            )
        else:
            raise ValueError(f"Unknown action: {action}")

    result = "\n".join(lines)
    if depth == 0:
        return "{\n" + result + "\n}"
    return result
