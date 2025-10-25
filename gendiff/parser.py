import json
import yaml
from pathlib import Path

def load_file(file_path):
  
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with path.open("r", encoding="utf-8") as f:
        if path.suffix == ".json":
            return json.load(f)
        elif path.suffix in (".yml", ".yaml"):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")