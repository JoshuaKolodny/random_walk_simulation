from Walker.walker import Walker
import random


class NoRepeatWalker(Walker):
    def __init__(self):
        super().__init__()

    def run(self) -> None:
        prev_position = self.prev_position
        self.prev_position = self.position
        directions = [(0.0, 1.0, 0.0), (0.0, -1.0, 0.0), (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)]

        if prev_position is not None:
            prev_direction = (self.position[0] - prev_position[0], self.position[1] - prev_position[1], self.position[2] - prev_position[2])
            if prev_direction in directions:
                directions.remove(prev_direction)

        direction = random.choice(directions)
        x, y, z = self.position

        x += direction[0]
        y += direction[1]
        z += direction[2]

        self.position = (x, y, z)
