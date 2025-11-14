def find_diff(first_data, second_data):
    """
    Создает diff между двумя словарями в виде списка словарей с ключами:
    'name', 'action', 'value', 'old_value', 'new_value', 'children'.
    """
    diff = []

    all_keys = sorted(set(first_data.keys()) | set(second_data.keys()))

    for key in all_keys:
        if key not in first_data:
            # ключ есть только во втором словаре → добавлено
            diff.append(
                {"name": key, "action": "added", "value": second_data[key]}
            )
        elif key not in second_data:
            # ключ есть только в первом словаре → удалено
            diff.append(
                {
                    "name": key,
                    "action": "deleted",
                    "old_value": first_data[key],
                }
            )
        else:
            first_value = first_data[key]
            second_value = second_data[key]

            if isinstance(first_value, dict) and isinstance(second_value, dict):
                # рекурсивно для вложенных словарей
                children_diff = find_diff(first_value, second_value)
                diff.append(
                    {
                        "name": key,
                        "action": "nested",
                        "children": children_diff,
                    }
                )
            elif first_value == second_value:
                # без изменений
                diff.append(
                    {"name": key, "action": "unchanged", "value": first_value}
                )
            else:
                # изменено
                diff.append(
                    {
                        "name": key,
                        "action": "modified",
                        "old_value": first_value,
                        "new_value": second_value,
                    }
                )

    return diff
