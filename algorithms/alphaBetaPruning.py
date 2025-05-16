import random
from algorithms.common import *


def alpha_beta_pruning(board, depth, alpha, beta, is_maximizing, max_player, min_player):
    """_summary_

    Args:
        board: 
        depth: 
        alpha: 
        beta:
        is_maximizing:
        max_player:
        min_player:

    Returns:
        score, x, y: Best score, & move with X & Y coordinates
    """
    current_player = max_player if is_maximizing else min_player
    opponent = min_player if is_maximizing else max_player

    # When the max depth is reached, the board is evaluated using a static heuristic score.
    if depth <= 0:
        return evaluate_board(board, max_player, min_player), None, None

    # If the current player can win immediately → return that move.
    winning_move = find_winning_move(board, current_player)
    if winning_move:
        return 100000, winning_move[0], winning_move[1]
    # If the opponent can win next turn → block it.
    blocking_move = find_winning_move(board, opponent)
    if blocking_move:
        return 10000, blocking_move[0], blocking_move[1]
    
    # Check for existing win/loss/draw conditions.
    if board.check_winner(max_player):
        return 100000, None, None
    if board.check_winner(min_player):
        return -100000, None, None
    if board.check_draw():
        return 0, None, None

    best_move = None, None

    # Get valid moves
    valid_moves = get_most_promising_moves(board, current_player, opponent, max_moves=7)
    # Defaults to center if no valid moves
    if not valid_moves:
        center = board.size // 2
        return 0, center, center

    dict_moves = {}
    if is_maximizing:
        best_score = float('-inf')
        for x, y in valid_moves:
            board.place_stone(x, y, current_player)
            score, _, _ = alpha_beta_pruning(board, depth - 1, alpha, beta, False, max_player, min_player)
            board.remove_stone(x, y)

            if score > best_score:
                best_score = score
                # best_move = x, y

            if score not in dict_moves:
                dict_moves[score] = [(x, y)]
            else:
                dict_moves[score].append((x, y))

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        best_move = random.choice(dict_moves[best_score])
        return best_score, best_move[0], best_move[1]

    else:
        best_score = float('inf')
        for x, y in valid_moves:
            board.place_stone(x, y, current_player)
            score, _, _ = alpha_beta_pruning(board, depth - 1, alpha, beta, True, max_player, min_player)
            board.remove_stone(x, y)

            if score < best_score:
                best_score = score
                # best_move = x, y

            if score not in dict_moves:
                dict_moves[score] = [(x, y)]
            else:
                dict_moves[score].append((x, y))

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        best_move = random.choice(dict_moves[best_score])
        return best_score, best_move[0], best_move[1]
