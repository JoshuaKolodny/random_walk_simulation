from Walker.walker import Walker
import random


class NoRepeatWalker(Walker):
    """
    A Walker subclass that simulates a random walk without repeating the previous direction.

    The walker can move in four directions: up, down, left, and right. The direction is chosen randomly at each step,
    with the constraint that the walker cannot move in the same direction as the previous step.

    Attributes:
        position (Tuple[float, float, float]): The current position of the walker.
        prev_position (Tuple[float, float, float]): The previous position of the walker.
    """

    def __init__(self):
        """
        Initialize a new NoRepeatWalker.

        The walker starts at the origin (0, 0, 0).
        """
        super().__init__()  # Start at position (0, 0, 0)

    def run(self) -> None:
        """
        Simulate the walker movement.

        The walker chooses a random direction and moves one step in that direction. The chosen direction cannot be the
        same as the direction of the previous step.
        """
        # Save the current position as the previous position
        prev_position = self.prev_position
        self.prev_position = self.position

        # Define the possible directions
        directions = [(0.0, 1.0, 0.0), (0.0, -1.0, 0.0), (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)]

        # If there was a previous position, calculate the direction of the previous step
        if prev_position is not None:
            prev_direction = (self.position[0] - prev_position[0], self.position[1] - prev_position[1], self.position[2] - prev_position[2])
            # If the direction of the previous step is in the list of possible directions, remove it
            if prev_direction in directions:
                directions.remove(prev_direction)

        # Choose a random direction from the remaining possible directions
        direction = random.choice(directions)

        # Unpack the current position
        x, y, z = self.position

        # Update the position based on the chosen direction
        x += direction[0]
        y += direction[1]
        z += direction[2]

        # Set the new position
        self.position = (x, y, z)
