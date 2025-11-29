import pygame 
from interactables import Interactable


class SavingsPile(Interactable):
    def __init__(self, x, y, width, height, game_state, image_path=None):
        super().__init__(x, y, width, height, "Savings", "Withdraw money", image_path)
        self.game_state = game_state

    def interact(self):
        # Withdraw fixed amount for simplicity (e.g., $20)
        amount = 20  

        if self.game_state.savings >= amount:
            self.game_state.savings -= amount
            print(f"You withdrew ${amount}. Savings now ${self.game_state.savings}")
        else:
            print("Not enough savings!")
