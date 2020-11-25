#hello
#change
#another change
import pygame, sys
from pygame.locals import *

screenWidth = 1280
screenHeight = 720
timer = None
window = None
fps = 30

wood = ("#deb887")
white = ("#ffffff")
black = ("#000000")

def InitPygame(screenWidth, screenHeight):
    global window
    global timer
    
    pygame.init()
    timer = pygame.time.Clock()
    window = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption( "Chess" )

InitPygame(screenWidth, screenHeight)

finished = False
while finished == False:
    
    for event in pygame.event.get():
        if ( event.type == QUIT ):
            finished = True
        
    window.fill(wood)

    square_x = []
    color = white
    for x in range(8):
        #square_y = []
        for y in range(8):
            #square_y.append(y)
            if (((x + y) % 2) == 0):
                color = white
            else:
                color = black    
            #square_x.append(square_y)
            pygame.draw.rect(window, color, pygame.Rect((x * 80) + 50, (y * 80) + 50, 80, 80))
    pygame.display.update()
    timer.tick(fps)



