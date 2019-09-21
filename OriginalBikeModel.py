"""
This program will be run once to calculate a data table of binary throttle values
and the distance each throttle value is held. It writes that data to a csv file the
powertrain simulation can read from.
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import pi


def main():
    def get_distance(start, end):
        distance = np.zeros(end-start)
        for n in range(start, end):  # calculate the distance that throttle is held high
            thisDistance = data_df['speed'][n] * (data_df['time'][n] - data_df['time'][n - 1])  # calculate distance for one time interval
            distance.put([n-start], thisDistance)  # add distance from a single time interval to distance array for this throttle
        total_dist = np.sum(distance)
        return total_dist

    def add_to_arrays(dists, final_speed):
        dists.put([data_timeDist_counter - 1], total_distance)  # total distance over segment
        final_speed.put([data_timeDist_counter - 1], data_df['speed'][all_i])  # speed at end of segment

    MPHoRPM = 0.019337455  # MPH/RPM
    MPSoRPM = 0.008644633  # meters/s/RPM
    GearRatio = 4
    WheelD = 0.6604  # Wheel diameter in meters

    location = os.path.abspath('CSVFiles\\BOLT3Data.csv')  # csv file trimmed for data from when the bike is racing

    # create DataFrame
    data = pd.read_csv(location, names=['time', 'throttle', 'motorRPM'], header=0, low_memory=False)
    data_df = pd.DataFrame(data)
    data_timeDist = pd.DataFrame(columns=['time start', 'high low', 'distances', 'final speed'])

    # initialize arrays for new speed and distance data
    speed = np.ones(len(data_df['time']))
    torque_scaling = np.ones(len(data_df['time']))

    max_throttle = data_df['throttle'].max()

    # calculate instantaneous speed
    for i in range(0, len(data_df['time'])):
        speed.put([i], data_df['motorRPM'][i] / GearRatio / 60 * WheelD * pi)  # speed in meters per second
    data_df['speed'] = speed  # add speed column to data frame

    # scale throttle values for use in finding new bike's torque
    for i in range(0, len(data_df['time'])):
        torque_scaling.put([i], data_df['throttle'][i] / max_throttle)  # add scaled torque to numpy array

    time_start = np.ones(len(data_df['time']))
    high_low = np.ones(len(data_df['time']))
    distances = np.ones(len(data_df['time']))
    finalSpeedSeg = np.ones(len(data_df['time']))

    start_index = np.ones(len(data_df['time']))
    time_start_i = 0
    data_timeDist_counter = 0
    prevThrottleDown = False
    prevThrottle = False

    for all_i in range(0, len(data_df['time'])):
        if torque_scaling[all_i] >= 0.5 and not prevThrottle:  # if throttle went high
            prevThrottle = True
            high_low.put([data_timeDist_counter], 1)  # throttle went high - treating as max acceleration
            time_start.put([data_timeDist_counter], data_df['time'][all_i])

            if prevThrottleDown is True:  # find distance for previous low throttle and add to previous row
                total_distance = get_distance(time_start_i, all_i)
                add_to_arrays(distances, finalSpeedSeg)

            data_timeDist_counter = data_timeDist_counter + 1
            time_start_i = all_i

        if torque_scaling[all_i] <= 0.5 and prevThrottle:  # if throttle went low
            prevThrottleDown = True
            prevThrottle = False
            high_low.put([data_timeDist_counter], 0)  # throttle went low - treating as brake
            time_start.put([data_timeDist_counter], data_df['time'][all_i])

            total_distance = get_distance(time_start_i, all_i)  # find distance for high throttle and add to previous row
            add_to_arrays(distances, finalSpeedSeg)

            data_timeDist_counter = data_timeDist_counter + 1
            time_start_i = all_i

    data_timeDist['time start'] = time_start
    data_timeDist['high low'] = high_low
    data_timeDist['distances'] = distances
    data_timeDist['final speed'] = finalSpeedSeg

    df_toRemove = data_timeDist[data_timeDist['time start'] == 1]
    data_timeDist = data_timeDist.drop(df_toRemove.index, axis=0)  # drop extra rows left over from original dataframe size

    data_timeDist.to_csv(os.path.abspath('CSVFiles\\EditedBOLT3Data.csv'), index=None, header=True)

    print('All data:')
    print('{}'.format(data_timeDist))

    plt.plot(data_timeDist['time start'], data_timeDist['final speed'])

    plt.ylabel('final speed')
    plt.xlabel('time start')
    plt.show()


main()
