#hello

import pygame, sys
from pygame.locals import *

screenWidth = 1280
screenHeight = 720
timer = None
window = None
fps = 30


bgColor = pygame.Color( 255, 255, 255 )
imgKing = pygame.image.load( "king.png" )

def InitPygame(screenWidth, screenHeight):
    global window
    global timer
    
    pygame.init()
    timer = pygame.time.Clock()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption( "Chess!" )

InitPygame(screenWidth, screenHeight)

finished = False
while finished == False:
    
    for event in pygame.event.get():
        if ( event.type == QUIT ):
            finished = True
        
    window.fill(bgColor)
    
    window.blit(imgKing, (0, 0))
    
    pygame.display.update()
    timer.tick(fps)


