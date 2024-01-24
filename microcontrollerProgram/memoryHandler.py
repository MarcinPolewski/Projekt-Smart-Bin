import json


class MemoryHandler:
    def __init__(self):
        self._configuration_path = "configuration.json"

    def save_configuration(self, data):
        with open(self._configuration_path, "w") as file_handle:
            json.dump(data, file_handle)

    def load_configuration(self):
        with open(self._configuration_path, "r") as file_handle:
            data = json.load(file_handle)
            return data
