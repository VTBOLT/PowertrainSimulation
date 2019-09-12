# this program is called by the optimization program to determine how quickly the new bike can finish the race

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

# inputs: motor max torque and total bike mass

MPHoRPM = 0.019337455  # MPH/RPM
MPSoRPM = 0.008644633  # meters/s/RPM
GearRatio = 4
WheelR = 0.3302  # Wheel diameter in meters

# for