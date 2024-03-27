import tkinter
from simulation_gui import SimulationGUI  # Import the SimulationGUI class
from simulation_gui import SimulationController


if __name__ == '__main__':
    controller = SimulationController()  # Create an instance of the SimulationController class
    root = tkinter.Tk()  # Create a root window
    controller.view = SimulationGUI(root, controller)  # Create an instance of the SimulationGUI class
    root.mainloop()  # Start the main event loop

    # parser = argparse.ArgumentParser(description='Run the simulation.')
    # parser.add_argument('parameters_path', type=str, help='The path to the parameters JSON file.')
    # parser.add_argument('stats_path', type=str, help='The path where the statistics JSON file will be saved.')
    # args = parser.parse_args()
    #
    # runner = SimulationRunner()  # Initialize a new SimulationRunner object
    # num_simulations, num_steps = runner.setup_simulation(args.parameters_path)
    # runner.run_simulation(num_simulations, num_steps, args.stats_path)  # Run the simulation
    #
