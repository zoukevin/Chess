
class Piece():

    @staticmethod
    def isValid(position, newPosition, pieceType):
        print(position)
        print(newPosition)
        print(pieceType)
        currentX = position[0]
        currentY = position[1]
        newX = newPosition[0]
        newY = newPosition[1]
        if (pieceType == 7):
            if (currentY == newY):
                if (abs(newX - currentX) == 1):
                    return True
            elif (currentX == newX):
                if (abs(newY - currentY) == 1):
                    return True
            else:
                return False

        return True

