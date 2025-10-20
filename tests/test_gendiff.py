from gendiff.scripts.gendiff import generate_diff

def test_diff_json():
    expected_file = "tests/test_data/expected_output.yaml"
    result = generate_diff(
        "tests/test_data/file1.json",
        "tests/test_data/file2.json",
        format_name='stylish'
    )
    with open(expected_file) as f:
        expected = f.read()
    assert result == expected
