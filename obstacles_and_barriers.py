from abc import ABC, abstractmethod
from typing import Tuple
from bounding_box import *

X = 0
Y = 1
Z = 2


class Obstacle(ABC):
    def __init__(self, x: float, y: float, width: float, height: float):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    @abstractmethod
    def bounds(self) -> BoundingBox:
        pass

    @abstractmethod
    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        pass

    @abstractmethod
    def intersects_with_walker(self, start: Tuple[float, float, float], end: Tuple[float, float, float]) -> bool:
        pass


class Barrier2D(Obstacle):
    def __init__(self, x: float, y: float, width: float, height: float):
        super().__init__(x, y, width, height)

    @property
    def bounds(self) -> BoundingBox:
        return BoundingBox(self._x, self._y, self._x + self._width, self._y + self._height)

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        return (self._x <= x <= self._x + self._width and
                self._y <= y <= self._y + self._height)

    def intersects_with_walker(self, start: Tuple[float, float, float], end: Tuple[float, float, float]) -> bool:
        line_segment_bounds = BoundingBox(min(start[X], end[X]), min(start[Y], end[Y]), max(start[X], end[X]),
                                          max(start[Y], end[Y]))
        return self.bounds.intersects_with(line_segment_bounds)


class Barrier3D(Obstacle):
    def __init__(self, x: float, y: float, z: float, width: float, height: float, depth: float):
        super().__init__(x, y, width, height)
        self.__z = z
        self.__depth = depth

    @property
    def bounds(self) -> BoundingBox:
        return BoundingBox3D(self._x, self._y, self.__z, self._x + self._width, self._y + self._height,
                             self.__z + self.__depth)

    def contains_point(self, x: float, y: float, z: float = None) -> bool:
        if z is None:
            return super().contains_point(x, y)
        else:
            return self.bounds.contains_point(x, y, z)

    def intersects_with_walker(self, start: Tuple[float, float, float], end: Tuple[float, float, float]) -> bool:
        line_segment_bounds = BoundingBox3D(min(start[X], end[X]), min(start[Y], end[Y]), min(start[Z], end[Z]),
                                            max(start[X], end[X]), max(start[Y], end[Y]), max(start[Z], end[Z]))
        return self.bounds.intersects_with(line_segment_bounds)
