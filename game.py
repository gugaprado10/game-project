import pygame
import os
import random
import vlc
import time

pygame.mixer.init()

# Variables
FPS = 50
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
MAX_BULLETS = 5
MAX_ZOMBIES = 4
MAX_CLOWNS = 0


# Initialization
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Shooter")
clock = pygame.time.Clock()

# Assets
background = pygame.transform.scale(pygame.image.load(
    'assets/background1.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
shooting_frames = [pygame.image.load(
    f"assets/player/shoot{i}.png") for i in range(0, 5)]
right_frames = [pygame.image.load(
    f'assets/player/run{i}.png') for i in range(0, 6)]
left_frames = [pygame.transform.flip(i, True, False) for i in right_frames]
zombie_sprite = pygame.image.load("assets/zombie.png")
clown_sprite = pygame.image.load("assets/clown.png")
heart_size = 30
heart_sprite = pygame.transform.scale(
    pygame.image.load("assets/heart.png"), (heart_size, heart_size))
knife_sprite = pygame.transform.scale(
    pygame.image.load("assets/knife.png"), (40, 20))
shoot_effect = pygame.mixer.Sound(
    'assets/music_sound_effects/shootsound.mp3')
damage_sound = pygame.mixer.Sound(
    'assets/music_sound_effects/damagesound.mp3')
laugh_sound = pygame.mixer.Sound(
    'assets/music_sound_effects/laugh.mp3')
song = vlc.MediaPlayer('assets/music_sound_effects/music.mp3')


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(center=(x, y)).center)
    return rotated_image


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
        if len(bullets) <= MAX_BULLETS:
            bullet = Projectile(player.x + player.rect().width,
                                player.y + player.rect().height//2 + 2, 10, 5, None, 15)
            bullets.append(bullet)

    def rect(self):
        return right_frames[0].get_rect(topleft=(self.x, self.y))


class Projectile(object):
    def __init__(self, x, y, width, height,  sprite=None, vel=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.color = (255, 0, 0)
        if not(sprite):
            self.rect = pygame.Rect(x, y, width, height)
            self.sprite = None
        else:
            self.sprite = sprite
            self.rect = sprite.get_rect(topleft=(x, y))

    def draw(self, window):
        if not(self.sprite):
            pygame.draw.rect(window, self.color, self.rect)
        else:
            window.blit(self.sprite, (self.x, self.y))

        self.move()

    def move(self):
        self.x += self.vel
        self.rect.x = self.x


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

    def shoot(self):
        if random.randrange(0, 500) < 1 and self.rect.x >= SCREEN_WIDTH//2:
            knife = Projectile(self.rect.x,
                               self.rect.y + 2, 10, 5, knife_sprite, -10)
            knives.append(knife)


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
    for clown in clowns:
        clown.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    for knife in knives:
        knife.draw(window)
    pygame.display.update()


player = Player(50, 270)
bullets = []
knives = []
zombies = []
clowns = []
enemies = []
score = 0
player_health = 5
font = pygame.font.Font('assets/font.ttf', 30)
level_font = pygame.font.Font('assets/font.ttf', 60)

level = 1

song.play()
vlc.MediaPlayer.audio_set_volume(song, 80)

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                pygame.mixer.Sound.play(shoot_effect)

    while len(zombies) < MAX_ZOMBIES:
        zombie = Enemy(zombie_sprite)
        zombies.append(zombie)

    while len(clowns) < MAX_CLOWNS:
        clown = Enemy(clown_sprite)
        clowns.append(clown)

    enemies = [*clowns, *zombies]

    for enemy in enemies:
        if enemy in clowns:
            enemy.shoot()
        if enemy.has_passed:
            pygame.mixer.Sound.play(damage_sound)
            player_health -= 1

            enemy.spawn()
            enemy.has_passed = False
        for bullet in bullets:
            if bullet.x >= SCREEN_WIDTH:
                bullets.remove(bullet)
            elif enemy.rect.colliderect(bullet.rect):
                if enemy in zombies:
                    zombies.remove(enemy)
                else:
                    clowns.remove(enemy)
                bullets.remove(bullet)
                score += 10

        for knife in knives:
            if knife.x <= 0:
                knives.remove(knife)
            if knife.rect.colliderect(player.rect()):
                pygame.mixer.Sound.play(damage_sound)
                knives.remove(knife)
                player_health -= 1

    if player_health <= 0:
        run = False

    # Change levels
    if score >= 100 and level == 1:

        level = 2
        background = pygame.transform.scale(pygame.image.load(
            'assets/background2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
        bullets = []
        zombies = []
        clowns = []

        level_text1 = level_font.render('Now Prepare...', 1, (0, 255, 0))
        level_text2 = level_font.render('For Level 2', 1, (0, 255, 0))
        level_text_rect1 = level_text1.get_rect()
        level_text_rect2 = level_text2.get_rect()
        pygame.draw.rect(window, (0, 0, 0), pygame.Rect(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        window.blit(level_text1, (SCREEN_WIDTH//2 -
                    level_text_rect1.width//2, SCREEN_HEIGHT//3 -
                    level_text_rect1.height//2))
        window.blit(level_text2, (SCREEN_WIDTH//2 -
                    level_text_rect2.width//2, (SCREEN_HEIGHT//3)*2 -
                    level_text_rect2.height//2))
        pygame.display.update()
        MAX_ZOMBIES = 4
        MAX_CLOWNS = 4
        pygame.mixer.Sound.play(laugh_sound)
        time.sleep(5)
        continue

    redraw_window()
