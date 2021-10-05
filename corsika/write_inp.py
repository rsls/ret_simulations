"""
Write CORSIKA input file for any run
Includes options for run number, seed, energy, primary particle type, azimuth, zenith, output directory, season, time of day, and location 
Output directed towards a file RUN$showernumber.inp where $shower number is 6 digits with 0s preceding unique shower indetifier number
"""
from optparse import OptionParser
import os

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-r", "--runnumber", default = "0", help = "run number")
parser.add_option("-s", "--seed", default = "1", help = "seed for corsika random number generator")
parser.add_option("-u", "--energy", default = "1e8", help = "cosmic ray primary energy (GeV)")
parser.add_option("-t", "--type", default = "14", help = "primary particle type ")
parser.add_option("-a", "--azimuth", default = "0", help = "azimuth angle (degrees)")
parser.add_option("-z", "--zenith", default = "0", help = "zenith angle (degrees) ")
parser.add_option("-d", "--dir", default = "/user/rstanley/CORSIKA/QGSJET/", help = "output directory") #**
parser.add_option("--season", default="s", help="Season for simulation, s=summer, w=winter, g=general/unspecified")
parser.add_option("--time", default="d", help="Time of day for simulation, d=day, n=night, g=general/unspecified")
parser.add_option("--location", default="td", help="Location for simulation, td=Taylor Dome")

(options, args) = parser.parse_args()

print("RUNNR " + str( int(options.runnumber)))
print("EVTNR   1")
print("NSHOW   1")
print("SEED " + str(int(options.seed)+(10*1)) + " 0 0")
print("SEED " + str(int(options.seed)+(10*2)) + " 0 0")
print("SEED " + str(int(options.seed)+(10*3)) + " 0 0")
print("PRMPAR " + str(options.type))
print("ERANGE " + str(float(options.energy)) + " " + str(float(options.energy))) 
print("THETAP " + str(float(options.zenith)) + " " + str(float(options.zenith)))
print("PHIP " + str( -270+float(options.azimuth)) + " " + str( -270+float(options.azimuth)))
print("THIN    1.000E-06 " + str(1e-6*float(options.energy)) + " 0.000E+00")
print("THINH   1.000E+02 1.000E+02")
print("DIRECT " + options.dir)
print("STEPFC  1.0")
print("ECUTS   3.000E-01 3.000E-01 5.0E-04 5.0E-04")
print("ELMFLG  T   T")
print("ECTMAP  1.0E+5")
print("MUADDI  T")
print("MUMULT  T")
print("MAXPRT  1")
print("PAROUT  T  F")
print("LONGI   T  5.0E+00  T  T")
print("RADNKG  5.0E+05")
print("DATBAS  F")

if options.location=="td":
    print("OBSLEV 2400.0E+02")
    print("MAGNET 5.2595 -58.1915")

    if options.season=="s":
        if options.time=="d":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2014_10_10_14.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2014_10_10_14.DAT")

        elif options.time=="n":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2014_10_10_20.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2014_10_10_20.DAT")

        elif options.time=="g":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2014_10_10_20.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2014_10_10_20.DAT")

    elif options.season=="w":
        if options.time=="d":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2010_9_9_14.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2010_9_9_14.DAT")

        elif options.time=="n":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2010_8_17_20.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2010_8_17_20.DAT")

        elif options.time=="g":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2010_8_17_20.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2010_8_17_20.DAT")

    elif options.season=="g":
        if options.time=="d":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2010_9_9_14.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2010_9_9_14.DAT")

        elif options.time=="n":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2010_8_17_20.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2014_8_17_20.DAT")

        elif options.time=="g":
            #print("ATMFILE /user/rstanley/CORSIKA/GDAS/atmfiles/ATM_2010_8_17_20.DAT")
            print("ATMFILE /pnfs/iihe/radar/gdas/td/atmfiles/ATM_2010_8_17_20.DAT")

#print("OBSLEV 2835.0E+02")
#print("OBSLEV 0.0E+01")
print("USER    rstanley")
print("EXIT")
