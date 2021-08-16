"""
Functions used by the dag file generation code to randomly generate theta angles in a distribution flat in theta or costheta
Function to generate phi angles in a uniform random distribution
Function for generating the random seeds for the CORSIKA monte carlo engine
Function for finding the bin numbers for an array of theta angles
"""
import numpy as np
import random

"""
flat_theta: generates an array of N theta angles where theta is flat in theta
Theta runs from 0 (zenith) to 65 degrees
Theta bins: 0 - 0 <= theta < 30 degrees
            1 - 30 <= theta < 45 degrees
            2 - 45 <= theta < 55 degrees
            3 - 55 <= theta < 65 degrees
Give max_degree in degrees and integer N
"""
def flat_theta(N, max_degree, min_degree):
    theta = np.zeros((N))
    max_radian = np.pi * (max_degree/180)
    min_radian = np.pi * (min_degree/180)
    gap_radian = max_radian - min_radian
    for i in range(N):
        rand1 = random.uniform(0,1)
        theta_rad = gap_radian*rand1 + min_radian
        theta[i] = 180 * (theta_rad/np.pi)
    return theta

"""
flat_costheta: generates an array of N theta angles where theta is flat in cos(theta)
Theta runs from 0 (zenith) to max_angle degrees
Theta bins: 0 - 0 <= theta < 30 degrees
            1 - 30 <= theta < 45 degrees
            2 - 45 <= theta < 55 degrees
            3 - 55 <= theta < 65 degrees
Give max_degree in degrees and integer N
"""
def flat_costheta(N, max_degree, min_degree):
    theta = np.zeros((N))
    max_radian = np.pi * (max_degree/180)
    max_random = np.cos(max_radian)
    min_radian = np.pi * (min_degree/180)
    min_random = np.cos(min_radian)
    for j in range(N):
        rand2 = random.uniform(max_random,min_random)
        theta_rad = np.arccos(rand2)
        theta[j] = 180 * (theta_rad/np.pi)
    return theta

"""
random_phi: generates an array of N phi angles where phi is in a uniform random distribution
Give max_degree in degrees and integer N
"""
def random_phi(N, max_degree):
    phi = np.zeros((N))
    max_radian = np.pi * (max_degree/180)
    for k in range(N):
        rand3 = random.uniform(0,1)
        phi_rad = max_radian*rand3
        phi[k] = 180 * (phi_rad/np.pi)
    return phi

"""
random_seed: generates an array of N random seeds 
Give integer N
"""
def random_seed(N):
    seed = np.zeros((N))
    for l in range(N):
        a = random.uniform(1, 100) 
        b = random.uniform(1, 100)
        c = random.uniform(1000, 9500)
        seed[l] = ((a**2) * b) + c
    return seed.astype(int)

"""
bin_theta: for an array of theta values, finds the corresponding bin number
Theta bins: 0 - 0 <= theta < 30 degrees
            1 - 30 <= theta < 45 degrees
            2 - 45 <= theta < 55 degrees
            3 - 55 <= theta < 65 degrees
"""
def bin_theta(theta_array):
    N = theta_array.shape[0]
    bins = np.zeros((N))
    for m in range(N):
        if (theta_array[m] >= 0) and (theta_array[m] < 30):
            bins[m] = 0
        elif (theta_array[m] >= 30) and (theta_array[m] < 45):
            bins[m] = 1
        elif (theta_array[m] >= 45) and (theta_array[m] < 55):
            bins[m] = 2
        elif (theta_array[m] >= 55) and (theta_array[m] < 65):
            bins[m] = 3
    return bins.astype(int)
"""
cr_spectrum: from an array of energies, an index and a number of showers in the first bin, calculate the number of showers in each bin in array given
If calculated value of shower number for a particular bin is 0, it is replaced with a 1
"""
def cr_spectrum(energy_array, gamma, N):
    a = N * (energy_array[0]**(-1*gamma))
    spectrum = (a * (energy_array**(gamma))).astype(int)
    spectrum[spectrum == 0] = 1
    return spectrum
