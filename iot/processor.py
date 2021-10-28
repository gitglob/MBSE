class Processor:
    cost = 0.0
    power_usage = 0.0
    running = False

    def __init__(self, cost, power_usage):
        self.cost = cost
        self.power_usage = power_usage
    
    def start(self):
        self.running = True
    
    def stop(self):
        self.running = False
