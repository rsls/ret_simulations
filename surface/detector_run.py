"""
Run code to 'fill' scintillators with energy deposits from binned GEANT files
Includes options
Output is a deposit_{}.dat with detector positions, deposits and core position
Needs to be run once for each geant file to be used 
"""
import detector_fill as det
import numpy as np
from numpy import random
from optparse import OptionParser
import os

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-r", "--runnumber", default = "0", help = "run number")
parser.add_option("-d", "--distribution", default = "theta", help = "theta angle distribution, flat in theta=theta, flat in cos(theta)=costheta")
parser.add_option("-z", "--zenithbin", default = "0", help = "zenith bin number of shower, 0-3 ")
parser.add_option("-e", "--energybin", default = "1e8", help = "energy bin number for primary particle energy, 150-190")
parser.add_option("-p", "--primary", default = "proton", help = "primary particle type, proton or iron")
parser.add_option("-s", "--season", default = "g", help = "season for atmosphere profile, s=summer, w=winter, g=general")
parser.add_option("-t", "--time", default = "g", help = "time for atmospheric profile, d=day, n=night, g=general")
parser.add_option("-l", "--location", default = "td", help = "location of detector, td=Taylor Dome")

parser.add_option("--arraynumber", default = "0", help = "number of array layout")
parser.add_option("--radius", default = "0", help = "maximum radius of shower core")
parser.add_option("--trynumber", default = "0", help = "number of core positions to chose")

(options, args) = parser.parse_args()

#initialise variables for input options
array_number = int(options.arraynumber)
max_radius = int(options.radius) #pick a core position within this radius
try_number = int(options.trynumber) #how many core positions to chose, each one will make a different file

run_number = "%06d" % int(options.runnumber) #CORSIKA run number, ( ie RET000040.txt is runnr=40)
theta_dist = str(options.distribution) #theta distribution to which the shower required belongs
theta_bin = int(options.zenithbin) #theta bin to which the shower required belongs
energy_bin = int(options.energybin) #energy bin to which the shower required belongs
prim_part = str(options.primary) #primary particle of shower
det_location = str(options.location) #detector location for which shower was simulated
det_season = str(options.season) #season for which the shower was simulated
det_time = str(options.time) #time of day for which the shower was simulated

#set up file paths for array layout and geant file to be use. 
arrayfile = '/user/rstanley/detector/layout/layout_{0}.txt'.format(array_number) #**
geantfile = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/geant/RET{7}.txt'.format(theta_dist, det_location, prim_part, energy_bin, theta_bin, det_season, det_time, run_number)

coreX = np.zeros(try_number)
coreY = np.zeros(try_number)

#make directory for storing energy deposits for different layouts
#deposit_dir_upper = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/deposit/'.format(theta_dist, det_location, prim_part, energy_bin, theta_bin, det_season, det_time)
#os.makedirs(deposit_dir_upper, exist_ok = True) 
#deposit_dir = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/deposit/deposit_{7}/'.format(theta_dist, det_location, prim_part, energy_bin, theta_bin, det_season, det_time, array_number)
#os.makedirs(deposit_dir, exist_ok = True) 

#find energy deposits in scintillators for each core position for the shower 
for i in np.arange(try_number):
    #choose radius and azimuth angle for core in shower plane
    coreR=max_radius*max_radius*(np.random.choice(100000)/100000.0);
    coreA=np.random.choice(360)*1.0;
    
    #convert r, azimuth to X,Y
    coreX[i]=np.sqrt(coreR)*np.cos(coreA*np.pi/180);
    coreY[i]=np.sqrt(coreR)*np.sin(coreA*np.pi/180);
    
    #return shower information, deposits, and antenna positions in shower plane
    info, deposit, pos, DetX, DetY = det.fill(geantfile, coreX[i], coreY[i], arrayfile)
                         
    #save info in file
    deposit_file = 'deposit{0}_{1}.dat'.format(options.runnumber, i) #deposit_dir +
    outfile=open(deposit_file, 'w')          
    outfile.write('{0}   {1}   {2}   {3}   {4}   {5}\n'.format(info['type'], info['energy'], info['zenith'], info['phi'], coreX[i], coreY[i]))

    #write out energy deposit and for each scintillator 
    for j in np.arange(len(deposit['total'])):
                 outfile.write('{0}   {1}   {2}   {3}   {4}   {5}   {6}\n'.format(DetX[j], DetY[j], deposit['total'][j], deposit['gamma'][j], deposit['electron'][j], deposit['muon'][j], deposit['hadron'][j], ))
    outfile.close()

