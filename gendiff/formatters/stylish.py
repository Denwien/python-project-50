INDENT = 4
SIGN_INDENT = 2


def format_value(value, depth):
    """Форматирование значения с учётом вложенности"""
    if isinstance(value, dict):
        lines = []
        indent = ' ' * ((depth + 1) * INDENT)
        for k, v in sorted(value.items()):  # Добавил сортировку для стабильности
            lines.append(f"{indent}{k}: {format_value(v, depth + 1)}")
        result = "{\n" + "\n".join(lines) + f"\n{' ' * (depth * INDENT)}}}"
        return result
    if value is None:
        return "null"  # Исправлено: было "" -> стало "null"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def format_diff_stylish(diff, depth=0):
    """Форматирование списка изменений в stylish"""
    # Добавим отладочную печать
    print(f"DEBUG format_diff_stylish: type(diff) = {type(diff)}")
    print(f"DEBUG format_diff_stylish: diff = {repr(diff)}")
    
    # Если diff - строка, попробуем её распарсить
    if isinstance(diff, str):
        try:
            import json
            diff = json.loads(diff)
            print(f"DEBUG: parsed diff = {diff}")
        except:
            print("DEBUG: cannot parse diff as JSON")
            return diff  # Вернем как есть
    
    lines = []
    indent = ' ' * (depth * INDENT)

    for item in diff:
        print(f"DEBUG item: type = {type(item)}, value = {item}")
        action = item['action']
        name = item['name']

        if action == 'nested':
            lines.append(f"{indent}    {name}: {{")
            lines.append(format_diff_stylish(item['children'], depth + 1))
            lines.append(f"{indent}    }}")
        elif action == 'added':
            lines.append(
                f"{indent}{' ' * (INDENT - SIGN_INDENT)}+ {name}: "
                f"{format_value(item['value'], depth + 1)}"
            )
        elif action in ('removed', 'deleted'):
            lines.append(
                f"{indent}{' ' * (INDENT - SIGN_INDENT)}- {name}: "
                f"{format_value(item.get('old_value'), depth + 1)}"
            )
        elif action in ('changed', 'modified'):
            lines.append(
                f"{indent}{' ' * (INDENT - SIGN_INDENT)}- {name}: "
                f"{format_value(item['old_value'], depth + 1)}"
            )
            lines.append(
                f"{indent}{' ' * (INDENT - SIGN_INDENT)}+ {name}: "
                f"{format_value(item['new_value'], depth + 1)}"
            )
        elif action == 'unchanged':
            lines.append(
                f"{indent}    {name}: {format_value(item['value'], depth + 1)}"
            )
        else:
            raise ValueError(f"Unknown action: {action}")

    result = "\n".join(lines)
    if depth == 0:
        return "{\n" + result + "\n}"
    return result
