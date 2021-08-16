#!/bin/bash

#Arguments = $(THETA_DIST) $(THETA_BIN) $(ENERGY_BIN) $(PRIM_PART) $(RUN_NUMBER) $(DET_SEASON) $(DET_TIME) $(DET_LOCATION)
#Numbering = ${1}          ${2}         ${3}          ${4}         ${5}          ${6}          ${7}        ${8}

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh`

python /user/rstanley/simulations/radio/get_footprint.py -r ${5} -d ${1} -z ${2} -e ${3} -p ${4} -s ${6} -t ${7} -l ${8}
#**
