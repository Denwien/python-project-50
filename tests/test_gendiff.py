import pytest
from gendiff.scripts.gendiff import generate_diff

def test_generate_diff():
    result = generate_diff('file1.txt', 'file2.txt', formatter='stylish')
    assert "Diff between file1.txt and file2.txt" in result


