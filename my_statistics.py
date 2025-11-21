from typing import Dict, List, Optional
from simulation import Simulation
import numpy as np

WALKER = 0
WALKER_LOCATIONS = 1
RADIUS_10 = 2
PASSED_Y = 3


class Statistics:
    """
    A class used to collect and calculate statistics from a simulation.

    ...

    Attributes
    ----------
    __total_simulations : int
        the total number of simulations
    __simulations : dict
        a dictionary of simulations
    __average_locations : dict
        a dictionary of average locations for each walker

    Methods
    -------
    add_simulation(name, simulation):
        Adds a simulation to the statistics.
    calculate_average_locations_per_cell():
        Calculates the average locations per cell for each walker.
    calculate_average_distance_from_origin():
        Calculates the average distance from the origin for each walker.
    calculate_distances_from_axis(axis):
        Calculates the distances from a specified axis for each walker.
    calculate_escape_radius_10():
        Calculates the average number of steps it took for each walker to escape a radius of 10 units.
    calculate_average_passed_y():
        Calculates the average number of times each walker passed the y-axis in all simulations.
    """

    def __init__(self) -> None:
        """
        Initializes a Statistics object with the necessary attributes.

        Attributes:
            __total_simulations (int): The total number of simulations conducted.
            __num_of_steps (int): The number of steps taken in a simulation.
            __simulations (Dict): A dictionary to store the simulation data.
            __average_locations (Dict[str, np.ndarray]): A dictionary to store the average locations of each walker.
        """
        self.__total_simulations = 0
        self.__num_of_steps = 0
        self.__simulations: Dict = {}
        self.__average_locations: Dict[str, np.ndarray] = {}

    @property
    def simulations(self):
        """
        Property to get the simulations data.

        Returns:
            Dict: The simulations data.
        """
        return self.__simulations

    @property
    def num_of_steps(self):
        """
        Property to get the number of steps taken in a simulation.

        Returns:
            int: The number of steps taken in a simulation.
        """
        return self.__num_of_steps

    @num_of_steps.setter
    def num_of_steps(self, num_of_steps):
        """
        Setter to set the number of steps taken in a simulation.

        Args:
            num_of_steps (int): The number of steps to be set.
        """
        self.__num_of_steps = num_of_steps

    @property
    def get_total_simulations(self):
        """
        Returns the total number of simulations.

        Returns
        -------
        int
            the total number of simulations
        """
        return self.__total_simulations

    def add_simulation(self, name: str, simulation: Simulation) -> None:
        """
        Adds a simulation to the statistics.

        Parameters
        ----------
        name : str- the name of the simulation

        simulation : Simulation
            the simulation to be added
        """
        self.__total_simulations += 1
        for walker_name, walker_info in simulation.walkers.items():
            if walker_name not in self.__simulations:
                self.__simulations[walker_name] = {}
            # Convert locations to a NumPy array for efficient computation
            locations = np.array(walker_info[WALKER_LOCATIONS])
            self.__simulations[walker_name][name] = {
                'locations': locations,
                'escaped_from_radius_10': walker_info[RADIUS_10],
                'passed_y_axis': np.array(walker_info[PASSED_Y]),
                'barriers': simulation.barriers,  # Add barriers to the dictionary
                'portal_gates': simulation.portal_gates  # Add portal_gates to the dictionary
            }

    def calculate_average_locations_per_step(self) -> Dict[str, np.ndarray]:
        """
        Calculates the average locations per step for each walker, using the absolute values of the locations,
        in order to account for the fact that the walkers can move in any direction, but we want for statistics
        purposes to know how far they are from the origin.

        Returns
        -------
        dict
            a dictionary where the keys are walker names and the values are numpy arrays of average locations
        """
        # Initialize a dictionary to store the total locations for each walker
        total_locations: Dict[str, np.ndarray] = {}
        simulation_counts: Dict[str, int] = {}

        # Iterate through each walker
        for walker_name, simulations in self.__simulations.items():
            # Initialize the total locations and count for this walker
            simulation_counts[walker_name] = 0

            # Iterate through each simulation for this walker
            for simulation_data in simulations.values():
                locations = simulation_data['locations']

                # If this is the first simulation for this walker,
                # set the total locations to a zero array of the same shape as the locations
                if walker_name not in total_locations:
                    total_locations[walker_name] = np.zeros_like(locations, dtype=float)

                # Add the absolute values of the locations of this simulation to the total locations
                total_locations[walker_name] += np.abs(locations)

                # Increment the count of simulations for this walker
                simulation_counts[walker_name] += 1

        # Calculate the average locations for each walker
        self.__average_locations = {
            walker_name: np.around(total_locations[walker_name] / simulation_counts[walker_name], decimals=5) for
            walker_name in self.__simulations.keys()}
        return self.__average_locations

    def calculate_average_distance_from_origin(self) -> Dict[str, List[float]]:
        """
        Calculates the average distance from the origin for each walker.

        Returns
        -------
        dict
            a dictionary where the keys are walker names and the values are lists of average distances
        """
        distances = {}
        origin_array = np.array((0, 0, 0))
        for walker, locations in self.__average_locations.items():
            # Convert locations to a NumPy array for efficient computation
            locations_array = np.array(locations)
            # Calculate distances using vectorized operations
            raw_distances = np.linalg.norm(locations_array - origin_array, axis=1)
            # Normalize distances to 5 decimal points
            distances[walker] = list(np.around(raw_distances, decimals=5))
        return distances

    def calculate_distances_from_axis(self, axis: str = 'X') -> Dict[str, List[float]]:
        """
        Calculates the distances from a specified axis for each walker.

        Parameters
        ----------
        axis : str, optional
            the axis from which distances are calculated (default is 'X')

        Returns
        -------
        dict
            a dictionary where the keys are walker names and the values are lists of distances
        """
        distances = {}
        axis_indices = {'X': (1, 2), 'Y': (0, 2), 'Z': (0, 1)}[axis.upper()]
        for walker, locations in self.__average_locations.items():
            # Convert locations to a NumPy array for efficient computation
            locations_array = np.array(locations)
            # Calculate distances using vectorized operations
            raw_distances = np.sqrt(np.sum(np.square(locations_array[:, axis_indices]), axis=1))
            # Normalize distances to 5 decimal points
            distances[walker] = list(np.around(raw_distances, decimals=5))
        return distances

    def calculate_escape_radius_10(self) -> Dict[str, Dict[str, Optional[float]]]:
        """
        This function calculates the average number of steps it took for each walker to escape a radius of 10 units.
        It also counts the number of times a walker did not escape the radius.

        Returns:
            dict: A dictionary where the keys are walker names and the values are dictionaries containing the average
            number of steps to escape and the count of times the walker did not escape.
        """
        # Initialize dictionaries to store total steps to escape and counts of not escaping for each walker
        walker_totals: Dict[str, int] = {}
        walker_counts: Dict[str, int] = {}

        # Iterate over all simulations for each walker
        for walker_name, simulations in self.__simulations.items():
            for simulation_name, simulation_data in simulations.items():
                # Get the number of steps it took for the walker to escape a radius of 10 units
                escaped_radius_10 = simulation_data['escaped_from_radius_10']
                # If the walker did not escape, increment the count for that walker
                if escaped_radius_10 == 0:
                    walker_counts[walker_name] = walker_counts.get(walker_name, 0) + 1
                # Otherwise, add the number of steps to the total for that walker
                else:
                    walker_totals[walker_name] = walker_totals.get(walker_name, 0) + escaped_radius_10

        # Initialize a dictionary to store the statistics for each walker
        walker_statistics = {}

        # Calculate the average number of steps to escape and the count of not escaping for each walker
        for walker_name in self.__simulations.keys():
            total = walker_totals.get(walker_name, 0)
            count = walker_counts.get(walker_name, 0)
            num_simulations = len(self.__simulations[walker_name])
            average = total / (num_simulations - count) if num_simulations - count > 0 else None
            walker_statistics[walker_name] = {'average': average, 'zero_count': count}

        return walker_statistics

    def calculate_average_passed_y(self) -> Dict[str, List[float]]:
        """
        This function calculates the average number of times each walker passed the y-axis in all simulations.

        Returns:
            dict: A dictionary where the keys are walker names and the values are lists of averages normalized to 5 decimal points.
        """
        # Initialize a dictionary to store the total number of times each walker passed the y-axis
        walker_passed_y_totals = {}

        # Iterate over all simulations for each walker
        for walker_name, simulations in self.__simulations.items():
            num_simulations = len(simulations)
            for simulation_name, simulation_data in simulations.items():
                # Get the list of times the walker passed the y-axis
                passed_y = simulation_data['passed_y_axis']
                # If this is the first simulation for this walker, initialize the total list with zeros
                if walker_name not in walker_passed_y_totals:
                    walker_passed_y_totals[walker_name] = [0.0] * len(passed_y)
                # Add the number of times the walker passed the y-axis to the total for that walker
                for i in range(len(passed_y)):
                    walker_passed_y_totals[walker_name][i] += passed_y[i] / num_simulations

        # Calculate the average number of times each walker passed the y-axis and normalize to 5 decimal points
        walker_passed_y_averages = {walker_name: [round(value, 5) for value in totals] for walker_name, totals in
                                    walker_passed_y_totals.items()}

        return walker_passed_y_averages

    def calculate_average_leads(self) -> Dict[str, float]:
        """
        Calculates the average number of times each walker led the race in all simulations. Meaning I increment
        after every step of every simulation the walker that is furthest from the origin, then divide
        each walker's count by the number of simulations to get the average.

        Returns
        -------
        dict
            a dictionary where the keys are walker names and the values are the average number of times they led the race.
        """
        # Initialize a dictionary to store the total lead counts for each walker
        walker_total_lead_counts = {walker_name: 0 for walker_name in self.__simulations.keys()}

        # Initialize a dictionary to store the distances for each walker after each step in each simulation
        walker_distances: Dict[str, List] = {walker_name: [] for walker_name in self.__simulations.keys()}

        # Iterate over all walkers and their simulations
        for walker_name, simulations in self.__simulations.items():
            # For each simulation, calculate the distance from the origin after each step
            for simulation_data in simulations.values():
                distances = [np.linalg.norm(location) for location in simulation_data['locations']]
                walker_distances[walker_name].append(distances)

        # Calculate the total number of steps across all simulations
        total_steps = self.__num_of_steps * self.__total_simulations

        # Iterate over each step of each simulation
        for step in range(total_steps):
            # For each step, compare the distances between walkers to determine who is leading
            leading_walker = max(walker_distances,
                                 key=lambda walker: sum(
                                     distances[step % self.__num_of_steps] for distances in walker_distances[walker]))
            # Increment the total lead count for the leading walker
            walker_total_lead_counts[leading_walker] += 1

        # Calculate the average lead count for each walker
        walker_average_leads = {walker_name: lead_count / self.__total_simulations for walker_name, lead_count in
                                walker_total_lead_counts.items()}

        return walker_average_leads
