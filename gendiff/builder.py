def build_diff(data1, data2):
    diff_lines = []
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    for key in all_keys:
        val1 = data1.get(key)
        val2 = data2.get(key)

        if key not in data1:
            diff_lines.append({
                "name": key,
                "action": "added",
                "value": val2,
                "children": []
            })
        elif key not in data2:
            diff_lines.append({
                "name": key,
                "action": "deleted",
                "value": val1,
                "children": []
            })
        elif isinstance(val1, dict) and isinstance(val2, dict):
            diff_lines.append({
                "name": key,
                "action": "nested",
                "children": build_diff(val1, val2)
            })
        elif val1 == val2:
            diff_lines.append({
                "name": key,
                "action": "unchanged",
                "value": val1,
                "children": []
            })
        else:
            diff_lines.append({
                "name": key,
                "action": "changed",
                "old_value": val1,
                "new_value": val2,
                "children": []
            })

    return diff_lines







