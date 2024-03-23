import matplotlib.pyplot as plt
import seaborn as sns
from my_statistics import Statistics
import pandas as pd
import textwrap

class Graph:
    def __init__(self, statistics: Statistics):
        self.statistics = statistics
        # Set the default seaborn theme
        sns.set_theme()

    def plot_single_simulation(self, simulation):
        for walker_name, walker_info in simulation.walkers.items():
            positions = walker_info[1]
            x_positions = [pos[0] for pos in positions]
            y_positions = [pos[1] for pos in positions]
            sns.scatterplot(x=x_positions, y=y_positions, label=walker_name)
        plt.legend()
        plt.title('Walker Positions')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.show()

    def plot_average_locations_per_cell(self):
        for walker_name, average_locations in self.statistics.calculate_average_locations_per_cell().items():
            sns.lineplot(data=average_locations, label=walker_name)
        plt.legend()
        plt.title('Average Locations Per Cell')
        plt.show()

    def plot_average_distance_from_origin(self):
        for walker_name, average_distance in self.statistics.calculate_average_distance_from_origin().items():
            sns.lineplot(data=average_distance, label=walker_name)
        plt.legend()
        plt.title('Average Distance From Origin')
        plt.xlabel('Number of Steps')
        plt.ylabel('Distance from Origin')
        plt.show()

    def plot_distances_from_axis(self, axis='X'):
        for walker_name, distances in self.statistics.calculate_distances_from_axis(axis).items():
            sns.lineplot(data=distances, label=walker_name)
        plt.legend()
        plt.title(f'Distances From {axis} Axis')
        plt.xlabel('Number of Steps')
        plt.ylabel(f'Distance from {axis} Axis')
        plt.show()

    def plot_escape_radius_10(self):
        data = []
        for walker_name, stats in self.statistics.calculate_escape_radius_10().items():
            average = stats['average'] if stats['average'] is not None else 0
            data.append({'walker_name': walker_name, 'average': average, 'zero_count': stats['zero_count']})

        df = pd.DataFrame(data)

        plt.figure(figsize=(10, 6))
        sns.barplot(x='walker_name', y='average', data=df)

        for i, row in df.iterrows():
            plt.annotate(f"No escape: {row['zero_count']} / {self.statistics.get_total_simulations}",
                         (i, row['average']),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')

        # plt.legend(title='Walker Names', title_fontsize='13', fontsize='10')
        plt.title('Escape Radius 10')
        plt.ylabel('Amount of Steps')
        plt.xlabel('Walker Names')
        plt.tight_layout()
        plt.show()

    def plot_average_passed_y(self):
        for walker_name, averages in self.statistics.calculate_average_passed_y().items():
            sns.lineplot(data=averages, label=walker_name)
        plt.legend()
        plt.title('Average Passed Y')
        plt.xlabel('Number of Steps')
        plt.ylabel('Number of Times Crossed Y Axis')
        plt.show()

    def plot_lead_counts(self):
        # Get the average lead counts
        average_leads = self.statistics.calculate_average_leads()

        # Convert the average lead counts to a DataFrame
        df = pd.DataFrame(list(average_leads.items()), columns=['Walker Name', 'Average Lead Count'])

        # Create the bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Walker Name', y='Average Lead Count', data=df)
        plt.title('Average Lead Count Per Simulation')
        plt.xlabel('Walker Name')
        plt.ylabel('Average Lead Count')
        plt.show()