# runtime/args.py
from __future__ import annotations

import argparse
import importlib
import sys
from types import ModuleType
from typing import Any

_ARGS: argparse.Namespace | None = None

def _detect_cli_module_name() -> str:
    """
    Determine which CLI module to use based on the executed -m package.

    Examples:
      python -m runtime                -> runtime.cli
      python -m piecewalker.calibration -> piecewalker.calibration.cli
    """
    main_mod: ModuleType | None = sys.modules.get("__main__")
    pkg = getattr(main_mod, "__package__", None)

    if not pkg:
        # Script executed as a file path: python path/to/something.py
        # In that case, we cannot reliably infer a package CLI without extra rules.
        raise RuntimeError(
            "Cannot infer CLI module because __main__.__package__ is empty. "
            "Run as a module: python -m <package>"
        )

    return f"{pkg}.cli"

def _get_args() -> argparse.Namespace:
    global _ARGS
    if _ARGS is not None:
        return _ARGS

    cli_mod_name = _detect_cli_module_name()
    cli_mod = importlib.import_module(cli_mod_name)

    # Expected contract: cli.py exposes parse_args() -> argparse.Namespace
    parse_args = getattr(cli_mod, "parse_args", None)
    if parse_args is None:
        raise RuntimeError(f"{cli_mod_name} must define parse_args() -> argparse.Namespace")

    _ARGS = parse_args()
    return _ARGS

def get_args_attr(arg: str, default: Any = None) -> Any:
    return getattr(_get_args(), arg, default)