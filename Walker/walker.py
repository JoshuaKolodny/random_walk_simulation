from typing import *
from abc import ABC, abstractmethod

X = 0
Y = 1
Z = 2


class Walker(ABC):
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.__prev_x = 0
        self.__prev_y = 0
        self.__prev_z = 0

    @property
    def position(self) -> Tuple[float, float, float]:
        return self.__x, self.__y, self.__z

    @position.setter
    def position(self, pos: Tuple[float, float, float]) -> None:
        if len(pos) < 2 or len(pos) > 3:
            raise ValueError("Position must be a 2D or 3D tuple")
        self.__x, self.__y = pos[:Z]
        self.__z = pos[Z] if len(pos) == 3 else 0

    @property
    def prev_position(self) -> Tuple[float, float, float]:
        return self.__prev_x, self.__prev_y, self.__prev_z

    @prev_position.setter
    def prev_position(self, pos: Tuple[float, float, float]) -> None:
        if len(pos) < 2 or len(pos) > 3:
            raise ValueError("Position must be a 2D or 3D tuple")
        self.__prev_x, self.__prev_y = pos[:2]
        self.__prev_z = pos[Z] if len(pos) == 3 else 0

    @abstractmethod
    def run(self):
        """Simulate the walker movement."""
        pass

    def calculate_distance_from_point(self, point: Tuple[float, float, float]) -> float:
        """Calculate the distance from current location to point"""
        x_diff = self.__x - point[X]
        y_diff = self.__y - point[Y]
        z_diff = self.__z - point[Z]
        distance = (x_diff ** 2 + y_diff ** 2 + z_diff ** 2) ** 0.5
        return distance

