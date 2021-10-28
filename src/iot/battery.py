class Battery :
    cost = 0.0
    watt = 0.0
    def __init__(self, cost, watt):
        self.cost = cost
        self.watt = watt
    
    def discharge(self, amount):
        self.watt -= amount