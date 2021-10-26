import os
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
        cols = os.get_terminal_size().columns
        rows = os.get_terminal_size().lines
        board_string = self.get_board_string()

        with open('2048.txt', 'r') as file:
            info_string = file.read()
            info_string += "\n\n"

        if play_mode:
            if not self.is_game_over():
                info_string += "Command-line 2048!\n"
                info_string += """
                Press up, down, left or right to control the board.\n\n
                """
            else:
                info_string += "GAME OVER"
                info_string += "\n\n"

        board_string = info_string + board_string
        board_string_lst = board_string.split('\n')
        print(len(board_string_lst))
        pad_string = "\n"*((rows - len(board_string_lst))//2)
        board_string = pad_string + board_string + pad_string
        for x in board_string:
            print("""\b""")
        for line in board_string.split('\n'):
            print(line.center(cols))

    def get_board_string(self):
        """Get a string representation of the boardstate."""
        board_string = f"Score: {int(self.score)}" + "\n"
        board_string += "+-----"*self.width
        board_string += "+\n"
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
        return board_string

    def update_game(self, action_str):
        """Given an action, update the game state and spawn a new number."""
        new_board, new_score = self.action(action_str)

        if (new_board == self.board).all():
            return

        self.board = new_board
        self.score = new_score
        self.spawn()

    def game_action(self, action_str):
        """Choose action in game mode."""
        if action_str == "up":
            self.update_game("up")
        if action_str == "down":
            self.update_game("down")
        if action_str == "left":
            self.update_game("left")
        if action_str == "right":
            self.update_game("right")
        if action_str == "q":
            sys.exit()
        if action_str == "quit":
            sys.exit()

    def run_game(self, interactive=True):
        """Launch the game."""
        if interactive:
            import keyboard
        self.spawn(2)
        self.print_board()

        while True:
            if interactive:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    key = event.name
                    self.game_action(key)
            else:
                key = input(
                    "Choose action ([u]p, [d]own, [l]eft, [r]ight, [q]uit): "
                )
                if len(key) == 1:
                    letter_dict = {
                        'u': 'up',
                        'd': 'down',
                        'l': 'left',
                        'r': 'right',
                        'q': 'quit',
                    }
                    key = letter_dict[key]
                self.game_action(key)
            self.print_board()
            if self.is_game_over():
                sys.exit()

    def simulate_game(self, strategy_str=None, do_print=True, sleep_time=0):
        """Simulate the game given some sequence of actions."""
        self.spawn(2)
        str_cntr = 0
        action_list = ['up', 'down', 'right', 'left']
        previous_action = ''
        while not self.is_game_over():
            if not strategy_str:
                action = self.rng.choice(
                    [i for i in action_list if i != previous_action],
                    1
                )
                action = action[0]
                self.update_game(action)
                previous_action = action
            else:
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
                if sleep_time:
                    time.sleep(sleep_time)
                self.print_board(play_mode=False)
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
        default=True,
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
        "--interactive",
        dest='interactive',
        default=True,
        help="Run game in interactive mode",
        action='store_true',
    )
    parser.add_argument(
        "--non-interactive",
        dest='interactive',
        help="Run game in non-interactive mode",
        action='store_false',
    )
    parser.add_argument(
        "--strategy",
        default="",
        help="Choose simulation strategy (u=up, d=down, r=right, l=left)",
        type=str,
    )
    parser.add_argument(
        "--sleep-time",
        dest='sleep_time',
        default=0.0,
        help="Set simulation printing speed (waiting time between iterations)",
        type=float,
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
        game.run_game(args.interactive)
    else:
        game.simulate_game(
            args.strategy,
            args.draw,
            args.sleep_time,
        )


if __name__ == '__main__':

    main()
