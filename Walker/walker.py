from typing import *
from abc import ABC, abstractmethod


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
        self.__x, self.__y = pos[:2]
        self.__z = pos[2] if len(pos) == 3 else 0

    @property
    def prev_position(self) -> Tuple[float, float, float]:
        return self.__prev_x, self.__prev_y, self.__prev_z

    @prev_position.setter
    def prev_position(self, pos: Tuple[float, float, float]) -> None:
        if len(pos) < 2 or len(pos) > 3:
            raise ValueError("Position must be a 2D or 3D tuple")
        self.__prev_x, self.__prev_y = pos[:2]
        self.__prev_z = pos[2] if len(pos) == 3 else 0

    @abstractmethod
    def run(self):
        """Simulate the walker movement."""
        pass
