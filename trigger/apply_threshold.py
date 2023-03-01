"""
From DEP*.txt files, apply threshold condition and make pandas dataframe of all showers
"""
import numpy as np
import pandas as pd
import os


def get_shower_list(theta_dist, prim_part, det_location, det_season, det_time, gen_number, array_number, shower_number, station_number, threshold, scint_type, energy_bin):

    col_names = ['try', 'type', 'energy', 'zenith', 'phi', 'core x', 'core y', 'detector x', 'detector y', 'total dep', 'gamma dep', 'e dep', 'mu dep', 'h dep']
    zenith_bin_list = [0, 1, 2, 3]
    shower_number = int(shower_number)

    all_shower_df = pd.DataFrame(columns=['try', 'type', 'energy', 'zenith', 'phi', 'core x', 'core y', 'detector x', 'detector y', 'total dep', 'gamma dep', 'e dep', 'mu dep', 'h dep', 'energy bin', 'zenith bin', 'shower number', 'over threshold'])

    for zenith_bin in zenith_bin_list:

        for i in range(shower_number):
            run_number = i + 1
            cor_run_number = "%06d" % run_number

            depositfile = '/pnfs/iihe/radar/corsika/QGSJET/{0}/{1}/{2}/{3}/{4}/{5}/{6}/deposit/deposit_{7}_{8}/DEP{9}_{10}.txt'.format(theta_dist, det_location, prim_part, energy_bin, zenith_bin, det_season, det_time, gen_number, array_number, cor_run_number, scint_type)

            if os.path.isfile(depositfile):
            #for n in range(1):
                    
                try:
                #for m in range(1):

                    single_shower_df = pd.read_csv(depositfile, sep='\t', names=col_names)
                    single_shower_df['energy bin'] = energy_bin
                    single_shower_df['zenith bin'] = zenith_bin
                    single_shower_df['shower number'] = run_number
                    single_shower_df['over threshold'] = np.where(single_shower_df['total dep'] >= threshold, True, False)

                    print(zenith_bin)  

                    all_shower_df = pd.concat([all_shower_df, single_shower_df], ignore_index=True, axis=0)

                except Exception as e_message:
                    print(depositfile)
                    print(e_message)
                            
    return all_shower_df
