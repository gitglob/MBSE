'''
This file contains all the necessary functions that will be called during the main loop of the simulation 
in order to execute certain tasks.
'''
import pandas as pd
import os
import random

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
                    
def generate_co2():
    for car in cars:
        car.generate_co2()