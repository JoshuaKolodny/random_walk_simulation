import json
import simulation_loader
from Walker.discrete_step_walker import DiscreteStepWalker
from Walker.one_unit_random_walker import OneUnitRandomWalker
from Walker.biased_walker import BiasedWalker
from Walker.random_step_walker import RandomStepWalker
from portal_gate import *
from simulation import Simulation
from statistics import Statistics
from Graph import Graph
import argparse

from statistics_exporter import StatisticsExporter


class SimulationRunner:
    def __init__(self):
        self.simulation = Simulation()
        self.statistics = Statistics()

    def run(self):
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Run a simulation.')
        parser.add_argument('filename', type=str,
                            help='The name of the JSON file containing the simulation parameters.')
        parser.add_argument('stats_path', type=str,
                            help='The path to save the statistics.')
        args = parser.parse_args()

        try:
            simulation_parameters = simulation_loader.load_from_json(args.filename)
        except FileNotFoundError:
            print(f"Error: The file {args.filename} does not exist.")
            return
        except json.JSONDecodeError:
            print(f"Error: The file {args.filename} is not a valid JSON file.")
            return

        required_parameters = ['walkers', 'num_simulations', 'num_steps']
        if not all(param in simulation_parameters for param in required_parameters):
            print(f"Error: The file {args.filename} does not contain all the required parameters.")
            return

        num_simulations = simulation_parameters['num_simulations']
        num_steps = simulation_parameters['num_steps']

        # Extract walkers and their parameters from simulation_parameters
        walkers = simulation_parameters['walkers']

        # Create instances of walkers and add them to the simulation
        for walker_type, walker_info in walkers.items():
            for walker_name, walker_params in walker_info.items():
                if 'count' not in walker_params:
                    print(f"Error: Walker parameters for {walker_name} does not contain 'count'.")
                    continue
                count = walker_params.pop('count')
                for _ in range(count):
                    try:
                        if walker_type == 'BiasedWalker':
                            walker = BiasedWalker(**walker_params)
                        elif walker_type == 'OneUnitRandomWalker':
                            walker = OneUnitRandomWalker()
                        elif walker_type == 'DiscreteStepWalker':
                            walker = DiscreteStepWalker()
                        elif walker_type == 'RandomStepWalker':
                            walker = RandomStepWalker()
                        else:
                            continue
                        self.simulation.add_walker(walker)
                    except TypeError as e:
                        print(
                            f"Error: Failed to create a walker of type {walker_type} with parameters {walker_params}. {e}")
                        continue
                    self.simulation.add_walker(walker)

        # Extract barriers and portal gates from simulation_parameters
        barriers = simulation_parameters.get('barriers', {})
        portal_gates = simulation_parameters.get('portal_gates', {})

        # Add barriers and portal gates to the simulation
        for barrier_name, barrier_params in barriers.items():
            try:
                barrier = Barrier2D(**barrier_params)
                self.simulation.add_barrier(barrier_name, barrier)
            except TypeError as e:
                print(f"Error: Failed to create a barrier with parameters {barrier_params}. {e}")
                continue

        for portal_gate_name, portal_gate_params in portal_gates.items():
            try:
                portal_gate = PortalGate(**portal_gate_params)
                self.simulation.add_portal_gate(portal_gate_name, portal_gate)
            except TypeError as e:
                print(f"Error: Failed to create a portal gate with parameters {portal_gate_params}. {e}")
                continue

        for i in range(1, num_simulations + 1):
            self.simulation.simulate(num_steps)
            self.statistics.add_simulation(f"Simulation {i}", self.simulation)
            self.simulation.reset()

        # Calculate statistics
        self.statistics.calculate_average_locations_per_cell()
        average_distance_from_origin = self.statistics.calculate_average_distance_from_origin()
        distances_from_axis_x = self.statistics.calculate_distances_from_axis(axis='Y')
        distances_from_axis_y = self.statistics.calculate_distances_from_axis(axis='X')
        escape_radius_10_stats = self.statistics.calculate_escape_radius_10()
        passed_y_stats = self.statistics.calculate_average_passed_y()

        # Save statistics to JSON file
        stats_exporter = StatisticsExporter()
        stats_exporter.add_data('average_distance_from_origin', average_distance_from_origin)
        stats_exporter.add_data('distances_from_axis_x', distances_from_axis_x)
        stats_exporter.add_data('distances_from_axis_y', distances_from_axis_y)
        stats_exporter.add_data('escape_radius_10_stats', escape_radius_10_stats)
        stats_exporter.add_data('passed_y_stats', passed_y_stats)
        try:
            stats_exporter.save_to_json(args.stats_path)
        except PermissionError:
            print(f"Error: Cannot write to the file {args.stats_path}. Check your permissions.")
            return
        except FileNotFoundError:
            print(f"Error: The directory to save the statistics does not exist.")
            return

        # Plot graphs
        g = Graph(self.statistics)
        g.plot_average_locations_per_cell()
        g.plot_average_distance_from_origin()
        g.plot_distances_from_axis(axis='X')
        g.plot_distances_from_axis(axis='Y')
        g.plot_escape_radius_10()
        g.plot_average_passed_y()

        # self.statistics= Statistics()
        # g1 = Graph(self.statistics)
        #
        # # Run simulation for 10 steps
        # for i in range(1, 10):
        #     self.simulation.simulate(100)
        #     self.statistics.add_simulation(f"Simulation {i}", self.simulation)
        #
        #     # Plot the positions of the walkers after each simulation run
        #     g1.plot_single_simulation(self.simulation)
        #
        #     self.simulation.reset()


if __name__ == '__main__':
    runner = SimulationRunner()
    runner.run()
