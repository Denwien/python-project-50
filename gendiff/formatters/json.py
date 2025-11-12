import json


def format_json(diff_tree):
    def transform(node):
        action = node.get("action")

        if action == "nested":
            children_transformed = [
                transform(child) for child in node["children"]
            ]
            merged = {k: v for d in children_transformed for k, v in d.items()}
            return {node["name"]: merged}

        if action == "added":
            val = node.get("new_value", node.get("value"))
            return {node["name"]: val}

        if action == "deleted":
            return {node["name"]: node.get("old_value")}

        if action == "modified":
            old_val = node["old_value"]
            new_val = node["new_value"]
            return {node["name"]: {"old_value": old_val, "new_value": new_val}}

        if action == "unchanged":
            return {node["name"]: node["value"]}

        return {}

    result = {}
    for node in diff_tree:
        result.update(transform(node))

    return json.dumps(result, indent=2)
