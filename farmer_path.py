import pygame
import os
from buttons import Button
from handlesprites import Character
from interactables import Interactable
from state import GameState
from savings import SavingsPile
import time
from HUD import HUD
from arrow import Arrow
from levels import LevelManager
from post_level_stats import EndLevelPopup
from camera import Camera 

pygame.init()
display = pygame.display.set_mode((1170, 720))
background = pygame.image.load("images\\farm aerial 2.png")
pygame.display.set_caption("Money Moves")
hud = HUD()
background = pygame.transform.scale(background, (1170, 720))
camera = Camera(2000, 2000, 1170, 720)

def farmer_path():
    player = Character(200, 250)
    clock = pygame.time.Clock()
    running = True

    screen_width = 1170
    screen_height = 720

    game_state = GameState()
    level_manager = LevelManager()
    arrow = Arrow()
    popup = EndLevelPopup()

    # Get first level and start it
    current_level = level_manager.get_current_level()
    if current_level:
        current_level.start()

    spawn_cooldown = 5  # Spawn events every 5 seconds
    last_spawn = time.time()

    # Level completion state
    showing_popup = False
    level_complete = False

    # Determine max sprite size
    sprite_width = max(f.get_width() for frames in player.animations.values() for f in frames)
    sprite_height = max(f.get_height() for frames in player.animations.values() for f in frames)

    while running:
        # Events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            
            # Handle popup input
            if e.type == pygame.KEYDOWN:
                if showing_popup and e.key == pygame.K_SPACE:
                    # Move to next level
                    level_manager.next_level()
                    current_level = level_manager.get_current_level()
                    
                    if current_level:
                        # Start next level
                        current_level.start()
                        game_state.events.clear()  # Clear old events
                        showing_popup = False
                        level_complete = False
                    else:
                        # Game complete!
                        print("Game completed! All levels finished!")
                        running = False

        # Only update game if not showing popup
        if not showing_popup:
            # Check if level time is up
            if current_level and current_level.is_finished():
                showing_popup = True
                level_complete = True

            # Spawn events based on current level
            if current_level and time.time() - last_spawn >= spawn_cooldown:
                level_manager.spawn_event_for_level(current_level, game_state)
                last_spawn = time.time()

            keys = pygame.key.get_pressed()

            # Movement
            is_moving = False
            if keys[pygame.K_w]:
                player.set_animation("walkup")
                player.y -= 5
                is_moving = True
            elif keys[pygame.K_s]:
                player.set_animation("walkdown")
                player.y += 5
                is_moving = True
            elif keys[pygame.K_a]:
                player.set_animation("walkleft")
                player.x -= 5
                is_moving = True
            elif keys[pygame.K_d]:
                player.set_animation("walkright")
                player.x += 5
                is_moving = True

            if not is_moving and player.current_animation.startswith('walk'):
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
                            
                            # Track stats based on event type
                            if hasattr(event, 'event_type'):
                                if event.event_type == "essential":
                                    level_manager.essentials_completed += 1
                                elif event.event_type == "distractor":
                                    level_manager.distractors_bought += 1
                                elif event.event_type == "scam":
                                    level_manager.scams_fell_for += 1
                        else:
                            print("Not enough money!")

            # Clamp player to new screen bounds
            player.x = max(0, min(player.x, screen_width - sprite_width))
            player.y = max(0, min(player.y, screen_height - sprite_height))

            # Update events (remove expired/completed)
            game_state.update()

        # DRAWING
        clock.tick(60)
        display.blit(background, (0, 0))

        # Draw player
        player.update()
        player.draw(display,camera)

        # Draw arrows pointing to each event
        if not showing_popup:
            player_center = (player.x + sprite_width // 2, player.y + sprite_height // 2)
            for event in game_state.events:
                event_center = (event.rect.centerx, event.rect.centery)
                arrow.draw(display, player_center, event_center)

        # Draw events
        for event in game_state.events:
            event.draw(display)

        # HUD
        hud.draw_money_text(display, game_state.savings)
        hud.draw_money_bar(display, game_state.savings, game_state.max_savings)
        
        # Draw level timer
        if current_level:
            remaining = int(current_level.get_remaining_time())
            timer_font = pygame.font.Font("Tiny5-Regular.ttf", 36)
            timer_text = timer_font.render(f"Time: {remaining}s", True, (255, 255, 255))
            display.blit(timer_text, (20, 100))
            
            # Draw level number
            level_text = timer_font.render(f"Level {current_level.level_num}", True, (255, 255, 255))
            display.blit(level_text, (20, 150))

        # Show popup if level complete
        if showing_popup:
            rank = level_manager.calculate_rank()
            popup.draw(display, 
                      level_manager.current_level,  # Shows the level just completed
                      rank,
                      level_manager.essentials_completed,
                      level_manager.distractors_bought,
                      level_manager.scams_fell_for)

        pygame.display.flip()