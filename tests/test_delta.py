from imagedetection.detector import Detector

def test_delta_move_capture():
    det = Detector(board_indices_csv="src/imagedetection/data/indices/board_indices.csv")

    prev = [0]*24
    prev[5] = 1
    prev[20] = -1

    curr = [0]*24
    curr[9] = 1   # moved to 9
    # 5 becomes 0, 20 becomes 0

    delta = det._infer_human_delta(prev, curr)
    assert delta["from_idx"] == 5
    assert delta["to_idx"] == 9
    assert delta["remove_idx"] == 20
    assert delta["player"] == 1
