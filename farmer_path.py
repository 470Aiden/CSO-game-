import pygame
import os
from buttons import Button
from handlesprites import Character

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
    sprite_width = 0
    sprite_height = 0
    for frames in player.animations.values():
        if frames:
            w, h = frames[0].get_size()
            sprite_width = max(sprite_width, w)
            sprite_height = max(sprite_height, h)
    
    while running:
        clock.tick(60)  # 60 FPS
        display.fill((0,0,0))
      
        
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
        else:
            player.set_idle()
        
        # Clamp position to screen bounds
        player.x = max(0, min(player.x, screen_width - sprite_width))
        player.y = max(0, min(player.y, screen_height - sprite_height))
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update and render
        player.update()
        player.draw(display)
        pygame.display.flip()

      