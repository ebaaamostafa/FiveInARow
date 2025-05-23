def find_winning_move(board, player):
    """Look for a move that would let the player win immediately.

    Args:
        board:
        player:

    Returns:
        x, y: Position of win move, or None if no immediate win is possible
    """
    moves = get_valid_moves(board)
    for x, y in moves:
        board.place_stone(x, y, player)
        is_win = board.check_winner(player)
        board.remove_stone(x, y)
        if is_win:
            return x, y
    return None


def get_most_promising_moves(board, player, opponent, max_moves=7):
    """Returns up to max_moves of the most promising moves using a heuristic.

    Args:
        board:
        player:
        opponent:
        max_moves (int, optional): Defaults to 7.

    Returns:
        Array: List of top N moves
    """
    
    # Get all valid moves
    all_moves = get_valid_moves(board)
    if not all_moves:
        center = board.size // 2
        return [(center, center)]

    move_scores = []
    # For each move
    # 1. Place it as a player, then evaluate
    # 2. Place it as the opponent, then evaluate
    # 3. Adds weighted scores for both
    for x, y in all_moves:
        board.place_stone(x, y, player)
        player_score = quick_evaluation(board, x, y, player)
        board.remove_stone(x, y)

        board.place_stone(x, y, opponent)
        opponent_score = quick_evaluation(board, x, y, opponent)
        board.remove_stone(x, y)

        total_score = player_score + opponent_score * 0.8
        move_scores.append((total_score, x, y))

    # Sort moves by total score
    move_scores.sort(reverse=True)
    # return top N moves
    return [(x, y) for _, x, y in move_scores[:max_moves]]


def quick_evaluation(board, x, y, player):
    """Evaluates how strong a move is by analyzing the pattern it creates at (x, y).

    Args:
        board:
        x:
        y:
        player:

    Returns:
        score: how strong a move is
    """
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dx, dy in directions:
        count, open_ends = count_in_line(board, x, y, dx, dy, player)
        if count >= 5:  # Win
            score += 10000
        elif count == 4:
            if open_ends == 2:  # Open four, both ends
                score += 2000
            elif open_ends == 1:  # Half-open four
                score += 500
        elif count == 3:
            if open_ends == 2:  # Open three
                score += 200
            elif open_ends == 1:  # Half-open three
                score += 50
        elif count == 2:
            if open_ends == 2:  # Open two
                score += 10
            elif open_ends == 1:  # Half-open two
                score += 3
        elif count == 1 and open_ends > 0:
            score += 1

    # add bonus points for being closer to the center
    center = board.size // 2
    center_distance = abs(x - center) + abs(y - center)
    score += max(0, 5 - center_distance) * 2

    return score


def count_in_line(board, x, y, dx, dy, player):
    """Counts how many similar cells are in a line (consecutive) AND how many open ends they have
    Args:
        board:
        x:
        y :        
        dx:
        dy:
        player:

    Returns:
        count, open_ends: count of similar cells in a line & open_ends
    """
    count = 1  # stone at (x,y)
    open_ends = 0

    # Positive direction
    for i in range(1, 5):
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < board.size and 0 <= ny < board.size:
            if board.board[nx][ny] == player:
                count += 1
            elif board.board[nx][ny] == '.':
                open_ends += 1
                break
            else:  # Opponent's
                break
        else:  # Out of bounds
            break

    # Negative direction
    for i in range(1, 5):
        nx, ny = x - i * dx, y - i * dy
        if 0 <= nx < board.size and 0 <= ny < board.size:
            if board.board[nx][ny] == player:
                count += 1
            elif board.board[nx][ny] == '.':
                open_ends += 1
                break
            else:  # Opponent's
                break
        else:  # Out of bounds
            break

    return count, open_ends


def get_valid_moves(board):
    """Generates a list of all valid positions where a player might want to move.

    Args:
        board:

    Returns:
        moves (list): List of valid moves
    """
    moves = []
    checked = set()

    for x in range(board.size):
        for y in range(board.size):
            if board.board[x][y] != '.':
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if (nx, ny) in checked:
                            continue
                        if 0 <= nx < board.size and 0 <= ny < board.size and board.board[nx][ny] == '.':
                            moves.append((nx, ny))
                            checked.add((nx, ny))

    if not moves:
        if all(cell == '.' for row in board.board for cell in row):
            center = board.size // 2
            moves.append((center, center))
        else:
            for x in range(board.size):
                for y in range(board.size):
                    if board.board[x][y] == '.':
                        moves.append((x, y))
                        if len(moves) > 0:
                            break
                if len(moves) > 0:
                    break

    return moves


def evaluate_board(board, max_player, min_player):
    """Perform static evaluation of a board state.

    Args:
        board:
        max_player: 
        min_player:

    Returns:
        score: difference between max_score and min_score
    """
    max_patterns = get_board_patterns(board, max_player)
    min_patterns = get_board_patterns(board, min_player)

    max_score = patterns_to_scores(max_patterns)
    min_score = patterns_to_scores(min_patterns)

    return max_score - min_score


def get_board_patterns(board, player):
    """Scans the board and counts important patterns for a given player:

    Args:
        board:
        player:

    Returns:
        patterns (dict): counts of patterns
    """
    patterns = {
        'open_two': 0,
        'open_three': 0,
        'open_four': 0,
        'half_open_four': 0,
        'five': 0
    }

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for x in range(board.size):
        for y in range(board.size):
            if board.board[x][y] != player:
                continue

            for dx, dy in directions:
                count, open_ends = count_in_line(board, x, y, dx, dy, player)

                if count >= 5:
                    patterns['five'] += 1
                elif count == 4:
                    if open_ends == 2:
                        patterns['open_four'] += 1
                    elif open_ends == 1:
                        patterns['half_open_four'] += 1
                elif count == 3 and open_ends == 2:
                    patterns['open_three'] += 1
                elif count == 2 and open_ends == 2:
                    patterns['open_two'] += 1

    return patterns


def patterns_to_scores(patterns):
    """Sssign numerical values to each pattern:

    Args:
        patterns (dict): Patterns count

    Returns:
        score: score based on patterns 
    """
    score = 0
    score += patterns['five'] * 100000
    score += patterns['open_four'] * 10000
    score += patterns['half_open_four'] * 1000
    score += patterns['open_three'] * 500
    score += patterns['open_two'] * 50
    return score
