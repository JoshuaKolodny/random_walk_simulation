import matplotlib.pyplot as plt
import numpy as np

from Walker.discrete_step_walker import DiscreteStepWalker
from Walker.one_unit_random_walker import OneUnitRandomWalker
from Walker.probabilistic_walker import ProbabilisticWalker
from Walker.random_step_walker import RandomStepWalker
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
        self.__passed_y_counter = 0

    @property
    def walkers(self):
        return self.__walkers

    @property
    def origin(self):
        return self.__origin

    def add_walker(self, walker: Walker) -> bool:
        if walker.__class__.__name__ in self.__walkers.keys():
            return False
        self.__walkers[walker.__class__.__name__] = [walker, [], 0, []]
        return True

    def __time_to_escape_radius_10(self, walker_name: str, num_steps: int) -> bool:
        walker = self.__walkers[walker_name][WALKER]
        if walker.calculate_distance_from_point(self.__origin) > 10:
            self.__walkers[walker_name][RADIUS_10] = num_steps
            return True
        return False

    # NEED TO GET LOGIC RIGHT
    def __passed_y_axis(self, walker_name: str, step: int):
        walker = self.__walkers[walker_name][WALKER]
        # Checks if walker crossed y-axis
        if walker.position[0] * self.__last_x_position < 0:
            self.__passed_y_counter += 1

        self.__walkers[walker_name][PASSED_Y].append(self.__passed_y_counter)
        # Changes the last x position of walker if it's not zero
        self.__last_x_position = walker.position[0] if walker.position[0] != 0 else self.__last_x_position

    def simulate(self, num_steps: int):
        for key in self.__walkers.keys():
            is_escaped = False
            self.__passed_y_counter = 0
            self.__last_x_position = 0
            for step in range(1, num_steps + 1):
                walker = self.__walkers[key][WALKER]
                walker.run()
                self.__walkers[key][WALKER_LOCATIONS].append(walker.position)
                self.__passed_y_axis(key, step)
                if not is_escaped:
                    is_escaped = self.__time_to_escape_radius_10(key, step)

    def reset(self):
        for walker_name, walker_info in self.__walkers.items():
            walker_info[WALKER].position = self.origin
            walker_info[WALKER_LOCATIONS] = []
            walker_info[RADIUS_10] = 0
            walker_info[PASSED_Y] = []
        self.__last_x_position = 0
        self.__passed_y_counter = 0



if __name__ == "__main__":
    simulation = Simulation()

    # Add some walkers
    walker1 = OneUnitRandomWalker()
    walker2 = DiscreteStepWalker()
    walker3 = ProbabilisticWalker(100, 1000, 100, 100, 100)
    walker4 = RandomStepWalker()
    simulation.add_walker(walker1)
    simulation.add_walker(walker2)
    simulation.add_walker(walker3)
    simulation.add_walker(walker4)

    # Run simulation for 2 steps
    simulation.simulate(2)

    # Check the results
    for walker_name, walker_info in simulation.walkers.items():
        print(f"Walker {walker_name}:")
        print(f"  Locations: {walker_info[WALKER_LOCATIONS]}")
        print(f"  Steps to escape radius 10: {walker_info[RADIUS_10]}")
        print(f"  Number of times passed y-axis: {walker_info[PASSED_Y]}")
