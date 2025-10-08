import json
from pathlib import Path
import pytest
from gendiff.scripts.gendiff import generate_diff

TEST_DATA_DIR = Path(__file__).parent / "test_data"

def test_generate_diff_matches_expected():
    file1 = TEST_DATA_DIR / "file1.json"
    file2 = TEST_DATA_DIR / "file2.json"
    expected_diff_file = TEST_DATA_DIR / "expected_diff.txt"

    # читаем ожидаемый результат
    expected_diff = expected_diff_file.read_text(encoding="utf-8").strip()

    # генерируем diff
    diff = generate_diff(str(file1), str(file2)).strip()

    assert diff == expected_diff
