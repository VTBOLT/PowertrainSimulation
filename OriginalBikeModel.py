# run this program once to calculate a data table of scalable throttle values versus distance on the track


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

MPHoRPM = 0.019337455  # MPH/RPM
MPSoRPM = 0.008644633  # meters/s/RPM
GearRatio = 4
WheelD = 0.6604  # Wheel diameter in meters

CurrentMotor = 120000
NewMotor = 120000
tolerance = 10

# laps = input("Number of laps: ")  # this can be included in csv file in the future if we find that easier

file_name = r'\RUN4ThrottleRPM4.csv'
file_path = r'C:\Users\sesch\Desktop\BOLT\Converted'
location = file_path + file_name

# create DataFrame
data = pd.read_csv(location, names=['time', 'throttle', 'motorRPM'], header=0, low_memory=False)
data_df = pd.DataFrame(data)
data_torqDist = pd.DataFrame(columns=['torque scale', 'distance'])

start_time = 0
# drop unused indexes
data_trimmed = data_df.shift(-start_time)
data_trimmed = data_trimmed.dropna()

# initialize arrays for new speed and distance data
speed = np.ones(len(data_trimmed['time']))
distance = np.ones(len(data_trimmed['time']))
throttle_binary = np.ones(len(data_trimmed['time']))
torque_scaling = np.ones(len(data_trimmed['time']))

max_throttle = data_trimmed['throttle'].max()

# calculate 'instantaneous' speed
for i in range(0, len(data_trimmed['time'])):
    speed.put([i], data_trimmed['motorRPM'][i] / GearRatio / 60 * WheelD * pi)  # speed in meters per second
data_trimmed['speed'] = speed  # add speed column to data frame

# calculate aggregated distance
for i in range(0, len(data_trimmed['time'])):
    if i == 0:
        distance.put([0], data_trimmed['speed'][0] * data_trimmed['time'][0] - 1)
    else:
        prevDistance = distance[i-1]
        thisDistance = data_trimmed['speed'][i] * (data_trimmed['time'][i] - data_trimmed['time'][i-1])
        distance.put([i], prevDistance + thisDistance)
data_torqDist['distance'] = distance  # add distance column to final data frame

# scale throttle values for use in finding new bike's torque
for i in range(0, len(data_trimmed['time'])):
    torque_scaling.put([i], data_trimmed['throttle'][i]/max_throttle)
data_torqDist['torque scale'] = torque_scaling  # add scaled torque column to final data frame

print('total distance over given time interval: {}'.format(distance[len(distance)-1]))
print('All data:')
print('{}'.format(data_trimmed))


plt.plot(data_torqDist['distance'], data_torqDist['torque scaling'])

plt.ylabel('Torque scaling')
plt.xlabel('Distance')
plt.show()

# still need intervals for acceleration vs braking so we know over what distance to scale the torque