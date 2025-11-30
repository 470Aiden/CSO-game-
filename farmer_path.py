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

pygame.init()
display = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Money Moves")
hud = HUD()
def farmer_path():

   
    arrow = Arrow()
    player = Character(200, 250)
    clock = pygame.time.Clock()
    running = True

    screen_width = 1170
    screen_height = 720
    world_width = 1600
    world_height = 900

    game_state = GameState()
    camera = Camera(world_width, world_height, screen_width, screen_height)



    spawn_cooldown = 10
    last_spawn = time.time()

    # Determine max sprite size
    sprite_width = max(f.get_width() for frames in player.animations.values() for f in frames)
    sprite_height = max(f.get_height() for frames in player.animations.values() for f in frames)

    background = pygame.image.load("images\\farm aerial 2.png")
    background = pygame.transform.scale(background, (screen_width * 2, screen_height * 2))
    level_manager = LevelManager()
    current_level = level_manager.get_current_level()
    current_level.start()



    while running:
        
       
        # events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # spawn events
        if time.time() - last_spawn >= 5:  # every 5 seconds spawn level-based events
            level_manager.spawn_event_for_level(current_level, game_state)
            last_spawn = time.time()

        keys = pygame.key.get_pressed()

        # Movement
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.set_animation("walkup")
            player.y -= 5
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.set_animation("walkdown")
            player.y += 5
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.set_animation("walkleft")
            player.x -= 5
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
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
                        if event.event_type == "essential":
                            level_manager.essentials_completed += 1
                        elif event.event_type == "distractor":
                            level_manager.distractors_bought += 1
                        elif event.event_type == "scam":
                            level_manager.scams_fell_for += 1
                        print(f"Paid {event.name} (${event.cost})")

                    else:
                        print("Not enough money!")

        # clamp player
        player.x = max(0, min(player.x, screen_width - sprite_width))
        player.y = max(0, min(player.y, screen_height - sprite_height))

        rect = player.get_rect()
        camera.update(rect.centerx, rect.centery)

        # update events (remove expired/completed)
        game_state.update()
        if current_level.is_finished():
            print(f"Level {current_level.level_num} finished!")

            level_manager.next_level()
            current_level = level_manager.get_current_level()

            if current_level is None:
                print("GAME COMPLETE!")
                running = False
                continue
            game_state.savings = game_state.max_savings
            current_level.start()
        # DRAWING
        clock.tick(60)
        dt = clock.get_time() / 16  # 16ms is 60 FPS baseline
        display.blit(background, (0, 0))

        # draw player
        player.update()
        player.draw(display, camera)

        player_center = (player.x + sprite_width // 2, player.y + sprite_height // 2)
        for event in game_state.events:
            event_center = (event.rect.centerx, event.rect.centery)
            arrow.draw(display, player_center, event_center)

        # draw events (EVERY frame!)
        for event in game_state.events:
            event.draw(display)

        # HUD
        hud.draw_money_text(display, game_state.savings)
        hud.draw_money_bar(display, game_state.savings, game_state.max_savings)
        hud.draw_level_info(display, current_level)

        pygame.display.flip()

class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)

    def apply(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)
    
    def update(self, targetx, targety):
        x = targetx - self.screen_width // 2
        y = targety - self.screen_height // 2

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(0, min(x, self.camera.width - self.screen_width))
        y = max(0, min(y, self.camera.height - self.screen_height))

        self.camera.topleft = (x, y)
        self.camera = pygame.Rect(x, y, self.screen_width, self.screen_height)