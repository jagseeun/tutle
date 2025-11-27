import pygame, sys, time, subprocess

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("거북이의 역전 대작전")
clock = pygame.time.Clock()

# 색상
PALE_GREEN = (230, 245, 230)
DARK_TEXT = (40, 40, 40)
BUTTON_BG = (200, 220, 200)
DISABLED_BTN = (180, 180, 180)
ACCENT_GREEN = (0, 190, 80)

font_medium = pygame.font.Font("PF.ttf", 48)
font_small = pygame.font.Font("PF.ttf", 30)

# 상태
GAME_STATE = "MENU"
speed = 0.0
goal = 100.0
last_key = None
last_situp_time = 0

# 이미지 로드
def load_img(name):
    try:
        return pygame.transform.scale(pygame.image.load(name).convert_alpha(), (300, 300))
    except:
        return None

turtle = load_img("img/turtle.png")
run1 = load_img("img/running1.png")
run2 = load_img("img/running2.png")
situp1 = load_img("img/situp1.png")
situp2 = load_img("img/situp2.png")


def text(surf, msg, font, color, x, y):
    t = font.render(msg, True, color)
    r = t.get_rect(center=(x, y))
    surf.blit(t, r)

def go_to_ending():
    pygame.quit()
    try:
        subprocess.run(["python", "ending.py"])
    except Exception as ex:
        print("ending.py 실행 실패!", ex)
    sys.exit()


#메뉴
def menu():
    global GAME_STATE

    btn_run = pygame.Rect(50, 250, 350, 60)
    btn_situp = pygame.Rect(50, 330, 350, 60)
    btn_mara = pygame.Rect(50, 410, 350, 60)  # ★ 마라톤 버튼

    while GAME_STATE == "MENU":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_run.collidepoint(e.pos):
                    GAME_STATE = "RUN"
                elif btn_situp.collidepoint(e.pos):
                    GAME_STATE = "SITUP"
                elif btn_mara.collidepoint(e.pos) and speed >= goal:
                    # speed 100일 때만 실행
                    go_to_ending()

        screen.fill(PALE_GREEN)
        text(screen, "거북이의 역전 대작전", font_medium, ACCENT_GREEN, 400, 120)
        text(screen, f"speed : {speed:.2f}", font_small, ACCENT_GREEN, 400, 200)

        # 런닝
        pygame.draw.rect(screen, BUTTON_BG, btn_run)
        text(screen, "런닝 하기", font_small, DARK_TEXT, btn_run.centerx, btn_run.centery)

        # 윗몸일으키기
        pygame.draw.rect(screen, BUTTON_BG, btn_situp)
        text(screen, "윗 몸 일으키기", font_small, DARK_TEXT, btn_situp.centerx, btn_situp.centery)

        # ★ 마라톤 버튼: speed < 100 → 비활성 색
        if speed >= goal:
            pygame.draw.rect(screen, ACCENT_GREEN, btn_mara)
            text(screen, "마라톤 대회 출전하기", font_small, (255,255,255), btn_mara.centerx, btn_mara.centery)
        else:
            pygame.draw.rect(screen, DISABLED_BTN, btn_mara)
            text(screen, "마라톤 (speed 100 필요)", font_small, (70,70,70), btn_mara.centerx, btn_mara.centery)

        if turtle:
            screen.blit(turtle, (450, 180))

        pygame.display.flip()
        clock.tick(30)

#런닝
def run_mode():
    global GAME_STATE, speed, last_key
    frame = run1

    while GAME_STATE == "RUN":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    GAME_STATE = "MENU"
                    last_key = None
                    return

                if e.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # 번갈아 누를 때만 증가
                    if last_key in (None, pygame.K_LEFT if e.key == pygame.K_RIGHT else pygame.K_RIGHT):
                        speed = min(goal, round(speed + 0.01, 2))
                        last_key = e.key
                        frame = run1 if e.key == pygame.K_RIGHT else run2

        screen.fill(PALE_GREEN)
        text(screen, "런닝 머신 타기", font_medium, ACCENT_GREEN, 400, 100)
        text(screen, "←, → 키를 번갈아 눌러요", font_small, DARK_TEXT, 400, 160)
        text(screen, f"speed : {speed:.2f}", font_small, ACCENT_GREEN, 700, 100)

        if frame:
            screen.blit(frame, (250, 250))

        text(screen, "ESC: 메뉴로 돌아가기", font_small, DARK_TEXT, 150, 530)
        pygame.display.flip()
        clock.tick(30)

#윗몸 일으키기
def situp_mode():
    global GAME_STATE, speed, last_situp_time
    frame = situp1
    toggle = False

    while GAME_STATE == "SITUP":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    GAME_STATE = "MENU"
                    return

                if e.key == pygame.K_SPACE:
                    now = time.time()
                    if now - last_situp_time >= 3:
                        last_situp_time = now

                        speed = min(goal, round(speed + 0.1, 2))
                        toggle = not toggle
                        frame = situp2 if toggle else situp1

        screen.fill(PALE_GREEN)
        text(screen, "윗몸일으키기 모드", font_medium, ACCENT_GREEN, 400, 80)

        # 카운트다운
        elapsed = time.time() - last_situp_time
        if elapsed < 1: msg = "1초..."
        elif elapsed < 2: msg = "2초..."
        elif elapsed < 3: msg = "3초!"
        else: msg = "스페이스바 눌러요!"

        text(screen, msg, font_small, DARK_TEXT, 400, 150)
        text(screen, f"speed : {speed:.2f}", font_small, ACCENT_GREEN, 700, 80)

        if frame:
            screen.blit(frame, (250, 210))

        text(screen, "ESC: 메뉴로 돌아가기", font_small, DARK_TEXT, 400, 530)
        pygame.display.flip()
        clock.tick(30)


def main():
    while True:
        if GAME_STATE == "MENU":
            menu()
        elif GAME_STATE == "RUN":
            run_mode()
        elif GAME_STATE == "SITUP":
            situp_mode()

if __name__ == "__main__":
    main()
