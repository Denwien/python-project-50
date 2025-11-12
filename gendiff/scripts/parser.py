import json
import os
import yaml
from typing import Any


def parse_data_from_file(file_path: str) -> Any:
    """
    Parse a YAML or JSON file and return its content.

    Args:
        file_path (str): Path to the YAML or JSON file.

    Returns:
        Any: Parsed data (dict, list, etc.).

    Raises:
        ValueError: If file extension is unsupported or parsing fails.
        IOError: If file cannot be read.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension not in (".json", ".yaml", ".yml"):
        raise ValueError(f"Unsupported file format: {extension}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            if extension in (".yaml", ".yml"):
                return yaml.safe_load(f)
            return json.load(f)
    except (json.JSONDecodeError, yaml.YAMLError) as parse_err:
        raise ValueError(f"Failed to parse {file_path}: {parse_err}") from parse_err
    except IOError as io_err:
        raise IOError(f"Failed to read {file_path}: {io_err}") from io_err

