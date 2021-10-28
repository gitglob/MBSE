'''
This is the main file, that executes the core loop of our simulation.
'''

import Preprocessing as pre
import SimulationFunctions as f
from Classes import *

def main():
    map_1d = pre.read_png_file()
    map_2d, rows, cols, height = pre.convert_1d_grid_to_2d(map_1d)
    map_3d, rows, cols, height = pre.convert_2d_grid_to_3d(map_2d, rows, cols, height)
    pre.visualize_3d_grid(map_3d, rows, cols, height)

    model = Grid(map_3d)

    # run the simulation
    simulation_flag = False
    iteration = -1
    while (simulation_flag):
        iteration +=1
        print("iteration # ", iteration)
        
        # generato co2
        f.generate_co2()
        
        # iterate over the entire grid
        f.calculate_co2()
        
        # calculate wind effect
        f.apply_wind()
        
        # apply dispersion
        f.apply_co2_dispersion()

    return 0

if __name__ == "__main__":
    main()