import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

MPHoRPM = 0.019337455  # MPH/RPM
MPSoRPM = 0.008644633  # meters/s/RPM
GearRatio = 4
WheelD = 0.6604 # Wheel diameter in meters

CurrentMotor = 120000
NewMotor = 120000
tolerance = 10

# laps = input("Number of laps: ")  # this can be included in csv file in the future if we find that easier

file_name = r'\NJMP6_first4lapstwice.csv'
file_path = r'C:\Users\sesch\Desktop\BOLT\Converted'
location = file_path + file_name

data = pd.read_csv(location, names=['time', 'throttle', 'motorRPM', '4', '5', '6'], header=0, low_memory=False)
data_df = pd.DataFrame(data)

speed = np.ones(len(data_df['time']), np.float64)

for i in range(1, len(data_df['time'])):                           # add bike speed to array for every time instance
    speed.put([i], data_df['motorRPM'][i] / 4 / 60 * WheelD * pi)  # speed in meters per second
data_df['speed'] = speed  # add new column to DataFrame
print(data_df)


"""
time_offset = []
for t in range(0, len(data)):
    if data['pack_current'][t] >= 10:
        start_time = t
        break
# print(len(data))
plt.plot(data['time'], data['pack_current'])

plt.ylabel('Pack Current')
plt.xlabel('Time')
plt.show()
"""