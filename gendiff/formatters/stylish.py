INDENT = 4
SIGN_INDENT = 2


def format_value(value, depth):
    """Форматирование значения с учётом вложенности."""
    if isinstance(value, dict):
        lines = []
        # базовый отступ для вложенных ключей внутри словаря
        indent = ' ' * ((depth + 1) * INDENT)
        for k, v in value.items():
            lines.append(f"{indent}{k}: {format_value(v, depth + 1)}")
        # закрывающая скобка на уровне текущей глубины
        return "{\n" + "\n".join(lines) + f"\n{' ' * (depth * INDENT)}}}"

    if value is None:
        # Ключевая правка: None должен печататься как "null"
        return "null"

    if isinstance(value, bool):
        # true / false в нижнем регистре
        return str(value).lower()

    # строки, числа и прочее — как есть
    return str(value)

def format_diff_stylish(diff, depth=0):
    """Форматирование списка изменений в stylish"""
    lines = []
    indent = ' ' * (depth * INDENT)

    for item in diff:
        action = item['action']
        name = item['name']

        if action == 'nested':
            lines.append(f"{indent}    {name}: {{")
            lines.append(format_diff_stylish(item['children'], depth + 1))
            lines.append(f"{indent}    }}")
        elif action in ('added',):
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
