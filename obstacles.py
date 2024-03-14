from abc import ABC, abstractmethod
from typing import Tuple


class Obstacle(ABC):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    @abstractmethod
    def position(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def contains_point(self, x, y):
        pass

    @abstractmethod
    def intersects_with_line_segment(self, start, end):
        pass


class Obstacle2D(Obstacle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.__width = width
        self.__height = height

    @property
    def position(self) -> Tuple[float, float]:
        return self._x, self._y

    def contains_point(self, x, y):
        return (self._x <= x <= self._x + self.__width and
                self._y <= y <= self._y + self.__height)

    def intersects_with_line_segment(self, start, end):
        # Define the obstacle's boundaries
        left, right = self._x, self._x + self.__width
        bottom, top = self._y, self._y + self.__height

        # Check if the line segment is completely outside the obstacle
        if max(start[0], end[0]) < left or min(start[0], end[0]) > right or max(start[1], end[1]) < bottom or min(
                start[1], end[1]) > top:
            return False

        # Calculate the line segment's slope and y-intercept
        if start[0] != end[0]:
            slope = (start[1] - end[1]) / (start[0] - end[0])
            y_intercept = start[1] - slope * start[0]

            # Check intersection with the obstacle's vertical sides
            for x in [left, right]:
                y = slope * x + y_intercept
                if bottom <= y <= top:
                    return True

        # If no intersection was found, return False
        return False


class Obstacle3D(Obstacle):
    def __init__(self, x, y, z, width, height, depth):
        super().__init__(x, y)
        self.__z = z
        self.__width = width
        self.__height = height
        self.__depth = depth

    @property
    def position(self) -> Tuple[float, float, float]:
        return self._x, self._y, self.__z

    def contains_point(self, x, y, z):
        return (self._x <= x <= self._x + self.__width and
                self._y <= y <= self._y + self.__height and
                self.__z <= z <= self.__z + self.__depth)

    def intersects_with_line_segment(self, start, end):
        # Define the obstacle's boundaries
        left, right = self._x, self._x + self.__width
        bottom, top = self._y, self._y + self.__height
        back, front = self.__z, self.__z + self.__depth

        # Check if the line segment is completely outside the obstacle
        if max(start[0], end[0]) < left or min(start[0], end[0]) > right or \
                max(start[1], end[1]) < bottom or min(start[1], end[1]) > top or \
                max(start[2], end[2]) < back or min(start[2], end[2]) > front:
            return False

        # Calculate the line segment's direction vector
        dir_vector = [end[i] - start[i] for i in range(3)]

        # For each axis (x, y, z)
        for i in range(3):
            # Calculate the line segment's projection onto the axis
            seg_min = min(start[i], end[i])
            seg_max = max(start[i], end[i])

            # Calculate the obstacle's projection onto the axis
            obs_min = self.position[i] if dir_vector[i] >= 0 else self.position[i] + \
                                                                  [self.__width, self.__height, self.__depth][i]
            obs_max = self.position[i] + [self.__width, self.__height, self.__depth][i] if dir_vector[i] >= 0 else \
            self.position[i]

            # If the projections do not overlap, return False
            if seg_max < obs_min or seg_min > obs_max:
                return False

        # If no separating axis was found, return True
        return True
