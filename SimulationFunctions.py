'''
This file contains all the necessary functions that will be called during the main loop of the simulation 
in order to execute certain tasks.
'''
import pandas as pd
import os
import random
from Classes import *

dir_path = os.path.dirname(os.path.realpath('wind_months.csv'))
wind_month_day_df = pd.read_csv(dir_path + '\wind_months.csv', header=0)
wind_directions_distribution_df = pd.read_csv(dir_path + '\wind_directions_distribution.csv', header=0)
# print(wind_month_day_df.[month]())

# calculate the CO2
def calculate_co2():
    # calculate car emissions
    co2_sum = 0
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                if city.grid3d[i][j][k].car_flag:
                    co2_sum += city.grid3d[i][j][k].co2
                    pass

# calculate the wind speed based on the date
def calculate_wind_speed(month, secs):
    secs = secs % 2628000
    month_name = match_month(month)
    col = wind_month_day_df[month_name]
    # print(month_name)
    
    for i, num_days in enumerate(col[:-1]): 
        num_secs = num_days * 86400
        if secs < num_secs:
            wind_speed = wind_month_day_df['Wind Speed (km/h)'][i]

    return wind_speed

def calculate_wind_directions(wind_speed):
    directions = ['w', 'wnw', 'nw', 'nnw', 'n', 'nne', 'ne', 'ene', 'e', 'ese',	'se', 'sse', 's', 'ssw', 'sw', 'wsw']
    # distribution of each wind speed
    row = wind_directions_distribution_df[wind_month_day_df['Wind Speed (km/h)'] == wind_speed]
    row = row.iloc[0,1:].tolist()
    wind_direction = random.choices(directions, weights=row, k=1)

    return wind_direction[0]

def match_month(m):
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
def apply_wind():
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                if city.grid3d[i][j][k].co2:
                    pass

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
    sec_absorbtion = year_absorbtion/(86400*30*12)

    # iterate over the 3d grid
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                # check if the current grid cell is a tree
                if isinstance(city.grid3d[i][j][k], Tree):
                    # find how many adjacent grid cells are empty for every tree
                    num_free_cells, adj_cells = find_num_free_adj_cells(city, i, j, k, "3d")



# Check for free adjacent cells in either 2d or 3d
def find_num_free_adj_cells(city, i, j, k, d): 
'''
i, j, k: position of cell in 3d grid
d: dimension of search - 2d or 3d
'''
    num_free_cells = 0
    adj_cells = []
    if d == "2d":
        if citty.grid3d[i][j-1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j-1,k]
        if citty.grid3d[i][j+1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j+1,k]
        if citty.grid3d[i-1][j][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j,k]
        if citty.grid3d[i+1][j][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j,k]
        if citty.grid3d[i-1][j-1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j-1,k]
        if citty.grid3d[i+1][j+1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j+1,k]
        if citty.grid3d[i+1][j-1][k]].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j-1,k]
        if citty.grid3d[i-1][j+1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j+1,k]
    elif d = "3d":
        if citty.grid3d[i][j-1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j-1,k]
        if citty.grid3d[i][j+1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j+1,k]
        if citty.grid3d[i][j][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j,k-1]
        if citty.grid3d[i][j][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j,k+1]
        if citty.grid3d[i][j-1][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j-1,k-1]
        if citty.grid3d[i][j+1][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j+1,k+1]
        if citty.grid3d[i][j-1][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j-1,k+1]
        if citty.grid3d[i][j+1][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i,j+1,k-1]

        if citty.grid3d[i-1][j][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j,k]
        if citty.grid3d[i+1][j][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j,k]
        if citty.grid3d[i-1][j][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j,k-1]
        if citty.grid3d[i+1][j][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j,k+1]
        if citty.grid3d[i-1][j][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j,k+1]
        if citty.grid3d[i+1][j][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j,k-1]

        if citty.grid3d[i+1][j+1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j+1,k]
        if citty.grid3d[i-1][j-1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j-1,k]
        if citty.grid3d[i-1][j+1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j+1,k]
        if citty.grid3d[i+1][j-1][k].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j-1,k]

        if citty.grid3d[i+1][j+1][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j+1,k+1]
        if citty.grid3d[i+1][j-1][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j-1,k-1]
        if citty.grid3d[i+1][j-1][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j-1,k+1]
        if citty.grid3d[i+1][j+1][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i+1,j+1,k-1]
        if citty.grid3d[i-1][j+1][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j+1,k+1]
        if citty.grid3d[i-1][j+1][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j+1,k-1]
        if citty.grid3d[i-1][j-1][k-1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j-1,k-1]
        if citty.grid3d[i-1][j-1][k+1].contains == "road" or city.grid3d[i-1][j][k].contains == "Empty":
            num_free_cells += 1
            adj_cells.append[i-1,j-1,k+1]

    return num_free_cells, adj_cells

        




