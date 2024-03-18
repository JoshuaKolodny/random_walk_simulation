import tkinter as tk
from tkinter import messagebox, ttk
from main import *


class SimulationGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Simulation Parameters")
        self.root.geometry("500x600")  # Set the size of the window to 400x300
        # self.root.resizable(False, False)  # Prevent the window from being resizable

        # Configure the grid to expand to fill the available space
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self._create_walker_selection()
        self._create_walker_table()
        self._create_simulation_parameters()
        self._create_simulation_buttons()

        # Call update_walker_parameters to add self.biased_walker_frame to the grid
        self.update_walker_parameters()

    def _create_walker_selection(self):
        self.walker_frame = tk.Frame(self.root)
        self.walker_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)

        # Configure the grid to expand to fill the available space
        self.walker_frame.grid_columnconfigure(0, weight=1)
        self.walker_frame.grid_rowconfigure(0, weight=1)
        tk.Label(self.walker_frame, text="Walker Type:").grid(row=0, padx=5, pady=5)

        self.walker_type_var = tk.StringVar()  # Create a StringVar
        self.walker_type_var.trace('w', self.update_walker_parameters)  # Use trace on the StringVar

        self.walker_type = ttk.Combobox(self.walker_frame,
                                        values=['BiasedWalker', 'OneUnitRandomWalker', 'DiscreteStepWalker',
                                                'RandomStepWalker'], state='readonly',
                                        textvariable=self.walker_type_var)
        tk.Label(self.walker_frame, text="Select Walker Type:").grid(row=0, column=0, padx=5, pady=5)
        self.walker_type.grid(row=0, column=1, padx=5, pady=5)

        # BiasedWalker parameters
        self.biased_walker_frame = tk.Frame(self.walker_frame)
        self.biased_walker_frame.grid(row=1, column=0, columnspan=2, rowspan=2, sticky=tk.W + tk.E + tk.N + tk.S)

        # Configure the grid to expand to fill the available space
        self.biased_walker_frame.grid_columnconfigure(0, weight=1)
        self.biased_walker_frame.grid_rowconfigure(0, weight=1)

        self.up_prob = tk.Entry(self.biased_walker_frame)
        self.down_prob = tk.Entry(self.biased_walker_frame)
        self.left_prob = tk.Entry(self.biased_walker_frame)
        self.right_prob = tk.Entry(self.biased_walker_frame)
        self.to_origin_prob = tk.Entry(self.biased_walker_frame)

        tk.Label(self.walker_frame, text="Walker Count:").grid(row=2, padx=5, pady=5)
        vcmd = (self.root.register(self.validate_walker_count), '%P')
        self.walker_count = tk.Entry(self.walker_frame, validate='key', validatecommand=vcmd)
        self.walker_count.grid(row=2, column=1, padx=5, pady=5)

        self.add_walker_button = tk.Button(self.walker_frame, text="Add Walker", command=self.add_walker)
        self.add_walker_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def update_walker_parameters(self, *args):
        walker_type = self.walker_type.get()

        if walker_type == 'BiasedWalker':
            tk.Label(self.biased_walker_frame, text="Up Probability:").grid(row=0, column=0)
            self.up_prob.grid(row=0, column=1)
            tk.Label(self.biased_walker_frame, text="Down Probability:").grid(row=0, column=2)
            self.down_prob.grid(row=0, column=3)
            tk.Label(self.biased_walker_frame, text="Left Probability:").grid(row=0, column=4)
            self.left_prob.grid(row=0, column=5)
            tk.Label(self.biased_walker_frame, text="Right Probability:").grid(row=0, column=6)
            self.right_prob.grid(row=0, column=7)
            tk.Label(self.biased_walker_frame, text="To Origin Probability:").grid(row=0, column=8)
            self.to_origin_prob.grid(row=0, column=9)
        else:
            for widget in self.biased_walker_frame.winfo_children():
                widget.grid_remove()

    def _create_walker_table(self):
        self.walker_table = ttk.Treeview(self.walker_frame, columns=('Type', 'Count'), show='headings')
        self.walker_table.heading('Type', text='Walker Type')
        self.walker_table.heading('Count', text='Walker Count')
        self.walker_table.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Create a new frame for the button and the label
        self.button_label_frame = tk.Frame(self.walker_frame)
        self.button_label_frame.grid(row=7, column=0, columnspan=2)  # Center the frame

        self.remove_walker_button = tk.Button(self.button_label_frame, text="Remove Walker", command=self.remove_walker)
        self.remove_walker_button.grid(row=0, column=0, padx=5, pady=5)  # Add spacing

        # Add the walker count label to the new frame
        self.walker_count_label = tk.Label(self.button_label_frame, text="Total Walkers: 0")
        self.walker_count_label.grid(row=0, column=1, padx=5, pady=5)  # Add spacing the "Remove Walker" button

    def _create_simulation_parameters(self):
        self.simulation_frame = tk.Frame(self.root)
        self.simulation_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=20)  # Increase pady to raise the frame

        tk.Label(self.simulation_frame, text="Number of Simulations:").grid(row=0, padx=5, pady=5)
        self.num_simulations = tk.Entry(self.simulation_frame)
        self.num_simulations.insert(0, '20')  # Insert the default value
        self.num_simulations.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.simulation_frame, text="Number of Steps:").grid(row=1, padx=5, pady=5)
        self.num_steps = tk.Entry(self.simulation_frame)
        self.num_steps.insert(0, '500')  # Insert the default value
        self.num_steps.grid(row=1, column=1, padx=5, pady=5)

    def validate_positive_integer(self, input_value):
        if input_value == '':
            return False
        try:
            value = int(input_value)
            if value > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def validate_walker_count(self, new_value):
        if not self.validate_positive_integer(new_value):
            self.walker_count.config(highlightbackground="red")
        else:
            self.walker_count.config(highlightbackground="white")
        return True  # Always return True to accept the input

    def _create_simulation_buttons(self):
        self.run_button = tk.Button(self.simulation_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def add_walker(self):
        walker_type = self.walker_type.get()
        walker_count_str = self.walker_count.get()

        if not walker_type:
            self.show_error("Error", "Please select a walker type!")
            return

        if not self.validate_positive_integer(walker_count_str):
            self.show_error("Error", "Walker count must be a positive integer!")
            return

        if not walker_count_str:
            self.show_error("Error", "Please enter a walker count!")
            return

        try:
            walker_count = int(walker_count_str)
            if not isinstance(walker_count, int) or walker_count <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Error", "Walker count must be a positive integer!")
            return

        if walker_type == 'BiasedWalker':
            if not self.up_prob.get() or not self.down_prob.get() or not self.left_prob.get() or not self.right_prob.get() or not self.to_origin_prob.get():
                self.show_error("Error", "Please enter all probabilities for the Biased Walker!")
                return
            up_prob = float(self.up_prob.get())
            down_prob = float(self.down_prob.get())
            left_prob = float(self.left_prob.get())
            right_prob = float(self.right_prob.get())
            to_origin_prob = float(self.to_origin_prob.get())
            self.controller.add_walker(walker_type, walker_count, up_prob, down_prob, left_prob, right_prob,
                                       to_origin_prob)
        else:
            self.controller.add_walker(walker_type, walker_count)
        self.walker_type.set('')
        self.walker_count.delete(0, 'end')

        # Update the walker table
        for row in self.walker_table.get_children():
            if self.walker_table.item(row)['values'][0] == walker_type:
                self.walker_table.set(row, 'Count', self.controller.walkers[walker_type])
                break
        else:
            self.walker_table.insert('', 'end', values=(walker_type, walker_count))

        # Update the walker count label
        self.update_walker_count_label()

    def remove_walker(self):
        selected_items = self.walker_table.selection()
        for item in selected_items:
            walker_type = self.walker_table.item(item)['values'][0]
            self.controller.remove_walker(walker_type)
            self.walker_table.delete(item)  # Delete the row from the walker table

        # Update the walker count label
        self.update_walker_count_label()

    def update_walker_count_label(self):
        total_walkers = sum(self.controller.walkers.values())
        self.walker_count_label.config(text=f"Total Walkers: {total_walkers}")

    def run_simulation(self):
        num_simulations_str = self.num_simulations.get()
        num_steps_str = self.num_steps.get()

        if not self.validate_positive_integer(num_simulations_str):
            self.show_error("Error", "Number of simulations must be a positive integer!")
            return

        if not self.validate_positive_integer(num_steps_str):
            self.show_error("Error", "Number of steps must be a positive integer!")
            return

        total_walkers = sum(self.controller.walkers.values())
        if total_walkers == 0:
            self.show_error("Error", "There must be at least one walker!")
            return

        num_simulations = int(num_simulations_str)
        num_steps = int(num_steps_str)
        self.controller.run_simulation(num_simulations, num_steps)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)


# Controller
class SimulationController:
    def __init__(self):
        self.model = SimulationRunner()
        self.view = SimulationGUI(tk.Tk(), self)
        self.walkers = {}  # Dictionary to keep track of the walkers added to the simulation

    def add_walker(self, walker_type, walker_count, up_prob=None, down_prob=None, left_prob=None, right_prob=None,
                   to_origin_prob=None):
        for _ in range(walker_count):
            if walker_type == 'BiasedWalker':
                walker = BiasedWalker(up_prob, down_prob, left_prob, right_prob, to_origin_prob)
            elif walker_type == 'OneUnitRandomWalker':
                walker = OneUnitRandomWalker()
            elif walker_type == 'DiscreteStepWalker':
                walker = DiscreteStepWalker()
            elif walker_type == 'RandomStepWalker':
                walker = RandomStepWalker()
            else:
                self.view.show_error("Error", "Invalid walker type! please select a walker")
                return
            self.model.simulation.add_walker(walker)
            self.walkers[walker_type] = self.walkers.get(walker_type, 0) + 1  # Increment the count of the walker type

    def remove_walker(self, walker_type):
        if walker_type in self.walkers:
            # Iterate over a copy of the keys to avoid modifying the dictionary while iterating
            for key in list(self.model.simulation.walkers.keys()):
                if key.startswith(walker_type):
                    self.model.simulation.remove_walker(key)  # Remove the walker from the simulation
            del self.walkers[walker_type]  # Remove the walker type from the dictionary

    def run_simulation(self, num_simulations, num_steps):
        # Run the simulation with the given parameters
        for i in range(num_simulations):
            self.model.simulation.simulate(num_steps)
            self.model.statistics.add_simulation(f"Simulation {i}",
                                                 self.model.simulation)  # Add the simulation to the statistics
            self.model.simulation.reset()  # Reset the simulation for the next run

        # Calculate statistics
        self.model.statistics.calculate_average_locations_per_cell()
        average_distance_from_origin = self.model.statistics.calculate_average_distance_from_origin()
        distances_from_axis_x = self.model.statistics.calculate_distances_from_axis(axis='Y')
        distances_from_axis_y = self.model.statistics.calculate_distances_from_axis(axis='X')
        escape_radius_10_stats = self.model.statistics.calculate_escape_radius_10()
        passed_y_stats = self.model.statistics.calculate_average_passed_y()

        # Save statistics to JSON file
        stats_exporter = StatisticsExporter()  # Initialize a new StatisticsExporter object
        stats_exporter.add_data('average_distance_from_origin', average_distance_from_origin)
        stats_exporter.add_data('distances_from_axis_x', distances_from_axis_x)
        stats_exporter.add_data('distances_from_axis_y', distances_from_axis_y)
        stats_exporter.add_data('escape_radius_10_stats', escape_radius_10_stats)
        stats_exporter.add_data('passed_y_stats', passed_y_stats)
        stats_exporter.save_to_json('stats.json')  # Save the statistics to a JSON file

        # Plot graphs
        g = Graph(self.model.statistics)  # Initialize a new Graph object
        g.plot_average_distance_from_origin()
        g.plot_distances_from_axis(axis='X')
        g.plot_distances_from_axis(axis='Y')
        g.plot_escape_radius_10()
        g.plot_average_passed_y()

        # Show a message box when the simulation is done
        self.view.show_message("Simulation", "Simulation completed!")


if __name__ == "__main__":
    controller = SimulationController()
    controller.view.root.mainloop()
