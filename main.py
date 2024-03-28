import tkinter
from simulation_gui import SimulationGUI  # Import the SimulationGUI class
from simulation_gui import SimulationController
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='To run the program write in the command line: python main.py')
    args = parser.parse_args()
    controller = SimulationController()  # Create an instance of the SimulationController class
    root = tkinter.Tk()  # Create a root window
    controller.view = SimulationGUI(root, controller)  # Create an instance of the SimulationGUI class
    root.mainloop()  # Start the main event loop

