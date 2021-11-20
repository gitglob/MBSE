# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:03:37 2021

@author: Bence Many
"""

import math
import csv
from os.path import exists

results_path = "figures\\results\\results.csv"


#Calculating the Root-Mean-Square Error of the measurement vs real values
def calculate_error(real, measured):
    summ = 0
    for i in range(len(real)):
        summ += pow(real[i] - measured[i], 2)
    error = math.sqrt(summ/len(real))
    return(error)



#Save results in csv file
def save_results(newline):    
    if exists(results_path) == False:
        with open(results_path, "a+") as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(["Cost", "Sensor distance",	"Static", "Sampling time", "Simulation time", "Error"])
            writer.writerow(newline)
    else:
        with open(results_path, "a+") as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(newline)
            
            
        