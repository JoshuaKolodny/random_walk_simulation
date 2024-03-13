from Walker.discrete_step_walker import DiscreteStepWalker
from Walker.one_unit_random_walker import OneUnitRandomWalker
from Walker.probabilistic_walker import ProbabilisticWalker
from Walker.random_step_walker import RandomStepWalker
from simulation import Simulation
import numpy as np
WALKER = 0
WALKER_LOCATIONS = 1
RADIUS_10 = 2
PASSED_Y = 3


class Statistics:
    def __init__(self):
        self.__simulations = {}
        self.__average_locations = {}

    def add_simulation(self, name: str, simulation: Simulation):
        for walker_name, walker_info in simulation.walkers.items():
            if walker_name not in self.__simulations:
                self.__simulations[walker_name] = {}
            self.__simulations[walker_name][name] = {
                'locations': walker_info[WALKER_LOCATIONS],
                'escaped_from_radius_10': walker_info[RADIUS_10],
                'passed_y_axis': walker_info[PASSED_Y]
            }

    def calculate_average_locations_per_cell(self):
        # Initialize a dictionary to store the total locations for each walker
        total_locations = {}
        simulation_counts = {}

        # Iterate through each walker
        for walker_name, simulations in self.__simulations.items():
            # Initialize the total locations and count for this walker
            simulation_counts[walker_name] = 0

            # Iterate through each simulation for this walker
            for simulation_data in simulations.values():
                locations = np.array(simulation_data['locations'])

                # If this is the first simulation for this walker, set the total locations to a zero array of the same shape as the locations
                if walker_name not in total_locations:
                    total_locations[walker_name] = np.zeros_like(locations, dtype=float)

                # Add the locations of this simulation to the total locations
                total_locations[walker_name] += locations

                # Increment the count of simulations for this walker
                simulation_counts[walker_name] += 1

        # Calculate the average locations for each walker
        self.__average_locations = {
            walker_name: np.around(total_locations[walker_name] / simulation_counts[walker_name], decimals=5) for
            walker_name in self.__simulations.keys()}
        print(self.__average_locations)

    def calculate_average_distance_from_origin(self):
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

    def calculate_distances_from_axis(self, axis='X'):
        distances = {}
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}[axis.upper()]
        for walker, locations in self.__average_locations.items():
            # Convert locations to a NumPy array for efficient computation
            locations_array = np.array(locations)
            # Calculate distances using vectorized operations
            raw_distances = np.abs(locations_array[:, axis_index])
            # Normalize distances to 5 decimal points
            distances[walker] = list(np.around(raw_distances, decimals=5))
        return distances

    def calculate_escape_radius_10(self):
        walker_totals = {}
        walker_counts = {}

        for simulation in self.__simulations.values():
            for walker_name, walker_data in simulation.walkers.items():
                escaped_radius_10 = walker_data[RADIUS_10]
                if escaped_radius_10 == 0:
                    walker_counts[walker_name] = walker_counts.get(walker_name, 0) + 1
                else:
                    walker_totals[walker_name] = walker_totals.get(walker_name, 0) + escaped_radius_10

        walker_statistics = {}

        for walker_name, total in walker_totals.items():
            count = walker_counts.get(walker_name, 0)
            num_simulations = len(self.__simulations)
            average = total / (num_simulations - count) if num_simulations - count > 0 else None
            walker_statistics[walker_name] = {'average': average, 'zero_count': count}

        return walker_statistics


if __name__ == '__main__':
    simulation1 = Simulation()

    # Add some walkers
    walker1 = OneUnitRandomWalker()
    walker2 = DiscreteStepWalker()
    walker3 = ProbabilisticWalker(100, 1000, 100, 100, 100)
    walker4 = RandomStepWalker()
    simulation1.add_walker(walker1)
    simulation1.add_walker(walker2)
    simulation1.add_walker(walker3)
    simulation1.add_walker(walker4)
    # Create instance of Statistics
    statistics = Statistics()

    # Run simulation for 10 steps
    for i in range(1, 3):
        simulation1.simulate(2)

        for walker_name, walker_info in simulation1.walkers.items():
            print(f"Walker {walker_name}:")
            print(f"  Locations: {walker_info[WALKER_LOCATIONS]}")
            print(f"  Steps to escape radius 10: {walker_info[RADIUS_10]}")
            print(f"  Number of times passed y-axis: {walker_info[PASSED_Y]}")

        statistics.add_simulation(f"Simulation {i}", simulation1)
        simulation1.reset()




    # Calculate statistics
    statistics.calculate_average_locations_per_cell()
    average_distance_from_origin = statistics.calculate_average_distance_from_origin()
    distances_from_axis_x = statistics.calculate_distances_from_axis(axis='Y')
    distances_from_axis_y = statistics.calculate_distances_from_axis(axis='X')
    # escape_radius_10_stats = statistics.calculate_escape_radius_10()
    #
    print(average_distance_from_origin)
    print(distances_from_axis_x)
    print(distances_from_axis_y)
    # print(escape_radius_10_stats)



