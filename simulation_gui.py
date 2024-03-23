import tkinter as tk
from tkinter import messagebox, ttk

from PIL import ImageTk, Image, ImageEnhance

from main import *


class GuiHelper:
    @staticmethod
    def create_label_entry_pair(frame, text, row):
        pair_frame = tk.Frame(frame)
        pair_frame.grid(row=row, column=0, padx=5, pady=5, sticky=tk.W + tk.E)

        label = tk.Label(pair_frame, text=text)
        label.grid(row=0, column=0, sticky=tk.W)

        entry = GuiHelper.create_custom_entry(pair_frame)
        entry.grid(row=0, column=1, sticky=tk.E)

        pair_frame.grid_columnconfigure(0, weight=1)  # Allow the label to expand
        pair_frame.grid_columnconfigure(1, weight=1)  # Allow the entry to expand

        # Add the Entry widget as an attribute to the Frame object
        pair_frame.entry = entry

        return pair_frame

    @staticmethod
    def create_custom_entry(parent, **kwargs):
        # Create a style
        style = ttk.Style()

        # Configure the style for Entry widget
        style.configure('Custom.TEntry', foreground='#333333', background='#f0f0f0', bordercolor='gray',
                        fieldbackground='#f0f0f0', font=('Arial', 12))

        # Create an entry with the custom style
        entry = ttk.Entry(parent, style="Custom.TEntry", **kwargs)

        return entry

    @staticmethod
    def create_styled_button(parent, **kwargs):
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

        # Define the hover function
        def on_hover(event):
            button['background'] = button_hover_color

        # Define the leave function
        def on_leave(event):
            button['background'] = regular_color

        # Bind the hover and leave functions to the button
        button.bind("<Enter>", on_hover)
        button.bind("<Leave>", on_leave)

        return button


class SimulationGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Random Walk Simulation")
        self.root.geometry("1200x600")  # Set the size of the window to 1200x600
        self.root.resizable(False, False)  # Prevent the window from being resizable

        # Load the background image
        bg_image = Image.open('background_app_image.jpg')
        bg_image = bg_image.resize((1200, 600))  #
        # Add opacity to the image by reducing its brightness
        enhancer = ImageEnhance.Brightness(bg_image)
        bg_image = enhancer.enhance(0.8)  # Reduce brightness to 50% to simulate 50% opacity
        self.background_image = ImageTk.PhotoImage(bg_image)

        # Create a label with the background image and place it at the bottom of the widget stack
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1,
                                    anchor="nw")  # "nw" anchor sets the label to the top-left corner

        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=3)

        self._create_gui_components()

    def _create_gui_components(self):
        self._create_walker_selection()
        self._create_walker_table()
        self._create_obstacle_creation()
        self._create_obstacle_table()
        self._create_simulation_parameters()
        self._create_simulation_buttons()

    def _create_obstacle_creation(self):
        self.obstacle_frame = tk.Frame(self.root)
        self.obstacle_frame.grid(row=0, column=2, padx=(5, 100), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create a frame for the title
        self.title_frame = tk.Frame(self.obstacle_frame)
        self.title_frame.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        self.obstacle_title = tk.Label(self.title_frame, text="Step 2:", font=("Arial", 20))
        self.obstacle_title.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        self.obstacle_type_var = tk.StringVar()  # Create a StringVar
        self.obstacle_type_var.trace('w', self.update_obstacle_parameters)  # Use trace on the StringVar

        self.obstacle_type_frame = tk.Frame(self.obstacle_frame)
        self.obstacle_type_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=2)  # Decrease pady to reduce the gap

        tk.Label(self.obstacle_type_frame, text="Select Obstacle Type:").grid(row=0, column=0, padx=5, pady=5)
        self.obstacle_type = ttk.Combobox(self.obstacle_type_frame,
                                          values=['Barrier', 'Portal Gate'], state='readonly',
                                          textvariable=self.obstacle_type_var)
        self.obstacle_type.grid(row=0, column=1, padx=5, pady=5)

        self.obstacle_name = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Obstacle name:", 2)
        self.obstacle_x = GuiHelper.create_label_entry_pair(self.obstacle_frame, "X:", 3)
        self.obstacle_y = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Y:", 4)
        self.obstacle_width = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Width:", 5)
        self.obstacle_height = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Height:", 6)

        self.obstacle_dest_x = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Dest X:", 7)
        self.obstacle_dest_y = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Dest Y:", 8)

        self.add_obstacle_button = GuiHelper.create_styled_button(self.obstacle_frame, text="Add Obstacle", command=self.add_obstacle)
        self.add_obstacle_button.grid(row=9, column=0, columnspan=2)

        # Set the default value for the obstacle type combobox
        self.obstacle_type_var.set('Barrier')
        # Update the obstacle parameters
        self.update_obstacle_parameters()

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
        self.obstacle_table.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        self.obstacle_table.column("Obstacle Name", width=100)
        self.obstacle_table.column("X", width=25)
        self.obstacle_table.column("Y", width=25)
        self.obstacle_table.column("Width", width=50)
        self.obstacle_table.column("Height", width=50)
        self.obstacle_table.column("Dest X", width=40)
        self.obstacle_table.column("Dest Y", width=40)

        self.obstacle_table.heading("Obstacle Name", text="Obstacle Name")
        self.obstacle_table.heading("X", text="X")
        self.obstacle_table.heading("Y", text="Y")
        self.obstacle_table.heading("Width", text="Width")
        self.obstacle_table.heading("Height", text="Height")
        self.obstacle_table.heading("Dest X", text="Dest X")
        self.obstacle_table.heading("Dest Y", text="Dest Y")

        # Create a new frame for the button
        self.obstacle_button_frame = tk.Frame(self.obstacle_frame)
        self.obstacle_button_frame.grid(row=11, column=0, padx=5, pady=5)  # Center the frame

        self.remove_obstacle_button = GuiHelper.create_styled_button(self.obstacle_button_frame, text="Remove Obstacle",
                                                                command=self.remove_obstacle)
        self.remove_obstacle_button.grid(row=0, column=0, padx=5, pady=5)  # Add spacing

    def _create_walker_selection(self):
        self.walker_frame = tk.Frame(self.root)
        self.walker_frame.grid(row=0, column=0, padx=(100, 5), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create a frame for the title
        self.title_frame = tk.Frame(self.walker_frame)
        self.title_frame.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        self.walker_title = tk.Label(self.title_frame, text="Step 1:", font=("Arial", 20))
        self.walker_title.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        # Rest of the content
        self.walker_type_var = tk.StringVar()  # Create a StringVar
        self.walker_type_var.trace('w', self.update_walker_parameters)  # Use trace on the StringVar

        self.walker_type_frame = tk.Frame(self.walker_frame)
        self.walker_type_frame.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)

        tk.Label(self.walker_type_frame, text="Select Walker Type:").grid(row=0, column=0, padx=5, pady=5)
        self.walker_type = ttk.Combobox(self.walker_type_frame,
                                        values=['BiasedWalker', 'OneUnitRandomWalker', 'DiscreteStepWalker',
                                                'RandomStepWalker','NoRepeatWalker'], state='readonly',
                                        textvariable=self.walker_type_var)
        self.walker_type.grid(row=0, column=1, padx=5, pady=5)

        # BiasedWalker parameters
        self.biased_walker_frame = tk.Frame(self.walker_frame)
        self.biased_walker_frame.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)

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
        self.walker_count_frame.grid(row=3, column=0, columnspan=2)  # Center the frame

        tk.Label(self.walker_count_frame, text="Amount of this walker to add:").grid(row=0, column=0, padx=5, pady=5)
        # vcmd = (self.root.register(self.validate_walker_count), '%P')
        self.walker_count = GuiHelper.create_custom_entry(self.walker_count_frame, validate='key')
        self.walker_count.grid(row=0, column=1, padx=5, pady=5)

        self.add_walker_button = GuiHelper.create_styled_button(self.walker_frame, text="Add Walker",
                                                                command=self.add_walker)
        self.add_walker_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Set the default value for the walker type combobox
        self.walker_type_var.set('BiasedWalker')
        # Update the walker parameters
        self.update_walker_parameters()

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
        self.walker_table.column('Type', width=100)
        self.walker_table.column('Count', width=100)
        self.walker_table.heading('Type', text='Walker Type')
        self.walker_table.heading('Count', text='Walker Count')
        self.walker_table.grid(row=7, column=0, padx=5, pady=5)

        # Create a new frame for the button and the label
        self.button_label_frame = tk.Frame(self.walker_frame)
        self.button_label_frame.grid(row=8, column=0, columnspan=2)  # Center the frame

        self.remove_walker_button = GuiHelper.create_styled_button(self.button_label_frame, text="Remove Walker", command=self.remove_walker)
        self.remove_walker_button.grid(row=0, column=0, padx=5, pady=5)  # Add spacing

        # Add the walker count label to the new frame
        self.walker_count_label = tk.Label(self.button_label_frame, text="Total Walkers: 0")
        self.walker_count_label.grid(row=0, column=1, padx=5, pady=5)  # Add spacing the "Remove Walker" button

    def _create_simulation_parameters(self):
        self.simulation_frame = tk.Frame(self.root)
        self.simulation_frame.grid(row=0, column=1, padx=10, pady=(20, 0), sticky=tk.S)

        # Create a frame for the title
        self.title_frame = tk.Frame(self.simulation_frame)
        self.title_frame.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        self.simulations_title = tk.Label(self.title_frame, text="Step 3:", font=("Arial", 20))
        self.simulations_title.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        tk.Label(self.simulation_frame, text="Number of Simulations:").grid(row=1, padx=5, pady=5)
        self.num_simulations = GuiHelper.create_custom_entry(self.simulation_frame)
        self.num_simulations.insert(0, '20')  # Insert the default value
        self.num_simulations.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.simulation_frame, text="Number of Steps:").grid(row=2, padx=5, pady=5)
        self.num_steps = GuiHelper.create_custom_entry(self.simulation_frame)
        self.num_steps.insert(0, '500')  # Insert the default value
        self.num_steps.grid(row=2, column=1, padx=5, pady=5)

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

    # def validate_walker_count(self, new_value):
    #     if not self.validate_positive_integer(new_value):
    #         self.walker_count.config(highlightbackground="red")
    #     else:
    #         self.walker_count.config(highlightbackground="white")
    #     return True  # Always return True to accept the input

    def _create_simulation_buttons(self):
        self.run_button = GuiHelper.create_styled_button(self.simulation_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

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
            # Extract probabilities from GUI inputs
            try:
                up_prob = float(self.biased_walker_params['up_prob'].entry.get())
                down_prob = float(self.biased_walker_params['down_prob'].entry.get())
                left_prob = float(self.biased_walker_params['left_prob'].entry.get())
                right_prob = float(self.biased_walker_params['right_prob'].entry.get())
                to_origin_prob = float(self.biased_walker_params['to_origin_prob'].entry.get())

                # Check if probabilities are positive
                if up_prob < 0 or down_prob < 0 or left_prob < 0 or right_prob < 0 or to_origin_prob < 0:
                    raise ValueError("Probabilities must be positive")
            except ValueError:
                self.show_error("Error", "Probabilities must be positive float numbers!")
                return

            # Pack additional arguments into a dictionary
            kwargs = {'up_prob': up_prob, 'down_prob': down_prob, 'left_prob': left_prob,
                      'right_prob': right_prob, 'to_origin_prob': to_origin_prob}

            self.controller.add_walker(walker_type, walker_count, **kwargs)
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
        if not selected_items:
            self.show_error("Error", "Please select a walker to remove!")
            return
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

    def reset_gui(self):
        # Reset walker type to 'BiasedWalker'
        self.walker_type_var.set('BiasedWalker')

        # Reset obstacle type to 'Barrier'
        self.obstacle_type_var.set('Barrier')

        # Clear the walker count entry field
        self.walker_count.delete(0, 'end')

        # Clear the obstacle entry fields
        self.obstacle_name.entry.delete(0, 'end')
        self.obstacle_x.entry.delete(0, 'end')
        self.obstacle_y.entry.delete(0, 'end')
        self.obstacle_width.entry.delete(0, 'end')
        self.obstacle_height.entry.delete(0, 'end')
        self.obstacle_dest_x.entry.delete(0, 'end')
        self.obstacle_dest_y.entry.delete(0, 'end')

        # Reset BiasedWalker parameters
        for entry in self.biased_walker_params.values():
            entry.entry.delete(0, 'end')

        # Clear the walker table
        for row in self.walker_table.get_children():
            self.walker_table.delete(row)

        # Clear the obstacle table
        for row in self.obstacle_table.get_children():
            self.obstacle_table.delete(row)

        # Reset the walker count label
        self.walker_count_label.config(text="Total Walkers: 0")

        # Reset the simulation parameters
        self.num_simulations.delete(0, 'end')
        self.num_simulations.insert(0, '20')  # Insert the default value
        self.num_steps.delete(0, 'end')
        self.num_steps.insert(0, '500')  # Insert the default value

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
        # Create a dictionary that maps the walker types to their respective classes
        self.walker_classes = {
            'BiasedWalker': BiasedWalker,
            'OneUnitRandomWalker': OneUnitRandomWalker,
            'DiscreteStepWalker': DiscreteStepWalker,
            'RandomStepWalker': RandomStepWalker,
            'NoRepeatWalker': NoRepeatWalker
        }

    def add_walker(self, walker_type, walker_count, **kwargs):
        for _ in range(walker_count):
            if walker_type in self.walker_classes:
                walker_class = self.walker_classes[walker_type]
                if walker_type == 'BiasedWalker':
                    walker = walker_class(**kwargs)
                else:
                    walker = walker_class()
                self.model.simulation.add_walker(walker)
                self.walkers[walker_type] = self.walkers.get(walker_type, 0) + 1
            else:
                self.view.show_error("Error", "Invalid walker type! please select a walker")

    def add_barrier(self, barrier_name, x, y, width, height):
        try:
            barrier = Barrier2D(x, y, width, height)
            result = self.model.simulation.add_barrier(barrier_name, barrier)
            if isinstance(result, str):
                self.view.show_error("Error", result)
                return False

            return True

        except Exception as e:
            self.view.show_error("Error", str(e))
            return False

    def add_portal_gate(self, portal_gate_name, x, y, width, height, dest_x, dest_y):
        try:
            portal_gate = PortalGate(x, y, width, height, dest_x, dest_y)
            result = self.model.simulation.add_portal_gate(portal_gate_name, portal_gate)
            if isinstance(result, str):
                self.view.show_error("Error", result)
                return False

            return True

        except Exception as e:
            self.view.show_error("Error", str(e))
            return False

    def remove_obstacle(self, obstacle_name):
        # Remove the obstacle from the simulation
        removed = self.model.simulation.remove_obstacle(obstacle_name)
        if not removed:
            self.view.show_error("Error", "The obstacle was not found in the simulation!")
        else:
            # If the obstacle was successfully removed, update the GUI
            self.view.show_message("Success",
                                   f"The obstacle '{obstacle_name}' was successfully removed from the simulation.")

    def remove_walker(self, walker_type):
        if walker_type in self.walkers:
            # Iterate over a copy of the keys to avoid modifying the dictionary while iterating
            for key in list(self.model.simulation.walkers.keys()):
                if key.startswith(walker_type):
                    self.model.simulation.remove_walker(key)  # Remove the walker from the simulation
            del self.walkers[walker_type]  # Remove the walker type from the dictionary

    def run_simulation(self, num_simulations, num_steps):
        if not self.model.simulation.walkers:
            self.view.show_error("Error", "There must be at least one walker!")
            return

        self.model.run_simulation(num_simulations, num_steps)
        # Show a message box when the simulation is done
        self.view.show_message("Simulation", "Simulation completed!")
        # Reset the GUI parameters
        self.view.reset_gui()


if __name__ == "__main__":
    controller = SimulationController()
    controller.view.root.mainloop()
