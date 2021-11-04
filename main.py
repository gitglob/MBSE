'''
This is the main file, that executes the core loop of our simulation.
'''
from random import randint
import math
import environment.preprocessing as pre
import environment.simulation_functions as f
import environment.visualize as vis
from environment.classes import *
from iot import SensorManager


SENSOR_DISTANCE = 1
TIME_TO_RUN = 3600*24
DEBUG = False


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

    sensor_manager = SensorManager(city)
    sensor_manager.distribute_sensors(SENSOR_DISTANCE)
    sensor_number = sensor_manager.get_sensors_count()
    print("Placed " + str(sensor_number) + " sensors")
    

    # run the simulation - Note: Every iteration is 1 second
    iteration = -1
    wind_speed_duration = 0
    score_values = []
    while True:
        iteration += 1
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
        current_month = month%12 + 2
        current_day = day%30 + 1
        current_hour = hour%24
        if iteration%86400 == 0:
            debug("Date: ", current_day, "/", current_month, "/", current_year)

        # every 6 hours generate new positions for cars
        if sec%21600 == 0:
            debug("Hour: ", current_hour)
            cars = f.generate_cars(city, roads, time=1, max_cars=5000)
            #vis.visualize_cars(city, cars)

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

        #get a measure
        if sec % sensor_manager.MEASURE_PERIOD == 0:
            debug("Taking a measure")
            measures = sensor_manager.measure(city)
            co2_per_sensor = np.sum(measures) / sensor_number
            co2_per_road_cell = f.calculate_co2(city) / len(roads)
            score_values.append(co2_per_sensor/co2_per_road_cell)


        if sec == TIME_TO_RUN:
            print()
            break
        else:
            step = TIME_TO_RUN // 100
            for i in range(100):
                if sec == step*i:
                    if DEBUG:
                        print(f"Simulation running... ({i}%)")
                    else:
                        print(f"Simulation running... ({i}%)", end="\r")

    # calculate and print the total co2 in the city
    total_co2 = f.calculate_co2(city)
    print("Total accumulated co2 in the city:", total_co2, "grams")
    total_measured_co2 = sensor_manager.get_total_co2()
    print("Total measured co2:", str(total_measured_co2), "grams")

    score = 0
    for s in score_values:
        score += 1 - abs(s-1)
    score = score * 100 / len(score_values)

    print(f"Average score of {round(score, 2)}% over {len(score_values)} samples")

    # after the simulation is done, visualize the co2 in the city
    #vis.visualize_co2(city, mesh=True, d=3)

if __name__ == "__main__":
    main()
