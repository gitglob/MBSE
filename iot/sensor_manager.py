import numpy as np

from .device import Device
from .battery import BatteryList
from .network import Network, NetworkList
from .sensor import Sensor
from .processor import ProcessorList

class SensorManager:
    MEASURE_PERIOD = 600 # 10 mins

    def __init__(self, city):
        self.devices = []
        self.latest_measure = np.zeros(1)
        self.city = city


    def distribute_sensors(self, distance):
        for i in range(self.city.rows):
            for j in range(self.city.cols):
                if (self.city.city_model[i][j][0] == self.city.ROAD
                        and not self.check_sensor_near(i, j, distance)):
                    self.add_sensor(i, j, 0)

    def check_sensor_near(self, row, col, distance):
        for d in self.devices:
            for i in range(-distance, distance):
                for j in range(-distance, distance):
                    if d.x == row+i and d.y == col+j:
                        return True
        return False

    def add_sensor(self, x, y, z):
        sensor = Sensor(0.03, 1, 1.5, 0.5)
        device = Device(sensor, NetworkList.LORA, BatteryList.TestBattery, ProcessorList.ESP32, len(self.devices)+1)
        device.set_position(x, y, z)
        self.devices.append(device)

    def measure(self, city):
        values = np.zeros(shape=(city.rows, city.cols))
        for d in self.devices:
            values[d.x][d.y] = d.measure(city.grid3d[d.x][d.y][d.z].co2)
        self.latest_measure = values
        return values
    
    def get_sensors_count(self):
        return len(self.devices)
    
    def get_total_co2(self):
            return np.sum(self.latest_measure)
