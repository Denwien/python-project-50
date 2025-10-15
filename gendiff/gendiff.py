import os
import json
import yaml
from gendiff.formaters.stylish import format_diff_stylish as format_stylish

def load_file(filepath):
    """Загружает JSON или YAML файл и возвращает словарь."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        if filepath.endswith('.json'):
            return json.load(f)
        elif filepath.endswith(('.yml', '.yaml')):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format: must be .json, .yml or .yaml")


def build_diff(dict1, dict2):
    """Строит промежуточный словарь diff с ключами и статусами."""
    keys = sorted(set(dict1.keys()) | set(dict2.keys()))
    diff = {}

    for key in keys:
        if key not in dict1:
            diff[key] = {'status': 'added', 'value': dict2[key]}
        elif key not in dict2:
            diff[key] = {'status': 'deleted', 'value': dict1[key]}
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            diff[key] = {'status': 'nested', 'value': build_diff(dict1[key], dict2[key])}
        elif dict1[key] != dict2[key]:
            diff[key] = {'status': 'modified', 'old_value': dict1[key], 'value': dict2[key]}
        else:
            diff[key] = {'status': 'unchanged', 'value': dict1[key]}
    return diff


def dict_to_list_diff(diff_dict):
    """Конвертирует словарь diff в список словарей для make_stylish_diff."""
    result = []
    for key, info in sorted(diff_dict.items()):
        status = info['status']
        if status == 'nested':
            children = dict_to_list_diff(info['value'])
            result.append({'name': key, 'action': 'nested', 'children': children})
        elif status == 'added':
            result.append({'name': key, 'action': 'added', 'value': info['value']})
        elif status == 'deleted':
            result.append({'name': key, 'action': 'deleted', 'old_value': info['value']})
        elif status == 'modified':
            result.append({'name': key, 'action': 'modified',
                           'old_value': info['old_value'], 'new_value': info['value']})
        else:  # unchanged
            result.append({'name': key, 'action': 'unchanged', 'value': info['value']})
    return result


def generate_diff(file1, file2, format_name='stylish'):
    """Генерирует diff между двумя файлами в заданном формате."""
    dict1 = load_file(file1)
    dict2 = load_file(file2)
    diff_dict = build_diff(dict1, dict2)
    diff_list = dict_to_list_diff(diff_dict)

    if format_name == 'stylish':
        return format_stylish(diff_list)
    else:
        raise ValueError(f"Unsupported format: {format_name}")

