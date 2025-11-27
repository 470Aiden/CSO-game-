import random
import pygame
from interactables import Interactable
from events import FinancialEvent  


class GameState:
    def __init__(self):
        self.savings = 200  # total savings stored in pile
        self.player_money = 0  # cash player is carrying

        self.events = []  # active financial events
        self.last_event_time = 0

        # Optional: Preload event images
        self.event_images = {
            "Rent Due": pygame.image.load("mr placeholder.jpg").convert_alpha(),
            "Buy Shoes": pygame.image.load("mr placeholder.jpg").convert_alpha(),
            "Light Bill": pygame.image.load("mr placeholder.jpg").convert_alpha()
        }

    def spawn_event(self):
        """Creates a new financial event"""
        event_types = [
            ("Rent Due", 100, 20),
            ("Light Bill", 60, 15),
            ("Buy Shoes", 50, 25),  # distraction purchase
        ]

        name, cost, duration = random.choice(event_types)

        x = random.randint(100, 800)
        y = random.randint(100, 700)

        event = FinancialEvent(
            x, y, 60, 60,
            name, cost, duration,
            image=self.event_images.get(name)
        )

        self.events.append(event)

    def update(self):
        """Updates event timers and removes expired ones"""
        for event in self.events:
            event.update()

        # Remove expired or completed
        self.events = [e for e in self.events if not (e.expired or e.completed)]
