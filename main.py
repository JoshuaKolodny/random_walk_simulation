import json
import simulation_loader
from Walker.discrete_step_walker import DiscreteStepWalker
from Walker.no_repeat_walker import NoRepeatWalker
from Walker.one_unit_random_walker import OneUnitRandomWalker
from Walker.biased_walker import BiasedWalker
from Walker.random_step_walker import RandomStepWalker
from obstacles_and_barriers import Barrier2D
from portal_gate import *
from simulation import Simulation
from my_statistics import Statistics
from Graph import Graph
import argparse

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

    def setup_simulation(self, filename):
        # Load the simulation parameters from the JSON file
        try:
            simulation_parameters = simulation_loader.load_from_json(filename)
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")
            return
        except json.JSONDecodeError:
            print(f"Error: The file {filename} is not a valid JSON file.")
            return

        # Check if the JSON file contains all the required parameters
        required_parameters = ['walkers', 'num_simulations', 'num_steps']
        if not all(param in simulation_parameters for param in required_parameters):
            print(f"Error: The file {filename} does not contain all the required parameters.")
            return

        # Extract walkers and their parameters from simulation_parameters
        walkers = simulation_parameters['walkers']

        # Create instances of walkers and add them to the simulation
        for walker_type, walker_info in walkers.items():
            for walker_name, walker_params in walker_info.items():
                if 'count' not in walker_params:
                    print(f"Error: Walker parameters for {walker_name} does not contain 'count'.")
                    continue
                count = walker_params.pop('count')  # Number of walkers of this type to add
                for _ in range(count):
                    try:
                        # Create a new walker of the specified type
                        if walker_type == 'BiasedWalker':
                            walker = BiasedWalker(**walker_params)
                        elif walker_type == 'OneUnitRandomWalker':
                            walker = OneUnitRandomWalker()
                        elif walker_type == 'DiscreteStepWalker':
                            walker = DiscreteStepWalker()
                        elif walker_type == 'RandomStepWalker':
                            walker = RandomStepWalker()
                        elif walker_type == 'NoRepeatWalker':
                            walker = NoRepeatWalker()
                        else:
                            continue
                        self.simulation.add_walker(walker)  # Add the walker to the simulation
                    except TypeError as e:
                        print(
                            f"Error: Failed to create a walker of type {walker_type} with parameters {walker_params}. {e}")
                        continue

        # Extract barriers and portal gates from simulation_parameters
        barriers = simulation_parameters.get('barriers', {})
        portal_gates = simulation_parameters.get('portal_gates', {})

        # Add barriers and portal gates to the simulation
        for barrier_name, barrier_params in barriers.items():
            try:
                barrier = Barrier2D(**barrier_params)  # Create a new Barrier2D object
                self.simulation.add_barrier(barrier_name, barrier)  # Add the barrier to the simulation
            except TypeError as e:
                print(f"Error: Failed to create a barrier with parameters {barrier_params}. {e}")
                continue

        for portal_gate_name, portal_gate_params in portal_gates.items():
            try:
                portal_gate = PortalGate(**portal_gate_params)  # Create a new PortalGate object
                self.simulation.add_portal_gate(portal_gate_name, portal_gate)  # Add the portal gate to the simulation
            except TypeError as e:
                print(f"Error: Failed to create a portal gate with parameters {portal_gate_params}. {e}")
                continue

        return simulation_parameters['num_simulations'], simulation_parameters['num_steps']

    def run_simulation(self, num_simulations, num_steps, json_path='stats.json'):
        self.statistics.num_of_steps = num_steps
        # Run the simulation for the specified number of steps and simulations
        for i in range(1, num_simulations + 1):
            self.simulation.simulate(num_steps)
            self.statistics.add_simulation(f"Simulation {i}", self.simulation)  # Add the simulation to the statistics
            self.simulation.reset()  # Reset the simulation for the next run

        # Calculate statistics
        self.statistics.calculate_average_locations_per_cell()
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
            stats_exporter.save_to_json(json_path)  # Save the statistics to a JSON file
        except PermissionError:
            print(f"Error: Cannot write to the file {json_path}. Check your permissions.")
            return
        except FileNotFoundError:
            print(f"Error: The directory to save the statistics does not exist.")
            return

        # Plot graphs
        g = Graph(self.statistics)  # Initialize a new Graph object
        g.plot_single_simulation()  # Plot the first simulation
        g.plot_average_distance_from_origin()
        g.plot_distances_from_axis(axis='X')
        g.plot_distances_from_axis(axis='Y')
        g.plot_escape_radius_10()
        g.plot_average_passed_y()
        g.plot_lead_counts()

        # Resets simulation runner parameters entirely
        self.simulation = Simulation()
        self.statistics =Statistics()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the simulation.')
    parser.add_argument('parameters_path', type=str, help='The path to the parameters JSON file.')
    parser.add_argument('stats_path', type=str, help='The path where the statistics JSON file will be saved.')
    args = parser.parse_args()

    runner = SimulationRunner()  # Initialize a new SimulationRunner object
    num_simulations, num_steps = runner.setup_simulation(args.parameters_path)
    runner.run_simulation(num_simulations, num_steps, args.stats_path)  # Run the simulation

