import numpy as np
import random

from .device import Device
from .battery import BatteryList
from .network import Network, NetworkList
from .sensor import Sensor
from .processor import ProcessorList

class SensorManager:
    def __init__(self, city, period):
        self.period = period
        self.devices = []
        self.m = np.zeros(shape=(city.rows, city.cols))
        self.city = city
        self.measure_history = []

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
        sensor = Sensor(0.10, 1, 1.5, 0.5)
        device = Device(sensor, NetworkList.LOWRA, BatteryList.INFINITE,
                ProcessorList.ESP32, len(self.devices), self.period)

        device.set_position(x, y, z)
        self.devices.append(device)

    def shuffle_sensors(self, roads):
        aux = roads.copy()
        random.shuffle(aux)
        for n, d in enumerate(self.devices):
            d.set_position(aux[n].x, aux[n].y, 0)
        self.m = np.zeros(shape=(self.city.rows, self.city.cols))

    def measure(self, city, minute):
        for d in self.devices:
            value = d.measure(city.grid3d[d.x][d.y][d.z].co2, minute)
            if value is not None:
                self.m[d.x][d.y] = value

    def gateway(self):
        self.measure_history.append(self.m)
        return self.m
    
    def get_sensors_count(self):
        return len(self.devices)
    
    def get_total_co2(self):
        return np.sum(self.measure_history[-1])
