import pygame
import os
from buttons import Button
from handlesprites import Character
from interactables import Interactable
from state import GameState
from savings import SavingsPile
import time
from HUD import HUD


pygame.init()
display = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Money Moves")
hud = HUD()
def farmer_path():

    player = Character(200, 250)
    clock = pygame.time.Clock()
    running = True

    screen_width = 1300
    screen_height = 800

    game_state = GameState()

    spawn_cooldown = 10
    last_spawn = time.time()

    # Determine max sprite size
    sprite_width = max(f.get_width() for frames in player.animations.values() for f in frames)
    sprite_height = max(f.get_height() for frames in player.animations.values() for f in frames)

    background = pygame.image.load("images\\farm aerial 2.png")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    while running:
        

        # events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # spawn events
        if time.time() - last_spawn >= spawn_cooldown:
            game_state.spawn_event()
            last_spawn = time.time()

        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_w]:
            player.set_animation("walkup")
            player.y -= 5
        elif keys[pygame.K_s]:
            player.set_animation("walkdown")
            player.y += 5
        elif keys[pygame.K_a]:
            player.set_animation("walkleft")
            player.x -= 5
        elif keys[pygame.K_d]:
            player.set_animation("walkright")
            player.x += 5
        if not any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]) and player.current_animation.startswith('walk'):
            player.set_idle()  

        # Interaction (independent of movement)
        if keys[pygame.K_e]:
            p_rect = player.get_rect()

            for event in game_state.events:
                if event.rect.colliderect(p_rect):
                    if game_state.savings >= event.cost:
                        game_state.savings -= event.cost
                        event.completed = True
                        print(f"Paid {event.name} (${event.cost})")
                    else:
                        print("Not enough money!")

        # clamp player
        player.x = max(0, min(player.x, screen_width - sprite_width))
        player.y = max(0, min(player.y, screen_height - sprite_height))

        # update events (remove expired/completed)
        game_state.update()

        # DRAWING
        clock.tick(60)
        display.blit(background, (0, 0))

        # draw player
        player.update()
        player.draw(display)

        # draw events (EVERY frame!)
        for event in game_state.events:
            event.draw(display)

        # HUD
        hud.draw_money_text(display, game_state.savings)
        hud.draw_money_bar(display, game_state.savings, game_state.max_savings)

        pygame.display.flip()
