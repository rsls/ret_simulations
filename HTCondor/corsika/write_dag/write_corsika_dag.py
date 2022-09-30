"""
Write dag file for multiple corsika job submission on T2B HTCondor
Writes out job name, variable names and values, and log name for each job allocated
Input options include number of 10^15.0 eV showers desired (used to calculate number of showers at other energies), index of cosmic ray spectrum (usually -1), and 
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

parser.add_option("-n", "--number", default = "0", help = "number of 10^15.0 eV showers to generate")
parser.add_option("-g", "--gamma", default = "-1", help = "index of cosmic ray spectrum")
parser.add_option("-d", "--distribution", default = "theta", help = "theta angle distribution, flat in theta=theta, flat in cos(theta)=costheta")
parser.add_option("-b", "--thetabin", default = "0", help = "bin for theta angle, sets the minimum and maximum theta angle. 0: 0 <= t < 30 degrees,1: 30 <= t < 45 degrees, 2: 45 <= t < 55 degrees, 3: 55 <= t < 65 degrees")
parser.add_option("-p", "--primary", default = "proton", help = "primary particle type, proton or iron")
parser.add_option("-s", "--season", default = "g", help = "season for atmosphere profile, s=summer, w=winter, g=general")
parser.add_option("-t", "--time", default = "g", help = "time for atmospheric profile, d=day, n=night, g=general")
parser.add_option("-l", "--location", default = "td", help = "location of detector, td=Taylor Dome")

(options, args) = parser.parse_args()

"""
Convert parsed options to the format and type needed in code and error parsing
"""
shower_number = int(options.number)
#cosmic ray index, error handling for positive indices
cr_index = int(options.gamma)
if (cr_index > 0):
    print('Your CR spectrum index is', cr_index, 'and therefore positive')
    answer = input('Do you want to continue? (y/n): ') 
    if (answer == 'y'):
        pass
    elif (answer == 'n'):
        exit()
#theta distribution, error handling for invalid distribution
theta_dist = str(options.distribution)
if (theta_dist != 'costheta') and (theta_dist != 'theta'):
    print(theta_dist, 'is not a currently supported theta distribution, please use --help for more information')
    exit()
#theta bin, error handling for invalid bin number
theta_bin = int(options.thetabin)
if (theta_bin == 0):
    min_theta = 0
    max_theta = 30
elif (theta_bin == 1):
    min_theta = 30
    max_theta = 45
elif (theta_bin == 2):
    min_theta = 45
    max_theta = 55
elif (theta_bin == 3):
    min_theta = 55
    max_theta = 65
else:
    print(theta_bin, 'is not a currently supported theta bin, please use --help for more information')
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

#log of energy bins available and variants for organisation and use in CORSIKA
log_energy = np.array([15.0, 15.2, 15.4, 15.6, 15.8, 16.0, 16.2, 16.4, 16.6, 16.8, 17.0, 17.2, 17.4, 17.6, 17.8, 18.0, 18.2, 18.4, 18.6, 18.8, 19.0])
energy = 10**log_energy
energy_GeV = 10**log_energy / 10**9
bin_names = (10*log_energy).astype(int)

#run number, try opening file containing run numbers for that theta distribution, if no file exists, start from 000001
offset_file = '/user/rstanley/simulations/HTCondor/corsika/offset/run_number_offset_{0}_{1}_{2}_{3}_{4}_{5}.txt'.format(prim_part, det_location, det_season, det_time, theta_bin, theta_dist)
try:
    run_number_offset = np.genfromtxt(offset_file, delimiter='\t')
    print('Run number offset taken from file')
except:
    run_number_offset = np.zeros([log_energy.shape[0]])
    print('Run number offset file not found')
    print('Run number offset set to 0 for all energies')

#generation of number of showers to run based on CR spectrum index and number of showers in first bin
numbers_to_generate = gp.cr_spectrum(energy, cr_index, shower_number)
new_offset = (numbers_to_generate + run_number_offset).astype(int)

#create dag file for output
get_date = date.today().strftime('%Y%m%d')
get_time = datetime.now().strftime("%H%M%S")
dag_file_path = '/user/rstanley/simulations/HTCondor/corsika/dagfiles/{0}/{1}/'.format(get_date, get_time)
os.makedirs(dag_file_path, exist_ok=True)
dag_file = '/user/rstanley/simulations/HTCondor/corsika/dagfiles/{0}/{1}/run_corsika_shower_{0}_{1}.dag'.format(get_date, get_time)
outfile=open(dag_file, 'w')

#generation of different jobs for dag file
job_counter = 0
for i in range(numbers_to_generate.shape[0]):
    energy_bin = bin_names[i]
    shw_energy = energy_GeV[i]

    rand_seed_list = gp.random_seed(numbers_to_generate[i])
    phi_list = gp.random_phi(numbers_to_generate[i], max_phi)

    if (theta_dist == 'costheta'):
        theta_list = gp.flat_costheta(numbers_to_generate[i], max_theta, min_theta)
    elif (theta_dist == 'theta'):
        theta_list = gp.flat_theta(numbers_to_generate[i], max_theta, min_theta)
  
    for j in range(numbers_to_generate[i]):
        zenith_angle = theta_list[j]
        azimuth_angle = phi_list[j]
        rand_seed = rand_seed_list[j]
        run_number = "%06d" % (j + 1 + run_number_offset[i])

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

outfile.close()
np.savetxt(offset_file, new_offset, delimiter='\t')



        
