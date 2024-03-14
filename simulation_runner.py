from Walker.discrete_step_walker import DiscreteStepWalker
from Walker.one_unit_random_walker import OneUnitRandomWalker
from Walker.probabilistic_walker import ProbabilisticWalker
from Walker.random_step_walker import RandomStepWalker
from obstacles import *
from simulation import Simulation
from statistics import Statistics
from Graph import Graph

class SimulationRunner:
    def __init__(self):
        self.simulation = Simulation()
        self.statistics = Statistics()

    def run(self):
        # Add some walkers
        walker1 = OneUnitRandomWalker()
        walker2 = DiscreteStepWalker()
        walker3 = ProbabilisticWalker(300, 300, 100, 100, 105)
        walker4 = RandomStepWalker()
        self.simulation.add_walker(walker1)
        self.simulation.add_walker(walker2)
        self.simulation.add_walker(walker3)
        self.simulation.add_walker(walker4)
        obstacle1 = Obstacle2D(3, 3, 2,2)
        obstacle2 = Obstacle2D(-3, -3, 1, 1)
        self.simulation.add_obstacle(type(obstacle1).__name__+'1', obstacle1)
        self.simulation.add_obstacle(type(obstacle2).__name__+'2', obstacle2)

        # Run simulation for 10 steps
        for i in range(1, 100):
            self.simulation.simulate(1000)
            self.statistics.add_simulation(f"Simulation {i}", self.simulation)
            self.simulation.reset()

        # Calculate statistics
        self.statistics.calculate_average_locations_per_cell()
        average_distance_from_origin = self.statistics.calculate_average_distance_from_origin()
        distances_from_axis_x = self.statistics.calculate_distances_from_axis(axis='Y')
        distances_from_axis_y = self.statistics.calculate_distances_from_axis(axis='X')
        escape_radius_10_stats = self.statistics.calculate_escape_radius_10()
        passed_y_stats = self.statistics.calculate_average_passed_y()

        # Print statistics
        # print(average_distance_from_origin)
        # print(distances_from_axis_x)
        # print(distances_from_axis_y)
        # print(escape_radius_10_stats)
        # print(passed_y_stats)

        # Plot graphs
        g = Graph(self.statistics)
        g.plot_average_locations_per_cell()
        g.plot_average_distance_from_origin()
        g.plot_distances_from_axis(axis='X')
        g.plot_distances_from_axis(axis='Y')
        g.plot_escape_radius_10()
        g.plot_average_passed_y()


if __name__ == '__main__':
    runner = SimulationRunner()
    runner.run()