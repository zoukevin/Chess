
class Piece():

    @staticmethod
    def isValid(position, newPosition, pieceType, targetPieceType, board, prevMovedPiece, prevMove, castleFlags):
        print(castleFlags)
        if not(Piece.isPiecePattern(position, newPosition, pieceType, targetPieceType, board, prevMovedPiece, prevMove)):
            return False
        if Piece.isTargetTeam(position, newPosition, pieceType, targetPieceType):
            return False
        if Piece.isPathCollision(position, newPosition, pieceType, targetPieceType, board):
            return False
        return True

    @staticmethod
    def isPathCollision(position, newPosition, pieceType, targetPieceType, board): #Queen, bishop, rook, pawn
        checkY = []
        checkX = []

        if (pieceType == 10) or (pieceType == 4) or (pieceType == 5) or (pieceType == 11) or (pieceType == 6) or (pieceType == 0) or (pieceType == 3) or (pieceType == 9):
            stride = 1 if newPosition[0] < position[0] else -1
            for i in range(newPosition[0], position[0] + stride, stride):
                checkY.append(i)
            stride = 1 if newPosition[1] < position[1] else -1
            for i in range(newPosition[1], position[1] + stride, stride):
                checkX.append(i)
            while(len(checkX) != len(checkY)):
                if len(checkX) < len(checkY):
                    checkX.append(checkX[0])
                else:
                    checkY.append(checkY[0])
            for i in range(len(checkX)):
                if (board[checkY[i], checkX[i]] != 12) and ((checkY[i], checkX[i]) != position) and ((checkY[i], checkX[i]) != newPosition):
                    return True
        return False

    #Returns true if the move follows a correct pattern of the piece
    @staticmethod
    def isTargetTeam(position, newPosition, pieceType, targetPieceType):
        if (pieceType <= 5):
            if (targetPieceType <= 5):
                return True
        elif (pieceType <= 11):
            if (6 <= targetPieceType <= 11):
                return True
        return False
        #King

    @staticmethod
    def isTargetEnemy(position, newPosition, pieceType, targetPieceType):
        if (pieceType <= 5):
            if (6 <= targetPieceType <= 11):
                return True
        elif (pieceType <= 11):
            if (targetPieceType <= 5):
                return True
        return False

    #Check both sides for enpessant validity
    @staticmethod
    def enPessant(position, newPosition, pieceType, targetPieceType, board, prevMovedPiece, prevMove):
        checkLeft = position[0], position[1] - 1
        checkRight = position[0], position[1] + 1
        validEP = False
        checkDirection = checkLeft

        #Correct row and turn to enpessant
        if (prevMove[0][0] == 1 and prevMove[1][0] == 3 and prevMovedPiece == 3) or (prevMove[0][0] == 6 and prevMove[1][0] == 4 and prevMovedPiece == 9):  
            if Piece.isTargetEnemy(position, checkLeft, pieceType, board[checkLeft]):   #Check for direction the pawn is enpessanting   
                checkDirection = checkLeft
                if board[checkLeft] == 3 or board[checkLeft] == 9: #Ensure the piece taken is a pawn
                    validEP = True
            if Piece.isTargetEnemy(position, checkRight, pieceType, board[checkRight]):
                checkDirection = checkRight
                if board[checkRight] == 3 or board[checkRight] == 9:
                    validEP = True

            return True if validEP == True and (checkDirection[1] == prevMove[1][1]) and (checkDirection[1] == newPosition[1]) else False

        else:
            return False

    #Returns true if the move follows a correct pattern of the piece
    @staticmethod
    def isPiecePattern(position, newPosition, pieceType, targetPieceType, board, prevMovedPiece, prevMove):

        if position == newPosition:
            return False

        #King
        if (pieceType == 7) or (pieceType == 1):
            if (position[1] == newPosition[1]):
                if (abs(newPosition[0] - position[0]) == 1):
                    return True
            elif (position[0] == newPosition[0]):
                if (abs(newPosition[1] - position[1]) == 1):
                    return True
            elif (abs(newPosition[1] - position[1]) == 1) and (abs(newPosition[0] - position[0]) == 1):
                return True
            return False

        #Pawn
        if (pieceType == 9) or (pieceType == 3):
            #Check for piece color and row position
            isWhite = 1 if pieceType == 9 else -1
            spawnPawnPos = 6 if isWhite == 1 else 1
            if (position[1] == newPosition[1]): #If moving straight vertically
                if ((position[0] - newPosition[0])*isWhite == 1):
                    if Piece.isTargetEnemy(position, newPosition, pieceType, targetPieceType):
                        return False
                    return True
                elif (((position[0] - newPosition[0])*isWhite == 2) and (position[0] == spawnPawnPos)):
                    if Piece.isTargetEnemy(position, newPosition, pieceType, targetPieceType):
                        return False
                    return True
            elif (abs(newPosition[1] - position[1]) == 1) and ((position[0] - newPosition[0])*isWhite == 1): #Taking piece diagonally
                if Piece.isTargetEnemy(position, newPosition, pieceType, targetPieceType):
                    return True
                elif Piece.enPessant(position, newPosition, pieceType, targetPieceType, board, prevMovedPiece, prevMove):
                    return True
            return False

        #Queen
        if (pieceType == 10) or (pieceType == 4):
            if (position[1] == newPosition[1]):
                return True
            elif (position[0] == newPosition[0]):
                return True
            elif (abs(newPosition[1] - position[1])) == (abs(newPosition[0] - position[0])):
                return True
            return False

        #Bishop
        if (pieceType == 6) or (pieceType == 0):
            if (abs(newPosition[1] - position[1])) == (abs(newPosition[0] - position[0])):
                return True
            return False

        #Knight
        if (pieceType == 8) or (pieceType == 2):
            if (abs(position[1] - newPosition[1]) == 2) and (abs(position[0] - newPosition[0]) == 1):
                return True
            elif (abs(position[0] - newPosition[0]) == 2) and (abs(position[1] - newPosition[1]) == 1):
                return True
            return False

        #Rook
        if (pieceType == 5) or (pieceType == 11):
            if (position[1] == newPosition[1]):
                return True
            elif (position[0] == newPosition[0]):
                return True
            return False


        return True





