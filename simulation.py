import matplotlib.pyplot as plt
import numpy as np

from Walker.walker import Walker

WALKER = 0
WALKER_LOCATIONS = 1
RADIUS_10 = 2
PASSED_Y = 3


# from scipy import stats

# class EventManager:
#     def __init__(self):
#         self._observers = []
#     def register_observer(self, func):
#         """Decorator method to register a function as an observer."""
#         self._observers.append(func)
#         return func
#     def notify_observers(self, info):
#         """Notify all registered observers with the given info."""
#         for observer in self._observers:
#             observer(info)


class Simulation:
    # event_manager = EventManager()
    def __init__(self):
        # self.__total_num_steps = total_num_steps
        self.__origin = (0, 0, 0)
        self.__walkers = {}
        self.__last_x_position = 0

    @property
    def walkers(self):
        return self.__walkers

    @property
    def origin(self):
        return self.__origin

    def add_walker(self, walker: Walker) -> bool:
        if walker.__name__ in self.__walkers.keys():
            return False
        self.__walkers[walker.__name__] = [walker, [], 0, 0]
        return True

    def __time_to_escape_radius_10(self, walker_name: str, num_steps: int):
        walker = self.__walkers[walker_name][WALKER]
        if walker.calculate_distance_from_point(walker.position, self.__origin) > 10:
            self.__walkers[walker_name][RADIUS_10] = num_steps

    # NEED TO GET LOGIC RIGHT
    def __passed_y_axis(self, walker_name: str):
        walker = self.__walkers[walker_name][WALKER]
        # Checks if walker crossed y-axis
        if walker.position[0] * self.__last_x_position < 0:
            self.__walkers[walker_name][PASSED_Y] += 1
        # Changes the last x position of walker if it's not zero
        self.__last_x_position = walker.position[0] if walker.position[0] != 0 else self.__last_x_position

    def simulate(self, num_steps: int):
        is_escaped = False
        for key in self.__walkers.keys():
            self.__last_x_position = 0
            for step in range(1, num_steps + 1):
                walker = self.__walkers[key][WALKER]
                walker.run()
                self.__walkers[key][WALKER_LOCATIONS].append(walker.position)
                self.__passed_y_axis(key)
                if not is_escaped:
                    self.__time_to_escape_radius_10(key, step)
                    is_escaped = True
