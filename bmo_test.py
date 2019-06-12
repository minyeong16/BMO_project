import unittest
import pygame
from pygame.locals import *
import math
import random
import sys

# pygame 실행을 위해 초기화
pygame.init()
# 오디오 실행을 위해 초기화
pygame.mixer.init()

# display 크기 설정
displayWidth = 480
displayHeight = 320
screen = pygame.display.set_mode((displayWidth, displayHeight))

# 조종 시간 설정
time = 90
timeSet = pygame.time.Clock()

# 입력 key 값 설정
keys = [False, False, False, False]

# player(jake) 위치
player_location = [100, 100]

# 변수 선언
attack = [0, 0]
arrows = []
villain_time01 = 100
villain_time02 = 0
villain = [[400, 100]]
life_value = 194

# 게임실행에 필요한 이미지 첨부
player_img = pygame.image.load("./images/jake.png")
background_img = pygame.image.load("./images/background.png")
bmo_img = pygame.image.load("./images/bmo.png")
arrow_img = pygame.image.load("./images/arrow.png")
villain01_img = pygame.image.load("./images/crocodile.png")
villain02_img = villain01_img
lifeBar_img = pygame.image.load("./images/lifebar.png")
life_img = pygame.image.load("./images/life.png")
gameOver_img = pygame.image.load("./images/game_over.png")
win_img = pygame.image.load("./images/win.png")

# 게임실행에 필요한 오디오 첨부 및 설정
hit = pygame.mixer.Sound("./audio/explode.wav")
enemy = pygame.mixer.Sound("./audio/enemy.wav")
shoot = pygame.mixer.Sound("./audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.set_volume(0.25)

finish_check = 1
exitcode = 0

def test_game():
    finish_check = 1
    villain_time01 = 100
    villain_time02 = 0
    life_value = 194
    # 게임 실행
    while finish_check:
        villain_time01 -= 1
        # 화면 초기화
        screen.fill(0)

        for x in range(displayWidth // background_img.get_width() + 1):
            for y in range(displayHeight // background_img.get_height() + 1):
                # 배경화면 설정
                screen.blit(background_img, (x * 80, y * 80))

        # bmo를 지켜라의 bmo 자리 설정
        screen.blit(bmo_img, (0, 30))
        screen.blit(bmo_img, (0, 120))
        screen.blit(bmo_img, (0, 210))

        # player 이미지를 마우스로 회전할 수 있도록 설정
        position = pygame.mouse.get_pos()
        # mouse 위치 값
        angle = math.atan2(position[1] - (player_location[1] + 32), position[0] - (player_location[0] + 26))
        # 각도 설정
        player_rotate = pygame.transform.rotate(player_img, 360 - angle * 57.29)
        player_location01 = (
        player_location[0] - player_rotate.get_rect().width / 2, player_location[1] - player_rotate.get_rect().height / 2)
        # 이미지에 대한 회전 설정
        screen.blit(player_rotate, player_location01)
        # 이미지에 대한 회전 값 적용

        # 공격하는 화살 값 설정 및 출력
        for bullet in arrows:
            index = 0
            # 삼각함수 원리 이용 - 화살 속도 : 10
            arrow_x = math.cos(bullet[0]) * 10
            arrow_y = math.sin(bullet[0]) * 10
            bullet[1] += arrow_x
            bullet[2] += arrow_y
            # 화면 크기에 따른 화살 값 설정 - 화면 벗어날 경우 삭제
            if bullet[1] < -40 or bullet[1] > 480 or bullet[2] < -40 or bullet[2] > 320:
                arrows.pop(index)
            index += 1
            # 화살 회전 설정
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow_img, 360 - projectile[0] * 57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))

        # 공경하는 악어 설정 및 출력
        if villain_time01 == 0:
            # 화면의 크기에 맞게 랜덤으로 악어 나타나게 설정
            villain.append([480, random.randint(50, 250)])
            villain_time01 = 100 - (villain_time02 * 2)
            if villain_time02 >= 35:
                villain_time02 = 35
            else:
                villain_time02 += 5
        index = 0
        for badguy in villain:
            if badguy[0] < -40:
                villain.pop(index)
            badguy[0] -= 7

            # 악어가 bmo를 공격할 때 설정
            badrect = pygame.Rect(villain02_img.get_rect())
            badrect.top = badguy[1]
            badrect.left = badguy[0]
            if badrect.left < 40:
                hit.play()
                # 공격할 때 음악소리
                life_value -= random.randint(5, 20)
                # 공격당하면 생명 값 5~20 사이의 랜덤으로 감소
                villain.pop(index)
            # 악어가 화살에 공격당했을 때 설정
            index1 = 0
            for bullet in arrows:
                # 화살 이미지 값
                bullrect = pygame.Rect(arrow_img.get_rect())
                bullrect.left = bullet[1]
                bullrect.top = bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    # 악어가 공격당했을 때 음악소리
                    attack[0] += 1
                    villain.pop(index)
                    arrows.pop(index1)
                index1 += 1
            index += 1
        # villain01_img villain02_img 반복적으로 출력
        for badguy in villain:
            screen.blit(villain02_img, badguy)

        # 오른쪽 상단의 시간 표시
        font = pygame.font.Font(None, 15)

        # 약 30초정도의 시간 출력
        survivedtext = font.render(str((90000 - pygame.time.get_ticks()) / 1000 % 60).zfill(2), True, (0, 0, 0))
        textRect = survivedtext.get_rect()
        textRect.topright = [430, 10]
        screen.blit(survivedtext, textRect)

        # 생명 이미지 출력
        screen.blit(lifeBar_img, (5, 5))
        for life01 in range(life_value):
            screen.blit(life_img, (life01 + 8, 8))

        pygame.display.flip()
        timeSet.tick(time)

        # 게임에세 반응이 일어났을 때 설정
        for event in pygame.event.get():
            # 닫기 버튼을 누르면 게임 종료 설정
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            # 게임을 동작할 키보드 값 설정
            # keys 배열을 이용하여 어떤 키를 눌렀는 지 check
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    keys[0] = True
                elif event.key == K_LEFT:
                    keys[1] = True
                elif event.key == K_DOWN:
                    keys[2] = True
                elif event.key == K_RIGHT:
                    keys[3] = True

                # esc->quit
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # keys 배열을 이용하여 어떤 키를 안누르는 지 check
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    keys[0] = False
                elif event.key == pygame.K_LEFT:
                    keys[1] = False
                elif event.key == pygame.K_DOWN:
                    keys[2] = False
                elif event.key == pygame.K_RIGHT:
                    keys[3] = False

            # 마우스를 눌렀을 때 화살 설정
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot.play()
                # 화살을 쏘았을 때 음악 소리
                position = pygame.mouse.get_pos()
                # 마우스의 위치 값
                attack[1] += 1
                # 화살을 쏘았을 때
                arrows.append(
                    [math.atan2(position[1] - (player_location01[1] + 32), position[0] - (player_location01[0] + 26)),
                     player_location01[0] + 32, player_location01[1] + 32])

        # keys 배열을 통해 어떠한 키를 눌렀을 때 player의 위치 변화
        if keys[0]:
            player_location[1] -= 5
        elif keys[2]:
            player_location[1] += 5
        if keys[1]:
            player_location[0] -= 5
        elif keys[3]:
            player_location[0] += 5

        # 시간내에 생명 값이 남았으면 이긴 것, 아니면 game over 설정
        if pygame.time.get_ticks() >= 90000:
            finish_check = 0
            exitcode = 1
        if life_value <= 0:
            finish_check = 0
            exitcode = 0
        if attack[1] != 0:
            # 화살의 정확도 계산
            accuracy = attack[0] * 1.0 / attack[1] * 100
        else:
            accuracy = 0

    # 이겼는지 졌는지 상태에 따라 이미지 출력
    if exitcode == 0:
        pygame.font.init()
        font = pygame.font.Font(None, 20)
        # 화살의 정확도 출력
        text = font.render("Accuracy: " + str(accuracy) + "%", True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(gameOver_img, (0, 0))
        screen.blit(text, textRect)
    else:
        pygame.font.init()
        font = pygame.font.Font(None, 20)
        text = font.render("Accuracy: " + str(accuracy) + "%", True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery + 24
        screen.blit(win_img, (0, 0))
        screen.blit(text, textRect)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()

class TestAdd(unittest.TestCase):
    def test_game(self):
        self.assertEqual(test_game())

if __name__ == '__main__':
    unittest.main()