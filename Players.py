from abc import abstractmethod


class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return f"Player {self.name} with symbol {self.symbol}"

    @abstractmethod
    # takes the board for minimax and alpha-beta pruning
    def get_move(self, board):
        pass


class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str):
        super().__init__(name, symbol)

    def get_move(self, board):
        move = input(f"{self.name}, enter your move (row and column): ")
        x, y = map(int, move.split())
        return x, y


class AIPlayer(Player):
    def __init__(self, name, symbol, algorithm, depth=3):
        super().__init__(name, symbol)
        self.algorithm = algorithm
        self.depth = depth
        self.opponent_symbol = 'W' if symbol == 'B' else 'B'

    def get_move(self, board):
        print(f"{self.name} is thinking...")
        score, x, y = self.algorithm(
            board,
            self.depth,
            True,
            self.symbol,
            self.opponent_symbol
        )
        print(f"{self.name} chose position ({x}, {y})")
        return x, y
