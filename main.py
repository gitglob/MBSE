'''
This is the main file, that executes the core loop of our simulation.
'''
import argparse
import csv

import environment.preprocessing as pre
import environment.simulation_functions as f
import environment.visualize as vis
from environment.classes import *
from iot import SensorManager
from iot import calculation
import matplotlib.pyplot as plt
import pandas as pd


# DEFAULT VALUES
TIME_TO_RUN     = 3600*24*2 # 1 day
SENSOR_DISTANCE = 8
SENSOR_PERIOD   = 900
SENSOR_STATIC   = True
SAVE_PLOTS      = False
DEBUG           = False

# Not configurable
REAL_C02_PERIOD = 300 # 5 min


def debug(*args):
    if DEBUG:
        print(*args)

def main():
    city = Grid()
    print("Our city is a {} grid".format([len(city.grid3d), len(city.grid3d[0]),
        len(city.grid3d[0][0])]))

    vis.visualize_3d_grid(city)

    # extract the tree cells
    trees, roads, emptys, emptys_0 = pre.extract_trees_roads_empty_blocks(city)

    sensor_manager = SensorManager(city, SENSOR_PERIOD)
    sensor_manager.distribute_sensors(SENSOR_DISTANCE)
    sensor_number = sensor_manager.get_sensors_count()
    print("Placed " + str(sensor_number) + " sensors")

    # visualiza the sensor placement
    vis.visualize_sensor(city, sensor_manager.devices, SENSOR_STATIC, SENSOR_PERIOD, SENSOR_DISTANCE)

    # run the simulation - Note: Every iteration is 1 second
    sec = -1
    wind_speed_duration = 0
    wind_speed_km = 0
    wind_speed = 0
    wind_direction = None
    score_values = []
    real_values = []
    measured_values = []
    total_co2 = 0
    print("Running simulation for {} days (this might take a while) ... \n\n".format(TIME_TO_RUN/3600/24))

    # data for dataframe
    data = {
        'measured_co2/cell': [],
        'real_co2/cell': [],
        'timeframe': [],
        'sec': []
    }

    while True:
        sec += 1

        date = str((f.sec_to(sec, "hour")%24)) + ":" + str(f.sec_to(sec, "minute")%60) + ":" + str(sec%60) + " - " + str(f.sec_to(sec, "day")%30 + 1) + "/" + str(f.sec_to(sec, "month")%12 + 1) + "/" + str(f.sec_to(sec, "year") + 1)
        # print the date every day
        if sec%86400 == 0:
            print("\nDate: ", date)

        # calculate wind speed
        if wind_speed_duration == 0 or sec%wind_speed_duration == 0:
            wind_speed_km, wind_speed_duration = f.calculate_wind_speed(f.sec_to(sec, "month")%12 + 1, sec)
            debug("\t\t\tWIND SPEED :: ", wind_speed_km)
            debug(f"\t\t\tfor ...  {wind_speed_duration} secs ({wind_speed_duration/60/60} hours)")

            # calculate wind direction
            wind_direction = f.calculate_wind_directions(wind_speed_km)

            # convert wind_speed from km/h to m/s
            wind_speed = float(wind_speed_km) * 1000 / 3600
            debug('wind_speed: ', wind_speed, "(m/sec)")
            debug('wind direction: ', wind_direction)

        # every 6 hours generate new positions for cars
        if sec%21600 == 0:
            debug("Hour: ", f.sec_to(sec, "hour")%24)
            current_time = f.calculate_tz(f.sec_to(sec, "hour")%24)
            cars = f.generate_cars(city, roads, time=current_time, max_cars=5000)
            # vis.visualize_cars(city, cars)

        # cars generate co2 every minute
        if sec % 600 == 0:
            f.generate_co2(cars, city, 600)

        # every 10 mins apply the wind effect and the trees effect
        if sec % 600 == 0:
            debug(date)

            #every one hour visualize co2
            if SAVE_PLOTS:
                vis.visualize_co2(city, mesh=False, d=0, wind_direction=wind_direction, wind_speed=wind_speed, date=date)
                vis.visualize_co2(city, mesh=False, d=3, wind_direction=wind_direction, wind_speed=wind_speed, date=date)

            # apply dispersion
            if SAVE_PLOTS:
                vis.visualize_diffusion(city, date)
            f.apply_diffusion_effect(city, roads, emptys, 600)
            if SAVE_PLOTS:
                vis.visualize_diffusion(city, date)

            # calculate wind effect
            if SAVE_PLOTS:
                vis.visualize_wind_effect(city, wind_speed, wind_direction, date)
            #f.apply_wind_effect(city, roads, emptys_0, wind_direction, wind_speed)
            if SAVE_PLOTS:
                vis.visualize_wind_effect(city, wind_speed, wind_direction, date)

            # apply trees effect
            if SAVE_PLOTS:
                vis.visualize_trees_effect(city, date)
            f.apply_trees_effect(city, trees)
            if SAVE_PLOTS:
                vis.visualize_trees_effect(city, date)

            # calculate rain effect
            if SAVE_PLOTS:
                vis.visualize_rain_effect(city, date)
            rain_flag = f.rain(city)
            if SAVE_PLOTS and rain_flag:
                vis.visualize_rain_effect(city, date)

            print("co2 generated: ", f.calculate_co2(roads, emptys) - total_co2)
            total_co2 = f.calculate_co2(roads, emptys)
            print("Total co2:", total_co2, "\n")

        if sec % 60 == 0:
            sensor_manager.measure(city, sec//60)


        if sec % REAL_C02_PERIOD == 0:
            # We calculate co2 in the entire 0 floor of the city, that means both the roads and the empty space
            co2_per_cell = f.calculate_co2(roads, emptys_0) / (len(roads + emptys_0))
            real_values.append(co2_per_cell / 125)


        #get a measure
        if sec % SENSOR_PERIOD == 0:
            debug("Taking gateway measurement...")
            measures = sensor_manager.gateway()
            co2_per_sensor = np.sum(measures) / sensor_number
            measured_values.append(co2_per_sensor/125)
            real_co2_per_cell = f.calculate_co2(roads, emptys_0) / (len(roads + emptys_0))
            data['measured_co2/cell'].append(co2_per_sensor)
            data['real_co2/cell'].append(real_co2_per_cell)
            data['timeframe'].append(SENSOR_PERIOD)
            data['sec'].append(sec)
            if not SENSOR_STATIC:
                debug("Moving sensors...")
                sensor_manager.shuffle_sensors(roads)


        if sec >= TIME_TO_RUN:
            print()
            break


    # save a plot of co2 vs measured co2
    if SAVE_PLOTS:
        vis.visualize_co2_comparison(co2=real_values, co2_measured=measured_values, duration=TIME_TO_RUN, frequency=SENSOR_PERIOD)


    score = calculation.calculate_error(real_values, measured_values)
    accuracy = calculation.accuracy(real_values, measured_values)
    print("Average accuracy = ", accuracy*100, "%")

    #Save results in csv file
    newline =  [str(sensor_manager.get_sensor_cost(TIME_TO_RUN)*sensor_number), str(SENSOR_DISTANCE), str(sensor_number), str(SENSOR_STATIC), str(SENSOR_PERIOD), str(TIME_TO_RUN), str(round(score, 4)), str(round(accuracy, 4))]
    calculation.save_results(newline)

    # save data for simulation
    df = pd.DataFrame.from_dict(data)
    df.to_csv(os.path.join('figures', 'run_data', f'{TIME_TO_RUN}_{SENSOR_PERIOD}_{str(sensor_number)}_{SENSOR_STATIC}_{str(sensor_manager.get_sensor_cost(TIME_TO_RUN)*sensor_number)}.csv'), index=False)

    # after the simulation is done, visualize the co2 in the city
    vis.visualize_co2(city, mesh=True, d=3, wind_direction=wind_direction, wind_speed=wind_speed, date=date)
    vis.visualize_accuracy(real_values, REAL_C02_PERIOD, measured_values, SENSOR_PERIOD)
    # calculate and print the total co2 in the city
    total_co2 = f.calculate_co2(roads, emptys)
    print("Total accumulated co2 in the city:", total_co2, "grams")
    total_measured_co2 = sensor_manager.get_total_co2()
    print("Total measured co2:", str(total_measured_co2), "grams")

    print(f"Root-Mean-Square Error: {round(score, 4)}")
    print(f"Sensors: {sensor_number}")

    print("Energy per device fro 1 year:", str(sensor_manager.get_used_power(TIME_TO_RUN)), "mAh")
    print("Cost per device:", str(sensor_manager.get_sensor_cost(TIME_TO_RUN)), " [€]")
    print("Total system cost:", str(sensor_manager.get_sensor_cost(TIME_TO_RUN)*sensor_number), " [€]")


    # after the simulation is done, visualize the co2 in the city
    vis.visualize_co2(city, mesh=True, d=3, wind_direction=wind_direction, wind_speed=wind_speed, date=date)
    #calculation.evaluate()



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
    #SAVE_PLOTS = False

    #create needed folders
    folders = [
        'co2_comparison', 'co2_diffusion', 'co2_normalized_acc', 'co2_rain_effect', 'co2_timeseries', 'co2_3d', 
        'co2_trees_effect', 'co2_wind_effect', 'results', 'city_model', 'sensor_placement'
    ]
    for folder in folders:
        os.makedirs(os.path.join('figures', f'{folder}'), exist_ok=True)

    os.makedirs(os.path.join('figures', 'run_data'), exist_ok=True)
    main()
