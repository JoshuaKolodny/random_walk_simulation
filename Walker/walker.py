from typing import *
from abc import ABC, abstractmethod

X = 0
Y = 1
Z = 2


class Walker(ABC):
    """
    Abstract base class for a walker in a simulation.

    Attributes:
        position (Tuple[float, float, float]): The current position of the walker.
        prev_position (Tuple[float, float, float]): The previous position of the walker.
    """

    def __init__(self):
        """Initialize a new Walker with position and previous position at the origin."""
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.__prev_x = 0
        self.__prev_y = 0
        self.__prev_z = 0

    @property
    def position(self) -> Tuple[float, float, float]:
        """Get the current position of the walker as a tuple."""
        return self.__x, self.__y, self.__z

    @position.setter
    def position(self, pos: Tuple[float, float, float]) -> None:
        """
        Set the current position of the walker.

        Args:
            pos (Tuple[float, float, float]): The new position of the walker.

        Raises:
            ValueError: If the position is not a 2D or 3D tuple.
        """
        try:
            if len(pos) < 2 or len(pos) > 3:
                raise ValueError("Position must be a 2D or 3D tuple")
            self.__x, self.__y = pos[:Z]
            self.__z = pos[Z] if len(pos) == 3 else 0
        except ValueError as e:
            print(e)

    @property
    def prev_position(self) -> Tuple[float, float, float]:
        """Get the previous position of the walker."""
        return self.__prev_x, self.__prev_y, self.__prev_z

    @prev_position.setter
    def prev_position(self, pos: Tuple[float, float, float]) -> None:
        """
        Set the previous position of the walker.

        Args:
            pos (Tuple[float, float, float]): The new previous position of the walker.

        Raises:
            ValueError: If the position is not a 2D or 3D tuple.
        """
        if len(pos) < 2 or len(pos) > 3:
            raise ValueError("Position must be a 2D or 3D tuple")
        self.__prev_x, self.__prev_y = pos[:2]
        self.__prev_z = pos[Z] if len(pos) == 3 else 0

    @abstractmethod
    def run(self):
        """
        Abstract method to simulate the walker movement.

        This method should be implemented by subclasses.
        """
        pass

    def calculate_distance_from_point(self, point: Tuple[float, float, float]) -> float:
        """
        Calculate the distance from the current location to a given point.

        Args:
            point (Tuple[float, float, float]): The point to calculate the distance to.

        Returns:
            float: The distance from the current location to the point.
        """
        x_diff = self.__x - point[X]
        y_diff = self.__y - point[Y]
        z_diff = self.__z - point[Z]
        distance = (x_diff ** 2 + y_diff ** 2 + z_diff ** 2) ** 0.5
        return distance


