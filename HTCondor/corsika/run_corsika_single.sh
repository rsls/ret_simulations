#!/bin/bash

#8 arguments to run the corsika shower
#Arguments = $(THETA_DIST) $(THETA_BIN) $(ENERGY_BIN) $(PRIM_PART) $(RUN_NUMBER) $(DET_SEASON) $(DET_TIME) $(DET_LOCATION)
#Numbering = ${1}          ${2}         ${3}          ${4}         ${5}          ${6}          ${7}         ${8}        
#All angles should be in degrees and energy in GeV

hold_dir="/user/rstanley/CORSIKA/QGSJET/reruns/${1}_${8}_${4}_${3}_${2}_${6}_${7}_${5}/"
output_dir="/pnfs/iihe/radar/corsika/qgsjet/single_runs/${1}_${8}_${4}_${3}_${2}_${6}_${7}_${5}/"
temp_dir="/scratch/rstanley/${5}${2}${4}/"

input_file="${temp_dir}/RUN${5}.inp"
list_file="${temp_dir}/SIM${5}.list"
reas_file="${temp_dir}/SIM${5}.reas"

rm -rf ${temp_dir}
mkdir -p ${temp_dir}

cp "${hold_dir}/RUN${5}.inp" ${input_file}
cp "${hold_dir}/SIM${5}.list" ${list_file}
cp "${hold_dir}/SIM${5}.reas" ${reas_file}

cd /software/corsika/corsika-77402/run/
echo Starting CORSIKA

./corsika77402Linux_QGSII_urqmd_thin_coreas < ${input_file}

cd ${temp_dir}

rm ${input_file} 
rm ${list_file} 
rm ${reas_file}

mv * ${output_dir}

rm -rf ${temp_dir}
