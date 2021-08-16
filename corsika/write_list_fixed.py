"""
Write CoREAS antenna .list file for any run with fixed antenna and core positions
Includes options for azimuth, zenith, and location 
Out put directed towards a file SIM$showernumber.list where $shower number is 6 digits with 0s preceding unique shower indetifier number
"""
from optparse import OptionParser
import numpy as np
import os

"""
Commandline options
"""
parser = OptionParser()

parser.add_option("-a", "--azimuth", default = "0", help = "azimuth angle (degrees)")
parser.add_option("-z", "--zenith", default = "0", help = "zenith angle (degrees) ")
parser.add_option("--location", default="td", help="Location for simulation, td=Taylor Dome")
parser.add_option("--corex", default="0", help="Core position on x axis in RET coordinates")
parser.add_option("--corey", default="0", help="Core position on y axis in RET coordinates")

(options, args) = parser.parse_args()

"""
Detector altitude
"""
if options.location=="td":
    altitude = 2400E+02

"""
Want an 6 antennas of RET in ground plane
"""
print('AntennaPosition = {0} {1} {2} {3}'.format(200, 0, altitude, 'RET_ant_1'))
print('AntennaPosition = {0} {1} {2} {3}'.format(90, 30, altitude, 'RET_ant_2'))
print('AntennaPosition = {0} {1} {2} {3}'.format(90, -30, altitude, 'RET_ant_3'))
print('AntennaPosition = {0} {1} {2} {3}'.format(-90, 30, altitude, 'RET_ant_4'))
print('AntennaPosition = {0} {1} {2} {3}'.format(-90, -30, altitude, 'RET_ant_5'))
print('AntennaPosition = {0} {1} {2} {3}'.format(-200, 0, altitude, 'RET_ant_6'))
