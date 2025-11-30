import pygame
import math

class Arrow:
    """Arrow that points from player to a target"""
    
    def __init__(self):
        self.color = (255, 200, 0)  # Golden yellow
        self.size = 30
        self.offset = 60  # Distance from player
        
    def draw(self, surface, player_pos, target_pos):
        """Draw arrow pointing from player to target"""
        player_x, player_y = player_pos
        target_x, target_y = target_pos
        
        # Calculate angle between player and target
        dx = target_x - player_x
        dy = target_y - player_y
        angle = math.atan2(dy, dx)
        
        # Position arrow near player in direction of target
        arrow_x = player_x + math.cos(angle) * self.offset
        arrow_y = player_y + math.sin(angle) * self.offset
        
        # Draw arrow triangle
        # Point of arrow
        point_x = arrow_x + math.cos(angle) * self.size
        point_y = arrow_y + math.sin(angle) * self.size
        
        # Back corners of arrow
        angle_left = angle + 2.5
        angle_right = angle - 2.5
        back_size = self.size * 0.6
        
        left_x = arrow_x + math.cos(angle_left) * back_size
        left_y = arrow_y + math.sin(angle_left) * back_size
        right_x = arrow_x + math.cos(angle_right) * back_size
        right_y = arrow_y + math.sin(angle_right) * back_size
        
        # Draw the arrow
        points = [(point_x, point_y), (left_x, left_y), (right_x, right_y)]
        pygame.draw.polygon(surface, self.color, points)
        
        # Optional: Add a distance text
        distance = int(math.sqrt(dx**2 + dy**2))
        font = pygame.font.Font(None, 20)
        dist_text = font.render(f"{distance}m", True, self.color)
        surface.blit(dist_text, (arrow_x - 15, arrow_y - 25))