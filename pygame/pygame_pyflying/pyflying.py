import sys
import pygame #pygame 라이브러리 import
import os
from pygame.locals import *
import random
from time import sleep

pygame.init()

#게임의 폭, 높이 등 전체 크기 및 사용할 png 이미지 크기
WHITE = (255,255,255)
RED = (255,0,0)
pad_width = 480
pad_height = 320
background_width= 480

aircraft_width = 55
aircraft_height = 31

Shotship_width = 63
Shotship_height = 25

sonic1_width = 55
sonic1_height = 41
sonic2_width = 48
sonic2_height = 36

#_______________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%___________________________
#text 화면 출력
def textObj(text,font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

#text 화면 중앙에 출력
def dispMessage(text):
    global gamepad

    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf,TextRect)
    pygame.display.update()
    sleep(2)
    runGame()
# 적에게 공격당했을 때 호출
def crash():
    global gamepad
    dispMessage('Crashed!')

def drawObject(obj, x, y): 
    global gamepad
    gamepad.blit(obj,(x,y))

#_______________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%___________________________
# 게임 실행
def runGame():
    global gamepad, aircraft, clock, background1, background2
    global Shotship, sonics, bullet, boom

    isShotship = False
    boom_count = 0

    bullet_xy = []
    #우주선 최초 위치 좌표 설정
    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0 #비행기 좌표 변화를 나타낼 

    background1_x = 0
    background2_x = background_width
    
    Shotship_x = pad_width
    Shotship_y = random.randrange(0, pad_height)

    sonic_x = pad_width
    sonic_y = random.randrange(0, pad_height)
    random.shuffle(sonics)
    sonic = sonics[0]

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            #키를 눌렀을 때 우주선이 위아래로 5픽셀씩 이동
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                #ctrl를 누르면 총알 발사
                elif event.key == pygame.K_LCTRL:
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height/2
                    bullet_xy.append([bullet_x, bullet_y])
                    
                #esc->quit
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    return

    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                    
        #Clear gamepad
        gamepad.fill(WHITE)

        #Draw Background
        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width 

        drawObject(background1,background1_x,0)
        drawObject(background2,background2_x,0)



        #Aircraft Position
        y += y_change
        if y < 0:
            y = 0
        elif y > pad_height - aircraft_height:
            y = pad_height - aircraft_height


        #Shotship Position
        # 적 우주선이 7픽셀씩 날아오도록 지정
        Shotship_x -= 7
        if Shotship_x <= 0:
            Shotship_x = pad_width
            Shotship_y = random.randrange(0,pad_height)

        #Sonic Position
        if sonic == None:
            sonic_x -= 30
        else:
            sonic_x -= 15

        if sonic_x <= 0:
            sonic_x = pad_width
            sonic_y = random.randrange(0,pad_height)
            random.shuffle(sonics)
            sonic = sonics[0]

        
        #Bullets Position
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]

                #Check if bullet strite Shotship
                if bxy[0] > Shotship_x:
                    if bxy[1] > Shotship_y and bxy[1] < Shotship_y + Shotship_height:
                        bullet_xy.remove(bxy)
                        isShotship = True
                if bxy[0] >= pad_width:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass
        #crash check
        if x + aircraft_width > Shotship_x:
            if ( y > Shotship_y and y < Shotship_y + Shotship_height) or \
            (y + aircraft_height > Shotship_y and y + aircraft_height < Shotship_y + Shotship_height):
                crash()
        sonic_width = 0
        sonic_height = 0
        if sonics[0] != None:
            if sonics[0] == sonic1:
                sonic_width = sonic1_width
                sonic_height = sonic1_height
            elif sonics[0] == sonic2:
                sonic_width = sonic2_width
                sonic_height = sonic2_height


        if x + aircraft_width > sonic_x:
            if(y > sonic_y and y < sonic_y + sonic_height) or \
            (y + aircraft_height > sonic_y and y + aircraft_height < sonic_y + sonic_height):
                crash()

        drawObject(aircraft,x,y)


        if len(bullet_xy) != 0:
            for bx,by in bullet_xy:
                drawObject(bullet,bx,by)

        if not isShotship:  
            drawObject(Shotship,Shotship_x,Shotship_y)
        #총알이 적을 명중하지 않았을 때 적 우주선 새로 화면에 갱신
        #명중시 폭발 + 새로운 적 우주선 
        else:
            drawObject(boom, Shotship_x, Shotship_y)
            boom_count += 1
            if boom_count > 5:
                boom_count = 0
                Shotship_x = pad_width
                Shotship_y = random.randrange(0, pad_height - Shotship_height)
                isShotship = False

        if sonic != None:
            drawObject(sonic,sonic_x,sonic_y)
        

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()
#_______________%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%___________________________
# 게임 초기화하고 시작
def initGame():
    global gamepad, aircraft, clock, background1, background2
    global Shotship, sonics, bullet, boom, sonic1, sonic2

    sonics = []

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height), FULLSCREEN)
    pygame.display.set_caption('Shooting game') #game title

    aircraft = pygame.image.load('/home/pi/BMO_project/pygame/image/spaceship.png')
    background1 = pygame.image.load("/home/pi/BMO_project/pygame/image/fly_background.png")
    background2 = background1.copy() #배경이 움직이도록 이미지 복사본을 원본 다음으로 좌표 지정

    Shotship = pygame.image.load("/home/pi/BMO_project/pygame/image/Shotship.png")
    
    sonic1 = pygame.image.load("/home/pi/BMO_project/pygame/image/sonic1.png")
    sonic2 = pygame.image.load("/home/pi/BMO_project/pygame/image/sonic2.png")
    sonics.append(sonic1)
    sonics.append(sonic2)
    
    boom = pygame.image.load("/home/pi/BMO_project/pygame/image/boom.png")

    for i in range(3):
        sonics.append(None)

    bullet = pygame.image.load("/home/pi/BMO_project/pygame/image/bullet.png")

    clock = pygame.time.Clock() #게임 초당 프레임 설정을 위한 Clock
    runGame()
    
    
if __name__=='__main__':
    initGame()

