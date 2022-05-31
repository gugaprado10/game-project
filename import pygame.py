import pygame
import os
import random

pygame.mixer.init()

# Variables
FPS = 50
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
MAX_BULLETS = 5
MAX_ZOMBIES = 5
shoot_effect = pygame.mixer.Sound('assets/music_sound_effects/mixkit-short-laser-gun-shot-1670.wav')

# Initialization
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Shooter")
clock = pygame.time.Clock()

# Assets
background = pygame.transform.scale(pygame.image.load(
    'assets/background2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
shooting_frames = [pygame.image.load(
    f"assets/player/shoot{i}.png") for i in range(0, 5)]
right_frames = [pygame.image.load(
    f'assets/player/run{i}.png') for i in range(0, 6)]
left_frames = [pygame.transform.flip(i, True, False) for i in right_frames]
zombie_sprite = pygame.image.load("assets/zombie.png")
heart_size = 30
heart_sprite = pygame.transform.scale(
    pygame.image.load("assets/heart.png"), (heart_size, heart_size))


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.left = False
        self.right = True
        self.walk_count = 0
        self.is_shooting = False
        self.shoot_count = 0

    def draw(self, window):
        if self.walk_count + 1 >= len(right_frames)*3:
            self.walk_count = 0

        if self.shoot_count + 1 >= len(shooting_frames)*3:
            self.shoot_count = 0
            self.is_shooting = False

        if not(self.is_shooting):
            if self.left:
                window.blit(left_frames[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                window.blit(right_frames[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
        else:
            window.blit(shooting_frames[self.shoot_count//3], (self.x, self.y))
            self.shoot_count += 1

        self.move()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.shoot()
            pygame.mixer.Sound.play(shoot_effect)
        if keys[pygame.K_RIGHT] and self.x + self.vel + self.rect().width < SCREEN_WIDTH//3:
            self.right = True
            self.left = False
            self.x += self.vel
        elif keys[pygame.K_LEFT] and self.x - self.vel > 10:
            self.right = False
            self.left = True
            self.x -= self.vel
        if keys[pygame.K_UP] and self.y - self.vel > 270:
            self.y -= self.vel
        elif keys[pygame.K_DOWN] and self.y + self.vel + self.rect().height < SCREEN_HEIGHT:
            self.y += self.vel

    def shoot(self):
        self.is_shooting = True
        if len(bullets) <= MAX_BULLETS and self.shoot_count == 0:
            bullet = Projectile(player.x + player.rect().width,
                                player.y + player.rect().height//2 + 2, 10, 5)
            bullets.append(bullet)

    def rect(self):
        return right_frames[0].get_rect(topleft=(self.x, self.y))


class Projectile(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        self.move()

    def move(self):
        self.x += self.vel
        self.rect.x = self.x
        if self.x > SCREEN_WIDTH:
            bullets.remove(self)


class Enemy(object):
    def __init__(self, sprite):
        self.vel = 5
        self.has_passed = False
        self.sprite = sprite
        self.rect = sprite.get_rect(topleft=(
            random.randrange(900, 1500),
            random.randrange(270, 500)))

    def draw(self, window):
        window.blit(self.sprite, self.rect)
        self.move()

    def move(self):
        self.rect.x -= self.vel
        if self.rect.x <= 20:
            self.has_passed = True
            self.spawn()

    def spawn(self):
        self.rect = self.sprite.get_rect(topleft=(SCREEN_WIDTH, random.randrange(
            270, 500)))


def draw_lives(window):
    for i in range(1, player_health+1):
        window.blit(heart_sprite, (SCREEN_WIDTH - i*(heart_size+5), 10))


def redraw_window():
    window.blit(background, (0, 0))
    draw_lives(window)
    score_text = font.render('Score: ' + str(score), 1, (0, 255, 0))
    window.blit(score_text, (20, 10))

    player.draw(window)
    for zombie in zombies:
        zombie.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    pygame.display.update()


player = Player(50, 270)
bullets = []
zombies = []
score = 0
player_health = 5
font = pygame.font.SysFont('assets/font.ttf', 45, True)


run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    while len(zombies) < MAX_ZOMBIES:
        zombie = Enemy(zombie_sprite)
        zombies.append(zombie)

    for zombie in zombies:
        if zombie.has_passed:
            player_health -= 1
            zombie.spawn()
            zombie.has_passed = False
        for bullet in bullets:
            if zombie.rect.colliderect(bullet.rect):
                zombies.remove(zombie)
                bullets.remove(bullet)
                score += 10
                if score > 250:
                    MAX_ZOMBIES = 10

    if player_health <= 0:
        run = False

    redraw_window()
