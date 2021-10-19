"""
Run code to calculate trigger efficiency for a particular array layout based on deposit files created with detector_run.py
Includes options
Output is a trigger_{}.txt with trigger efficiency per energy or zenith bin and dictionary of all shower information including trigger status
Needs to be run once for each array layout
Collects all information about a shower in a dictionary, including whether it's triggered in particular conditions, outputs dictionary and calculates trigger efficiency
"""

import numpy as np
import pandas as pd
import pickle
import shower_list as sl
import efficiency_energy as ee
import efficiency_zenith as ez
from optparse import OptionParser
import os

# Parse commandline options
parser = OptionParser()

parser.add_option("-r", "--runnumber", default = "0", help = "number of showers to use at each energy")
parser.add_option("-d", "--distribution", default = "theta", help = "theta angle distribution, flat in theta=theta, flat in cos(theta)=costheta")
parser.add_option("-p", "--primary", default = "proton", help = "primary particle type, proton or iron")
parser.add_option("-s", "--season", default = "g", help = "season for atmosphere profile, s=summer, w=winter, g=general")
parser.add_option("-t", "--time", default = "g", help = "time for atmospheric profile, d=day, n=night, g=general")
parser.add_option("-l", "--location", default = "td", help = "location of detector, td=Taylor Dome")

parser.add_option("--arraynumber", default = "0", help = "number of array layout")
parser.add_option("--threshold", default = "energy", help = "trigger threshold on scintillators in MeV")
parser.add_option("--trynumber", default = "0", help = "number of core positions to take")

(options, args) = parser.parse_args()

#initialise variables for input options
array_number = int(options.arraynumber)
trigger_thresh = float(options.threshold)
trys_number = int(options.trynumber)

shower_number = "%06d" %int(options.runnumber) #number of showers to use at each energy
theta_dist = str(options.distribution) #theta distribution to which the shower required belongs
prim_part = str(options.primary) #primary particle of shower
det_location = str(options.location) #detector location for which shower was simulated
det_season = str(options.season) #season for which the shower was simulated
det_time = str(options.time) #time of day for which the shower was simulated

#get number of scintillator pairs in detector layout
arrayfile = '/user/rstanley/detector/layout/layout_{0}.txt'.format(array_number) 
array_file=open(arrayfile,'r')
det_positions=np.genfromtxt(array_file,skip_header=1)#,usecols=(0,1))
array_file.close()
det_number = det_positions.shape[0]
station_number = int(det_number / 2)

#create list of ALL showers for a particular array layout and whether they trigger the array above a threshold with half the stations triggering 
#if it doesn't exist already
shower_dict_file = 'shower_info_{0}_{1}.pkl'.format(array_number, int(trigger_thresh))
shower_dict_path = '/user/rstanley/detector/shower_info/' + shower_dict_file

if os.path.isfile(shower_dict_path):
    print('loaded pickled shower list file')
    in_file = open(shower_dict_path, 'rb')
    shower_dict = pickle.load(in_file)
    

else:
    print('created new shower list file')
    shower_dict = sl.get_shower_list(theta_dist, prim_part, det_location, det_season, det_time, array_number, shower_number, trys_number, station_number, trigger_thresh)

    out_file = open(shower_dict_file, 'wb')
    pickle.dump(shower_dict, out_file)
    out_file.close()
    
#create dataframe with all information from dictionary
shower_df = pd.DataFrame(shower_dict)

#calculate trigger efficiency for energy and save in human readable format
logE, Etrigeff = ee.get_eff_energy(shower_df)
trigger_energy_dict = {'log energy':logE, 'trig eff energy':Etrigeff}
trigger_energy_df = pd.DataFrame(trigger_energy_dict)
save_energy_file = 'trigger_energy_eff_{0}_{1}.csv'.format(array_number, int(trigger_thresh))
trigger_energy_df.to_csv(save_energy_file, sep='\t')


#calculate trigger efficiency for energy in different zenith bins and save in human readable format
zenith_bin_list = np.array([0, 1, 2, 3])

for i in range (zenith_bin_list.shape[0]):
    zenith_bin = zenith_bin_list[i]
    
    logE, Etrigeff_bin = ee.get_eff_energy_binned(shower_df, zenith_bin)
    trigger_energy_binned_dict = {'log energy':logE, 'trig eff energy bin':Etrigeff_bin}
    trigger_energy_binned_df = pd.DataFrame(trigger_energy_binned_dict)
    save_energy_binned_file = 'trigger_energy_eff_binned_{0}_{1}_{2}.csv'.format(array_number, int(trigger_thresh), zenith_bin)
    trigger_energy_binned_df.to_csv(save_energy_binned_file, sep='\t')

#calculate trigger efficiency for zenith and save in human readable format
Zlow, Ztrigeff = ez.get_eff_zenith(shower_df)
trigger_zenith_dict = {'zenith bin deg low':Zlow, 'trig eff zenith':Ztrigeff}
trigger_zenith_df = pd.DataFrame(trigger_zenith_dict)
save_zenith_file = 'trigger_zenith_eff_{0}_{1}.csv'.format(array_number, int(trigger_thresh))
trigger_zenith_df.to_csv(save_zenith_file, sep='\t')


#calculate trigger efficiency for zenith in different energy bins and save in human readable format
energy_bin_list = np.array([150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190])

for j in range (energy_bin_list.shape[0]):
    energy_bin = energy_bin_list[j]
    
    Zlow, Ztrigeff_bin = ez.get_eff_zenith_binned(shower_df, energy_bin)
    trigger_zenith_binned_dict = {'zenith bin deg low':Zlow, 'trig eff zenith':Ztrigeff_bin}
    trigger_zenith_binned_df = pd.DataFrame(trigger_zenith_binned_dict)
    save_zenith_binned_file = 'trigger_zenith_eff_binned_{0}_{1}_{2}.csv'.format(array_number, int(trigger_thresh), energy_bin)
    trigger_zenith_binned_df.to_csv(save_zenith_binned_file, sep='\t')




