"""
'Fill' scintillators with specified positions and areas with energy deposits from binned GEANT file
Imported into detector_run
"""
import os
import numpy as np
import re

detectorpath='./array_layouts/'
area=0.9  #m^2

"""
read_det_file: reads detector file, taking coordinates of scintillators in the ground plane
"""
def read_det_file(name):
    file=open(name,'r')
    positions=np.genfromtxt(file,skip_header=1)#,usecols=(0,1))
    file.close()
    return positions

"""
theta_phi:converts detector positions to the shower plane
Transform x0, y0 and z0 to shower plane
Converts corsika phi to lofar phi system
"""
def theta_phi(theta, phi, x0, y0, z0): 
    psi = 2*np.pi - phi
    x1 = x0*np.cos(phi) + y0*np.sin(phi)
    y1 = -1*x0*np.sin(phi) + y0*np.cos(phi)
    z1 = z0
    
    x2 = x1*np.cos(theta) - z1*np.sin(theta)
    y2 = y1
    z2 = x1*np.sin(theta) + z1*np.cos(theta)
    
    x = x2*np.cos(psi) + y2*np.sin(psi)
    y = -1*x2*np.sin(psi) + y2*np.cos(psi)
    z = z2
    
    return x,y,z

"""
fill: fill the detector with energy deposits from CORSIKA shower
"""
def fill(file, xcore, ycore, array): 
    geantfile = open(file)
    info = geantfile.readline().split()
    type = int(info[0])            #type, 14=proton, 56=iron
    energy = float(info[1])*1e9    #energy in eV
    zenith = float(info[2]) #zenith angle in radians
    phi = float(info[3]) #azimuth angle in radians

    #make a dictonary with info
    shower_info = {'type':type, 'energy':energy, 'zenith':zenith, 'phi':phi}
    #read detector positions
    detectors = read_det_file(array)
    #effective area of scintillator
    Aeff = area*np.cos(zenith)  
    #number of scintillator plates in the array
    nDet = detectors.shape[0]
    
    #project detector positions into shower plane
    xdet, ydet, zdet = theta_phi(zenith,phi,detectors.T[0]-xcore,detectors.T[1]-ycore,detectors.T[2])

    #find radius of detectors from shower core and find bin associated with geant file binning
    #data is energy deposit binned radially, 5m bins
    rad = np.sqrt(xdet*xdet+ydet*ydet)
    radBin = (rad/5.0).astype(int)
    #read rest of geant file
    data = np.genfromtxt(file,skip_header=1)  
    
    dep = np.zeros([nDet])  #energy deposited in each detector
    depg = np.zeros([nDet]) #gamma energy deposited in each detector
    depe = np.zeros([nDet]) #electron energy deposited in each detector
    depm = np.zeros([nDet]) #muon energy deposited in each detector
    deph = np.zeros([nDet]) #hadron energy deposited in each detector
    Xx = np.zeros([nDet]) #X position of each detector
    Yy = np.zeros([nDet]) #Y position of each detector

    lenData=data.shape[0]
    
    
    # fill detectors, checking that you are still within the range of binned geant data
    for j in np.arange(nDet):
        if radBin[j]>=lenData:
            dep[j]=0.0
        else:
            dep[j] = Aeff*data.T[1][radBin[j]]  #select EM deposit from poisson distribution
            depg[j] = dep[j]*(data.T[2][j]/100) #other columns give percentage of energy deposition in gama, electron, muon and hadron components
            depe[j] = dep[j]*(data.T[3][j]/100) #these lines find the energy deposit for all of these components
            depm[j] = dep[j]*(data.T[4][j]/100)
            deph[j] = dep[j]*(data.T[5][j]/100)
            Xx[j] = detectors.T[0][j] #detector x position in area
            Yy[j] = detectors.T[1][j] #detector y position in area

    #make dictionary of energy deposits
    energy_deposit = {'total':dep, 'gamma':depg, 'electron':depe, 'muon':depm, 'hadron':deph}

    # return shower information, deposits,and detector positions in shower plane
    return shower_info, energy_deposit, np.asarray([xdet,ydet,zdet]).T, Xx, Yy
