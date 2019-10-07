"""
This document is going to become the main scrip that will analyze a powertrain.
This will likely need to be imported as if it were a library so parameters can be passed in. As a result, this script
will not be able to run by itself.
"""

import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
import OriginalBikeModel as obike


# add motor/motor controller compatibility check?

# def main(data_df, max_torque, max_rpm_max_torque, min_torque, rpm_min_torque, motor_mass, mc_mass, pack_cap_kwh,
#         data_stripper, powertrain_id):


def main():

    def get_accel(current_speed):
        # calculate RPM from speed
        current_RPM = current_speed / (wheel_r * 2 * math.pi) * 60

        # find accel for that RPM
        if current_RPM < max_rpm_max_torque / (increment * data_stripper):
            # Flat slope for torque curve
            accel = max_a
        else:
            # Slope of torque curve
            accel = (torque_slope * current_RPM + torque_b) * t_to_a
        return accel

    max_torque = 200
    max_rpm_max_torque = 3000
    min_torque = 20
    rpm_min_torque = 6000
    motor_mass = 20
    mc_mass = 10.7
    data_stripper = 6000
    powertrain_id = 1

    # Traction control for beginning of race
    #   extra weight from rider makes center of mass near 0.49-0.48L (L is distance between centers of wheels)
    # Traction control for rest of race
    #   rider moves forward so center of mass near .5L

    # BOLT4 ratio and wheel radius
    gear_ratio = 4
    wheel_r = 0.3302  # Wheel radius in meters
    bike_mass = 200  # mass input from optimization program in kgs

    # add mass of each different pack type
    total_mass = bike_mass + motor_mass + mc_mass

    max_accel = max_torque * gear_ratio / wheel_r / total_mass  # Some scaling factors definitely need to be added to this

    # Make m and b values for y=mx+b
    torque_slope = (max_torque - min_torque) / (max_rpm_max_torque - rpm_min_torque)
    torque_b = max_torque - (torque_slope * max_rpm_max_torque)

    t_to_a = 0.1

    # define max torque
    max_a = max_torque * t_to_a

    # making torque curve for specific powertrain setup (this is only useful if you want to see how the curve looks)
    increment = 0.1

    # the six pairs of points required to create the simplified torque curve
    accels = np.array([t_to_a * max_torque, t_to_a * max_torque, t_to_a * min_torque])
    motorRPMs = np.array([0, max_rpm_max_torque, rpm_min_torque])

    plt.plot(motorRPMs, accels)
    plt.ylabel("Accel (m/s^2)")
    plt.xlabel("Motor RPM")
    plt.show()

    data_df = obike.main()
    # torque curve
    # input max rpm, power, and max torque
    # make torque curve
    # Make list of RPMs at each moment in time for each segment.
    # Make equation for acceleration.
    # Find velocity at each time point.
    # Calculate distance traveled.
    # If traveled enough distance, break.

    timeIncrements = data_df.shape[0] / (increment * data_stripper)
    dataSync = increment * data_stripper

    # make array of times
    # find distance traveled over each time interval AND speed at end of time interval
    # if distance is greater than or equal to distance for that segment, brake (braking is modeled as linear
    # because we don't have a brake curve yet
    segment_times = 0
    i = 0
    totalDistance = 0
    # CONTINUE WHILE TOTAL DISTANCE HASN'T BEEN COVERED
        # assume initial speed is zero
        # any other initial speeds become data_df['final speed'][(i-1) / dataSync]
        # this whole thing is weird because we have to use time to increment through each segment but using distance to
        #   determine when to stop
    while totalDistance < data_df['distances'].sum():
        if (i / dataSync) % 2 is 1:  # segments bike is braking. Divided so i lines up with data_df
            time = (2 * data_df['distances'][i / dataSync]) / (data_df['final speed'][i / dataSync] - data_df['final speed'][(i - 1) / dataSync])
            segment_times = segment_times + time
            totalDistance = totalDistance + data_df['distances'][i / dataSync]
        elif (i / dataSync) % 2 is 1:  # segments bike is accelerating
            if i is 0:
                current_speed = 0
            else:
                current_speed = data_df['final speed'][(i - 1) / dataSync]
                
            segDistance = 0
            while segDistance < data_df['distances'][i]:
                this_accel = get_accel(current_speed)

                det = 2 * get_accel(current_speed) * data_df['distances'][i]
                time = math.sqrt(det) / this_accel

                # time it takes to complete this segment
                segment_times = segment_times + time

                # add this interval's distance to the segment's distance
                segDistance = segDistance + distance

                # final speed of this segment
                current_speed = time * this_accel
            # add this segment's distance to the total distance
            totalDistance = totalDistance + segDistance
        i = i + data_stripper

    total_time = np.sum(segment_times)

    print("Total time for powertrain {} is {}".format(powertrain_id, total_time))
    return total_time


if __name__ == '__main__':
    main()
