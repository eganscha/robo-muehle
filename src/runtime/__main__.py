from ai_placeholder import Ai
from piecewalker.ned2 import Ned2
from runtime import game_loop
from yolo_detection.detector import Detector

from .args import parse_args

if __name__ == "__main__":
    args = parse_args()
    ned2 = Ned2()
    ai = Ai(args.model_play)
    detector = Detector()
    game_loop.run_game_loop(ned2, detector, ai, args.human_start, args.robot_only)
