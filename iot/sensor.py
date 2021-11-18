import random


class Sensor:
    def __init__(self, error, range, cost, power):
        self.error = error
        self.range = range
        self.cost = cost
        self.power = power

    def measure(self, co2_value):
        error = self.error*random.uniform(-1.0, 1.0)
        return co2_value*(1 + error)
