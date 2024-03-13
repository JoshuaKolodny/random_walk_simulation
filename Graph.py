import matplotlib.pyplot as plt
from statistics import Statistics

class Graph:
    def __init__(self, statistics: Statistics):
        self.statistics = statistics

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
        plt.show()

    def plot_distances_from_axis(self, axis='X'):
        for walker_name, distances in self.statistics.calculate_distances_from_axis(axis).items():
            plt.plot(distances, label=walker_name)
        plt.legend()
        plt.title(f'Distances From {axis} Axis')  # Add title
        plt.show()

    def plot_escape_radius_10(self):
        for walker_name, stats in self.statistics.calculate_escape_radius_10().items():
            plt.bar(walker_name, stats['average'], label='Average steps to escape')
            plt.bar(walker_name, stats['zero_count'], label='Count of not escaping')
        plt.legend()
        plt.title('Escape Radius 10')  # Add title
        plt.show()

    def plot_average_passed_y(self):
        for walker_name, averages in self.statistics.calculate_average_passed_y().items():
            plt.plot(averages, label=walker_name)
        plt.legend()
        plt.title('Average Passed Y')  # Add title
        plt.show()