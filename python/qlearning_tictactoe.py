import random

NTRIALS = 500        # Number of trials to run
NUMBER_OF_GAMES = 200000
FIRST_TURN = 'player'
# ALPHA = 0.3
# GAMMA = 0.9
# EPSILON = 0.3

ALPHA = 0.01
GAMMA = 0.9
EPSILON = 0.5

def drawBoard(board):
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')

def inputPlayerLetter():
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        letter = raw_input('Do you want to be X or O?').upper()
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def playAgain():
    print('Do you want to play again? (yes or no)')
    return raw_input().lower().startswith('y')

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(board, letter):
    return ((board[7] == letter and board[8] == letter and board[9] == letter) or 
    (board[4] == letter and board[5] == letter and board[6] == letter) or 
    (board[1] == letter and board[2] == letter and board[3] == letter) or 
    (board[7] == letter and board[4] == letter and board[1] == letter) or 
    (board[8] == letter and board[5] == letter and board[2] == letter) or 
    (board[9] == letter and board[6] == letter and board[3] == letter) or 
    (board[7] == letter and board[5] == letter and board[3] == letter) or 
    (board[9] == letter and board[5] == letter and board[1] == letter)) 

def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

def getBoardCopy(board):
    dupeBoard = []
    for i in board:
        dupeBoard.append(i)
    return dupeBoard

def isSpaceFree(board, move):
    return board[move] == ' '

def getPlayerMove(board):
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = raw_input()
    return int(move)

def getMoveList(board):
    possibleMoves = []
    for i in range(1, len(board)):
        if isSpaceFree(board, i):
            possibleMoves.append(i) 
    return possibleMoves

def chooseRandomMoveFromBoard(board):
    possibleMoves = getMoveList(board)
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def isFinish(board):
    return isBoardFull(board) or isWinner(board, 'X') or isWinner(board, 'O')

def switchPlayer(playerLetter):
    if playerLetter == 'X':
        return 'O'
    else:
        return 'X'

def getAdvancedMove(board, moveList, playerLetter):
    for i in moveList:
        checkWinMoveBoard = getBoardCopy(board)
        if isSpaceFree(checkWinMoveBoard, i):
            makeMove(checkWinMoveBoard, playerLetter, i)
            if isWinner(checkWinMoveBoard, playerLetter):
                return i

    for i in moveList:
        checkWinMoveBoardOpponent = getBoardCopy(board)
        if isSpaceFree(checkWinMoveBoardOpponent, i):
            makeMove(checkWinMoveBoardOpponent, switchPlayer(playerLetter), i)
            if isWinner(checkWinMoveBoardOpponent, switchPlayer(playerLetter)):
                return i
    return -1

def trial(board, playerLetter):
    while not isFinish(board):
        moveList = getMoveList(board)
        advancedMove = getAdvancedMove(board, moveList, playerLetter)
        # if advancedMove == -1:
        #     makeMove(board, playerLetter, random.choice(moveList))
        # else:
        #     makeMove(board, playerLetter, advancedMove)
        if advancedMove != -1:
            moveList.extend([advancedMove] * 5)
        if 5 in moveList:
            moveList.extend([5] * 3)
        makeMove(board, playerLetter, random.choice(moveList))
        playerLetter = switchPlayer(playerLetter)
        # print
        # print
        # print
        # drawBoard(board)
    # drawBoard(board)
    pass

q_X = {}
q_O = {}

def getQ(state, action, playerLetter):
    if playerLetter == 'O':
        if q_O.get((state, action)) == None:
            q_O[(state, action)] = 1.0
        else:
            return q_O.get((state, action))
    pass

def updateScores(scores, move, board, playerLetter):
    if isBoardFull(board) and (not isWinner(board, 'X')) and (not isWinner(board, 'O')):
        scores[move] += 0.5
    elif isWinner(board, playerLetter): 
        scores[move] += 1

def reward(lastBoard, lastMove, r, resultBoard, playerLetter):
    # print('q_o_1', q_O)
    getQ(tuple(lastBoard), lastMove, playerLetter)
    prev =  getQ(tuple(lastBoard), lastMove, playerLetter)
    # prev = 

    for action in getMoveList(resultBoard):
        getQ(tuple(resultBoard),action,playerLetter)

    if isBoardFull(resultBoard):
        expect = 0
    else:
        expect_list = [getQ(tuple(resultBoard), action, playerLetter) for action in getMoveList(resultBoard)]
        expect = max(expect_list)
    
    # print('score before update')
    # print(q_O.get((tuple(lastBoard),lastMove)))

    # print('score of arg max')
    # print([q_O.get(tuple(resultBoard),action) for action in expect_list])

    # print('r', r)
    # print('q_O[(tuple(lastBoard), lastMove)]', q_O[(tuple(lastBoard), lastMove)])
    # print('expect_list', expect_list)
    # print('prev', prev)
    # print('prev + ALPHA*(r + GAMMA*expect - prev)', prev + ALPHA*(r + GAMMA*expect - prev))

    q_O[(tuple(lastBoard), lastMove)] = prev + ALPHA*(r + GAMMA*expect - prev)

    # print('score after update')
    # print(q_O.get((tuple(lastBoard),lastMove)))

    pass

def decideMove(board, playerLetter, trials):
    # last_board = getBoardCopy(board)


    moveList = getMoveList(board)
    # print(moveList)
    if len(moveList) == 0:
        return
    if random.random() < EPSILON:
        print('exploration move')
        return random.choice(moveList)
    scores_array = [getQ(tuple(board), action, playerLetter) for action in moveList]
    # print('q_O')
    # print(q_O)
    max_score = max(scores_array)
    # print('scores ',scores_array)
    # print('decided move', scores_array.index(max_score))
    if scores_array.count(max_score) > 1:
        list_index = [i for i in range(len(scores_array)) if scores_array[i] == max_score]
        index = random.choice(list_index)
        # print('score array', scores_array)
        # print('move list', moveList)
        # print('list index', list_index)
        # print('index random', index)
        # print('decided move', moveList[index])
    else:
        index = scores_array.index(max_score)

    return moveList[index]


print('Welcome to Tic Tac Toe!')

computer_win = 0
player_win = 0
draw = 0
for i in xrange(0, NUMBER_OF_GAMES):
    #set up 
    theBoard = [' '] * 10
    scores = [0] * 10   
    playerLetter = 'X'
    computerLetter = 'O'
    turn = FIRST_TURN

    print(i)
    print('computer_win', computer_win)
    print('player win', player_win)
    print('draw', draw)
    gameIsPlaying = True
    while gameIsPlaying:
        if turn == 'player':
            # drawBoard(theBoard)
            # move = getPlayerMove(theBoard)

            move = chooseRandomMoveFromBoard(theBoard)

            # move = decideMove(theBoard, playerLetter, NTRIALS)
            makeMove(theBoard, playerLetter, move)
            if isWinner(theBoard, playerLetter):
                player_win += 1
                reward(lastBoard, move, -1, theBoard, computerLetter)

                drawBoard(theBoard)
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    draw += 1
                    reward(lastBoard, move, 0.5, theBoard, computerLetter)

                    # drawBoard(theBoard)
                    # print('The game is a tie!')
                    break
                else:
                    turn = 'computer'
        else:
            lastBoard = getBoardCopy(theBoard)
            move = decideMove(theBoard, computerLetter, NTRIALS)
            # print('decided move', move)
            makeMove(theBoard, computerLetter, move)
            if isWinner(theBoard, computerLetter):
                computer_win += 1
                reward(lastBoard, move, 1, theBoard, computerLetter)

                # drawBoard(theBoard)
                # print('The computer has beaten you! You lose.')
                # gameIsPlaying = False

                break
            else:
                if isBoardFull(theBoard):
                    draw += 1
                    reward(lastBoard, move, 0.5, theBoard, computerLetter)

                    # drawBoard(theBoard)
                    # print('The game is a tie!')
                    break
                else:
                    turn = 'player'
            reward(lastBoard, move, 0, theBoard, computerLetter)
    pass


for i in xrange(0, 2):
    #set up 
    theBoard = [' '] * 10
    scores = [0] * 10   
    playerLetter = 'X'
    computerLetter = 'O'
    turn = FIRST_TURN

    print(i)
    print('computer_win', computer_win)
    print('player win', player_win)
    print('draw', draw)
    gameIsPlaying = True
    while gameIsPlaying:
        if turn == 'player':
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)

            # move = chooseRandomMoveFromBoard(theBoard)

            # move = decideMove(theBoard, playerLetter, NTRIALS)
            makeMove(theBoard, playerLetter, move)
            if isWinner(theBoard, playerLetter):
                player_win += 1
                drawBoard(theBoard)
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    draw += 1
                    # drawBoard(theBoard)
                    # print('The game is a tie!')
                    break
                else:
                    turn = 'computer'
        else:
            lastBoard = getBoardCopy(theBoard)
            move = decideMove(theBoard, computerLetter, NTRIALS)
            makeMove(theBoard, computerLetter, move)
            if isWinner(theBoard, computerLetter):
                computer_win += 1
                reward(lastBoard, move, 1, theBoard, computerLetter)

                # drawBoard(theBoard)
                # print('The computer has beaten you! You lose.')
                # gameIsPlaying = False

                break
            else:
                if isBoardFull(theBoard):
                    draw += 1
                    reward(lastBoard, move, 0.5, theBoard, computerLetter)

                    # drawBoard(theBoard)
                    # print('The game is a tie!')
                    break
                else:
                    turn = 'player'
            reward(lastBoard, move, 5, theBoard, computerLetter)
    pass

print('computer win: ', computer_win)
print('player win: ', player_win)
print('draw: ', draw)

