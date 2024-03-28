import tkinter
from simulation_gui import SimulationGUI
from simulation_gui import SimulationController
import argparse


if __name__ == '__main__':
    # Create a parser for command-line options, arguments and sub-commands
    parser = argparse.ArgumentParser(description='To run the program write in the command line: python main.py')
    # Parse the arguments passed to the script
    args = parser.parse_args()
    # Create an instance of the SimulationController class
    controller = SimulationController()
    # Create a root window using tkinter
    root = tkinter.Tk()
    # Create an instance of the SimulationGUI class and assign it to the view attribute of the controller
    controller.view = SimulationGUI(root, controller)
    # Start the main event loop of tkinter
    root.mainloop()

