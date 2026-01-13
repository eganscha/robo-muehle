from pathlib import Path

import torch

from .policy import ThePolicy
from .train import SelfPlayAgent


def load_model(path: Path):
    model = ThePolicy()
    state_dict = torch.load(path, map_location="cpu")
    model.load_state_dict(state_dict)
    return SelfPlayAgent(model)
