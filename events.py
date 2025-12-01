import pygame
import time


display = pygame.display.set_mode((1000, 800))

class FinancialEvent:
    def __init__(self, x, y, w, h, name, cost, duration, image=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.cost = cost
        self.end_time = time.time() + duration
        self.image = image
        self.completed = False
        self.expired = False

    def update(self):
        """Mark event expired when timer runs out"""
        if not self.completed and time.time() > self.end_time:
            self.expired = True

    def draw(self, surface):
        """Draw icon + labels"""
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (200, 50, 50), self.rect)

        # Name
        font = pygame.font.Font(None, 26)
        label = font.render(self.name, True, (255, 255, 255))
        surface.blit(label, (self.rect.x, self.rect.y - 20))

        cost_text = font.render(f"${self.cost}", True, (255, 255, 0))
        surface.blit(cost_text, (self.rect.x, self.rect.y + 60))

        # Timer
        time_left = max(0, int(self.end_time - time.time()))
        timer = font.render(f"{time_left}s", True, (255, 255, 0))
        surface.blit(timer, (self.rect.x + 5, self.rect.y + 70))