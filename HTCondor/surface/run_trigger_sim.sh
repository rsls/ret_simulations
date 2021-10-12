#!/bin/bash

#Arguments = $(THETA_DIST) $(PRIM_PART) $(RUN_NUMBER) $(DET_SEASON) $(DET_TIME) $(DET_LOCATION) $(ARRAY_NUMBER) $(TRY_NUMBER) $(THRESH)
#Numbering = ${1}          ${2}         ${3}          ${4}          ${5}        ${6}            ${7}            ${8}          ${9}

trigger_dir="/user/rstanley/detector/trigger/"
shower_dir="/user/rstanley/detector/shower_info/"

mkdir -p ${TMPDIR}

cd ${TMPDIR}

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh`

python /user/rstanley/simulations/surface/detector_trigger.py -r ${3} -d ${1} -p ${2} -s ${4} -t ${5} -l ${6} --arraynumber ${7} --threshold ${9} --trynumber ${8} 

cp -rf ${TMPDIR}/shower_info_*.pkl ${shower_dir}
cp -rf ${TMPDIR}/trigger_*_eff_*.csv ${trigger_dir}

rm -rf ${TMPDIR}
