from ai_placeholder import Ai
from muehle_game import Muehle
from piecewalker.ned2 import Ned2
from yolo_detection.detector import Detector


def run_game_loop(robot: Ned2, detector: Detector, ai: Ai):
    game = Muehle()
    while True:
        # todo: update
        detector.get_next_gamestate(game)
        if game.is_terminal():
            break
        from_idx, to, remove = ai.next_move(game)
        robot.move(from_idx=from_idx, to_idx=to)
        if remove:
            robot.move(from_idx=remove, to_idx=None)
        if game.is_terminal():
            break
