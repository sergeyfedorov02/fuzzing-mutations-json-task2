from typing import Self


class Seed:
    def __init__(
            self: Self,
            data: str,
    ) -> None:
        self.data = data
        self.energy = 0.0

        self.covered_lines = set()
        self.path_frequency = 0

        self.covered_functions = set()
        self.distance = 0.0

        self.result = None

    def __eq__(self, other):
        return isinstance(other, Seed) and self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def get_data(self):
        return str(self.data)

    def set_data(self, new_data):
        self.data = new_data

    def get_energy(self):
        return self.energy

    def set_energy(self, energy):
        self.energy = energy

    def get_covered_lines(self):
        return set(self.covered_lines)

    def set_covered_lines(self, new_covered_lines):
        self.covered_lines = new_covered_lines

    def get_path_frequency(self):
        return int(self.path_frequency)

    def set_path_frequency(self, new_path_frequency):
        self.path_frequency = new_path_frequency

    def get_covered_functions(self):
        return set(self.covered_functions)

    def set_covered_functions(self, new_covered_functions):
        self.covered_functions = new_covered_functions

    def get_distance(self):
        return self.distance

    def set_distance(self, new_distance):
        self.distance = new_distance

    def set_result(self, new_result):
        self.result = new_result

    def get_result(self):
        return self.result