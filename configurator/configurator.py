from contracts.settings import Config
import json
import os
import dataclasses
from pathlib import Path

def _get_config_path() -> Path:
    app_name = "IRSProject"
    if os.name == 'nt':
        base_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
    else:
        base_dir = os.environ.get('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config'))
    
    config_dir = Path(base_dir) / app_name
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def set_config(config: Config) -> None:
    path = _get_config_path()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dataclasses.asdict(config), f, indent=4)


def get_config() -> Config:
    path = _get_config_path()
    if not path.exists():
        return Config()
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return Config(**data)
    except (json.JSONDecodeError, TypeError, KeyError):
        return Config()