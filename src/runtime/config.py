import tomllib
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
NIRYO_CFG_PATH: Path = PROJECT_ROOT / "configs/niryo_config.toml"

_CFG: dict | None = None

def get_config() -> dict:
    global _CFG
    if _CFG is not None:
        return _CFG

    path = NIRYO_CFG_PATH
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found at path: {path}")

    with path.open("rb") as f:
        data = tomllib.load(f)

    general = data.get("general", {})
    piecewalker = data.get("piecewalker", {})
    _CFG = {
        "path": path,
        "general": general,
        "piecewalker": {
            "robot_ip": str(piecewalker.get("robot_ip", "10.10.10.10")),
            "fixed_z": float(piecewalker.get("fixed_z", 10.0)),
        },
    }
    return _CFG