import os
import json
from typing import Any, Dict


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

    def save_to_json(self, filename: str) -> None:
        """
        Saves the data dictionary to a JSON file.

        If a file with the same name already exists, a counter is appended to the filename.

        Parameters
        ----------
        filename : str
            the name of the JSON file
        """
        # Validate the filename to prevent directory traversal
        # if ".." in filename or "/" in filename:
        #     raise ValueError("Invalid filename.")

        base_filename, file_extension = os.path.splitext(filename)
        counter = 1

        while os.path.exists(filename):
            filename = f"{base_filename}_{counter}{file_extension}"
            counter += 1

        try:
            with open(filename, 'w') as f:
                json.dump(self.data, f, indent=4)
        except OSError as e:
            print(f"Error: Cannot write to the file {filename}. {e.strerror}.")