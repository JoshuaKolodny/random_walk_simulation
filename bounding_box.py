from typing import Optional, Tuple


class BoundingBox:
    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def bounds(self) -> Tuple[float, float, float, float]:
        return self.min_x, self.min_y, self.max_x, self.max_y

    def intersects_with(self, other: 'BoundingBox') -> bool:
        return not (self.max_x < other.min_x or
                    self.min_x > other.max_x or
                    self.max_y < other.min_y or
                    self.min_y > other.max_y)

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y


class BoundingBox3D(BoundingBox):
    def __init__(self, min_x: float, min_y: float, min_z: float, max_x: float, max_y: float, max_z: float):
        super().__init__(min_x, min_y, max_x, max_y)
        self.min_z = min_z
        self.max_z = max_z

    def bounds(self) -> Tuple[float, float, float, float]:
        return self.min_x, self.min_y, self.min_z, self.max_z

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        if z is None:
            return super().contains_point(x, y)
        else:
            return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y and self.min_z <= z <= self.max_z
