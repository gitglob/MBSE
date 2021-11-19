'''
This file initializes the classes that we will use throughout the simulation.
'''
import os

import numpy as np
from PIL import Image

# class for the entire grid
class Grid():
    ROAD = 278 # sum of brown rgb color
    TREE = 331 # sum of green rgb color
    BUILDING = 416 # sum of blue rgb color
    NOTHING = 765 # sum of white rgb color

    def __init__(self):
        self.city_model = self.load_from_png()
        self.rows = self.city_model.shape[0]
        self.cols = self.city_model.shape[1]
        self.height = self.city_model.shape[2]
        
        # initialize all the grid cells
        self.grid3d = []
        for i in range(0,self.rows):
            self.grid3d.append([])
            for j in range(0,self.cols):
                self.grid3d[i].append([])
                for k in range(0,self.height):
                    if self.city_model[i][j][k] == self.ROAD:
                        if i in [0, 1, self.rows-2, self.rows-1] or j in [0, 1, self.cols-2, self.cols-1]:
                            road_type = "high road"
                        else:
                            road_type = "inner road"
                        item = Road([i,j,k], road_type)
                    elif self.city_model[i][j][k] == self.TREE:
                        item = Tree([i,j,k])
                    elif self.city_model[i][j][k] == self.BUILDING:
                        item = Building([i,j,k])
                    elif self.city_model[i][j][k] == self.NOTHING:
                        item = Empty([i,j,k])
                        
                    self.grid3d[i][j].append(item)

    def load_from_png(self):
        im_frame = Image.open(os.path.join("model_data", "city.png"))
        data = np.array(im_frame.getdata())
        data = np.delete(data, -1, axis=1)
        data = np.reshape(data, (60, 60, 3))
        data = np.sum(data, axis=2)
        aux = np.empty((180, 180, 3), dtype=np.uint16)
        for i in range(aux.shape[0]):
            for j in range(aux.shape[1]):
                v = data[i//3][j//3]
                aux[i][j][0] = v
                if v == self.ROAD:
                    aux[i][j][1] = self.NOTHING
                    aux[i][j][2] = self.NOTHING
                else:
                    aux[i][j][1] = v
                    aux[i][j][2] = v
        return aux

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

        # here we save the co2 that is to be added due to the wind effect
        self.stashed_co2 = 0

    # method that checks if the current cell is free
    def is_free(self):
        if (self.contains == "vehicle") or (self.contains == "empty") or (self.contains == "road"):
            return True
        else:
            return False

    def add_co2(self, co2):
        self.co2 += co2

    def remove_co2(self, co2):
        if self.co2>0:
            if self.co2 > co2:
                self.co2 -= co2
            else:
                self.co2 = 0

    def stash_co2(self, co2):
        self.stashed_co2 += co2

    def merge_stashed_co2(self):
        self.co2 += self.stashed_co2
        if self.co2 < 0:
            self.co2 = 0
        self.reset_stash()

    def reset_stash(self):
        self.stashed_co2 = 0

    def empty_block(self):
        self.co2 = 0

# building objects
class Building(GridCell):
    def __init__(self, cell):
        super().__init__(cell)
        self.contains = 'building'

# road object
class Road(GridCell):
    def __init__(self, cell, road_type):
        super().__init__(cell)
        self.contains = 'road'
        self.road_type = road_type
        self.get_speed()

    def get_speed(self):
        if self.road_type == "high road":
            self.speed = 19.44 #70 km/h = 19.44 m/s
        elif self.road_type == "inner road":
            self.speed = 8.33 #30 km/h = 8.33 m/s

# car objects
class Vehicle(Road):
    def __init__(self, cell, road_type):
        super().__init__(cell, road_type)
        self.contains = 'vehicle'
        self.fuel_co2_factor = 0
        self.consumption = 0

    def generate_co2(self, cell, seconds):
        co2 = self.consumption * seconds * self.speed * self.fuel_co2_factor / 100000
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

