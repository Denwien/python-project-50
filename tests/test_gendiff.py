import pytest
from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_files():
    file1 = "tests/test_data/file1.yml"
    file2 = "tests/test_data/file2.yml"

    expected_output = """{
  - follow: false
    host: hexlet.io
    proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""

    result = generate_diff(file1, file2)
    assert result == expected_output




