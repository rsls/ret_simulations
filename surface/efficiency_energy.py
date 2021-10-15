"""
Calculate trigger efficiency with respect to shower energy
"""
import numpy as np
import pandas as pd

def get_eff_energy(shower_df):

    energy_bin_list = np.array([150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190])
    energy_bin_low_list = energy_bin_list - 1
    energy_bin_high_list = energy_bin_list + 1 

    log_energy_list = energy_bin_list / 10
    log_energy_low_list = energy_bin_low_list / 10
    log_energy_high_list = energy_bin_high_list / 10

    energy_trigger_efficiency = np.empty([energy_bin_list.shape[0]])

    for i in range(energy_bin_list.shape[0]):
        energy_low = 10 ** log_energy_low_list[i]
        energy_high = 10 ** log_energy_high_list[i]

        energy_df = shower_df[((shower_df['energy'] >= energy_low) & (shower_df['energy'] <= energy_high))]
        trigger_df = energy_df[(energy_df['trigger'] == 1)]

        number_of_showers = len(energy_df.index)
        number_of_trigger = len(trigger_df.index)
    
        energy_trigger_efficiency[i] = number_of_trigger / number_of_showers

    return log_energy_list, energy_trigger_efficiency

"""
def get_eff_energy_binned(shower_df, zenith_bin):
    
    zenith_bin = int(zenith_bin)

    energy_bin_list = np.array([150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190])
    energy_bin_low_list = energy_bin_list - 1
    energy_bin_high_list = energy_bin_list + 1 

    log_energy_list = energy_bin_list / 10
    log_energy_low_list = energy_bin_low_list / 10
    log_energy_high_list = energy_bin_high_list / 10

    energy_trigger_efficiency_binned = np.empty([energy_bin_list.shape[0]])

    shower_df_stripped = shower_df[shower_df['zenith_bin'] == zenith_bin]

    for i in range(energy_bin_list.shape[0]):
        energy_low = 10 ** log_energy_low_list[i]
        energy_high = 10 ** log_energy_high_list[i]

        energy_df = shower_df[((shower_df_stripped['energy'] >= energy_low) & (shower_df_stripped['energy'] <= energy_high))]
        trigger_df = energy_df[(energy_df['trigger'] == 1)]

        number_of_showers = len(energy_df.index)
        number_of_trigger = len(trigger_df.index)
    
        energy_trigger_efficiency_binned[i] = number_of_trigger / number_of_showers


    return log_energy_list, energy_trigger_efficiency_binned

"""
