# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:03:37 2021

@author: Bence Many
"""

import matplotlib.pyplot as plt

def calculate_accuracy(score_values, real_values):
    score = 0
    real_normalized = []
    for s in score_values:
        score += s
    score = score * 100 / len(score_values)
    real_min = min(real_values)
    real_max = max(real_values)
    for r in real_values:
        real_normalized.append((r - real_min) / (real_max - real_min))
    plt.figure()
    plt.plot(range(len(score_values)), score_values, real_normalized)
    plt.legend(["Accuracy", "Normalized CO2 amount"])
    plt.show()
    return(score)