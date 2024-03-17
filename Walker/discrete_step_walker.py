from Walker.walker import Walker
import random


class DiscreteStepWalker(Walker):
    def __init__(self):
        super().__init__()  # Start at position (0, 0, 0)

    def run(self) -> None:
        self.prev_position = self.position
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)
        x, y, z = self.position
        if direction == "up":
            y += 1
        elif direction == "down":
            y -= 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
        self.position = (x, y, z)
