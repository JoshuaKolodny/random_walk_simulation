from abc import ABC, abstractmethod
from bounding_box import *

X = 0  # Index for x-coordinate in a tuple
Y = 1  # Index for y-coordinate in a tuple
Z = 2  # Index for z-coordinate in a tuple

class Obstacle(ABC):
    """
    An abstract base class representing an obstacle.

    ...

    Attributes
    ----------
    _x : float
        the x-coordinate of the obstacle
    _y : float
        the y-coordinate of the obstacle
    _width : float
        the width of the obstacle
    _height : float
        the height of the obstacle

    Methods
    -------
    bounds():
        Returns the bounding box of the obstacle.
    contains_point(x, y, z):
        Checks if a point is within the obstacle.
    intersects_with_walker(start, end):
        Checks if a line segment intersects with the obstacle.
    """

    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Constructs all the necessary attributes for the Obstacle object.

        Parameters
        ----------
            x : float
                the x-coordinate of the obstacle
            y : float
                the y-coordinate of the obstacle
            width : float
                the width of the obstacle
            height : float
                the height of the obstacle
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    @abstractmethod
    def bounds(self) -> BoundingBox:
        """
        Returns the bounding box of the obstacle.

        Returns
        -------
        BoundingBox
            the bounding box of the obstacle
        """
        pass

    @abstractmethod
    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        """
        Checks if a point is within the obstacle.

        Parameters
        ----------
        x : float
            the x-coordinate of the point
        y : float
            the y-coordinate of the point
        z : float, optional
            the z-coordinate of the point (default is None)

        Returns
        -------
        bool
            True if the point is within the obstacle, False otherwise
        """
        pass

    @abstractmethod
    def intersects_with_walker(self, start: Tuple[float, float, float], end: Tuple[float, float, float]) -> bool:
        """
        Checks if a line segment intersects with the obstacle.

        Parameters
        ----------
        start : tuple
            the start point of the line segment
        end : tuple
            the end point of the line segment

        Returns
        -------
        bool
            True if the line segment intersects with the obstacle, False otherwise
        """
        pass


class Barrier2D(Obstacle):
    """
    A class representing a 2D barrier, which is a subclass of Obstacle.

    ...

    Methods
    -------
    bounds():
        Returns the bounding box of the barrier.
    contains_point(x, y, z):
        Checks if a point is within the barrier.
    intersects_with_walker(start, end):
        Checks if a line segment intersects with the barrier.
    """

    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Constructs all the necessary attributes for the Barrier2D object.

        Parameters
        ----------
            x : float
                the x-coordinate of the barrier
            y : float
                the y-coordinate of the barrier
            width : float
                the width of the barrier
            height : float
                the height of the barrier
        """
        super().__init__(x, y, width, height)

    @property
    def bounds(self) -> BoundingBox:
        """
        Returns the bounding box of the barrier.

        Returns
        -------
        BoundingBox
            the bounding box of the barrier
        """
        return BoundingBox(self._x, self._y, self._x + self._width, self._y + self._height)

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        """
        Checks if a point is within the barrier.

        Parameters
        ----------
        x : float
            the x-coordinate of the point
        y : float
            the y-coordinate of the point
        z : float, optional
            the z-coordinate of the point (default is None)

        Returns
        -------
        bool
            True if the point is within the barrier, False otherwise
        """
        return (self._x <= x <= self._x + self._width and
                self._y <= y <= self._y + self._height)

    def intersects_with_walker(self, start: Tuple[float, float, float], end: Tuple[float, float, float]) -> bool:
        """
        Checks if a line segment intersects with the barrier.

        Parameters
        ----------
        start : tuple
            the start point of the line segment
        end : tuple
            the end point of the line segment

        Returns
        -------
        bool
            True if the line segment intersects with the barrier, False otherwise
        """
        line_segment_bounds = BoundingBox(min(start[X], end[X]), min(start[Y], end[Y]), max(start[X], end[X]),
                                          max(start[Y], end[Y]))
        return self.bounds.intersects_with(line_segment_bounds)


class Barrier3D(Obstacle):
    """
    A class representing a 3D barrier, which is a subclass of Obstacle.

    ...

    Attributes
    ----------
    __z : float
        the z-coordinate of the barrier
    __depth : float
        the depth of the barrier

    Methods
    -------
    bounds():
        Returns the bounding box of the barrier.
    contains_point(x, y, z):
        Checks if a point is within the barrier.
    intersects_with_walker(start, end):
        Checks if a line segment intersects with the barrier.
    """

    def __init__(self, x: float, y: float, z: float, width: float, height: float, depth: float):
        """
        Constructs all the necessary attributes for the Barrier3D object.

        Parameters
        ----------
            x : float
                the x-coordinate of the barrier
            y : float
                the y-coordinate of the barrier
            z : float
                the z-coordinate of the barrier
            width : float
                the width of the barrier
            height : float
                the height of the barrier
            depth : float
                the depth of the barrier
        """
        super().__init__(x, y, width, height)
        self.__z = z
        self.__depth = depth

    @property
    def bounds(self) -> BoundingBox:
        """
        Returns the bounding box of the barrier.

        Returns
        -------
        BoundingBox
            the bounding box of the barrier
        """
        return BoundingBox3D(self._x, self._y, self.__z, self._x + self._width, self._y + self._height,
                             self.__z + self.__depth)

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        """
        Checks if a point is within the barrier.

        Parameters
        ----------
        x : float
            the x-coordinate of the point
        y : float
            the y-coordinate of the point
        z : float, optional
            the z-coordinate of the point (default is None)

        Returns
        -------
        bool
            True if the point is within the barrier, False otherwise
        """
        if z is None:
            raise NotImplementedError("This method must be implemented in a subclass")
        else:
            return self.bounds.contains_point(x, y, z)

    def intersects_with_walker(self, start: Tuple[float, float, float], end: Tuple[float, float, float]) -> bool:
        """
        Checks if a line segment intersects with the barrier.

        Parameters
        ----------
        start : tuple
            the start point of the line segment
        end : tuple
            the end point of the line segment

        Returns
        -------
        bool
            True if the line segment intersects with the barrier, False otherwise
        """
        line_segment_bounds = BoundingBox3D(min(start[X], end[X]), min(start[Y], end[Y]), min(start[Z], end[Z]),
                                            max(start[X], end[X]), max(start[Y], end[Y]), max(start[Z], end[Z]))
        return self.bounds.intersects_with(line_segment_bounds)
