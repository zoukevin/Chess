import pygame, sys
from pygame.locals import *
import numpy as np
import math
from pieces import *

screenWidth = 1280
screenHeight = 800
squareWidth = 100
timer = None
window = None
fps = 30

finished = False
isPieceSelected = False
pieceSelected = (0,0)
turn = True
dragging = False
pieceIsDragged = False

wood, white, black, red = ("#DEB887", "#FFFFFF", "#D3D3D3", "#FF0606")

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

window.fill(wood)

while finished == False:
    
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if ( event.type == QUIT ):
            finished = True

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
                    if Piece.isValid(pieceSelected, (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)), board[pieceSelected], board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)], board):
                        board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)] = board[pieceSelected]
                        board[pieceSelected] = 12
                        turn = False if turn == True else True

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

                if Piece.isValid(pieceSelected, (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)), movingPiece, board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)], board):
                    board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)] = movingPiece
                    turn = False if turn == True else True     
                else:
                    board[pieceSelected] = movingPiece
                pieceIsDragged = False
                dragging = False

    #Draw the chessboard
    for x in range(8):
        for y in range(8):
            color = white if (((x + y) % 2) == 0) else black
            if isPieceSelected and (x, y) == pieceSelected:
                color = red
            else:
                color = white if (((x + y) % 2) == 0) else black

            pygame.draw.rect(window, color, pygame.Rect((y * squareWidth), (x * squareWidth), squareWidth, squareWidth))
            if (board[x, y] != 12):
                window.blit(images[pieceNames[board[x, y]]], (y*squareWidth, x*squareWidth))
    
    if pieceIsDragged:
        window.blit(images[pieceNames[movingPiece]], (math.floor(pos[0] - squareWidth // 2), math.floor(pos[1] - squareWidth // 2)))

    pygame.display.flip()
    timer.tick(fps)

