import os
import math
import csv
from os.path import exists
import pandas as pd
from matplotlib import pyplot as plt
from numpy import diff
import numpy as np

results_path = os.path.join("figures", "results", "results.csv")

# Calculating the Root-Mean-Square Error of the measurement vs real values
def calculate_error(real, measured):
    summ = 0
    for i in range(len(real)):
        summ += pow(real[i] - measured[i], 2)
    error = math.sqrt(summ/len(real))
    return(error)

def calculate_accuracy(real, measured):
    acc_list = []
    
    # Calculating accuracy
    for i in range(len(measured)):
        acc = 100 - (100*(abs(measured[i] - real[i])/real[i]))
        acc_list.append(acc)
    
    accuracy = sum(acc_list)/len(acc_list)

    return(accuracy)

# Save results in csv file
def save_results(newline):    
    if exists(results_path) == False:
        with open(results_path, "a+", newline = "") as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(["Cost", "Sensor distance","Number of sensors", "Static", "Sampling time", "Simulation time", "Error", "Accuracy"])
            writer.writerow(newline)
    else:
        with open(results_path, "a+", newline = "") as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(newline)
            
#Evaluation of Root-Mean-Square Error against Total system cost
def evaluate():
    number = []
    accuracy = []
    
    df = pd.read_csv(results_path, delimiter=';')
    rows = [tuple(x) for x in df.values]
    for i in rows:
        number.append(i[2])
        accuracy.append(round(i[7], 3)*100)
        
    #Plotting accuracy vs error
    plt.figure()
    plt.scatter(number, accuracy, s = 300)
    # plt.plot(cost, error10, 'ro')
    # plt.plot(cost, error30, 'bo')
    # plt.plot(cost, error60, 'go')
    # plt.plot(cost, error120, 'yo')
    
    plt.ylabel("Accuracy [%]", fontsize = 30)
    #plt.ylabel("Root-Mean-Square Error")
    plt.xlabel("Number of sensors", fontsize = 30)
    #plt.legend(["10 minutes", "30 minutes", "60 minutes", "120 minutes"])
    plt.xticks(fontsize = 30)
    plt.yticks(fontsize = 30)
    plt.show()
    
def accuracy_per_cost():
    cost = []
    accuracy = []
    df = pd.read_csv(results_path, delimiter=';')
    rows = [tuple(x) for x in df.values]
    for i in rows:
        cost.append(i[0])
        accuracy.append(i[7])
    
    #Normalize error
    acc_norm = []
    added_value = []
    for i in accuracy:
        acc_norm.append((i - min(accuracy)) / (max(accuracy) - min(accuracy)))

    for i in range(len(acc_norm)):
        added_value.append(acc_norm[i] / cost[i])
    
       
    #Plotting cost vs error
    plt.figure()
    plt.plot(cost, acc_norm, 'ro')
    #plt.plot(cost, added_value, 'go')
    plt.ylabel("Accuracy / cost")
    plt.xlabel("Total system cost [€]")
    plt.title("Value of price")
    plt.show()
    
    print("Highest value: ", max(added_value), " at the price of: ", cost[added_value.index(max(added_value))])
    
    # real = [1, 1, 1, 2]
    # mes = [1, 1.9, 1.9, 2]
    # print(accuracy(real, mes))
    # plt.plot(range(len(real)), real)
    # plt.plot(range(len(mes)), mes)
    # plt.show()
    #evaluate()
    #accuracy_per_cost()
        
def remove_outliers(measured, n):
    # replace measured values with average measured values every 10 points
    avg_measured = []
    sum_ = 0
    count = 0
    for i, x in enumerate(measured):
        sum_ += x
        count += 1
        if count==n or i == len(measured)-1:
            avg_measured.append(sum_/count)
            sum_ = 0
            count = 0
        
    return avg_measured

def interpolate(real, measured):
    diff = (len(real)-1) / (len(measured)-1)
    interp_measured =np.interp(range(len(real)),
            [x*diff for x in range(len(measured))],
            measured)

    return interp_measured

def compare():
    # read csv
    df = pd.read_csv(os.path.join(os.getcwd(), 'figures', 'results', 'results.csv'), sep=';')
    df = df[df['Accuracy']>0]

    # cost-efficiency factor
    df['ce'] = df['Cost']/(df['Accuracy']*100)

    # most cost efficient solution
    print('The most accurate simulation has the following characteristics:')
    print('Number of sensors: ', df.loc[[df['Accuracy'].idxmax()]]['Number of sensors'].item())
    print('Sensor distance: ', df.loc[[df['Accuracy'].idxmax()]]['Sensor distance'].item())
    print('Sampling time: ', df.loc[[df['Accuracy'].idxmax()]]['Sampling time'].item())
    print('Static placement: ', df.loc[[df['Accuracy'].idxmax()]]['Static'].item())
    print('Accuracy: ', df.loc[[df['Accuracy'].idxmax()]]['Accuracy'].item(), '\n')

    # most cost efficient solution
    print('The most cost-efficient simulation has the following characteristics:')
    print('Number of sensors: ', df.loc[[df['ce'].idxmin()]]['Number of sensors'].item())
    print('Sensor distance: ', df.loc[[df['ce'].idxmin()]]['Sensor distance'].item())
    print('Sampling time: ', df.loc[[df['ce'].idxmin()]]['Sampling time'].item())
    print('Static placement: ', df.loc[[df['ce'].idxmin()]]['Static'].item())
    print('Accuracy: ', df.loc[[df['ce'].idxmin()]]['Accuracy'].item())

    return
