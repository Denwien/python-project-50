from gendiff.formaters.stylish import format_diff_stylish

def generate_diff(file_path1, file_path2, format_name='stylish'):
    """Генерация diff между двумя файлами."""
    import json
    import os

    # Чтение файлов
    if not os.path.exists(file_path1) or not os.path.exists(file_path2):
        raise FileNotFoundError("Один из файлов не найден")

    with open(file_path1) as f1, open(file_path2) as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Генерация diff
    diff_list = build_diff(data1, data2)
    
    # Форматирование
    if format_name == 'stylish':
        return format_diff_stylish(diff_list)
    else:
        raise ValueError(f"Unknown format: {format_name}")


def build_diff(data1, data2):
    """Создание списка изменений между двумя словарями."""
    keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff = []

    for key in keys:
        if key not in data1:
            diff.append({"name": key, "action": "added", "value": data2[key]})
        elif key not in data2:
            diff.append({"name": key, "action": "deleted", "value": data1[key]})
        elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
            diff.append({"name": key, "action": "nested", "children": build_diff(data1[key], data2[key])})
        elif data1[key] != data2[key]:
            diff.append({"name": key, "action": "deleted", "value": data1[key]})
            diff.append({"name": key, "action": "added", "value": data2[key]})
        else:
            diff.append({"name": key, "action": "unchanged", "value": data1[key]})

    return diff



