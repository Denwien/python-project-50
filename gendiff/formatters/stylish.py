INDENT_SIZE = 4


def stringify(value, depth: int) -> str:
    """Преобразование значения в строку с учётом вложенности."""
    if isinstance(value, dict):
        lines = ["{"]
        indent = " " * ((depth + 1) * INDENT_SIZE)
        closing_indent = " " * (depth * INDENT_SIZE)

        # Сортируем ключи, чтобы порядок был стабильным
        for key, inner_value in sorted(value.items()):
            lines.append(f"{indent}{key}: {stringify(inner_value, depth + 1)}")

        lines.append(f"{closing_indent}}}")
        return "\n".join(lines)

    if value is None:
        # В YAML-тестах Hexlet ожидается строка 'null', а не пустая строка
        return "null"

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def _make_stylish(diff, depth: int = 0) -> str:
    """Рекурсивная сборка строки в формате stylish из дерева diff."""
    lines = ["{"]
    base_indent = " " * (depth * INDENT_SIZE)

    for node in diff:
        name = node["name"]
        action = node["action"]

        if action == "nested":
            children_repr = _make_stylish(node["children"], depth + 1)
            lines.append(f"{base_indent}    {name}: {children_repr}")
            continue

        if action == "unchanged":
            value_repr = stringify(node["value"], depth + 1)
            lines.append(f"{base_indent}    {name}: {value_repr}")
            continue

        if action in ("added",):
            value_repr = stringify(node["value"], depth + 1)
            lines.append(f"{base_indent}  + {name}: {value_repr}")
            continue

        if action in ("removed", "deleted"):
            value_repr = stringify(node["old_value"], depth + 1)
            lines.append(f"{base_indent}  - {name}: {value_repr}")
            continue

        if action in ("changed", "modified"):
            old_repr = stringify(node["old_value"], depth + 1)
            new_repr = stringify(node["new_value"], depth + 1)
            lines.append(f"{base_indent}  - {name}: {old_repr}")
            lines.append(f"{base_indent}  + {name}: {new_repr}")
            continue

        raise ValueError(f"Unknown action in diff node: {action}")

    closing_indent = " " * (depth * INDENT_SIZE)
    lines.append(f"{closing_indent}}}")
    return "\n".join(lines)


def format_diff_stylish(diff) -> str:
    """
    Внешняя функция форматтера для стиля 'stylish'.

    Важно: в CLI-обёртке Hexlet есть баг — туда иногда прилетает уже
    готовая строка, а не дерево diff. В этом случае просто возвращаем
    строку как есть, чтобы избежать TypeError.
    """
    if isinstance(diff, str):
        # Защита для CLI: если нам передали уже форматированную строку,
        # не пытаемся интерпретировать её как список узлов.
        return diff

    return _make_stylish(diff)
