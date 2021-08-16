"""
Write CoREAS antenna .list file for any run
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

(options, args) = parser.parse_args()

"""
Convert degrees to radians
"""
azimuth=float(options.azimuth)
az = np.pi * (azimuth / 180.)   
zenith=float(options.zenith)
zen = np.pi * (zenith / 180.)

if options.location=="td":
    Binc = -83.5/180 * np.pi
    altitude = 2400E+02

"""
Want an 8 armed star in the vxB-vxvxB plane
"""
B = np.array([0,np.cos(Binc),-np.sin(Binc)])
v = np.array([-np.cos(az)*np.sin(zen),-np.sin(az)*np.sin(zen),-np.cos(zen)])
vxB = np.array([v[1]*B[2]-v[2]*B[1],v[2]*B[0]-v[0]*B[2],v[0]*B[1]-v[1]*B[0]])
vxB = vxB/np.linalg.norm(vxB)
vxvxB = np.array([v[1]*vxB[2]-v[2]*vxB[1],v[2]*vxB[0]-v[0]*vxB[2],v[0]*vxB[1]-v[1]*vxB[0]])


for i in np.arange(1,21):
   for j in np.arange(8):
      xyz = i*25*(np.cos(j/4.0*np.pi)*vxB+np.sin(j/4.0*np.pi)*vxvxB)
      c = xyz[2]/v[2]
      name="pos_{0}_{1}".format(i*25,j*45)
      print('AntennaPosition = {0} {1} {2} {3}'.format(100*(xyz[1]-c*v[1]), -100*(xyz[0]-c*v[0]), altitude, name))
