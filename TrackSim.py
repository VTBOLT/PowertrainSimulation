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

# find race start time - needs to be more accurate
start_time = 0
for i in range(0, len(data['4'])):
    if data['5'][i] >= 10:
        start_time = i
        break

# add indexes to drop
drop = np.ones(start_time, np.int8)
for i in range(0, start_time):
    drop.put([i], i)  # builds array for removing non-race data from data frame
print(drop)
for i in range(0, len(drop)):
    data_trimmed = data_df.take(data_df.index[drop])  # removes non-race data


speed = np.ones(len(data_trimmed['time']), np.float64)
distance = np.ones(len(data_trimmed['time']), np.float64)

for i in range(0, len(data_trimmed['time'])):                           # add bike speed to array for every time instance
    speed.put([i], data_trimmed['motorRPM'][i] / 4 / 60 * WheelD * pi)  # speed in meters per second
data_trimmed['speed'] = speed  # add new column to data frame

for i in range(0, len(data_trimmed['time'])):
    if i == 0:
        distance.put([0], data_trimmed['speed'][0] * data_trimmed['time'][0] - 1)
    else:
        distance.put([i], data_trimmed['speed'][i] * (data_trimmed['time'][i] - data_trimmed['time'][i-1]))
totalDistance = np.sum(distance, axis=0)  # total distance traveled on time interval in meters
print('total distance over given time interval: {}'.format(totalDistance))
print('All data: {}'.format(data_trimmed))

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