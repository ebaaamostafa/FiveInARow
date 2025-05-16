from abc import abstractmethod


class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return f"Player {self.name} with symbol {self.symbol}"

    @abstractmethod
    def get_move(self, board):
        pass


class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str):
        super().__init__(name, symbol)

    def get_move(self, board):
        """Prompts the human to input a move like 2 3.

        Args:
            board (_type_):

        Returns:
            x, y: input row and column
        """
        move = input(f"{self.name}, enter your move (row and column): ")
        x, y = map(int, move.split())
        return x, y


class AIPlayer(Player):
    def __init__(self, name, symbol, algorithm, depth=3):
        super().__init__(name, symbol)
        self.algorithm = algorithm
        self.depth = depth
        self.opponent_symbol = 'W' if symbol == 'B' else 'B'
        self.is_alpha_beta = 'alpha_beta' in algorithm.__name__

    def get_move(self, board):
        """Gets a move based on selected algorithm (Minimax | Alpha-Beta)

        Args:
            board (_type_): Board to make move on

        Returns:
            x, y: Row and column of AI move 
        """
        print(f"{self.name} is thinking...")

        if self.is_alpha_beta:
            score, x, y = self.algorithm(
                board,
                self.depth,
                float('-inf'),  # alpha
                float('inf'),  # beta
                True,  # is_maximizing
                self.symbol,  # max_player
                self.opponent_symbol  # min_player
            )
        else:
            # minimax
            score, x, y = self.algorithm(
                board,
                self.depth,
                True,  # is_maximizing
                self.symbol,  # max_player
                self.opponent_symbol  # min_player
            )

        print(f"{self.name} chose position ({x}, {y})")
        return x, y
