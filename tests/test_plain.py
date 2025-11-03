from gendiff import generate_diff

def test_plain_format():
    file1 = "tests/test_data/file1.json"
    file2 = "tests/test_data/file2.json"
    expected_file = "tests/test_data/expected_output_plain.txt"

    result = generate_diff(file1, file2, format_name='plain')

    with open(expected_file, 'r', encoding='utf-8') as f:
        expected = f.read().strip()

    assert result.strip() == expected
