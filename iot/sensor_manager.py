import numpy as np
import random
import copy

from .device import Device
from .battery import BatteryList, get_best_battery
from .network import Network, NetworkList
from .sensor import SensorList
from .processor import ProcessorList

class SensorManager:
    def __init__(self, city, period):
        self.period = period
        self.devices = []
        self.m = np.zeros(shape=(city.rows, city.cols))
        self.city = city
        self.measure_history = []

    def distribute_sensors(self, distance):
        valid_pos = np.ones(shape=(self.city.rows, self.city.cols))
        for i in range(self.city.rows):
            for j in range(self.city.cols):
                if ((self.city.city_model[i][j][0] == self.city.ROAD or self.city.city_model[i][j][0] == self.city.NOTHING) and valid_pos[i][j] == 1):
                    self.add_sensor(i, j, 0)
                    #mark positions around as invalid
                    bottom_x = max(0, j-distance-1)
                    bottom_y = max(0, i-distance-1)
                    top_x = min(self.city.cols, j + distance+1)
                    top_y = min(self.city.rows, i + distance+1)
                    for y in range(bottom_y, top_y):
                        for x in range(bottom_x, top_x):
                            valid_pos[y][x] = 0

    def check_sensor_near(self, row, col, distance):
        for d in self.devices:
            for i in range(-distance, distance):
                for j in range(-distance, distance):
                    if d.x == row+i and d.y == col+j:
                        return True
        return False

    def add_sensor(self, x, y, z):
        device = Device(copy.deepcopy(SensorList.SCD4),
                copy.deepcopy(NetworkList.LORA), len(self.devices),
                self.period)

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
    
    def get_sensor_cost(self, runtime):
        name, battery = get_best_battery(self.get_used_power(runtime))
        print("Battery", name)
        return self.devices[0].get_total_cost() + battery.cost

    def get_used_power(self, runtime):
        used_power = self.devices[0].get_used_power() * 3600*24*365 / runtime
        return used_power
