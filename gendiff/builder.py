def build_diff(data1, data2):
    """Строит дерево различий в формате словаря."""
    keys = sorted(data1.keys() | data2.keys())
    diff = {}

    for key in keys:
        if key not in data1:
            diff[key] = {"action": "added", "value": data2[key]}
        elif key not in data2:
            diff[key] = {"action": "deleted", "old_value": data1[key]}
        else:
            val1, val2 = data1[key], data2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                children = build_diff(val1, val2)
                diff[key] = {"action": "nested", "children": children}
            elif val1 == val2:
                diff[key] = {"action": "unchanged", "value": val1}
            else:
                diff[key] = {"action": "modified", "old_value": val1, "new_value": val2}
    return diff
