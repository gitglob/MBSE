class Network:
    def __init__(self, cost, power_per_msg):
        self.cost = cost
        self.mAh = power_per_msg
        self.power_used = 0

    def send_msg(self):
        self.power_used += self.mAh

class NetworkList:
    LORA = Network(5, 1.7e-3) # 5€ 1.7e-3 mAh per msg
