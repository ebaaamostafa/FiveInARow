import Players, Board


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
        """
        ### This is where the game is actually played.
        #### An infinite loop runs until someone wins or the game ends in a draw.
        ---
        ### Steps
        1. Display Board.
        2. Ask the current player for a move.
        3. Validate and place the move.
        4. Check for a win or draw.
        5. If game not over, switch to the other player and repeat.
        
        """
        while True:
            # display
            self.board.display()
            print(f"{self.current_player.name}'s turn ({self.current_player.symbol})")
            
            # get move
            x, y = self.current_player.get_move(self.board)
            
            # validate move
            if not self.board.place_stone(x, y, self.current_player.symbol):
                print("Invalid move. Try again.")
                continue

            # check winner
            if self.board.check_winner(self.current_player.symbol):
                self.board.display()
                print(f"{self.current_player.name} wins!")
                break

            # check draw
            if self.board.check_draw():
                self.board.display()
                print("It's a draw!")
                break

            # Switch players
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1
