# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:03:37 2021

@author: Bence Many
"""

import math
import csv
from os.path import exists
import pandas as pd
from matplotlib import pyplot as plt


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
        with open(results_path, "a+", newline = "") as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(["Cost", "Sensor distance",	"Static", "Sampling time", "Simulation time", "Error"])
            writer.writerow(newline)
    else:
        with open(results_path, "a+", newline = "") as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(newline)
            
            
def evaluate():
    cost = []
    error10 = []
    error30 = []
    error120 = []
    df = pd.read_csv(results_path, delimiter=';')
    rows = [tuple(x) for x in df.values]
    for i in rows:
        cost.append(i[0])
        if (i[3] == 1800):
            error30.append(i[5])
            error10.append(None)
            error120.append(None)
        if (i[3] == 600):
            error10.append(i[5])
            error30.append(None)
            error120.append(None)
        if (i[3] == 7200):
            error10.append(None)
            error30.append(None)
            error120.append(i[5])
       
    #Plotting cost vs error
    plt.figure()
    plt.plot(cost, error30, 'bo')
    plt.plot(cost, error10, 'ro')
    plt.plot(cost, error120, 'yo')
    plt.ylabel("Root-Mean-Square Error")
    plt.xlabel("Total system cost [€]")
    plt.title("Static")
    plt.legend(["30 minutes", "10 minutes", "120 minutes"])
    plt.show()
    
    
#evaluate()
        

            

            
        