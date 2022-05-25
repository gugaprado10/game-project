from logging import FileHandler
import pygame
import os
<<<<<<< HEAD
<<<<<<< Updated upstream
import random
=======
>>>>>>> parent of 3b4f468 (added 1 zombie and 3 live system)

FPS = 60
PLAYER_VELOCITY = 5
BULLET_VEL = 7
RED = (255,0,0)

pygame.init()
SCREENWIDTH = 960
SCREENHEIGHT = 540
WIN  = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50

player_sprite_image = pygame.image.load(
    os.path.join('assets', 'player_sprite.png'))
enemy_sprite_image = pygame.image.load(
    os.path.join('assets', 'zombie_sprite.png'))
background = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background.png')), (SCREENWIDTH, SCREENHEIGHT))

player_sprite = pygame.transform.scale(
    player_sprite_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_window(player, player_bullets):
    WIN.blit(background, (0, 0))
    WIN.blit(player_sprite, (player.x, player.y))
    for bullets in player_bullets:
        pygame.draw.rect(WIN, RED, bullets)

    pygame.display.update()

def player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_UP] and player.y - PLAYER_VELOCITY > 270:
        player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN] and player.y + PLAYER_VELOCITY + player.height < SCREENHEIGHT:
        player.y += PLAYER_VELOCITY

def handle_bullets (player_bullets, player):
    for bullet in player_bullets:
        bullet.x += BULLET_VEL
        if bullet.x > SCREENWIDTH:
            player_bullets.remove(bullet)

def main():
    player = pygame.Rect(20, 270, PLAYER_WIDTH, PLAYER_HEIGHT)

    player_bullets = []
    zombie_health = 1
    player_health = 1

=======

FPS = 60
PLAYER_VELOCITY = 5

pygame.init()
SCREENWIDTH = 900
SCREENHEIGHT = 500
WIN  = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
PLAYER_WIDTH, PLAYER_HEIGHT = 80, 80

player_sprite_image = pygame.image.load(
    r"C:\Users\Giba\Documents\GitHub\game-project\assets\player_sprite.png")
enemy_sprite_image = pygame.image.load(
    r"C:\Users\Giba\Documents\GitHub\game-project\assets\zombie_sprite.png")

player_sprite = pygame.transform.scale(player_sprite_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_window(player):
    WIN.fill((255, 255, 255))
    WIN.blit(player_sprite, (player.x, player.y))
    pygame.display.update()

def player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_UP]:
        player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN]:
        player.y += PLAYER_VELOCITY

def main():
    player = pygame.Rect(20, 250, PLAYER_WIDTH, PLAYER_HEIGHT)
>>>>>>> Stashed changes
    clock = pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
<<<<<<< Updated upstream

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.x + player.width, player.y + player.height//2 - 2, 10,5)
                    player_bullets.append(bullet)
        
        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player)

        handle_bullets(player_bullets, player)

<<<<<<< HEAD
        draw_window(player, player_bullets, zombie)
=======
        
        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player)
        draw_window(player)
>>>>>>> Stashed changes
=======
        draw_window(player, player_bullets)
>>>>>>> parent of 3b4f468 (added 1 zombie and 3 live system)
    pygame.quit()

if __name__ == "__main__":
    main()