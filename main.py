'''
This is the main file, that executes the core loop of our simulation.
'''
from random import randint
import math
import time
import argparse
import csv

import environment.preprocessing as pre
import environment.simulation_functions as f
import environment.visualize as vis
from environment.classes import *
from iot import SensorManager
from iot import calculation
import matplotlib.pyplot as plt


# DEFAULT VALUES
TIME_TO_RUN     = 3600*24*3 # 1 day
SENSOR_DISTANCE = 30
SENSOR_PERIOD   = 1800
SENSOR_STATIC   = True
SAVE_PLOTS      = False
DEBUG           = False

results_path = "figures\\results\\results.csv"

def debug(*args):
    if DEBUG:
        print(*args)

def main():
    city = Grid()
    print("Our city is a {} grid".format([len(city.grid3d), len(city.grid3d[0]),
        len(city.grid3d[0][0])]))

    #vis.visualize_3d_grid(city)

    # extract the tree cells
    trees, roads, emptys = pre.extract_trees_roads_empty_blocks(city)

    sensor_manager = SensorManager(city, SENSOR_PERIOD)
    sensor_manager.distribute_sensors(SENSOR_DISTANCE)
    sensor_number = sensor_manager.get_sensors_count()
    print("Placed " + str(sensor_number) + " sensors")

    vis.visualize_sensor(city, sensor_manager.devices)

    # run the simulation - Note: Every iteration is 1 second
    sec = -1
    wind_speed_duration = 0
    wind_speed = 0
    wind_direction = None
    score_values = []
    real_values = []
    print("Running simulation for {} days (this might take a while) ... ".format(int(TIME_TO_RUN/3600/24)))

    # Profiling times
    t0 = 0
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0

    while True:
        sec += 1

        a0 = time.time()
        date = str((f.sec_to(sec, "hour")%24)) + ":" + str(f.sec_to(sec, "minute")%60) + ":" + str(sec%60) + " - " + str(f.sec_to(sec, "day")%30 + 1) + "/" + str(f.sec_to(sec, "month")%12 + 1) + "/" + str(f.sec_to(sec, "year") + 1)
        # print the date every day
        if sec%86400 == 0:
            debug("Date: ", date)

        # every hour generate new positions for cars
        if sec%21600 == 0:#21600 == 0:
            debug("Hour: ", f.sec_to(sec, "hour")%24)
            current_time = f.calculate_tz(f.sec_to(sec, "hour")%24)
            cars = f.generate_cars(city, roads, time=current_time, max_cars=5000)
            # vis.visualize_cars(city, cars)

        a1 = time.time()

        #every one hour visualize co2
        if sec%3600 == 0 and SAVE_PLOTS:
            vis.visualize_co2(city, mesh=False, d=0, wind_direction=wind_direction, wind_speed=wind_speed, date=date)

        a2 = time.time()

        # cars generate co2
        if sec % 60 == 0:
            f.generate_co2(cars, city, 60)

        a3 = time.time()

        # every hour apply the wind effect and the trees effect
        if sec%3600 == 0:
            # calculate wind speed
            if wind_speed_duration == 0 or sec%wind_speed_duration == 0:
                wind_speed_km, wind_speed_duration = f.calculate_wind_speed(f.sec_to(sec, "month")%12 + 1, sec)

            # calculate wind direction
            wind_direction = f.calculate_wind_directions(wind_speed_km)

            # convert wind_speed from km/h to m/s
            wind_speed = float(wind_speed_km) * 1000 / 3600
            #print('wind_speed: ', wind_speed, "(m/sec)")
            #print('wind direction: ', wind_direction)

            # calculate wind effect
            if SAVE_PLOTS:
                vis.visualize_wind_effect(city, wind_direction, wind_speed, date)
            f.apply_wind_effect(city, roads, emptys, wind_direction, wind_speed)
            if SAVE_PLOTS:
                vis.visualize_wind_effect(city, wind_direction, wind_speed, date)

            # apply trees effect
            if SAVE_PLOTS:
                vis.visualize_trees_effect(city, date)
            f.apply_trees_effect(city, trees)
            if SAVE_PLOTS:
                vis.visualize_trees_effect(city, date)

            # apply dispersion
            f.apply_diffusion_effect(city)

        a4 = time.time()

        if sec % 60 == 0:
            sensor_manager.measure(city, sec//60)

        #get a measure
        if sec % SENSOR_PERIOD == 0:
            debug("Taking gateway measurement...")
            measures = sensor_manager.gateway()
            co2_per_sensor = np.sum(measures) / sensor_number
            co2_per_cell = f.calculate_co2(roads) / (len(roads))
            score_values.append(1 - (abs(co2_per_sensor - co2_per_cell) /co2_per_cell))
            real_values.append(co2_per_cell)
            if not SENSOR_STATIC:
                debug("Moving sensors...")
                sensor_manager.shuffle_sensors(roads)

        a5 = time.time()
        t0 += a1 - a0
        t1 += a2 - a1
        t2 += a3 - a2
        t3 += a4 - a3
        t4 += a5 - a4

        if sec >= TIME_TO_RUN:
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

    # Print accumulated time
    print(f"Times: {round(t0, 2)} {round(t1, 2)}, {round(t2, 2)}, "
        + f"{round(t3, 2)}, {round(t4, 2)}")
    
    # calculate and print the total co2 in the city
    total_co2 = f.calculate_co2(roads)
    print("Total accumulated co2 in the city:", total_co2, "grams")
    total_measured_co2 = sensor_manager.get_total_co2()
    print("Total measured co2:", str(total_measured_co2), "grams")
    
    score = calculation.calculate_accuracy(score_values, real_values)
    
    #Save results in csv file
    with open(results_path, 'a+', newline = "") as file:
        writer = csv.writer(file, delimiter = ";")
        newline =  [str(sensor_manager.get_sensor_cost()*sensor_number), str(SENSOR_DISTANCE), str(SENSOR_STATIC), str(SENSOR_PERIOD), str(TIME_TO_RUN), str(round(score/100, 2))]
        writer.writerow(newline)
    file.close()
    


    print(f"Average score of {round(score, 2)}% over {len(score_values)} samples")
    print(f"Sensors: {sensor_number}")

    print("Cost per device:", str(sensor_manager.get_sensor_cost()))
    print("Total system cost:", str(sensor_manager.get_sensor_cost()*sensor_number))

    # after the simulation is done, visualize the co2 in the city
    vis.visualize_co2(city, mesh=True, d=3, wind_direction=wind_direction, wind_speed=wind_speed, date=date)


parser = argparse.ArgumentParser(description='CO2 Monitoring simulator.')
parser.add_argument('-d', '--days', type=float, default=TIME_TO_RUN/3600/24,
        help='Number of days to run.')
parser.add_argument('-n', '--sensor-distance', type=int, default=SENSOR_DISTANCE,
        help='Cell distance between sensors')
parser.add_argument('-p', '--sensor-period', type=int, default=SENSOR_PERIOD,
        help='Sensor measurement period in secs.')
parser.add_argument('-m', '--sensor-movement', type=str, default='static',
        choices=['static', 'random'], help='Sensors movement type.')
parser.add_argument('-s', '--save-plots', action='store_true',
        help='Save intermediate plots.')
parser.add_argument('-v', '--verbose', action='store_true',
        help='Activate debug logs.')



if __name__ == "__main__":
    args = parser.parse_args()
    TIME_TO_RUN = int(args.days * 3600 * 24)
    DEBUG = args.verbose
    SENSOR_DISTANCE = args.sensor_distance
    SENSOR_PERIOD = args.sensor_period
    SENSOR_STATIC = bool(args.sensor_movement == "static")
    SAVE_PLOTS = args.save_plots

    if SAVE_PLOTS:
        os.makedirs(os.path.join('figures', 'co2_timeseries'), exist_ok=True)

    main()
