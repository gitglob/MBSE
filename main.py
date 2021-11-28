'''
This is the main file, that executes the core loop of our simulation.
'''
import sys
import csv
import os
import pandas as pd
from random import randint
import math
import environment.preprocessing as pre
import environment.simulation_functions as f
import environment.visualize as vis
from environment.classes import *
from iot import SensorManager
from iot import calculation
from pprint import pprint
from gui.gui import GUI
import tkinter as tk


def main():
    #%% GUI
    root = tk.Tk()
    root.geometry("971x828")
    root.title("AIR POLLUTION SIMULATION")
    bg = tk.PhotoImage(file="pollution.png")
    my_canvas = tk.Canvas(root, width=971, height=828)
    my_canvas.pack()
    my_canvas.create_image(0, 0, image=bg, anchor="nw")
    my_canvas.create_text(470, 584, text="Air Pollution Simulation", font=(
        "Helvetica", 50), fill="white")
    app = GUI(root, my_canvas)
    root.mainloop()

#%%
    # pprint(vars(app))
    running_time_in_days = int(app.days)
    SAVE_PLOTS = app.save_plots
    SENSOR_DISTANCE = int(app.sensors_distance)
    SENSOR_PERIOD = int(app.sensors_period)
    SENSOR_STATIC = int(app.sensors_movement)
    DEBUG = app.debug

    results_path = "figures\\results\\results.csv"
    folders = ['co2_comparison', 'co2_diffusion', 'co2_normalized_acc', 'co2_rain_effect',
               'co2_timeseries', 'co2_trees_effect', 'co2_wind_effect', 'co2_3d', 'run_data' 'results', 'city_model', 'sensor_placement']
    try:
        os.mkdir("figures")
    except FileExistsError:
        pass

    if SAVE_PLOTS:
        for folder in folders:
            try:
                os.mkdir("figures/" + folder)
            except FileExistsError:
                pass

    if DEBUG:
        print("TIME TO RUN:", running_time_in_days,
              "\nSENSORS DISTANCE IN METERS:", SENSOR_DISTANCE,
              "\nSENSORS SAMPLING PERIOD IN SECONDS", SENSOR_PERIOD,
              "\nSAVE_PLOTS:", SAVE_PLOTS)

    TIME_TO_RUN = running_time_in_days * 3600 * 24
    if TIME_TO_RUN != 0:
        city = Grid()
        print("Our city is a {} grid".format([len(city.grid3d), len(city.grid3d[0]),
                                              len(city.grid3d[0][0])]))

        vis.visualize_3d_grid(city)

        # extract the tree cells
        trees, roads, emptys, emptys_0 = pre.extract_trees_roads_empty_blocks(
            city)

        sensor_manager = SensorManager(city, SENSOR_PERIOD)
        sensor_manager.distribute_sensors(SENSOR_DISTANCE)
        sensor_number = sensor_manager.get_sensors_count()
        print("Placed " + str(sensor_number) + " sensors")

        # visualiza the sensor placement
        vis.visualize_sensor(city, sensor_manager.devices, SENSOR_STATIC, SENSOR_PERIOD, SENSOR_DISTANCE)

        # run the simulation - Note: Every iteration is 1 second
        sec = -1
        wind_speed_duration = 0
        wind_speed = 0
        wind_direction = None
        score_values = []
        real_values = []
        measured_values = []
        total_co2 = 0
        print("Running simulation for {} days (this might take a while) ... \n\n".format(
            TIME_TO_RUN / 3600 / 24))

        # data for dataframe
        data = {
            'measured_co2/cell': [],
            'real_co2/cell': [],
            'timeframe': [],
            'sec': []
        }

        while True:
            sec += 1

            date = str((f.sec_to(sec, "hour") % 24)) + ":" + str(f.sec_to(sec, "minute") % 60) + ":" + str(sec % 60) + " - " + str(
                f.sec_to(sec, "day") % 30 + 1) + "/" + str(f.sec_to(sec, "month") % 12 + 1) + "/" + str(f.sec_to(sec, "year") + 1)
            # print the date every day
            if sec % 86400 == 0:
                print("\nDate: ", date)

            # every 6 hours generate new positions for cars

            if sec % 21600 == 0:
                print("Hour: ", f.sec_to(sec, "hour") % 24)
                current_time = f.calculate_tz(f.sec_to(sec, "hour") % 24)
                cars = f.generate_cars(
                    city, roads, time=current_time, max_cars=5000)
                # vis.visualize_cars(city, cars)

            # cars generate co2 every minute
            if sec % 600 == 0:
                f.generate_co2(cars, city, 600)

            # every hour apply the wind effect and the trees effect
            if sec % 600 == 0:
                # every one hour visualize co2
                if SAVE_PLOTS:
                    vis.visualize_co2(
                        city, mesh=False, d=0, wind_direction=wind_direction, wind_speed=wind_speed, date=date)
                    vis.visualize_co2(
                        city, mesh=False, d=3, wind_direction=wind_direction, wind_speed=wind_speed, date=date)

                # apply dispersion
                if SAVE_PLOTS:
                    vis.visualize_diffusion(city, date)
                f.apply_diffusion_effect(city, roads, emptys, 600)
                if SAVE_PLOTS:
                    vis.visualize_diffusion(city, date)

                # calculate wind speed
                if wind_speed_duration == 0 or sec % wind_speed_duration == 0:
                    wind_speed_km, wind_speed_duration = f.calculate_wind_speed(
                        f.sec_to(sec, "month") % 12 + 1, sec)

                # calculate wind direction
                wind_direction = f.calculate_wind_directions(wind_speed_km)

                # convert wind_speed from km/h to m/s
                wind_speed = float(wind_speed_km) * 1000 / 3600
                print('wind_speed: ', wind_speed, "(m/sec)")
                print('wind direction: ', wind_direction)

                # calculate wind effect
                if SAVE_PLOTS:
                    vis.visualize_wind_effect(
                        city, wind_speed, wind_direction, date)
                f.apply_wind_effect(city, roads, emptys,
                                    wind_direction, wind_speed)
                if SAVE_PLOTS:
                    vis.visualize_wind_effect(
                        city, wind_speed, wind_direction, date)

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

                print("co2 generated: ", f.calculate_co2(
                    roads, emptys) - total_co2)
                total_co2 = f.calculate_co2(roads, emptys)
                print("Total co2:", total_co2, "\n")

            if sec % 60 == 0:
                sensor_manager.measure(city, sec // 60)

            if sec % SENSOR_PERIOD == 0:
                # We calculate co2 in the entire 0 floor of the city, that means both the roads and the empty space
                co2_per_cell = f.calculate_co2(
                    roads, emptys_0) / (len(roads + emptys_0))
                real_values.append(co2_per_cell / 125)

            # get a measure
            if sec % SENSOR_PERIOD == 0:
                print("Taking gateway measurement...")
                measures = sensor_manager.gateway()
                co2_per_sensor = np.sum(measures) / sensor_number
                measured_values.append(co2_per_sensor / 125)
                real_co2_per_cell = f.calculate_co2(
                    roads, emptys_0) / (len(roads + emptys_0))
                data['measured_co2/cell'].append(co2_per_sensor)
                data['real_co2/cell'].append(real_co2_per_cell)
                data['timeframe'].append(SENSOR_PERIOD)
                data['sec'].append(sec)
                if not SENSOR_STATIC:
                    print("Moving sensors...")
                    sensor_manager.shuffle_sensors(roads)

            if sec >= TIME_TO_RUN:
                print()
                break

        # save a plot of co2 vs measured co2
        if SAVE_PLOTS:
            vis.visualize_co2_comparison(
                co2=real_values, co2_measured=measured_values, duration=TIME_TO_RUN, frequency=SENSOR_PERIOD)

        score = calculation.calculate_error(real_values, measured_values)
        accuracy = calculation.accuracy(real_values, measured_values)
        print("Average accuracy = ", accuracy*100, "%")

        # Save results in csv file
        newline =  [str(sensor_manager.get_sensor_cost(TIME_TO_RUN)*sensor_number), str(SENSOR_DISTANCE), 
                    str(sensor_number), str(SENSOR_STATIC), str(SENSOR_PERIOD), str(TIME_TO_RUN), str(round(score, 4)), str(round(accuracy, 4))]
        
        calculation.save_results(newline)

        # save data for simulation
        df = pd.DataFrame.from_dict(data)
        df.to_csv(os.path.join('figures', 'run_data',
                               f'{TIME_TO_RUN}_{SENSOR_PERIOD}_{str(sensor_number)}_{SENSOR_STATIC}_{str(sensor_manager.get_sensor_cost(TIME_TO_RUN)*sensor_number)}.csv'), index=False)

        # after the simulation is done, visualize the co2 in the city
        vis.visualize_co2(
            city, mesh=True, d=3, wind_direction=wind_direction, wind_speed=wind_speed, date=date)
        vis.visualize_accuracy(real_values, SENSOR_PERIOD,
                               measured_values, SENSOR_PERIOD)
        # calculate and print the total co2 in the city
        total_co2 = f.calculate_co2(roads, emptys)
        print("Total accumulated co2 in the city:", total_co2, "grams")
        total_measured_co2 = sensor_manager.get_total_co2()
        print("Total measured co2:", str(total_measured_co2), "grams")

        print(f"Root-Mean-Square Error: {round(score, 4)}")
        print(f"Sensors: {sensor_number}")

        print("Energy per device fro 1 year:", str(
            sensor_manager.get_used_power(TIME_TO_RUN)), "mAh")
        print("Cost per device:", str(
            sensor_manager.get_sensor_cost(TIME_TO_RUN)))
        print("Total system cost:", str(
            sensor_manager.get_sensor_cost(TIME_TO_RUN) * sensor_number))

        # after the simulation is done, visualize the co2 in the city
        vis.visualize_co2(
            city, mesh=True, d=3, wind_direction=wind_direction, wind_speed=wind_speed, date=date)
        # calculation.evaluate()


if __name__ == "__main__":

    main()
