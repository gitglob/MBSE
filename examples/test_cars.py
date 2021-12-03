"""
This is a test to determine if the co2 generation is being done correctly and that the cars are dispearsed correctly.

To run: 
1. Copy the .py file in MBSE folder 
2. Run from that directory
3. produces 8 graphs in figures/co2_timeseries, 4 before and 4 after co2 generation
"""

import environment.simulation_functions as f
import environment.preprocessing as pre
import environment.visualize as vis
from environment.classes import *
import matplotlib.pyplot as plt

def runfortime(city, roads, current_time):
    cars = f.generate_cars(city, roads, time=current_time, max_cars=5000)

    vis.visualize_co2(city, mesh=False, d=0, wind_direction='default', wind_speed='default', date=str(current_time))
    f.generate_co2(cars, city, 1200)
    vis.visualize_co2(city, mesh=False, d=0, wind_direction='default', wind_speed='default', date=str(current_time))

def main():
    for current_time in [1,2,3,4]:
        city = Grid()
        trees, roads, emptys = pre.extract_trees_roads_empty_blocks(city)
        runfortime(city, roads, current_time)

if __name__ == '__main__':
    main()