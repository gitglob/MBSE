import numpy as np
from Classes import Grid

from iot.device import Device
class PeriodicExecTask:
    LOOP_PERIOD = 1 # in seconds

    def __init__(self, period, function, *args, **kwargs):
        self.period = period
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.counter = 0

    def trigger(self):
        if self.counter % self.period == 0:
            self.function(*self.args, **self.kwargs)
        else:
            self.counter += self.LOOP_PERIOD


class PeriodicExecManager:
    def __init__(self):
        self.tasks = []

    def add(self, period, function, *args, **kwargs):
        self.task.append(PeriodicExecTask(period, function, args, kwargs))

    def run(self):
        for task in self.tasks:
            task.trigger()


class Gateway: #Or receiver or whatever
    pass

class SensorManager:
    MEASURE_PERIOD = 600 # 10 mins
    def __init__(self):
        self.devices = []
        self.periodic_manager = PeriodicExecManager()

    def measure(self, map: Grid):
        values = np.zeros(shape=(map.rows, map.cols, map.height)) # TODO: CHECK
        for d in self.devices:
            value = d.measure(map.grid3d[d.x][d.y][d.z].co2)
            print(value)
            if value is not None:
                values[d.x][d.y][d.z] = value
        return values

    def start(self):
        self.periodic_manager.add(self.MEASURE_PERIOD, self.measure)

    def run(self):
        self.periodic_manager.run()

    def place_sensor(self, x, y, z, device: Device):
        device.set_position(x, y, z)
        self.devices.append(device)
        print("placing sensor " + str(device.sensor_id) + " in " + str(x) + ", " + str(y) + ", " + str(z))
    
    def get_sensors_count(self):
        return len(self.devices)

