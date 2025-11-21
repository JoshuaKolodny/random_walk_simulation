import numpy as np
from Walker.walker import Walker


class RandomStepWalker(Walker):
    """
    A Walker subclass that simulates a random step walk.

    The walker can move in any direction in the x-y plane. The direction and step size are chosen randomly at each step.

    Attributes:
        position (Tuple[float, float, float]): The current position of the walker.
        prev_position (Tuple[float, float, float]): The previous position of the walker.
    """

    def __init__(self):
        """
        Initialize a new RandomStepWalker.

        The walker starts at the origin (0, 0, 0).
        """
        super().__init__()  # Start at position (0, 0, 0)

    def run(self) -> None:
        """
        Simulate the walker movement.

        The walker chooses a random direction and moves a random step size in that direction.
        """
        self.prev_position = self.position  # Save the current position as the previous position
        # Generate a random angle between 0 and 2*pi (360 degrees)
        theta = np.random.uniform(0, 2 * np.pi)

        # Generate a random step size between 0.5 and 1.5
        step_size = np.random.uniform(0.5, 1.5)

        # Calculate new position
        x = self.position[0] + step_size * np.cos(theta)  # Move a random step size in the x direction based on the angle
        y = self.position[1] + step_size * np.sin(theta)  # Move a random step size in the y direction based on the angle
        z = self.position[2]  # Use the current z value
        self.position = (x, y, z)  # Set the new position
