import json
from pathlib import Path
from typing import Any, Dict

import yaml


class Helpers:

    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        with open(filepath, "r") as f:
            return json.load(f)

    @staticmethod
    def load_yaml(filepath: str) -> Dict[str, Any]:
        with open(filepath, "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str, indent: int = 2) -> None:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=indent)

    @staticmethod
    def ensure_dir(path: str) -> Path:
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @staticmethod
    def read_file(filepath: str) -> str:
        with open(filepath, "r") as f:
            return f.read()

    @staticmethod
    def write_file(filepath: str, content: str) -> None:
        with open(filepath, "w") as f:
            f.write(content)
