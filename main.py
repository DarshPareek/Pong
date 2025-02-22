import pygame
import tomllib
import time

fp = open("settings.toml", "rb")
settings = tomllib.load(fp)
SCREEN_WIDTH = settings["SCREEN_WIDTH"]
SCREEN_HEIGHT = settings["SCREEN_HEIGHT"]
BG_COLOR = settings["BG_COLOR"]
PAD_COLOR = settings["PAD_COLOR"]
BALL_COLOR = settings["BALL_COLOR"]
SCORE_COLOR = settings["SCORE_COLOR"]
PAD_HEIGHT = settings["PAD_HEIGHT"]
PAD_WIDTH = settings["PAD_WIDTH"]
BALL_RADIUS = settings["BALL_RADIUS"]
# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

delta_time = 0
# Paddles
p1 = [PAD_HEIGHT, PAD_WIDTH, PAD_COLOR, 0, 0]
p2 = [PAD_HEIGHT, PAD_WIDTH, PAD_COLOR, SCREEN_WIDTH - PAD_WIDTH, 0]
p1_r = pygame.Rect(p1[3], p1[4], p1[1], p1[0])
p2_r = pygame.Rect(p2[3], p2[4], p2[1], p2[0])
p_move = 0
score = 0
pygame.font.init()
my_font = pygame.font.SysFont("sans", 30)
# ball
b = [BALL_RADIUS, BALL_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
b_r = pygame.Rect(b[2], b[3], b[0] * 2, b[0] * 2)
b_acc_x = -0.3
b_acc_y = 0.2
hit_sound = pygame.mixer.Sound("Yeeeee.wav")
end_sound = pygame.mixer.Sound("Brrrr.wav")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    if b[2] > SCREEN_WIDTH or b[2] < 0:
        pygame.mixer.Sound.play(end_sound)
        pygame.mixer.music.stop()
        time.sleep(2)
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p_move = -0.5

            if event.key == pygame.K_s:
                p_move = 0.5
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_COLOR)
    if p_move > 0:
        if p1_r.top < SCREEN_HEIGHT - PAD_HEIGHT:
            p1_r.top += p_move * delta_time
            p2_r.top += p_move * delta_time
    elif p_move < 0:
        if p1_r.top > 0:
            p1_r.top += p_move * delta_time
            p2_r.top += p_move * delta_time
    if b[3] < BALL_RADIUS:
        b_acc_y = abs(b_acc_y)
    elif b[3] > SCREEN_HEIGHT - BALL_RADIUS:
        b_acc_y = -1 * abs(b_acc_y)
    if (
        b[3] > p1_r.top
        and b[3] < p1_r.top + PAD_HEIGHT
        and (b[2] - BALL_RADIUS) < PAD_WIDTH
    ):
        b_acc_x = abs(b_acc_x) + 0.1
        score += 1
        pygame.mixer.Sound.play(hit_sound)
        pygame.mixer.music.stop()
    if (
        b[3] > p2_r.top
        and b[3] < p2_r.top + PAD_HEIGHT
        and (b[2] + BALL_RADIUS) > SCREEN_WIDTH - PAD_WIDTH
    ):
        b_acc_x = abs(b_acc_x) * -1 - 0.1
        score += 1
        pygame.mixer.Sound.play(hit_sound)
        pygame.mixer.music.stop()

    b[2] += b_acc_x * delta_time
    b[3] += b_acc_y * delta_time
    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, p1[2], p1_r)
    pygame.draw.rect(screen, p1[2], p2_r)
    pygame.draw.circle(screen, BALL_COLOR, (b[2], b[3]), b[0])
    # flip() the display to put your work on screen
    text_surface = my_font.render(str(score), True, SCORE_COLOR)
    text_r = text_surface.get_rect()
    text_r.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(text_surface, text_r)
    pygame.display.flip()

    delta_time = clock.tick(60)  # limits FPS to 60


pygame.quit()
