
class Piece():

    @staticmethod
    def isValid(position, newPosition, pieceType, targetPieceType, board, prevMovedPiece, prevMove, castleFlags):
        if not(Piece.isPiecePattern(position, newPosition, pieceType, targetPieceType, board, prevMovedPiece, prevMove, castleFlags)):
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
        if (prevMove[0][0] == 1 and prevMove[1][0] == 3) or (prevMove[0][0] == 6 and prevMove[1][0] == 4): #If Pawn moves forward twice
            if board[newPosition] == 12:
                if newPosition[1] == prevMove[1][1]: #Checks for the direction the piece is moving in is correct
                    #Checks for the piece you are taking is a pawn
                    if Piece.isTargetEnemy(position, newPosition, pieceType, board[prevMove[1]]) and board[prevMove[1]] == 3 or board[prevMove[1]] == 9: 
                        return True
                return False

    #Returns true if the move follows a correct pattern of the piece
    @staticmethod
    def isPiecePattern(position, newPosition, pieceType, targetPieceType, board, prevMovedPiece, prevMove, castleFlags):

        if position == newPosition:
            return False

        #King
        #TO DO HARD CODE POSITION TO MAKE SURE ITS EMPTY BEFORE CASTLING
        if (pieceType == 7) or (pieceType == 1):
            if (position[1] == newPosition[1]):
                if (abs(newPosition[0] - position[0]) == 1):
                    return True
            elif (position[0] == newPosition[0]):
                if (abs(newPosition[1] - position[1]) == 1):
                    return True
                if (abs(newPosition[1] - position[1]) == 2): #Castles
                    if pieceType == 7 and castleFlags[2] == False: #White King
                        if newPosition[1] == 2 and castleFlags[0] == False: #lwR
                            print('leftCastle')
                            return True
                        elif newPosition[1] == 6 and castleFlags[1] == False: #rwR
                            print('rightCastle')
                            return True
                    if pieceType == 1 and castleFlags[5] == False: #Black King
                        if newPosition[1] == 2 and castleFlags[3] == False: #lbR
                            print('leftCastle')
                            return True
                        elif newPosition[1] == 6 and castleFlags[4] == False: #rbR
                            print('rightCastle')
                            return True
                    return False
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





