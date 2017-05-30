import pygame
import sys
import os
import random
import time

pygame.init()


#DEFINING CONSTANTS

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 731
BALL_DIMENSIONS = [5, 5]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FPS = 50
PADDLE_WIDTH = 119
PADDLE_HEIGHT = 10
PADDLE_DIMENSIONS = (PADDLE_WIDTH, PADDLE_HEIGHT)
PADDLE_SPEED = 15
X_SPACING = 30
Y_SPACING = 20
BRICKS_HORIZONTAL = 9
BRICKS_VERTICAL = 5
BRICK_HEIGHT = 10
BRICK_WIDTH = (SCREEN_WIDTH - (BRICKS_HORIZONTAL + 1)*X_SPACING) / BRICKS_HORIZONTAL
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

#DEFINING GLOBAL VARIABLES


ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]


#DEFINING CLASSES

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(BALL_DIMENSIONS)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH / 2, (SCREEN_HEIGHT - PADDLE_HEIGHT / 2)]
        self.speed = ball_speed
        random_number = random.randint(1, 2)
        if random_number == 1:
            self.speed[0] *= -1

    def update_ball(self):
        self.rect.move_ip(self.speed)

        if self.rect.x > SCREEN_WIDTH or self.rect.x < 0:
            self.speed[0] *= -1
        if self.rect.y < 0:
            self.speed[1] *= -1
        if (self.rect.x < 0 and self.rect.y < 0) or (self.rect.x + self.rect.width > SCREEN_WIDTH and self.rect.y < 0):
            self.speed[0] *= -1
            self.speed[1] *= -1


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(PADDLE_DIMENSIONS)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH / 2, (SCREEN_HEIGHT - PADDLE_HEIGHT/2)]
        self.speed = PADDLE_SPEED
        self.score = 0

    def update_paddle(self, direction):
        if direction == "left":
            self.rect.move_ip(-self.speed, 0)
            if self.rect.x < 0:
                self.rect.x = 0

        if direction == "right":
            self.rect.move_ip(self.speed, 0)
            if self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
                self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH


# DEFINING GLOBAL FUNCTIONS

def load_sound(file_name):
    full_path = os.path.join("requirements", file_name)
    try:
        sound = pygame.mixer.Sound(full_path)
    except pygame.error as message:
        raise message

    return sound


def check_collision(ball, paddle, hit_sound):
    if pygame.sprite.collide_rect(ball, paddle):
        if ball.speed[0] > 0:
            if ball.rect.x + ball.rect.width/2 < paddle.rect.centerx:
                ball.speed[1] *= -0.8
            else:
                ball.speed[1] *= -1.5
        if ball.speed[0] < 0:
            if ball.rect.x - ball.rect.width/2 > paddle.rect.centerx:
                ball.speed[1] *= -0.8
            else:
                ball.speed[1] *= -1.5

    if ball.speed[0] > 10:
        ball.speed[0] = 10
    if ball.speed[1] > 10:
        ball.speed[1] = 10

        hit_sound.play()


def draw_again(bricks, screen):
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)


def update_score(paddle, background, screen):
    score_font_obj = pygame.font.Font("freesansbold.ttf", 32)
    score_font_surface = score_font_obj.render(str(paddle.score), True, RED)
    score_font_surface_rect = score_font_surface.get_rect()
    score_font_surface_rect.centerx, score_font_surface_rect.centery = SCREEN_WIDTH / 2, 0.8 * SCREEN_HEIGHT
    background.blit(score_font_surface, score_font_surface_rect)
    screen.blit(background, (0, 0))


def create_bricks(screen):
    bricks = []
    y = Y_SPACING
    for i in range(0, BRICKS_VERTICAL):
        x = X_SPACING
        for j in range(0, BRICKS_HORIZONTAL):
            temp = pygame.draw.rect(screen, RED, (x, y, BRICK_WIDTH, BRICK_HEIGHT))
            bricks.append(temp)
            x = x + BRICK_WIDTH + X_SPACING
        y = y + BRICK_HEIGHT + Y_SPACING

    return bricks


def remove_brick(bricks, ball, paddle):
    for brick in bricks:
        if ball.rect.colliderect(brick):
            bricks.remove(brick)
            ball.speed[1] *= -1
            paddle.score += 1


def won_or_lost(bricks, ball):
    if len(bricks) == 0:
        return "won"
    if ball.rect.y + ball.rect.height > SCREEN_HEIGHT:
        return "lost"


def exit_properly():
    pygame.quit()
    sys.exit()


def show_game_over(screen):
    screen.fill(BLACK)
    game_over_font_obj = pygame.font.Font("freesansbold.ttf", 72)
    game_over_font_obj_surface = game_over_font_obj.render("GAME OVER!!!", True, WHITE)
    game_over_font_obj_surface_rect = game_over_font_obj_surface.get_rect()
    game_over_font_obj_surface_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(game_over_font_obj_surface, game_over_font_obj_surface_rect)
    pygame.display.update()
    time.sleep(2)
    exit_properly()


def show_you_won(screen):
    screen.fill(BLACK)
    won_font_obj = pygame.font.Font("freesansbold.ttf", 72)
    won_font_obj_surface = won_font_obj.render("CONGRATULATIONS !!! YOU WON", True, WHITE)
    won_font_obj_surface_rect = won_font_obj_surface.get_rect()
    won_font_obj_surface_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(won_font_obj_surface, won_font_obj_surface_rect)
    pygame.display.update()
    time.sleep(2)
    exit_properly()

#DEFINING MAIN FUNCTION


def main():
    gameloop = True
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BRICKS BREAKER")
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    background_music = load_sound("background_breakout.ogg")
    background_music.play(-1)

    hit_sound = load_sound("beep.wav")

    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    ball = Ball()
    paddle = Paddle()
    all_sprites = pygame.sprite.RenderPlain(ball, paddle)

    bricks = create_bricks(screen)

    while gameloop:
        background.fill(WHITE)
        update_score(paddle, background, screen)

        all_sprites.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_properly()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.update_paddle("left")
        if keys[pygame.K_RIGHT]:
            paddle.update_paddle("right")

        check_collision(ball, paddle, hit_sound)

        ball.update_ball()

        remove_brick(bricks, ball, paddle)
            
        game_state = won_or_lost(bricks, ball)
        if game_state == "lost":
	    background_music.stop()
            show_game_over(screen)
        if game_state == "won":
	    background_music.stop()
            show_you_won(screen)

        draw_again(bricks, screen)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

