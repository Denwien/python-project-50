import json
import os
from typing import Any

import yaml


def parse_data_from_file(file_path: str) -> Any:
    _, extension = os.path.splitext(file_path)
    try:
        with open(file_path) as f:
            if extension in (".yaml", ".yml"):
                return yaml.safe_load(f)
            elif extension == ".json":
                return json.load(f)
            else:
                raise ValueError(
                    f"Unsupported file format: {extension}"
                )
    except (json.JSONDecodeError, yaml.YAMLError) as parse_err:
        raise ValueError(
            f"Failed to parse {file_path}: {parse_err}"
        ) from parse_err
    except OSError as os_err:
        raise OSError(
            f"Failed to read {file_path}: {os_err}"
        ) from os_err
