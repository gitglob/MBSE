'''
This file contains all the necessary functions that will be called during the main loop of the simulation 
in order to execute certain tasks.
'''

# calculate the CO2
def calculate_co2():
    # calculate car emissions
    co2_sum = 0
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                if city.grid3d[i][j][k].car_flag:
                    co2_sum += city.grid3d[i][j][k].co2
                    pass

# apply wind effect
def apply_wind():
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                if city.grid3d[i][j][k].co2:
                    pass

# apply air dispersion dynamics
def apply_co2_dispersion():
    for i in city.rows:
        for j in city.cols:
            for k in city.height:
                if city.grid3d[i][j][k].co2:
                    pass
                    
def generate_co2():
    for car in cars:
        car.generate_co2()