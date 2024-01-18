import json
import csv


class MemoryHandler:
    def __init__(self):
        self._database_path = "database.csv"
        self._configuration_path = "configurations.json"

    def read_data_base(self):
        with open(self._database_path, "r") as file_handle:
            data = json.load(file_handle)
            return data

    def write_to_database(self, data):
        with open(self._database_path, "w") as file_handle:
            json.dump(file_handle, data)

    def save_configuration(self, data):
        with open(self._configuration_path, "w") as file_handle:
            json.dump(file_handle, data)

    def load_configuration(self):
        with open(self._configuration_pat, "r") as file_handle:
            data = json.load(file_handle)
            return data
