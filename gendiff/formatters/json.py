import json


def format_json(diff_tree):
    """
    Форматирует дерево изменений в JSON.
    """

    def transform(node):
        action = node.get("action")
        if action == "nested":
            return {
                node["name"]: [transform(child) for child in node["children"]]
            }
        elif action == "added":
            return {node["name"]: node["value"]}
        elif action == "deleted":
            return {node["name"]: node["old_value"]}
        elif action == "modified":
            return {
                node["name"]: {
                    "old_value": node["old_value"],
                    "new_value": node["new_value"],
                }
            }
        elif action == "unchanged":
            return {node["name"]: node["value"]}
        return node

    # Merge all transformed nodes into a single dict
    result = {}
    for node in diff_tree:
        result.update(transform(node))

    return json.dumps(result, indent=2)
