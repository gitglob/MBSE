'''
This file initializes the classes that we will use throughout the simulation.
'''
import numpy as np

# class for the entire grid
class Grid():
    def __init__(self, city_model):
        self.rows = np.shape(city_model)[0]
        self.cols = np.shape(city_model)[1]
        self.height = np.shape(city_model)[2]
        
        # initialize all the grid cells
        self.grid3d = []
        for i in range(0,self.rows):
            self.grid3d.append([])
            for j in range(0,self.cols):
                self.grid3d[i].append([])
                for k in range(0,self.height):
                    if city_model[i][j][k] == 't':
                        if i in [0, 1, self.rows-2, self.rows-1] or j in [0, 1, self.cols-2, self.cols-1]:
                            road_type = "high road"
                        else:
                            road_type = "inner road"
                        item = Road([i,j,k], road_type)
                    elif city_model[i][j][k] == 'g':
                        item = Tree([i,j,k])
                    elif city_model[i][j][k] == 'b':
                        item = Building([i,j,k])
                    elif city_model[i][j][k] == 'w':
                        item = Empty([i,j,k])
                        
                    self.grid3d[i][j].append(item)

# class that contains all the grid cells
class GridCell():
    def __init__(self, cell):
        self.x = cell[0] # x coordinate
        self.y = cell[1] # y coordinate
        self.z = cell[2] # z coordinate
        
        # boolean flags
        self.sensor_flag = False
        self.co2 = 0

        # variable that defines what is inside the cell
        self.contains = None

    # method that checks if the current cell is free
    def is_free():
        if (self.contains == "vehicle") or (self.contains == "empty") or (self.contains == "road"):
            return True
        else:
            return False

    def add_co2(self, co2):
        self.co2 += co2

    def remove_co2(self, co2):
        self.co2 -= co2

# building objects
class Building(GridCell):
    def __init__(self, cell):
        self.contains = 'building'

# road object
class Road(GridCell):
    def __init__(self, cell, road_type):
        super().__init__(cell)
        self.contains = 'road'
        self.road_type = road_type

        if road_type == "high road":
            self.speed = 19.44 #70 km/h = 19.44 m/s
        elif road_type == "inner road":
            self.speed = 8.33 #30 km/h = 8.33 m/s

# car objects
class Vehicle(Road):
    def __init__(self, cell, road_type):
        super().__init__(cell, road_type)
        self.contains = 'vehicle'
        self.fuel_co2_factor = 0
        self.consumption = 0

    def generate_co2(self, cell):
        co2 = self.consumption * self.speed * self.fuel_co2_factor / 100000
        cell.add_co2(co2)

# gasolin cars
class Gasolin_Car(Vehicle):
    def __init__(self, cell, road_type):
        super().__init__(cell, road_type)
        self.fuel_co2_factor = 33.64093867
        self.get_consumption()

    def get_consumption(self):
        if self.road_type == "high road":
            self.consumption = 5.5
        elif self.road_type == "inner road":
            self.consumption = 8

# diesel cars
class Diesel_Car(Vehicle):
    def __init__(self, cell, road_type):
        super().__init__(cell, road_type)
        self.fuel_co2_factor = 38.5354738
        self.get_consumption()

    def get_consumption(self):
        if self.road_type == "high road":
            self.consumption = 4.5
        elif self.road_type == "inner road":
            self.consumption = 6

# tree object
class Tree(GridCell):
    def __init__(self, cell):
        super().__init__(cell)
        self.contains = 'tree'

# empty object
class Empty(GridCell):
    def __init__(self, cell):
        super().__init__(cell)
        self.contains = 'empty'

