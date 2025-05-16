class Board:
    
    def __init__(self, size: int = 15):
        """ Initialize a board for Five in a row game

        Args:
            size (int, optional): Board size defaults to 15.
        """
        self.size = size
        self.board = [['.'] * size for _ in range(size)]

    def __is_valid_move(self, x: int, y: int) -> bool:
        """Validates a move is withing boundary & cell is empty

        Args:
            x (int): X position
            y (int): Y position

        Returns:
            bool: Move is within boundary or not
        """
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == '.'

    def place_stone(self, x: int, y: int, player_symbol: str) -> bool:
        """Place a stone on board

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            player_symbol (str): Player

        Returns:
            bool: True if move is made, False otherwise
        """
        if self.__is_valid_move(x, y):
            self.board[x][y] = player_symbol
            return True
        return False

    def remove_stone(self, x: int, y: int) -> bool:
        """Remove a stone from the board

        Args:
            x (int): x coordinate
            y (int): y coordinate
        """
        self.board[x][y] = '.'

    def display(self):
        """Displays board
        """
        print('__' * (self.size + 1))
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print('__' * (self.size + 1))

    def check_winner(self, player: str) -> bool:
        """Checks a winner

        Args:
            player (str): Player to check if he win

        Returns:
            bool: True if player wins
        """
        for x in range(self.size):
            for y in range(self.size):
                if self.__check_line(x, y, player, 5):
                    return True
        return False

    def check_draw(self) -> bool:
        """Check draw state in board

        Returns:
            bool: True if draw, False otherwise
        """
        for row in self.board:
            if '.' in row:
                return False
        return True

    def __check_line(self, x: int, y: int, player: str, length: int) -> bool:
        """**Checks from (x, y) whether the player has a continuous line of length stones.**
        \nChecks in 4 directions:
        1. Horizontal
        2. Vertical
        3. Diagonal (top-left to bottom-right)
        4. Diagonal (bottom-left to top-right)
        ---
        ## Args:
            x (int): x start position
            y (int): y start position
            player (str): player to check for
            length (int): length of checks

        ## Returns:
            bool: True if player has continuous stones of size length in a certain direction, False otherwise
        """
        # Check horizontal
        if y + length - 1 < self.size and all(self.board[x][y + i] == player for i in range(length)):
            return True

        # Check vertical
        if x + length - 1 < self.size and all(self.board[x + i][y] == player for i in range(length)):
            return True

        # Check diagonal (top-left to bottom-right)
        if x + length - 1 < self.size and y + length - 1 < self.size and all(
                self.board[x + i][y + i] == player for i in range(length)):
            return True

        # Check diagonal (bottom-left to top-right)
        if x - (length - 1) >= 0 and y + length - 1 < self.size and all(
                self.board[x - i][y + i] == player for i in range(length)):
            return True

        return False
