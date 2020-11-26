
class Piece():

    @staticmethod
    def isValid(position, newPosition, pieceType):
        return Piece.isPiecePattern(position, newPosition, pieceType)

    #Returns true if the move follows a correct pattern of the piece
    @staticmethod
    def isPiecePattern(position, newPosition, pieceType):
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

        return True


