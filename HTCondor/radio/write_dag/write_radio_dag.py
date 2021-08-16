"""
Write dag file for multiple radio calculation job submission on T2B HTCondor
Writes out job name, variable names and values, and log name for each job allocated
Input options
Outputs a dag file with all jobs for all showers requested
"""
from optparse import OptionParser
import os
import os.path
import numpy as np
from datetime import date
from datetime import datetime

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-r", "--runnumber", default = "0", help = "number of showers to use at each energy")
parser.add_option("-d", "--distribution", default = "theta", help = "theta angle distribution, flat in theta=theta, flat in cos(theta)=costheta")
parser.add_option("-z", "--zenithbin", default = "0", help = "zenith bin number of shower, 0-3 ")
parser.add_option("-p", "--primary", default = "proton", help = "primary particle type, proton or iron")
parser.add_option("-s", "--season", default = "g", help = "season for atmosphere profile, s=summer, w=winter, g=general")
parser.add_option("-t", "--time", default = "g", help = "time for atmospheric profile, d=day, n=night, g=general")
parser.add_option("-l", "--location", default = "td", help = "location of detector, td=Taylor Dome")

(options, args) = parser.parse_args()

"""
Convert parsed options to the format and type needed in code and error parsing 
"""
shower_number = int(options.runnumber)
#theta distribution, error handling for invalid distributions
theta_dist = str(options.distribution)
if (theta_dist != 'costheta') and (theta_dist != 'theta'):
    print(theta_dist, 'is not a currently supported theta distribution, please use --help for more information')
    exit()
#zenith bin, error handling for invalid bin numbers
theta_bin = int(options.zenithbin)
if (theta_bin != 0) and (theta_bin != 1) and (theta_bin != 2) and (theta_bin != 3):
    print(theta_bin, 'is not a currently supported zenith bin, please use --help for more information')
    exit()
#primary, error handling for invalid primary particles
prim_part = str(options.primary)
if (prim_part != 'proton') and (prim_part != 'iron'):
    print(prim_part, 'is not a currently supported primary particle, please use --help for more information')
    exit()
#detector season, error handling for invalid seasons
det_season = str(options.season)
if (det_season != 's') and (det_season != 'w') and (det_season != 'g'):
    print(det_season, 'is not a currently supported season, please use --help for more informaiton')
    exit()
#detector time, error handling for invalid times
det_time = str(options.time)
if (det_time != 'd') and (det_time != 'n') and (det_time != 'g'):
    print(det_time, 'is not a currently supported time, please use --help for more information')
    exit()
#detector location, error handling for invalid locations
det_location = str(options.location)
if (det_location != 'td'):
    print(det_location, 'is not a currently supported location, please use --help for more information')
    exit()

#energy_bin
log_energy = np.array([15.0, 15.2, 15.4, 15.6, 15.8, 16.0, 16.2, 16.4, 16.6, 16.8, 17.0, 17.2, 17.4, 17.6, 17.8, 18.0, 18.2, 18.4, 18.6, 18.8, 19.0])
bin_names = (10*log_energy).astype(int)

#create dag file for output
get_date = date.today().strftime('%Y%m%d')
get_time = datetime.now().strftime("%H%M%S")
dag_file_path = '/user/rstanley/simulations/HTCondor/radio/dagfiles/{0}/{1}/'.format(get_date, get_time)
os.makedirs(dag_file_path, exist_ok=True)
dag_file = '/user/rstanley/simulations/HTCondor/radio/dagfiles/{0}/{1}/run_radio_sim_{0}_{1}.dag'.format(get_date, get_time)
outfile=open(dag_file, 'w')

#generation of different jobs for dag file
job_counter = 0
for i in range(bin_names.shape[0]):
    energy_bin = bin_names[i]

    for j in range(shower_number):
        #check if run number exists for the particular energy bin
        run_number = "%06d" % (j + 1)
        longfile = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/DAT{7}.long'.format(theta_dist, det_location, prim_part, energy_bin, theta_bin, det_season, det_time, run_number)
        print(longfile)
        if os.path.isfile(longfile): #if file exists add a job to the dag file
            outfile.write('JOB job_{0} /user/rstanley/simulations/HTCondor/radio/run_radio_sim.submit\n'.format(job_counter))
            outfile.write('VARS job_{0} '.format(job_counter))
            outfile.write('THETA_DIST="{0}" '.format(theta_dist))
            outfile.write('THETA_BIN="{0}" '.format(theta_bin))
            outfile.write('ENERGY_BIN="{0}" '.format(energy_bin))
            outfile.write('PRIM_PART="{0}" '.format(prim_part))
            outfile.write('RUN_NUMBER="{0}" '.format(j))
            outfile.write('DET_SEASON="{0}" '.format(det_season))
            outfile.write('DET_TIME="{0}" '.format(det_time))
            outfile.write('DET_LOCATION="{0}" '.format(det_location))
            outfile.write('LOG_NAME="{0}_{1}_{2}_{3}_{4}"\n'.format(theta_dist, energy_bin, theta_bin, prim_part, j))

            job_counter += 1





