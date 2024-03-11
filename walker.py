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

    @position.setter
    def position(self, pos: Tuple[float, float, float]) -> None:
        if len(pos) < 2 or len(pos) > 3:
            raise ValueError("Position must be a 2D or 3D tuple")
        self.__prev_x, self.__prev_y = pos[:2]
        self.__prev_z = pos[2] if len(pos) == 3 else 0

    @abstractmethod
    def run(self):
        """Simulate the walker movement."""
        pass


# def plot_walk(x, y):
#     """Plot the walker's movement."""
#     plt.figure(figsize=(8, 6))
#     plt.plot(x, y, lw=1.5)
#     plt.title("Walker's Movement")
#     plt.xlabel("X")
#     plt.ylabel("Y")
#     plt.grid(True)
#     plt.show()

#
# def main():
#     """Main function to run the simulation."""
#     n_steps = 1000  # Number of steps in the random walk
#     walker = Walker()
#
#     # Simulate walker movement
#     x = [walker.x]
#     y = [walker.y]
#     for _ in range(n_steps):
#         walker.run()
#         x.append(walker.x)
#         y.append(walker.y)
#
#     plot_walk(x, y)
#
#
# if __name__ == "__main__":
#     main()
