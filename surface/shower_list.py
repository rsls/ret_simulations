"""
Make list of all showers and whether they trigger with a particular array layout
"""
import numpy as np

def get_shower_list(theta_dist, prim_part, det_location, det_season, det_time, array_number, shower_number, trys_number, station_number, threshold):

    energy_bin_list = [150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190]
    zenith_bin_list = [0, 1, 2, 3]
    
    energy_list = np.empty()
    zenith_list = np.empty()
    azimuth_list = np.empty()
    corex_list = np.empty()
    corey_list = np.empty()
    trigger_list = np.empty()
    trigger_number_list = np.empty()

    for i in range(len(energy_bin_list)):
        energy_bin = energy_bin_list[i]
    
        for j in range(len(zenith_bin_list)):
            zenith_bin = zenith_bin_list[j]

            for k in range(shower_number):
                run_number = k + 1
                
                for l in range(trys_number):
                    try_number = l

                    depositfile = '/pnfs/iihe/radar/corsika/qgsjet/{0}/{1}/{2}/{3}/{4}/{5}/{6}/deposit/deposit_{7}/deposit{8}_{9}.dat'.format(theta_dist, det_location, prim_part, energy_bin, theta_bin, det_season, det_time, array_number, run_number, try_number)
                
                    if os.path.isfile(depositfile):
                        deposit_file = open(depositfile)
                        header = deposit_file.readline().split()
                        #take header information and add to list for dictionary
                        energy, zenith, azimuth, corex, corey = float(header[1]), float(header[2]), float(header[3]), float(header[4]), float(header[5])
                        #convert rest of file into deposits and check if they trigger detector above threshold
                        energy_deposit = np.genfromtxt(depositfile,skip_header=1)

                        scint_deposits = energy_deposit.T[2]
                        stations_split = np.split(scint_deposits, station_number)

                        triggered_stations = np.zeros([station_number])
                    
                        for m in range(triggered_stations.shape[0]):
                            station = stations_split[m]
                            station_trigger = len(station[station >= threshold])
                            if station_trigger == 2:
                                triggered_stations[m] = 1

                        triggered_stations_number = len(triggered_stations[triggered_stations == 1])

                        detector_halves = np.split(triggered_stations, 2)
                        number_in_half = station_number / 2

                        if (np.sum(detector_halves) >= number_in_half):
                            trigger = 1

                        else:
                            trigger = 0

                        energy_list = np.concatenate((energy_list, [energy]))
                        zenith_list = np.concatenate((zenith_list, [zenith]))
                        azimuth_list = np.concatenate((azimuth_list, [azimuth]))
                        corex_list = np.concatenate((corex_list, [corex]))
                        corey_list = np.concatenate((corey_list, [corey]))
                        trigger_list = np.concatenate((trigger_list, [trigger]))
                        trigger_number_list = np.concatenate((trigger_number_list, [triggered_stations_number]))
    
    shower_dict = dictionary = {'energy':energy_list, 'zenith':zenith_list, 'azimuth':azimuth_list, 'corex':corex_list, 'corey':corey_list, 'trigger':trigger_list, 'trigger number':trigger_number_list}
return shower_dict
