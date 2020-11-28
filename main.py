import pygame, sys
from pygame.locals import *
import numpy as np
import math
from pieces import *
import string

screenWidth = 1280
screenHeight = 800
squareWidth = 100
timer = None
window = None
fps = 60

finished = False
isPieceSelected = False
pieceSelected = (0,0)
oldLocation = (0,0)
newLocation = (0,0)
turn = True
dragging = False
pieceIsDragged = False
turnNumber = 1
whiteMoves = []
blackMoves = []
allMoves = []
numTurnsShown = 14
wood, white, black, red, gray = ("#DEB887", "#FFFFFF", "#000000", "#FF0606", "#D3D3D3")
moveColor = white
prevMovedPiece = 12
prevMove = (0, 0)

def InitPygame(screenWidth, screenHeight):
    global window
    global timer
    
    pygame.init()
    timer = pygame.time.Clock()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption( "Chess" )

InitPygame(screenWidth, screenHeight)

#Black Pieces
bB, bK, bN, bp, bQ, bR = 0, 1, 2, 3, 4, 5

#White Pieces
wB, wK, wN, wp, wQ, wR = 6, 7, 8, 9, 10, 11

#Load piece images
pieceNames = ["bB", "bK", "bN", "bp", "bQ", "bR", "wB", "wK", "wN", "wp", "wQ", "wR"]
images = {}
for i in pieceNames:
    images[i] = pygame.transform.scale(pygame.image.load("assets/" + i + ".png"), (squareWidth, squareWidth))

#Initialize board state
board = np.zeros((8,8), dtype = int) #Creates matrix with numpy (y, x)
board[:,:] = 12 #Initialise pieces to none
board[0, :] = [bR, bN, bB, bQ, bK, bB, bN, bR] 
board[1, :] = bp
board[7, :] = [wR, wN, wB, wQ, wK, wB, wN, wR]
board[6, :] = wp

while finished == False:
    window.fill(wood)
    
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if ( event.type == QUIT ):
            finished = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board[:,:] = 12 #Initialise pieces to none
                board[0, :] = [bR, bN, bB, bQ, bK, bB, bN, bR] 
                board[1, :] = bp
                board[7, :] = [wR, wN, wB, wQ, wK, wB, wN, wR]
                board[6, :] = wp
                turn = True
                whiteMoves = []
                blackMoves = []
                allMoves = []
                turnNumber = 1

        #Mouse click to move
        if pygame.mouse.get_pressed()[0]:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and dragging == False:
                #Prepare to select a piece.
                if (isPieceSelected == False): 
                    isPieceSelected = True
                    pieceSelected = (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth))
                    if (turn and board[pieceSelected] < 6) or (turn == False and board[pieceSelected] > 5):
                        isPieceSelected = False
                    #If the square is empty, then reset the selected piece.
                    if board[pieceSelected] == 12:
                        pieceSelected = (0, 0)
                        isPieceSelected = False 
                    dragging = False

                #Move the selected piece and remove the previous position from the board
                else:
                    isPieceSelected = False
                    if Piece.isValid(pieceSelected, (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)), board[pieceSelected], board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)], board, prevMovedPiece, prevMove):
                        board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)] = board[pieceSelected]
                        oldLocation = pieceSelected
                        newLocation = (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth))
                        savedMove = (string.ascii_lowercase[pieceSelected[1]] + str(9 - (pieceSelected[0] + 1)), string.ascii_lowercase[math.floor(pos[0]/squareWidth)] + str(9 - (math.floor(pos[1]/squareWidth) + 1)))
                        if turn == True:
                            whiteMoves.append(savedMove)
                            allMoves.append(savedMove)
                        else:
                            blackMoves.append(savedMove)
                            allMoves.append(savedMove)
                        turn = False if turn == True else True
                        turnNumber += 1
                        board[pieceSelected] = 12
                        prevMovedPiece = movingPiece
                        prevMove = (oldLocation, newLocation)
                    dragging = False

            #Mouse drag to move
            if event.type == pygame.MOUSEMOTION:
                #Make the piece follow the mouse cursor 
                if isPieceSelected and pieceIsDragged == False:
                    movingPiece = board[pieceSelected]
                    board[pieceSelected] = 12
                    pieceIsDragged = True           
                dragging = True   
                #Prepare to select a piece. 
                if (isPieceSelected == False):
                    isPieceSelected = True
                    pieceSelected = (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth))
                    if (turn and board[pieceSelected] < 6) or (turn == False and board[pieceSelected] > 5):
                        isPieceSelected = False
                    # #If the square is empty, then reset the selected piece
                    if board[pieceSelected] == 12:
                        pieceSelected = (0, 0)
                        isPieceSelected = False 
                    dragging = False

        if event.type == pygame.MOUSEBUTTONUP and dragging == True:
            #Move the selected piece and remove the previous position from the board
            if isPieceSelected:
                isPieceSelected = False
                if Piece.isValid(pieceSelected, (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)), movingPiece, board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)], board, prevMovedPiece, prevMove):
                    board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)] = movingPiece
                    oldLocation = pieceSelected
                    newLocation = (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth))
                    savedMove = (string.ascii_lowercase[pieceSelected[1]] + str(9 - (pieceSelected[0] + 1)), string.ascii_lowercase[math.floor(pos[0]/squareWidth)] + str(9 - (math.floor(pos[1]/squareWidth) + 1)))
                    if turn == True:
                        whiteMoves.append(savedMove)
                        allMoves.append(savedMove)
                    else:
                        blackMoves.append(savedMove)
                        allMoves.append(savedMove)
                    turn = False if turn == True else True
                    turnNumber += 1
                    prevMovedPiece = board[pieceSelected]
                    prevMove = (oldLocation, newLocation)
                else:
                    board[pieceSelected] = movingPiece
                pieceIsDragged = False
                dragging = False

    #Draw the chessboard
    for x in range(8):
        for y in range(8):
            if isPieceSelected and (x, y) == pieceSelected:
                color = red
            else:
                color = white if (((x + y) % 2) == 0) else gray
            if (turnNumber != 1):
                if (x, y) == oldLocation or (x, y) == newLocation:
                    color = "#FFFF00"	
            pygame.draw.rect(window, color, pygame.Rect((y * squareWidth), (x * squareWidth), squareWidth, squareWidth))
            
            if (board[x, y] != 12):
                window.blit(images[pieceNames[board[x, y]]], (y*squareWidth, x*squareWidth))
    
    #Draw piece on moving cursor
    if pieceIsDragged:
        window.blit(images[pieceNames[movingPiece]], (math.floor(pos[0] - squareWidth // 2), math.floor(pos[1] - squareWidth // 2)))

    #Display king for turn indicator
    if (turn == True):
        window.blit(images[pieceNames[7]], (squareWidth*8, screenHeight - 200))
    else:
        window.blit(images[pieceNames[1]], (squareWidth*8, 200))

    #Display grid labels
    myfont = pygame.font.SysFont('Comic Sans MS', 22)
    colLabels = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for x in range(8):
        colText = myfont.render(colLabels[x], True, red)
        (textWidth, textHeight) = colText.get_size()
        window.blit(colText,((x+1)*squareWidth - textWidth, 8*squareWidth - textHeight))
        rowText = myfont.render(str(9 - (x + 1)), False, red)
        window.blit(rowText,(0, x*squareWidth))

    #Display moves played for every turn
    if len(allMoves) > numTurnsShown:
        moveColor = white if turn == True else black
    tempColor = moveColor
    for i in range(len(allMoves)):
        if i == numTurnsShown:
            break
        moveIndex = i
        if len(allMoves) > numTurnsShown:
            moveIndex = len(allMoves) - numTurnsShown + i
        moveText = myfont.render(str(moveIndex//2 + 1) + ".", True, tempColor)
        window.blit(moveText,(9.3*squareWidth, i*50 + 50))
        moveText = myfont.render(str(allMoves[moveIndex][0]), True, tempColor)
        window.blit(moveText,(9.8*squareWidth, i*50 + 50))
        moveText = myfont.render(str(allMoves[moveIndex][1]), True, tempColor)
        window.blit(moveText,(10.3*squareWidth, i*50 + 50))
        tempColor = black if tempColor == white else white

    pygame.display.update()
    timer.tick(fps)

