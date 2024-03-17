import matplotlib.pyplot as plt
from statistics import Statistics
import textwrap


class Graph:
    def __init__(self, statistics: Statistics):
        self.statistics = statistics

    def plot_single_simulation(self, simulation):
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
        for walker_name, average_locations in self.statistics.calculate_average_locations_per_cell().items():
            plt.plot(average_locations, label=walker_name)
        plt.legend()
        plt.title('Average Locations Per Cell')  # Add title
        plt.show()

    def plot_average_distance_from_origin(self):
        for walker_name, average_distance in self.statistics.calculate_average_distance_from_origin().items():
            plt.plot(average_distance, label=walker_name)
        plt.legend()
        plt.title('Average Distance From Origin')  # Add title
        plt.xlabel('Number of Steps')  # Add x-axis label
        plt.ylabel('Distance from Origin')  # Add y-axis label
        plt.show()

    def plot_distances_from_axis(self, axis='X'):
        for walker_name, distances in self.statistics.calculate_distances_from_axis(axis).items():
            plt.plot(distances, label=walker_name)
        plt.legend()
        plt.title(f'Distances From {axis} Axis')  # Add title
        plt.xlabel('Number of Steps')  # Add x-axis label
        plt.ylabel(f'Distance from {axis} Axis')  # Add y-axis label
        plt.show()

    def plot_escape_radius_10(self):
        plt.figure(figsize=(10, 6))  # Increase figure size
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
        for walker_name, averages in self.statistics.calculate_average_passed_y().items():
            plt.plot(averages, label=walker_name)
        plt.legend()
        plt.title('Average Passed Y')  # Add title
        plt.xlabel('Number of Steps')  # Add x-axis label
        plt.ylabel('Number of Times Crossed Y Axis')  # Add y-axis label
        plt.show()
