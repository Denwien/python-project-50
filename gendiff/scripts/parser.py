import json
import os
from typing import Any

import yaml


def parse_data_from_file(file_path: str) -> Any:
    """
    Parse a YAML or JSON file and return its content.
    """
    try:
        with open(file_path, "r") as f:
            if file_path.endswith((".yml", ".yaml")):
                return yaml.safe_load(f)
            return json.load(f)
    except (json.JSONDecodeError, yaml.YAMLError) as parse_err:
        raise ValueError(
            f"Failed to parse {file_path}: {parse_err}"
        ) from parse_err
    except IOError as io_err:
        raise IOError(
            f"Failed to read {file_path}: {io_err}"
        ) from io_err