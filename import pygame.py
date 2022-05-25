from logging import FileHandler
import pygame
import os
import random

FPS = 60
PLAYER_VELOCITY = 5
ZOMBIE_VELOCITY = 5
BULLET_VEL = 7
RED = (255,0,0)

ZOMBIE_HIT = pygame.USEREVENT + 1

pygame.init()
SCREENWIDTH = 960
SCREENHEIGHT = 540
WIN  = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
ZOMBIE_WIDTH, ZOMBIE_HEIGHT = 40, 40

player_sprite_image = pygame.image.load(
    os.path.join('assets', 'player_sprite.png'))
enemy_sprite_image = pygame.image.load(
    os.path.join('assets', 'zombie.png'))
background = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'background.png')), (SCREENWIDTH, SCREENHEIGHT))

player_sprite = pygame.transform.scale(
    player_sprite_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
zombie_sprite = pygame.transform.scale(
    enemy_sprite_image, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))

def draw_window(player, player_bullets, zombie):
    WIN.blit(background, (0, 0))
    WIN.blit(player_sprite, (player.x, player.y))
    for bullets in player_bullets:
        pygame.draw.rect(WIN, RED, bullets)
    WIN.blit(zombie_sprite, (zombie.x, zombie.y))

    pygame.display.update()
    

def player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_UP] and player.y - PLAYER_VELOCITY > 270:
        player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN] and player.y + PLAYER_VELOCITY + player.height < SCREENHEIGHT:
        player.y += PLAYER_VELOCITY

def handle_bullets (player_bullets, player, zombie):
    for bullet in player_bullets:
        bullet.x += BULLET_VEL
        if zombie.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ZOMBIE_HIT))
            player_bullets.remove(bullet)
            zombie.x = 900
            zombie.y = random.randrange(270, 500)
        elif bullet.x > SCREENWIDTH:
            player_bullets.remove(bullet)

def main():
    player = pygame.Rect(20, 270, PLAYER_WIDTH, PLAYER_HEIGHT)
    zombie = pygame.Rect(900, random.randrange(270, 500), ZOMBIE_WIDTH, ZOMBIE_HEIGHT)

    player_bullets = []
    zombie_health = 1
    player_health = 3
    score = 0 

    clock = pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.x + player.width, player.y + player.height//2 - 2, 10,5)
                    player_bullets.append(bullet)

        zombie.x -= ZOMBIE_VELOCITY

        
        if zombie.x <= 20:
            zombie.x = 900
            zombie.y = random.randrange(270, 500)
            player_health -= 1

        if player_health == 0:
            run = False
        keys_pressed = pygame.key.get_pressed()

        player_movement(keys_pressed, player)
        handle_bullets(player_bullets, player, zombie)
        draw_window(player, player_bullets, zombie)

        
        

        
    pygame.quit()

if __name__ == "__main__":
    main()