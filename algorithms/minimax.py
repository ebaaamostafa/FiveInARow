import random
from algorithms.common import *


def minimax(board, depth, is_maximizing, max_player, min_player):
    """
    Minimax algorithm for an AI player. Uses recursive game tree evaluation to decide its best move, up to a specified depth.
    ---
    #### Steps:
    1. Determine Whose Turn It Is
    2. Check Depth Limit
    3. Check for Immediate Wins or Blocks
    4. Check for Game Over
    5. Get Best Move Among Promising Moves
    6. Explore Moves Recursively
    7. Choose Best Move Based on Score 
    8. Pick Random Move Among Best Scored Ones
    
    Args:
        board:
        depth:
        is_maximizing:
        max_player:
        min_player:

    Returns:
        _type_: _description_
    """
    
    # Determine whose turn it is
    current_player = max_player if is_maximizing else min_player
    opponent = min_player if is_maximizing else max_player

    # Check depth limit
    if depth <= 0:
        return evaluate_board(board, max_player, min_player), None, None

    #If current player can win immediately, do it.
    winning_move = find_winning_move(board, current_player)
    if winning_move:
        return 100000, winning_move[0], winning_move[1]

    #If opponent can win in the next move, block it.
    blocking_move = find_winning_move(board, opponent)
    if blocking_move:
        return 10000, blocking_move[0], blocking_move[1]

    # If either player has already won, return a very high or low score.
    if board.check_winner(max_player):
        return 100000, None, None
    if board.check_winner(min_player):
        return -100000, None, None
    # If the game is a draw, return 0.
    if board.check_draw():
        return 0, None, None

    best_score = float('-inf') if is_maximizing else float('inf')
    best_move = None, None

    valid_moves = get_most_promising_moves(board, current_player, opponent, max_moves=7)

    # If no good moves, place in the center as a fallback.
    if not valid_moves:
        center = board.size // 2
        return 0, center, center

    dict_moves = {}
    for x, y in valid_moves:
        # Place the stone.
        board.place_stone(x, y, current_player)
        next_depth = depth - 1
        # Call minimax recursively to evaluate that move
        score, _, _ = minimax(board, next_depth, not is_maximizing, max_player, min_player)
        # remove stone (backtracking)
        board.remove_stone(x, y)
        
        # Keep track of the best score and the moves that resulted in it.
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
    
    # If multiple moves result in the same best score, randomly choose one to introduce variety.
    best_move = random.choice(dict_moves[best_score])
    return best_score, best_move[0], best_move[1]
