from logging import FileHandler
import pygame
import os

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
    if keys_pressed[pygame.K_UP] and player.y - PLAYER_VELOCITY > 0:
        player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN] and player.y + PLAYER_VELOCITY + player.height < SCREENHEIGHT:
        player.y += PLAYER_VELOCITY

def main():
    player = pygame.Rect(20, 250, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player)
        draw_window(player)
    pygame.quit()

if __name__ == "__main__":
    main()