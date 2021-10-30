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

    # initialize our 3d grid
    city = Grid(map_3d)
    print ("Our city is a: {} grid".format([len(city.grid3d), len(city.grid3d[0]), len(city.grid3d[0][0])]))

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
        wind_direction = f.calculate_wind_directions(wind_speed)
        # convert km/h to m/s
        wind_speed = float(wind_speed) * 1000 / 3600
        print('wind_speed: ', wind_speed, "(m/sec)")
        print('wind direction: ', wind_direction)

        # apply trees effect
        #f.apply_trees_effect(city)
        
        # calculate wind effect
        #f.apply_wind_effect(city, wind_direction, wind_speed)
        
        # apply dispersion
        #apply_co2_dispersion()

        # iterate over the entire grid
        #f.calculate_co2()

        if iteration == 0:
            simulation_flag = False

    return 0

    

if __name__ == "__main__":
    main()