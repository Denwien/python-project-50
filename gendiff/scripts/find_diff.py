def find_diff(first_data, second_data):
    diff = []
    all_keys = list(first_data.keys()) + [
        k for k in second_data.keys() if k not in first_data
    ]

    for key in all_keys:
        if key not in first_data:
            diff.append({"name": key, "action": "added", "value": second_data[key]})
        elif key not in second_data:
            diff.append({"name": key, "action": "deleted",
                         "old_value": first_data[key]})
        else:
            first_value = first_data[key]
            second_value = second_data[key]

            if isinstance(first_value, dict) and isinstance(second_value, dict):
                children_diff = find_diff(first_value, second_value)
                diff.append({"name": key, "action": "nested",
                             "children": children_diff})
            elif first_value == second_value:
                diff.append({"name": key, "action": "unchanged",
                             "value": first_value})
            else:
                diff.append({
                    "name": key,
                    "action": "modified",
                    "old_value": first_value,
                    "new_value": second_value
                })

    return diff
