import yaml
from pathlib import Path


class ConfigLoaderError(Exception):
    pass


def load_yaml(path: str) -> dict:
    """
    Load YAML file and return its content as dict.
    Raises ConfigLoaderError if file does not exist or is invalid.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise ConfigLoaderError(f"Config file not found: {path}")

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigLoaderError(f"Invalid YAML format in {path}: {e}")

    if data is None:
        raise ConfigLoaderError(f"Config file is empty: {path}")

    return data
