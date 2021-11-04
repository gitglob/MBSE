from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from pylab import *

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
    ax.scatter(x5, y5, z5, c='black', s=0.5, alpha=1)
    plt.show()

# Visualize CO2 levels in 3d grid or just one floor (d=[0,1,2] -> show this floow, d=3 -> show a 3d visualization)
def visualize_co2(city, mesh=False, d = 3):
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
        ax.set_title("City 3D CO2 Heatmap")
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        
        # displaying plot
        plt.show()
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
        ax.set_title("City 2d CO2 Heatmap")
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        
        # displaying plot
        plt.show()

def visualize_co2_measures(values):
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
