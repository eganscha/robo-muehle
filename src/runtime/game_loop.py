from ai_placeholder import Ai
from muehle_game import Muehle
from piecewalker.ned2 import Ned2
from yolo_detection.detector import Detector


def run_game_loop(robot: Ned2, detector: Detector, ai: Ai, human_start):
    game = Muehle()
    skip_first = not human_start
    while True:
        if not skip_first:
            # todo: update
            detector.get_next_gamestate(game)
            skip_first = False
            if game.is_terminal():
                break
        from_idx, to, remove = ai.next_complete_move(game)
        robot.move(from_idx=from_idx, to_idx=to)
        if remove:
            robot.move(from_idx=remove, to_idx=None)
        if game.is_terminal():
            break
