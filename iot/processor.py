from time import time
class Processor:

    #power usage is the amount of power consumed per ms
    def __init__(self, cost, power_usage):
        self.cost = cost
        self.power_usage = power_usage#mAh / hour
        self.running = False
        self.starting_time = 0.0
        self.stopping_time = 0.0
    
    def start(self):
        if self.running:
            return
        self.running = True
        self.starting_time = time()
    
    def stop(self):
        if not self.running:
            return
        self.running = False
        self.stopping_time = time()
    
    def get_power_consumed(self):
        return self.power_usage * (self.stopping_time - self.starting_time) / 3600
    

class ProcessorList:
    ESP32 = Processor(8, 120)