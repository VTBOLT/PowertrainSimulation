# this program is called by the optimization program to determine how quickly the new bike can finish the race

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

# inputs: motor max torque and total bike mass

# from originalbikemodel.py: list of times rider throttles and for what distance they hold the throttle
# also need max braking acceleration from bolt 3

GearRatio = 4
WheelR = 0.3302  # Wheel diameter in nanometers
BikeM = 200  # mass input from optimization program in kgs
max_torque = 10  # max torque of bike motor

# torque = torque wheel = torque shaft * 4
# f*r = torque
# torque / r = f
# f = m * a
# torque_shaft * 4 / r / m = a

max_accel = max_torque * GearRatio / WheelR / BikeM

accelNew = np.ones(len(data_trimmed['time']))

for i in range(0, len(data_trimmed['time'])):
    accelNew.put([i], max_accel * data_trimmed['torque scaling'])
