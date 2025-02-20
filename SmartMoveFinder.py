import random
import Engine

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [[0,1,2,2,2,2,1,0],
                [1,3,5,5,5,5,3,1],
                [2,5,6,6.5,6.5,6,5,2],
                [2,5.5,6.5,7,7,6.5,5.5,2],
                [2,5,6.5,7,7,6.5,5,2],
                [2,5.5,6,6.5,6.5,6,5.5,2],
                [1,3,5,5.5,5.5,5,3,1],
                [0,1,2,2,2,2,1,0]]

bishopScores = [[0,2,2,2,2,2,2,0],
                [2,4,4,4,4,4,4,2],
                [2,4,5,6,6,5,4,2],
                [2,5,5,6,6,5,5,2],
                [2,4,6,6,6,6,4,2],
                [2,6,6,6,6,6,6,2],
                [2,5,4,4,4,4,5,2],
                [0,2,2,2,2,2,2,0]]

queenScores = [[0,2,2,3,3,2,2,0],
               [2,4,4,4,4,4,4,2],
               [2,4,5,5,5,5,4,2],
               [3,4,5,5,5,5,4,3],
               [4,4,5,5,5,5,4,3],
               [2,5,5,5,5,5,4,2],
               [2,4,5,4,4,4,4,2],
               [0,2,2,3,3,2,2,0]]
               
rookScores = [[2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5],
              [5,7.5,7.5,7.5,7.5,7.5,7.5,5],
              [0,2.5,2.5,2.5,2.5,2.5,2.5,0],
              [0,2.5,2.5,2.5,2.5,2.5,2.5,0],
              [0,2.5,2.5,2.5,2.5,2.5,2.5,0],
              [0,2.5,2.5,2.5,2.5,2.5,2.5,0],
              [0,2.5,2.5,2.5,2.5,2.5,2.5,0],
              [2.5,2.5,2.5,5,5,2.5,2.5,2.5]]
              
pawnScores = [[8,8,8,8,8,8,8,8],
              [7,7,7,7,7,7,7,7],
              [3,3,4,5,5,4,3,3],
              [2.5,2.5,3,4.5,4.5,3,2.5,2.5],
              [2,2,2,4,4,2,2,2],
              [2.5,1.5,1,2,2,1,1.5,2.5],
              [2.5,3,3,0,0,3,3,2.5],
              [2,2,2,2,2,2,2,2]]
                 
piecePositionScores = {"wN": knightScores,
                       "bN": knightScores[::-1],
                       "wQ": queenScores,
                       "bQ": queenScores[::-1],           
                       "wB": bishopScores,
                       "bB": bishopScores[::-1],               
                       "wR": rookScores,
                       "bR": rookScores[::-1],                   
                       "wp": pawnScores, 
                       "bp": pawnScores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]
    
def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE,1 if gs.whiteToMove else -1)
    returnQueue.put(nextMove)
        
def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore = STALEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()      
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore    
        
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore
    
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
        
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square[1] != "K":
                    piecePositionScore = piecePositionScores[square][row][col]
                if square[0] == "w":
                    score += pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == "b":
                    score -= pieceScore[square[1]] + piecePositionScore * .1
    return score    
    
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]
    return score
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    