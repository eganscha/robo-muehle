import tomllib

from runtime.paths import Paths, build_paths

_CFG: dict | None = None

def get_config() -> dict:
    global _CFG
    if _CFG is not None:
        return _CFG

    paths: Paths = build_paths()
    path = paths.niryo_cfg_path
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