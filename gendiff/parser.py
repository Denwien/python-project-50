import json
import yaml
from pathlib import Path

def load_file(file_path: str):
    path = Path(file_path)
    ext = path.suffix.lower()

    with open(file_path, "r") as f:
        if ext in [".json"]:
            return json.load(f)
        if ext in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        raise ValueError(f"Unsupported file format: {ext}")
