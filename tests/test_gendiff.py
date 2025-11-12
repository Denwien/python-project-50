from gendiff import generate_diff


def test_diff_json():
    file1 = "tests/test_data/file1.json"
    file2 = "tests/test_data/file2.json"
    expected_file = "tests/test_data/expected_output.yaml"

    result = generate_diff(file1, file2, format_name='stylish')

    with open(expected_file, 'r', encoding='utf-8') as f:
        expected = f.read().strip()

    assert result.strip() == expected

