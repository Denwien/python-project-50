from collections.abc import Mapping, Sequence

INDENT_SIZE = 4


def _stringify(value, depth: int) -> str:
    """
    Преобразует значение в строку с учётом вложенности.
    Словари форматирует с фигурными скобками и правильными отступами.
    """
    if isinstance(value, dict):
        lines = ['{']
        inner_indent = ' ' * ((depth + 1) * INDENT_SIZE)
        closing_indent = ' ' * (depth * INDENT_SIZE)

        for key, inner_value in sorted(value.items()):
            rendered = _stringify(inner_value, depth + 1)
            lines.append(f"{inner_indent}{key}: {rendered}")

        lines.append(f"{closing_indent}}}")
        return "\n".join(lines)

    if value is None:
        return "null"

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def _is_ast_node(node) -> bool:
    """
    Проверяем, похож ли объект на ноду дифа.
    """
    return isinstance(node, Mapping) and "name" in node and "action" in node


def _make_stylish(diff, depth: int = 0) -> str:
    """
    Собирает строку в формате stylish из АСТ (списка нод).
    """
    lines: list[str] = ['{']
    base_indent = ' ' * (depth * INDENT_SIZE)

    for node in diff:
        if not _is_ast_node(node):
            # На всякий случай: если вдруг прилетело что-то не по формату,
            # просто выводим его как строку, не падаем.
            lines.append(f"{base_indent}{_stringify(node, depth + 1)}")
            continue

        name = node["name"]
        action = node["action"]

        if action == "nested":
            children_repr = _make_stylish(node["children"], depth + 1)
            lines.append(f"{base_indent}    {name}: {children_repr}")
            continue

        if action == "unchanged":
            value_repr = _stringify(node["value"], depth + 1)
            lines.append(f"{base_indent}    {name}: {value_repr}")
            continue

        if action == "added":
            value_repr = _stringify(node["value"], depth + 1)
            lines.append(f"{base_indent}  + {name}: {value_repr}")
            continue

        if action in ("removed", "deleted"):
            value_repr = _stringify(node["old_value"], depth + 1)
            lines.append(f"{base_indent}  - {name}: {value_repr}")
            continue

        if action in ("changed", "modified"):
            old_repr = _stringify(node["old_value"], depth + 1)
            new_repr = _stringify(node["new_value"], depth + 1)
            lines.append(f"{base_indent}  - {name}: {old_repr}")
            lines.append(f"{base_indent}  + {name}: {new_repr}")
            continue

        raise ValueError(f"Unknown action in diff node: {action}")

    closing_indent = ' ' * (depth * INDENT_SIZE)
    lines.append(f"{closing_indent}}}")
    return "\n".join(lines)


def format_diff_stylish(diff, depth: int = 0) -> str:
    """
    Универсальная обёртка для форматирования diff в 'stylish'.

    Поддерживает два вида входных данных:
    1) АСТ (список нод с полями 'name'/'action' и др.) — основной путь,
       которым пользуются тесты Hexlet (test_10_diff.py).
    2) Уже готовый вывод в виде строки или списка строк — так может
       вызывать форматтер CLI-обёртка из site-packages, и в этом случае
       форматировать ничего не нужно, важно просто не упасть.
    """
    # 1. Уже готовая строка — просто возвращаем её.
    if isinstance(diff, str):
        return diff

    # 2. Последовательность (list/tuple и т.п.)
    if isinstance(diff, Sequence) and not isinstance(diff, (dict, bytes, bytearray)):
        # 2.1. Все элементы — строки: считаем, что это уже готовые строки вывода.
        if all(isinstance(node, str) for node in diff):
            return "\n".join(diff)

        # 2.2. Все элементы похожи на ноды АСТ: форматируем как обычно.
        if all(_is_ast_node(node) for node in diff):
            return _make_stylish(diff, depth)

    # 3. Одинокая нода (словарь с name/action) — оформляем как список из одной ноды.
    if _is_ast_node(diff):
        return _make_stylish([diff], depth)

    # 4. Фолбэк на случай неожиданного типа: просто аккуратно превращаем в строку.
    return _stringify(diff, depth)
