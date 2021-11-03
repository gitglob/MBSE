import numpy as np

from .device import Device
from .battery import BatteryList
from .network import Network
from .sensor import Sensor

class SensorManager:
    MEASURE_PERIOD = 600 # 10 mins
    def __init__(self):
        self.devices = []
        self.latest_measure = np.zeros(1)

    def measure(self, city):
        values = np.zeros(shape=(city.rows, city.cols))
        for d in self.devices:
            values[d.x][d.y] = d.measure(city.grid3d[d.x][d.y][d.z].co2)
        self.latest_measure = values
        return values

    def create_sensor(self, x, y, z):
        sensor = Sensor(0.03, 1, 1.5, 0.5)
        network = Network()
        device = Device(sensor, network, BatteryList.TestBattery, len(self.devices)+1)
        device.set_position(x, y, z)
        self.devices.append(device)
    
    def get_sensors_count(self):
        return len(self.devices)
    
    def get_total_co2(self):
            return np.sum(self.latest_measure)
