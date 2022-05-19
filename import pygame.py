from logging import FileHandler
import pygame
import os

FPS = 60
da,kjfad,FileHandler



pygame.init()
SCREENWIDTH = 900
SCREENHEIGHT = 500
WIN  = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

def draw_window():
    WIN.fill((255, 255, 255))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False

        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()