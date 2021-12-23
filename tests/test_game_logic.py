import os
import json
import numpy as np
from NumPy2048.main import CoreGame


def test_game_logic():
    """Game logic test."""
    game = CoreGame()
    test_path = os.path.join("test_files")
    test_dir = os.listdir(test_path)
    for f in test_dir:
        with open(os.path.join(test_path, f)) as fp:
            test_dict = json.load(fp)
        start_board = np.array(test_dict['start_board'])
        out_dict = test_dict['outputs']
        for out in out_dict:
            action = out['action']
            out_board = np.array(out['out_board'])
            out_score = out['score_increment']
            new_board, new_score = game.action(action, start_board, 0)
            assert np.array_equal(new_board, out_board), (
                f"""
                Starting board:\n
                {start_board}
                \n
                with action {action} resulted in board:\n
                {new_board}
                \n
                but should have yielded:\n
                {out_board}
                \n
                """
            )
            assert new_score == out_score, (
                f"""
                Starting board:\n
                {start_board}
                \n
                with action {action} resulted in score increment:\n
                {new_score}
                \n
                but should have yielded:\n
                {out_score}
                \n
                """
            )


def main():
    test_game_logic()


if __name__ == '__main__':
    main()
