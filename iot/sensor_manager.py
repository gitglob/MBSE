import numpy as np


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


class SensorManager:
    MEASURE_PERIOD = 600 # 10 mins
    def __init__(self, city_nap):
        self.map = city_map
        self.devices = []
        self.periodic_manager = PeriodicExecManager()

    def measure(self):
        values = np.zeros(size=self.map.size()) # TODO: CHECK
        for d in self.devices:
            value = d.measure(self.map[d.x][d.y][d.z])
            if value is not None:
                values[d.x][d.y][d.z] = value

    def start(self):
        self.periodic_manager.add(self.MEASURE_PERIOD, self.measure)

    def run(self):
        self.periodic_manager.run()

