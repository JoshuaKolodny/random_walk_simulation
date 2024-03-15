class BoundingBox:
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def intersects_with(self, other):
        """The intersects_with method checks if the current
        bounding box (self) intersects with another bounding box (other)."""
        return not (self.max_x < other.min_x or
                    self.min_x > other.max_x or
                    self.max_y < other.min_y or
                    self.min_y > other.max_y)

    def contains_point(self, x, y):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y


class BoundingBox3D:
    def __init__(self, min_x, min_y, min_z, max_x, max_y, max_z):
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z

    def intersects_with(self, other):
        return not (self.max_x < other.min_x or
                    self.min_x > other.max_x or
                    self.max_y < other.min_y or
                    self.min_y > other.max_y or
                    self.max_z < other.min_z or
                    self.min_z > other.max_z)

    def contains_point(self, x, y, z):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y and self.min_z <= z <= self.max_z