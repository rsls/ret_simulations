import numpy as np
import pandas as pd
import pickle
from optparse import OptionParser
import efficiency_energy as ee
import efficiency_zenith as ez
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

(options, args) = parser.parse_args()

#initialise variables for input options
scint_type = str(options.scint)

gen_number = int(options.gennumber)
array_number = int(options.arraynumber)
trigger_thresh = float(options.threshold)

shower_number = int(options.runnumber) #CORSIKA run number, ( ie RET000040.txt is runnr=40)
energy_bin = int(options.energy)
theta_dist = str(options.distribution) #theta distribution to which the shower required belongs
prim_part = str(options.primary) #primary particle of shower
det_location = str(options.location) #detector location for which shower was simulated
det_season = str(options.season) #season for which the shower was simulated
det_time = str(options.time) #time of day for which the shower was simulated

column_names = ['try', 'type', 'energy bin', 'energy', 'zenith bin', 'zenith', 'phi', 'core x', 'core y', 'trigger', 'stations trigger']
energy_bin_list = [150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190]

all_shower_df = pd.DataFrame()

for energy_bin in energy_bin_list:
    trigger_dict_file = 'trigger_info_{0}_{1}_{3}_{2}_{4}_{5}.csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin)
    #trigger_dict_file = 'trigger_info_{0}_{1}_{3}_{2}_{4}_{5}_3.csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin)
    #trigger_dict_file = 'trigger_info_{0}_{1}_{3}_{2}_{4}_{5}_hm.csv'.format(gen_number, array_number, int(trigger_thresh), scint_type, shower_number, energy_bin)
    trigger_dict_path = '/user/rstanley/detector/trigger_info/' + trigger_dict_file

    small_shower_df = pd.read_csv(trigger_dict_path, index_col=False, header=None)

    all_shower_df = pd.concat([all_shower_df, small_shower_df], ignore_index=True, axis=0)

all_shower_df.columns = column_names
all_shower_df.to_csv('/user/rstanley/all_shower_df.csv', index=False)
#all_shower_df.to_csv('/user/rstanley/all_shower_df_3.csv', index=False)
#all_shower_df.to_csv('/user/rstanley/all_shower_df_hm.csv', index=False)

#calculate trigger efficiency for energy and save in human readable format
logE, Etrigeff = ee.get_eff_energy(all_shower_df)
trigger_energy_dict = {'log energy':logE, 'trig eff energy':Etrigeff}
trigger_energy_df = pd.DataFrame(trigger_energy_dict)
save_energy_file = '/user/rstanley/detector/efficiency/trigger_energy_eff_{0}_{1}.csv'.format(array_number, int(trigger_thresh))
#save_energy_file = '/user/rstanley/detector/efficiency/trigger_energy_eff_{0}_{1}_3.csv'.format(array_number, int(trigger_thresh))
#save_energy_file = '/user/rstanley/detector/efficiency/trigger_energy_eff_{0}_{1}_hm.csv'.format(array_number, int(trigger_thresh))
trigger_energy_df.to_csv(save_energy_file, sep='\t')


#calculate trigger efficiency for energy in different zenith bins and save in human readable format
zenith_bin_list = [0, 1, 2, 3]

for zenith_bin in zenith_bin_list:
    
    logE, Etrigeff_bin = ee.get_eff_energy_binned(all_shower_df, zenith_bin)
    trigger_energy_binned_dict = {'log energy':logE, 'trig eff energy bin':Etrigeff_bin}
    trigger_energy_binned_df = pd.DataFrame(trigger_energy_binned_dict)
    save_energy_binned_file = '/user/rstanley/detector/efficiency/trigger_energy_eff_binned_{0}_{1}_{2}.csv'.format(array_number, int(trigger_thresh), zenith_bin)
    #save_energy_binned_file = '/user/rstanley/detector/efficiency/trigger_energy_eff_binned_{0}_{1}_{2}_3.csv'.format(array_number, int(trigger_thresh), zenith_bin)
    #save_energy_binned_file = '/user/rstanley/detector/efficiency/trigger_energy_eff_binned_{0}_{1}_{2}_hm.csv'.format(array_number, int(trigger_thresh), zenith_bin)
    trigger_energy_binned_df.to_csv(save_energy_binned_file, sep='\t')

#calculate trigger efficiency for zenith and save in human readable format
Zlow, Ztrigeff = ez.get_eff_zenith(all_shower_df)
trigger_zenith_dict = {'zenith bin deg low':Zlow, 'trig eff zenith':Ztrigeff}
trigger_zenith_df = pd.DataFrame(trigger_zenith_dict)
save_zenith_file = '/user/rstanley/detector/efficiency/trigger_zenith_eff_{0}_{1}.csv'.format(array_number, int(trigger_thresh))
#save_zenith_file = '/user/rstanley/detector/efficiency/trigger_zenith_eff_{0}_{1}_3.csv'.format(array_number, int(trigger_thresh))
#save_zenith_file = '/user/rstanley/detector/efficiency/trigger_zenith_eff_{0}_{1}_hm.csv'.format(array_number, int(trigger_thresh))
trigger_zenith_df.to_csv(save_zenith_file, sep='\t')

#calculate trigger efficiency for zenith in different energy bins and save in human readable format

for energy_bin in energy_bin_list:
   
    Zlow, Ztrigeff_bin = ez.get_eff_zenith_binned(all_shower_df, energy_bin)
    trigger_zenith_binned_dict = {'zenith bin deg low':Zlow, 'trig eff zenith':Ztrigeff_bin}
    trigger_zenith_binned_df = pd.DataFrame(trigger_zenith_binned_dict)
    save_zenith_binned_file = '/user/rstanley/detector/efficiency/trigger_zenith_eff_binned_{0}_{1}_{2}.csv'.format(array_number, int(trigger_thresh), energy_bin)
    #save_zenith_binned_file = '/user/rstanley/detector/efficiency/trigger_zenith_eff_binned_{0}_{1}_{2}_3.csv'.format(array_number, int(trigger_thresh), energy_bin)
    #save_zenith_binned_file = '/user/rstanley/detector/efficiency/trigger_zenith_eff_binned_{0}_{1}_{2}_hm.csv'.format(array_number, int(trigger_thresh), energy_bin)
    trigger_zenith_binned_df.to_csv(save_zenith_binned_file, sep='\t')    


