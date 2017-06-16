import pygame
import os
import sys
import random
import time

pygame.init()

#CONSTANTS

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 722
FPSCLOCK = 50
GRAVITY = 7
PIPES_WIDTH = 100
PIPES_HEIGHT = 500
GAP_IN_PIPES = 150
BIRD_X = 50
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BLACK = (0, 0, 0)
SCORE_COLOR = (0, 0, 255)


def exit_properly(background_music):
    background_music.stop()
    pygame.quit()
    sys.exit()


def load_sound(file_name):
    full_path = os.path.join("requirements", file_name)

    try:
        sound = pygame.mixer.Sound(full_path)
    except pygame.error, message:
        raise SystemExit, message

    return sound


def load_image(file_name):
    full_path = os.path.join("requirements", file_name)

    try:
        image_surface = pygame.image.load(full_path)
    except pygame.error, message:
        raise SystemExit, message

    return image_surface


def display_game_over(game_over_font_object, screen, background_music):
    game_over_font_object_surface = game_over_font_object.render("GAME  OVER!!", True, SCORE_COLOR)
    game_over_font_object_surface_rect = game_over_font_object_surface.get_rect()
    game_over_font_object_surface_rect.center = (SCREEN_WIDTH/2 + 22, SCREEN_HEIGHT/2 + 60)
    screen.blit(game_over_font_object_surface, game_over_font_object_surface_rect)
    pygame.display.update()
    background_music.stop()
    time.sleep(2)
    main()


def display_score(score_font_object, screen, bird):
    score_font_object_surface = score_font_object.render(str(bird.score), True, SCORE_COLOR)
    score_font_object_surface_rect = score_font_object_surface.get_rect()
    score_font_object_surface_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    screen.blit(score_font_object_surface, score_font_object_surface_rect)


class Bird:
    def __init__(self):
        self.flying_image_surface = load_image("bird_flying.png")
        self.falling_image_surface = load_image("bird_falling.png")
        self.y = 50
        self.rect = pygame.Rect(BIRD_X, 50, BIRD_WIDTH, BIRD_HEIGHT)
        self.flying = False
        self.dead = False
        self.score = 0
        self.current_image_surface = self.falling_image_surface

    def update_bird(self):
        self.flying = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.flying = True

        if self.flying:
            self.current_image_surface = self.flying_image_surface
            self.y -= 5
        else:
            self.current_image_surface = self.falling_image_surface
            self.y += GRAVITY

        self.rect = pygame.Rect(BIRD_X, self.y, BIRD_WIDTH, BIRD_HEIGHT)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()
    pygame.display.set_caption("fLaPpY bIrD")
    pygame.mouse.set_visible(False)

    background_music = load_sound("background_flappy.ogg")
    background_music.play(-1)

    background_image_surface = load_image("flappy_background.jpg")
    upper_pipe_image_surface = load_image("upper_pipe.jpg")
    lower_pipe_image_surface = load_image("lower_pipe.jpg")

    upper_pipe_image_surface_rect = upper_pipe_image_surface.get_rect()
    lower_pipe_image_surface_rect = lower_pipe_image_surface.get_rect()

    bird = Bird()

    random_value = random.randint(-200, 200)
    upper_pipe_image_surface_rect.x, upper_pipe_image_surface_rect.y = 450, 361 + random_value - GAP_IN_PIPES/2 - 500
    lower_pipe_image_surface_rect.x, lower_pipe_image_surface_rect.y = 450, 361 + random_value + GAP_IN_PIPES/2

    score_font_object = pygame.font.Font("freesansbold.ttf", 40)
    game_over_font_object = pygame.font.Font("freesansbold.ttf", 50)

    change_pipes = False

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPSCLOCK)

        bird.update_bird()

        if bird.rect.colliderect(upper_pipe_image_surface_rect) or bird.rect.colliderect(lower_pipe_image_surface_rect):
            bird.dead = True
        if bird.y < 0 or bird.y > SCREEN_HEIGHT - BIRD_HEIGHT:
            bird.dead = True

        if bird.dead:
            display_game_over(game_over_font_object, screen, background_music)

        screen.blit(background_image_surface, (screen_rect.x, screen_rect.y))
        screen.blit(upper_pipe_image_surface, upper_pipe_image_surface_rect)
        screen.blit(lower_pipe_image_surface, lower_pipe_image_surface_rect)
        screen.blit(bird.current_image_surface, (BIRD_X, bird.y))
        display_score(score_font_object, screen, bird)

        upper_pipe_image_surface_rect.x -= 2
        lower_pipe_image_surface_rect.x -= 2

        if upper_pipe_image_surface_rect.x < -100:
            upper_pipe_image_surface_rect.x = 400
            lower_pipe_image_surface_rect.x = 400
            bird.score += 1
            change_pipes = True

        if change_pipes:
            random_value = random.randint(-200, 200)
            upper_pipe_image_surface_rect.x, upper_pipe_image_surface_rect.y = 450, 361 + random_value - GAP_IN_PIPES/2 - 500
            lower_pipe_image_surface_rect.x, lower_pipe_image_surface_rect.y = 450, 361 + random_value + GAP_IN_PIPES/2
            change_pipes = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_properly(background_music)

        pygame.display.update()

if __name__ == "__main__":
    main()
