from typing import Tuple, Optional
from Walker.walker import Walker
from bounding_box import BoundingBox
from obstacles_and_barriers import Obstacle


class PortalGate(Obstacle):
    """
    A class representing a PortalGate, which is a subclass of Obstacle.

    ...

    Attributes
    ----------
    __dest_x : float
        the x-coordinate of the portal gate's destination
    __dest_y : float
        the y-coordinate of the portal gate's destination
    __dest_z : float
        the z-coordinate of the portal gate's destination

    Methods
    -------
    bounds():
        Returns the bounding box of the portal gate.
    destination():
        Returns the destination of the portal gate.
    contains_point(x, y, z):
        Checks if a point is within the portal gate.
    intersects_with_walker(start, end):
        Checks if a line segment intersects with the portal gate.
    teleport(walker):
        Teleports a walker to the destination of the portal gate if the walker intersects with the portal gate.
    """

    def __init__(self, x: float, y: float, width: float, height: float, dest_x: float, dest_y: float,
                 dest_z: float = 0.0):
        """
        Constructs all the necessary attributes for the PortalGate object.

        Parameters
        ----------
            x : float
                the x-coordinate of the portal gate
            y : float
                the y-coordinate of the portal gate
            width : float
                the width of the portal gate
            height : float
                the height of the portal gate
            dest_x : float
                the x-coordinate of the portal gate's destination
            dest_y : float
                the y-coordinate of the portal gate's destination
            dest_z : float
                the z-coordinate of the portal gate's destination
        """
        super().__init__(x, y, width, height)
        self.__dest_x = dest_x
        self.__dest_y = dest_y
        self.__dest_z = dest_z

    @property
    def bounds(self) -> BoundingBox:
        """
        Returns the bounding box of the portal gate.

        Returns
        -------
        BoundingBox
            the bounding box of the portal gate
        """
        return BoundingBox(self._x, self._y, self._x + self._width, self._y + self._height)

    @property
    def destination(self) -> Tuple[float, float, float]:
        """
        Returns the destination of the portal gate.

        Returns
        -------
        tuple
            a tuple containing the x-coordinate, y-coordinate, and z-coordinate of the portal gate's destination
        """
        return self.__dest_x, self.__dest_y, self.__dest_z

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        """
        Checks if a point is within the portal gate.

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
            True if the point is within the portal gate, False otherwise
        """
        return (self._x <= x <= self._x + self._width and
                self._y <= y <= self._y + self._height)

    def intersects_with_walker(self, start: Tuple[float, float, float], end: Tuple[float, float, float]) -> bool:
        """
        Checks if a line segment intersects with the portal gate.

        Parameters
        ----------
        start : tuple
            the start point of the line segment
        end : tuple
            the end point of the line segment

        Returns
        -------
        bool
            True if the line segment intersects with the portal gate, False otherwise
        """
        line_segment_bounds = BoundingBox(min(start[0], end[0]), min(start[1], end[1]), max(start[0], end[0]),
                                          max(start[1], end[1]))
        return self.bounds.intersects_with(line_segment_bounds)

    def teleport(self, walker: Walker) -> bool:
        """
        Teleports a walker to the destination of the portal gate if the walker intersects with the portal gate.

        Parameters
        ----------
        walker : Walker
            the walker to be teleported

        Returns
        -------
        bool
            True if the walker was teleported, False otherwise
        """
        if self.intersects_with_walker(walker.prev_position, walker.position):
            walker.position = self.destination
            return True
        return False
