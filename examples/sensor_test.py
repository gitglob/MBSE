
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py

import matplotlib.pyplot as plt

from iot.sensor import Sensor


def errorSensorTest():
    x = range(100)

    sensor_5 = Sensor(0.05, 0, 0, 0)
    sensor_10 = Sensor(0.1, 0, 0, 0)
    sensor_20 = Sensor(0.2, 0, 0, 0)
    y_5 = [sensor_5.measure(50) for _ in x]
    y_5 = [sensor_5.measure(50) for _ in x]
    y_10 = [sensor_10.measure(50) for _ in x]
    y_20 = [sensor_20.measure(50) for _ in x]

    fig, axs = plt.subplots(3, 1)
    plt.title("Sensor error")

    axs[0].plot(x, [50 for _ in x], "black")
    axs[0].plot(x, [47.5 for _ in x], c="#1f77b4", linestyle='dashed')
    axs[0].plot(x, [52.5 for _ in x], c="#1f77b4", linestyle='dashed')
    axs[0].scatter(x, y_5, 10)
    axs[0].set_title("5% error")
    axs[0].set_ylim(39, 61)

    axs[1].plot(x, [50 for _ in x], "black")
    axs[1].plot(x, [45 for _ in x], c="#1f77b4", linestyle='dashed')
    axs[1].plot(x, [55 for _ in x], c="#1f77b4", linestyle='dashed')
    axs[1].scatter(x, y_10, 10)
    axs[1].set_title("10% error")
    axs[1].set_ylim(39, 61)

    axs[2].plot(x, [50 for _ in x], "black")
    axs[2].plot(x, [40 for _ in x], c="#1f77b4", linestyle='dashed')
    axs[2].plot(x, [60 for _ in x], c="#1f77b4", linestyle='dashed')
    axs[2].scatter(x, y_20, 10)
    axs[2].set_title("20% error")
    axs[2].set_ylim(39, 61)
    plt.show()

errorSensorTest()
