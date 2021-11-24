import random


class Sensor:
    N_MEASURES = 5
    def __init__(self, error, range, cost, power):
        self.error = error
        self.range = range
        self.cost = cost
        self.power = power

    def measure(self, co2_value):
        result = 0.0
        for _ in range(self.N_MEASURES):
            error = self.error*random.uniform(-1.0, 1.0)
            result += co2_value*(1 + error)
        result /= self.N_MEASURES
        return result
