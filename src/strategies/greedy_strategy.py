class GreedyStrategy():
    """Greedy strategy for 2048."""

    def __init__(self, game, search_depth=0):
        """Initialize the class."""
        self.game = game
        self.search_depth = search_depth
        self.action_list = [
            'up',
            'down',
            'left',
            'right',
        ]
        self.recent_actions = self.action_list.copy()

    def find_current_best_move(self, board):
        """Find the best move given the current board."""
        if self.game.action_history:
            best_action = self.game.action_history[-1]
        else:
            best_action = 'up'
        best_improvement = 0
        for action in self.recent_actions:
            _, score = self.game.action(action, board, 0)
            if score > best_improvement:
                best_action = action
                best_improvement = score
        if self.game.valid_action(best_action, board):
            self.recent_actions = [best_action] + [
                i for i in self.recent_actions if i != best_action
            ]
            return best_action
        else:
            best_action = self.game.rng.choice(
                self.action_list
            )
            return best_action

    def apply(self):
        """Apply the greedy strategy."""
        while not self.game.is_game_over():
            self.game.draw_game()
            action = self.find_current_best_move(self.game.board)
            self.game.game_action(action)


def main():
    import sys
    sys.path.append(
        "/Users/wilhelmsoderqvistwermelin/Documents/Python/Projects/2048/src/"
    )
    from main import TerminalGame
    import numpy as np
    rng = np.random.RandomState()

    game = TerminalGame(rng)
    strat = GreedyStrategy(game)
    final_board, final_score = strat.apply()
    print(final_board)
    print(final_score)
    return strat


if __name__ == '__main__':

    strat = main()
