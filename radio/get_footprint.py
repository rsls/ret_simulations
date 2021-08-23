import fluence
import process_data
import process_files
import pickle
import numpy as np
import scipy.interpolate as intp
from optparse import OptionParser
from matplotlib import pyplot as plt
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

parser.add_option("--filterlow", default = "30", help = "lower frequency of efield filter, usually (default) 30 Hz")
parser.add_option("--filterhigh", default = "200", help = "higher frequency of efield filter, usually (default) 200 Hz, 80 Hz also accepted")

(options, args) = parser.parse_args()

#initialtise variables for input options
run_number = int(options.runnumber) #CORSIKA run number, ( ie RET000040.txt is runnr=40)
theta_dist = str(options.distribution) #theta distribution to which the shower required belongs
theta_bin = int(options.zenithbin) #theta bin to which the shower required belongs
energy_bin = int(options.energybin) #energy bin to which the shower required belongs
prim_part = str(options.primary) #primary particle of shower
det_location = str(options.location) #detector location for which shower was simulated
det_season = str(options.season) #season for which the shower was simulated
det_time = str(options.time) #time of day for which the shower was simulated

filt_low = float(options.filterlow)
filt_high = float(options.filterhigh)

shower_number = str(run_number).zfill(6)

data_dir = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/'.format(theta_dist, det_location, prim_part, energy_bin, theta_bin, det_season, det_time)

#make output directory
out_file_path = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/radio/{7}_{8}'.format(theta_dist, det_location, prim_part, energy_bin, theta_bin, det_season, det_time, options.filterlow, options.filterhigh)
os.makedirs(out_file_path, exist_ok=True)

#set magnetic field inclination and alititude based on the detector location
if (det_location == 'td'):
    Binc = -83.5/180 * np.pi
    altitude = 2400

"""
Calculate antenna positions and efield for specified criteria and run number
xyz: antenna positions in ground plane (8 armed, wonky star when plotted on a square)
uvw: antenna positions in shower plane (8 armed, even star when plotted on a square)
efield: (160, 4082, 3), 160 antennas, 4082 points in time, north, west, and vertical components, in shower plane?
poldata: (160, 4082, 2), 160 antennas., 4082 points in time, horizontal? and vertical? polarisations
"""
ant_pos_xyz, ant_pos_uvw, time, efield_uvw, efield_xyz, poldata, zenith, azimuth_rot, energy, xmax = process_files.get_efield(data_dir, run_number, Binc, altitude)

"""
Efield filter
applies filter to CoREAS data which is for an infinite bandwidth
"""
efield_filt_uvw, time_filt = process_data.lofar_filter(efield_uvw, time, filt_low, filt_high, 1.0)
efield_filt_xyz, time_filt = process_data.lofar_filter(efield_xyz, time, filt_low, filt_high, 1.0)

"""
Fluence calculation
"""
fluence_uvw = fluence.calculate_energy_fluence_vector(efield_filt_uvw, time_filt, signal_window=100.0, remove_noise=True)
fluence_xyz = fluence.calculate_energy_fluence_vector(efield_filt_xyz, time_filt, signal_window=100.0, remove_noise=True)

"""
parameter conversion from radians to degrees
"""
theta = 180 * (zenith/np.pi)
phi = 180 * (azimuth_rot/np.pi)

"""
data_dict = {"energy":energy, "zenith":theta, "azimuth":phi, "xmax":xmax, "filter low":filt_low, "filter high":filt_high, "ant pos shw":ant_pos_uvw, "ant pos grd":ant_pos_xyz, "time":time, "efield shw":efield_uvw, "efield grd":efield_xyz, "poldata":poldata, "efield filt shw":efield_filt, "time filt":time_filt, "filt fluence":fluence}

out_file = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/radio/{7}_{8}/RAD{9}.pkl'.format(theta_dist, det_location, prim_part, energy_bin, theta_bin, det_season, det_time, options.filterlow, options.filterhigh, shower_number)

out_file_obj = open(out_file, 'wb')
pickle.dump(data_dict, out_file_obj)
out_file_obj.close()
"""

"""
Uncomment this block if you want to plot the graphs for a single shower as a sanity check and to check if you understand what calculations are being done above
"""

ant_pos_xyz_x, ant_pos_xyz_y = ant_pos_xyz.T[0], ant_pos_xyz.T[1]
ant_pos_uvw_x, ant_pos_uvw_y = ant_pos_uvw.T[0], ant_pos_uvw.T[1]

fluence_all = fluence_uvw.T[0] + fluence_uvw.T[1]
fluence_all_xyz = fluence_xyz.T[0] + fluence_xyz.T[1]

#print(theta, 'degrees,', phi, 'degrees,', np.log10(energy), 'GeV,', xmax, 'g/cm^2')
#print('efield', efield_uvw.shape)
#print('poldata', poldata.shape)
#print('efield filt', efield_filt.shape)
#print('time filt', time_filt.shape)
#print('fluence', fluence.shape)

plot_dir = '/user/rstanley/simulations/radio/162_0_46/'

lim = np.max(ant_pos_xyz_x) + 100
#Antenna positions
plt.scatter(ant_pos_xyz_x, ant_pos_xyz_y, label='xyz')
plt.scatter(ant_pos_uvw_x, ant_pos_uvw_y, label='uvw')
plt.legend()
plt.axis('square')
plt.xlim([-1*lim, lim])
plt.ylim([-1*lim, lim])
plt.title('Antenna positions')
plt.xlabel('x')
plt.ylabel('y')
plot_name = plot_dir + 'antenna_positions.png'
plt.savefig(plot_name)
plt.close()

#Electric field in antenna 40 in shower plane
plt.plot(time[40], efield_uvw[40].T[0], label='east?')
plt.plot(time[40], efield_uvw[40].T[1], label='north?')
plt.plot(time[40], efield_uvw[40].T[2], label='vertical?')
plt.legend()
plt.title('Electric field in antenna 40 in shower plane')
plt.xlabel('Time')
plt.ylabel('Electric field (V/m)')
plot_name = plot_dir + 'electric_field_uvw_40.png'
plt.savefig(plot_name)
plt.close()

#Electric field in antenna 40 in ground plane
plt.plot(time[40], efield_xyz[40].T[0], label='east?')
plt.plot(time[40], efield_xyz[40].T[1], label='north?')
plt.plot(time[40], efield_xyz[40].T[2], label='vertical?')
plt.legend()
plt.title('Electric field in antenna 40 in ground plane')
plt.xlabel('Time')
plt.ylabel('Electric field (V/m)')
plot_name = plot_dir + 'electric_field_xyz_40.png'
plt.savefig(plot_name)
plt.close()

#Polarisation data in antenna 40
plt.plot(time[40], poldata[40].T[0], label='horizontal?')
plt.plot(time[40], poldata[40].T[1], label='vertical?')
plt.legend()
plt.title('Polarisation data in antenna 40')
plt.xlabel('Time')
plt.ylabel('???')
plot_name = plot_dir + 'poldata_40.png'
plt.savefig(plot_name)
plt.close()

#Filtered electric field in antenna 40
plt.plot(time_filt[40], efield_filt_uvw[40].T[0], label='horizontal?')
plt.plot(time_filt[40], efield_filt_uvw[40].T[1], label='vertical?')
plt.legend()
plt.title('Filtered electric field in antenna 40 in shower plane')
plt.xlabel('Time')
plt.ylabel('Electric field (V/m)')
plot_name = plot_dir + 'filt_electric_field_uvw_40.png'
plt.savefig(plot_name)
plt.close()

#Interpolation for shower plane
rbf = intp.Rbf(ant_pos_uvw_x, ant_pos_uvw_y, fluence_all, smooth=0, function='quintic')
dist_scale = np.max(ant_pos_uvw_x)
ti = np.linspace(-dist_scale, dist_scale, 400)
XI, YI = np.meshgrid(ti, ti)
ZI = rbf(XI, YI)
maxp_uvw = np.max([fluence_all])
        
#Interpolation for ground plane
rbf2 = intp.Rbf(ant_pos_xyz_x, ant_pos_xyz_y, fluence_all_xyz, smooth=0, function='quintic')
dist_scale=np.max(ant_pos_xyz_x)
ti2 = np.linspace(-dist_scale, dist_scale, 400)
XI2, YI2 = np.meshgrid(ti2, ti2)
ZI2 = rbf2(XI2, YI2)
maxp_xyz = np.max([fluence_all_xyz])
    
  
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 7.5))
ax[0].pcolor(XI, YI, ZI,vmax=maxp_uvw, vmin=0, cmap='jet')
ax[0].set_aspect('equal')
ax[0].set_title('shower plane')
im = ax[1].pcolor(XI2, YI2, ZI2, vmax=maxp_xyz, vmin=0, cmap='jet')
ax[1].set_title('ground plane')
ax[1].set_aspect('equal')
cbar_ax = fig.add_axes([0.92, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)
plt.suptitle('Xmax = {0} g/cm^2, Zenith = {1} degree'.format(xmax, theta))
plot_name = plot_dir + 'interpolation.png'
plt.savefig(plot_name)
plt.close()

