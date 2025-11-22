INDENT = 4
SIGN_INDENT = 2


def format_value(value, depth):
    """Форматирование значения с учётом вложенности"""
    if isinstance(value, dict):
        lines = []
        indent = ' ' * ((depth + 1) * INDENT)
        for k, v in sorted(value.items()):
            lines.append(f"{indent}{k}: {format_value(v, depth + 1)}")
        result = "{\n" + "\n".join(lines) + f"\n{' ' * (depth * INDENT)}}}"
        return result
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def format_diff_stylish(diff, depth=0):
    """Форматирование списка изменений в stylish"""
    lines = []
    indent = ' ' * (depth * INDENT)

    # Определяем, с чем работаем: список или словарь
    items_to_process = []
    
    if isinstance(diff, list):
        # Прямой вызов - список элементов
        items_to_process = [(item.get('name'), item) for item in diff]
    elif isinstance(diff, dict):
        # CLI вызов - словарь
        items_to_process = [(key, value) for key, value in sorted(diff.items())]
    else:
        return ""

    for name, item in items_to_process:
        # Для CLI case, имя берется из ключа, для прямого вызова - из item['name']
        if isinstance(item, dict) and 'action' in item:
            action = item['action']
            # Для прямого вызова имя уже есть в item, для CLI мы используем name из ключа
            actual_name = item.get('name', name)
            
            if action == 'nested':
                lines.append(f"{indent}    {actual_name}: {{")
                lines.append(format_diff_stylish(item['children'], depth + 1))
                lines.append(f"{indent}    }}")
            elif action == 'added':
                lines.append(
                    f"{indent}{' ' * (INDENT - SIGN_INDENT)}+ {actual_name}: "
                    f"{format_value(item['value'], depth + 1)}"
                )
            elif action in ('removed', 'deleted'):
                lines.append(
                    f"{indent}{' ' * (INDENT - SIGN_INDENT)}- {actual_name}: "
                    f"{format_value(item.get('old_value'), depth + 1)}"
                )
            elif action in ('changed', 'modified'):
                lines.append(
                    f"{indent}{' ' * (INDENT - SIGN_INDENT)}- {actual_name}: "
                    f"{format_value(item['old_value'], depth + 1)}"
                )
                lines.append(
                    f"{indent}{' ' * (INDENT - SIGN_INDENT)}+ {actual_name}: "
                    f"{format_value(item['new_value'], depth + 1)}"
                )
            elif action == 'unchanged':
                lines.append(
                    f"{indent}    {actual_name}: {format_value(item['value'], depth + 1)}"
                )
            else:
                raise ValueError(f"Unknown action: {action}")
        else:
            # Если это простой словарь без action (вложенная структура)
            lines.append(f"{indent}    {name}: {format_value(item, depth + 1)}")

    result = "\n".join(lines)
    if depth == 0:
        return "{\n" + result + "\n}"
    return result
