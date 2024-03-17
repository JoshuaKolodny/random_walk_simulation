import matplotlib.pyplot as plt
from statistics import Statistics
import textwrap

class Graph:
    """
    A class used to represent a Graph for visualizing data.

    ...

    Attributes
    ----------
    statistics : Statistics
        an instance of the Statistics class which contains the data to be visualized

    Methods
    -------
    plot_single_simulation(simulation):
        Plots the positions of walkers in a single simulation.
    plot_average_locations_per_cell():
        Plots the average locations per cell for all walkers.
    plot_average_distance_from_origin():
        Plots the average distance from the origin for all walkers.
    plot_distances_from_axis(axis='X'):
        Plots the distances from a specified axis for all walkers.
    plot_escape_radius_10():
        Plots the escape radius for all walkers.
    plot_average_passed_y():
        Plots the average number of times each walker crossed the Y axis.
    """

    def __init__(self, statistics: Statistics):
        """
        Constructs all the necessary attributes for the Graph object.

        Parameters
        ----------
            statistics : Statistics
                an instance of the Statistics class which contains the data to be visualized
        """
        self.statistics = statistics

    def plot_single_simulation(self, simulation):
        """
        Plots the positions of walkers in a single simulation.

        Parameters
        ----------
        simulation : Simulation
            a single simulation instance containing walker data
        """
        # Iterate over each walker in the simulation
        for walker_name, walker_info in simulation.walkers.items():
            positions = walker_info[1]
            x_positions = [pos[0] for pos in positions]
            y_positions = [pos[1] for pos in positions]
            plt.scatter(x_positions, y_positions, label=walker_name)
        plt.legend()
        plt.title('Walker Positions')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.show()

    def plot_average_locations_per_cell(self):
        """
        Plots the average locations per cell for all walkers.
        """
        # Iterate over each walker's average locations
        for walker_name, average_locations in self.statistics.calculate_average_locations_per_cell().items():
            plt.plot(average_locations, label=walker_name)
        plt.legend()
        plt.title('Average Locations Per Cell')  # Add title
        plt.show()

    def plot_average_distance_from_origin(self):
        """
        Plots the average distance from the origin for all walkers.
        """
        # Iterate over each walker's average distance from origin
        for walker_name, average_distance in self.statistics.calculate_average_distance_from_origin().items():
            plt.plot(average_distance, label=walker_name)
        plt.legend()
        plt.title('Average Distance From Origin')  # Add title
        plt.xlabel('Number of Steps')  # Add x-axis label
        plt.ylabel('Distance from Origin')  # Add y-axis label
        plt.show()

    def plot_distances_from_axis(self, axis='X'):
        """
        Plots the distances from a specified axis for all walkers.

        Parameters
        ----------
        axis : str
            the axis from which distances are calculated ('X' or 'Y')
        """
        # Iterate over each walker's distances from the specified axis
        for walker_name, distances in self.statistics.calculate_distances_from_axis(axis).items():
            plt.plot(distances, label=walker_name)
        plt.legend()
        plt.title(f'Distances From {axis} Axis')  # Add title
        plt.xlabel('Number of Steps')  # Add x-axis label
        plt.ylabel(f'Distance from {axis} Axis')  # Add y-axis label
        plt.show()

    def plot_escape_radius_10(self):
        """
        Plots the escape radius for all walkers.
        """
        plt.figure(figsize=(10, 6))  # Increase figure size
        # Iterate over each walker's escape radius statistics
        for walker_name, stats in self.statistics.calculate_escape_radius_10().items():
            # Replace None with a default value
            average = stats['average'] if stats['average'] is not None else 0
            plt.bar(walker_name, average, label=walker_name)
            plt.annotate(f"Didn't escape: {stats['zero_count']} out of {self.statistics.get_total_simulations}",
                         (walker_name, average),
                         textcoords="offset points",
                         xytext=(0, 0),  # Adjust the position of the annotation
                         ha='center')

        # Wrap x-axis labels
        plt.xticks([i for i in range(len(self.statistics.calculate_escape_radius_10().items()))],
                   [textwrap.fill(name, 10) for name in self.statistics.calculate_escape_radius_10().keys()],
                   fontsize=5)

        plt.legend()
        plt.title('Escape Radius 10')  # Add title
        plt.ylabel('Amount of Steps')
        plt.tight_layout()  # Adjust layout to fit everything nicely
        plt.show()

    def plot_average_passed_y(self):
        """
        Plots the average number of times each walker crossed the Y axis.
        """
        # Iterate over each walker's average number of times crossing the Y axis
        for walker_name, averages in self.statistics.calculate_average_passed_y().items():
            plt.plot(averages, label=walker_name)
        plt.legend()
        plt.title('Average Passed Y')  # Add title
        plt.xlabel('Number of Steps')  # Add x-axis label
        plt.ylabel('Number of Times Crossed Y Axis')  # Add y-axis label
        plt.show()