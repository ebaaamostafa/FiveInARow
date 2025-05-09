from abc import abstractmethod
class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return f"Player {self.name} with symbol {self.symbol}"

    @abstractmethod
    # takes the board for minimax and alpha-beta pruning
    def get_move(self,board):
        pass


class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str):
        super().__init__(name, symbol)

    def get_move(self,board):
        move = input(f"{self.name}, enter your move (row and column): ")
        x, y = map(int, move.split())
        return x, y



class AIPlayer(Player):
    def __init__(self, name: str, symbol: str):
        super().__init__(name, symbol)

    def get_move(self,board):
        # after implementing minimax and alpha-beta pruning
        pass
