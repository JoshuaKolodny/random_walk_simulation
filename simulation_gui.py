import tkinter as tk
from tkinter import messagebox, ttk
from main import *


class GuiHelper:
    @classmethod
    def create_label_entry_pair(cls, frame, text, row):
        pair_frame = tk.Frame(frame)
        pair_frame.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        label = tk.Label(pair_frame, text=text)
        label.grid(row=0, column=0, sticky=tk.E)

        entry = tk.Entry(pair_frame)
        entry.grid(row=0, column=1, sticky=tk.W)

        pair_frame.grid_columnconfigure(0, weight=1)  # Allow the label to expand
        pair_frame.grid_columnconfigure(1, weight=1)  # Allow the entry to expand

        # Add the Entry widget as an attribute to the Frame object
        pair_frame.entry = entry

        return pair_frame


class SimulationGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Random Walk Simulation")
        self.root.geometry("1000x600")  # Set the size of the window to 400x300
        # self.root.resizable(False, False)  # Prevent the window from being resizable

        # Configure the grid to expand to fill the available space
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self._create_gui_components()

    def create_styled_button(self, parent, **kwargs):
        # Define the button style
        button_hover_color = 'gray'
        regular_color = 'lightgray'
        button_active_color = 'slateblue'

        button_style = {"font": ("Arial", 10),
                        "borderwidth": 1,
                        "relief": tk.RAISED,
                        "bg": regular_color,
                        "activebackground": button_active_color,
                        "activeforeground": button_hover_color}

        # Create the button with the desired style
        button = tk.Button(parent, **button_style, **kwargs)

        return button

    def _create_gui_components(self):
        self._create_walker_selection()
        self._create_walker_table()
        self._create_simulation_parameters()
        self._create_simulation_buttons()
        self._create_obstacle_creation()
        self._create_obstacle_table()

    def _create_obstacle_creation(self):
        self.obstacle_frame = tk.Frame(self.root)
        self.obstacle_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)

        self.obstacle_type_var = tk.StringVar()  # Create a StringVar
        self.obstacle_type_var.trace('w', self.update_obstacle_parameters)  # Use trace on the StringVar

        self.obstacle_type_frame = tk.Frame(self.obstacle_frame)
        self.obstacle_type_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=2)  # Decrease pady to reduce the gap

        tk.Label(self.obstacle_type_frame, text="Select Obstacle Type:").grid(row=0, column=0, padx=5, pady=5)
        self.obstacle_type = ttk.Combobox(self.obstacle_type_frame,
                                          values=['Barrier', 'Portal Gate'], state='readonly',
                                          textvariable=self.obstacle_type_var)
        self.obstacle_type.grid(row=0, column=1, padx=5, pady=5)

        self.obstacle_name = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Obstacle name:", 1)
        self.obstacle_x = GuiHelper.create_label_entry_pair(self.obstacle_frame, "X:", 2)
        self.obstacle_y = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Y:", 3)
        self.obstacle_width = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Width:", 4)
        self.obstacle_height = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Height:", 5)

        self.obstacle_dest_x = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Dest X:", 6)
        self.obstacle_dest_y = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Dest Y:", 7)

        self.add_obstacle_button = self.create_styled_button(self.obstacle_frame, text="Add Obstacle", command=self.add_obstacle)
        self.add_obstacle_button.grid(row=8, column=0, columnspan=2)

    def update_obstacle_parameters(self, *args):
        obstacle_type = self.obstacle_type.get()

        if obstacle_type == 'Portal Gate':
            self.obstacle_dest_x.grid()
            self.obstacle_dest_y.grid()
        else:
            self.obstacle_dest_x.grid_remove()
            self.obstacle_dest_y.grid_remove()

    def add_obstacle(self):
        obstacle_type = self.obstacle_type.get()
        if not obstacle_type:
            self.show_error("Error", "Please select an obstacle type!")
            return
        obstacle_name = self.obstacle_name.entry.get()
        x_str = self.obstacle_x.entry.get()
        y_str = self.obstacle_y.entry.get()
        width_str = self.obstacle_width.entry.get()
        height_str = self.obstacle_height.entry.get()

        # Check if any of the entry fields are empty
        if not obstacle_name or not x_str or not y_str or not width_str or not height_str:
            self.show_error("Error", "Please fill in all fields!")
            return

        try:
            x = float(x_str)
            y = float(y_str)
            width = float(width_str)
            height = float(height_str)
        except ValueError:
            self.show_error("Error", "Please enter valid numbers for x, y, width, and height!")
            return

        # Assign default values to dest_x and dest_y
        dest_x = dest_y = None

        if obstacle_type == 'Portal Gate':
            dest_x_str = self.obstacle_dest_x.entry.get()
            dest_y_str = self.obstacle_dest_y.entry.get()

            # Check if dest_x and dest_y fields are empty
            if not dest_x_str or not dest_y_str:
                self.show_error("Error", "Please fill in all fields for Portal Gate!")
                return

            try:
                dest_x = float(dest_x_str)
                dest_y = float(dest_y_str)
            except ValueError:
                self.show_error("Error", "Please enter valid numbers for dest_x and dest_y!")
                return

        added_obstacle = False
        # Add the obstacle to the simulation and check if it was added successfully
        if obstacle_type == 'Barrier':
            added_obstacle = self.controller.add_barrier(obstacle_name, x, y, width, height)
        elif obstacle_type == 'Portal Gate':
            added_obstacle = self.controller.add_portal_gate(obstacle_name, x, y, width, height, dest_x, dest_y)

        # If the obstacle was added successfully, add it to the obstacle table
        if added_obstacle:
            self.obstacle_table.insert("", "end", values=(obstacle_name, x, y, width, height, dest_x, dest_y))

    def remove_obstacle(self):
        # Get the selected obstacle from the obstacle table
        selected_items = self.obstacle_table.selection()
        if not selected_items:
            self.show_error("Error", "Please select an obstacle to remove!")
            return

        selected_item = selected_items[0]
        selected_obstacle = self.obstacle_table.item(selected_item)['values'][0]

        # Call the remove_obstacle method of the controller to remove the obstacle from the simulation
        self.controller.remove_obstacle(selected_obstacle)

        # Remove the obstacle from the obstacle table in the GUI
        self.obstacle_table.delete(selected_item)

    def _create_obstacle_table(self):
        self.obstacle_table = ttk.Treeview(self.obstacle_frame,
                                           columns=("Obstacle Name", "X", "Y", "Width", "Height", "Dest X", "Dest Y"),
                                           show="headings", height=5)
        self.obstacle_table.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        self.obstacle_table.column("Obstacle Name", width=100)
        self.obstacle_table.column("X", width=50)
        self.obstacle_table.column("Y", width=50)
        self.obstacle_table.column("Width", width=50)
        self.obstacle_table.column("Height", width=50)
        self.obstacle_table.column("Dest X", width=50)
        self.obstacle_table.column("Dest Y", width=50)

        self.obstacle_table.heading("Obstacle Name", text="Obstacle Name")
        self.obstacle_table.heading("X", text="X")
        self.obstacle_table.heading("Y", text="Y")
        self.obstacle_table.heading("Width", text="Width")
        self.obstacle_table.heading("Height", text="Height")
        self.obstacle_table.heading("Dest X", text="Dest X")
        self.obstacle_table.heading("Dest Y", text="Dest Y")

        # Create a new frame for the button
        self.obstacle_button_frame = tk.Frame(self.obstacle_frame)
        self.obstacle_button_frame.grid(row=10, column=0, padx=5, pady=5)  # Center the frame

        self.remove_obstacle_button = tk.Button(self.obstacle_button_frame, text="Remove Obstacle",
                                                command=self.remove_obstacle)
        self.remove_obstacle_button.grid(row=0, column=0, padx=5, pady=5)  # Add spacing

    def _create_walker_selection(self):
        self.walker_frame = tk.Frame(self.root)
        self.walker_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)

        # Configure the grid to expand to fill the available space
        self.walker_frame.grid_columnconfigure(0, weight=1)
        self.walker_frame.grid_rowconfigure(0, weight=1)

        self.walker_type_var = tk.StringVar()  # Create a StringVar
        self.walker_type_var.trace('w', self.update_walker_parameters)  # Use trace on the StringVar

        self.walker_type_frame = tk.Frame(self.walker_frame)
        self.walker_type_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=2)  # Decrease pady to reduce the gap

        tk.Label(self.walker_type_frame, text="Select Walker Type:").grid(row=0, column=0, padx=5, pady=5)
        self.walker_type = ttk.Combobox(self.walker_type_frame,
                                        values=['BiasedWalker', 'OneUnitRandomWalker', 'DiscreteStepWalker',
                                                'RandomStepWalker'], state='readonly',
                                        textvariable=self.walker_type_var)
        self.walker_type.grid(row=0, column=1, padx=5, pady=5)

        # BiasedWalker parameters
        self.biased_walker_frame = tk.Frame(self.walker_frame)
        self.biased_walker_frame.grid(row=1, column=0, padx=5, pady=2,
                                      sticky=tk.W + tk.E + tk.N + tk.S)  # Decrease pady to reduce the gap

        # Configure the grid to expand to fill the available space
        self.biased_walker_frame.grid_columnconfigure(0, weight=1)
        self.biased_walker_frame.grid_rowconfigure(0, weight=1)

        # Create label-entry pairs for each parameter
        self.biased_walker_params = {
            'up_prob': GuiHelper.create_label_entry_pair(self.biased_walker_frame, "Up Probability:", 0),
            'down_prob': GuiHelper.create_label_entry_pair(self.biased_walker_frame, "Down Probability:", 1),
            'left_prob': GuiHelper.create_label_entry_pair(self.biased_walker_frame, "Left Probability:", 2),
            'right_prob': GuiHelper.create_label_entry_pair(self.biased_walker_frame, "Right Probability:", 3),
            'to_origin_prob': GuiHelper.create_label_entry_pair(self.biased_walker_frame, "To Origin Probability:", 4)
        }

        # Create a new frame for the walker count
        self.walker_count_frame = tk.Frame(self.walker_frame)
        self.walker_count_frame.grid(row=4, column=0, columnspan=2)  # Center the frame

        tk.Label(self.walker_count_frame, text="Amount of this walker to add:").grid(row=0, column=0, padx=5, pady=5)
        vcmd = (self.root.register(self.validate_walker_count), '%P')
        self.walker_count = tk.Entry(self.walker_count_frame, validate='key', validatecommand=vcmd)
        self.walker_count.grid(row=0, column=1, padx=5, pady=5)

        self.add_walker_button = self.create_styled_button(self.walker_frame, text="Add Walker", command=self.add_walker)
        self.add_walker_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def update_walker_parameters(self, *args):
        walker_type = self.walker_type.get()

        # Hide all parameter pairs
        for pair in self.biased_walker_params.values():
            pair.grid_remove()

        if walker_type == 'BiasedWalker':
            # Show parameter pairs for BiasedWalker
            for pair in self.biased_walker_params.values():
                pair.grid()

    def _create_walker_table(self):
        self.walker_table = ttk.Treeview(self.walker_frame, columns=('Type', 'Count'), show='headings', height=5)
        self.walker_table.heading('Type', text='Walker Type')
        self.walker_table.heading('Count', text='Walker Count')
        self.walker_table.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Create a new frame for the button and the label
        self.button_label_frame = tk.Frame(self.walker_frame)
        self.button_label_frame.grid(row=7, column=0, columnspan=2)  # Center the frame

        self.remove_walker_button = self.create_styled_button(self.button_label_frame, text="Remove Walker", command=self.remove_walker)
        self.remove_walker_button.grid(row=0, column=0, padx=5, pady=5)  # Add spacing

        # Add the walker count label to the new frame
        self.walker_count_label = tk.Label(self.button_label_frame, text="Total Walkers: 0")
        self.walker_count_label.grid(row=0, column=1, padx=5, pady=5)  # Add spacing the "Remove Walker" button

    def _create_simulation_parameters(self):
        self.simulation_frame = tk.Frame(self.root)
        self.simulation_frame.grid(row=1, column=1, padx=10, pady=20, sticky=tk.N + tk.S + tk.E + tk.W)

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
        self.run_button = self.create_styled_button(self.simulation_frame, text="Run Simulation", command=self.run_simulation)
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
            up_prob = self.biased_walker_params['up_prob'].entry.get()
            down_prob = self.biased_walker_params['down_prob'].entry.get()
            left_prob = self.biased_walker_params['left_prob'].entry.get()
            right_prob = self.biased_walker_params['right_prob'].entry.get()
            to_origin_prob = self.biased_walker_params['to_origin_prob'].entry.get()

            if not up_prob or not down_prob or not left_prob or not right_prob or not to_origin_prob:
                self.show_error("Error", "Please enter all probabilities for the Biased Walker!")
                return

            try:
                up_prob = float(up_prob)
                down_prob = float(down_prob)
                left_prob = float(left_prob)
                right_prob = float(right_prob)
                to_origin_prob = float(to_origin_prob)

                if up_prob < 0 or down_prob < 0 or left_prob < 0 or right_prob < 0 or to_origin_prob < 0:
                    raise ValueError

                if up_prob == 0 and down_prob == 0 and left_prob == 0 and right_prob == 0 and to_origin_prob == 0:
                    raise ValueError

            except ValueError:
                self.show_error("Error",
                                "Probabilities must be non-negative floats and at least one of them must be non-zero!")
                return

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

    def add_barrier(self, barrier_name, x, y, width, height):
        try:
            barrier = Barrier2D(x, y, width, height)
            added = self.model.simulation.add_barrier(barrier_name, barrier)
            if not added:
                self.view.show_error("Error", "The new barrier intersects with an existing obstacle or the origin!")
            return added
        except Exception as e:
            self.view.show_error("Error", str(e))
            return False

    def add_portal_gate(self, portal_gate_name, x, y, width, height, dest_x, dest_y):
        try:
            portal_gate = PortalGate(x, y, width, height, dest_x, dest_y)
            added = self.model.simulation.add_portal_gate(portal_gate_name, portal_gate)
            if not added:
                self.view.show_error("Error", "The new portal gate intersects with an existing obstacle or the origin!")
            return added
        except Exception as e:
            self.view.show_error("Error", str(e))
            return False

    def remove_obstacle(self, obstacle_name):
        # Remove the obstacle from the simulation
        if obstacle_name in self.model.simulation.barriers:
            del self.model.simulation.barriers[obstacle_name]
        elif obstacle_name in self.model.simulation.portal_gates:
            del self.model.simulation.portal_gates[obstacle_name]

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
