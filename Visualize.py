from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Visualize 3d grid
def visualize_3d_grid(map_3d, rows, cols, height):
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

    for i in range(rows):
        for j in range(cols):
            for k in range(height):
                if map_3d[i][j][k]=='t':
                    x1.append(i)
                    y1.append(j)
                    z1.append(k)
                elif map_3d[i][j][k]=='g':
                    x2.append(i)
                    y2.append(j)
                    z2.append(k)
                elif map_3d[i][j][k]=='b':
                    x3.append(i)
                    y3.append(j)
                    z3.append(k)
                elif map_3d[i][j][k]=='w':
                    x4.append(i)
                    y4.append(j)
                    z4.append(k)

    plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["figure.autolayout"] = True
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x1, y1, z1, c='red', alpha=1)
    ax.scatter(x2, y2, z2, c='green', alpha=1)
    ax.scatter(x3, y3, z3, c='blue', alpha=1)
    ax.scatter(x4, y4, z4, c='white', alpha=1)
    plt.show()

# Visualize CO2 levels in 3d grid
def visualize_co2(city):
    # create the grid
    x = []
    y = []
    z = []
    for i in range(180):
        for j in range(180):
            for k in range(1):
                x.append(i)
                y.append(j)
                z.append(k)

    # extract the co2 levels from the grid 
    co2 = []
    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(1):
                co2.append(city.grid3d[i][j][k].co2)
    
    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # setting color bar
    color_map = cm.ScalarMappable(cmap=cm.Greys)
    color_map.set_array(co2)
    
    # creating the heatmap
    img = ax.scatter(x, y, z, marker='s', s=1, c=co2)
    #plt.colorbar(color_map)
    
    # adding title and labels
    ax.set_title("3D Heatmap")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    
    # displaying plot
    plt.show()