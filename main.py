import pygame
import sys
from button import Button
import textwrap


pygame.init()

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("menu_assets/bg-menu.png")
BG = pygame.transform.scale(pygame.image.load(
    "menu_assets/bg-menu.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

run = True


def get_font(size):
    return pygame.font.Font("menu_assets/pixel.ttf", size)


def play():
    global run
    import game
    run = False


def credits():
    while True:
        CREDITS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        font = pygame.font.Font("menu_assets/pixel.ttf", 45, bold=True)
        your_text = "The gruesome zombie apocalypse had broken out three days ago. The world you once knew is gone. The bustling streets are now quiet, except for the occasional cry for help. You are face to face with terrifying creatures - zombies and (sneaky) clowns, which are eager to drink your blood and eat your brain. Keep your eyes open and don't let your weapon out of your hands. Good luck!"
        txtX, txtY = 125, 70
        wraplen = 50
        count = 0
        my_wrap = textwrap.TextWrapper(width=wraplen)
        wrap_list = my_wrap.wrap(text=your_text)
        # Draw one line at a time further down the screen
        for i in wrap_list:
            txtY = txtY + 35
            Mtxt = font.render(f"{i}", True, (255, 255, 255))
            SCREEN.blit(Mtxt, (txtX, txtY))
            count += 1

        # CREDITS_RECT = CREDITS_TEXT.get_rect(
        #     center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200))
        # SCREEN.blit(CREDITS_TEXT, CREDITS_RECT)

        CREDITS_BACK = Button(image=None, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+180),
                              text_input="BACK", font=get_font(75), base_color="White", hovering_color="#1dd200")

        CREDITS_BACK.changeColor(CREDITS_MOUSE_POS)
        CREDITS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CREDITS_BACK.checkForInput(CREDITS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while run == True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("ZombiePopper", True, "#1dd200")
        MENU_RECT = MENU_TEXT.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 200))

        PLAY_BUTTON = Button(image=pygame.image.load("menu_assets/Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        CREDITS_BUTTON = Button(image=pygame.image.load("menu_assets/Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40),
                                text_input="STORY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("menu_assets/Rect.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 180),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, CREDITS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credits()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
