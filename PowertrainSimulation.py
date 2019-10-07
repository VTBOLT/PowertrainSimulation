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
    max_torque = 200
    max_rpm_max_torque = 3000
    min_torque = 20
    rpm_min_torque = 6000
    motor_mass = 20
    mc_mass = 10.7
    data_stripper = 1
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

    # Make m and b values for y=mx+b
    torque_slope = (max_torque - min_torque) / (max_rpm_max_torque - rpm_min_torque)
    torque_b = max_torque - (torque_slope * max_rpm_max_torque)

    # back calculate to get rpm
    # for now,
    currentSpeed = 10
    currentRPM = currentSpeed/(wheel_r * 2 * math.pi) * 60  # rotations per minute

    # making torque curve for specific powertrain setup
    increment = 0.1
    motorRPMs = np.arange(0, rpm_min_torque, (increment * data_stripper))
    torques = np.zeros(len(motorRPMs))
    for RPM in range(0, len(motorRPMs)):  # data stripper makes fewer datapoints
        if RPM < max_rpm_max_torque / (increment * data_stripper):
            # Flat slope for torque curve
            print(RPM)
            torques[RPM] = max_torque
        else:
            # Slope of torque curve
            torques[RPM] = torque_slope * currentRPM + torque_b

    plt.plot(motorRPMs, torques)
    plt.ylabel("Torque (N)")
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

    # torque = torque wheel = torque shaft * 4
    # f*r = torque
    # torque / r = f
    # f = m * a
    # torque_shaft * 4 / r / m = a

    max_accel = max_torque * gear_ratio / wheel_r / total_mass  # Some scaling factors definitely need to be added to this

    segment_times = np.zeros(data_df.shape[0])

    for i in range(0, data_df.shape[0]):
        if i % 2 is 1:  # segments bike is braking
            time = (2 * data_df['distances'][i]) / (data_df['final speed'][i] + data_df['final speed'][i - 1])
            segment_times.put([i], time)
        else:  # segments bike is accelerating
            if i is 0:
                det = 2 * max_accel * data_df['distances'][i]
                time = math.sqrt(det) / max_accel
                segment_times.put([i], time)
            else:
                det = pow(data_df['final speed'][i - 1], 2) + 2 * max_accel * data_df['distances'][i]
                time = (math.sqrt(det) - data_df['final speed'][i - 1]) / max_accel
                segment_times.put([i], time)

    total_time = np.sum(segment_times)

    print("Total time for powertrain {} is {}".format(powertrain_id, total_time))
    return total_time


if __name__ == '__main__':
    main()
