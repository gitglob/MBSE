"""
This file contains all the necessary functions that will be called during the main loop of the simulation 
in order to execute certain tasks.
"""
import pandas as pd
import os
import random
from Classes import *

dir_path = os.path.dirname(os.path.realpath('wind_months.csv'))
wind_month_day_df = pd.read_csv(dir_path + '\wind_months.csv', header=0)
wind_directions_distribution_df = pd.read_csv(dir_path + '\wind_directions_distribution.csv', header=0)

# calculate the CO2 for the entire grid
def calculate_co2():
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

def match_month(m):
    """
    Function to match integer to the corresponding month
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
def apply_wind_effect(direction, speed):
    # iterate over the entire grid
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                cell = city.grid3d[i][j][k]
                # check if the current cell has co2
                if cell.co2 > 0:
                    # find percentage of wind flowing to nearby cells and to which cells
                    pct, cells = match_direction(direction)

                    # find how many and which adjacent grid cells are free for the current cell
                    num_free_cells, adj_cells = find_num_free_adj_cells(city, i, j, k, "2d")

def match_direction(d):
    """
    function to match direction (east, west, north, south) to a percentage
    input:
        d -> direction of wind ('w', 'wnw', 'nw', 'nnw', 'n', 'nne', 'ne', 'ene', 'e', 'ese',	'se', 'sse', 's', 'ssw', 'sw', 'wsw')
    output:
        p -> list with percentage of wind flowing to adjacent cells
        c -> list with the corresponding adjacent cells that the wind flows to
    """
    if len(d) > 1:
        p = [0.5, 0.5]
    else:
        p = [1]

    if d == 'e':
        c = [[i+1]]
    elif d == 'w':
        c = [[i-1]]
    elif d == 'n':
        c = [[j+1]]
    elif d == 's':
        c = [[j-1]]

    elif d == 'ne':
        c = [[i+1, j+1]]
    elif d == "nw":
        c = [[i-1, j+1]]
    elif d == "se":
        c = [[i+1, j-1]]
    elif d == "sw":
        c = [[i-1, j-1]]

    elif d == "ene":
        c = [[i+1, j], [i+1, j+1]]
    elif d == "ese":
        c = [[i+1, j], [i+1, j-1]]
    elif d == "wnw":
        c = [[i-1, j], [i-1, j+1]]
    elif d == "wsw":
        c = [[i-1, j], [i-1, j-1]]
    elif d == "nne":
        c = [[i, j+1], [i+1, j+1]]
    elif d == "nnw":
        c = [[i, j+1], [i-1, j+1]]
    elif d == "sse":
        c = [[i, j-1], [i+1, j-1]]
    elif d == "ssw":
        c = [[i, j-1], [i-1, j-1]]

    return p, c

# apply air dispersion dynamics
def apply_co2_dispersion():
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                if city.grid3d[i][j][k].co2:
                    pass

# apply trees effect on co2 levels
def apply_trees_effect(city):
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
                    num_free_cells, adj_cells = find_num_free_adj_cells(city, i, j, k, "3d")

                    # how much co2 will be absorved from free adjacent cells
                    adj_cells_co2_absorbtion = sec_absorbtion/num_free_cells

                    # subtract the absorbed co2 from the free adjacent cells
                    for adj_cell in adj_cells:
                        ii = adj_cell[0]
                        jj = adj_cell[1]
                        kk = adj_cell[2]
                        city.grid3d[ii][jj][kk].co2 -= adj_cells_co2_absorbtion 

# Check for free adjacent cells in either 2d or 3d
def find_num_free_adj_cells(city, x, y, z, d): 
    """
    x, y, z: position of cell in 3d grid
    d: dimension of search - 2d or 3d
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

