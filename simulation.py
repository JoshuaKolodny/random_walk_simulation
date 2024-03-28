from typing import Dict, List, Union
from Walker.walker import Walker
from obstacles_and_barriers import *
from portal_gate import PortalGate

WALKER = 0
WALKER_LOCATIONS = 1
RADIUS_10 = 2
PASSED_Y = 3


class Simulation:
    """
    A class used to represent a Simulation.

    ...

    Attributes
    ----------
    __origin : tuple
        the origin point of the simulation
    __walkers : dict
        a dictionary of walkers participating in the simulation
    __barriers : dict
        a dictionary of barriers present in the simulation
    __portal_gates : dict
        a dictionary of portal gates present in the simulation
    __sim_obstacles_locations : set
        a set of locations occupied by obstacles in the simulation
    __last_x_position : int
        the last x position of a walker
    __passed_y_counter : int
        the counter for the number of times a walker has passed the y-axis

    Methods
    -------
    add_walker(walker):
        Adds a walker to the simulation.
    add_barrier(barrier_name, barrier):
        Adds a barrier to the simulation.
    add_portal_gate(portal_gate_name, portal_gate):
        Adds a portal gate to the simulation.
    simulate(num_steps, max_attempts):
        Runs the simulation for a specified number of steps.
    reset():
        Resets the simulation to its initial state.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the Simulation object.
        """
        self.__origin = (0, 0, 0)
        self.__walkers = {}
        self.__barriers = {}
        self.__portal_gates = {}
        self.__sim_obstacles_locations = {}
        self.__last_x_position = 0
        self.__passed_y_counter = 0

    @property
    def walkers(self) -> Dict[str, List[Union[Walker, List[Tuple[float, float, float]], int, List[int]]]]:
        """
        Returns the walkers participating in the simulation.

        Returns
        -------
        dict
            a dictionary of walkers participating in the simulation
        """
        return self.__walkers

    @property
    def origin(self) -> Tuple[float, float, float]:
        """
        Returns the origin point of the simulation.

        Returns
        -------
        tuple
            a tuple representing the origin point of the simulation
        """
        return self.__origin

    @property
    def barriers(self) -> Dict[str, Barrier2D]:
        """
        Returns the barriers present in the simulation.

        Returns
        -------
        dict
            a dictionary of barriers present in the simulation
        """
        return self.__barriers

    @property
    def portal_gates(self) -> Dict[str, PortalGate]:
        """
        Returns the portal gates present in the simulation.

        Returns
        -------
        dict
            a dictionary of portal gates present in the simulation
        """
        return self.__portal_gates

    @property
    def sim_obstacles_locations(self) -> Dict:
        """
        Returns the locations of obstacles in the simulation.

        Returns
        -------
        set
            a set of locations occupied by obstacles in the simulation
        """
        return self.__sim_obstacles_locations

    def add_walker(self, walker: Walker) -> bool:
        """
        Adds a walker to the simulation.

        Parameters
        ----------
        walker : Walker
            the walker to be added to the simulation

        Returns
        -------
        bool
            True if the walker was added successfully, False otherwise
        """
        if not isinstance(walker, Walker):
            return False

        walker_type = walker.__class__.__name__
        walker_count = sum(walker_name.startswith(walker_type) for walker_name in self.__walkers.keys())
        unique_walker_name = f"{walker_type}{walker_count + 1}"
        self.__walkers[unique_walker_name] = [walker, [], 0, []]
        return True

    def remove_walker(self, walker_name: str) -> bool:
        """
        Removes all walkers from the simulation that start with the given walker name.

        Parameters
        ----------
        walker_name : str
            the start of the name of the walkers to be removed

        Returns
        -------
        bool
            True if any walkers were removed successfully, False otherwise
        """
        removed = False
        for key in list(self.__walkers.keys()):  # Use list to create a copy of keys for iteration
            if key.startswith(walker_name):
                del self.__walkers[key]
                removed = True
        return removed

    def __add_obstacle(self, obstacle_name: str, obstacle: Obstacle, obstacle_dict: Dict[str, Obstacle]) -> Union[bool, str]:
        """
        Adds an obstacle to the simulation.

        Parameters
        ----------
        obstacle_name : str
            The name of the obstacle.
        obstacle : Obstacle
            The obstacle to be added to the simulation.
        obstacle_dict : dict
            The dictionary to which the obstacle will be added.

        Returns
        -------
        bool or str
            True if the obstacle was added successfully, otherwise a string with an error message.
        """
        # Check if the obstacle intersects with any existing obstacles or portal gates
        for existing_bounds in self.__sim_obstacles_locations:
            if obstacle.bounds.intersects_with(existing_bounds):
                return "Obstacle intersects with an existing obstacle."

        # Check if the obstacle intersects with the origin location
        if obstacle.bounds.contains_point(self.__origin[X], self.__origin[Y]):
            return "Obstacle intersects with the origin location."

        # If the name is already used, don't allow to be added
        if obstacle_name in obstacle_dict:
            return f"Obstacle name '{obstacle_name}' is already used."

        # Add the obstacle to the dictionary and its bounds to the locations dictionary
        obstacle_dict[obstacle_name] = obstacle
        self.__sim_obstacles_locations[obstacle.bounds] = obstacle_name

        return True

    def remove_obstacle(self, obstacle_name: str) -> bool:
        """
        Removes an obstacle from the simulation.

        Parameters
        ----------
        obstacle_name : str
            the name of the obstacle to be removed

        Returns
        -------
        bool
            True if the obstacle was removed successfully, False otherwise
        """
        # Check if the obstacle is a barrier
        if obstacle_name in self.__barriers:
            # Get the barrier
            barrier = self.__barriers[obstacle_name]
            # Check if the barrier's bounds are in self.__sim_obstacles_locations
            if barrier.bounds in self.__sim_obstacles_locations:
                # If they are, remove the barrier's bounds from self.__sim_obstacles_locations
                del self.__sim_obstacles_locations[barrier.bounds]
            # Remove the barrier from the simulation
            del self.__barriers[obstacle_name]
            return True

        # Check if the obstacle is a portal gate
        elif obstacle_name in self.__portal_gates:
            # Get the portal gate
            portal_gate = self.__portal_gates[obstacle_name]
            # Check if the portal gate's bounds are in self.__sim_obstacles_locations
            if portal_gate.bounds in self.__sim_obstacles_locations:
                # If they are, remove the portal gate's bounds from self.__sim_obstacles_locations
                del self.__sim_obstacles_locations[portal_gate.bounds]
            # Remove the portal gate from the simulation
            del self.__portal_gates[obstacle_name]
            return True

        # The obstacle was not found
        return False

    def add_barrier(self, barrier_name: str, barrier: Barrier2D) -> Union[bool, str]:
        """
        Adds a barrier to the simulation.

        Parameters
        ----------
        barrier_name : str
            the name of the barrier.
        barrier :
            Barrier2D the barrier to be added to the simulation

        Returns
        -------
        bool
            True if the barrier was added successfully, False otherwise
        """
        return self.__add_obstacle(barrier_name, barrier, self.__barriers)

    def add_portal_gate(self, portal_gate_name: str, portal_gate: PortalGate) -> Union[bool, str]:
        """
        Adds a portal gate to the simulation.

        Parameters
        ----------
        portal_gate_name : str
            the name of the portal gate
        portal_gate : PortalGate
            the portal gate to be added to the simulation

        Returns
        -------
        bool
            True if the portal gate was added successfully, False otherwise
        """
        # Create a bounding box for the destination of the portal gate
        dest_bounds = BoundingBox(portal_gate.destination[0], portal_gate.destination[1],
                                  portal_gate.destination[0], portal_gate.destination[1])

        # Check if the destination of the portal gate intersects with any existing obstacles' locations
        for existing_bounds in self.__sim_obstacles_locations:
            if dest_bounds.intersects_with(existing_bounds):
                return False

        # If the destination is clear, add the portal gate as usual
        return self.__add_obstacle(portal_gate_name, portal_gate, self.__portal_gates)

    def __time_to_escape_radius_10(self, walker_name: str, num_steps: int) -> bool:
        """
        Checks if a walker has escaped a radius of 10 from the origin.

        Parameters
        ----------
        walker_name : str
            the name of the walker
        num_steps : int
            the number of steps taken by the walker

        Returns
        -------
        bool
            True if the walker has escaped a radius of 10 from the origin, False otherwise
        """
        walker = self.__walkers[walker_name][WALKER]
        if walker.calculate_distance_from_point(self.__origin) > 10:
            self.__walkers[walker_name][RADIUS_10] = num_steps
            return True
        return False

    def __passed_y_axis(self, walker_name: str) -> None:
        """
        Checks if a walker has passed the y-axis.

        Parameters
        ----------
        walker_name : str
            the name of the walker
        """
        walker = self.__walkers[walker_name][WALKER]
        # Checks if walker crossed y-axis
        if walker.position[0] * self.__last_x_position < 0:
            self.__passed_y_counter += 1

        self.__walkers[walker_name][PASSED_Y].append(self.__passed_y_counter)
        # Changes the last x position of walker if it's not zero
        self.__last_x_position = walker.position[0] if walker.position[0] != 0 else self.__last_x_position

    def __check_barrier_collision(self, walker: Walker, new_position: Tuple[float, float, float]) -> bool:
        """
        Checks if a walker has collided with a barrier.

        Parameters
        ----------
        walker : Walker
            the walker to be checked
        new_position : tuple
            the new position of the walker

        Returns
        -------
        bool
            True if the walker has collided with a barrier, False otherwise
        """
        for barrier in self.__barriers.values():
            if barrier.intersects_with_walker(walker.prev_position, new_position):
                return True
        return False

    def __check_portal_gate_collision(self, walker: Walker) -> bool:
        """
        Checks if a walker has collided with a portal gate.

        Parameters
        ----------
        walker : Walker
            the walker to be checked

        Returns
        -------
        bool
            True if the walker has collided with a portal gate, False otherwise
        """
        for portal_gate in self.__portal_gates.values():
            if portal_gate.teleport(walker):
                return True
        return False

    def simulate(self, num_steps: int, max_attempts: int = 1000) -> None:
        """
        Runs the simulation for a specified number of steps.

        Parameters
        ----------
        num_steps : int
            the number of steps to be taken in the simulation
        max_attempts : int, optional
            the maximum number of attempts to find a valid move for a walker (default is 1000)
        """
        # Iterate over all walkers in the simulation
        for key in self.__walkers.keys():
            # Initialize escape status, y-axis counter and last x position for each walker
            is_escaped = False
            self.__passed_y_counter = 0
            self.__last_x_position = 0

            # Run the simulation for the specified number of steps
            for step in range(1, num_steps + 1):
                # Get the current walker
                walker = self.__walkers[key][WALKER]

                # Initialize valid move flag and attempts counter
                valid_move = False
                attempts = 0

                # Try to find a valid move for the walker
                while not valid_move and attempts < max_attempts:
                    # Save the current position of the walker
                    walker.prev_position = walker.position

                    # Move the walker
                    walker.run()

                    # Check if the walker collided with a barrier
                    if self.__check_barrier_collision(walker, walker.position):
                        # If a collision occurred, reset the walker's position and increment the attempts counter
                        walker.position = walker.prev_position
                        attempts += 1
                        continue

                    # Check if the walker collided with a portal gate
                    if self.__check_portal_gate_collision(walker):
                        # If a collision occurred, the walker is teleported and the loop is exited
                        break

                    # If no collisions occurred, the move is valid
                    valid_move = True

                # If a valid move not found after maximum attempts, stop the simulation for this walker
                if attempts == max_attempts:
                    print(
                        f"Walker {key} could not find a valid move after {max_attempts} attempts."
                        f" Stopping simulation for this walker.")
                    break

                # Add the walker's new position to its list of locations
                self.__walkers[key][WALKER_LOCATIONS].append(walker.position)

                # Check if the walker has passed the y-axis
                self.__passed_y_axis(key)

                # Check if the walker has escaped a radius of 10 from the origin
                if not is_escaped:
                    is_escaped = self.__time_to_escape_radius_10(key, step)

    def reset(self) -> None:
        """
        Resets the simulation to its initial state.
        """
        for walker_name, walker_info in self.__walkers.items():
            walker_info[WALKER].position = self.origin
            walker_info[WALKER_LOCATIONS] = []
            walker_info[RADIUS_10] = 0
            walker_info[PASSED_Y] = []
        self.__last_x_position = 0
        self.__passed_y_counter = 0
