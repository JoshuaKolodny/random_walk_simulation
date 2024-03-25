import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore
from my_statistics import Statistics
import pandas as pd
import textwrap


class Graph:
    def __init__(self, statistics: Statistics):
        self.statistics = statistics
        # Set the default seaborn theme
        sns.set_theme()

    def plot_single_simulation(self):
        # Get the first simulation name
        first_simulation_name = list(next(iter(self.statistics.simulations.values())).keys())[0]

        plt.figure(figsize=(8, 6))
        for walker_name, walker_data in self.statistics.simulations.items():
            if walker_name not in ['barriers', 'portal_gates']:
                first_simulation_walker_data = walker_data[first_simulation_name]
                walker_locations = first_simulation_walker_data['locations']

                plt.plot(walker_locations[:, 0], walker_locations[:, 1], label=walker_name)

        # Plot barriers with a solid color fill
        if 'barriers' in self.statistics.simulations:
            for barrier in self.statistics.simulations['barriers'].values():
                # Define the corners of the barrier
                barrier_corners = [
                    (barrier.x, barrier.y),  # Bottom left
                    (barrier.x + barrier.width, barrier.y),  # Bottom right
                    (barrier.x + barrier.width, barrier.y + barrier.height),  # Top right
                    (barrier.x, barrier.y + barrier.height)  # Top left
                ]
                # Extract the x and y coordinates
                xs, ys = zip(*barrier_corners)
                plt.fill(xs, ys, color='red')

        # Plot portal gates with a solid color fill
        if 'portal_gates' in self.statistics.simulations:
            for portal_gate in self.statistics.simulations['portal_gates'].values():
                # Define the corners of the portal gate
                portal_gate_corners = [
                    (portal_gate.x, portal_gate.y),  # Bottom left
                    (portal_gate.x + portal_gate.width, portal_gate.y),  # Bottom right
                    (portal_gate.x + portal_gate.width, portal_gate.y + portal_gate.height),  # Top right
                    (portal_gate.x, portal_gate.y + portal_gate.height)  # Top left
                ]
                # Extract the x and y coordinates
                xs, ys = zip(*portal_gate_corners)
                plt.fill(xs, ys, color='green')
                plt.arrow(portal_gate.x, portal_gate.y, portal_gate.dest_x - portal_gate.x,
                          portal_gate.dest_y - portal_gate.y,
                          color='green', length_includes_head=True, head_width=0.5)

        plt.legend()
        plt.title('Walker Positions (First Simulation)')
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
        sns.barplot(x='Walker Name', y='Average Lead Count', data=df, hue='Walker Name', dodge=False)
        plt.title('Average Lead Count Per Simulation')
        plt.ylabel('Number of steps in lead')
        ax = plt.gca()
        ax.set_xticks(range(len(df['Walker Name'])))
        ax.set_xticklabels(['\n'.join(textwrap.wrap(name, 10)) for name in df['Walker Name']])
        plt.xlabel('Walker Name')
        plt.show()
