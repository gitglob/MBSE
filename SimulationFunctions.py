"""
This file contains all the necessary functions that will be called during the main loop of the simulation 
in order to execute certain tasks.
"""
import pandas as pd
import os
import random
from Classes import *
from math import sqrt

# here we read once the necessary csv files with the information about wind in Copenhagen
dir_path = os.path.dirname(os.path.realpath('wind_months.csv'))
wind_month_day_df = pd.read_csv(dir_path + '\wind_months.csv', header=0)
wind_directions_distribution_df = pd.read_csv(dir_path + '\wind_directions_distribution.csv', header=0)

def generate_cars(city, time, max_cars):
    """
    
    """
    print("Generating cars...")
    city_size = city.rows

    # list of car objects
    cars = []

    # time zones
    if time == 1: time_zone_car_percentage = 0.1  # 0-6
    if time == 2: time_zone_car_percentage = 1    # 6-12
    if time == 3: time_zone_car_percentage = 1    # 12-18
    if time == 4: time_zone_car_percentage = 0.5  # 18-24

    # calculate number of cars based on time
    max_cars *= time_zone_car_percentage

    # city zones
    city_zone1 = {'bound': city_size/6, 'probability': 0.3, 'roads': 0} 
    city_zone2 = {'bound': city_size/3, 'probability': 0.2, 'roads': 0}
    city_zone3 = {'bound': city_size/2, 'probability': 0.5, 'roads': 0}

    # number of roads in each zone
    for x in range(city_size):
        for y in range(city_size):
            if city.grid3d[x][y][0].contains == 'road':
                if x < city_zone1['bound'] or x > city_size - city_zone1['bound'] and y < city_zone1['bound'] or y > city_size - city_zone1['bound']:
                    city_zone1['roads'] += 1
                elif x < city_zone2['bound'] or x > city_size - city_zone2['bound'] and y < city_zone2['bound'] or y > city_size - city_zone2['bound']:
                    city_zone2['roads'] += 1
                else:
                    city_zone3['roads'] += 1

    # calculate new probabilities
    city_zone1['probability'] = max_cars * city_zone1['probability'] / city_zone1['roads']
    city_zone2['probability'] = max_cars * city_zone2['probability'] / city_zone2['roads']
    city_zone3['probability'] = max_cars * city_zone3['probability'] / city_zone3['roads']

    #generate cars based on the probability for each zone
    for x in range(city_size):
        for y in range(city_size):
            if city.grid3d[x][y][0].contains == 'road':
                if x < city_zone1['bound'] or x > city_size - city_zone1['bound'] and y < city_zone1['bound'] or y > city_size - city_zone1['bound']:
                    if random.random() < city_zone1['probability']:
                        if random.random() < 0.5:
                            car = Gasolin_Car([x, y, 0], city.grid3d[x][y][0].road_type)
                        else:
                            car = Diesel_Car([x, y, 0], city.grid3d[x][y][0].road_type)
                        cars.append(car)
                elif x < city_zone2['bound'] or x > city_size - city_zone2['bound'] and y < city_zone2['bound'] or y > city_size - city_zone2['bound']:
                    if random.random() < city_zone2['probability']:
                        if random.random() < 0.5:
                            car = Gasolin_Car([x, y, 0], city.grid3d[x][y][0].road_type)
                        else:
                            car = Diesel_Car([x, y, 0], city.grid3d[x][y][0].road_type)
                        cars.append(car)
                else:
                    if random.random() < city_zone3['probability']:
                        if random.random() < 0.5:
                            car = Gasolin_Car([x, y, 0], city.grid3d[x][y][0].road_type)
                        else:
                            car = Diesel_Car([x, y, 0], city.grid3d[x][y][0].road_type)
                        cars.append(car)

    return cars

# calculate the CO2 for the entire grid
def calculate_co2(city):
    # calculate car emissions
    co2_sum = 0
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                if city.grid3d[i][j][k].is_free():
                    co2_sum += city.grid3d[i][j][k].co2
                    
    return(co2_sum)

# calculate the wind speed based on the date
def calculate_wind_speed(month, secs):
    """
    Function that calculates the wind speed of a city based on the month and the amount of time that has passed in that month.

    Input:
        month -> integer inside [1, 12]
        secs -> amount of seconds that have passed in that month [0, 2.592.000]
    Output:
        wind_speed -> speed of wind (km/h)
    """
    secs = secs % 2628000
    month_name = match_month(month)
    col = wind_month_day_df[month_name]
    
    # calculate the wind speed 
    for i, num_days in enumerate(col[:-1]): 
        num_secs = num_days * 86400
        if secs < num_secs:
            wind_speed = wind_month_day_df['Wind Speed (km/h)'][i]

    return wind_speed

# calculate the wind direction
def calculate_wind_directions(wind_speed):
    """
    This function calculates the wind direction. As a general rule:
    east -> i+
    west -> i-
    north -> j+
    south -> j-

    Input:
        wind_speed -> wind speed in km/h
    Output:
        wind_direction[0] -> a string that shows the direction of the wind (i.e. 'n', or "nne", or "ne", or "ene" ...)
    """

    # possible wind directions
    directions = ['w', 'wnw', 'nw', 'nnw', 'n', 'nne', 'ne', 'ene', 'e', 'ese',	'se', 'sse', 's', 'ssw', 'sw', 'wsw']
    
    # distribution of each wind speed
    col = wind_month_day_df['Wind Speed (km/h)'][:-1]
    mask = col == wind_speed
    row = wind_directions_distribution_df[mask]
    row = row.iloc[0,1:].tolist()

    # calculate the wind direction based on a custom random distribution
    wind_direction = random.choices(directions, weights=row, k=1)

    return wind_direction[0]

# match month from integer to string
def match_month(m):
    """
    Function to match integer to the corresponding month.

    Input:
        m -> Integer, corresponds to month [1,12].
    Output:
        string that haw the name of the month that corresponds to the input integer.
    """
    if m == 1:
        return "January"
    elif m == 2:
        return "February"
    elif m == 3:
        return "March"
    elif m == 4: 
        return "April"
    elif m == 5:  
        return "May"
    elif m == 6:  
        return "June"
    elif m == 7:  
        return "July"
    elif m == 8:  
        return "August"
    elif m == 9: 
        return "September"
    elif m == 10: 
        return "October"
    elif m == 11: 
        return "November"
    elif m == 12: 
        return "December"
        
# apply wind effect
def apply_wind_effect(city, direction, speed):
    """
    Function that applies the effect of wind to the co2 inside a 3d city model.

    Input:
        city -> the 3d grid of the model of our city as a 3d list with objects of grid_cell inside
        direction -> the wind direction ('w', 'wnw', 'nw', 'nnw', 'n', 'nne', 'ne', 'ene', 'e', 'ese',	'se', 'sse', 's', 'ssw', 'sw', 'wsw')
        speed -> the wind speed (m/sec)
    Output:
        none, changes the city object
    """

    # iterate over the entire grid
    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                cell = city.grid3d[i][j][k]
                # check if the current cell has co2
                if cell.co2 > 0:
                    # find how many and which adjacent grid cells are free for the current cell
                    _, adj_cells = find_free_adj_cells(city, i, j, k, "2d")

                    # find which cells the wind flows towards
                    flow_cells = match_direction(direction, i, j, k)

                    # check if the wind flows to 1 cell
                    if len(flow_cells) == 1:
                        # check if that cell is free
                        if flow_cells.is_free():
                            # and give it all the co2 this cell contains
                            city.grid3d[flow_cells[0]][flow_cells[1]][flow_cells[2]] += cell.co2
                        # if the flow cell is not free
                        else:
                            # find the closest free cells to it
                            closest_free_cells = find_closest_free_cells(flow_cells, adj_cells)
                            # if there is exactly 1 free cell closest to the flow cell
                            if len(closest_free_cells) == 1:
                                city.grid3d[closest_free_cells[0]][closest_free_cells[1]][closest_free_cells[2]] += cell.co2
                            else:
                                # if there are 2 adjacent free cells that are the closest to the flow cell
                                for free_cell in closest_free_cells:
                                    city.grid3d[free_cell[0]][free_cell[1]][free_cell[2]] += 0.5*cell.co2
                    # else, if the wind flows to 2 cells
                    else:
                        # for every flow cell
                        for flow_cell in flow_cells:
                            # check if the cell is free
                            if flow_cell.is_free():
                                # and give it half the co2 this cell contains if it is
                                city.grid3d[flow_cell[0]][flow_cell[1]][flow_cell[2]] += 0.5*cell.co2
                            else:
                                # if it isn't free, check which is the closest free cell to it
                                closest_free_cells = find_closest_free_cells(flow_cells, adj_cells)
                                # if there is exactly 1 free cell closest to the flow cell give it 50% of the co2
                                if len(closest_free_cells) == 1:
                                    city.grid3d[closest_free_cells[0]][closest_free_cells[1]][closest_free_cells[2]] += 0.5*cell.co2
                                # else there are 2 free cells that are the closest to the flow cell
                                else:
                                    # give 25% of co2 to each
                                    for free_cell in closest_free_cells:
                                        city.grid3d[free_cell[0]][free_cell[1]][free_cell[2]] += 0.25*cell.co2

                # since the co2 moved to nearby cells, this cell has now 0 co2 again
                cell.co2 = 0

# find the closest free cells
def find_closest_free_cells(cell, adj_cells):
    """
    Function that finds the closest free grid cell to the current one based on euclidean distance.

    Input:
        cell -> 1d integer list of current cell index ([i, j, k])
        adj_cells -> 2d integer list of free adjacent cells ([[i+1, j, k][i-1, j, k], ...])
    Output:
        closest_cells -> 2d integer list of the closest cell(s) based on euclidean distance ([[i+1, j, k], [i, j+1, k], ...])
    """
    # find the euclidean distance for all the adjacent cells
    euc_distance_list = []
    for c in adj_cells:
        euc_distance = sqrt((cell[0] - c[0])**2 + (cell[1] - c[1])**2 + (cell[2] - c[2])**2)
        euc_distance_list.append(euc_distance)

    # find the minimum euclidean distance
    min_euc_distance = min(euc_distance_list)

    # get all the closest elements
    closest_cells = []
    for index, d in enumerate(euc_distance_list):
        if d == min_euc_distance:
            closest_cells.append(adj_cells[index])

    return closest_cells

# match wind direction to adjacent cell
def match_direction(d, i, j, k):
    """
    Function to match wind direction (east, west, north, south) to a adjacent cell

    input:
        d -> direction of wind ('w', 'wnw', 'nw', 'nnw', 'n', 'nne', 'ne', 'ene', 'e', 'ese',	'se', 'sse', 's', 'ssw', 'sw', 'wsw')
    output:
        c -> 2d list with the corresponding adjacent cells that the wind flows to
    """

    if d == 'e':
        c = [[i+1, j, k]]
    elif d == 'w':
        c = [[i-1, j, k]]
    elif d == 'n':
        c = [[j+1, j, k]]
    elif d == 's':
        c = [[j-1, j, k]]

    elif d == 'ne':
        c = [[i+1, j+1, k]]
    elif d == "nw":
        c = [[i-1, j+1, k]]
    elif d == "se":
        c = [[i+1, j-1, k]]
    elif d == "sw":
        c = [[i-1, j-1, k]]

    elif d == "ene":
        c = [[i+1, j, k], [i+1, j+1, k]]
    elif d == "ese":
        c = [[i+1, j, k], [i+1, j-1, k]]
    elif d == "wnw":
        c = [[i-1, j, k], [i-1, j+1, k]]
    elif d == "wsw":
        c = [[i-1, j, k], [i-1, j-1, k]]
    elif d == "nne":
        c = [[i, j+1, k], [i+1, j+1, k]]
    elif d == "nnw":
        c = [[i, j+1, k], [i-1, j+1, k]]
    elif d == "sse":
        c = [[i, j-1, k], [i+1, j-1, k]]
    elif d == "ssw":
        c = [[i, j-1, k], [i-1, j-1, k]]

    return c

# apply air dispersion dynamics
def apply_co2_dispersion():
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                if city.grid3d[i][j][k].co2:
                    pass
                    
def generate_co2(cars, city):
    for car in cars:
        car.generate_co2(city.grid3d[car.x][car.y][car.z])

# apply trees effect on co2 levels
def apply_trees_effect(city):
    """
    Function that applies the effect that trees have to co2.

    Input:
        city -> the 3d grid of the model of our city as a 3d list with objects of grid_cell inside
    Output:
        none, changes the city object
    """
    # a tree roughly absorbs 48 pounds of co2 per year (21,7724 kg)
    year_absorbtion = 15 # we will consider a mature tree, but not a huge one, because we are in a city, so ~15kg/year 
    sec_absorbtion = year_absorbtion/(86400*30*12) # we might need an hourly absorbtion, to reduce the computation time

    # iterate over the 3d grid
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                # check if the current grid cell is a tree
                if city.grid3d[i][j][k].contains == "tree":
                    # find how many adjacent grid cells are free for every tree
                    num_free_cells, adj_cells = find_free_adj_cells(city, i, j, k, "3d")

                    # how much co2 will be absorved from free adjacent cells
                    adj_cells_co2_absorbtion = sec_absorbtion/num_free_cells

                    # subtract the absorbed co2 from the free adjacent cells
                    for adj_cell in adj_cells:
                        ii = adj_cell[0]
                        jj = adj_cell[1]
                        kk = adj_cell[2]
                        city.grid3d[ii][jj][kk].co2 -= adj_cells_co2_absorbtion 

# Check for free adjacent cells in either 2d or 3d
def find_free_adj_cells(city, x, y, z, d): 
    """
    Function that finds the number and the position of the free adjacent cells for a city grid block in 2d or 3d.
    
    Input:
        city -> 3d grid of model of a city in the form of 3d list with grid_cell objects as elements
        x, y, z -> position of cell in 3d grid
        d -> dimension of search - 2d or 3d
    Output:
        num_free_cells -> number that shows how many adjacent free cells there are
        adj_cells -> 2d list that contains [i, j, k] elements with the position of the adjacent cells
    """

    # chck if this is a corner cell
    corner_x_flag = False
    corner_y_flag = False
    corner_z_flag = False
    if x == 0 or x == len(city.grid3d[0]):
        corner_x_flag = True
    if y == 0 or y == len(city.grid3d[0][0]):
        corner_y_flag = True
    if z == 0 or z == len(city.grid3d[0][0][0]):
        corner_z_flag = True

    # count the # of adjacent cells in 2d or 3d
    num_free_cells = 0
    adj_cells = []
    if d == "2d":
        for i in [x, x-1, x+1]:
            for j in [y, y-1, y+1]:
                if (i==x and j==y) or ((i==x+1 or i==x-1) and corner_x_flag) or ((j==y-1 or j==y+1) and corner_y_flag):
                    continue
                k = z
                index = [i, j, k]
                cell = city.grid3d[i][j][k]
                if cell.is_free():
                    num_free_cells += 1
                    adj_cells.append[index]
    elif d == "3d":
        for i in [x, x-1, x+1]:
            for j in [y, y-1, y+1]:
                for k in [z, z-1, z+1]:
                    if (i==x and j==y and z==k) or ((i==x+1 or i==x-1) and corner_x_flag) or ((j==y-1 or j==y+1) and corner_y_flag) or ((k==z-1 or k==z+1) and corner_z_flag):
                        continue
                    index = [i, j, k]
                    cell = city.grid3d[i][j][k]
                    if cell.is_free():
                        num_free_cells += 1
                        adj_cells.append[index]

    return num_free_cells, adj_cells
