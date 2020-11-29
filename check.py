from pieces import *
import pygame, sys
from pygame.locals import *
import copy

class Check():

    @staticmethod
    # def isCheck(pieceType, boardCurrent, prevMovedPiece, prevMove, castleFlags):
    def isCheck(selectedPieceIndices, clickedIndices, selectedPieceType, targetPieceType, originalBoard, prevMovedPiece, prevMove, castleFlags, eventType, eventButton, dragging):
        
        board = copy.deepcopy(originalBoard)
        
        board[selectedPieceIndices] = 12

        if ((selectedPieceType == 9) or (selectedPieceType == 3)) and Piece.enPessant(selectedPieceIndices, clickedIndices, selectedPieceType, board[clickedIndices], board, prevMovedPiece, prevMove):
                board[selectedPieceIndices[0], selectedPieceIndices[1] + (clickedIndices[1] - selectedPieceIndices[1])] = 12
        oldLocation = selectedPieceIndices
        newLocation = clickedIndices
        prevMove = (oldLocation, newLocation)
        prevMovedPiece = selectedPieceType

        board[clickedIndices] = selectedPieceType

        if eventType == pygame.MOUSEBUTTONDOWN and eventButton == 1 and dragging == False:
            board[selectedPieceIndices] = 12

        ownKingLoc = (0, 0)
        if selectedPieceType >= 6:
            #Get own King location
            for x in range(8):
                for y in range(8):
                    if board[y, x] == 7:
                        ownKingLoc = (y, x)
                        break
            #Get enemy pieces
            for i in range(8):
                for j in range(8):
                    if (board[i,j] <= 5):
                        targetPieceType = board[i,j]
                        #Check if enemy piece can take king
                        if Piece.isValid((i, j), ownKingLoc, targetPieceType, 7, board, prevMovedPiece, prevMove, castleFlags):
                            return False
        elif selectedPieceType < 12:
            #Get own King location
            for x in range(8):
                for y in range(8):
                    if board[y, x] == 1:
                        ownKingLoc = (y, x)
                        break
            #Get enemy pieces
            for i in range(8):
                for j in range(8):
                    if (board[i,j] >= 6) and board[i,j] != 12:
                        targetPieceType = board[i,j]
                        #Check if enemy piece can take king
                        if Piece.isValid((i, j), ownKingLoc, targetPieceType, 1, board, prevMovedPiece, prevMove, castleFlags):
                            return False
        
        return True
