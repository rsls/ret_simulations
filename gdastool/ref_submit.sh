#!/bin/bash
#PBS -N mean_ref
eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh`
time python /user/rstanley/CORSIKA/GDAS/mean_ref_general.py > /user/rstanley/CORSIKA/GDAS/output/mean_ref_general.txt
exit

