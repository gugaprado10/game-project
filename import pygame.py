from logging import FileHandler
import pygame
import os
import random

FPS = 60
PLAYER_VELOCITY = 5
ZOMBIE_VELOCITY = 5
BULLET_VEL = 7
MAX_BULLETS = 7
RED = (255, 0, 0)

ZOMBIE_HIT = pygame.USEREVENT + 1

pygame.init()
SCREENWIDTH = 960
SCREENHEIGHT = 540
WIN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
right = False
left = False
walk_count = 0
shoot_count = 0
is_shooting = False

walk_right_frames = []
walk_left_frames = []
shooting_frames = []


for i in range(0, 6):
    if i < 5:
        shoot_sprite = pygame.image.load(f'assets/player/shoot{i}.png')

        shooting_frames.append(shoot_sprite)

    run_right = pygame.image.load(f'assets/player/run{i}.png')

    run_left = pygame.transform.flip(run_right, True, False)

    walk_right_frames.append(run_right)
    walk_left_frames.append(run_left)


player_sprite = pygame.image.load('assets/player/run5.png')
zombie_sprite = pygame.image.load('assets/zombie.png')
background = pygame.transform.scale(pygame.image.load(
    'assets/background.png'), (SCREENWIDTH, SCREENHEIGHT))


def draw_window(player, player_bullets, zombie, zombie_list):
    global walk_count
    global is_shooting
    global shoot_count

    WIN.blit(background, (0, 0))

    if walk_count + 1 >= len(walk_right_frames)*3:
        walk_count = 0

    if shoot_count + 1 >= len(shooting_frames)*3:
        shoot_count = 0
        is_shooting = False

    if is_shooting == True:
        WIN.blit(shooting_frames[shoot_count//3], (player.x, player.y))
        shoot_count += 1
    else:
        if left:
            WIN.blit(walk_left_frames[walk_count//3], (player.x, player.y))
            walk_count += 1
        elif right:
            WIN.blit(walk_right_frames[walk_count//3], (player.x, player.y))
            walk_count += 1
        else:
            WIN.blit(player_sprite, (player.x, player.y))

    for bullets in player_bullets:
        pygame.draw.rect(WIN, RED, bullets)
    for zombie in zombie_list:
        WIN.blit(zombie_sprite, (zombie.x, zombie.y))

    pygame.display.update()


def player_movement(keys_pressed, player):
    global left
    global right

    if keys_pressed[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width < SCREENWIDTH//3:
        right = True
        left = False
        player.x += PLAYER_VELOCITY
    if keys_pressed[pygame.K_LEFT] and player.x - PLAYER_VELOCITY > 10:
        right = False
        left = True
        player.x -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_UP] and player.y - PLAYER_VELOCITY > 270:
        player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN] and player.y + PLAYER_VELOCITY + player.height < SCREENHEIGHT:
        player.y += PLAYER_VELOCITY


def handle_bullets(player_bullets, player, zombie, zombie_list):
    for bullet in player_bullets:
        bullet.x += BULLET_VEL
        for zombie in zombie_list:
            score=0
            if zombie.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ZOMBIE_HIT))
                score+=10
                print(score)
                if len(player_bullets)>1:
                    player_bullets.remove(bullet)
                zombie_list.remove(zombie)
        if bullet.x > SCREENWIDTH:
            player_bullets.remove(bullet)


def main():
    global left, right, walk_count, is_shooting

    player = player_sprite.get_rect(topleft=(20, 270))

    player_bullets = []
    zombie_list = []
    player_health = 3

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullets) <= MAX_BULLETS:
                    is_shooting = True
                    bullet = pygame.Rect(
                        player.x + player.width, player.y + player.height//2 + 2, 10, 5)
                    player_bullets.append(bullet)

        while len(zombie_list)<3:
            zombie = zombie_sprite.get_rect(topleft=(900, random.randrange(
        270, 500)))
            zombie_list.append(zombie)
        
        for zombie in zombie_list:
            zombie.x -= ZOMBIE_VELOCITY

        for zombie in zombie_list:
            if zombie.x <= 20:
                zombie.x = 900
                zombie.y = random.randrange(270, 500)
                player_health -= 1

        if player_health == 0:
            run = False
        keys_pressed = pygame.key.get_pressed()

        player_movement(keys_pressed, player)
        handle_bullets(player_bullets, player, zombie, zombie_list)
        draw_window(player, player_bullets, zombie, zombie_list)

    pygame.quit()


if __name__ == "__main__":
    main()
