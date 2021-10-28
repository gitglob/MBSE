import battery
import processor
import sensor
import network

class Device:
    def __init__(self, sensor, network, battery, sensor_id):
        self.sensor = sensor
        self.network = network
        self.battery = battery
        self.sensor_id = sensor_id
        self.x = 0
        self.y = 0
        self.z = 0

    def get_total_cost(self):
        return self.sensor.cost + self.battery.cost + self.network.cost

    def measure(self, real_co2):
        # Inside sensor we should add error
        if not self.is_empty():
            return None
        power_consumed = self.sensor.power
        powerconsumed += network.power
        self.battery.discharge(power_consumed)
        return self.sensor.measure(real_co2)

