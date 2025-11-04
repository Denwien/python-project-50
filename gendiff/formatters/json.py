import json

def format_diff_json(diff):
    def serialize(diff_list):
        result = {}
        for item in diff_list:
            name = item['name']
            action = item['action']
            if action == 'nested':
                result[name] = serialize(item['children'])
            elif action == 'added':
                result[name] = item.get('value')
            elif action == 'deleted':
                result[name] = None
            elif action == 'changed':
                result[name] = {
                    'old_value': item.get('old_value'),
                    'new_value': item.get('new_value')
                }
            else:  # unchanged
                result[name] = item.get('value')
        return result

    return json.dumps(serialize(diff), indent=4)
