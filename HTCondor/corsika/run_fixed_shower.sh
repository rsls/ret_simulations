#!/bin/bash

#13 arguments to run the corsika shower
#Arguments = $(THETA_DIST) $(THETA_BIN) $(ENERGY_BIN) $(PRIM_PART) $(RUN_NUMBER) $(RAND_SEED) $(SHW_ENERGY) $(PRIM_TYPE) $(AZIMUTH_ANGLE) $(ZENITH_ANGLE) $(DET_SEASON) $(DET_TIME) $(DET_LOCATION)
#Numbering = ${1}          ${2}         ${3}          ${4}         ${5}          ${6}         ${7}          ${8}         ${9}             ${10}           ${11}         ${12}       ${13}
#All angles should be in degrees and energy in GeV

input_file="${TMPDIR}/${6}/RUN${5}.inp"
list_file="${TMPDIR}/${6}/SIM${5}.list"
reas_file="${TMPDIR}/${6}/SIM${5}.reas"
geant_file="${TMPDIR}/${6}/RET${5}.txt"


output_dir="/pnfs/iihe/radar/fixed/QGSJET/${1}/${13}/${4}/${3}/${2}/${11}/${12}/"
steering_dir="/pnfs/iihe/radar/fixed/QGSJET/${1}/${13}/${4}/${3}/${2}/${11}/${12}/steering/"
geant_dir="/pnfs/iihe/radar/fixed/QGSJET/${1}/${13}/${4}/${3}/${2}/${11}/${12}/geant/"
temp_dir="${TMPDIR}/${6}/"

echo ${3} ${5}

mkdir -p ${output_dir}
mkdir -p ${steering_dir}
mkdir -p ${geant_dir}

rm -rf ${temp_dir}
mkdir -p ${temp_dir}

eval `/cvmfs/icecube.opensciencegrid.org/py3-v4.0.1/setup.sh`
echo Creating run files

python /user/rstanley/simulations/corsika/write_inp.py -r ${5} -s ${6} -u ${7} -a ${9} -z ${10} -t ${8} -d ${temp_dir} --season ${11} --time ${12} --location ${13} > ${input_file} #**
python /user/rstanley/simulations/corsika/write_fixed_list.py -a ${9} -z ${10} --location ${13}  > ${list_file} #**
python /user/rstanley/simulations/corsika/write_fixed_reas.py -a ${9} -z ${10} -u ${7} --season ${11} --time ${12} --location ${13} > ${reas_file} #**

cd /software/corsika/corsika-77402/run/
echo Starting CORSIKA

./corsika77402Linux_QGSII_urqmd_thin_coreas < ${input_file}

echo Starting GEANT

cd /software/geant4/LORA_simulation/
source /software/geant4/geant4.9.6-install/bin/geant4.sh

./DAT2txt "${TMPDIR}/${6}/DAT${5}" "${TMPDIR}/${6}/DAT${5}.txt"
./LORA_simulation "${TMPDIR}/${6}/DAT${5}.txt" ${geant_file}

cd ${TMPDIR}/${6}/
rm ${TMPDIR}/${6}/DAT${5}.txt

cp -rf ${input_file} ${steering_dir}
cp -rf ${list_file} ${steering_dir}
cp -rf ${reas_file} ${steering_dir}
cp -rf ${geant_file} ${geant_dir}
cp -rf * ${output_dir}

rm -rf ${temp_dir}
