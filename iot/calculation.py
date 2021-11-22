import math
import csv
from os.path import exists
import pandas as pd
from matplotlib import pyplot as plt
from numpy import diff



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
            
#Evaluation of Root-Mean-Square Error against Total system cost
def evaluate():
    cost = []
    error10 = []
    error30 = []
    error60 = []
    error120 = []
    df = pd.read_csv(results_path, delimiter=';')
    rows = [tuple(x) for x in df.values]
    for i in rows:
        cost.append(i[0])
        if (i[3] == 600):
            error10.append(i[5])
            error30.append(None)
            error60.append(None)
            error120.append(None)
        elif (i[3] == 1800):
            error30.append(i[5])
            error10.append(None)
            error60.append(None)
            error120.append(None)
        elif (i[3] == 3600):
            error10.append(None)
            error30.append(None)
            error60.append(i[5])
            error120.append(None)
        elif (i[3] == 7200):
            error10.append(None)
            error30.append(None)
            error60.append(None)
            error120.append(i[5])
       
        
    #Plotting cost vs error
    plt.figure()
    plt.plot(cost, error10, 'ro')
    plt.plot(cost, error30, 'bo')
    plt.plot(cost, error60, 'go')
    plt.plot(cost, error120, 'yo')
    plt.ylabel("Root-Mean-Square Error")
    plt.xlabel("Total system cost [€]")
    plt.title("Static")
    plt.legend(["10 minutes", "30 minutes", "60 minutes", "120 minutes"])
    plt.show()
    
    
    
def accuracy_per_cost():
    cost = []
    error = []
    df = pd.read_csv(results_path, delimiter=';')
    rows = [tuple(x) for x in df.values]
    for i in rows:
        cost.append(i[0])
        error.append(-i[5])
    
    #Normalize error
    acc_norm = []
    added_value = []
    for i in error:
        acc_norm.append((i - min(error)) / (max(error) - min(error)))

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
    
    
#evaluate()
#accuracy_per_cost()