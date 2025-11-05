import json

def format_json(diff_tree):
    def transform(node):
        action = node.get('action')
        if action == 'nested':
            return {node['name']: {k: v for d in [transform(child) for child in node['children']] for k, v in d.items()}}
        if action == 'added':
            return {node['name']: node.get('new_value', node.get('value'))}
        if action == 'deleted':
            return {node['name']: node.get('old_value')}
        if action == 'modified':
            return {node['name']: {'old_value': node['old_value'], 'new_value': node['new_value']}}
        if action == 'unchanged':
            return {node['name']: node['value']}
        return {}

    result = {}
    for node in diff_tree:
        result.update(transform(node))
    return json.dumps(result, indent=2)
