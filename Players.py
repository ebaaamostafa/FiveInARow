class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return f"Player {self.name} with symbol {self.symbol}"

    def get_move(self):
        pass


class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str):
        super().__init__(name, symbol)

    def get_move(self):
        move = input(f"{self.name}, enter your move (row and column): ")
        x, y = map(int, move.split())
        return x, y



class AIPlayer(Player):
    def __init__(self, name: str, symbol: str):
        super().__init__(name, symbol)

    def get_move(self):
        # after implementing minimax and alpha-beta pruning
        pass
