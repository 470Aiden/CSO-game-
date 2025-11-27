import pygame
import time

class FinancialEvent:
    def __init__(self, x, y, width, height, name, cost, duration, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.cost = cost
        self.end_time = time.time() + duration
        self.image = image
        self.completed = False
        self.expired = False

    def update(self):
        if not self.completed and time.time() > self.end_time:
            self.expired = True

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, (200, 50, 50), self.rect)

        # Display event name + cost
        font = pygame.font.Font(None, 24)
        label = f"{self.name} - ${self.cost}"
        text = font.render(label, True, (255, 255, 255))
        surface.blit(text, (self.rect.x, self.rect.y - 20))

        # Timer
        time_left = max(0, int(self.end_time - time.time()))
        timer_txt = font.render(f"{time_left}s", True, (255, 220, 100))
        surface.blit(timer_txt, (self.rect.centerx - 10, self.rect.bottom + 5))
