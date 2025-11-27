import numpy as np
import pytest

from muehle_game import Muehle


def test_initial_state():
    game = Muehle()
    assert isinstance(game.board, np.ndarray)
    assert game.board.shape[0] == 24
    assert np.all(game.board == 0)
    assert game.done() == 0


def test_reset_board():
    game = Muehle()
    game.board[0] = 1
    game.reset(reinit_board=True)
    assert np.all(game.board == 0)
    assert game.done() == 0


def test_place_piece():
    game = Muehle()
    result = game.move(None, 0)
    assert result in ["ok", "remove"]
    assert game.board[0] in [1, -1]


def test_move_piece():
    game = Muehle()
    game.player = 1
    game.move(None, 0)
    with pytest.raises(Exception):
        game.move(None, 0)
    game.to_place[1] = 0
    game.player = 1
    game.board[1] = -1
    game.board[2] = 1
    game.board[15] = 1
    game.board[16] = 1

    with pytest.raises(Exception):
        game.move(0, 0)
    with pytest.raises(Exception):
        game.move(None, 9)
    with pytest.raises(Exception):
        game.move(0, 1)

    result = game.move(0, 9)
    assert result in ["ok", "remove", "done"]
    assert game.board[9] == 1
    assert game.board[0] == 0


def test_remove_piece():
    game = Muehle()
    game.board[0] = 1
    game.board[1] = -1
    game.player = -1
    game.remove_piece(1)
    assert game.board[1] == 0
    with pytest.raises(Exception):
        game.remove_piece(1)


def test_is_mill_detection():
    game = Muehle()
    game.board[0:3] = 1
    assert game.is_mill(0, 1) is True
    assert game.is_mill(1, 1) is True
    assert game.is_mill(2, 1) is True
    assert game.is_mill(3, 1) is False


def test_jumping_and_moving():
    game = Muehle()
    game.board[0:3] = 1
    game.to_place[1] = 0
    assert game._is_jumping(1) is True
    game.board[3:6] = 1
    assert game._is_moving(1) is True


def test_game_completion():
    game = Muehle()
    game.board[0:3] = 1
    assert game.done() in [0, 1, -1]
