import math


class Battery:
    def __init__(self, cost, mAh):
        self.cost = cost
        self.mAh = mAh
    

class BatteryList:
    CR2032 = Battery(1.1, 210)
    RCR123A = Battery(3.2, 750)
    CR2A = Battery(4, 1200)
    CR123 = Battery(5, 1500)
    S25R = Battery(7, 2500)
    PLUGGED = Battery(100, math.inf)

def get_best_battery(mAh_used):
    best = BatteryList.PLUGGED
    name = "PLUGGED"
    for  attr_name in dir(BatteryList):
        attr = getattr(BatteryList, attr_name)
        if isinstance(attr, Battery):
            if attr.mAh >= mAh_used and attr.mAh < best.mAh:
                best = attr
                name = attr_name
    return name, best
