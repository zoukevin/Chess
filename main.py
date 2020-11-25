#hello

import pygame, sys
from pygame.locals import *
import numpy as np
import math

screenWidth = 1280
screenHeight = 800
timer = None
window = None
fps = 30

wood = ("#deb887")
white = ("#ffffff")
black = ("#000000")

pieceNames = ["bB", "bK", "bN", "bp", "bQ", "bR",               "wB", "wK", "wN", "wp", "wQ", "wR"]
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

#1,2,3,...,12 = black: bishop, king, knight, pawn, queen, rook, white:...
board = np.zeros((8,8), dtype = int)
board[:,:] = 12
#white pieces
board[0, :] = [11, 6, 8, 7, 10, 8, 6, 11]
board[1, :] = 9


#black pieces
board[7, :] = [5, 0, 2, 4, 1, 2, 0, 5]
board[6, :] = 3


finished = False
isPieceSelected = False
pieceSelected = (0,0)
while finished == False:
    
    for event in pygame.event.get():
        if ( event.type == QUIT ):
            finished = True
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if (isPieceSelected == True):
                isPieceSelected = False
                #move the piece
                print("moving piece")
                print(pieceSelected)
                board[math.floor(pos[1]/80), math.floor(pos[0]/80)] = board[pieceSelected[0], pieceSelected[1]]
                board[pieceSelected[0], pieceSelected[1]] = 12
            else:
                isPieceSelected = True
                pieceSelected = (math.floor(pos[1]/80), math.floor(pos[0]/80))
                print(pieceSelected)

        
    window.fill(wood)

    for x in range(8):
        #square_y = []
        for y in range(8):
            #square_y.append(y)
            if (((x + y) % 2) == 0):
                color = white
            else:
                color = black    
            #square_x.append(square_y)
            pygame.draw.rect(window, color, pygame.Rect((x * 80), (y * 80), 80, 80))

    for i in range(8):
        for j in range(8):
            if (board[i, j] != 12):
                window.blit(images[pieceNames[board[i, j]]], (j*80, i*80))
    
    
    pygame.display.update()
    timer.tick(fps)


