from iot.sensor import Sensor
from iot.processor import Processor
from iot.sensor import Sensor
from iot.network import Network
from iot.battery import Battery

class Device:
    def __init__(self, sensor, network, battery, sensor_id):
        self.sensor: Sensor = sensor
        self.network: Network = network
        self.battery: Battery = battery
        self.sensor_id = sensor_id
        self.x = 0
        self.y = 0
        self.z = 0

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_total_cost(self):
        return self.sensor.cost + self.battery.cost + self.network.cost

    def measure(self, real_co2):
        # Inside sensor we should add error
        if not self.battery.is_empty():
            return 0
        power_consumed = self.sensor.power
        #power_consumed += network.power
        self.battery.discharge(power_consumed)
        return self.sensor.measure(real_co2)

