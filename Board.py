class Board:
    def __init__(self, size: int = 15):
        self.size = size
        self.board = [['.'] * size for _ in range(size)]

    def __is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == '.'

    def place_stone(self, x: int, y: int, player_symbol: str) -> bool:
        if self.__is_valid_move(x, y):
            self.board[x][y] = player_symbol
            return True
        return False

    def remove_stone(self, x: int, y: int) -> bool:
        self.board[x][y] = '.'

    def display(self):
        print('__' * (self.size + 1))
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print('__' * (self.size + 1))

    def check_winner(self, player: str) -> bool:
        for x in range(self.size):
            for y in range(self.size):
                if self.__check_line(x, y, player, 5):
                    return True
        return False

    def check_draw(self) -> bool:
        for row in self.board:
            if '.' in row:
                return False
        return True

    def __check_line(self, x: int, y: int, player: str, length: int) -> bool:
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

    # for heuristic evaluation
    # def count_four_in_a_row(self, player: str) -> int:
    #     count = 0
    #     for x in range(self.size):
    #         for y in range(self.size):
    #             if self.__check_line(x, y, player):
    #                 count += 1
    #     return count
