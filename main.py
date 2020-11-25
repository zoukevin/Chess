#hello

import pygame, sys
from pygame.locals import *
import numpy as np
import math

screenWidth = 1280
screenHeight = 800
squareWidth = 80
timer = None
window = None
fps = 30

wood, white, black = ("#deb887", "#ffffff", "#D3D3D3")

pieceNames = ["bB", "bK", "bN", "bp", "bQ", "bR", "wB", "wK", "wN", "wp", "wQ", "wR"]
images = {}
for i in pieceNames:
    images[i] = pygame.transform.scale(pygame.image.load("assets/" + i + ".png"), (80, 80))

bgColor = pygame.Color( 255, 255, 255 )

def InitPygame(screenWidth, screenHeight):
    global window
    global timer
    
    pygame.init()
    timer = pygame.time.Clock()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption( "Chess!" )

InitPygame(screenWidth, screenHeight)

board = np.zeros((8,8), dtype = int) #Creates matrix with numpy

board[:,:] = 12 #Initialise pieces to none

#Black Pieces
#0 - Bishop
#1 - King
#2 - Knight
#3 - Pawn
#4 - Queen
#5 - Rook

#White Pieces
#6 - Bishop
#7 - King
#8 - Knight
#9 - Pawn
#10 - Queen
#11 - Rook

#White pieces
board[0, :] = [5, 2, 0, 4, 1, 0, 2, 5] 
board[1, :] = 3

#Black pieces
board[7, :] = [11, 8, 6, 10, 7, 6, 8, 11]
board[6, :] = 9

finished = False
isPieceSelected = False
pieceSelected = (0,0)

window.fill(wood)

while finished == False:
    
    for event in pygame.event.get():
        if ( event.type == QUIT ):
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if (isPieceSelected == True):
                isPieceSelected = False
                #move the piece
                print("moving piece")
                print(pieceSelected)
                #Assigns the new position to the clicked piece
                board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)] = board[pieceSelected[0], pieceSelected[1]]
                board[pieceSelected[0], pieceSelected[1]] = 12
                #If mouse is being held down
                    #Draw at mouse position by deleting the piece first then making it follow the cursor
            else:
                #If piece is selected, prepare to move it
                isPieceSelected = True
                pieceSelected = (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth))
                print(pieceSelected)

    #Draw the chessboard
    for x in range(8):
        for y in range(8):
            if (((x + y) % 2) == 0):
                color = white
            else:
                color = black    
            pygame.draw.rect(window, color, pygame.Rect((x * 80), (y * 80), 80, 80))

    for i in range(8):
        for j in range(8):
            if (board[i, j] != 12):
                window.blit(images[pieceNames[board[i, j]]], (j*80, i*80))
       
    pygame.display.flip()
    timer.tick(fps)