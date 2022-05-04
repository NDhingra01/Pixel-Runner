import pygame
import os
from sys import exit
from random import randint, choice

# Colors
BLACK = (64, 64, 64)
BACKGROUND = '#c0e8ec'
BLUE = (94, 129, 162)
GROUND = 300
GREEN = (111, 196, 169)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_1.png')).convert_alpha()
        player_walk_2 = pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_2.png')).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(os.path.join('graphics', 'Player', 'jump.png')).convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, GROUND))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 or keys[pygame.K_UP] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load(os.path.join('graphics', 'Fly', 'Fly1.png')).convert_alpha()
            fly_2 = pygame.image.load(os.path.join('graphics', 'Fly', 'Fly2.png')).convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210

        else:
            snail_1 = pygame.image.load(os.path.join('graphics', 'snail', 'snail1.png')).convert_alpha()
            snail_2 = pygame.image.load(os.path.join('graphics', 'snail', 'snail2.png')).convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks()/100) - start_time
    score_surf = font.render(f'Score: {current_time}', False, BLACK)
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obs_group, False):
        obs_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font = pygame.font.Font(os.path.join('font', 'Pixeltype.ttf'), 50)
game_active = False
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obs_group = pygame.sprite.Group()


# Sky and Ground
sky_surf = pygame.image.load(os.path.join('graphics', 'Sky.png')).convert()
ground_surf = pygame.image.load(
    os.path.join('graphics', 'Ground.png')).convert()

# Intro screen
player_stand = pygame.image.load(os.path.join(
    'graphics', 'Player', 'player_stand.png')).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = font.render('Pixel Runner', False, GREEN)
game_name_rect = game_name.get_rect(center=(400, 80))

game_msg = font.render('Press Space or UP arrow to start', False, GREEN)
game_msg_rect = game_msg.get_rect(center=(400, 340))


# Timer
obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer, 1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obs_timer:
                obs_group.add(
                    Obstacles(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND))
        score = display_score()

        player.draw(screen)
        player.update()

        obs_group.draw(screen)
        obs_group.update()

        game_active = collision_sprite()

    else:
        screen.fill(BLUE)
        screen.blit(player_stand, player_stand_rect)

        score_msg = font.render(f'Your Score: {score}', False, GREEN)
        score_msg_rect = score_msg.get_rect(center=(400, 340))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_msg, game_msg_rect)
        else:
            screen.blit(score_msg, score_msg_rect)

    pygame.display.update()
    clock.tick(60)
