"""
Calculate trigger efficiency with respect to shower energy
"""
import numpy as np
import pandas as pd

def get_eff_energy(shower_df):

    energy_bin_list = np.array([150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190])
    log_energy_list = energy_bin_list / 10
    energy_trigger_efficiency = np.empty([len(energy_bin_list)])

    for i in range(len(energy_bin_list)):
        energy_bin = energy_bin_list[i]

        energy_df = shower_df[shower_df['energy bin'] == energy_bin]
        trigger_df = energy_df[(energy_df['trigger'] == 1)]

        number_of_showers = len(energy_df.index)
        number_of_trigger = len(trigger_df.index)
    
        energy_trigger_efficiency[i] = number_of_trigger / number_of_showers

    return log_energy_list, energy_trigger_efficiency


def get_eff_energy_binned(shower_df, zenith_bin):
    
    zenithbin = int(zenith_bin)

    energy_bin_list = np.array([150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190])
    log_energy_list = energy_bin_list / 10
    energy_trigger_efficiency_binned = np.empty([len(energy_bin_list)])

    shower_df['zenith bin'] = shower_df['zenith bin'].astype(int)
  
    shower_df_stripped = shower_df[shower_df['zenith bin'] == zenithbin].reset_index(drop=True)

    for i in range(len(energy_bin_list)):
        energy_bin = energy_bin_list[i]

        energy_df = shower_df_stripped[shower_df_stripped['energy bin'] == energy_bin]
        trigger_df = energy_df[(energy_df['trigger'] == 1)]

        number_of_showers = len(energy_df.index)
        number_of_trigger = len(trigger_df.index)
    
        energy_trigger_efficiency_binned[i] = number_of_trigger / number_of_showers


    return log_energy_list, energy_trigger_efficiency_binned


