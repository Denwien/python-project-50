from gendiff import generate_diff

def test_json_format():
    file1 = "tests/test_data/file1.json"
    file2 = "tests/test_data/file2.json"

    result = generate_diff(file1, file2, format_name='json')
    
    import json
    parsed = json.loads(result)
    
    assert isinstance(parsed, dict)
    assert 'common' in parsed or 'group1' in parsed
