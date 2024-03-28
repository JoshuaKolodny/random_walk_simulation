import os
import json
from typing import Any, Dict

from utils import MessageUtils


class StatisticsExporter:
    """
    A class used to export statistics data to a JSON file.

    ...

    Attributes
    ----------
    data : dict
        a dictionary to store the statistics data

    Methods
    -------
    add_data(key, value):
        Adds a key-value pair to the data dictionary.
    save_to_json(filename):
        Saves the data dictionary to a JSON file.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the StatisticsExporter object.
        """
        self.data: Dict[str, Any] = {}

    def add_data(self, key: str, value: Any) -> None:
        """
        Adds a key-value pair to the data dictionary.

        Parameters
        ----------
        key : str
            the key for the data dictionary
        value : Any
            the value for the data dictionary
        """
        self.data[key] = value

    def save_to_json(self, filepath: str):
        """
        Saves the data dictionary to a JSON file.

        Parameters
        ----------
        filepath : str
            the path of the directory or 'stats.json'
        """

        base_filename = 'stats'
        extension = '.json'
        counter = 1

        # If the filepath is a directory, append 'stats.json' to it
        if os.path.isdir(filepath):
            filename = f"{base_filename}{extension}"
            while os.path.exists(os.path.join(filepath, filename)):
                filename = f"{base_filename}_{counter}{extension}"
                counter += 1
            filepath = os.path.join(filepath, filename)
        # If the filepath is a relative path to 'stats.json' and the file exists, append a counter to it
        elif os.path.basename(filepath) == f"{base_filename}{extension}" and os.path.exists(filepath):
            directory = os.path.dirname(filepath)
            filename = f"{base_filename}_{counter}{extension}"
            while os.path.exists(os.path.join(directory, filename)):
                filename = f"{base_filename}_{counter}{extension}"
                counter += 1
            filepath = os.path.join(directory, filename)

        # Try to open the file and dump the data into it
        try:
            with open(filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except OSError as e:
            MessageUtils.show_error('Error',
                                    f"Error: Cannot save the statistics json file to {filepath}. {e.strerror}. Please enter a valid path.")

