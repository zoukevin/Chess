class Piece:
    def __init__(self, classPiece, position):
        self.classPiece = classPiece
        self.position = position

    def isValid(newPosition):
        pass

    def movePiece(newPosition):
        position = newPosition

class King(Piece):
    def __init__(self, classPiece, position):
        super().__init__(self, classPiece, position)

    def isValid(newPosition):
        currentX = position[0]
        currentY = position[1]
        newX = newPosition[0]
        newY = newPosition[1]
        if (currentY == newY):
            if (abs(newX - currentX) == 1):
                return True
        if (currentX == newX):
            if (abs(newY - currentY) == 1):
                return True

        return False

    def movePiece(newPosition):
        if isValid(newPosition):
            super().movePiece(newPosition)

