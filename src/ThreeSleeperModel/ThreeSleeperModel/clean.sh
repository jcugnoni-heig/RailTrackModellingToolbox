#!/bin/bash

rmFiles=("gen3Sleeper.mesh.med" "temp.mesh.med" "frequencies_b1.txt" "frequencies_b2.txt" "frequencies_b3.txt" "frequencies_b4.txt" "E_bal.csv" "tanD_bal.csv" "E_USP.csv" "tanD_USP.csv" "acGrid.med" "data_b1" "data_b2" "data_b3" "data_b4" "resuHarm_b1.res.med" "resuHarm_b2.res.med" "resuHarm_b3.res.med" "resuHarm_b4.res.med" "resuAcc_b1.res.med" "resuAcc_b2.res.med" "resuAcc_b3.res.med" "resuAcc_b4.res.med" "FRF_concat.txt" "power_concat.txt" "FRF_b1.txt" "FRF_b2.txt" "FRF_b3.txt" "FRF_b4.txt" "power_b1.txt" "power_b2.txt" "power_b3.txt" "power_b4.txt" "E_hard.csv" "E_soft.csv" "tanD_hard.csv" "tanD_soft.csv" "allPressureDataPickled")
rmDirs=("base1" "temp_parameters")

for file in ${rmFiles[*]}; do
 if [[ -f ./$file ]]; then
  rm ./$file
 fi
done

for dir in ${rmDirs[*]}; do
 if [[ -d ./$dir ]]; then
  rm -r ./$dir
 fi
done