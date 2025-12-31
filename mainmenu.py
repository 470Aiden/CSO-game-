import pygame
import sys
from buttons import Button
from farmer_path import farmer_path
from cutscene import play_farmer_cutscene
pygame.init()
pygame.mixer.init()

# Load the music file
pygame.mixer.music.load('caribbean-beach.mp3')

# Play the music in a loop
pygame.mixer.music.play(-1)

# Set up the display
screen = pygame.display.set_mode((1170, 720))

# load background image
menu_bg = pygame.image.load("images\\menu_bg.jpg")
screen_width = 1170
screen_height = 720
menu_bg = pygame.transform.scale(menu_bg, (screen_width, screen_height))
# create buttons
play_button = Button((screen_width // 2) - 100, 250, 200, 50, "Play", (25, 176, 70))
options_button = Button((screen_width // 2) - 100, 320, 200, 50, "Options", (25, 176, 70))
quit_button = Button((screen_width // 2) - 100, 390, 200, 50, "Quit", (25, 176, 70))

running = True

def play_screen():
    # Load farmer frames for animation
    farmer_frames = []
    try:
        for i in range(0, 8):
            path = f"farmer_frames\\frame_{i:03d}.webp"
            img = pygame.image.load(path).convert_alpha()
            farmer_frames.append(pygame.transform.scale(img, (150, 150)))
    except Exception:
        # If loading fails, create a simple placeholder surface
        farmer_frames = [pygame.Surface((150, 150), pygame.SRCALPHA) for _ in range(4)]
        for s in farmer_frames:
            s.fill((200, 150, 100))

    # For now reuse farmer frames as placeholders for other characters
    other_frames_1 = farmer_frames
    other_frames_2 = farmer_frames

    frame_index = 0
    frame_timer = 0
    frame_delay = 120  # milliseconds per frame

    # Define character selection rects (three horizontally centered)
    slot_w, slot_h = 180, 220
    gap = 60
    total_width = slot_w * 3 + gap * 2
    start_x = (screen_width - total_width) // 2
    y = 220

    slot_rects = [pygame.Rect(start_x + (slot_w + gap) * i, y, slot_w, slot_h) for i in range(3)]

    selected = None
    playing = True
    while playing:
        pygame.mixer.music.set_volume(0.5)
        dt = pygame.time.Clock().tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                for idx, rect in enumerate(slot_rects):
                    if rect.collidepoint((mx, my)):
                        selected = idx
                        if idx == 0:
                            # Play an introductory cutscene for the farmer path,
                            # then transition into the farmer path game.
                            try:
                                play_farmer_cutscene(screen)
                            except SystemExit:
                                raise
                            except Exception:
                                # If cutscene fails for any reason, fallback to game
                                pass
                            farmer_path()
                        playing = False

        # Update animation frame timer
        frame_timer += dt
        if frame_timer >= frame_delay:
            frame_timer = 0
            frame_index = (frame_index + 1) % len(farmer_frames)

        screen.blit(menu_bg, (0, 0))
        pygame.display.set_caption("Play Screen")
        play_title = pygame.font.Font("Tiny5-Regular.ttf", 54).render("Select Character", True, (255, 255, 255))
        text_rect = play_title.get_rect(center=(screen_width // 2, 140))
        screen.blit(play_title, text_rect)
        mouse = pygame.mouse.get_pos()

        # Draw slots and animations
        for i, rect in enumerate(slot_rects):
            # background box
            pygame.draw.rect(screen, (40, 40, 40), rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 3)

            # choose frame set per slot
            if i == 0:
                frame = farmer_frames[frame_index]
            elif i == 1:
                frame = other_frames_1[frame_index % len(other_frames_1)]
            else:
                frame = other_frames_2[frame_index % len(other_frames_2)]


            # center frame inside slot
            f_rect = frame.get_rect(center=(rect.centerx, rect.centery - 10))
            screen.blit(frame, f_rect)

            # label
            label = pygame.font.Font(None, 30).render(f"Character {i+1}", True, (255, 255, 255))
            l_rect = label.get_rect(center=(rect.centerx, rect.bottom - 20))
            screen.blit(label, l_rect)

        pygame.display.flip()

    # After selection: you could return the selected index or transition to game
    return selected

# main menu function for loading the main menu
def main_menu():
    running = True
    while running:
        pygame.mixer.music.set_volume(0.5)
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
                    play_screen()
                if options_button.is_clicked(menu_mouse_pos):
                    print("Options button clicked")
                if quit_button.is_clicked(menu_mouse_pos):
                    running = False
            

       
        pygame.display.flip()


main_menu()

