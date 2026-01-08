import pygame
import os
from buttons import Button
from handlesprites import Character
from state import GameState
import time
from HUD import HUD
from arrow import Arrow
from levels import LevelManager
from post_level_stats import EndLevelPopup
from camera import Camera
from drawbackground import draw_background
from cutscene import play_good_ending, play_bad_ending

display = pygame.display.set_mode((1170, 720))
pygame.init()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background = pygame.image.load("images\\farm aerial 2.png").convert()
pygame.display.set_caption("Money Moves")
hud = HUD()
background = pygame.transform.scale(background, (2000, 1500))


def farmer_path():
    world_width = 2000
    world_height = 1500
    zoom = 1.4
    player = Character(450, 420)
    clock = pygame.time.Clock()
    running = True

    screen_width = display.get_width()
    screen_height = display.get_height()
    camera = Camera(world_width, world_height, screen_width, screen_height, zoom=zoom)
    game_state = GameState()
    level_manager = LevelManager()
    arrow = Arrow()
    popup = EndLevelPopup()

    # Pause state
    paused = False
    pause_start_time = None

    # Pause menu buttons (screen-space)
    resume_button = Button((screen_width // 2) - 100, (screen_height // 2) - 40, 200, 50, "Resume", (25, 176, 70))
    quit_button = Button((screen_width // 2) - 100, (screen_height // 2) + 20, 200, 50, "Quit", (200, 50, 50))

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
        pygame.mixer.music.set_volume(0.5)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            # Handle pause toggle and popup input
            if e.type == pygame.KEYDOWN:
                # Toggle pause when Escape pressed (only when not showing level-complete popup)
                if e.key == pygame.K_ESCAPE and not showing_popup:
                    if not paused:
                        paused = True
                        pause_start_time = time.time()
                    else:
                        # Resume: advance timers by paused duration
                        paused_duration = time.time() - pause_start_time if pause_start_time else 0
                        if current_level and current_level.start_time:
                            current_level.start_time += paused_duration
                        last_spawn += paused_duration
                        paused = False

                # Popup handling (space to continue)
                if showing_popup and e.key == pygame.K_SPACE:
                    # Move to next level
                    game_state.savings = game_state.max_savings
                    try:
                        level_score = level_manager.calculate_score()
                    except Exception:
                        level_score = 0
                    level_manager.cumulative_score += level_score
                    level_manager.next_level()

                    current_level = level_manager.get_current_level()

                    if current_level:
                        current_level.start()
                        game_state.events.clear()
                        showing_popup = False
                        level_complete = False
                    else:
                        # End game
                        num_levels = len(level_manager.levels) if level_manager.levels else 1
                        avg_score = level_manager.cumulative_score / num_levels
                        try:
                            if avg_score >= 20:
                                play_good_ending(display)
                            else:
                                play_bad_ending(display)
                        except Exception:
                            pass
                        running = False

            # Mouse handling for pause menu buttons
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and paused:
                mx, my = pygame.mouse.get_pos()
                if resume_button.is_clicked((mx, my)):
                    # Resume via button
                    paused_duration = time.time() - pause_start_time if pause_start_time else 0
                    if current_level and current_level.start_time:
                        current_level.start_time += paused_duration
                    last_spawn += paused_duration
                    paused = False
                if quit_button.is_clicked((mx, my)):
                    # Quit to menu
                    running = False
                    return

        # Only update game if not showing popup and not paused
        if not showing_popup and not paused:
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
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.set_animation("walkup")
                player.y -= 5
                is_moving = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.set_animation("walkdown")
                player.y += 5
                is_moving = True
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.set_animation("walkleft")
                player.x -= 5
                is_moving = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
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
                                    level_manager.essentials_completed.append(event.name)
                                elif event.event_type == "distractor":
                                    level_manager.distractors_bought.append(event.name)
                                elif event.event_type == "scam":
                                    level_manager.scams_fell_for.append(event.name)
                        else:
                            print("Not enough money!")

            # Clamp player to new screen bounds
            player.x = max(0, min(player.x, world_width - sprite_width))
            player.y = max(0, min(player.y, world_height - sprite_height))

            # Update events (remove expired/completed)
            game_state.update()

        # Camera update regardless of pause so view stays centered on player position
        player_center_x = player.x + sprite_width // 2
        player_center_y = player.y + sprite_height // 2
        camera.update(player_center_x, player_center_y)

        # DRAWING
        clock.tick(60)

        draw_background(display, background, camera.camera, world_width, world_height)

        # Draw events at their world positions (respect camera)
        for event in game_state.events:
            # Convert world rect to screen-space via camera
            event_screen_rect = camera.apply(event.rect)
            # Temporarily set rect so event.draw uses screen coordinates
            original_rect = event.rect
            event.rect = event_screen_rect
            event.draw(display)
            # Restore world rect
            event.rect = original_rect

        # Draw player
        player.update()
        player_rect = pygame.Rect(player.x, player.y, sprite_width, sprite_height)
        player_screen_rect = camera.apply(player_rect)

        # Temporarily change player position for drawing
        temp_x, temp_y = player.x, player.y
        player.x = player_screen_rect.x
        player.y = player_screen_rect.y
        player.draw(display)
        player.x, player.y = temp_x, temp_y

        # Draw arrows pointing to each event (use their screen positions)
        if not showing_popup:
            player_center_x = player_screen_rect.centerx
            player_center_y = player_screen_rect.centery
            player_center = (player_center_x, player_center_y)

            for event in game_state.events:
                event_screen_rect = camera.apply(event.rect)
                event_center = (event_screen_rect.centerx, event_screen_rect.centery)
                arrow.draw(display, player_center, event_center)

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

        # If paused, draw pause overlay and buttons
        if paused:
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            display.blit(overlay, (0, 0))

            pause_title = pygame.font.Font(None, 64).render("Paused", True, (255, 255, 255))
            title_rect = pause_title.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
            display.blit(pause_title, title_rect)

            resume_button.draw(display)
            quit_button.draw(display)

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

    # End of farmer_path, return to caller (main menu)
    return