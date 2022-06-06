import pygame
import os
import random
import vlc
import sched, time

def main_game():
    # Variables
    FPS = 50
    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 540
    MAX_BULLETS = 5
    MAX_ZOMBIES = 3
    MAX_CLOWNS = 0
    MAX_FIREBALLS = 4


    # Initialization
    pygame.init()
    pygame.mixer.init()
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
    zombie_sprite = pygame.image.load("assets/zombie.png")
    clown_sprite = pygame.image.load("assets/clown.png")
    boss_sprite = pygame.transform.scale(pygame.image.load('assets/boss sprite.png'), (350, 350))
    heart_size = 30
    heart_sprite = pygame.transform.scale(
        pygame.image.load("assets/heart.png"), (heart_size, heart_size))
    knife_sprite = pygame.transform.scale(
        pygame.image.load("assets/knife.png"), (40, 20))
    fireball_sprite = pygame.transform.scale(
        pygame.image.load("assets/fireball2.png"), (72, 45))
    fireball2_sprite = pygame.transform.scale(
        pygame.image.load("assets/fireball1.png"), (257, 150))
    shoot_effect = pygame.mixer.Sound(
        'assets/music_sound_effects/shootsound.mp3')
    damage_sound = pygame.mixer.Sound(
        'assets/music_sound_effects/Minecraft Oof.mp3')
    laugh_sound = pygame.mixer.Sound(
        'assets/music_sound_effects/laugh.mp3')
    song = vlc.MediaPlayer('assets/music_sound_effects/music.mp3')
    secret_music = vlc.MediaPlayer('assets/music_sound_effects/secret music.mp3')
    boss_hit = pygame.mixer.Sound('assets/music_sound_effects/boss hit.wav')
    victory_fanfare = vlc.MediaPlayer('assets/music_sound_effects/victory fanfare.mp3')

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
                    window.blit(right_frames[self.walk_count//3], (self.x, self.y))
                    self.walk_count += 1
                elif self.right:
                    window.blit(right_frames[self.walk_count//3], (self.x, self.y))
                    self.walk_count += 1
            else:
                window.blit(shooting_frames[self.shoot_count//3], (self.x, self.y))
                self.shoot_count += 1

            self.move(level)

        def move(self, level):
            keys = pygame.key.get_pressed()

            if level == 3: 
                if keys[pygame.K_RIGHT] and self.x + self.vel + self.rect().width < 620:
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
            else:
                if keys[pygame.K_RIGHT] and self.x + self.vel + self.rect().width < SCREEN_WIDTH:
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

    class Boss(object):
        def __init__(self, sprite):
            self.sprite = sprite
            self.rect = sprite.get_rect(topleft=(620,180))
            self.health = 100

        def draw(self, window):
            window.blit(self.sprite, self.rect)

        def health_bar(self, window):
            pygame.draw.rect(window, (255, 215, 0), (715, 135, self.health*2, 25))
            pygame.draw.rect(window, (0, 0, 0), (711, 135, 204, 25), width=4)

        def shoot(self):
                fireball = Projectile(self.rect.x,
                                random.randrange(200, 490), 100, 50, fireball_sprite, -5)
                fireballs.append(fireball)
        
        def shoot2(self):
            fireball2 = Projectile(self.rect.x,
                                random.randrange(200, 490), 100, 50, fireball2_sprite, -5)
            big_fireballs.append(fireball2)

    def draw_lives(window):
        for i in range(1, player_health+1):
            window.blit(heart_sprite, (SCREEN_WIDTH - i*(heart_size+5), 10))


    def redraw_window():
        window.blit(background, (0, 0))
        draw_lives(window)
        score_text = font.render('Score: ' + str(score), 1, (0, 255, 0))
        window.blit(score_text, (20, 10))

        player.draw(window)
        if level == 3:
            boss.draw(window)
            boss.health_bar(window)
        for zombie in zombies:
            zombie.draw(window)
        for clown in clowns:
            clown.draw(window)
        for bullet in bullets:
            bullet.draw(window)
        for knife in knives:
            knife.draw(window)
        for fireball in fireballs:
            fireball.draw(window)
        for fireball2 in big_fireballs:
            fireball2.draw(window)
        pygame.display.update()


    player = Player(50, 270)
    bullets = []
    knives = []
    zombies = []
    clowns = []
    enemies = []
    fireballs = []
    big_fireballs = []
    score = 0
    player_health = 5
    font = pygame.font.Font('assets/font.ttf', 30)
    level_font = pygame.font.Font('assets/font.ttf', 60)
    level2_font = pygame.font.Font('assets/font.ttf', 45)
    level = 1
    secret = False
    boss_special = False
    
    run = True
    while run:
        clock.tick(FPS)
        if level == 1 or level == 2:
            song.play()
            vlc.MediaPlayer.audio_set_volume(song, 80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                song.stop()
                secret_music.stop()
                victory_fanfare.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    pygame.mixer.Sound.play(shoot_effect)
                if event.key == pygame.K_LSHIFT and score > 100 and level == 2:
                    secret = True

        while len(zombies) < MAX_ZOMBIES:
            zombie = Enemy(zombie_sprite)
            zombies.append(zombie)

        for zombie in zombies:
            if zombie.rect.colliderect(player):
                player_health -= 1
                zombie.spawn()
                pygame.mixer.Sound.play(damage_sound)

        for clown in clowns:
            if clown.rect.colliderect(player):
                player_health -= 1
                clown.spawn()
                pygame.mixer.Sound.play(damage_sound)

        if level == 1 and score >= 100 and score < 250:
            MAX_ZOMBIES = 5
        if level == 1 and score >= 250 and score < 500:
            MAX_ZOMBIES = 7
        if level == 1 and score >= 500:
            MAX_ZOMBIES = 10

        if level == 2 and score >= 500 and score < 700:
            MAX_CLOWNS = 6

        if level == 2 and score >= 700 and score < 900:
            MAX_CLOWNS = 8

        if level == 2 and score >= 1000:
            MAX_CLOWNS = 10

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
            if level != 3:
                for bullet in bullets:
                    if bullet.x >= SCREEN_WIDTH:
                        bullets.remove(bullet)
                    elif enemy.rect.colliderect(bullet.rect):
                        if enemy in zombies:
                            zombies.remove(enemy)
                            score += 10
                        else:
                            clowns.remove(enemy)
                            score += 20
                        bullets.remove(bullet)
                for knife in knives:
                    if knife.rect.colliderect(player.rect()):
                        pygame.mixer.Sound.play(damage_sound)
                        player_health -= 1
                        if len(knives) > 0:
                            knives.remove(knife)
                    if knife.x <= 0 and len(knives)>0:
                        knives.remove(knife)

        if level == 3:
            for bullet in bullets:
                if bullet.x >= 680:
                    bullets.remove(bullet)
                    boss.health-=1
                    pygame.mixer.Sound.play(boss_hit)
                    pygame.mixer.Sound.set_volume(boss_hit, 0.5)
                    if boss.health <= 0:
                        secret_music.stop()
                        victory_fanfare.play()
            
            for fireball in fireballs:
                if fireball.rect.colliderect(player.rect()):
                    pygame.mixer.Sound.play(damage_sound)
                    player_health -= 1
                    if len(fireballs) > 0:
                        fireballs.remove(fireball)
                if fireball.x <= 0 and len(fireballs)>0:
                    fireballs.remove(fireball)
            for fireball2 in big_fireballs:
                if fireball2.rect.colliderect(player.rect()):
                    pygame.mixer.Sound.play(damage_sound)
                    player_health -= 1
                    if len(big_fireballs) > 0:
                        fireballs.remove(fireball)
                if fireball2.x + 123 <= 0 and len(fireballs)>0:
                    big_fireballs.remove(fireball2)
            
            #Alternative 1: 
    
            # if boss.health>50:
            #     while len(fireballs)<2:
            #         boss.shoot()
            # if boss.health <= 50:
            #     while len(fireballs)<3:
            #         boss.shoot()
            # if boss.health == 25:
            #     if boss_special == False:
            #         boss.shoot2()
            #         boss_special = True
            # if boss.health == 10:
            #     if boss_special == True:
            #         boss.shoot2()
            #         boss_special = False

            # Alternative 2:

            if boss.health > 50:
                if random.randrange(0, 120) <= 2 and len(fireballs)<MAX_FIREBALLS:
                    boss.shoot()
            if boss.health <= 50:
                MAX_FIREBALLS = 8 
                if random.randrange(0, 100) <= 2 and len(fireballs)<MAX_FIREBALLS:
                    boss.shoot()
            if len(fireballs)==0:
                boss.shoot()
            if boss.health == 25:
                if boss_special == False:
                    boss.shoot2()
                    boss_special = True
            if boss.health == 10:
                if boss_special == True:
                    boss.shoot2()
                    boss_special = False    


        if player_health <= 0: 
            run = False
            song.stop()
            secret_music.stop()

        # Change levels
        if score >= 50 and level == 1:
            level = 2
            background = pygame.transform.scale(pygame.image.load(
                'assets/background2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
            bullets.clear()
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
            MAX_ZOMBIES = 0
            MAX_CLOWNS = 4
            pygame.mixer.Sound.play(laugh_sound)
            time.sleep(5)

        if secret == True and level == 2:
            level = 3
            background = pygame.transform.scale(pygame.image.load(
                'assets/background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
            song.stop()
            secret_music.play()
            MAX_BULLETS = 4
            level_text1 = level2_font.render('You have found the', 1, (0, 255, 0))
            level_text2 = level2_font.render('secret level...', 1, (0, 255, 0))
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
            time.sleep(4)
            MAX_ZOMBIES = 0
            MAX_CLOWNS = 0
            knives.clear()
            zombies.clear()
            clowns.clear()
            enemies.clear()
            player_health = 5
            boss = Boss(boss_sprite)        
            


        redraw_window()

if __name__ == '__main__':
    main_game()