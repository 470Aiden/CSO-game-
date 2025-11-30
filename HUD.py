import pygame

class HUD:
    def __init__(self):
        self.font = pygame.font.Font("Tiny5-Regular.ttf", 48)

        # Bar settings
        self.bar_width = 250
        self.bar_height = 22
        self.bar_color = (50, 220, 50)
        self.bar_bg = (30, 80, 30)
        self.pixel_edge = (0, 0, 0)

    def draw_money_text(self, surface, savings):
        text = self.font.render(f"${savings}", True, (255, 255, 255))
        surface.blit(text, (20, 20))

    def draw_money_bar(self, surface, current, maximum):
        """Draw the pixel-style savings bar."""
        x, y = 20, 70

        # Background
        pygame.draw.rect(surface, self.bar_bg, (x, y, self.bar_width, self.bar_height))

        # Foreground based on percentage
        ratio = max(0, current / maximum)
        fill_width = int(self.bar_width * ratio)

        pygame.draw.rect(surface, self.bar_color, (x, y, fill_width, self.bar_height))

        # Pixel outline
        pygame.draw.rect(surface, self.pixel_edge, (x, y, self.bar_width, self.bar_height), 3)
    def draw_level_info(self, surface, level):
        font = pygame.font.Font("Tiny5-Regular.ttf", 36)

        text = font.render(f"Level {level.level_num}", True, (255, 255, 255))
        surface.blit(text, (20, 140))

        timer = font.render(f"Time: {int(level.get_remaining_time())}", True, (255, 255, 0))
        surface.blit(timer, (20, 180))