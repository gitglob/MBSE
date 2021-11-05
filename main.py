'''
This is the main file, that executes the core loop of our simulation.
'''
import sys
from random import randint
import math

import environment.preprocessing as pre
import environment.simulation_functions as f
import environment.visualize as vis
from environment.classes import *
from iot import SensorManager

DEBUG = False
SENSOR_DISTANCE = 1

def debug(*args):
    if DEBUG:
        print(*args)

def main(argv):
    """
    argv[0]: Int - time to run the simulation, in days
    argv[1]: True/False or nonzero/0 - whether to produce debug messages
    """
    TIME_TO_RUN = int(argv[0])*3600*24
    DEBUG = bool(argv[1])
    
    city = Grid()
    print("Our city is a {} grid".format([len(city.grid3d), len(city.grid3d[0]),
        len(city.grid3d[0][0])]))
    vis.visualize_3d_grid(city)

    # extract the tree cells
    trees, roads, emptys = pre.extract_trees_roads_empty_blocks(city)

    sensor_manager = SensorManager(city)
    sensor_manager.distribute_sensors(SENSOR_DISTANCE)
    sensor_number = sensor_manager.get_sensors_count()
    print("Placed " + str(sensor_number) + " sensors")
    
    # run the simulation - Note: Every iteration is 1 second
    iteration = -1
    wind_speed_duration = 0
    score_values = []
    print("Running simulation for {} days (this might take a while) ... ".format(int(TIME_TO_RUN/3600)))
    while True:
        iteration += 1
        sec = iteration
        #print("iteration # ", iteration)
        
        # print the date every day        
        if iteration%86400 == 0:
            debug("Date: ", f.sec_to(iteration, "day")%30 + 1, "/", f.sec_to(iteration, "month")%12 + 1, "/", f.sec_to(iteration, "day")%24)

        # every hour generate new positions for cars
        if sec%3600 == 0:#21600 == 0:
            debug("Hour: ", f.sec_to(iteration, "hour")%24)
            cars = f.generate_cars(city, roads, time=1, max_cars=5000)
            vis.visualize_cars(city, cars)
            vis.visualize_co2(city, mesh=False, d=0)

        # cars generate co2
        f.generate_co2(cars, city)

        # every hour apply the wind effect and the trees effect
        if sec%3600 == 0:
            # calculate wind speed
            if wind_speed_duration == 0 or sec%wind_speed_duration == 0:
                wind_speed_km, wind_speed_duration = f.calculate_wind_speed(f.sec_to(iteration, "month")%12 + 1, sec)

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
            f.apply_diffusion_effect(city)

        #get a measure
        if sec % sensor_manager.MEASURE_PERIOD == 0:
            debug("Taking a measurement...")
            measures = sensor_manager.measure(city)
            co2_per_sensor = np.sum(measures) / sensor_number
            co2_per_cell = f.calculate_co2(roads, emptys) / (len(roads)+len(emptys))
            score_values.append(co2_per_sensor/co2_per_cell)

        if sec == TIME_TO_RUN:
            print()
            break
        # Is this efficient? It runs every second and does 100 iterations and 3 if statements
        # else:
        #     step = TIME_TO_RUN // 100
        #     for i in range(100):
        #         if sec == step*i:
        #             if DEBUG:
        #                 print(f"Simulation running... ({i}%)")
        #             else:
        #                 print(f"Simulation running... ({i}%)", end="\r")

    # calculate and print the total co2 in the city
    total_co2 = f.calculate_co2(roads, emptys)
    print("Total accumulated co2 in the city:", total_co2, "grams")
    total_measured_co2 = sensor_manager.get_total_co2()
    print("Total measured co2:", str(total_measured_co2), "grams")

    score = 0
    for s in score_values:
        score += 1 - abs(s-1)
    score = score * 100 / len(score_values)

    print(f"Average score of {round(score, 2)}% over {len(score_values)} samples")

    # after the simulation is done, visualize the co2 in the city
    vis.visualize_co2(city, mesh=True, d=3)

if __name__ == "__main__":
    main(sys.argv[1:])
