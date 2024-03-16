import os
import json


class StatisticsExporter:
    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def save_to_json(self, filename):
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