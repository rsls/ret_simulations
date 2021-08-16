#!/bin/bash

#Arguments = $(THETA_DIST) $(THETA_BIN) $(ENERGY_BIN) $(PRIM_PART) $(RUN_NUMBER) $(DET_SEASON) $(DET_TIME) $(DET_LOCATION) $(ARRAY_NUMBER) $(RADIUS) $(TRY_NUMBER)
#Numbering = ${1}          ${2}         ${3}          ${4}         ${5}          ${6}          ${7}        ${8}            ${9}            ${10}     ${11}

deposit_dir="/pnfs/iihe/radar/corsika/qgsjet/${1}/${8}/${4}/${3}/${2}/${6}/${7}/deposit/deposit_${9}"

mkdir -p ${deposit_dir}
mkdir -p ${TMPDIR}

cd ${TMPDIR}

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh`

python /user/rstanley/simulations/surface/detector_run.py -r ${5} -d ${1} -z ${2} -e ${3} -p ${4} -s ${6} -t ${7} -l ${8} --arraynumber ${9} --radius ${10} --trynumber ${11} 

cp -rf ${TMPDIR}/deposit* ${deposit_dir}


