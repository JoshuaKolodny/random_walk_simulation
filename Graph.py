from typing import Dict
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore
from my_statistics import Statistics
import pandas as pd
import textwrap
from obstacles_and_barriers import Barrier2D
from portal_gate import PortalGate


class Graph:
    def __init__(self, statistics: Statistics, barriers: Dict[str, Barrier2D], portal_gates: Dict[str, PortalGate]):
        """
        Initialize the Graph class.

        Args:
            statistics (Statistics): The statistics object.
            barriers (Dict): The barrier's dictionary.
            portal_gates (Dict): The portal gates dictionary.
        """
        self.statistics = statistics
        self.barriers = barriers
        self.portal_gates = portal_gates
        # Set the default seaborn theme
        sns.set_theme()

    def plot_barriers(self):
        """
        Plot barriers with a solid color fill.
        """
        for barrier in self.barriers.values():
            # Extract barrier coordinates
            min_x, min_y, max_x, max_y = barrier.bounds.bounds()

            # Calculate width and height
            width = max_x - min_x
            height = max_y - min_y

            # Plot the barrier rectangle
            plt.fill([min_x, min_x + width, min_x + width, min_x], [min_y, min_y, min_y + height, min_y + height],
                     color='red', alpha=0.5)

    def plot_portal_gates(self):
        """
        Plot portal gates with a solid color fill and an arrow.
        """
        for portal_gate in self.portal_gates.values():
            # Extract portal gate coordinates
            min_x, min_y, max_x, max_y = portal_gate.bounds.bounds()

            # Calculate width and height
            width = max_x - min_x
            height = max_y - min_y

            # Plot the portal gate rectangle
            plt.fill([min_x, min_x + width, min_x + width, min_x], [min_y, min_y, min_y + height, min_y + height],
                     color='green', alpha=0.5)

            # Extract destination coordinates
            dest_x, dest_y, _ = portal_gate.destination

            # Calculate portal gate center
            center_x = (max_x + min_x) / 2
            center_y = (max_y + min_y) / 2

            # Plot the arrow from the portal gate to its destination
            plt.arrow(center_x, center_y, dest_x - center_x, dest_y - center_y, color='green',
                      length_includes_head=True, head_width=0.5)

    def plot_single_simulation(self):
        """
        Plot the first simulation that the user ran.
        """
        # Get the first simulation name
        first_simulation_name = list(next(iter(self.statistics.simulations.values())).keys())[0]

        plt.figure(figsize=(8, 6))
        for walker_name, walker_data in self.statistics.simulations.items():
            if walker_name not in ['barriers', 'portal_gates']:
                first_simulation_walker_data = walker_data[first_simulation_name]
                walker_locations = first_simulation_walker_data['locations']
                # Plotting the X and Y coordinates by elements in first column being X and second column Y
                plt.plot(walker_locations[:, 0], walker_locations[:, 1], label=walker_name)

        # Call the plot_barriers function
        self.plot_barriers()

        # Call the plot_portal_gates function
        self.plot_portal_gates()

        plt.legend()
        plt.title('Walker Positions (First Simulation)')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.show()

    def plot_average_distance_from_origin(self):
        """
        Plot the average distance from origin.
        """
        for walker_name, average_distance in self.statistics.calculate_average_distance_from_origin().items():
            sns.lineplot(data=average_distance, label=walker_name)
        plt.legend()
        plt.title('Average Distance From Origin')
        plt.xlabel('Number of Steps')
        plt.ylabel('Distance from Origin')
        plt.show()

    def plot_distances_from_axis(self, axis='X'):
        """
        Plot the distances from the specified axis.

        Args:
            axis (str): The axis to calculate distances from. Default is 'X'.
        """
        for walker_name, distances in self.statistics.calculate_distances_from_axis(axis).items():
            sns.lineplot(data=distances, label=walker_name)
        plt.legend()
        plt.title(f'Distances From {axis} Axis')
        plt.xlabel('Number of Steps')
        plt.ylabel(f'Distance from {axis} Axis')
        plt.show()

    def plot_escape_radius_10(self):
        """
        Plot the escape radius 10 statistics.
        """
        data = []
        for walker_name, stats in self.statistics.calculate_escape_radius_10().items():
            average = stats['average'] if stats['average'] is not None else 0
            data.append({'walker_name': walker_name, 'average': average, 'zero_count': stats['zero_count']})

        df = pd.DataFrame(data)

        plt.figure(figsize=(10, 6))
        sns.barplot(x='walker_name', y='average', data=df, hue='walker_name', dodge=False)

        for i, row in df.iterrows():
            plt.annotate(f"No escape: {row['zero_count']} / {self.statistics.get_total_simulations}",
                         (i, row['average']),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')

        plt.title('Escape Radius 10')
        plt.ylabel('Amount of Steps')
        plt.xlabel('Walker Names')
        ax = plt.gca()
        ax.set_xticks(range(len(df['walker_name'])))
        ax.set_xticklabels(['\n'.join(textwrap.wrap(name, 10)) for name in df['walker_name']])

        plt.tight_layout()
        plt.show()

    def plot_average_passed_y(self):
        """
        Plot the average amount of times each walker passed the Y axis.
        """
        for walker_name, averages in self.statistics.calculate_average_passed_y().items():
            sns.lineplot(data=averages, label=walker_name)
        plt.legend()
        plt.title('Average Passed Y')
        plt.xlabel('Number of Steps')
        plt.ylabel('Number of Times Crossed Y Axis')
        plt.show()

    def plot_lead_counts(self):
        """
        Plot the average amount of times each walker lead per simulation meaning was furthest from origin.
        """
        # Get the average lead counts
        average_leads = self.statistics.calculate_average_leads()

        # Convert the average lead counts to a DataFrame
        df = pd.DataFrame(list(average_leads.items()), columns=['Walker Name', 'Average Lead Count'])

        # Create the bar plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Walker Name', y='Average Lead Count', data=df, hue='Walker Name', dodge=False)
        plt.title('Average Lead Count Per Simulation')
        plt.ylabel('Number of steps in lead')
        ax = plt.gca()
        ax.set_xticks(range(len(df['Walker Name'])))
        ax.set_xticklabels(['\n'.join(textwrap.wrap(name, 10)) for name in df['Walker Name']])
        plt.xlabel('Walker Name')
        plt.show()
