import random

NTRIALS = 300        # Number of trials to run
NUMBER_OF_GAMES = 10000
FIRST_TURN = 'player'

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
            moveList.append(advancedMove)
            moveList.append(advancedMove)
            moveList.append(advancedMove)
            moveList.append(advancedMove)
            moveList.append(advancedMove)
            # moveList.append(advancedMove)
            # moveList.append(advancedMove)
            # moveList.append(advancedMove)
        makeMove(board, playerLetter, random.choice(moveList))
        playerLetter = switchPlayer(playerLetter)
        # print
        # print
        # print
        # drawBoard(board)
    # drawBoard(board)
    pass



def updateScores(scores, move, board, playerLetter):
    if isBoardFull(board) and (not isWinner(board, 'X')) and (not isWinner(board, 'O')):
        scores[move] += 0.5
    elif isWinner(board, playerLetter): 
        scores[move] += 1

def decideMove(board, playerLetter, trials):
    scores = [0] * 10
    moveList = getMoveList(board)
    if len(moveList) == 0:
        return
    for move in moveList:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, playerLetter, move)

        for i in range(0, trials):
            dupeBoardAfterFirstMove = getBoardCopy(dupeBoard)
            trial(dupeBoardAfterFirstMove, switchPlayer(playerLetter))
            updateScores(scores, move, dupeBoardAfterFirstMove, playerLetter)
    # print(scores[1:])
    # print(scores.index(max(scores)))
    if scores.index(max(scores)) not in moveList:
        print('not in move list')
        print('this is move list', moveList)
        print('this is what you return', scores)
        print('this is board', drawBoard(board))
    return scores.index(max(scores))


print('Welcome to Tic Tac Toe!')

computer_win = 0
player_win = 0
drawn = 0
for i in xrange(0, NUMBER_OF_GAMES):
    #set up 
    theBoard = [' '] * 10
    scores = [0] * 10   
    playerLetter = 'X'
    computerLetter = 'O'
    turn = FIRST_TURN

    print(i)
    print('player win', player_win)
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
                    drawn += 1
                    # drawBoard(theBoard)
                    # print('The game is a tie!')
                    break
                else:
                    turn = 'computer'
        else:
            move = decideMove(theBoard, computerLetter, NTRIALS)
            makeMove(theBoard, computerLetter, move)
            if isWinner(theBoard, computerLetter):
                computer_win += 1
                # drawBoard(theBoard)
                # print('The computer has beaten you! You lose.')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawn += 1
                    # drawBoard(theBoard)
                    # print('The game is a tie!')
                    break
                else:
                    turn = 'player'
    pass

print('computer win: ', computer_win)
print('player win: ', player_win)
print('drawn: ', drawn)

