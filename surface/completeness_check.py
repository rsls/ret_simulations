"""
Check the completeness of the surface simulations already run
Identify missing deposit files
Create summary of surface simulations that are incomplete or missing and need to be submitted again
"""
import numpy as np
import os
import os.path
from optparse import OptionParser

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-r", "--runnumber", default = "0", help = "number of showers to use at each energy")
parser.add_option("-d", "--distribution", default = "theta", help = "theta angle distribution, flat in theta=theta, flat in cos(theta)=costheta")
parser.add_option("-p", "--primary", default = "proton", help = "primary particle type, proton or iron")
parser.add_option("-s", "--season", default = "g", help = "season for atmosphere profile, s=summer, w=winter, g=general")
parser.add_option("-t", "--time", default = "g", help = "time for atmospheric profile, d=day, n=night, g=general")
parser.add_option("-l", "--location", default = "td", help = "location of detector, td=Taylor Dome")
parser.add_option("--arraynumber", default = "0", help = "number of array layout")
parser.add_option("--trynumber", default = "0", help = "number of core positions to chose")

(options, args) = parser.parse_args()

"""
Convert parsed options to the format and type needed in code
"""
file_number = int(options.runnumber)
theta_dist = str(options.distribution)
prim_part = str(options.primary)
det_season = str(options.season)
det_time = str(options.time)
det_location = str(options.location)
array_number = int(options.arraynumber)
attempt_number = int(options.trynumber)

energy_bin_list = np.array([150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190])
zenith_bin_list = np.array([0, 1, 2, 3])

#cycle through different energy and zenith bins
for i in range(energy_bin_list.shape[0]):
    energy_bin = energy_bin_list[i]

    for j in range(zenith_bin_list.shape[0]):
        zenith_bin = zenith_bin_list[j]

        #select directory to search in and offset file to compare run numbers against
        directory = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/'.format(theta_dist, det_location, prim_part, energy_bin, zenith_bin, det_season, det_time)
        offset_file = '/user/rstanley/simulations/HTCondor/corsika/offset/run_number_offset_{2}_{1}_{4}_{5}_{3}_{0}.txt'.format(theta_dist, det_location, prim_part, zenith_bin, det_season, det_time)
        run_number_offset = np.genfromtxt(offset_file, delimiter='\t')
        max_file_number = int(run_number_offset[i])

        for k in range(file_number):
            run_number = k + 1
            long_run_number = "%06d" % (k + 1)
        
            dat_file = directory + 'DAT{0}'.format(long_run_number)

            attempt_success = np.empty([attempt_number])

            for l in range(attempt_number):
                try_number = l
               
                deposit_file = directory + 'deposit/deposit_{2}/deposit{0}_{1}.dat'.format(run_number, try_number, array_number)

                if os.path.isfile(dat_file) and os.path.isfile(deposit_file):
                    attempt_success[l] = 0

                elif os.path.isfile(dat_file) and not os.path.isfile(deposit_file):
                    attempt_success[l] = 1

                elif not os.path.isfile(dat_file):
                    attempt_success[l] = 2
                    print(directory, 'with', long_run_number, 'missing dat file')

            try_number_fail = np.where(attempt_success == 1)
    
            if try_number_fail[0].shape[0] >= 1:
                print(directory, 'with', long_run_number, 'missing tries with numbers', try_number_fail)

            else:
                continue






















