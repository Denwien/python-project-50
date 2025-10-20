from gendiff.scripts.load_file import load_file


def generate_diff(file_path1, file_path2):
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)

    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff_lines = []

    for key in all_keys:
        val1 = data1.get(key)
        val2 = data2.get(key)

        if isinstance(val1, dict) and isinstance(val2, dict):
            diff_lines.append({
                "name": key,
                "action": "nested",
                "children": generate_diff(
                    file_path1,
                    file_path2
                )  # рекурсивный diff
            })
        else:
            diff_lines.append({
                "name": key,
                "action": "value",
                "value1": val1,
                "value2": val2
            })

    return diff_lines







