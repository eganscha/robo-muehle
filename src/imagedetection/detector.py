from ultralytics import YOLO

from board_geometry import BoardIndexMap
from homography import warp_from_corners
from index_mapping import nearest_index, estimate_grid_spacing_px, build_state_dict
from morris_ascii import render_morris_ascii
from vision.stone_center import stone_centers
from vision.board_bbox import best_board_box, corners_from_bbox
from vision.debug_vis import _resize_to_height, _hstack_safe


class Detector:
    def __init__(
        self,
        board_indices_csv: str,
        board_model_path: str | None=None,
        stones_model_path: str | None=None,
        stacks_model_path: str | None=None,
        conf_min: float = 0.25,
        conf_accept: float = 0.45,
        dist_max_factor: float = 0.9,
        black_cls_id: int = 0,
        white_cls_id: int = 1,
    ):
        self.board = BoardIndexMap(board_indices_csv)
        self.board_model = YOLO(board_model_path) if board_model_path else None
        self.stones_model = YOLO(stones_model_path) if stones_model_path else None
        self.stacks_model = YOLO(stacks_model_path) if stacks_model_path else None
        self.conf_min = conf_min
        self.conf_accept = conf_accept
        self.dist_max_factor = dist_max_factor
        self.black_cls_id = black_cls_id
        self.white_cls_id = white_cls_id

        grid = estimate_grid_spacing_px(self.board)
        self.dist_max = self.dist_max_factor * grid


    def get_gamestate(self, img_bgr):
        
        board_res0 = self.board_model(img_bgr)[0]
        box = best_board_box(board_res0)
        if box is None:
            raise RuntimeError("No board detected")

        corners = corners_from_bbox(*box)
        warped, H = warp_from_corners(img_bgr, corners)

        
        stones_res0 = self.stones_model(warped)[0]
        
        best_per_idx = {}

        for cls_id, conf, cx, cy in stone_centers(stones_res0, conf_thres=self.conf_min):
            idx, dist = nearest_index(cx, cy, self.board)
            if idx is None:
                continue

            if dist > self.dist_max:
                continue

            candidate = {
                "cls_id": cls_id, 
                "conf": conf, 
                "cx": cx, 
                "cy": cy, 
                "dist": dist
            }

            if idx not in best_per_idx:
                best_per_idx[idx] = candidate
            else:
                prev = best_per_idx.get(idx)
                if (prev is None
                    or candidate["conf"] > prev["conf"]
                    or (candidate["conf"] == prev["conf"] and candidate["dist"] < prev["dist"])):
                    best_per_idx[idx] = candidate

        accepted_per_idx = {
            i: d for i, 
            d in best_per_idx.items() if d["conf"] >= self.conf_accept
        }

        vis_orig = board_res0.plot(img=img_bgr.copy())
        
        if self.stacks_model is not None:
            stacks_res0 = self.stacks_model(img_bgr)[0]
            vis_orig = stacks_res0.plot(img=vis_orig)

        vis_warp = stones_res0.plot(img=warped.copy())


        state = build_state_dict(
            self.board, 
            accepted_per_idx, 
            black_cls_id=self.black_cls_id, 
            white_cls_id=self.white_cls_id
        )

        remap = {-1: 0, 0: -1, 1: 1}
        state = {i: remap[v] for i, v in state.items()}


        ascii_board = render_morris_ascii(state, mode="value")


        h = 560
        left = _resize_to_height(vis_orig, h)
        right = _resize_to_height(vis_warp, h)
        
        debug_vis = _hstack_safe(left, right)


        order = self.board.get_abs_indices()
        state_arr = [state[i] for i in order]


        return state, {
            "H": H, 
            "ascii": ascii_board,
            "debug_vis": debug_vis,
            "state_arr": state_arr
        }
