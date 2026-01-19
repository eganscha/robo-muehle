import random
from pathlib import Path
from typing import Literal, cast

import numpy as np
import torch

from muehle_game import Muehle

from .policy import ThePolicy
from .train import SelfPlayAgent


def load_model(path: Path):
    model = ThePolicy()
    state_dict = torch.load(path, map_location="cpu")
    model.load_state_dict(state_dict)
    return SelfPlayAgent(model)


if __name__ == "__main__":
    game = Muehle()
    model = load_model(Path("models/policy_final.pth"))
    count = 0
    Path("game").mkdir(parents=True, exist_ok=True)

    rendered = game.render()
    rendered.save(f"game/{count}.png")
    count += 1

    legal_moves = np.where(game.legal_actions_mask())[0]
    random_move = 0
    game.move(None, random_move)

    while True:
        rendered = game.render()
        rendered.save(f"game/{count}.png")
        count += 1
        if game.is_terminal():
            print("Game over!")
            break
        s, t, r = model.get_complete_move(game)
        if t is None:
            raise ValueError("Invalid move")
        game.move(s, t)
        if r is not None:
            game.remove_piece(r)
