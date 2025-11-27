import pygame
import os
from buttons import Button
from handlesprites import Character
from interactables import Interactable
from state import GameState
from savings import SavingsPile
import time


pygame.init()
display = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Money Moves")

def farmer_path():
    """Main game loop for farmer character"""
    player = Character(200, 250)
    clock = pygame.time.Clock()
    running = True
    screen_width = 1000
    screen_height = 800
    # Determine max sprite size from actual frames
    interactables = [
    Interactable(400, 300, 80, 80, "cash", "Collect money", "images\\cash pile.png")]
    game_state = GameState()
    savings_pile = SavingsPile(100, 600, 80, 80, game_state, "images\\cash pile.png")

    spawn_cooldown = 10  # event every 10 seconds
    last_spawn = time.time()
    
    sprite_width = 0
    sprite_height = 0
    for frames in player.animations.values():
        if frames:
            w, h = frames[0].get_size()
            sprite_width = max(sprite_width, w)
            sprite_height = max(sprite_height, h)
    
    while running:

              # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if time.time() - last_spawn > spawn_cooldown:
            game_state.spawn_event()
            last_spawn = time.time()
        # Handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.set_animation('walkup')
            player.y -= 5
        elif keys[pygame.K_s]:
            player.set_animation('walkdown')
            player.y += 5
        elif keys[pygame.K_a]:
            player.set_animation('walkleft')
            player.x -= 5
        elif keys[pygame.K_d]:
            player.set_animation('walkright')
            player.x += 5
        elif keys[pygame.K_e]:
            player_rect = player.get_rect()
            for obj in interactables:
                if obj.check_near_player(player_rect):
                    obj.interact()
        else:
            player.set_idle()

        for event in game_state.events:
            if event.rect.colliderect(player.get_rect()):
                if keys[pygame.K_e]:  # interact button
                    if game_state.player_money >= event.cost:
                        game_state.player_money -= event.cost
                        event.completed = True
                        print(f"Paid {event.name}. Cost: ${event.cost}")
                    else:
                        print("Not enough money!")

        # Clamp position to screen bounds
        player.x = max(0, min(player.x, screen_width - sprite_width))
        player.y = max(0, min(player.y, screen_height - sprite_height))
        

        # Update and render
        clock.tick(60)
        display.fill((0, 0, 0))
        for obj in interactables:
            obj.draw(display)
        player.update()
        player.draw(display)
        pygame.display.flip()
        
        