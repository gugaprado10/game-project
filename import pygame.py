from logging import FileHandler
import pygame
import os

FPS = 60
PLAYER_VELOCITY = 5
BULLET_VEL = 7
MAX_BULLET = 5
RED = (255,0,0)

PLAYER_HIT = pygame.USEREVENT + 1 #playernãoéatingidone?
ZOMBIE_HIT = pygame.USEREVENT + 2

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
    if keys_pressed[pygame.K_UP] and player.y - PLAYER_VELOCITY > 0:
        player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN] and player.y + PLAYER_VELOCITY + player.height < SCREENHEIGHT:
        player.y += PLAYER_VELOCITY

def handle_bullets (player_bullets, player):
    for bullet in player_bullets:
        bullet.x += BULLET_VEL
        if zombie.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ZOMBIE_HIT))
            player_bullets.remove(bullet)
        elif bullet.x > SCREENWIDTH:
            player_bullets.remove(bullet)





def main():
    player = pygame.Rect(20, 270, PLAYER_WIDTH, PLAYER_HEIGHT)

    player_bullets = []
    zombie_health = 1
    player_health = 1

    clock = pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(player.x + player.width, player.y + player.height//2 - 2, 10,5)
                    player_bullets.append(bullet)
        if event.type == PLAYER_HIT:
            player_health -=1

        if event.type == ZOMBIE_HIT:
            zombie_health -=1

    if player_health <= 0:
        winner_text = "You lost"
    if zombie_health <=0:
        #zombiedesaparecer





        
        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player)

        handle_bullets(player_bullets, player)

        draw_window(player, player_bullets)
    pygame.quit()

if __name__ == "__main__":
    main()