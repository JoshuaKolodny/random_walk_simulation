import os
import json
from typing import Any, Dict


class StatisticsExporter:
    def __init__(self) -> None:
        self.data: Dict[str, Any] = {}

    def add_data(self, key: str, value: Any) -> None:
        self.data[key] = value

    def save_to_json(self, filename: str) -> None:
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