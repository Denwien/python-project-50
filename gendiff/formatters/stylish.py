INDENT = 4
SIGN_INDENT = 2  # оставим, даже если сейчас не используем — на логику не влияет


def _stringify(value, depth: int) -> str:
    """
    Преобразует значение в строку с учётом вложенности.

    - словари выводим многострочно в "коробке" { ... }
    - None -> 'null'
    - bool -> 'true' / 'false'
    - остальные типы -> str(value)
    """
    if isinstance(value, dict):
        lines = ['{']
        # сортировка ключей, чтобы порядок был стабильным
        for key, inner_value in sorted(value.items()):
            indent = ' ' * ((depth + 1) * INDENT)
            lines.append(f"{indent}{key}: {_stringify(inner_value, depth + 1)}")
        closing_indent = ' ' * (depth * INDENT)
        lines.append(f"{closing_indent}}}")
        return '\n'.join(lines)

    if value is None:
        return 'null'

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def format_diff_stylish(diff, depth: int = 0) -> str:
    """
    Форматирование АСТ различий в стиль stylish.

    diff — список узлов вида:
    {
        "name": str,
        "action": "nested" | "added" | "deleted" | "removed"
                  | "changed" | "modified" | "unchanged",
        ... значения зависят от action ...
    }
    """
    lines = ['{']
    base_indent = ' ' * (depth * INDENT)

    # Поддержка двух форматов представления diff:
    # 1) список узлов с ключами name/action/... (find_diff)
    # 2) словарь {key: {action: ..., ...}} (builder)
    if isinstance(diff, dict):
        for key in sorted(diff.keys()):
            item = diff[key]
            action = item['action']

            if action == 'nested':
                children_repr = format_diff_stylish(item['children'], depth + 1)
                lines.append(f"{base_indent}    {key}: {children_repr}")
                continue

            if action == 'unchanged':
                value_repr = _stringify(item['value'], depth + 1)
                lines.append(f"{base_indent}    {key}: {value_repr}")
                continue

            if action in ('added',):
                value_repr = _stringify(item['value'], depth + 1)
                lines.append(f"{base_indent}  + {key}: {value_repr}")
                continue

            if action in ('removed', 'deleted'):
                value_repr = _stringify(item['old_value'], depth + 1)
                lines.append(f"{base_indent}  - {key}: {value_repr}")
                continue

            if action in ('changed', 'modified'):
                old_repr = _stringify(item['old_value'], depth + 1)
                new_repr = _stringify(item['new_value'], depth + 1)
                lines.append(f"{base_indent}  - {key}: {old_repr}")
                lines.append(f"{base_indent}  + {key}: {new_repr}")
                continue

            raise ValueError(f"Unknown action in diff node: {action}")
    else:
        for node in diff:
            key = node['name']
            action = node['action']

            # Вложенный объект: рекурсивно форматируем children
            if action == 'nested':
                children_repr = format_diff_stylish(node['children'], depth + 1)
                lines.append(f"{base_indent}    {key}: {children_repr}")
                continue

            # Значение не изменилось
            if action == 'unchanged':
                value_repr = _stringify(node['value'], depth + 1)
                lines.append(f"{base_indent}    {key}: {value_repr}")
                continue

            # Ключ был добавлен
            if action in ('added',):
                value_repr = _stringify(node['value'], depth + 1)
                lines.append(f"{base_indent}  + {key}: {value_repr}")
                continue

            # Ключ был удалён
            if action in ('removed', 'deleted'):
                value_repr = _stringify(node['old_value'], depth + 1)
                lines.append(f"{base_indent}  - {key}: {value_repr}")
                continue

            # Значение изменилось
            if action in ('changed', 'modified'):
                old_repr = _stringify(node['old_value'], depth + 1)
                new_repr = _stringify(node['new_value'], depth + 1)
                lines.append(f"{base_indent}  - {key}: {old_repr}")
                lines.append(f"{base_indent}  + {key}: {new_repr}")
                continue

            # На случай, если в дереве окажется неизвестный action
            raise ValueError(f"Unknown action in diff node: {action}")

    closing_indent = ' ' * (depth * INDENT)
    lines.append(f"{closing_indent}}}")
    return '\n'.join(lines)

