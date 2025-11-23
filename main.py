import pygame
import sys
from buttons import Button

pygame.init()
# Set up the display
screen = pygame.display.set_mode((800, 600))
# create buttons
play_button = Button(300, 250, 200, 50, "Play", (25, 176, 70))
options_button = Button(300, 320, 200, 50, "Options", (25, 176, 70))
quit_button = Button(300, 390, 200, 50, "Quit", (25, 176, 70))
# load background image
menu_bg = pygame.image.load("images\\menu_bg.jpg")
screen_width = 800
screen_height = 600
menu_bg = pygame.transform.scale(menu_bg, (screen_width, screen_height))

running = True
# main menu function for loading the main menu
def main_menu():
    running = True
    while running:

        screen.blit(menu_bg, (0, 0))
        pygame.display.set_caption("Main Menu")
        menu_title = pygame.font.Font("Tiny5-Regular.ttf", 74).render("Main Menu", True, (255, 255, 255))
        text_rect = menu_title.get_rect(center=(screen_width // 2, 150))
        screen.blit(menu_title, text_rect)
        menu_mouse_pos = pygame.mouse.get_pos()
        #places buttons on the screen
        play_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)
        play_button.check_hover(menu_mouse_pos)
        options_button.check_hover(menu_mouse_pos)
        quit_button.check_hover(menu_mouse_pos)


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(menu_mouse_pos):
                    print("Play button clicked")
                if options_button.is_clicked(menu_mouse_pos):
                    print("Options button clicked")
                if quit_button.is_clicked(menu_mouse_pos):
                    running = False
            

       
        pygame.display.flip()


main_menu()

