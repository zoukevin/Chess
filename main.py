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
selectedPieceIndices = (0,0)
oldLocation = (0,0)
newLocation = (0,0)
turn = True
dragging = False
pieceIsDragged = False
turnNumber = 1
whiteMoves = []
blackMoves = []
allMoves = []
numTurnsShown = 10
wood, white, black, red, gray = ("#DEB887", "#FFFFFF", "#000000", "#FF0606", "#D3D3D3")
moveColor = white
prevMovedPiece = 12
prevMove = ((0, 0), (0, 0))
defeatedWhite = []
defeatedBlack = []
movePiece = False
castleFlags = [False, False, False, False, False, False] #wlR, wrR, wk, blR, brR, bk

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
smallImages = {}
for i in pieceNames:
    images[i] = pygame.transform.scale(pygame.image.load("assets/" + i + ".png"), (squareWidth, squareWidth))
    smallImages[i] = pygame.transform.scale(pygame.image.load("assets/" + i + ".png"), (math.floor(squareWidth*5/8), math.floor(squareWidth*5/8)))

#Initialize board state
board = np.zeros((8,8), dtype = int) #Creates matrix with numpy (y, x)
board[:,:] = 12 #Initialise pieces to none
board[0, :] = [bR, bN, bB, bQ, bK, bB, bN, bR] 
board[1, :] = bp
board[7, :] = [wR, wN, wB, wQ, wK, wB, wN, wR]
board[6, :] = wp

selectedPieceType = board[selectedPieceIndices]

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
                castleFlags = [False, False, False, False, False, False]
                defeatedWhite = []
                defeatedBlack = []

        #Mouse click to move
        if pygame.mouse.get_pressed()[0]:
            clickedIndices = (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and dragging == False:
                #Prepare to select a piece.
                if (isPieceSelected == False): 
                    isPieceSelected = True
                    selectedPieceIndices = clickedIndices
                    selectedPieceType = board[selectedPieceIndices]
                    if (turn and selectedPieceType < 6) or (turn == False and selectedPieceType > 5):
                        isPieceSelected = False
                    #If the square is empty, then reset the selected piece.
                    if board[selectedPieceIndices] == 12:
                        selectedPieceIndices = (0, 0)
                        isPieceSelected = False 
                    dragging = False

                #Move the selected piece and remove the previous position from the board
                else:
                    isPieceSelected = False
                    if Piece.isValid(selectedPieceIndices, clickedIndices, selectedPieceType, board[clickedIndices], board, prevMovedPiece, prevMove, castleFlags):
                        movePiece = True
                    dragging = False

            #Mouse drag to move
            if event.type == pygame.MOUSEMOTION:
                #Make the piece follow the mouse cursor 
                if isPieceSelected and pieceIsDragged == False:
                    selectedPieceType = board[selectedPieceIndices]
                    board[selectedPieceIndices] = 12
                    pieceIsDragged = True           
                dragging = True   
                #Prepare to select a piece. 
                if (isPieceSelected == False):
                    isPieceSelected = True
                    selectedPieceIndices = clickedIndices
                    if (turn and board[selectedPieceIndices] < 6) or (turn == False and board[selectedPieceIndices] > 5):
                        isPieceSelected = False
                    # #If the square is empty, then reset the selected piece
                    if board[selectedPieceIndices] == 12:
                        selectedPieceIndices = (0, 0)
                        isPieceSelected = False 
                    dragging = False

        if event.type == pygame.MOUSEBUTTONUP and dragging == True:
            #Move the selected piece and remove the previous position from the board
            if isPieceSelected:
                isPieceSelected = False
                if Piece.isValid(selectedPieceIndices, clickedIndices, selectedPieceType, board[clickedIndices], board, prevMovedPiece, prevMove, castleFlags):
                    movePiece = True
                else:
                    board[selectedPieceIndices] = selectedPieceType
                pieceIsDragged = False
                dragging = False

        #Update board logic
        if movePiece:
            movePiece = False
            if ((selectedPieceType == 9) or (selectedPieceType == 3)) and Piece.enPessant(selectedPieceIndices, clickedIndices, selectedPieceType, board[clickedIndices], board, prevMovedPiece, prevMove):
                board[selectedPieceIndices[0], selectedPieceIndices[1] + (clickedIndices[1] - selectedPieceIndices[1])] = 12
            if selectedPieceIndices == (7, 0) or clickedIndices == (7, 0) :
                castleFlags[0] = True
            elif selectedPieceIndices == (7, 7) or clickedIndices == (7, 7) :
                castleFlags[1] = True
            elif selectedPieceIndices == (7, 4) or clickedIndices == (7, 4) :
                castleFlags[2] = True
            elif selectedPieceIndices == (0, 0) or clickedIndices == (0, 0) :
                castleFlags[3] = True
            elif selectedPieceIndices == (0, 7) or clickedIndices == (0, 7) :
                castleFlags[4] = True
            elif selectedPieceIndices == (0, 4) or clickedIndices == (0, 4) :
                castleFlags[5] = True
            
            oldLocation = selectedPieceIndices
            newLocation = clickedIndices
            prevMove = (oldLocation, newLocation)
            prevMovedPiece = selectedPieceType

            if board[clickedIndices] < 6:
                defeatedBlack.append(board[clickedIndices])
            elif board[clickedIndices] < 12:
                defeatedWhite.append(board[clickedIndices])
            board[clickedIndices] = selectedPieceType
            
            savedMove = (string.ascii_lowercase[selectedPieceIndices[1]] + str(9 - (selectedPieceIndices[0] + 1)), string.ascii_lowercase[clickedIndices[1]] + str(9 - (clickedIndices[0] + 1)))
            if turn == True:
                whiteMoves.append(savedMove)
                allMoves.append(savedMove)
            else:
                blackMoves.append(savedMove)
                allMoves.append(savedMove)
                
            turn = False if turn == True else True
            turnNumber += 1
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and dragging == False:
                board[selectedPieceIndices] = 12
            

    #Draw the chessboard
    for x in range(8):
        for y in range(8):
            if isPieceSelected and (x, y) == selectedPieceIndices:
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
        window.blit(images[pieceNames[selectedPieceType]], (math.floor(pos[0] - squareWidth // 2), math.floor(pos[1] - squareWidth // 2)))

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
        window.blit(moveText,(9.3*squareWidth, i*50 + squareWidth))
        moveText = myfont.render(str(allMoves[moveIndex][0]), True, tempColor)
        window.blit(moveText,(9.8*squareWidth, i*50 + squareWidth))
        moveText = myfont.render(str(allMoves[moveIndex][1]), True, tempColor)
        window.blit(moveText,(10.3*squareWidth, i*50 + squareWidth))
        tempColor = black if tempColor == white else white

    #Display defeated pieces
    pieceOffset = 0
    for i in defeatedWhite:
        window.blit(smallImages[pieceNames[i]], (squareWidth*8 + pieceOffset, screenHeight - 100))
        pieceOffset += 25

    pieceOffset = 0
    for i in defeatedBlack:
        window.blit(smallImages[pieceNames[i]], (squareWidth*8 + pieceOffset, 0))
        pieceOffset += 25

    pygame.display.update()
    timer.tick(fps)

