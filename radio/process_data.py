import numpy as np
import os
import pickle
#import matplotlib.pyplot as plt
import sys
import glob
import process_files
import re
#import matplotlib as mpl
#import matplotlib.cm as cm
from scipy.optimize import curve_fit
from scipy import signal

"""

"""
def lofar_filter(efield,times,lowco,hico,res):  # resolution in ns
    tstep = times[0][1]-times[0][0]
    dlength=len(times[0])
    new_length= 2*(int(np.floor(tstep/(res*1e-9) * dlength/2.)+1)-1)

    nantennas=len(times)
    onskypower=np.zeros([nantennas,2])
    #antenna_position=np.zeros([nantennas,3])
    filteredpower=np.zeros([nantennas,2])
    peak_time=np.zeros([nantennas,2])
    peak_bin=np.zeros([nantennas,2])
    peak_amplitude=np.zeros([nantennas,2])

    #return_signal=np.zeros([nantennas,new_length,2])
    return_signal=np.zeros([nantennas,dlength,2])

    times_up=np.arange(0,dlength*res,res)
    times_return=np.zeros([nantennas,dlength])
    for j in np.arange(nantennas):
    #for j in np.arange(1):

        time=times[j]
        poldata=np.ndarray([dlength,2])

        poldata[:,0] = efield[j].T[0]
        poldata[:,1] = efield[j].T[1]
        spec=np.fft.rfft(poldata, axis=-2)
        #print spec.shape
        # Apply antenna model
        tstep = time[1]-time[0]
        #onskypower[j]=np.array([np.sum(poldata[:,0]*poldata[:,0]),np.sum(poldata[:,1]*poldata[:,1])])*tstep


        freqhi = 0.5/tstep/1e6 # MHz
        freqstep = freqhi/(1.0*dlength/2.0+1.0) # MHz
        frequencies = np.arange(0,freqhi,freqstep)*1e6 # Hz
        frequencies = np.arange(0,dlength/2+1)*freqstep*1e6

        #Apply window and reduce maximum frequency to acquire downsampled signal
        fb = int(np.floor(lowco/freqstep))
        lb = int(np.floor(hico/freqstep)+1)
        window = np.zeros([1,int(1.0*dlength/2.0+1.0),1])
        window[0,fb:lb+1,0]=1

        #ospow0=np.abs(spec[:,0])*np.abs(spec[:,0])
        #ospow1=np.abs(spec[:,1])*np.abs(spec[:,1])
        #power[j]=np.array([np.sum(pow0[fb:lb+1]),np.sum(pow1[fb:lb+1])])/(dlength/2.)*tstep
        #filteredpower[j]=np.array([np.sum(ospow0[fb:lb+1]),np.sum(ospow1[fb:lb+1])])/(dlength/2.)*tstep

        # assume that simulated time resolution is higher than LOFAR time resolution (t_step=5 ns)
        maxfreqbin= int(np.floor(tstep/(res*1e-9) * dlength/2.)+1)
        shortspec=np.array([spec[0:maxfreqbin,0]*window[0,0:maxfreqbin,0],spec[0:maxfreqbin,1]*window[0,0:maxfreqbin,0]])
        filt=np.fft.irfft(shortspec, axis=-1)
        # after downsampling, renormalize the signal!
        dlength_new=filt.shape[1]
        filt=filt*1.0*dlength_new/dlength
    
        want=np.zeros([2,dlength])
        result = np.zeros(want.shape)
        result[:filt.shape[0],:filt.shape[1]] = filt
        return_signal[j]=result.T

        times_return[j]=times_up

    return return_signal,times_return*1e-9
