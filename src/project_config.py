# Project root is 2 levels up, resolve is its path, so parents [1]


from pathlib import Path
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = PROJECT_ROOT / "configs" / "config.yaml"


def load_config():
    """Load project configuration from config.yaml."""
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


CONFIG = load_config()

RAW_DATA_DIR = PROJECT_ROOT / CONFIG["paths"]["raw_data"]
INTERIM_DATA_DIR = PROJECT_ROOT / CONFIG["paths"]["interim_data"]
PROCESSED_DATA_DIR = PROJECT_ROOT / CONFIG["paths"]["processed_data"]
RESULTS_DIR = PROJECT_ROOT / CONFIG["paths"]["results"]