import sys
import time
import argparse
import numpy as np


class Game():
    """Implementation of the game 2048."""

    def __init__(self, rng, width=4, height=4):
        """Initialize the game."""
        self.width = width
        self.height = height
        self.board = np.zeros((self.height, self.width))
        self.rng = rng
        self.score = 0

    def spawn(self, n_spawns=1):
        """Spawn either 2 or 4 in a vacant position on the board."""
        for s in range(n_spawns):
            vacant_positions = self.find_vacant_positions()

            if not vacant_positions.size:
                return

            position = self.rng.choice(len(vacant_positions), 1)[0]
            self.board[
                vacant_positions[position][0],
                vacant_positions[position][1]
            ] = 2 if self.rng.rand() > 0.5 else 4

    def find_vacant_positions(self):
        """Find vacant positions on the board."""
        return np.argwhere(self.board == 0)

    def action(self, action_str):
        """Choose an action."""
        previous_board = self.board.copy()
        new_board = self.board.copy()

        for col in range(self.width):
            empty_places = np.argwhere(new_board[:, col] == 0).flatten()
            non_empty_places = np.argwhere(new_board[:, col] != 0).flatten()
            if len(non_empty_places) == 0:
                continue
            if len(empty_places) == 0:
                continue

            if action_str == "up":
                new_board[
                    :len(non_empty_places),
                    col
                ] = previous_board[non_empty_places, col]
                new_board[
                    -len(empty_places):,
                    col
                ] = previous_board[empty_places, col]

            if action_str == "down":
                new_board[
                    -len(non_empty_places):,
                    col
                ] = previous_board[non_empty_places, col]
                new_board[
                    :len(empty_places),
                    col
                ] = previous_board[empty_places, col]

        for row in range(self.height):
            empty_places = np.argwhere(new_board[row, :] == 0).flatten()
            non_empty_places = np.argwhere(new_board[row, :] != 0).flatten()
            if len(non_empty_places) == 0:
                continue
            if len(empty_places) == 0:
                continue

            if action_str == "left":
                new_board[
                    row,
                    :len(non_empty_places)
                ] = previous_board[row, non_empty_places]
                new_board[
                    row,
                    -len(empty_places):
                ] = previous_board[row, empty_places]

            if action_str == "right":
                new_board[
                    row,
                    -len(non_empty_places):
                ] = previous_board[row, non_empty_places]
                new_board[
                    row,
                    :len(empty_places)
                ] = previous_board[row, empty_places]

        new_board, score = self.merge(action_str, new_board)

        return new_board, score

    def merge(self, action_str, board):
        """Merge adjacent values after action given the action."""
        score = self.score

        if action_str == "up":
            for col in range(self.width):
                for row in range(self.height-1):
                    if board[row, col] == 0:
                        continue
                    if board[row, col] == board[row + 1, col]:
                        board[row, col] = 2*board[row, col]
                        board[row+1:-1, col] = board[row+2:, col]
                        board[-1, col] = 0
                        score += board[row, col]
        if action_str == "down":
            for col in range(self.width):
                for row in range(self.height-1, 0, -1):
                    if board[row, col] == 0:
                        continue
                    if board[row, col] == board[row - 1, col]:
                        board[row, col] = 2*board[row, col]
                        board[1:row, col] = board[:row - 1, col]
                        board[0, col] = 0
                        score += board[row, col]
        if action_str == "left":
            for row in range(self.height):
                for col in range(self.width - 1):
                    if board[row, col] == 0:
                        continue
                    if board[row, col] == board[row, col + 1]:
                        board[row, col] = 2*board[row, col]
                        board[row, col+1:-1] = board[row, col + 2:]
                        board[row, -1] = 0
                        score += board[row, col]
        if action_str == "right":
            for row in range(self.height):
                for col in range(self.width-1, 0, -1):
                    if board[row, col] == 0:
                        continue
                    if board[row, col] == board[row, col - 1]:
                        board[row, col] = 2*board[row, col]
                        board[row, 1:col] = board[row, :col - 1]
                        board[row, 0] = 0
                        score += board[row, col]
        return board, score

    def print_board(self, play_mode=True):
        """Print the game state."""
        board_string = self.get_board_string()
        if play_mode:
            board_string = """
            Command-line 2048!

            Press up, down, left or right to control the board.

            """ + "\n\n" + board_string
        for x in board_string:
            print("""\b""")
        print(board_string, end='')

    def get_board_string(self):
        """Get a string representation of the boardstate."""
        board_string = "+-----"*self.width
        board_string += "+" + 10*" " + f"Score: {int(self.score)}" + "\n"
        for row in self.board:
            board_string += "|"
            for value in row:
                if value:
                    val_str = str(int(value))
                    if len(val_str) == 1:
                        board_string += f"  {val_str}  |"
                    elif len(val_str) == 2:
                        board_string += f"  {val_str} |"
                    elif len(val_str) == 3:
                        board_string += f" {val_str} |"
                    elif len(val_str) == 4:
                        board_string += f" {val_str}|"
                    elif len(val_str) == 5:
                        board_string += f"{val_str}|"
                else:
                    board_string += "     |"
            board_string += "\n"
            board_string += "+-----"*self.width
            board_string += "+\n"
        board_string = f"""{board_string}"""
        return board_string

    def update_game(self, action_str):
        """Given an action, update the game state and spawn a new number."""
        new_board, new_score = self.action(action_str)

        if (new_board == self.board).all():
            return

        self.board = new_board
        self.score = new_score
        self.spawn()

    def run_game(self):
        """Launch the game."""
        import keyboard
        self.spawn(2)
        self.print_board()

        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                if key == "up":
                    self.update_game("up")
                if key == "down":
                    self.update_game("down")
                if key == "left":
                    self.update_game("left")
                if key == "right":
                    self.update_game("right")
                if key == "q":
                    sys.exit()
            self.print_board()
            if self.is_game_over():
                print("Game Over!")
                sys.exit()

    def simulate_game(self, strategy_str='urdl', do_print=True):
        """Simulate the game given some sequence of actions."""
        self.spawn(2)
        str_cntr = 0
        while not self.is_game_over():
            action = strategy_str[str_cntr]
            if action == "u":
                self.update_game("up")
            if action == "d":
                self.update_game("down")
            if action == "l":
                self.update_game("left")
            if action == "r":
                self.update_game("right")
            str_cntr = (str_cntr + 1) % len(strategy_str)

            if do_print:
                # time.sleep(0.1)
                self.print_board(play_mode=True)
        self.print_board(play_mode=False)

    def is_game_over(self):
        """Check if the game should be terminated due to no possible moves."""
        current_board = self.board.copy()
        action_list = [
            "up",
            "down",
            "right",
            "left",
        ]
        if self.find_vacant_positions().size:
            return False

        for action in action_list:
            check_board, check_score = self.action(action)
            if not (check_board == current_board).all():
                return False
        return True

    def clear_board(self):
        """Clear the board."""
        self.board = np.zeros((self.width, self.height))

    def reset_game(self):
        """Reset the game."""
        self.clear_board()
        self.spawn(2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--height",
        default=4,
        help="Choose board height",
        type=int,
    )
    parser.add_argument(
        "--width",
        default=4,
        help="Choose board size width",
        type=int,
    )
    parser.add_argument(
        "--seed",
        default=None,
        help="Choose RNG seed",
        type=int,
    )
    parser.add_argument(
        "--size",
        default=None,
        help="Choose board size (size x size square)",
        type=int,
    )
    parser.add_argument(
        "--play",
        dest='play',
        default=True,
        help="Run in interactive play mode",
        action='store_true',
    )
    parser.add_argument(
        "--simulate",
        dest='play',
        default=False,
        help="Run in simulate mode",
        action='store_false',
    )
    parser.add_argument(
        "--draw",
        dest='draw',
        help="Draw board in simulate mode",
        action='store_true',
    )
    parser.add_argument(
        "--no-draw",
        dest='draw',
        help="Do not draw board in simulate mode",
        action='store_false',
    )
    parser.add_argument(
        "--strategy",
        default="urdl",
        help="Choose simulation strategy (u=up, d=down, r=right, l=left)",
        type=str,
    )
    args = parser.parse_args()
    if args.seed is None:
        rng = np.random.RandomState()
    else:
        rng = np.random.RandomState(args.seed)
    if args.size is None:
        game = Game(
            rng=rng,
            height=args.height,
            width=args.width,
        )
    else:
        game = Game(
            rng=rng,
            height=args.size,
            width=args.size,
        )
    if args.play:
        game.run_game()
    else:
        game.simulate_game(args.strategy, args.draw)


if __name__ == '__main__':

    main()
