from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
DEFAULT_CONFIGS_DIR: Path = PROJECT_ROOT / "configs"

@dataclass(frozen=True)
class Paths:
    project_root: Path
    configs_dir: Path
    calibrations_dir: Path
    niryo_cfg_path: Path

def build_paths(*, configs_dir: Path) -> Paths:
    cfg_dir = configs_dir.resolve()
    return Paths(
        project_root=PROJECT_ROOT,
        configs_dir=cfg_dir,
        calibrations_dir=cfg_dir / "calibrations",
        niryo_cfg_path=cfg_dir / "niryo_config.toml",
    )