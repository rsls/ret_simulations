"""
From shower list dataframe, apply trigger conditions and make pandas dataframe of all showers
"""
import numpy as np
import pandas as pd
import os

def get_trigger_list(shower_df, station_number, det_number, station_req):

    slice_start = 0
    slice_end = det_number

    slice_number = int(shower_df.shape[0] / det_number)

    all_shower_df = pd.DataFrame()

    for i in range(slice_number):
        slice_df = shower_df.iloc[slice_start:slice_end, :]

        station_slice = np.array_split(np.array(slice_df['over threshold']), station_number)
        station_trigger = [sum(array) for array in station_slice]
        station_trigger_number = int(sum([array/2 if array==2 else 0 for array in station_trigger]))

        half_slice = np.array_split(station_trigger, 2)
        half_trigger = [sum(array) for array in half_slice]

        if station_trigger_number >= int(station_req):
            array_trigger = 1

        else:
            array_trigger = 0
        
        single_shower_list = [slice_df['try'].iloc[0], slice_df['type'].iloc[0], slice_df['energy bin'].iloc[0], slice_df['energy'].iloc[0], slice_df['zenith bin'].iloc[0], slice_df['zenith'].iloc[0], slice_df['phi'].iloc[0], slice_df['core x'].iloc[0], slice_df['core y'].iloc[0], array_trigger, station_trigger_number]
        column_names = ['try', 'type', 'energy bin', 'energy', 'zenith bin', 'zenith', 'phi', 'core x', 'core y', 'trigger', 'stations trigger']

        single_shower_df = pd.DataFrame([single_shower_list], columns=column_names)

        all_shower_df = pd.concat([all_shower_df, single_shower_df], ignore_index=True, axis=0)

        slice_start += det_number
        slice_end += det_number

    return all_shower_df


        
