import tkinter as tk
from Board import Board
from Players import HumanPlayer, AIPlayer
from algorithms.alphaBetaPruning import alpha_beta_pruning
from algorithms.minimax import minimax

CELL_SIZE = 40
GRID_COLOR = "black"
GRID_WIDTH = 2
PLAYER_COLORS = {'B': 'black', 'W': 'white'}


class GomokuGUI:
    def __init__(self, root, board_size=15):
        self.root = root
        self.root.title("Gomoku")
        self.root.geometry("600x700")
        self.board_size = board_size
        self.board = Board(board_size)
        self.players = []
        self.frame_start = tk.Frame(self.root)
        self.frame_game = tk.Frame(self.root)
        self.canvas = None
        self.reset_button = None
        self.current_player_index = 0

        self.setup_start_page()

    def setup_start_page(self):
        self.frame_start.configure(bg="#F0F0F0")
        self.frame_start.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title = tk.Label(self.frame_start, text="Welcome to Gomoku!", font=("Helvetica", 20, "bold"), bg="#F0F0F0")
        title.pack(pady=10)

        # Player 1
        p1_frame = tk.LabelFrame(self.frame_start, text="Player 1 (Black)", font=("Helvetica", 12, "bold"),
                                 bg="#DDEEFF", padx=10, pady=10)
        p1_frame.pack(fill=tk.X, pady=10)

        self.p1_type = tk.StringVar(value="Human")
        tk.Radiobutton(p1_frame, text="Human", variable=self.p1_type, value="Human", bg="#DDEEFF").grid(row=0, column=0,
                                                                                                        sticky="w")
        tk.Radiobutton(p1_frame, text="AI (Alpha-Beta)", variable=self.p1_type, value="AI", bg="#DDEEFF").grid(row=0,
                                                                                                               column=1,
                                                                                                               sticky="w")

        self.p1_name_entry = tk.Entry(p1_frame)
        self.p1_name_entry.insert(0, "Player 1")
        self.p1_name_entry.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        # Player 2
        p2_frame = tk.LabelFrame(self.frame_start, text="Player 2 (White)", font=("Helvetica", 12, "bold"),
                                 bg="lightpink", padx=10, pady=10)
        p2_frame.pack(fill=tk.X, pady=10)

        self.p2_type = tk.StringVar(value="AI")
        tk.Radiobutton(p2_frame, text="Human", variable=self.p2_type, value="Human", bg="lightpink").grid(row=0,
                                                                                                          column=0,
                                                                                                          sticky="w")
        tk.Radiobutton(p2_frame, text="AI (Minimax)", variable=self.p2_type, value="AI", bg="lightpink").grid(row=0,
                                                                                                              column=1,
                                                                                                              sticky="w")

        self.p2_name_entry = tk.Entry(p2_frame)
        self.p2_name_entry.insert(0, "Player 2")
        self.p2_name_entry.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        starter_frame = tk.Frame(self.frame_start, bg="#F0F0F0")
        starter_frame.pack(pady=10)

        tk.Label(starter_frame, text="Who starts?", bg="#F0F0F0").pack(side=tk.LEFT, padx=(0, 10))
        self.starting_player = tk.StringVar(value="Player 1")
        starter_dropdown = tk.OptionMenu(starter_frame, self.starting_player, "Player 1", "Player 2")
        starter_dropdown.pack(side=tk.LEFT)

        start_button = tk.Button(self.frame_start, text="Start Game", font=("Helvetica", 12, "bold"),
                                 bg="#107A99", fg="white", command=self.start_game)
        start_button.pack(pady=20)

    def start_game(self):
        p1_name = self.p1_name_entry.get()
        p2_name = self.p2_name_entry.get()
        self.current_player_index = 0 if self.starting_player.get() == "Player 1" else 1
        self.board = Board(self.board_size)

        if self.p1_type.get() == "Human":
            player1 = HumanPlayer(p1_name, 'B')
        else:
            player1 = AIPlayer(p1_name, 'B', alpha_beta_pruning, depth=2)

        if self.p2_type.get() == "Human":
            player2 = HumanPlayer(p2_name, 'W')
        else:
            player2 = AIPlayer(p2_name, 'W', minimax, depth=2)

        self.players = [player1, player2]
        self.frame_start.pack_forget()
        self.setup_game_page()

    def setup_game_page(self):
        if self.frame_start.winfo_ismapped():
            self.frame_start.pack_forget()

        for widget in self.frame_game.winfo_children():
            widget.destroy()

        self.frame_game.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas_frame = tk.Frame(self.frame_game)
        canvas_frame.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(canvas_frame, width=self.board_size * CELL_SIZE,
                                height=self.board_size * CELL_SIZE, bg='#107A99')
        self.canvas.pack(pady=(10, 10))

        button_frame = tk.Frame(self.frame_game)
        button_frame.pack(fill=tk.X, pady=10)

        self.reset_button = tk.Button(
            button_frame, text="Reset", font=("Helvetica", 12, "bold"),
            bg="#107A99", fg="white", command=self.reset_game,
            width=10, height=1
        )
        self.reset_button.pack(pady=5)

        self.canvas.bind("<Button-1>", self.human_move)
        self.draw_board()

        print("Reset button created")

        if isinstance(self.players[self.current_player_index], AIPlayer):
            self.root.after(500, self.ai_move)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.board_size + 1):
            self.canvas.create_line(i * CELL_SIZE, 0,
                                    i * CELL_SIZE, self.board_size * CELL_SIZE,
                                    fill=GRID_COLOR, width=GRID_WIDTH, tags="grid")
            self.canvas.create_line(0, i * CELL_SIZE,
                                    self.board_size * CELL_SIZE, i * CELL_SIZE,
                                    fill=GRID_COLOR, width=GRID_WIDTH, tags="grid")

        for x in range(self.board_size):
            for y in range(self.board_size):
                symbol = self.board.board[x][y]
                if symbol != '.':
                    self.draw_piece(x, y, symbol)

    def draw_piece(self, x, y, symbol):
        padding = 5
        x1 = y * CELL_SIZE + padding
        y1 = x * CELL_SIZE + padding
        x2 = (y + 1) * CELL_SIZE - padding
        y2 = (x + 1) * CELL_SIZE - padding
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=PLAYER_COLORS[symbol], tags="piece")

    def human_move(self, event):
        player = self.players[self.current_player_index]
        if not isinstance(player, HumanPlayer):
            return

        x = event.y // CELL_SIZE
        y = event.x // CELL_SIZE

        if x >= self.board_size or y >= self.board_size or self.board.board[x][y] != '.':
            return

        self.board.place_stone(x, y, player.symbol)
        self.draw_board()
        if self.check_game_end():
            return
        self.current_player_index = 1 - self.current_player_index
        self.root.after(100, self.ai_move)

    def ai_move(self):
        player = self.players[self.current_player_index]
        if not isinstance(player, AIPlayer):
            return
        x, y = player.get_move(self.board)
        if x is not None and y is not None:
            self.board.place_stone(x, y, player.symbol)
            self.draw_board()
            if self.check_game_end():
                return
            self.current_player_index = 1 - self.current_player_index

            next_player = self.players[self.current_player_index]
            if isinstance(next_player, AIPlayer):
                self.root.after(1000, self.ai_move)

    def check_game_end(self):
        player = self.players[self.current_player_index]
        if self.board.check_winner(player.symbol):
            self.show_game_over_popup(f"{player.name} wins!")
            return True
        elif self.board.check_draw():
            self.show_game_over_popup("It's a draw!")
            return True
        return False

    def show_game_over_popup(self, message):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.geometry("300x150")
        popup.transient(self.root)
        popup.grab_set()

        label = tk.Label(popup, text=message, font=("Helvetica", 14))
        label.pack(pady=20)

        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Replay", command=lambda: [popup.destroy(), self.reset_game()],
                  bg="#4CAF50", fg="white", width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Quit", command=self.root.quit,
                  bg="#F44336", fg="white", width=10).pack(side=tk.LEFT, padx=10)

    def reset_game(self):
        if self.frame_game.winfo_ismapped():
            self.frame_game.pack_forget()
        self.board = Board(self.board_size)
        self.players = []
        self.current_player_index = 0
        self.frame_start.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        print("Game reset - returning to start screen")


if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGUI(root)
    root.mainloop()
