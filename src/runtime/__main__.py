from ai_placeholder import Ai
from piecewalker.ned2 import Ned2
from runtime import game_loop
from imagedetection.detector import Detector

from .args import parse_args

if __name__ == "__main__":
    args = parse_args()
    ned2 = Ned2()
    ai = Ai(args.model_play)
    detector = Detector(
        board_indices_csv="imagedetection/data/indices/board_indices.csv",
        board_model_path="imagedetection/models/board_best.pt",
        stones_model_path="imagedetection/models/stones_best.pt",
        stacks_model_path="imagedetection/models/stacks_best.pt",
        conf_min=0.25,
        conf_accept=0.45,
        dist_max_factor=0.9,
        black_cls_id=0,
        white_cls_id=1,
    )
    game_loop.run_game_loop(ned2, detector, ai, args.human_start, args.robot_only)
