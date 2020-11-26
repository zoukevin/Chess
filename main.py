import pygame, sys
from pygame.locals import *
import numpy as np
import math

screenWidth = 1280
screenHeight = 800
squareWidth = 100
timer = None
window = None
fps = 30

wood, white, black = ("#deb887", "#ffffff", "#D3D3D3")

def InitPygame(screenWidth, screenHeight):
    global window
    global timer
    
    pygame.init()
    timer = pygame.time.Clock()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption( "Chess!" )

InitPygame(screenWidth, screenHeight)

#Black Pieces
bB = 0
bK = 1
bN = 2
bp = 3
bQ = 4
bR = 5

#White Pieces
wB = 6
wK = 7
wN = 8
wp = 9
wQ = 10
wR = 11

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
            if (isPieceSelected == False):
                #If piece is selected, prepare to move it. 
                isPieceSelected = True
                pieceSelected = (math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth))
                #If the square is empty, then reset the selected piece.
                if board[pieceSelected] == 12:
                    pieceSelected = (0, 0)
                    isPieceSelected = False 
            else:
                #Move the piece
                isPieceSelected = False
                board[math.floor(pos[1]/squareWidth), math.floor(pos[0]/squareWidth)] = board[pieceSelected[0], pieceSelected[1]] #Assigns the new position to the clicked piece
                board[pieceSelected[0], pieceSelected[1]] = 12
                #If mouse is being held down
                    #Draw at mouse position by deleting the piece first then making it follow the cursor
                
    #Draw the chessboard
    for x in range(8):
        for y in range(8):
            color = white if (((x + y) % 2) == 0) else black
            pygame.draw.rect(window, color, pygame.Rect((y * squareWidth), (x * squareWidth), squareWidth, squareWidth))
            if (board[x, y] != 12):
                window.blit(images[pieceNames[board[x, y]]], (y*squareWidth, x*squareWidth))

    pygame.display.flip()
    timer.tick(fps)

