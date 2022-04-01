"""
Run code to calculate ...
Includes options
Output is shower_info_{}.txt and trigger_info_{}.txt, one for each energy bin
Needs to be run once for each array layout

"""

import numpy as np
import pandas as pd
import pickle
from optparse import OptionParser
import apply_threshold as thresh
import apply_trigger as trig
import os

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-r", "--runnumber", default = "0", help = "run number")
parser.add_option("-e", "--energy", default = "150", help = "energy bin")
parser.add_option("-d", "--distribution", default = "theta", help = "theta angle distribution, flat in theta=theta, flat in cos(theta)=costheta")
parser.add_option("-p", "--primary", default = "proton", help = "primary particle type, proton or iron")
parser.add_option("-s", "--season", default = "g", help = "season for atmosphere profile, s=summer, w=winter, g=general")
parser.add_option("-t", "--time", default = "g", help = "time for atmospheric profile, d=day, n=night, g=general")
parser.add_option("-l", "--location", default = "td", help = "location of detector, td=Taylor Dome")

parser.add_option("--scint", default="lo", help = "scintillator type, lo=Lofar, it=IceTop")

parser.add_option("--gennumber", default="0", help = "generation number of array layout")
parser.add_option("--arraynumber", default = "0", help = "number of array layout")
parser.add_option("--threshold", default = "energy", help = "trigger threshold on scintillators in MeV")
parser.add_option("--trynumber", default = "0", help = "number of core positions to chose")

(options, args) = parser.parse_args()

#initialise variables for input options
scint_type = str(options.scint)

gen_number = int(options.gennumber)
array_number = int(options.arraynumber)
trigger_thresh = float(options.threshold)
tries_number = int(options.trynumber) #how many core positions to chose, each one will make a different file

shower_number = int(options.runnumber) #CORSIKA run number, ( ie RET000040.txt is runnr=40)
energy_bin = int(options.energy)
theta_dist = str(options.distribution) #theta distribution to which the shower required belongs
prim_part = str(options.primary) #primary particle of shower
det_location = str(options.location) #detector location for which shower was simulated
det_season = str(options.season) #season for which the shower was simulated
det_time = str(options.time) #time of day for which the shower was simulated

#get number of scintillator pairs in detector layout
arrayfile = '/user/rstanley/detector/layout/layout_{0}_{1}.txt'.format(gen_number, array_number) 
array_file=open(arrayfile,'r')
det_positions=np.genfromtxt(array_file,skip_header=1)#,usecols=(0,1))
array_file.close()
det_number = det_positions.shape[0]
station_number = int(det_number / 2)

#create list of ALL showers for a particular array layout and whether they trigger the array above a threshold with half the stations triggering 
#if it doesn't exist already
shower_dict_file = 'shower_info_{0}_{1}_{3}_{2}_{4}_{5].csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin) #original system
#shower_dict_file = 'shower_info_{0}_{1}_{3}_{2}_{4}_{5}_3.csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin) #any 3 stations
#shower_dict_file = 'shower_info_{0}_{1}_{3}_{2}_{4}_{5}_hm.csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin) #half and mid
shower_dict_path = '/user/rstanley/detector/shower_info/' + shower_dict_file

if os.path.isfile(shower_dict_path):
    print('loaded shower dataframe file with threshold applied')
    shower_df = pd.read_csv(shower_dict_path, index_col=False, names=['try', 'type', 'energy', 'zenith', 'phi', 'core x', 'core y', 'detector x', 'detector y', 'total dep', 'gamma dep', 'e dep', 'mu dep', 'h dep', 'energy bin', 'zenith bin', 'shower number', 'over threshold'])

else:
    print('created new shower list file')
    shower_df = thresh.get_shower_list(theta_dist, prim_part, det_location, det_season, det_time, gen_number, array_number, shower_number, station_number, trigger_thresh, scint_type, energy_bin)
    shower_df.to_csv(shower_dict_path, header=False, index=False)


#apply trigger conditions to create new dataframe
trigger_dict_file = 'trigger_info_{0}_{1}_{3}_{2}_{4}_{5}.csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin)
#trigger_dict_file = 'trigger_info_{0}_{1}_{3}_{2}_{4}_{5}_3.csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin)
#trigger_dict_file = 'trigger_info_{0}_{1}_{3}_{2}_{4}_{5}_hm.csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin)
trigger_dict_path = '/user/rstanley/detector/trigger_info/' + trigger_dict_file


trigger_df = trig.get_trigger_list(shower_df, station_number, det_number)
trigger_df.to_csv(trigger_dict_path, header=False, index=False)





