#!/bin/bash
#PBS -N gdasin
eval `/cvmfs/icecube.opensciencegrid.org/py2-v3.1.1/setup.sh`
time python /user/rstanley/CORSIKA/GDAS/write_gdasin.py
exit

