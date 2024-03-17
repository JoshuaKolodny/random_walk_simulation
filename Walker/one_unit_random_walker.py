import numpy as np
from Walker.walker import Walker


class OneUnitRandomWalker(Walker):
    """
    A Walker subclass that simulates a one unit random walk.

    The walker can move in any direction in the x-y plane. The direction is chosen randomly at each step.

    Attributes:
        position (Tuple[float, float, float]): The current position of the walker.
        prev_position (Tuple[float, float, float]): The previous position of the walker.
    """

    def __init__(self):
        """
        Initialize a new OneUnitRandomWalker.

        The walker starts at the origin (0, 0, 0).
        """
        super().__init__()  # Start at position (0, 0, 0)

    def run(self) -> None:
        """
        Simulate the walker movement.

        The walker chooses a random direction and moves one unit in that direction.
        """
        self.prev_position = self.position  # Save the current position as the previous position
        # Generate a random angle between 0 and 2*pi (360 degrees)
        theta = np.random.uniform(0, 2*np.pi)

        # Calculate new position
        x = self.position[0] + np.cos(theta)  # Move one unit in the x direction based on the angle
        y = self.position[1] + np.sin(theta)  # Move one unit in the y direction based on the angle
        z = self.position[2]  # Use the current z value
        self.position = (x, y, z)  # Set the new position
