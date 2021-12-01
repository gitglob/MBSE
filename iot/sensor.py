import random


class Sensor:
    N_MEASURES = 5
    def __init__(self, error, cost, power):
        self.error = error
        self.cost = cost
        self.power = power
        self.power_used = 0

    def measure(self, co2_value):
        result = 0.0
        for _ in range(self.N_MEASURES):
            error = self.error*random.uniform(-1.0, 1.0)
            result += co2_value*(1 + error)
            self.power_used += self.power
        result /= self.N_MEASURES
        return result

class SensorList:
    SCD4 = Sensor(0.05, 7, 9.72e-3)
