import random
from algorithms.common import *


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
