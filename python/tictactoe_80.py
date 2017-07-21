"""
Monte Carlo Tic-Tac-Toe Player
"""
 
import random
import poc_ttt_gui
import poc_ttt_provided as provided
 
# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player
     
def mc_trial(board, player):
    """
    play a game starting with the given player by making
    random moves, alternating between players.
    """
    while not board.check_win():
        open_squares = board.get_empty_squares()
        row, col = open_squares[random.randrange(len(open_squares))]
        board.move(row, col, player)
        if player==provided.PLAYERX:
            player = provided.PLAYERO
        elif player==provided.PLAYERO:
            player = provided.PLAYERX
 
 
def mc_update_scores(scores, board, player):
    """
    score the completed board and update the scores grid. 
    """
    winner = board.check_win()
    if winner==provided.DRAW:
        return
    nrow = ncol = board.get_dim()
    coef = 1
    if player!=winner:
        coef = -1
    for row in range(nrow):
        for col in range(ncol):
            if board.square(row, col)==player:
                scores[row][col] += coef*SCORE_CURRENT
            elif board.square(row, col)!=provided.EMPTY:
                scores[row][col] -= coef*SCORE_OTHER
 
def get_best_move(board, scores):
    """
    find all of the empty squares with the maximum score
    and randomly return the best position
    """
    best_square = board.get_empty_squares()[0]
    best_score = scores[best_square[0]][best_square[1]]
    for square in board.get_empty_squares():
        if scores[square[0]][square[1]]>best_score:
            best_square = square
            best_score = scores[square[0]][square[1]]
    out = []
    for square in board.get_empty_squares():
        if scores[square[0]][square[1]]==best_score:
            out.append(square)
    return out[random.randrange(len(out))]
     
def mc_move(board, player, trials):
    """
    use the Monte Carlo simulation to return a move 
    for the machine player
    """
    nrow = ncol = board.get_dim()
    # scores = [[0]*ncol for num in range(nrow)]
    scores = []
    while len(scores)<nrow:
        scores.append([0]*ncol)
    num = 0
    while num<trials:
        board_copy = board.clone()
        mc_trial(board_copy, player)
        mc_update_scores(scores, board_copy, player)
        num += 1
    return get_best_move(board, scores)
     
# board = provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.PLAYERX, provided.EMPTY]])
# print board
# mc_trial(board, provided.PLAYERX)
#mc_move(board,provided.PLAYERX, NTRIALS)
# print board
 
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
 
# provided.play_game(mc_move, NTRIALS, False)        