import numpy as np
from Walker.walker import Walker


class RandomStepWalker(Walker):

    def __init__(self):
        super().__init__()

    def run(self):
        """Simulate the walker movement."""
        self.prev_position = self.position
        # Generate a random angle between 0 and 2*pi (360 degrees)
        theta = np.random.uniform(0, 2 * np.pi)

        # Generate a random step size between 0.5 and 1.5
        step_size = np.random.uniform(0.5, 1.5)

        # Calculate new position
        x = self.position[0] + step_size * np.cos(theta)
        y = self.position[1] + step_size * np.sin(theta)
        self.position = (x, y)
