import numpy as np
import random

from .device import Device
from .battery import BatteryList
from .network import Network, NetworkList
from .sensor import Sensor
from .processor import ProcessorList

class SensorManager:
    MEASURE_PERIOD = 3600

    def __init__(self, city):
        self.devices = {}
        for n in range(60):
            self.devices[n] = []
        self.m = np.zeros(shape=(city.rows, city.cols))
        self.city = city
        self.measure_history = []
        self.number_devices = 0

    def distribute_sensors(self, distance):
        for i in range(self.city.rows):
            for j in range(self.city.cols):
                if (self.city.city_model[i][j][0] == self.city.ROAD
                        and not self.check_sensor_near(i, j, distance)):
                    self.add_sensor(i, j, 0)

    def check_sensor_near(self, row, col, distance):
        for d_list in list(self.devices.values()):
            for d in d_list:
                for i in range(-distance, distance):
                    for j in range(-distance, distance):
                        if d.x == row+i and d.y == col+j:
                            return True
        return False

    def add_sensor(self, x, y, z):
        sensor = Sensor(0.03, 1, 1.5, 0.5)
        device = Device(sensor, NetworkList.LOWRA, BatteryList.INFINITE,
                ProcessorList.ESP32, self.number_devices)
        self.number_devices += 1

        device.set_position(x, y, z)
        r = random.randint(0, 59)
        self.devices[r].append(device)

    def shuffle_sensors(self, roads, minute):
        aux = roads.copy()
        random.shuffle(aux)
        for n, d in enumerate(self.devices[minute]):
            d.set_position(aux[n].x, aux[n].y, 0)

    def measure(self, city, minute):
        for d in self.devices[minute]:
            self.m[d.x][d.y] = d.measure(city.grid3d[d.x][d.y][d.z].co2)

    def gateway(self):
        self.measure_history.append(self.m)
        return self.m
    
    def get_sensors_count(self):
        total = 0
        for l in self.devices.values():
            total += len(l)
        return total
    
    def get_total_co2(self):
        return np.sum(self.measure_history[:-1])
