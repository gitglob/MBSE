class Sensor:
    accuracy = 0.0
    range = 0.0
    cost = 0.0
    power = 0.0

    def __init__(self, accuracy, range, cost, power):
        self.accuracy = accuracy
        self.range = range
        self.cost = cost
        self.power = power

    def get_measurement(self):
        return None