from gendiff.parser import load_file
from gendiff.builder import build_diff
from gendiff.formaters.stylish import format_diff_stylish

def generate_diff(file_path1: str, file_path2: str, format_name: str = "stylish") -> str:
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)

    diff_tree = build_diff(data1, data2)

    if format_name == "stylish":
        return format_diff_stylish(diff_tree)
    return diff_tree
