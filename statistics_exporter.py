import json


class StatisticsExporter:
    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)
