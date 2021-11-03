'''
This is the main file, that executes the core loop of our simulation.
'''

import Preprocessing as pre
import SimulationFunctions as f
import Visualize as vis
from Classes import *

def main():
    # reading our model file and creating the object structure
    map_1d = pre.read_png_file()
    map_2d, rows, cols, height = pre.convert_1d_grid_to_2d(map_1d)
    map_3d, rows, cols, height = pre.convert_2d_grid_to_3d(map_2d, rows, cols, height)

    # initialize our 3d grid
    city = Grid(map_3d)
    print ("Our city is a: {} grid".format([len(city.grid3d), len(city.grid3d[0]), len(city.grid3d[0][0])]))
    #vis.visualize_3d_grid(city)

    # extract the tree cells
    trees, roads, emptys = pre.extract_trees_roads_empty_blocks(city)

    # run the simulation - Note: Every iteration is 1 second
    simulation_flag = True
    iteration = -1
    wind_speed_duration = 0

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
        current_year = year + 1
        current_month = month%12 + 1
        current_day = day%30 + 1
        current_hour = hour%24
        if iteration%86400 == 0:
            print("Date: ", current_day, "/", current_month, "/", current_year)

        # every 6 hours generate new positions for cars
        if sec%21600 == 0:
            print("Hour: ", current_hour)
            cars = f.generate_cars(city, roads, time=1, max_cars=5000)
            #vis.visualize_cars(city, cars)
            vis.visualize_co2(city, mesh=False, d=0)

        # cars generate co2
        f.generate_co2(cars, city)

        # every hour apply the wind effect and the trees effect
        if sec%3600 == 0:
            # calculate wind speed
            if wind_speed_duration == 0 or sec%wind_speed_duration == 0:
                wind_speed_km, wind_speed_duration = f.calculate_wind_speed(current_month, sec)

            # calculate wind direction
            wind_direction = f.calculate_wind_directions(wind_speed_km)

            # convert wind_speed from km/h to m/s
            wind_speed = float(wind_speed_km) * 1000 / 3600
            #print('wind_speed: ', wind_speed, "(m/sec)")
            #print('wind direction: ', wind_direction)

            # calculate wind effect
            f.apply_wind_effect(city, roads, emptys, wind_direction, wind_speed)
        
            # apply trees effect
            f.apply_trees_effect(city, trees)

        # apply dispersion
        #f.apply_co2_dispersion()

        if day == 10:
            simulation_flag = False

    # calculate and print the total co2 in the city
    total_co2 = f.calculate_co2(city)
    print("Total accumulated co2 in the city:", total_co2, "grams")

    # after the simulation is done, visualize the co2 in the city
    vis.visualize_co2(city, mesh=True, d=3)

    return 0

if __name__ == "__main__":
    main()