from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import seaborn as sns
import os
import datetime
import pandas as pd


# Visualize 3d grid
def visualize_3d_grid(city):
    print("Visualizing city...")
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    z1 = []
    z2 = []
    z3 = []
    z4 = []

    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                if city.grid3d[i][j][k].contains == 'road':
                    x1.append(i)
                    y1.append(j)
                    z1.append(k)
                elif city.grid3d[i][j][k].contains == "tree":
                    x2.append(i)
                    y2.append(j)
                    z2.append(k)
                elif city.grid3d[i][j][k].contains == "building":
                    x3.append(i)
                    y3.append(j)
                    z3.append(k)
                elif city.grid3d[i][j][k].contains == "empty":
                    x4.append(i)
                    y4.append(j)
                    z4.append(k)

    plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["figure.autolayout"] = True
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x1, y1, z1, s=0.5, c='red', alpha=1)
    ax.scatter(x2, y2, z2, s=0.5, c='green', alpha=1)
    ax.scatter(x3, y3, z3, s=0.5, c='blue', alpha=1)
    ax.scatter(x4, y4, z4, s=0.5, c='white', alpha=1)
    plt.title("3d CITY MODEL \n\nBlue: buildings \nGreen: trees \nRed: roads \n White: empty (air)")
    plt.savefig(os.path.join('figures', 'city_model', 'city_3d_model.png'))
    plt.show()


# Visualize cards
def visualize_cars(city, cars):
    print("Visualizing cars...")
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    z1 = []
    z2 = []
    z3 = []
    z4 = []
    z5 = []

    car_pos = []
    for car in cars:
        x5.append(car.x)
        y5.append(car.y)
        z5.append(car.z)
        car_pos.append([car.x, car.y, car.z])

    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                if city.grid3d[i][j][k].contains == "empty":
                    x4.append(i)
                    y4.append(j)
                    z4.append(k)
                elif city.grid3d[i][j][k].contains == "building":
                    x3.append(i)
                    y3.append(j)
                    z3.append(k)
                elif city.grid3d[i][j][k].contains == "tree":
                    x2.append(i)
                    y2.append(j)
                    z2.append(k)
                else:
                    if [i, j, k] not in car_pos:
                        x1.append(i)
                        y1.append(j)
                        z1.append(k)

    plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["figure.autolayout"] = True
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x1, y1, z1, c='red', s=0.5, alpha=1)
    ax.scatter(x2, y2, z2, c='green', s=0.5, alpha=1)
    ax.scatter(x3, y3, z3, c='blue', s=0.5, alpha=1)
    ax.scatter(x4, y4, z4, c='white', s=0.5, alpha=1)
    ax.scatter(x5, y5, z5, c='black', s=0.75, alpha=1)
    plt.show()

# Visualize CO2 levels in 3d grid or just one floor (d=[0,1,2] -> show this floor, d=3 -> show a 3d visualization)
def visualize_co2(city, mesh=False, d = 3, wind_direction=None, wind_speed=0, date=None):
    print("Visualizing real co2...")

    # 3d visualization
    if d == 3:
        # extract the co2 levels from the grid
        co2 = []
        for i in range(city.rows):
            for j in range(city.cols):
                for k in range(city.height):
                    co2.append(city.grid3d[i][j][k].co2)

        # creating figures
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

        # create a color map based on the co2
        colmap = cm.ScalarMappable(cmap=cm.Greys)
        colmap.set_array(co2)

        # create the grid
        x = []
        y = []
        z = []
        for i in range(city.rows):
            for j in range(city.cols):
                for k in range(city.height):
                    x.append(i)
                    y.append(j)
                    z.append(k)

        # creating the heatmap
        ax.scatter(x, y, z, marker='s', s = 5, c=co2, alpha=0.2, cmap='Greys')
        cb = fig.colorbar(colmap)

        # if mesh==True then mesh the co2 plot with the city plot
        if mesh:
            x1 = []
            x2 = []
            y1 = []
            y2 = []
            z1 = []
            z2 = []

            for i in range(city.rows):
                for j in range(city.cols):
                    for k in range(city.height):
                        if city.grid3d[i][j][k].contains == "tree":
                            x1.append(i)
                            y1.append(j)
                            z1.append(k)
                        elif city.grid3d[i][j][k].contains == "building":
                            x2.append(i)
                            y2.append(j)
                            z2.append(k)

            ax.scatter(x1, y1, z1, s=0.5, c='green', alpha=1)
            ax.scatter(x2, y2, z2, s=0.5, c='blue', alpha=1)

        # adding title and labels
        ax.set_title(date+"\n\nCity 3D CO2 Heatmap. \n\nWind speed: {} (m/s) \nWind direction: {}".format(wind_speed, wind_direction))
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')

        # displaying plot
        # plt.show()
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        plt.savefig(os.path.join('figures', 'co2_3d', f'{now}.png'))
        plt.close()

    # 2d visualization
    else:
        # extract the co2 levels from the grid
        co2 = []
        for i in range(city.rows):
            for j in range(city.cols):
                k = d
                co2.append(city.grid3d[i][j][k].co2)

        # creating figures
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)

        # create a color map based on the co2
        colmap = cm.ScalarMappable(cmap=cm.Greys)
        colmap.set_array(co2)

        # create the grid
        x = []
        y = []
        for i in range(city.rows):
            for j in range(city.cols):
                x.append(i)
                y.append(j)

        # creating the heatmap
        ax.scatter(x, y, marker='s', s = 5, c=co2, alpha=0.5, cmap='Greys')
        cb = fig.colorbar(colmap)

        # if mesh==True then mesh the co2 plot with the city plot
        if mesh:
            x1 = []
            x2 = []
            y1 = []
            y2 = []
            z1 = []
            z2 = []

            for i in range(city.rows):
                for j in range(city.cols):
                    k = 2
                    if city.grid3d[i][j][k].contains == "tree":
                        x1.append(i)
                        y1.append(j)
                    elif city.grid3d[i][j][k].contains == "building":
                        x2.append(i)
                        y2.append(j)

            ax.scatter(x1, y1, s=0.5, c='green', alpha=1)
            ax.scatter(x2, y2, s=0.5, c='blue', alpha=1)

        # adding title and labels
        ax.set_title(date + "\n\nCity 3D CO2 Heatmap. \n\nWind speed: {} (m/s) \nWind direction: {}".format(wind_speed, wind_direction))
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')

        # displaying plot
        # plt.show()
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        plt.savefig(os.path.join('figures', 'co2_timeseries', f'{now}.png'))
        plt.close()

def visualize_sensor(city, sensors, static, T, d):
    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    x1 = []
    x2 = []
    x3 = []
    y1 = []
    y2 = []
    y3 = []

    for i in range(city.rows):
        for j in range(city.cols):
            if city.grid3d[i][j][0].contains == "tree":
                x1.append(i)
                y1.append(j)
            elif city.grid3d[i][j][0].contains == "building":
                x2.append(i)
                y2.append(j)
            elif city.grid3d[i][j][0].contains == "road":
                x3.append(i)
                y3.append(j)

    size = 8
    ax.scatter(x1, y1, s=size, marker='s', c='green', alpha=1)
    ax.scatter(x2, y2, s=size, marker='s', c='blue', alpha=1)
    ax.scatter(x3, y3, s=size, marker='s', c='#919191', alpha=1)

    s_x = []
    s_y = []
    for s in sensors:
        s_x.append(s.x)
        s_y.append(s.y)
    ax.scatter(s_x, s_y, s=4, marker='o', c='#a10000', alpha=1)

    # adding title and labels
    if static:
        placement = "static"
    else:
        placement = "dynamic"
    ax.set_title(f"City 2d Sensor location (ground floor, sensors marked as red dots) \n\n Sensor placement: {placement} \nSensor period: {T} sec \nSensor distance: {d} m")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # displaying plot
    plt.savefig(os.path.join('figures', 'sensor_placement', 'sensor_placement.png'))
    plt.show()

def visualize_co2_measures(values):
    print("Visualizing real co2...")

    # create the grid
    x = []
    y = []
    for i in range(len(values)):
        for j in range(len(values[0])):
            x.append(i)
            y.append(j)
    co2 = []
    for i in range(len(values)):
        for j in range(len(values[0])):
            co2.append(values[i][j])
    colmap = cm.ScalarMappable(cmap=cm.Greys)
    colmap.set_array(co2)

    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # setting color bar
    color_map = cm.ScalarMappable(cmap=cm.Greys)
    color_map.set_array(co2)

    # creating the heatmap
    ax.scatter(x, y, marker='s', s = 5, c=co2, cmap='Greys')
    cb = fig.colorbar(colmap)

    # adding title and labels
    ax.set_title("3D Heatmap of CO2 measures")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # displaying plot
    plt.show()

# Visualize CO2 levels in 3d grid or just one floor (d=[0,1,2] -> show this floor, d=3 -> show a 3d visualization)
def visualize_trees_effect(city, date):
    print("Visualizing trees effect...")

    # extract the co2 levels from the grid
    co2 = []
    for i in range(city.rows):
        for j in range(city.cols):
            k = 0
            co2.append(city.grid3d[i][j][k].co2)

    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # create a color map based on the co2
    colmap = cm.ScalarMappable(cmap=cm.Greys)
    colmap.set_array(co2)

    # create the grid
    x = []
    y = []
    for i in range(city.rows):
        for j in range(city.cols):
            x.append(i)
            y.append(j)

    # creating the heatmap
    ax.scatter(x, y, marker='s', s = 5, c=co2, alpha=0.5, cmap='Greys')
    cb = fig.colorbar(colmap)

    x1 = []
    y1 = []

    for i in range(city.rows):
        for j in range(city.cols):
            k = 2
            if city.grid3d[i][j][k].contains == "tree":
                x1.append(i)
                y1.append(j)

    ax.scatter(x1, y1, s=0.5, c='green', alpha=1)

    # adding title and labels
    ax.set_title(date + "\n\nCity 2d CO2 Heatmap - trees effect")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # displaying plot
    # plt.show()
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    plt.savefig(os.path.join('figures', 'co2_trees_effect', f'{now}.png'))
    plt.close()

def visualize_wind_effect(city, wind_speed, wind_direction, date):
    print("Visualizing wind effect...")

    # extract the co2 levels from the grid
    co2 = []
    for i in range(city.rows):
        for j in range(city.cols):
            k = 0
            co2.append(city.grid3d[i][j][k].co2)

    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # create a color map based on the co2
    colmap = cm.ScalarMappable(cmap=cm.Greys)
    colmap.set_array(co2)

    # create the grid
    x = []
    y = []
    for i in range(city.rows):
        for j in range(city.cols):
            x.append(i)
            y.append(j)

    # creating the heatmap
    ax.scatter(x, y, marker='s', s = 5, c=co2, alpha=0.5, cmap='Greys')
    cb = fig.colorbar(colmap)

    x1 = []
    x2 = []
    y1 = []
    y2 = []

    for i in range(city.rows):
        for j in range(city.cols):
            k = 2
            if city.grid3d[i][j][k].contains == "tree":
                x1.append(i)
                y1.append(j)
            elif city.grid3d[i][j][k].contains == "building":
                x2.append(i)
                y2.append(j)

    ax.scatter(x1, y1, s=0.5, c='green', alpha=1)
    ax.scatter(x2, y2, s=0.5, c='blue', alpha=1)

    # adding title and labels
    ax.set_title(date + "\n\nCity 2d CO2 heatmap - wind effect. \n\nWind speed: {} (m/s) \nWind direction: {}".format(wind_speed, wind_direction))
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # displaying plot
    # plt.show()
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    plt.savefig(os.path.join('figures', 'co2_wind_effect', f'{now}.png'))
    plt.close()

def visualize_rain_effect(city, date):
    print("Visualizing rain effect...")

    # extract the co2 levels from the grid
    co2 = []
    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                co2.append(city.grid3d[i][j][k].co2)

    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")

    # create a color map based on the co2
    colmap = cm.ScalarMappable(cmap=cm.Greys)
    colmap.set_array(co2)

    # create the grid
    x = []
    y = []
    z = []
    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                x.append(i)
                y.append(j)
                z.append(k)

    # creating the heatmap
    ax.scatter(x, y, z, marker='s', s = 5, c=co2, alpha=0.2, cmap='Greys')
    cb = fig.colorbar(colmap)

    x1 = []
    x2 = []
    y1 = []
    y2 = []
    z1 = []
    z2 = []

    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                if city.grid3d[i][j][k].contains == "tree":
                    x1.append(i)
                    y1.append(j)
                    z1.append(k)
                elif city.grid3d[i][j][k].contains == "building":
                    x2.append(i)
                    y2.append(j)
                    z2.append(k)

    ax.scatter(x1, y1, z1, s=0.5, c='green', alpha=1)
    ax.scatter(x2, y2, z2, s=0.5, c='blue', alpha=1)

    # adding title and labels
    ax.set_title(date + "\n\nCity 3D CO2 Heatmap - Rain effect \n\n")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # displaying plot
    #plt.show()
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    plt.savefig(os.path.join('figures', 'co2_rain_effect', f'{now}.png'))
    plt.close()
    
    
def visualize_accuracy (real, real_period, measured, sensor_period):
    plt.figure()
    plt.plot([x*real_period/3600 for x in range(len(real))], real, "-")
    plt.plot([x*sensor_period/3600 for x in range(len(measured))], measured, "-")
    plt.legend(["Real", "Measured"], fontsize = 30)
    plt.ylabel("CO2 amount [g/m3]", fontsize = 30)
    plt.xlabel("Time [h]", fontsize = 30)
    plt.title("CO2 level in the city", fontsize = 30)
    plt.xticks(fontsize = 30)
    plt.yticks(fontsize = 30)
    plt.show()

def visualize_diffusion(city, date):
    print("Visualizing diffusion...")

    # extract the co2 levels from the grid
    co2 = []
    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                co2.append(city.grid3d[i][j][k].co2)

    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")

    # create a color map based on the co2
    colmap = cm.ScalarMappable(cmap=cm.Greys)
    colmap.set_array(co2)

    # create the grid
    x = []
    y = []
    z = []
    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                x.append(i)
                y.append(j)
                z.append(k)

    # creating the heatmap
    ax.scatter(x, y, z, marker='s', s = 5, c=co2, alpha=0.2, cmap='Greys')
    cb = fig.colorbar(colmap)

    # x1 = []
    # x2 = []
    # y1 = []
    # y2 = []
    # z1 = []
    # z2 = []

    # for i in range(city.rows):
    #     for j in range(city.cols):
    #         for k in range(city.height):
    #             if city.grid3d[i][j][k].contains == "tree":
    #                 x1.append(i)
    #                 y1.append(j)
    #                 z1.append(k)
    #             elif city.grid3d[i][j][k].contains == "building":
    #                 x2.append(i)
    #                 y2.append(j)
    #                 z2.append(k)

    # ax.scatter(x1, y1, z1, s=0.5, c='green', alpha=1)
    # ax.scatter(x2, y2, z2, s=0.5, c='blue', alpha=1)

    # adding title and labels
    ax.set_title(date + "\n\nCity 3D CO2 Heatmap - Diffusion \n\n")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # displaying plot
    #plt.show()
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    plt.savefig(os.path.join('figures', 'co2_diffusion', f'{now}.png'))
    plt.close()

def visualize_co2_comparison(co2, co2_measured, duration, frequency):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    plt.plot(np.arange(len(co2))*frequency/3600, co2, '--r', label="real co2")
    plt.plot(np.arange(len(co2_measured))*frequency/3600, co2_measured, '-b', label="measured co2")

    # adding title and labels
    ax.legend(loc='upper left')
    ax.set_title("\n\nReal co2 vs Measured co2\n\n Simulation duration: " + str(duration/(60*60*24)) + "days.\n")
    ax.set_xlabel('time (hour)')
    ax.set_ylabel('co2 quantity (grams)')

    # displaying plot
    #plt.show()
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    plt.savefig(os.path.join('figures', 'co2_comparison', f'{now}.png'))
    plt.close()

def visualize_norm_co2(score_values, real_normalized, duration, frequency):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)    
    
    plt.plot(np.arange(len(score_values))*frequency/3600, score_values, '-g', label="accuracy")
    plt.plot(np.arange(len(real_normalized))*frequency/3600, real_normalized, '-b', label="normalized co2")
    
    ax.set_title("Sensing accuracy per cell / Normalized co2 amount per cell\n\n Simulation duration: " + str(duration/(60*60*24)) + " days.\n")
    ax.legend()
    ax.set_xlabel('time (hour)')
    ax.set_ylabel('accuracy / normalized co2')

    # displaying plot
    #plt.show()
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    plt.savefig(os.path.join('figures', 'co2_normalized_acc', f'{now}.png'))
    plt.close()
