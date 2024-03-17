from typing import Dict, List, Union
from Walker.walker import Walker
from obstacles_and_barriers import *
from portal_gate import PortalGate

WALKER = 0
WALKER_LOCATIONS = 1
RADIUS_10 = 2
PASSED_Y = 3


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
        self.__origin = (0, 0, 0)
        self.__walkers = {}
        self.__barriers = {}
        self.__portal_gates = {}
        self.__sim_obstacles_locations = set()
        self.__last_x_position = 0
        self.__passed_y_counter = 0

    @property
    def walkers(self) -> Dict[str, List[Union[Walker, List[Tuple[float, float, float]], int, List[int]]]]:
        return self.__walkers

    @property
    def origin(self) -> Tuple[float, float, float]:
        return self.__origin

    def add_walker(self, walker: Walker) -> bool:
        if not isinstance(walker, Walker):
            return False

        walker_type = walker.__class__.__name__
        walker_count = sum(walker_name.startswith(walker_type) for walker_name in self.__walkers.keys())
        unique_walker_name = f"{walker_type}{walker_count + 1}"
        self.__walkers[unique_walker_name] = [walker, [], 0, []]
        return True

    def add_obstacle(self, obstacle_name: str, obstacle: Obstacle, obstacle_dict: Dict[str, Obstacle]) -> bool:
        # Check if the obstacle intersects with any existing obstacles or portal gates
        for existing_bounds in self.__sim_obstacles_locations:
            if obstacle.bounds.intersects_with(existing_bounds):
                return False

        # Check if the obstacle intersects with the origin location
        if obstacle.bounds.contains_point(self.__origin[X], self.__origin[Y]):
            return False

        # If the name is already used, append a unique ID
        if obstacle_name in obstacle_dict:
            obstacle_name += str(len(obstacle_dict))

        # Add the obstacle to the dictionary and its bounds to the locations set
        obstacle_dict[obstacle_name] = obstacle
        self.__sim_obstacles_locations.add(obstacle.bounds)

        return True

    def add_barrier(self, barrier_name: str, barrier: Barrier2D) -> bool:
        return self.add_obstacle(barrier_name, barrier, self.__barriers)

    def add_portal_gate(self, portal_gate_name: str, portal_gate: PortalGate) -> bool:
        # Create a bounding box for the destination of the portal gate
        dest_bounds = BoundingBox(portal_gate.destination[0], portal_gate.destination[1],
                                  portal_gate.destination[0], portal_gate.destination[1])

        # Check if the destination of the portal gate intersects with any existing obstacles' locations
        for existing_bounds in self.__sim_obstacles_locations:
            if dest_bounds.intersects_with(existing_bounds):
                return False

        # If the destination is clear, add the portal gate as usual
        return self.add_obstacle(portal_gate_name, portal_gate, self.__portal_gates)

    def __time_to_escape_radius_10(self, walker_name: str, num_steps: int) -> bool:
        walker = self.__walkers[walker_name][WALKER]
        if walker.calculate_distance_from_point(self.__origin) > 10:
            self.__walkers[walker_name][RADIUS_10] = num_steps
            return True
        return False

    def __passed_y_axis(self, walker_name: str) -> None:
        walker = self.__walkers[walker_name][WALKER]
        # Checks if walker crossed y-axis
        if walker.position[0] * self.__last_x_position < 0:
            self.__passed_y_counter += 1

        self.__walkers[walker_name][PASSED_Y].append(self.__passed_y_counter)
        # Changes the last x position of walker if it's not zero
        self.__last_x_position = walker.position[0] if walker.position[0] != 0 else self.__last_x_position

    def check_barrier_collision(self, walker: Walker, new_position: Tuple[float, float, float]) -> bool:
        for barrier in self.__barriers.values():
            if barrier.intersects_with_walker(walker.prev_position, new_position):
                return True
        return False

    def check_portal_gate_collision(self, walker: Walker) -> bool:
        for portal_gate in self.__portal_gates.values():
            if portal_gate.teleport(walker):
                return True
        return False

    def simulate(self, num_steps: int, max_attempts: int = 1000) -> None:
        for key in self.__walkers.keys():
            is_escaped = False
            self.__passed_y_counter = 0
            self.__last_x_position = 0
            for step in range(1, num_steps + 1):
                walker = self.__walkers[key][WALKER]
                valid_move = False
                attempts = 0
                while not valid_move and attempts < max_attempts:
                    walker.prev_position = walker.position
                    walker.run()
                    if self.check_barrier_collision(walker, walker.position):
                        walker.position = walker.prev_position
                        attempts += 1
                        continue
                    if self.check_portal_gate_collision(walker):
                        break
                    valid_move = True
                if attempts == max_attempts:
                    print(
                        f"Walker {key} could not find a valid move after {max_attempts} attempts."
                        f" Stopping simulation for this walker.")
                    break
                self.__walkers[key][WALKER_LOCATIONS].append(walker.position)
                self.__passed_y_axis(key)
                if not is_escaped:
                    is_escaped = self.__time_to_escape_radius_10(key, step)

    def reset(self) -> None:
        for walker_name, walker_info in self.__walkers.items():
            walker_info[WALKER].position = self.origin
            walker_info[WALKER_LOCATIONS] = []
            walker_info[RADIUS_10] = 0
            walker_info[PASSED_Y] = []
        self.__last_x_position = 0
        self.__passed_y_counter = 0


# if __name__ == "__main__":
#     simulation = Simulation()
#
#     # Add some walkers
#     walker1 = OneUnitRandomWalker()
#     walker2 = DiscreteStepWalker()
#     walker3 = ProbabilisticWalker(100, 1000, 100, 100, 100)
#     walker4 = RandomStepWalker()
#     simulation.add_walker(walker1)
#     simulation.add_walker(walker2)
#     simulation.add_walker(walker3)
#     simulation.add_walker(walker4)
#
#     # Run simulation for 2 steps
#     simulation.simulate(2)
#
#     # Check the results
#     for walker_name, walker_info in simulation.walkers.items():
#         print(f"Walker {walker_name}:")
#         print(f"  Locations: {walker_info[WALKER_LOCATIONS]}")
#         print(f"  Steps to escape radius 10: {walker_info[RADIUS_10]}")
#         print(f"  Number of times passed y-axis: {walker_info[PASSED_Y]}")
