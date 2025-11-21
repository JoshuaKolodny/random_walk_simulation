import random
import numpy as np
from Walker.walker import Walker


class BiasedWalker(Walker):
    """
    A Walker subclass that simulates a biased random walk.

    The walker can move in four directions: up, down, left, and right. It can also move towards the origin.
    The probabilities for each direction are specified at initialization and are normalized to sum to 1.

    Attributes:
        __up_prob (float): The probability of moving up.
        __down_prob (float): The probability of moving down.
        __left_prob (float): The probability of moving left.
        __right_prob (float): The probability of moving right.
        __to_origin_prob (float): The probability of moving towards the origin.
    """

    def __init__(self, up_prob: float = 0.25, down_prob: float = 0.25, left_prob: float = 0.25,
                 right_prob: float = 0.25, to_origin_prob: float = 0.0):
        """
        Initialize a new BiasedWalker.

        Args:
            up_prob (float): The initial probability of moving up. Defaults to 0.25.
            down_prob (float): The initial probability of moving down. Defaults to 0.25.
            left_prob (float): The initial probability of moving left. Defaults to 0.25.
            right_prob (float): The initial probability of moving right. Defaults to 0.25.
            to_origin_prob (float): The initial probability of moving towards the origin. Defaults to 0.0.

        Raises:
            ValueError: If any of the probabilities are negative or if their sum is not positive.
        """
        super().__init__()  # Start at position (0, 0, 0)
        # Ensure probabilities are non-negative
        if up_prob < 0 or down_prob < 0 or left_prob < 0 or right_prob < 0 or to_origin_prob < 0:
            raise ValueError("Probabilities must be non-negative.")

        # Normalize probabilities
        total_prob = up_prob + down_prob + left_prob + right_prob + to_origin_prob
        if total_prob <= 0:
            raise ValueError("Total probability must be positive.")
        self.__up_prob = up_prob / total_prob
        self.__down_prob = down_prob / total_prob
        self.__left_prob = left_prob / total_prob
        self.__right_prob = right_prob / total_prob
        self.__to_origin_prob = to_origin_prob / total_prob

    def run(self) -> None:
        """
        Simulate the walker movement.

        The walker chooses a random direction based on the probabilities and moves one step in that direction.
        If the direction is towards the origin, the walker moves one step along the unit vector towards the origin.
        """
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
            direction_to_origin = np.array([0, 0, 0]) - np.array(self.position)
            # Calculate the norm
            norm = np.linalg.norm(direction_to_origin)
            # Check if norm is greater than 0 to avoid division by zero
            if norm > 0:
                # Calculate the unit vector towards the origin
                unit_direction_to_origin = direction_to_origin / norm
                # Define the step size towards the origin
                step_size = 1
                # Calculate the displacement vector towards the origin
                displacement = step_size * unit_direction_to_origin
                # Update the position by adding the displacement
                self.position = tuple(np.array(self.position) + displacement)
