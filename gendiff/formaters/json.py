import json

def format_diff_json(diff):
    def build_dict(diff_list):
        result = {}
        for item in diff_list:
            name = item['name']
            action = item['action']
            if action == 'nested':
                result[name] = build_dict(item['children'])
            elif action == 'changed':
                result[name] = {
                    'old_value': item['old_value'],
                    'new_value': item['new_value'],
                }
            elif action in ('added', 'deleted', 'unchanged'):
                result[name] = item.get('value')
        return result

    structured = build_dict(diff)
    return json.dumps(structured, indent=4)
