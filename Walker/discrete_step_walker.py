from walker import Walker
import random


class DiscreteStepWalker(Walker):
    def __init__(self):
        super().__init__()  # Start at position (0, 0, 0)

    def run(self):
        """Simulate the walker movement."""
        self.prev_position = self.position
        # Define the possible directions: up, down, left, right
        directions = ["up", "down", "left", "right"]

        # Choose a random direction
        direction = random.choice(directions)

        # Initialize new_position
        x, y, z = self.position

        # Define the movement offsets for each direction and update new_position
        if direction == "up":
            y += 1
        elif direction == "down":
            y -= 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1

        # Update the position
        self.position = (x, y, z)
