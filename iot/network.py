class Network:
    def __init__(self, cost, power_usage, time_per_msg):
        self.power_usage = power_usage
        self.recv_buffer = []
        self.time_per_msg = time_per_msg
        self.power_consumed = 0.0
        self.cost = cost

    def receive_data(self, msg):
        self.recv_buffer.append(msg)
        self.power_consumed = self.power_consumed + self.power_usage * self.time_per_msg
    
    def empty_buffer(self):
        for msg in self.recv_buffer:
            self.send_msg(msg)
        self.recv_buffer.clear()
    
    def send_msg(self, msg):
        self.power_consumed = self.power_consumed + self.power_usage * self.time_per_msg

    def get_power_consumed(self):
        value = self.power_consumed
        self.power_consumed = 0.0
        return value

class NetworkList:
    LORA = Network(10, 60, 2.8*10**-6) #mAh

