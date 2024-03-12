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
        if name in self.__simulations:
            raise ValueError(f"Simulation with name '{name}' already exists.")
        self.__simulations[name] = simulation

    def calculate_average_locations_per_cell(self):
        # Initialize dictionaries to store summed coordinates and counts per cell per walker
        sum_coordinates_per_cell = {}
        count_coordinates_per_cell = {}

        # Iterate over simulations
        for simulation_data in self.__simulations.values():
            # Iterate over walkers and their coordinates
            for walker, walker_data in simulation_data.items():
                walker_locations = np.array(walker_data[WALKER_LOCATIONS])
                # Sum coordinates and update counts
                if walker not in sum_coordinates_per_cell:
                    sum_coordinates_per_cell[walker] = np.zeros_like(walker_locations[0])
                    count_coordinates_per_cell[walker] = np.zeros(len(walker_locations[0]), dtype=int)
                sum_coordinates_per_cell[walker] += np.sum(walker_locations, axis=0)
                count_coordinates_per_cell[walker] += len(walker_locations)

        # Calculate averages
        average_coordinates_per_walker = {}
        for walker, sum_coords in sum_coordinates_per_cell.items():
            count_coords = count_coordinates_per_cell[walker]
            averages = sum_coords / count_coords[:, None]
            average_coordinates_per_walker[walker] = [tuple(coords) for coords in averages]

        self.__average_locations = average_coordinates_per_walker

    def calculate_average_distance_from_origin(self):
        distances = {}
        origin_array = np.array((0, 0, 0))
        for walker, locations in self.__average_locations.items():
            # Convert locations to a NumPy array for efficient computation
            locations_array = np.array(locations)
            # Calculate distances using vectorized operations
            distances[walker] = np.linalg.norm(locations_array - origin_array, axis=1)
        return distances

    def calculate_distances_from_axis(self, axis='X'):
        distances = {}
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}[axis.upper()]
        for walker, locations in self.__average_locations.items():
            # Convert locations to a NumPy array for efficient computation
            locations_array = np.array(locations)
            # Calculate distances using vectorized operations
            distances[walker] = np.abs(locations_array[:, axis_index])
        return distances

    def calculate_average_and_zero_counts(self):
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



