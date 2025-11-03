from gendiff.parser import load_file
from gendiff.builder import build_diff
from gendiff.formaters.stylish import format_diff_stylish
from gendiff.formaters.plain import format_diff_plain

def generate_diff(file_path1: str, file_path2: str, format_name: str = "stylish") -> str:
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)

    diff_tree = build_diff(data1, data2)

    if format_name == "stylish":
        return format_diff_stylish(diff_tree)
    elif format_name == "plain":
        return format_diff_plain(diff_tree)
    else:
        # возвращаем raw diff для отладки или других форматов
        return diff_tree
