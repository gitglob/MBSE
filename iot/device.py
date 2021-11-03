from iot.sensor import Sensor
from iot.processor import Processor
from iot.sensor import Sensor
from iot.network import Network
from iot.battery import Battery

class Device:
    def __init__(self, sensor, network, battery, processor, sensor_id):
        self.sensor: Sensor = sensor
        self.network: Network = network
        self.battery: Battery = battery
        self.sensor_id = sensor_id
        self.processor: Processor = processor
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
        if self.battery.is_empty():
            print("Device", self.sensor_id, "ran out of battery")
            return 0
        self.processor.start()
        value = self.sensor.measure(real_co2)
        power_consumed = self.sensor.power
        self.network.send_msg(value)
        self.network.empty_buffer()
        self.processor.stop()
        power_consumed = power_consumed + self.processor.get_power_consumed()
        power_consumed = power_consumed + self.network.get_power_consumed()
        self.battery.discharge(power_consumed)
        print(self.sensor_id, "battery left:", self.battery.get_battery_level())
        return value

