import simulation_loader
from Walker.discrete_step_walker import DiscreteStepWalker
from Walker.one_unit_random_walker import OneUnitRandomWalker
from Walker.probabilistic_walker import ProbabilisticWalker
from Walker.random_step_walker import RandomStepWalker
from portal_gate import *
from simulation import Simulation
from statistics import Statistics
from Graph import Graph
import argparse

class SimulationRunner:
    def __init__(self):
        self.simulation = Simulation()
        self.statistics = Statistics()

    def run(self):
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Run a simulation.')
        parser.add_argument('filename', type=str,
                            help='The name of the JSON file containing the simulation parameters.')
        args = parser.parse_args()

        simulation_parameters = simulation_loader.load_from_json(args.filename)

        # Extract walkers and their parameters from simulation_parameters
        walkers = simulation_parameters['walkers']

        # Create instances of walkers and add them to the simulation
        for walker_type, walker_info in walkers.items():
            for walker_name, walker_params in walker_info.items():
                count = walker_params.pop('count')
                for _ in range(count):
                    if walker_type == 'ProbabilisticWalker':
                        walker = ProbabilisticWalker(**walker_params)
                    elif walker_type == 'OneUnitRandomWalker':
                        walker = OneUnitRandomWalker()
                    elif walker_type == 'DiscreteStepWalker':
                        walker = DiscreteStepWalker()
                    elif walker_type == 'RandomStepWalker':
                        walker = RandomStepWalker()
                    else:
                        continue
                    self.simulation.add_walker(walker)

        # Extract barriers and portal gates from simulation_parameters
        barriers = simulation_parameters.get('barriers', {})
        portal_gates = simulation_parameters.get('portal_gates', {})

        # Add barriers and portal gates to the simulation
        for barrier_name, barrier_params in barriers.items():
            barrier = Barrier2D(**barrier_params)
            self.simulation.add_barrier(barrier_name, barrier)

        for portal_gate_name, portal_gate_params in portal_gates.items():
            portal_gate = PortalGate(**portal_gate_params)
            self.simulation.add_portal_gate(portal_gate_name, portal_gate)

        num_simulations = simulation_parameters['num_simulations']
        num_steps = simulation_parameters['num_steps']

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