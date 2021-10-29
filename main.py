'''
This is the main file, that executes the core loop of our simulation.
'''

import Preprocessing as pre
import SimulationFunctions as f
from Classes import *

def main():
    map_1d = pre.read_png_file()
    map_2d, rows, cols, height = pre.convert_1d_grid_to_2d(map_1d)
    map_3d, rows, cols, height = pre.convert_2d_grid_to_3d(map_2d, rows, cols, height)
    pre.visualize_3d_grid(map_3d, rows, cols, height)

    model = Grid(map_3d)

    # run the simulation - Note: Every iteration is 1 second
    simulation_flag = True
    iteration = -1

    while (simulation_flag):
        iteration +=1
        #print("iteration # ", iteration)
        
        # update the date
        year = iteration // (86400*30*12)
        month = iteration // (86400*30)
        week = iteration // (86400*7)
        day = iteration // (86400)
        hour = iteration // 3600
        minute = iteration // 60
        sec = iteration

        # calculate date starting from 1/1/1
        current_month = month%12 + 1
        current_day = day%30 + 1
        current_year = year + 1
        if iteration%86400 == 0:
            print("Date: ", current_day, "/", current_day, "/", current_year)

        # calculate wind speed
        wind_speed = f.calculate_wind_speed(current_month, sec)
        print('wind_speed: ', wind_speed)
        wind_direction = f.calculate_wind_directions(wind_speed)
        print('wind direction: ', wind_direction)
        if iteration == 2:
            simulation_flag=False

        # apply trees effect
        f.apply_trees_effect(model)

        # iterate over the entire grid
        #calculate_co2()
        
        # calculate wind effect
        #apply_wind()
        
        # apply dispersion
        #apply_co2_dispersion()

    return 0

if __name__ == "__main__":
    main()