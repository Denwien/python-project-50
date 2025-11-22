from collections.abc import Mapping, Sequence

INDENT_SIZE = 4


def stringify(value, depth: int) -> str:
    """
    Преобразует значение в строку с учётом вложенности.
    Словари форматирует с фигурными скобками и отступами по INDENT_SIZE.
    """
    if isinstance(value, dict):
        lines = ["{"]
        inner_indent = " " * ((depth + 1) * INDENT_SIZE)
        closing_indent = " " * (depth * INDENT_SIZE)

        for key, inner_value in sorted(value.items()):
            rendered = stringify(inner_value, depth + 1)
            lines.append(f"{inner_indent}{key}: {rendered}")

        lines.append(f"{closing_indent}}}")
        return "\n".join(lines)

    if value is None:
        return "null"

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def _make_stylish(nodes, depth: int = 0) -> str:
    """
    Собирает строку в формате stylish из списка нод.
    Каждая нода имеет поля: name, action, value/old_value/new_value/children.
    """
    lines: list[str] = ["{"]
    base_indent = " " * (depth * INDENT_SIZE)

    for node in nodes:
        name = node["name"]
        action = node["action"]

        if action == "nested":
            children = node["children"]
            children_repr = _make_stylish(children, depth + 1)
            lines.append(f"{base_indent}    {name}: {children_repr}")
            continue

        if action == "unchanged":
            value_repr = stringify(node["value"], depth + 1)
            lines.append(f"{base_indent}    {name}: {value_repr}")
            continue

        if action == "added":
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


def _is_list_ast(diff) -> bool:
    """
    Проверяет, является ли diff списком нод формата:
    {"name": ..., "action": ...}.
    """
    if not isinstance(diff, Sequence) or isinstance(
        diff,
        (str, bytes, bytearray),
    ):
        return False
    if not diff:
        return False
    return all(
        isinstance(node, Mapping) and "name" in node and "action" in node
        for node in diff
    )



def _is_cli_mapping_ast(diff) -> bool:
    """
    Проверяет, является ли diff "словарием нод" формата, который использует CLI:
    {
        key: { "action": ..., ... },
        ...
    }
    """
    if not isinstance(diff, Mapping):
        return False
    if not diff:
        return False

    has_node = False
    for value in diff.values():
        if isinstance(value, Mapping) and "action" in value:
            has_node = True
        else:
            return False
    return has_node


def _from_cli_mapping_to_nodes(mapping_ast) -> list[Mapping]:
    """
    Конвертирует AST формата CLI (dict name -> node) в список нод вида,
    который понимает _make_stylish.
    """
    nodes: list[Mapping] = []

    for name in sorted(mapping_ast.keys()):
        raw_node = mapping_ast[name]
        if not isinstance(raw_node, Mapping) or "action" not in raw_node:
            # Защита от странных данных: пропускаем неожиданные элементы.
            continue

        node = dict(raw_node)  # копия
        node["name"] = name

        if node["action"] == "nested":
            children = node.get("children")
            if _is_cli_mapping_ast(children):
                node["children"] = _from_cli_mapping_to_nodes(children)

        nodes.append(node)

    return nodes


def format_diff_stylish(diff, depth: int = 0) -> str:
    """
    Универсальная обёртка для форматирования diff в стиль 'stylish'.

    Поддерживает:
    - список нод (формат generate_diff в тестах Hexlet);
    - словарь нод (формат, который использует CLI-обёртка);
    - уже готовую строку (на всякий случай).
    """
    # Уже готовая строка — просто вернуть
    if isinstance(diff, str):
        return diff

    # Список нод
    if _is_list_ast(diff):
        return _make_stylish(diff, depth)

    # CLI-формат: dict name -> node
    if _is_cli_mapping_ast(diff):
        nodes = _from_cli_mapping_to_nodes(diff)
        return _make_stylish(nodes, depth)

    # Одиночная нода
    if isinstance(diff, Mapping) and "name" in diff and "action" in diff:
        return _make_stylish([diff], depth)

    # Фолбэк: честно превращаем в строку как обычное значение
    return stringify(diff, depth)
