SEPARATOR = " "
ADD_SIGN = "+ "
DEL_SIGN = "- "
NO_SIGN = "  "  # строка без знака (для неизменённых и заголовков блоков)


def _format_value(value, indent_level: int = 2) -> str:
    """Преобразование значения в строку с учётом вложенности."""
    # None -> "null"
    if value is None:
        return "null"

    # bool -> "true"/"false"
    if isinstance(value, bool):
        return str(value).lower()

    # Вложенный словарь – рисуем «коробку»
    if isinstance(value, dict):
        inner_indent = SEPARATOR * (indent_level + 4)
        result_lines = []

        for key, inner_value in value.items():
            formatted_inner = _format_value(inner_value, indent_level + 4)
            result_lines.append(
                f"{inner_indent}{NO_SIGN}{key}: {formatted_inner}"
            )

        closing_indent = SEPARATOR * (indent_level + 2)
        return "{\n" + "\n".join(result_lines) + f"\n{closing_indent}}}"

    # Числа/строки и прочее – просто str()
    return str(value)


def _make_stylish(diff: list[dict], indent_level: int = 2) -> str:
    """Рекурсивное построение stylish-строки по дереву diff."""
    indent = SEPARATOR * indent_level
    lines: list[str] = []

    for node in diff:
        key = node["name"]
        action = node["action"]

        # Вложенный узел – у него есть children
        if action == "nested":
            children_str = _make_stylish(
                node["children"],
                indent_level + 4,
            )
            lines.append(f"{indent}{NO_SIGN}{key}: {children_str}")
            continue

        # Остальные варианты берут значения
        value = _format_value(node.get("value"), indent_level)
        old_value = _format_value(node.get("old_value"), indent_level)
        new_value = _format_value(node.get("new_value"), indent_level)

        if action == "unchanged":
            lines.append(f"{indent}{NO_SIGN}{key}: {value}")
        elif action in ("deleted", "removed"):
            lines.append(f"{indent}{DEL_SIGN}{key}: {old_value}")
        elif action == "added":
            lines.append(f"{indent}{ADD_SIGN}{key}: {new_value}")
        elif action in ("modified", "changed"):
            lines.append(f"{indent}{DEL_SIGN}{key}: {old_value}")
            lines.append(f"{indent}{ADD_SIGN}{key}: {new_value}")
        else:
            raise ValueError(f"Unknown action: {action!r}")

    closing_indent = SEPARATOR * (indent_level - 2)
    return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"


def format_diff_stylish(diff: list[dict]) -> str:
    """Публичная точка входа – форматирование дерева diff в stylish."""
    return _make_stylish(diff)
