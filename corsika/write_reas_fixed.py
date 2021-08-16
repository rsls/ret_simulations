"""
Write CoREAS .reas file for any run with fixed core and antenna positions
Includes options for energy, azimuth, zenith, season, time of day, and location 
Season, time of day, and location determine the refractive index at sea level
Out put directed towards a file SIM$showernumber.reas where $shower number is 6 digits with 0s preceding unique shower indetifier number
"""
from optparse import OptionParser
import numpy as np
import os

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-u", "--energy", default = "1e8", help = "cosmic ray primary energy (GeV)")
parser.add_option("-a", "--azimuth", default = "0", help = "azimuth angle (degrees)")
parser.add_option("-z", "--zenith", default = "0", help = "zenith angle (degrees) ")
parser.add_option("--season", default="s", help="Season for simulation, s=summer, w=winter, g=general/unspecified")
parser.add_option("--time", default="d", help="Time of day for simulation, d=day, n=night, g=general/unspecified")
parser.add_option("--location", default="td", help="Location for simulation, td=Taylor Dome")
parser.add_option("--corex", default="0", help="Core position on x axis in RET coordinates")
parser.add_option("--corey", default="0", help="Core position on y axis in RET coordinates")

(options, args) = parser.parse_args()

print("# CoREAS V1 parameter file")
print("# parameters setting up the spatial observer configuration:")
print("CoreCoordinateNorth  =  " + options.corey + "  ; in cm")
print("CoreCoordinateWest  =  -" + options.corex + "  ; in cm")

if options.location=="td":
    print("CoreCoordinateVertical  =  +2400.0E+02  ; in cm")

print("# parameters setting up the temporal observer configuration:    =               ;")
print("AutomaticTimeBoundaries  =  4.0E-07  ; 0: off, x: automatic boundaries with width x in s")
print("TimeLowerBoundary  =  -1  ; in s, only if AutomaticTimeBoundaries set to 0")
print("TimeUpperBoundary  =  +1  ; in s, only if AutomaticTimeBoundaries set to 0")
print("TimeResolution  =  1.0E-10  ; in s")
print("ResolutionReductionScale  =  0  ; 0: off, x: decrease time resolution linearly every x cm in radius")

if options.location=="td":
    if options.season=="s":
        if options.time=="d":
            print("GroundLevelRefractiveIndex  = 1.0003033087651108  ; specify refractive index at 0 m asl")

        elif options.time=="n":
            print("GroundLevelRefractiveIndex  = 1.000304063662562  ; specify refractive index at 0 m asl")

        elif options.time=="g":
            print("GroundLevelRefractiveIndex  = 1.000303686401219  ; specify refractive index at 0 m asl")

    elif options.season=="w":
        if options.time=="d":
            print("GroundLevelRefractiveIndex  = 1.000320568490007  ; specify refractive index at 0 m asl")

        elif options.time=="n":
            print("GroundLevelRefractiveIndex  = 1.0003206441341195  ; specify refractive index at 0 m asl")

        elif options.time=="g":
            print("GroundLevelRefractiveIndex  = 1.0003206063518753  ; specify refractive index at 0 m asl")

    elif options.season=="g":
        if options.time=="d":
            print("GroundLevelRefractiveIndex  = 1.0003134193514573  ; specify refractive index at 0 m asl")

        elif options.time=="n":
            print("GroundLevelRefractiveIndex  = 1.0003137808223976  ; specify refractive index at 0 m asl")

        elif options.time=="g":
            print("GroundLevelRefractiveIndex  = 1.0003136002355402  ; specify refractive index at 0 m asl")

print("# parameters read from CORSIKA files, these are not interpreted by CoREAS but stated here for your convenience")
print("PrimaryParticleEnergy  = " + str(float(options.energy)) +  "  ; in eV")
print("ShowerZenithAngle  = " + str( float(options.zenith)) +  "  ; in degrees")
print("ShowerAzimuthAngle  = " + str(float(options.azimuth)) + "  ; in degrees, 0: shower propagates to north, 90: to west")
