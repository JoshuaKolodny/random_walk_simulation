import tkinter as tk
from tkinter import ttk, filedialog
from typing import Optional, Callable, Any, Dict
from utils import Utils, MessageUtils, FileUtils
from PIL import ImageTk, Image, ImageEnhance
from Walker.biased_walker import BiasedWalker
from Walker.discrete_step_walker import DiscreteStepWalker
from Walker.no_repeat_walker import NoRepeatWalker
from Walker.one_unit_random_walker import OneUnitRandomWalker
from Walker.random_step_walker import RandomStepWalker
from simulation_runner import SimulationRunner
from obstacles_and_barriers import Barrier2D
from portal_gate import PortalGate


class EntryFrame(tk.Frame):
    # Used to allow pairing of ttk.Entry with a tk.Frame
    def __init__(self, master: Optional[tk.Widget] = None, cnf: Dict = {}, **kw: Any):
        super().__init__(master=master, cnf=cnf, **kw)
        self.entry: Optional[ttk.Entry] = None


class GuiHelper:
    @staticmethod
    def create_label_entry_pair(frame: tk.Frame, text: str, row: int) -> EntryFrame:
        """
        Creates a pair of label and entry widgets and places them in a new frame.

        Args:
            frame (tk.Frame): The parent frame for the new frame.
            text (str): The text to be displayed in the label.
            row (int): The row in the grid of the parent frame where the new frame will be placed.

        Returns:
            EntryFrame: The new frame containing the label and entry widgets.
        """
        pair_frame = EntryFrame(frame)
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
    def create_custom_entry(parent: tk.Widget, **kwargs) -> ttk.Entry:
        """
        Creates a custom styled ttk.Entry widget.

        Args:
            parent (tk.Widget): The parent widget for the new Entry widget.
            **kwargs: Arbitrary keyword arguments to be passed to the ttk.Entry constructor.

        Returns:
            ttk.Entry: The new Entry widget.
        """
        # Create a style
        style = ttk.Style()

        # Configure the style for Entry widget
        style.configure('Custom.TEntry', foreground='#333333', background='#f0f0f0', bordercolor='gray',
                        fieldbackground='#f0f0f0', font=('Arial', 12))

        # Create an entry with the custom style
        entry = ttk.Entry(parent, style="Custom.TEntry", **kwargs)

        return entry

    @staticmethod
    def create_styled_button(parent: tk.Widget, text: str, command: Callable[[], Any] = lambda: None,
                             **kwargs) -> tk.Button:
        """
        Creates a custom styled tk.Button widget.

        Args:
            parent (tk.Widget): The parent widget for the new Button widget.
            text (str): The text to be displayed on the button.
            command (Callable[[], Any], optional): The function to be called when the button is clicked.
             Defaults to a dummy function.
            **kwargs: Arbitrary keyword arguments to be passed to the tk.Button constructor.

        Returns:
            tk.Button: The new Button widget.
        """
        button_hover_color = 'gray'
        regular_color = 'lightgray'
        button_active_color = 'slateblue'

        button = tk.Button(parent, text=text, command=command, font=("Arial", 10),
                           borderwidth=1, relief=tk.RAISED, bg=regular_color,
                           activebackground=button_active_color, activeforeground=button_hover_color, **kwargs)

        def on_hover(event):
            button['background'] = button_hover_color

        def on_leave(event):
            button['background'] = regular_color

        button.bind("<Enter>", on_hover)
        button.bind("<Leave>", on_leave)

        return button


class SimulationGUI:
    def __init__(self, root, controller):
        """
        Initialize the SimulationGUI class.

        Args:
            root (tkinter.Tk): The root window for the GUI.
            controller (SimulationController): The controller for the simulation.
        """
        self.root = root
        self.controller = controller
        self.root.title("Random Walk Simulation")
        self.root.geometry("1100x550")  # Set the size of the window to 1200x550
        self.root.resizable(False, False)  # Prevent the window from being resizable

        # Load and process the background image
        bg_image = Image.open('background_app_image.jpg')
        bg_image = bg_image.resize((1100, 550))  # Resize the image to fit the window
        # Add opacity to the image by reducing its brightness
        enhancer = ImageEnhance.Brightness(bg_image)
        bg_image = enhancer.enhance(0.8)  # Reduce brightness to 50% to simulate 50% opacity
        self.background_image = ImageTk.PhotoImage(bg_image)

        # Create a label with the background image and place it at the bottom of the widget stack
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1,
                                    anchor="nw")  # "nw" anchor sets the label to the top-left corner

        # Configure the grid layout of the root window
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=3)

        # Create a new frame for the help button in the top right corner
        self.help_button_frame = tk.Frame(self.root)
        self.help_button_frame.grid(row=0, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.E + tk.N)

        # Create a title label
        self.title_label = tk.Label(self.root, text="Random Walk Simulation", font=("Arial", 20, 'bold'),
                                    bg=self.root.cget('bg'))
        self.title_label.grid(row=0, column=1, pady=(5, 0), sticky=tk.N)

        # Create the GUI components
        self._create_gui_components()

    def _create_gui_components(self):
        """
        Create the GUI components for the simulation.
        """
        self._create_walker_selection()
        self._create_walker_table()
        self._create_obstacle_creation()
        self._create_obstacle_table()
        self._create_simulation_parameters()
        self._create_simulation_buttons()

    def _create_obstacle_creation(self):
        """
        Create the GUI components for obstacle creation.
        """
        self.obstacle_frame = tk.Frame(self.root)
        self.obstacle_frame.grid(row=0, column=2, padx=(5, 50), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create a frame for the title
        self.title_frame = tk.Frame(self.obstacle_frame)
        self.title_frame.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        # Create a label for the title
        self.obstacle_title = tk.Label(self.title_frame, text="Step 2:", font=("Arial", 20))
        self.obstacle_title.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        # Create a StringVar for the obstacle type
        self.obstacle_type_var = tk.StringVar()  # Create a StringVar
        self.obstacle_type_var.trace('w', self.update_obstacle_parameters)  # Use trace on the StringVar

        # Create a frame for the obstacle type selection
        self.obstacle_type_frame = tk.Frame(self.obstacle_frame)
        self.obstacle_type_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=2)  # Decrease pady to reduce the gap

        # Create a label and a combobox for the obstacle type selection
        tk.Label(self.obstacle_type_frame, text="Select Obstacle Type:").grid(row=0, column=0, padx=5, pady=5)
        self.obstacle_type = ttk.Combobox(self.obstacle_type_frame,
                                          values=['Barrier', 'Portal Gate'], state='readonly',
                                          textvariable=self.obstacle_type_var)
        self.obstacle_type.grid(row=0, column=1, padx=5, pady=5)

        # Create label-entry pairs for the obstacle parameters
        self.obstacle_name = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Obstacle name:", 2)
        self.obstacle_x = GuiHelper.create_label_entry_pair(self.obstacle_frame, "X:", 3)
        self.obstacle_y = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Y:", 4)
        self.obstacle_width = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Width:", 5)
        self.obstacle_height = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Height:", 6)

        # Create label-entry pairs for the destination parameters (only for Portal Gate)
        self.obstacle_dest_x = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Dest X:", 7)
        self.obstacle_dest_y = GuiHelper.create_label_entry_pair(self.obstacle_frame, "Dest Y:", 8)

        # Create a button for adding the obstacle
        self.add_obstacle_button = GuiHelper.create_styled_button(self.obstacle_frame,
                                                                  text="Add Obstacle", command=self.add_obstacle)
        self.add_obstacle_button.grid(row=9, column=0, columnspan=2)

        # Set the default value for the obstacle type combobox
        self.obstacle_type_var.set('Barrier')
        # Update the obstacle parameters
        self.update_obstacle_parameters()

    def update_obstacle_parameters(self, *args):
        """
        Update the obstacle parameters based on the selected obstacle type.
        """
        obstacle_type = self.obstacle_type.get()

        # If the obstacle type is 'Portal Gate', show the destination parameters
        if obstacle_type == 'Portal Gate':
            self.obstacle_dest_x.grid()
            self.obstacle_dest_y.grid()
        else:
            # If the obstacle type is not 'Portal Gate', hide the destination parameters
            self.obstacle_dest_x.grid_remove()
            self.obstacle_dest_y.grid_remove()

    def add_obstacle(self):
        """
        Add an obstacle to the simulation.
        """
        obstacle_type = self.obstacle_type.get()
        if not obstacle_type:
            MessageUtils.show_error("Error", "Please select an obstacle type!")
            return
        obstacle_name = self.obstacle_name.entry.get()
        x_str = self.obstacle_x.entry.get()
        y_str = self.obstacle_y.entry.get()
        width_str = self.obstacle_width.entry.get()
        height_str = self.obstacle_height.entry.get()

        # Check if any of the entry fields are empty
        if not obstacle_name or not x_str or not y_str or not width_str or not height_str:
            MessageUtils.show_error("Error", "Please fill in all fields!")
            return

        # try converting the entries into float values
        try:
            x = float(x_str)
            y = float(y_str)
            width = float(width_str)
            height = float(height_str)
        except ValueError:
            MessageUtils.show_error("Error", "Please enter valid numbers for x, y, width, and height!")
            return
        if width < 0 or height < 0:
            MessageUtils.show_error("Error", "Please enter non negative values for height and width")
            return

        # Assign default values to dest_x and dest_y
        dest_x = dest_y = None

        # Section for when obstacle is a portal gate
        if obstacle_type == 'Portal Gate':
            dest_x_str = self.obstacle_dest_x.entry.get()
            dest_y_str = self.obstacle_dest_y.entry.get()

            # Check if dest_x and dest_y fields are empty
            if not dest_x_str or not dest_y_str:
                MessageUtils.show_error("Error", "Please fill in all fields for Portal Gate!")
                return

            try:
                dest_x = float(dest_x_str)
                dest_y = float(dest_y_str)
            except ValueError:
                MessageUtils.show_error("Error", "Please enter valid numbers for dest_x and dest_y!")
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
        self.__clear_obstacle_entry_fields()

    def remove_obstacle(self):
        """
        Removes the selected obstacle from the simulation and the GUI.
        """
        # Get the selected obstacle from the obstacle table
        selected_items = self.obstacle_table.selection()
        # If no obstacle is selected, show an error message and return
        if not selected_items:
            MessageUtils.show_error("Error", "Please select an obstacle to remove!")
            return

        # Get the first selected item
        selected_item = selected_items[0]
        # Get the obstacle name from the selected item
        selected_obstacle = self.obstacle_table.item(selected_item)['values'][0]

        # Call the remove_obstacle method of the controller to remove the obstacle from the simulation
        self.controller.remove_obstacle(selected_obstacle)

        # Remove the obstacle from the obstacle table in the GUI
        self.obstacle_table.delete(selected_item)

    def _create_obstacle_table(self):
        """
        Creates the obstacle table in the GUI.
        """
        # Create a Treeview widget for the obstacle table
        self.obstacle_table = ttk.Treeview(self.obstacle_frame,
                                           columns=("Obstacle Name", "X", "Y", "Width", "Height", "Dest X", "Dest Y"),
                                           show="headings", height=5)
        # Position the obstacle table in the grid
        self.obstacle_table.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        # Set the column widths
        self.obstacle_table.column("Obstacle Name", width=100)
        self.obstacle_table.column("X", width=25)
        self.obstacle_table.column("Y", width=25)
        self.obstacle_table.column("Width", width=50)
        self.obstacle_table.column("Height", width=50)
        self.obstacle_table.column("Dest X", width=40)
        self.obstacle_table.column("Dest Y", width=40)

        # Set the column headings
        self.obstacle_table.heading("Obstacle Name", text="Obstacle Name")
        self.obstacle_table.heading("X", text="X")
        self.obstacle_table.heading("Y", text="Y")
        self.obstacle_table.heading("Width", text="Width")
        self.obstacle_table.heading("Height", text="Height")
        self.obstacle_table.heading("Dest X", text="Dest X")
        self.obstacle_table.heading("Dest Y", text="Dest Y")

        # Create a new frame for the button
        self.obstacle_button_frame = tk.Frame(self.obstacle_frame)
        # Position the button frame in the grid
        self.obstacle_button_frame.grid(row=11, column=0, padx=5, pady=5)  # Center the frame

        # Create a button for removing obstacles
        self.remove_obstacle_button = GuiHelper.create_styled_button(self.obstacle_button_frame, text="Remove Obstacle",
                                                                     command=self.remove_obstacle)
        # Position the button in the grid
        self.remove_obstacle_button.grid(row=0, column=0, padx=5, pady=5)  # Add spacing

    def _create_walker_selection(self):
        """
        Creates the walker selection section in the GUI.
        """
        # Create a frame for the walker selection section
        self.walker_frame = tk.Frame(self.root)
        # Position the walker frame in the grid
        self.walker_frame.grid(row=0, column=0, padx=(50, 5), pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        # Create a frame for the title
        self.title_frame = tk.Frame(self.walker_frame)
        # Position the title frame in the grid
        self.title_frame.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        # Create a title label
        self.walker_title = tk.Label(self.title_frame, text="Step 1:", font=("Arial", 20))
        # Position the title label in the grid
        self.walker_title.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        # Rest of the content
        # Create a StringVar for the walker type
        self.walker_type_var = tk.StringVar()
        # Use trace on the StringVar to call update_walker_parameters when the walker type changes
        self.walker_type_var.trace('w', self.update_walker_parameters)

        # Create a frame for the walker type selection
        self.walker_type_frame = tk.Frame(self.walker_frame)
        # Position the walker type frame in the grid
        self.walker_type_frame.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)

        # Create a label for the walker type selection
        tk.Label(self.walker_type_frame, text="Select Walker Type:").grid(row=0, column=0, padx=5, pady=5)
        # Create a combobox for the walker type selection
        self.walker_type = ttk.Combobox(self.walker_type_frame,
                                        values=['BiasedWalker', 'OneUnitRandomWalker', 'DiscreteStepWalker',
                                                'RandomStepWalker', 'NoRepeatWalker'], state='readonly',
                                        textvariable=self.walker_type_var)
        # Position the combobox in the grid
        self.walker_type.grid(row=0, column=1, padx=5, pady=5)

        # BiasedWalker parameters
        # Create a frame for the BiasedWalker parameters
        self.biased_walker_frame = tk.Frame(self.walker_frame)
        # Position the BiasedWalker frame in the grid
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
        # Position the walker count frame in the grid
        self.walker_count_frame.grid(row=3, column=0, columnspan=2)  # Center the frame

        # Create a label for the walker count
        tk.Label(self.walker_count_frame, text="Amount of this walker to add:").grid(row=0, column=0, padx=5, pady=5)
        # Create an entry for the walker count
        self.walker_count = GuiHelper.create_custom_entry(self.walker_count_frame, validate='key')
        # Position the walker count entry in the grid
        self.walker_count.grid(row=0, column=1, padx=5, pady=5)

        # Create a button for adding walkers
        self.add_walker_button = GuiHelper.create_styled_button(self.walker_frame, text="Add Walker",
                                                                command=self.add_walker)
        # Position the add walker button in the grid
        self.add_walker_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Set the default value for the walker type combobox
        self.walker_type_var.set('BiasedWalker')
        # Update the walker parameters
        self.update_walker_parameters()

    def update_walker_parameters(self, *args):
        """
        Updates the displayed walker parameters based on the selected walker type.
        """
        # Get the selected walker type
        walker_type = self.walker_type.get()

        # Hide all parameter pairs
        for pair in self.biased_walker_params.values():
            pair.grid_remove()

        # If the selected walker type is 'BiasedWalker', show the parameter pairs for BiasedWalker
        if walker_type == 'BiasedWalker':
            for pair in self.biased_walker_params.values():
                pair.grid()

    def _create_walker_table(self):
        """
        Create a table to display the walkers in the simulation.
        """
        # Create a Treeview widget for the walker table
        self.walker_table = ttk.Treeview(self.walker_frame, columns=('Type', 'Count'), show='headings', height=5)
        # Set the width of the columns
        self.walker_table.column('Type', width=100)
        self.walker_table.column('Count', width=100)
        # Set the headings of the columns
        self.walker_table.heading('Type', text='Walker Type')
        self.walker_table.heading('Count', text='Walker Count')
        # Position the walker table in the grid
        self.walker_table.grid(row=7, column=0, padx=5, pady=5)

        # Create a new frame for the button and the label
        self.button_label_frame = tk.Frame(self.walker_frame)
        # Position the frame in the grid
        self.button_label_frame.grid(row=8, column=0, columnspan=2)  # Center the frame

        # Create a button for removing walkers
        self.remove_walker_button = GuiHelper.create_styled_button(self.button_label_frame,
                                                                   text="Remove Walker", command=self.remove_walker)
        # Position the button in the grid
        self.remove_walker_button.grid(row=0, column=0, padx=5, pady=5)  # Add spacing

        # Create a label for displaying the total number of walkers
        self.walker_count_label = tk.Label(self.button_label_frame, text="Total Walkers: 0")
        # Position the label in the grid
        self.walker_count_label.grid(row=0, column=1, padx=5, pady=5)  # Add spacing the "Remove Walker" button

    def _create_simulation_parameters(self):
        """
        Create the simulation parameters section of the GUI.
        """
        # Create a frame for the simulation parameters
        self.simulation_frame = tk.Frame(self.root)
        # Position the frame in the grid
        self.simulation_frame.grid(row=0, column=1, padx=10, pady=(20, 0), sticky=tk.S)

        # Create a frame for the title
        self.title_frame = tk.Frame(self.simulation_frame)
        # Position the frame in the grid
        self.title_frame.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        # Create a label for the title
        self.simulations_title = tk.Label(self.title_frame, text="Step 3:", font=("Arial", 20))
        # Position the label in the grid
        self.simulations_title.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)

        # Create labels and entry fields for the number of simulations and steps
        tk.Label(self.simulation_frame, text="Number of Simulations:").grid(row=1, padx=5, pady=5)
        self.num_simulations = GuiHelper.create_custom_entry(self.simulation_frame)
        self.num_simulations.insert(0, '20')  # Insert the default value
        self.num_simulations.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.simulation_frame, text="Number of Steps:").grid(row=2, padx=5, pady=5)
        self.num_steps = GuiHelper.create_custom_entry(self.simulation_frame)
        self.num_steps.insert(0, '500')  # Insert the default value
        self.num_steps.grid(row=2, column=1, padx=5, pady=5)

        # Create field for path to save Json
        tk.Label(self.simulation_frame, text="Path to save Stats: (Optional)").grid(row=3, padx=5, pady=5)

        # Create a button that opens the file dialog when clicked
        self.browse_button = tk.Button(self.simulation_frame, text="Browse", command=self.browse)
        self.browse_button.grid(row=3, column=1, padx=5, pady=5)

        # Create a label to display the selected directory
        self.stats_path = tk.Label(self.simulation_frame, text="", wraplength=200)
        self.stats_path.grid(row=4, column=0, columnspan=2, pady=5)

    def browse(self):
        # Open the file dialog and get the selected directory
        selected_directory = filedialog.askdirectory()

        # Update the stats_path label with the selected directory
        self.stats_path.config(text=selected_directory)

    def _create_simulation_buttons(self):
        """
        Create the buttons for running the simulation and opening the help file.
        """
        # Create a button for running the simulation
        self.run_button = GuiHelper.create_styled_button(self.simulation_frame,
                                                         text="Run Simulation", command=self.run_simulation)
        # Position the button in the grid
        self.run_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Create a button for opening the help file
        self.help_button = GuiHelper.create_styled_button(self.help_button_frame, text="Help",
                                                          command=self._open_help_file)
        # Position the button in the grid
        self.help_button.grid(row=1, column=0, columnspan=2)

    def _open_help_file(self, event=None):
        """
        Open a help file with the default application.
        """
        FileUtils.open_file('Instructions.txt', event)

    def add_walker(self):
        """
        Add a walker to the simulation.
        """
        # Get the walker type and count from the GUI inputs
        walker_type = self.walker_type.get()
        walker_count_str = self.walker_count.get()

        # Validate the walker type and count
        if not walker_type:
            MessageUtils.show_error("Error", "Please select a walker type!")
            return

        if not Utils.validate_positive_integer(walker_count_str):
            MessageUtils.show_error("Error", "Walker count must be a positive integer!")
            return

        if not walker_count_str:
            MessageUtils.show_error("Error", "Please enter a walker count!")
            return

        # Convert the walker count to an integer
        try:
            walker_count = int(walker_count_str)
            if not isinstance(walker_count, int) or walker_count <= 0:
                raise ValueError
        except ValueError:
            MessageUtils.show_error("Error", "Walker count must be a positive integer!")
            return

        # If the walker type is 'BiasedWalker', extract the probabilities from the GUI inputs
        if walker_type == 'BiasedWalker':
            try:
                up_prob = float(self.biased_walker_params['up_prob'].entry.get())
                down_prob = float(self.biased_walker_params['down_prob'].entry.get())
                left_prob = float(self.biased_walker_params['left_prob'].entry.get())
                right_prob = float(self.biased_walker_params['right_prob'].entry.get())
                to_origin_prob = float(self.biased_walker_params['to_origin_prob'].entry.get())

                # Check if the probabilities are positive
                if up_prob < 0 or down_prob < 0 or left_prob < 0 or right_prob < 0 or to_origin_prob < 0:
                    raise ValueError("Probabilities must be positive")
            except ValueError:
                MessageUtils.show_error("Error", "Probabilities must be positive float numbers!")
                return

            # Pack the probabilities into a dictionary and add the walker to the simulation
            kwargs = {'up_prob': up_prob, 'down_prob': down_prob, 'left_prob': left_prob,
                      'right_prob': right_prob, 'to_origin_prob': to_origin_prob}

            self.controller.add_walker(walker_type, walker_count, **kwargs)
        else:
            # Add the walker to the simulation
            self.controller.add_walker(walker_type, walker_count)

        # Clear the walker type and count from the GUI inputs
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
        """
        Remove a walker from the simulation.
        """
        # Get the selected items from the walker table
        selected_items = self.walker_table.selection()
        if not selected_items:
            MessageUtils.show_error("Error", "Please select a walker to remove!")
            return
        for item in selected_items:
            # Get the walker type from the selected item
            walker_type = self.walker_table.item(item)['values'][0]
            # Remove the walker from the simulation
            self.controller.remove_walker(walker_type)
            # Delete the row from the walker table
            self.walker_table.delete(item)

        # Update the walker count label
        self.update_walker_count_label()

    def update_walker_count_label(self):
        """
        Update the label that displays the total number of walkers.
        """
        total_walkers = sum(self.controller.walkers.values())
        self.walker_count_label.config(text=f"Total Walkers: {total_walkers}")

    def run_simulation(self):
        """
        Run the simulation based on the number of simulations and steps input by the user.
        The function validates the inputs, checks if there is at least one walker, and then runs the simulation.
        """
        # Get the number of simulations and steps from the GUI inputs
        num_simulations_str = self.num_simulations.get()
        num_steps_str = self.num_steps.get()

        # Validate the number of simulations and steps
        if not Utils.validate_positive_integer(num_simulations_str):
            MessageUtils.show_error("Error", "Number of simulations must be a positive integer!")
            return

        if not Utils.validate_positive_integer(num_steps_str):
            MessageUtils.show_error("Error", "Number of steps must be a positive integer!")
            return

        # Check if there is at least one walker
        total_walkers = sum(self.controller.walkers.values())
        if total_walkers == 0:
            MessageUtils.show_error("Error", "There must be at least one walker!")
            return

        # Convert the number of simulations and steps to integers and run the simulation
        num_simulations = int(num_simulations_str)
        num_steps = int(num_steps_str)
        stats_path = self.stats_path.cget("text")
        if stats_path:  # Check if stats_path is not empty
            self.controller.run_simulation(num_simulations, num_steps, stats_path)
        else:
            self.controller.run_simulation(num_simulations, num_steps)  # If stats_path is empty

    def __clear_obstacle_entry_fields(self):
        """
        Clear all the obstacle entry fields in the GUI.
        """
        self.obstacle_name.entry.delete(0, 'end')
        self.obstacle_x.entry.delete(0, 'end')
        self.obstacle_y.entry.delete(0, 'end')
        self.obstacle_width.entry.delete(0, 'end')
        self.obstacle_height.entry.delete(0, 'end')
        self.obstacle_dest_x.entry.delete(0, 'end')
        self.obstacle_dest_y.entry.delete(0, 'end')

    def reset_gui(self):
        """
        Reset all the GUI components to their default state.
        """
        # Reset walker type to 'BiasedWalker'
        self.walker_type_var.set('BiasedWalker')

        # Clear the walker count entry field
        self.walker_count.delete(0, 'end')

        # Reset obstacle type to 'Barrier'
        self.obstacle_type_var.set('Barrier')

        # Clear the obstacle entry fields
        self.__clear_obstacle_entry_fields()

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


class SimulationController:
    """
    The SimulationController class is responsible for controlling the simulation process.
    It manages the walkers, barriers, and portal gates in the simulation.
    """

    def __init__(self):
        """
        Initializes a new instance of the SimulationController class.
        """
        self.model = SimulationRunner()  # The simulation runner
        self.view = None  # The GUI view
        self.walkers = {}  # Dictionary to keep track of the walkers added to the simulation
        # Create a dictionary that maps the walker types to their respective classes
        self.walker_classes = {
            'BiasedWalker': BiasedWalker,
            'OneUnitRandomWalker': OneUnitRandomWalker,
            'DiscreteStepWalker': DiscreteStepWalker,
            'RandomStepWalker': RandomStepWalker,
            'NoRepeatWalker': NoRepeatWalker
        }

    def add_walker(self, walker_type: str, walker_count: int, **kwargs):
        """
        Adds a walker of the specified type to the simulation.

        Args:
            walker_type (str): The type of the walker to add.
            walker_count (int): The number of walkers to add.
            **kwargs: Additional parameters for the walker.
        """
        try:
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
                    MessageUtils.show_error("Error", "Invalid walker type! please select a walker")
        except ValueError as e:
            MessageUtils.show_error("Error", str(e))

    def add_barrier(self, barrier_name: str, x: float, y: float, width: float, height: float) -> bool:
        """
        Adds a barrier to the simulation.

        Args:
            barrier_name (str): The name of the barrier.
            x (float): The x-coordinate of the barrier.
            y (float): The y-coordinate of the barrier.
            width (float): The width of the barrier.
            height (float): The height of the barrier.

        Returns:
            bool: True if the barrier was added successfully, False otherwise.
        """
        try:
            barrier = Barrier2D(x, y, width, height)
            result = self.model.simulation.add_barrier(barrier_name, barrier)
            if isinstance(result, str):
                MessageUtils.show_error("Error", result)
                return False

            return True

        except Exception as e:
            MessageUtils.show_error("Error", str(e))
            return False

    def add_portal_gate(self, portal_gate_name: str, x: float, y: float, width: float,
                        height: float, dest_x: float, dest_y: float) -> bool:
        """
        Adds a portal gate to the simulation.

        Args:
            portal_gate_name (str): The name of the portal gate.
            x (float): The x-coordinate of the portal gate.
            y (float): The y-coordinate of the portal gate.
            width (float): The width of the portal gate.
            height (float): The height of the portal gate.
            dest_x (float): The x-coordinate of the destination of the portal gate.
            dest_y (float): The y-coordinate of the destination of the portal gate.

        Returns:
            bool: True if the portal gate was added successfully, False otherwise.
        """
        try:
            portal_gate = PortalGate(x, y, width, height, dest_x, dest_y)
            result = self.model.simulation.add_portal_gate(portal_gate_name, portal_gate)
            if isinstance(result, str):
                MessageUtils.show_error("Error", result)
                return False

            return True

        except Exception as e:
            MessageUtils.show_error("Error", str(e))
            return False

    def remove_obstacle(self, obstacle_name: str):
        """
        Removes an obstacle from the simulation.

        Args:
            obstacle_name (str): The name of the obstacle to remove.
        """
        # Remove the obstacle from the simulation
        removed = self.model.simulation.remove_obstacle(obstacle_name)
        if not removed:
            MessageUtils.show_error("Error", "The obstacle was not found in the simulation!")
        else:
            # If the obstacle was successfully removed, update the GUI
            MessageUtils.show_message("Success",f"The obstacle '{obstacle_name}' "
                                                f"was successfully removed from the simulation.")

    def remove_walker(self, walker_type: str):
        """
        Removes a walker of the specified type from the simulation.

        Args:
            walker_type (str): The type of the walker to remove.
        """
        if walker_type in self.walkers:
            # Iterate over a copy of the keys to avoid modifying the dictionary while iterating
            for key in list(self.model.simulation.walkers.keys()):
                if key.startswith(walker_type):
                    self.model.simulation.remove_walker(key)  # Remove the walker from the simulation
            del self.walkers[walker_type]  # Remove the walker type from the dictionary

    def run_simulation(self, num_simulations: int, num_steps: int, stats_path: Optional[str] = 'stats.json'):
        """
        Runs the simulation for the specified number of simulations and steps.

        Args:
            num_simulations (int): The number of simulations to run.
            num_steps (int): The number of steps per simulation.
            stats_path (str): The path to save the statistics.
        """
        if not self.model.simulation.walkers:
            MessageUtils.show_error("Error", "There must be at least one walker!")
            return
        self.model.run_simulation(num_simulations, num_steps, stats_path)

        MessageUtils.show_message("Simulation", "Simulation completed!")
        # Reset the GUI parameters
        self.walkers= {}
        self.view.reset_gui()
