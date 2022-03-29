#!/bin/bash

#Arguments = $(THETA_DIST) $(THETA_BIN) $(ENERGY_BIN) $(PRIM_PART) $(RUN_NUMBER) $(DET_SEASON) $(DET_TIME) $(DET_LOCATION) $(SCINT) $(GEN_NUMBER) $(ARRAY_NUMBER) $(RADIUS) $(TRY_NUMBER)
#Numbering = ${1}          ${2}         ${3}          ${4}         ${5}          ${6}          ${7}        ${8}            ${9}     ${10}         ${11}           ${12}     ${13}

deposit_dir="/pnfs/iihe/radar/corsika/QGSJET/${1}/${8}/${4}/${3}/${2}/${6}/${7}/deposit/deposit_${10}_${11}"

mkdir -p ${deposit_dir}
mkdir -p ${TMPDIR}

cd ${TMPDIR}

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh`

python /user/rstanley/simulations/surface/detector_run.py -r ${5} -d ${1} -z ${2} -e ${3} -p ${4} -s ${6} -t ${7} -l ${8} --scint ${9} --gennumber ${10} --arraynumber ${11} --radius ${12} --trynumber ${13} 

cp -rf ${TMPDIR}/DEP*.txt ${deposit_dir}


