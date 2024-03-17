import numpy as np
from Walker.walker import Walker


class OneUnitRandomWalker(Walker):
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        """Simulate the walker movement."""
        self.prev_position = self.position
        # Generate a random angle between 0 and 2*pi (360 degrees)
        theta = np.random.uniform(0, 2*np.pi)

        # Calculate new position
        x = self.position[0] + np.cos(theta)
        y = self.position[1] + np.sin(theta)
        z = self.position[2]  # Use the current z value
        self.position = (x, y, z)
