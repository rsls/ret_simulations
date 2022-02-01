"""
Check the completeness of the corsika simulations already run
Identify missing showers
Identify missing files from showers that have been run successfully
Create summary of corsika showers that are incomplete or missing and need to be submitted again
"""
import numpy as np
import os
import os.path
from optparse import OptionParser

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-d", "--distribution", default = "theta", help = "theta angle distribution, flat in theta=theta, flat in cos(theta)=costheta")
parser.add_option("-p", "--primary", default = "proton", help = "primary particle type, proton or iron")
parser.add_option("-s", "--season", default = "g", help = "season for atmosphere profile, s=summer, w=winter, g=general")
parser.add_option("-t", "--time", default = "g", help = "time for atmospheric profile, d=day, n=night, g=general")
parser.add_option("-l", "--location", default = "td", help = "location of detector, td=Taylor Dome")

(options, args) = parser.parse_args()

"""
Convert parsed options to the format and type needed in code
"""
theta_dist = str(options.distribution)
prim_part = str(options.primary)
det_season = str(options.season)
det_time = str(options.time)
det_location = str(options.location)

energy_bin_list = np.array([150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190])
zenith_bin_list = np.array([0, 1, 2, 3])

#cycle through different energy and zenith bins
for i in range(energy_bin_list.shape[0]):
    energy_bin = energy_bin_list[i]

    for j in range(zenith_bin_list.shape[0]):
        zenith_bin = zenith_bin_list[j]

        #select directory to search in and offset file to compare run numbers against
        directory = '/pnfs/iihe/radar/corsika/QGSJET/{0}/{1}/{2}/{3}/{4}/{5}/{6}/'.format(theta_dist, det_location, prim_part, energy_bin, zenith_bin, det_season, det_time)
        offset_file = '/user/rstanley/simulations/HTCondor/corsika/offset/run_number_offset_{2}_{1}_{4}_{5}_{3}_{0}.txt'.format(theta_dist, det_location, prim_part, zenith_bin, det_season, det_time)
        run_number_offset = np.genfromtxt(offset_file, delimiter='\t')
        file_number = int(run_number_offset[i])
        
        for k in range(file_number):
            run_number = "%06d" % (k + 1)

            #get file names that are supposed to exist
            dat_file = directory + 'DAT{0}'.format(run_number)
            bin_file = directory + 'SIM{0}_coreas.bins'.format(run_number)
            long_file = directory + 'DAT{0}.long'.format(run_number)
            sim_dir = directory + 'SIM{0}_coreas/'.format(run_number)

            #check if files exist
            if os.path.isfile(dat_file):
                dat_file_exist = True
                if os.path.isfile(long_file):
                    long_file_exist = True
                    if os.path.isfile(bin_file):
                        bin_file_exist = True
                        if os.path.isdir(sim_dir):
                            sim_dir_exist = True
                            if os.listdir(sim_dir):
                                sim_dir_filled = True
                            else:
                                sim_dir_filled = False
                        else:
                            sim_dir_exist = False
                    else:
                        bin_file_exist = False
                else:
                    long_file_exist = False            
            else: 
                dat_file_exist = False
            
            #figure out how many and which files don't exist
            bools = {"DAT": dat_file_exist, "SIM bins": bin_file_exist, "DAT long": long_file_exist, "SIM dir": sim_dir_filled}
            files_false = [i for i in bools if not bools[i]]
            number_false = len(files_false)
            
            #print directory and run number of shower for which files don't exist
            if number_false >= 1:
                print(directory, 'with', run_number, 'files_missing:', files_false)
            else:
                continue

