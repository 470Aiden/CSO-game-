import random
import pygame

from events import FinancialEvent  


class GameState:
    def __init__(self):
        self.savings = 500
        self.max_savings = 500
        self.player_money = 0
        self.events = []

        # Load icons
        self.event_images = {
            "Rent Due": pygame.image.load("CSO-game-\\images\\rent due.png").convert_alpha(),
            "Light Bill": pygame.image.load("CSO-game-\\images\\light bill icon.png").convert_alpha(),
            "Buy Shoes": pygame.image.load("CSO-game-\\images\\shoe.png").convert_alpha(),
        }

        # Resize all icons
        for k, img in self.event_images.items():
            self.event_images[k] = pygame.transform.scale(img, (64, 64))

    def spawn_event(self):
        import random
        name, cost, duration = random.choice([
            ("Rent Due", 100, 15),
            ("Light Bill", 60, 12),
            ("Buy Shoes", 50, 25),
        ])

        x = random.randint(100, 900)
        y = random.randint(100, 700)

        img = self.event_images[name]

        event = FinancialEvent(x, y, 64, 64, name, cost, duration, image=img)
        self.events.append(event)
    def update(self):
        """Updates event timers and removes resolved events"""
        for event in self.events:
            event.update()

        # Remove events that are completed OR expired
        self.events = [e for e in self.events if not (e.completed or e.expired)]
