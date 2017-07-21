import random

NTRIALS = 1000         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

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


def isFinish(board):
    return isBoardFull(board) or isWinner(board, 'X') or isWinner(board, 'O')

def trial(board, playerLetter):
    while not isFinish(board):
        moveList = getMoveList(board)
        makeMove(board, playerLetter, random.choice(moveList))
        if playerLetter == 'X':
            playerLetter = 'O'
        else:
            playerLetter = 'X'
    drawBoard(board)
    pass

def updateScores(scores, board, playerLetter):
    if isBoardFull(board):
        return
    lengthBoard = len(board) - 1 #drop position 0 of board
    coef = 1
    if not isWinner(board, playerLetter):
        coef = -1
    for i in range(1, lengthBoard+1):
        if board[i] == playerLetter:
            scores[i] += coef*SCORE_CURRENT
        elif board[i] != ' ':
            scores[i] -= coef*SCORE_OTHER
    pass

def findBestMove(board, scores):
    moveList = getMoveList(board)
    if len(moveList) == 0:
        return
    best_move = moveList[0]
    best_score = scores[best_move]
    for i in moveList[1:]:
        if scores[i] > best_score:
            best_move = i
            best_score = scores[i]
    return best_move

def decideMove(board, playerLetter, trials):
    scores = [0] * 10
    for i in range(0, trials):
        dupeBoard = getBoardCopy(board)
        trial(dupeBoard, playerLetter)
        updateScores(scores, dupeBoard, playerLetter)

        print(scores[1:])
    return findBestMove(board, scores)

# scores = [0] * 10
# board = [' '] * 10

print('Welcome to Tic Tac Toe!')
while True:
    theBoard = [' '] * 10
    scores = [0] * 10   
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True
    while gameIsPlaying:
        if turn == 'player':
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'
        else:
            move = decideMove(theBoard, computerLetter, NTRIALS)
            makeMove(theBoard, computerLetter, move)
            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you! You lose.')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player'
    if not playAgain():
        break



