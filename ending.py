import pygame
import sys
import random
import time
import subprocess

pygame.init()

#이미지, 글꼴 불러오기,,,,,,,
img = pygame.image.load('img/race.png')
rabbit = pygame.image.load('img/rabbit.png')
cat = pygame.image.load('img/cat.png')
tiger = pygame.image.load('img/tiger.png')
turtle = pygame.image.load('img/run_turtle.png')

W, H = img.get_size()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Race Track")
clock = pygame.time.Clock()

font_big = pygame.font.Font("PF.ttf", 100)
font_mid = pygame.font.Font("PF.ttf", 48)
font_small = pygame.font.Font("PF.ttf", 30)

# 텍스트 출력 함수
def draw_text(txt, font, x, y, color):
    screen.blit(font.render(txt, True, color), (x, y))

#변수들...
game = "count"     #count -> race1 -> pause -> cheer -> race2 -> finish
count = 3
last_tick = pygame.time.get_ticks()

#위치
start_x = 130
rabbit_x = turtle_x = tiger_x = cat_x = start_x

lane = H // 4
rabbit_y = lane + 35
turtle_y = lane + 140
tiger_y = lane + 220
cat_y = lane + 320

#속도
tiger_s = 3
cat_s = 2.5
rabbit_s = 2
turtle_s = 0.7
turtle_fast = 8
turtle_slow = 0.3

finish = W - 150

#응원
cheer_cnt = 0
cheer_goal = 15
cheer_limit = 10
cheer_start = 0
btn_x = btn_y = 0
btn_size = 100

#메시지 출력 시간
success_time = 0
fail_time = 0
pause_start = 0


running = True
while running:

    now = pygame.time.get_ticks()
    screen.blit(img, (0, 0))

    # ------- 이벤트 ---------
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

        # 클릭 처리
        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = e.pos

            # 응원 상태에서 버튼 클릭
            if game == "cheer":
                dist = ((mx - btn_x)**2 + (my - btn_y)**2)**0.5
                if dist < btn_size/2:
                    cheer_cnt += 1
                    btn_x = random.randint(100, W - 200)
                    btn_y = random.randint(100, H - 200)

            # 다시하기
            if game == "finish":
                bx = W//2 - 150
                by = H//2 + 20
                if bx < mx < bx+300 and by < my < by+80:
                    pygame.quit()
                    subprocess.run([sys.executable, "training.py"])
                    sys.exit()

    #캐릭터들 그리기
    screen.blit(pygame.transform.scale(rabbit, (85, 85)), (rabbit_x, rabbit_y))
    screen.blit(pygame.transform.scale(turtle, (85, 85)), (turtle_x, turtle_y))
    screen.blit(pygame.transform.scale(tiger, (100, 100)), (tiger_x - 10, tiger_y))
    screen.blit(pygame.transform.scale(cat, (95, 75)), (cat_x, cat_y))


    #레이스시작전카운트다운
    if game == "count":
        if now - last_tick >= 1000:
            count -= 1
            last_tick = now
            if count == 0:
                game = "race1"

        if count > 0:
            draw_text(str(count), font_big, W//2-50, H//2-80, (255, 0, 0))


    #우선뛰기
    elif game == "race1":
        tiger_x += tiger_s
        cat_x += cat_s
        rabbit_x += rabbit_s
        turtle_x += turtle_s

        if tiger_x >= W//3:
            game = "pause"
            pause_start = time.time()


    #응원하는방법알려주기
    elif game == "pause":
        if time.time() - pause_start >= 3:
            game = "cheer"
            cheer_start = time.time()
            cheer_cnt = 0
            btn_x = random.randint(100, W - 200) #랜덤임
            btn_y = random.randint(100, H - 200) #랜덤임

        draw_text("거북이를 응원할 준비!", font_mid, W//2-250, H//2-60, (255, 255, 255))
        draw_text("버튼을 클릭해서 응원하세요!", font_small, W//2-220, H//2, (255, 255, 0))


    # 응원하기
    elif game == "cheer":
        remain = cheer_limit - (time.time() - cheer_start)

        if cheer_cnt >= cheer_goal:
            success_time = time.time()
            game = "race2"
        elif remain <= 0:
            fail_time = time.time()
            game = "race2"
        else:
            pygame.draw.circle(screen, (255, 255, 0), (btn_x, btn_y), btn_size//2)
            draw_text("화이팅!", font_mid, btn_x-60, btn_y-30, (0, 0, 0))

            draw_text(f"응원 {cheer_cnt}/{cheer_goal}", font_small, 20, 20, (255, 255, 255))
            draw_text(f"시간 {int(remain)}초", font_small, 20, 60, (255, 255, 255))


    #결과알려주기
    elif game == "race2":
        tiger_x += tiger_s
        cat_x += cat_s
        rabbit_x += rabbit_s

        if cheer_cnt >= cheer_goal:
            turtle_x += turtle_fast
        else:
            turtle_x += turtle_slow

        #15개 했을 때
        if success_time and time.time() - success_time < 2:
            draw_text("우리 거북이 화이팅!", font_mid, W//2-200, H//2-50, (50, 255, 50))
        #15개 못했을 시
        if fail_time and time.time() - fail_time < 2:
            draw_text("응원이 부족합니다!", font_mid, W//2-200, H//2-50, (255, 50, 50))

        # 도착
        if tiger_x >= finish or turtle_x >= finish:
            game = "finish"


    #진짜결과
    elif game == "finish":

        if turtle_x >= finish and cheer_cnt >= cheer_goal:
            draw_text("거북이 우승!", font_big, W//2-250, H//2-120, (0, 255, 0))
        else:
            draw_text("호랑이 우승!", font_big, W//2-250, H//2-120, (255, 180, 0))

        #다시하기 버튼
        bx = W//2 - 150
        by = H//2 + 20
        pygame.draw.rect(screen, (100, 200, 100), (bx, by, 300, 80), border_radius=15)
        draw_text("다시 하기", font_mid, bx+70, by+15, (255, 255, 255))


    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
