'''
This is the preprocessing file, which creates the 3d grid of the city we are simulating.
'''
# extract city tree/road/empty blocks
def extract_trees_roads_empty_blocks(city):
    trees_list = []
    empty_blocks_list = []
    empty_0_blocks_list = []
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
                    if k==0:
                        empty_0_blocks_list.append(city.grid3d[i][j][k])

    return (trees_list, roads_list, empty_blocks_list, empty_0_blocks_list)
