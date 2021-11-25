import random


class Device:
    def __init__(self, sensor, network, sensor_id, period):
        self.sensor = sensor
        self.network = network
        self.sensor_id = sensor_id
        self.x = 0
        self.y = 0
        self.z = 0
        self.period = max(1, period//60)
        self.min = random.randint(1, max(self.period, 2))
        self.n = 0

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_total_cost(self):
        return self.sensor.cost + self.network.cost

    def get_used_power(self):
        return self.sensor.power_used + self.network.power_used

    def measure(self, real_co2, minute):
        if (minute-self.min) % self.period != 0:
            return None
        self.n += 1
        value = self.sensor.measure(real_co2)
        self.network.send_msg()
        return value
