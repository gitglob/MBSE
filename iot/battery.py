import math

class Battery:
    def __init__(self, cost, mAh):
        self.cost = cost
        self.mAh = mAh
    
    def discharge(self, amount):
        self.mAh -= amount

    def is_empty(self):
        return self.mAh <= 0
    
    def get_battery_level(self):
        return self.mAh

class BatteryList:
    CR2032 = Battery(1.1, 210)
    TestBattery = Battery(10, 2100)
    INFINITE = Battery(0, math.inf)
