from Walker.walker import Walker
from obstacles_and_barriers import *


class PortalGate(Obstacle):
    def __init__(self, x: float, y: float, width: float, height: float, dest_x: float, dest_y: float, dest_z: float = 0.0):
        super().__init__(x, y, width, height)
        self.__dest_x = dest_x
        self.__dest_y = dest_y
        self.__dest_z = dest_z

    @property
    def bounds(self) -> BoundingBox:
        return BoundingBox(self._x, self._y, self._x + self._width, self._y + self._height)

    @property
    def destination(self) -> Tuple[float, float, float]:
        return self.__dest_x, self.__dest_y, self.__dest_z

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        # Check if the point is within the bounds of the portal gate
        return (self._x <= x <= self._x + self._width and
                self._y <= y <= self._y + self._height)

    def intersects_with_walker(self, start: Tuple[float, float, float], end: Tuple[float, float, float]) -> bool:
        # Create a bounding box for the line segment from start to end
        line_segment_bounds = BoundingBox(min(start[0], end[0]), min(start[1], end[1]), max(start[0], end[0]),
                                          max(start[1], end[1]))

        # Check if the bounding box of the line segment intersects with the bounding box of the obstacle
        return self.bounds.intersects_with(line_segment_bounds)

    def teleport(self, walker: Walker) -> bool:
        # Check if the walker intersects with the portal gate
        if self.intersects_with_walker(walker.prev_position, walker.position):
            # If there's an intersection, move the walker's position to the destination of the portal gate
            walker.position = self.destination
            return True
        return False
    