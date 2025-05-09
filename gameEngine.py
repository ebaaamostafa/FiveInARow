import rules, Players, Board, AIPlayer


# while game is running
#   take current state
#   apply search algorithm and limit search space to specified depth limit
#   move
#   send chosen move and state to user and display

class GameEngine:
    def __init__(self, player1: Players.Player, player2: Players.Player, board_size: int = 15):
        self.board = Board.Board(board_size)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

    def start(self):
        while True:
            self.board.display()
            print(f"{self.current_player.name}'s turn ({self.current_player.symbol})")
            x, y = self.current_player.get_move(self.board)
            if not self.board.place_stone(x, y, self.current_player.symbol):
                print("Invalid move. Try again.")
                continue

            if self.board.check_winner(self.current_player.symbol):
                self.board.display()
                print(f"{self.current_player.name} wins!")
                break

            if self.board.check_draw():
                self.board.display()
                print("It's a draw!")
                break

            # Switch players
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
