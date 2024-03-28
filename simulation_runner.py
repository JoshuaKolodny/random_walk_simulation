from portal_gate import *
from simulation import Simulation
from my_statistics import Statistics
from Graph import Graph
from statistics_exporter import StatisticsExporter


class SimulationRunner:
    """
    A class used to run a simulation from the configuration file.

    ...

    Attributes
    ----------
    simulation : Simulation
        an instance of the Simulation class which contains the simulation to be run
    statistics : Statistics
        an instance of the Statistics class which contains the statistics of the simulation

    Methods
    -------
    run():
        Runs the simulation.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the SimulationRunner object.
        """
        self.simulation = Simulation()  # Initialize a new Simulation object
        self.statistics = Statistics()  # Initialize a new Statistics object

    def run_simulation(self, num_simulations: int, num_steps: int, json_path: Optional[str] = 'stats.json'):
        """
        Runs the simulation for a specified number of steps and simulations, calculates statistics, saves the statistics to a JSON file, and plots graphs.

        Args:
            num_simulations (int): The number of simulations to run.
            num_steps (int): The number of steps per simulation.
            json_path (str, optional): The path to the JSON file to save the statistics to. Defaults to 'stats.json'.
        """
        self.statistics.num_of_steps = num_steps
        barriers_dict = self.simulation.barriers
        portal_gates_dict = self.simulation.portal_gates
        # Run the simulation for the specified number of steps and simulations
        for i in range(1, num_simulations + 1):
            self.simulation.simulate(num_steps)
            self.statistics.add_simulation(f"Simulation {i}", self.simulation)  # Add the simulation to the statistics
            self.simulation.reset()  # Reset the simulation for the next run

        # Calculate statistics
        self.statistics.calculate_average_locations_per_step()
        average_distance_from_origin = self.statistics.calculate_average_distance_from_origin()
        distances_from_axis_x = self.statistics.calculate_distances_from_axis(axis='Y')
        distances_from_axis_y = self.statistics.calculate_distances_from_axis(axis='X')
        escape_radius_10_stats = self.statistics.calculate_escape_radius_10()
        passed_y_stats = self.statistics.calculate_average_passed_y()
        average_lead_count = self.statistics.calculate_average_leads()

        # Save statistics to JSON file
        stats_exporter = StatisticsExporter()  # Initialize a new StatisticsExporter object
        stats_exporter.add_data('average_distance_from_origin', average_distance_from_origin)
        stats_exporter.add_data('distances_from_axis_x', distances_from_axis_x)
        stats_exporter.add_data('distances_from_axis_y', distances_from_axis_y)
        stats_exporter.add_data('escape_radius_10_stats', escape_radius_10_stats)
        stats_exporter.add_data('passed_y_stats', passed_y_stats)
        stats_exporter.add_data('average lead count', average_lead_count)
        try:
            if json_path is None:
                raise ValueError("json_path cannot be None")
            stats_exporter.save_to_json(json_path)  # Save the statistics to a JSON file
        except PermissionError:
            print(f"Error: Cannot write to the file {json_path}. Check your permissions.")
            return
        except FileNotFoundError:
            print(f"Error: The directory to save the statistics does not exist.")
            return
        except ValueError as e:
            print(e)
            return

        # Plot graphs
        g = Graph(self.statistics, barriers_dict, portal_gates_dict)  # Initialize a new Graph object
        g.plot_single_simulation()  # Plot the first simulation
        g.plot_average_distance_from_origin()
        g.plot_distances_from_axis(axis='X')
        g.plot_distances_from_axis(axis='Y')
        g.plot_escape_radius_10()
        g.plot_average_passed_y()
        g.plot_lead_counts()

        # Resets simulation runner parameters entirely
        self.simulation = Simulation()
        self.statistics = Statistics()
