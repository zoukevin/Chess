
class Piece():

    @staticmethod
    def isValid(position, newPosition, pieceType, targetPieceType):
        if not(Piece.isPiecePattern(position, newPosition, pieceType, targetPieceType)):
            return False
        return True

    #Returns true if the move follows a correct pattern of the piece
    @staticmethod
    def isPiecePattern(position, newPosition, pieceType, targetPieceType):
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
            if (position[1] == newPosition[1]):
                isWhite = 1 if pieceType == 9 else -1
                spawnPawnPos = 6 if isWhite == 1 else 1
                if ((position[0] - newPosition[0])*isWhite == 1):
                    return True
                elif (((position[0] - newPosition[0])*isWhite == 2) and (position[0] == spawnPawnPos)):
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

        return True





