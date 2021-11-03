'''
This is the preprocessing file, which creates the 3d grid of the city we are simulating.
'''

from PIL import Image
import numpy as np
import os

# read map png file
def read_png_file():
    dir_path = os.path.dirname(os.path.realpath('city.png'))
    im_frame = Image.open(dir_path + '\city.png')
    map_1d = np.array(im_frame.getdata())

    return (map_1d)

# convert 1d map grid to 2d
def convert_1d_grid_to_2d(map_1d):
    map_1d = np.delete(map_1d, -1, axis=1)
    map_2d = np.reshape(map_1d, (60, 60, 1, 3))

    # define map dimensions
    rows = np.shape(map_2d)[0]
    cols = np.shape(map_2d)[1]
    height = 1
    colors = np.shape(map_2d)[2]

    # initialize color variables as their corresponding rgb values
    brown = [121, 85, 72]
    green = [76, 175, 80]
    blue = [3, 169, 244]
    white = [255,255,255]

    # Convert rgb values to chars :
    #road = 't'
    #trees = 'g'
    #building = 'b'
    #nothing = 'w'
    map_2d_list = [[[  [] for _ in range(height)] for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if map_2d[i,j,0,:].tolist() == brown:
                map_2d_list[i][j][0] = 't'
            elif map_2d[i,j,0,:].tolist() == green:
                map_2d_list[i][j][0] = 'g'
            elif map_2d[i,j,0,:].tolist() == blue:
                map_2d_list[i][j][0] = 'b'
            elif map_2d[i,j,0,:].tolist() == white:
                map_2d_list[i][j][0] = 'w'

    return (map_2d_list, rows, cols, height)

# Convert 2d map grid to 3d 
def convert_2d_grid_to_3d(map_2d, rows, cols, height):
    # initialize empty 3d list
    map_3d = [[[  [] for _ in range(height*3)] for _ in range(cols*3)] for _ in range(rows*3)]


    # split each cell to 3
    for i in range(rows):
        for j in range(cols):
            for k in range(height):
                for t1 in range(3):
                    for t2 in range(3):
                        for t3 in range(3):
                            map_3d[i*3 + t1][j*3 + t2][k*3 + t3] = map_2d[i][j][k]

    # set new rows, col, height numbers
    rows = 180
    cols = 180
    height = 3

    for i in range(rows):
        for j in range(cols):
            for k in [1,2]:
                if map_3d[i][j][k] == 't':
                    map_3d[i][j][k] = 'w'
                    
    return(map_3d, rows, cols, height)

# extract city tree/road/empty blocks
def extract_trees_roads_empty_blocks(city):
    trees_list = []
    empty_blocks_list = []
    roads_list = []

    # iterate over the 3d grid
    for i in range(city.rows):
        for j in range(city.cols):
            for k in range(city.height):
                # check if the current grid cell is a tree
                if city.grid3d[i][j][k].contains == "tree":
                    trees_list.append(city.grid3d[i][j][k])
                if city.grid3d[i][j][k].contains == "road":
                    roads_list.append(city.grid3d[i][j][k])
                if city.grid3d[i][j][k].contains == "empty":
                    empty_blocks_list.append(city.grid3d[i][j][k])

    return (trees_list, roads_list, empty_blocks_list)