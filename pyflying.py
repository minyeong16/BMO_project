import sys
import pygame
import os
from pygame.locals import *
import random
from time import sleep

pygame.init()

WHITE = (255,255,255)
pad_width = 1024
pad_height = 512
background_width= 1024


def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj,(x,y))
    

def runGame():
    global gamepad, aircraft, clock, background1, background2
    global Shotship1,Shotship2

    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0
    background2_x = background_width
    
    Shotship1_x = pad_width
    Shotship1_y = random.randrange(0, pad_height)

    Shotship2_x = pad_width
    Shotship2_y = random.randrange(0, pad_height)
    #random.shuffle(Shotship2)
    Shotship2 = Shotships[0]

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                    
        y += y_change
        gamepad.fill(WHITE)

        background1_x -= 2
        background2_x -= 2
        
        Shotship1_x-= 7
        if Shotship1_x <= 0:
                Shotship1_x = pad_width
                Shotship1_y = random.randrange(0, pad_height)
                
        if Shotship2 == None:
            Shotship2_x -= 30
        else:
            Shotship2_x -= 15
            
        if Shotship2_x <= 0:
            Shotship2_x = pad_width
            Shotship2_y = random.randrange(0, pad_height)
            random.shuffle(Shotships)
            Shotship2 = Shotships[0]

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width 

        drawObject(background1,background1_x,0)
        drawObject(background2,background2_x,0)
        drawObject(Shotship1,Shotship1_x,Shotship1_y)

        if Shotship2 != None:
            drawObject(Shotship2,Shotship2_x,Shotship2_y)
        drawObject(aircraft,x,y)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

def initGame():
    global gamepad, aircraft, clock, background1, background2
    global Shotship1,Shotships
    
    Shotships = []
    
    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('pyflying')
    aircraft = pygame.image.load('/home/pi/pygame/image/spaceship.png')
    background1 = pygame.image.load("/home/pi/pygame/pygame_pyflying/image/fly_background.png")
    background2 = background1.copy()
    Shotship1 = pygame.image.load("/home/pi/pygame/image/Shotship.png")
    Shotships.append(pygame.image.load("/home/pi/pygame/image/Y_Shotship.png"))
    Shotships.append(pygame.image.load("/home/pi/pygame/image/Y_Shotship.png"))
    
    #for i in range(5):
    #    Shotship2.append(None)

    clock = pygame.time.Clock()
    runGame()
    
    
if __name__=='__main__':
    initGame()

