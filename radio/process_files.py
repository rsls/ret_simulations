"""
Calculation of efield 
Taken and adapted from process_files.py from Katie/LOFAR
"""
import numpy as np
import sys
import pickle
import re
import os

"""
Translate from ground plane (xyz) to shower plane (uvw)
"""
def GetUVW(pos, cx, cy, cz, zen, az, Binc):
    relpos = pos-np.array([cx,cy,cz])

    B = np.array([0,np.cos(Binc),-np.sin(Binc)])
    v = np.array([-np.cos(az)*np.sin(zen),-np.sin(az)*np.sin(zen),-np.cos(zen)])

    vxB = np.array([v[1]*B[2]-v[2]*B[1],v[2]*B[0]-v[0]*B[2],v[0]*B[1]-v[1]*B[0]])
    vxB = vxB/np.linalg.norm(vxB)
    vxvxB = np.array([v[1]*vxB[2]-v[2]*vxB[1],v[2]*vxB[0]-v[0]*vxB[2],v[0]*vxB[1]-v[1]*vxB[0]])

    return np.array([np.inner(vxB,relpos),np.inner(vxvxB,relpos),np.inner(v,relpos)]).T

"""

"""
def get_efield(datadir, fileno, binc, altitude):
    dlength = 4082

    longfile = '{0}/DAT{1}.long'.format(datadir,str(fileno).zfill(6))
    steerfile = '{0}/steering/RUN{1}.inp'.format(datadir,str(fileno).zfill(6))
    listfile = open('{0}/steering/SIM{1}.list'.format(datadir,str(fileno).zfill(6)))

    lines = listfile.readlines()
    nTotalAnt=len(lines)

    antenna_positions=np.zeros([0,3])
    antenna_files=[]

    efield=np.zeros([nTotalAnt,dlength,3])
    polfield=np.zeros([nTotalAnt,dlength,2])
    XYZ_all=np.zeros([nTotalAnt,dlength,3])
    time=np.zeros([nTotalAnt,dlength])

    for l in np.arange(nTotalAnt):
        antenna_position_hold=np.asarray([float(lines[l].split(" ")[2]),float(lines[l].split(" ")[3]),float(lines[l].split(" ")[4])])#read antenna position...
        antenna_file_hold=(lines[l].split(" ")[5].split()[0])   #... and output filename from the antenna list file
        antenna_files.append(antenna_file_hold)
        antenna_positions=np.concatenate((antenna_positions,[antenna_position_hold]))


    nantennas=len(antenna_files)

    file=open(longfile,'r')
    param_list=(re.findall("PARAMETERS.*",file.read()))[0]
    xmax=(float(param_list.split()[4]))
    file.close()

    file=open(steerfile,'r')
    az_list=re.findall("PHI.*",file.read())[0]
    azimuth=np.mod(float(az_list.split()[1]),360.0)*np.pi/180. #rad; CORSIKA coordinates
    az_rot=3*np.pi/2+azimuth #LOFAR coordinates?
     
    file.seek(0)
    zenith_list=(re.findall("THETAP.*",file.read()))[0]
    zenith=float(zenith_list.split()[1])*np.pi/180. #rad; CORSIKA coordinates

    file.seek(0)
    energy_list=(re.findall("ERANGE.*",file.read()))[0]
    energy=float(energy_list.split()[1]) #GeV
    file.close()
     
    for j in np.arange(nantennas):

        antenna_file = lines[j].split(" ")[5]
        coreasfile = '{0}/SIM{1}_coreas/raw_{2}.dat'.format(datadir,str(fileno).zfill(6),antenna_files[j])

        data=np.genfromtxt(coreasfile)
        data[:,1:]*=2.99792458e4 #convert Ex, Ey and Ez (not time!) to Volt/meter
        dlength=data.shape[0]
        poldata=np.ndarray([dlength,2])

        XYZ=np.zeros([dlength,3])
        XYZ[:,0]=-data[:,2] #conversion from CORSIKA coordinates to 0=east, pi/2=north
        XYZ[:,1]=data[:,1]
        XYZ[:,2]=data[:,3]

        XYZ[:,0]=np.roll(XYZ[:,0], 800)
        XYZ[:,1]=np.roll(XYZ[:,1], 800)
        XYZ[:,2]=np.roll(XYZ[:,2], 800)

        UVW=GetUVW(XYZ, 0, 0, 0, zenith, az_rot, binc)
        poldata[:,0] = -1.0/np.sin(zenith)*XYZ[:,2] #-1/sin(theta) *z
        poldata[:,1] = -1*np.sin(az_rot)*XYZ[:,0] + np.cos(az_rot)*XYZ[:,1] #-sin(phi) *x + cos(phi)*y in coREAS 0=positive y, 1=negative x

        polfield[j]=poldata
        efield[j]=UVW #data[:,1:]#UVW#
        time[j]=data.T[0]
        XYZ_all[j]=XYZ
        temp=np.copy(antenna_positions)

    antenna_positions[:,0], antenna_positions[:,1], antenna_positions[:,2] = -1*(temp[:,1])/100.,(temp[:,0])/100., temp[:,2]/100.
    ant_pos_uvw=GetUVW(antenna_positions, 0, 0, altitude, zenith, az_rot, binc)

    return antenna_positions, ant_pos_uvw, time, efield, XYZ_all, polfield, zenith, az_rot, energy, xmax
