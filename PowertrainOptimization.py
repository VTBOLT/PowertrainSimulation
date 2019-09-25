"""
This program will ask for a csv of powertrain components to input and run them through PowertrainSimulation.py
"""

import numpy as np
import pandas as pd
import OriginalBikeModel as obike
import PowertrainSimulation as psim
import os

def main():
    # Create csv for all components then add to abspath line.
    # Create data frame with every possible combination of components.
    # Call OriginalBikeModel.py to get data from bolt 3
    # Call PowertrainSimulation.py with inputs as bolt 3 data frame and data in a row from
    # data frame of every possible combination corresponding to the ID of the powertrain being simulated.
    # data_frame, max_torque, max_rpm_of_max_torque, max_rpm, mass, pack_capacity_kWh, data_stripper

    location = os.path.abspath('CSVFiles\\BOLT3Data.csv')
    data = pd.read_csv(location, names=["max_torque", "max_rpm_of_max_torque", "max_rpm", "mass",
                                        "pack_capacity_kWh", "data_stripper"], header=0, low_memory=False)
    specs_df = data.DataFrame(data)
    combinations_df = pd.DataFrame()
    # iterate through every possible combination of specs and add each combination to combinations_df

    bolt3_df = obike.main()  # call OriginalBikeModel.py

    IDs_times = {}

    times = np.zeros(len(bolt3_df))

    for i in range(0, len(specs_df)):
        IDs_times[i] = psim.main(bolt3_df, specs_df.iloc[i])  # call PowertrainSimulation.py

main()