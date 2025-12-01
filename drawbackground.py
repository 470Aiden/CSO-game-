import pygame 

def draw_background(screen, background, cam_x, cam_y, world_width, world_height):
    """
    Draws a non-repeating background relative to the camera position.
    cam_x, cam_y: center of the camera in world coordinates
    """
    screen_width, screen_height = screen.get_size()
    
    # Calculate the top-left corner of the portion to draw
    left = int(cam_x - screen_width // 2)
    top = int(cam_y - screen_height // 2)

    # Clamp to world bounds
    left = max(0, min(left, world_width - screen_width))
    top = max(0, min(top, world_height - screen_height))

    # Create a rect for the portion of the background to blit
    bg_rect = pygame.Rect(left, top, screen_width, screen_height)
    
    # Blit only this portion
    screen.blit(background, (0, 0), bg_rect)
