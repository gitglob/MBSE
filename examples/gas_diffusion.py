# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 14:43:18 2021

@author: Bence Mány

Project: Air pollution simulation
"""
import matplotlib.pyplot as plt

class cube:

    def __init__(self, conc):
        self.conc = conc
        self.values = []
        
    def add(self, value):
        self.values.append(value)
    


cubes = []
for i in range(5):
    cubes.append(cube(0))
       
f0 = 1


#It matters how far we define the edge of the simulation (zero CO2 concentration)
size = 5
area = 25
vol = 125
diffrate = 1.6e-5
time = range(100000)



for x in time:
    for i in range(len(cubes)):
        if i == 0 and x%24<8:
            cubes[i].conc += f0
        cubes[i].add(cubes[i].conc)
        if i == len(cubes)-1:
            flow = diffrate*((cubes[i].conc)/size)*area*3600
            cubes[i].conc -= flow/vol
        else:
            flow = diffrate*((cubes[i].conc-cubes[i+1].conc)/size)*area*3600
            cubes[i].conc -= flow/vol
            cubes[i+1].conc += flow/vol
        

    
    

plt.plot(time, cubes[0].values, label = "0 m")
plt.plot(time, cubes[1].values, label = "5 m")
plt.plot(time, cubes[2].values, label = "10 m")
plt.plot(time, cubes[3].values, label = "15 m")
plt.plot(time, cubes[4].values, label = "20 m")
plt.legend()
plt.show

