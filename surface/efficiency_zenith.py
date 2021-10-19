"""
Calculate trigger efficiency with respect to shower zenith
"""

import numpy as np
import pandas as pd

def get_eff_zenith(shower_df):
    
    zenith_bin_low_deg_list = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
    zenith_bin_high_deg_list = zenith_bin_low_deg_list + 5

    zenith_bin_low_list = (np.pi / 180) * zenith_bin_low_deg_list
    zenith_bin_high_list = (np.pi / 180) * zenith_bin_high_deg_list

    zenith_trigger_efficiency = np.empty([zenith_bin_low_deg_list.shape[0]])

    for i in range(zenith_bin_low_deg_list.shape[0]):
        zenith_low = zenith_bin_low_list[i]
        zenith_high = zenith_bin_high_list[i]
        
        zenith_df = shower_df[((shower_df['zenith'] > zenith_low) & (shower_df['zenith'] <= zenith_high))]
        trigger_df = zenith_df[(zenith_df['trigger'] == 1)]

        number_of_showers = len(zenith_df.index)
        number_of_trigger = len(trigger_df.index)
    
        zenith_trigger_efficiency[i] = number_of_trigger / number_of_showers

    return zenith_bin_low_deg_list, zenith_trigger_efficiency


def get_eff_zenith_binned(shower_df, energy_bin):
    
    energy_bin = int(energy_bin)

    zenith_bin_low_deg_list = np.array([0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
    zenith_bin_high_deg_list = np.array([10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65])

    zenith_bin_low_list = (np.pi / 180) * zenith_bin_low_deg_list
    zenith_bin_high_list = (np.pi / 180) * zenith_bin_high_deg_list

    zenith_trigger_efficiency_binned = np.empty([zenith_bin_low_deg_list.shape[0]])

    shower_df_stripped = shower_df[shower_df['energy_bin'] == energy_bin]

    for i in range(zenith_bin_low_deg_list.shape[0]):
        zenith_low = zenith_bin_low_list[i]
        zenith_high = zenith_bin_high_list[i]
        
        zenith_df = shower_df_stripped[((shower_df_stripped['zenith'] > zenith_low) & (shower_df_stripped['zenith'] <= zenith_high))]
        trigger_df = zenith_df[(zenith_df['trigger'] == 1)]

        number_of_showers = len(zenith_df.index)
        number_of_trigger = len(trigger_df.index)
        
        if (number_of_trigger == 0) and (number_of_showers == 0):
            zenith_trigger_efficiency_binned[i] = 0
        else:
            zenith_trigger_efficiency_binned[i] = number_of_trigger / number_of_showers

    return zenith_bin_low_deg_list, zenith_trigger_efficiency_binned


