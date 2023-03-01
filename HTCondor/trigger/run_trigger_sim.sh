#!/bin/bash

#Arguments = $(THETA_DIST) $(PRIM_PART) $(RUN_NUMBER) $(DET_SEASON) $(DET_TIME) $(DET_LOCATION) $(ARRAY_NUMBER) $(TRY_NUMBER) $(THRESH) $(GEN_NUMBER) $(ENERGY_BIN) $(STATION_REQ) $(SCINT)
#Numbering = ${1}          ${2}         ${3}          ${4}          ${5}        ${6}            ${7}            ${8}          ${9}      ${10}         ${11}         ${12}          ${13}

trigger_info_dir="/user/rstanley/detector/trigger_info/"
shower_dir="/user/rstanley/detector/shower_info/"

mkdir -p ${TMPDIR}

cd ${TMPDIR}

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh`

python /user/rstanley/simulations/trigger/detector_trigger.py -r ${3} -e ${11} -d ${1} -p ${2} -s ${4} -t ${5} -l ${6} --gennumber ${10} --arraynumber ${7} --threshold ${9} --trynumber ${8} --stationreq ${12} --scint ${13}


