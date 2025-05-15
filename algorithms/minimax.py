import random
def minimax(board, depth, is_maximizing, max_player, min_player):
    current_player = max_player if is_maximizing else min_player
    opponent = min_player if is_maximizing else max_player

    if depth <= 0:
        return evaluate_board(board, max_player, min_player), None, None

    winning_move = find_winning_move(board, current_player)
    if winning_move:
        return 100000, winning_move[0], winning_move[1]

    blocking_move = find_winning_move(board, opponent)
    if blocking_move:
        return 10000, blocking_move[0], blocking_move[1]

    if board.check_winner(max_player):
        return 100000, None, None

    if board.check_winner(min_player):
        return -100000, None, None

    if board.check_draw():
        return 0, None, None

    best_score = float('-inf') if is_maximizing else float('inf')
    best_move = None, None

    valid_moves = get_most_promising_moves(board, current_player, opponent, max_moves=7)

    if not valid_moves:
        center = board.size // 2
        return 0, center, center

    dict_moves = {}
    for x, y in valid_moves:
        board.place_stone(x, y, current_player)
        next_depth = depth - 1
        score, _, _ = minimax(board, next_depth, not is_maximizing, max_player, min_player)
        board.remove_stone(x, y)
        if is_maximizing and score > best_score:
            best_score = score
            # best_move = x, y
        elif not is_maximizing and score < best_score:
            best_score = score
            # best_move = x, y
        if score not in dict_moves:
            dict_moves[score] = [(x, y)]
        else:
            dict_moves[score].append((x, y))
    best_move = random.choice(dict_moves[best_score])
    return best_score, best_move[0], best_move[1]


def find_winning_move(board, player):
    moves = get_valid_moves(board)
    for x, y in moves:
        board.place_stone(x, y, player)
        is_win = board.check_winner(player)
        board.remove_stone(x, y)
        if is_win:
            return x, y
    return None


def get_most_promising_moves(board, player, opponent, max_moves=7):
    all_moves = get_valid_moves(board)
    if not all_moves:
        center = board.size // 2
        return [(center, center)]

    move_scores = []
    for x, y in all_moves:
        board.place_stone(x, y, player)
        player_score = quick_evaluation(board, x, y, player)
        board.remove_stone(x, y)

        board.place_stone(x, y, opponent)
        opponent_score = quick_evaluation(board, x, y, opponent)
        board.remove_stone(x, y)

        total_score = player_score + opponent_score * 0.8
        move_scores.append((total_score, x, y))

    move_scores.sort(reverse=True)
    return [(x, y) for _, x, y in move_scores[:max_moves]]


def quick_evaluation(board, x, y, player):
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dx, dy in directions:
        count, open_ends = count_in_line(board, x, y, dx, dy, player)
        if count >= 5:  # Win
            score += 10000
        elif count == 4:
            if open_ends == 2:  # Open four (very strong)
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

    center = board.size // 2
    center_distance = abs(x - center) + abs(y - center)
    score += max(0, 5 - center_distance) * 2

    return score


# counts how many similar marks are in a line (consecutive) AND how many open ends they have
def count_in_line(board, x, y, dx, dy, player):
    count = 1  # the stone at (x,y)
    open_ends = 0

    # Check in the positive direction
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

    # Check in the negative direction
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
    max_patterns = get_board_patterns(board, max_player)
    min_patterns = get_board_patterns(board, min_player)

    max_score = patterns_to_scores(max_patterns)
    min_score = patterns_to_scores(min_patterns)

    return max_score - min_score


def get_board_patterns(board, player):
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
    score = 0
    score += patterns['five'] * 100000
    score += patterns['open_four'] * 10000
    score += patterns['half_open_four'] * 1000
    score += patterns['open_three'] * 500
    score += patterns['open_two'] * 50
    return score
