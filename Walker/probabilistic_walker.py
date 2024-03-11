import random
import numpy as np
from walker import Walker


class ProbabilisticWalker(Walker):
    def __init__(self, up_prob=0.25, down_prob=0.25, left_prob=0.25, right_prob=0.25, to_origin_prob=0.0):
        super().__init__()  # Start at position (0, 0, 0)
        self.__up_prob = up_prob
        self.__down_prob = down_prob
        self.__left_prob = left_prob
        self.__right_prob = right_prob
        self.__to_origin_prob = to_origin_prob

    def run(self):
        """Simulate the walker movement."""
        self.prev_position = self.position
        # Define the possible directions: up, down, left, right, and towards origin
        directions = ["up", "down", "left", "right", "to_origin"]

        # Define the probabilities for each direction
        probabilities = [self.__up_prob, self.__down_prob, self.__left_prob, self.__right_prob, self.__to_origin_prob]

        # Choose a random direction based on probabilities
        direction = random.choices(directions, probabilities)[0]

        # Update the position based on the chosen direction
        if direction == "up":
            self.position = (self.position[0], self.position[1] + 1, self.position[2])
        elif direction == "down":
            self.position = (self.position[0], self.position[1] - 1, self.position[2])
        elif direction == "left":
            self.position = (self.position[0] - 1, self.position[1], self.position[2])
        elif direction == "right":
            self.position = (self.position[0] + 1, self.position[1], self.position[2])
        elif direction == "to_origin":
            # Calculate the direction vector towards the origin
            direction_to_origin = np.array((0, 0, 0)) - np.array(self.position)
            # Normalize the direction vector to obtain a unit vector
            norm = np.linalg.norm(direction_to_origin)
            if norm > 0:  # To avoid division by zero
                direction_to_origin /= norm
            # Update the position by moving one step towards the origin
            self.position = tuple(np.array(self.position) +
                                  np.sign(direction_to_origin) * np.ceil(np.abs(direction_to_origin)))
