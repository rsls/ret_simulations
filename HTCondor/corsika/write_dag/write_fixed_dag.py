"""
Write dag file for multiple corsika job submission on T2B HTCondor with fixed core positions and antenna locations in ground plane for CoREAS with core positions, zenith, and azimuth taken from file
Writes out job name, variable names and values, and log name for each job allocated
Input options include energy showers desired (used to calculate number of showers at other energies), index of cosmic ray spectrum (usually -1), and many more
Outputs a dag file with all jobs for all energies requested as well as txt file containing number of showers at each energy requested
"""
from optparse import OptionParser
import os
import numpy as np
from datetime import date
from datetime import datetime
import gen_parameters as gp

max_phi = 360
cr_index = -1

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-d", "--distribution", default = "theta", help = "theta angle distribution, flat in theta=theta, flat in cos(theta)=costheta")
parser.add_option("-p", "--primary", default = "proton", help = "primary particle type, proton or iron")
parser.add_option("-s", "--season", default = "g", help = "season for atmosphere profile, s=summer, w=winter, g=general")
parser.add_option("-t", "--time", default = "g", help = "time for atmospheric profile, d=day, n=night, g=general")
parser.add_option("-l", "--location", default = "td", help = "location of detector, td=Taylor Dome")
parser.add_option("-u", "--energy", default = "0", help = "log energy of showers with properties taken from file")
parser.add_option("--inputfile", default = "/user/rstanley/", help = "location of file with core positions, zenith and azimuths")
(options, args) = parser.parse_args()

"""
Convert parsed options to the format and type needed in code and error parsing
"""
#theta distribution, error handling for invalid distribution
theta_dist = str(options.distribution)
if (theta_dist != 'costheta') and (theta_dist != 'theta'):
    print(theta_dist, 'is not a currently supported theta distribution, please use --help for more information')
    exit()
#primary type, error handling for invalid type
prim_part = str(options.primary)
if (prim_part == 'proton'):
    prim_type = 14
elif (prim_part == 'iron'):
    prim_type = 5626
else:
    print(prim_part, 'is not a currently supported primary particle type, please use --help for more information')
    exit()
#season, error handling for invalid season
det_season = str(options.season)
if (det_season != 's') and (det_season != 'w') and (det_season != 'g'):
    print(det_season, 'is not a currently supported option for season, please use --help for more information')
    exit()
#time, error handling for invalid season
det_time = str(options.time)
if (det_time != 'd') and (det_time != 'n') and (det_time != 'g'):
    print(det_time, 'is not a currently supported option for time, please use --help for more inforamtion')
    exit()
#location, error handling for invalid location
det_location = str(options.location)
if (det_location != 'td'):
    print(det_location, 'is not a currently supported location, please use --help for more information')
    exit()
#theta bin, 0-45 degrees shoved in bin 0 because I just need a number
theta_bin = 0
#energy
log_energy = float(options.energy)
energy = 10**log_energy
energy_GeV = energy / (10**9)
energy_bin = int(10*log_energy)
#import file with core positions, zenith, and azimuth
input_parameters = np.genfromtxt(options.inputfile, usecols=(3,4,5,6))
corex = input_parameters.T[0]
corey = input_parameters.T[1]
theta_list = input_parameters.T[2]
phi_list = input_parameters.T[3]

#run number, try opening file containing run numbers for that theta distribution, if no file exists, start from 000001
offset_file = '/user/rstanley/simulations/HTCondor/corsika/offset/run_number_fixed_offset_{0}_{1}_{2}_{3}_{4}_{5}.txt'.format(prim_part, det_location, det_season, det_time, theta_bin, theta_dist)
try:
    run_number_offset = np.genfromtxt(offset_file, delimiter='\t')
    print('Run number offset taken from file')
except:
    run_number_offset = np.zeros(1)
    print('Run number offset file not found')
    print('Run number offset set to 0 for all energies')

#generation of number of showers to run based on CR spectrum index and number of showers in first bin
numbers_to_generate = int(corex.shape[0])
new_offset = (numbers_to_generate + run_number_offset).astype(int)

#create dag file for output
get_date = date.today().strftime('%Y%m%d')
get_time = datetime.now().strftime("%H%M%S")
dag_file_path = '/user/rstanley/simulations/HTCondor/corsika/dagfiles/{0}/{1}/'.format(get_date, get_time)
os.makedirs(dag_file_path, exist_ok=True)
dag_file = '/user/rstanley/simulations/HTCondor/corsika/dagfiles/{0}/{1}/run_fixed_shower_{0}_{1}.dag'.format(get_date, get_time)
outfile=open(dag_file, 'w')

#generation of different jobs for dag file
job_counter = 0

shw_energy = energy_GeV

rand_seed_list = gp.random_seed(numbers_to_generate)
  
for j in range(numbers_to_generate):
    zenith_angle = theta_list[j]
    azimuth_angle = phi_list[j]
    rand_seed = rand_seed_list[j]
    run_number = "%06d" % (j + 1 + run_number_offset)

    outfile.write('JOB job_{0} /user/rstanley/simulations/HTCondor/corsika/run_corsika_shower.submit\n'.format(job_counter))
    outfile.write('VARS job_{0} '.format(job_counter))
    outfile.write('THETA_DIST="{0}" '.format(theta_dist))
    outfile.write('THETA_BIN="{0}" '.format(theta_bin))
    outfile.write('ENERGY_BIN="{0}" '.format(energy_bin))
    outfile.write('PRIM_PART="{0}" '.format(prim_part))
    outfile.write('RUN_NUMBER="{0}" '.format(run_number))
    outfile.write('RAND_SEED="{0}" '.format(rand_seed))
    outfile.write('SHW_ENERGY="{0}" '.format(shw_energy))
    outfile.write('PRIM_TYPE="{0}" '.format(prim_type))
    outfile.write('AZIMUTH_ANGLE="{0}" '.format(azimuth_angle))
    outfile.write('ZENITH_ANGLE="{0}" '.format(zenith_angle))
    outfile.write('DET_SEASON="{0}" '.format(det_season))
    outfile.write('DET_TIME="{0}" '.format(det_time))
    outfile.write('DET_LOCATION="{0}" '.format(det_location))
    outfile.write('LOG_NAME="{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}"\n'.format(theta_dist, energy_bin, theta_bin, prim_part, det_location, det_season, det_time, run_number))

    job_counter += 1


np.savetxt(offset_file, new_offset, delimiter='\t')



        
