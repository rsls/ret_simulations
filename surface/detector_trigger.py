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
shower_dict = sl.get_shower_list(theta_dist, prim_part, det_location, det_season, det_time, array_number, shower_number, trys_number, station_number, trigger_thresh)

out_file = open('shower_info_{0}_{1}.pkl'.format(arraynr, int(trigger_thresh)), 'wb')
pickle.dump(shower_dict, out_file)
out_file.close()

#create dataframe with all information from dictionary
shower_df = pd.DataFrame(shower_dict)

#calculate trigger efficiency
log_energy_list, energy_trigger_efficiency = ee.get_eff_energy(shower_df)
zenith_bin_low_deg_list, zenith_trigger_efficiency = ez.get_eff_zenith(shower_df)

#save trigger efficiency
save_file = 'trigger_eff_{0}_{1}.npz'.format(arraynr, int(trigger_thresh))
np.savez(save_file, log_energy_list=logE, energy_trigger_efficiency=Etrigeff, zenith_bin_low_deg_list=Zlow, zenith_trigger_efficiency=Ztrigeff)

