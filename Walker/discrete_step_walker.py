from Walker.walker import Walker
import random


class DiscreteStepWalker(Walker):
    """
    A Walker subclass that simulates a discrete step random walk.

    The walker can move in four directions: up, down, left, and right. The direction is chosen randomly at each step.

    Attributes:
        position (Tuple[float, float, float]): The current position of the walker.
        prev_position (Tuple[float, float, float]): The previous position of the walker.
    """

    def __init__(self):
        """
        Initialize a new DiscreteStepWalker.

        The walker starts at the origin (0, 0, 0).
        """
        super().__init__()  # Start at position (0, 0, 0)

    def run(self) -> None:
        """
        Simulate the walker movement.

        The walker chooses a random direction and moves one step in that direction.
        """
        self.prev_position = self.position  # Save the current position as the previous position
        directions = ["up", "down", "left", "right"]  # Define the possible directions
        direction = random.choice(directions)  # Choose a random direction
        x, y, z = self.position  # Unpack the current position

        # Update the position based on the chosen direction
        if direction == "up":
            y += 1
        elif direction == "down":
            y -= 1
        elif direction == "left":
            x -= 1
        elif direction == "right":
            x += 1

        self.position = (x, y, z)  # Set the new position
