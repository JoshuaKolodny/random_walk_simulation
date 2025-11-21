from typing import Optional, Tuple


class BoundingBox:
    """
    A class used to represent a 2D bounding box.

    ...

    Attributes
    ----------
    min_x : float
        the minimum x-coordinate of the bounding box
    min_y : float
        the minimum y-coordinate of the bounding box
    max_x : float
        the maximum x-coordinate of the bounding box
    max_y : float
        the maximum y-coordinate of the bounding box

    Methods
    -------
    bounds():
        Returns the bounds of the bounding box as a tuple.
    intersects_with(other):
        Checks if the bounding box intersects with another bounding box.
    contains_point(x, y, z=None):
        Checks if a point is within the bounding box.
    """

    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float):
        """
        Constructs all the necessary attributes for the bounding box object.

        Parameters
        ----------
            min_x : float
                the minimum x-coordinate of the bounding box
            min_y : float
                the minimum y-coordinate of the bounding box
            max_x : float
                the maximum x-coordinate of the bounding box
            max_y : float
                the maximum y-coordinate of the bounding box
        """
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Returns the bounds of the bounding box as a tuple.

        Returns
        -------
        tuple
            a tuple containing the minimum x-coordinate, minimum y-coordinate,
            maximum x-coordinate, and maximum y-coordinate of the bounding box
        """
        return self.min_x, self.min_y, self.max_x, self.max_y

    def __eq__(self, other):
        if isinstance(other, BoundingBox):
            return self.min_x == other.min_x and self.min_y == other.min_y and self.max_x == other.max_x and self.max_y == other.max_y
        return False

    def __hash__(self):
        return hash((self.min_x, self.min_y, self.max_x, self.max_y))

    def intersects_with(self, other: 'BoundingBox') -> bool:
        """
        Checks if the bounding box intersects with another bounding box.

        Parameters
        ----------
        other : BoundingBox
            another bounding box to check for intersection

        Returns
        -------
        bool
            True if the bounding boxes intersect, False otherwise
        """
        # Bounding boxes do not intersect if one bounding box is to the left of the other
        # or one bounding box is above the other
        return not (self.max_x < other.min_x or
                    self.min_x > other.max_x or
                    self.max_y < other.min_y or
                    self.min_y > other.max_y)

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        """
        Checks if a point is within the bounding box.

        Parameters
        ----------
        x : float
            the x-coordinate of the point
        y : float
            the y-coordinate of the point
        z : Optional[float]
            the z-coordinate of the point, not used in this method but included for compatibility with subclasses

        Returns
        -------
        bool
            True if the point is within the bounding box, False otherwise
        """
        # A point is within the bounding box if its x-coordinate is between the minimum and maximum x-coordinates
        # of the bounding box and its y-coordinate is between the minimum and maximum y-coordinates of the bounding box
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y


class BoundingBox3D(BoundingBox):
    """
    A class used to represent a 3D bounding box.

    ...

    Attributes
    ----------
    min_z : float
        the minimum z-coordinate of the bounding box
    max_z : float
        the maximum z-coordinate of the bounding box

    Methods
    -------
    bounds():
        Returns the bounds of the bounding box as a tuple.
    contains_point(x, y, z=None):
        Checks if a point is within the bounding box.
    """

    def __init__(self, min_x: float, min_y: float, min_z: float, max_x: float, max_y: float, max_z: float):
        """
        Constructs all the necessary attributes for the 3D bounding box object.

        Parameters
        ----------
            min_x : float
                the minimum x-coordinate of the bounding box
            min_y : float
                the minimum y-coordinate of the bounding box
            min_z : float
                the minimum z-coordinate of the bounding box
            max_x : float
                the maximum x-coordinate of the bounding box
            max_y : float
                the maximum y-coordinate of the bounding box
            max_z : float
                the maximum z-coordinate of the bounding box
        """
        super().__init__(min_x, min_y, max_x, max_y)
        self.min_z = min_z
        self.max_z = max_z

    def bounds(self) -> Tuple[float, float, float, float]:
        """
        Returns the bounds of the bounding box as a tuple.

        Returns
        -------
        tuple
            a tuple containing the minimum x-coordinate, minimum y-coordinate,
            maximum x-coordinate, and maximum y-coordinate of the bounding box
        """
        return self.min_x, self.min_y, self.max_x, self.max_y

    def bounds_z(self) -> Tuple[float, float]:
        """
        Returns the z-coordinate bounds of the bounding box as a tuple.

        Returns
        -------
        tuple
            a tuple containing the minimum z-coordinate and maximum z-coordinate of the bounding box
        """
        return self.min_z, self.max_z

    def contains_point(self, x: float, y: float, z: Optional[float] = None) -> bool:
        """
        Checks if a point is within the bounding box.

        Parameters
        ----------
        x : float
            the x-coordinate of the point
        y : float
            the y-coordinate of the point
        z : Optional[float]
            the z-coordinate of the point

        Returns
        -------
        bool
            True if the point is within the bounding box, False otherwise
        """
        if z is None:
            # If the z-coordinate is not provided, check if the point is within the 2D bounding box
            return super().contains_point(x, y)
        else:
            # A point is within the bounding box if its x-coordinate is between the minimum and maximum x-coordinates
            # of the bounding box, its y-coordinate is between the min and max y-coordinates of the bounding box,
            # and its z-coordinate is between the min and max z-coordinates of the bounding box
            return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y and self.min_z <= z <= self.max_z