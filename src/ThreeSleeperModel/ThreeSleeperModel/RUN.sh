#!/bin/bash

## Parameters
#salome killall
parametersFile=$1
meshesDir=./Meshes/
materialsDir=./Materials_properties/
messagesDir=./messages/
TERMCMD="xterm -e"
TERMCMDHOLD="xterm -hold  -e"
ASRUNPATH=__path__asRun
PYTHONPATH=__path__python
SALOMEPATH=__path__salome

#########################################################################################
# FUNCTIONS
#########################################################################################

RemoveFiles() {
 rmFiles=("frequencies_b1.txt" "frequencies_b2.txt" "frequencies_b3.txt" "frequencies_b4.txt" "E_bal.csv" "tanD_bal.csv" "E_USP.csv" "tanD_USP.csv" "acGrid.med" "data_b1" "data_b2" "data_b3" "data_b4" "resuHarm_b1.res.med" "resuHarm_b2.res.med" "resuHarm_b3.res.med" "resuHarm_b4.res.med" "resuAcc_b1.res.med" "resuAcc_b2.res.med" "resuAcc_b3.res.med" "resuAcc_b4.res.med" "FRF_concat.txt" "power_concat.txt" "FRF_b1.txt" "FRF_b2.txt" "FRF_b3.txt" "FRF_b4.txt" "power_b1.txt" "power_b2.txt" "power_b3.txt" "power_b4.txt" "E_hard.csv" "E_soft.csv" "tanD_hard.csv" "tanD_soft.csv" "allPressureDataPickled")
 for file in ${rmFiles[*]}; do
  if [[ -f ./$file ]]; then
   rm ./$file
  fi
 done
}

#########################################################################################
# READ parametersFile variables
#########################################################################################

if [ "$parametersFile" == "" ]; then
 parametersFile=./parameters.py
fi

echo Running $parametersFile ...

## Get simu name
IFS="'"
line=$(grep 'simuName =' $parametersFile)
read -a strarr <<< "$line"
simuName="${strarr[-1]}"

## Get padMesh name
line=$(grep 'padMesh =' $parametersFile)
read -a strarr <<< "$line"
padMesh="${strarr[-1]}"

## Get pad hard E
line=$(grep 'padHardE =' $parametersFile)
read -a strarr <<< "$line"
padHardE="${strarr[-1]}"

## Get pad soft E
line=$(grep 'padSoftE =' $parametersFile)
read -a strarr <<< "$line"
padSoftE="${strarr[-1]}"

## Get pad hard tanD
line=$(grep 'padHardTanD =' $parametersFile)
read -a strarr <<< "$line"
padHardTanD="${strarr[-1]}"

## Get pad soft tanD
line=$(grep 'padSoftTanD =' $parametersFile)
read -a strarr <<< "$line"
padSoftTanD="${strarr[-1]}"

## Get ballast E
line=$(grep 'ballastE =' $parametersFile)
read -a strarr <<< "$line"
ballastE="${strarr[-1]}"

## Get ballast tanD
line=$(grep 'ballastTanD =' $parametersFile)
read -a strarr <<< "$line"
ballastTanD="${strarr[-1]}"

## Get USP E
line=$(grep 'USPE =' $parametersFile)
read -a strarr <<< "$line"
USPE="${strarr[-1]}"

## Get USP tanD
line=$(grep 'USPTanD =' $parametersFile)
read -a strarr <<< "$line"
USPTanD="${strarr[-1]}"

## Get acoustic mesh name
line=$(grep 'acousticGrid =' $parametersFile)
read -a strarr <<< "$line"
acousticGrid="${strarr[-1]}"

## Get simulation folder where to save everything
line=$(grep 'saveToDir =' $parametersFile)
read -a strarr <<< "$line"
saveToDir="${strarr[-1]}"

## Get run acoustic boolean
line=$(grep 'computeAcoustic =' $parametersFile)
IFS=" "
read -a strarr <<< "$line"
computeAcoustic="${strarr[-1]}"

## Get include USPs boolean
line=$(grep 'includeUSPs =' $parametersFile)
read -a strarr <<< "$line"
includeUSPs="${strarr[-1]}"

## Get nCPUs
line=$(grep 'nCPUs =' $parametersFile)
read -a strarr <<< "$line"
nCPUs="${strarr[-1]}"

## Select the right FE mesh
mesh=$padMesh
#mesh="gen3Sleeper_"$padMesh".mesh.med"

#########################################################################################
# PREPARE FILES FOR SIMULATION
#########################################################################################

## Copy acoustic mesh to ./
if [ ${acousticGrid:${#acousticGrid}-4:4} == ".med" ]; then
 cp $meshesDir$acousticGrid ./acGrid.med
else
 cp $meshesDir$acousticGrid".med" ./acGrid.med
fi

## Copy FE mesh to ./ as "temp.mesh.med"
cp $meshesDir$mesh ./temp.mesh.med

## Include USPs to the standard FE mesh in ./ if required. 
## Note that ./genUSP.py generates ./Meshes/USPs.med with custom parameters on top of the file
if [ $includeUSPs == True ]; then
 $TERMCMD "$SALOMEPATH -t ./gen3sleepersUSP.py"
fi

## Check if phase 1 needs to be run
## temp is the mesh for next simu. gen3Sleeper is the mesh of last simu
runPhase1=True

## NOTE uncomment the following line to avoid recomputing the phase 1 (model buildup) when not necessary
#if [[ $(stat -c%s "./temp.mesh.med") -eq $(stat -c%s "./gen3Sleeper.mesh.med") ]]; then
# runPhase1=False
#else
# runPhase1=True
#fi

cp "./temp.mesh.med" "./gen3Sleeper.mesh.med"
rm "./temp.mesh.med"
# gen3Sleeper.mesh.med is now the FE mesh file for the coming simu

## Update export files with parametersFile path
if [ $runPhase1 == True ]; then
 sed -i "s!F libr .*\.py D *2!F libr ${parametersFile} D  2!" ./harmoPhase1.export
fi
sed -i "s!F libr .*\.py D *2!F libr ${parametersFile} D  2!" ./harmoPhase2_b1.export
sed -i "s!F libr .*\.py D *2!F libr ${parametersFile} D  2!" ./harmoPhase2_b2.export
sed -i "s!F libr .*\.py D *2!F libr ${parametersFile} D  2!" ./harmoPhase2_b3.export
sed -i "s!F libr .*\.py D *2!F libr ${parametersFile} D  2!" ./harmoPhase2_b4.export

## Select the right materials properties files and copy them to ./
cp $USPE ./E_USP.csv
cp $USPTanD ./tanD_USP.csv
cp $ballastE ./E_bal.csv
cp $ballastTanD ./tanD_bal.csv
## Check if for pads, a file or a material name is given
if [[ -f $padHardE ]]; then
 cp $padHardE ./E_hard.csv
 cp $padHardTanD ./tanD_hard.csv
else
 cp $materialsDir"E_"$padHardE".csv" ./E_hard.csv
 cp $materialsDir"tanD_"$padHardTanD".csv" ./tanD_hard.csv
fi

if [[ -f $padSoftE ]]; then
 cp $padSoftE ./E_soft.csv
 cp $padSoftTanD ./tanD_soft.csv
else
 cp $materialsDir"E_"$padSoftE".csv" ./E_soft.csv
 cp $materialsDir"tanD_"$padSoftTanD".csv" ./tanD_soft.csv
fi

#########################################################################################
# RUN SIMULATION
#########################################################################################

error=False
lastLine1="0"
lastLine2="0"
lastLine3="0"

## Run Phase 1 of Harmonic model: generation of model with ties
#runPhase1=True
if [ $runPhase1 == True ]; then
 ASRUNJOB1="harmoPhase1.export"
 t=0
 count=0
 while [ $t -le 5 ]  && [ $count -le 5 ]; do
  SECONDS=0

  $TERMCMD $ASRUNPATH $ASRUNJOB1
  t=$SECONDS
  count=$(( $count + 1 ))
 done
 lastLine1=$(tail -1 $messagesDir"harmo1.mess")
 echo $simuName "Phase 1 exit code :" $lastLine1
else
 echo Phase 1 from previous simulation could be used
fi

if [ "${lastLine1: -1}" != "0" ]; then
  echo "Error in simulation..."
  RemoveFiles
  exit
fi

## Run Phase 2 of Harmonic model: vibro(-acoustic) computation
ASRUNJOB2="harmoPhase2_b"
t=0
n=0
count=0
while [ $t -le 5 ]  && [ $count -le 5 ]; do
 n=$((n+1))
 if (( n>3 )); then
  lastLine2=$(tail -1 $messagesDir"harmo2_b1.mess")
  echo $simuName "Phase 2 exit code :" $lastLine2

  if [ "${lastLine2: -1}" != "0" ]; then
    echo "Error in simulation..."
    RemoveFiles
    exit
  fi
  
 fi
 
 SECONDS=0
 count=$(( $count + 1 )) 
 
 for (( i=1; i<=$nCPUs; i++ ))
 do
  myCommand="$TERMCMD $ASRUNPATH $ASRUNJOB2$i.export &"
  eval $myCommand
  myString="pid""$i""=""\$!"
  eval $myString
 done

 for (( i=1; i<=$nCPUs; i++ ))
 do
  myCommand="wait ""$""pid"$i
  eval $myCommand
 done
 
 #wait $pid1
 #wait $pid2
 #wait $pid3
 #wait $pid4
 t=$SECONDS
done

lastLine3=$(tail -1 $messagesDir"harmo2_b1.mess")
echo $simuName "Phase 2 exit code :" $lastLine3

if [ "${lastLine3: -1}" != "0" ]; then
  echo "Error in simulation..."
  RemoveFiles
  exit
fi


#########################################################################################
# POST-PROCESSING
#########################################################################################

## Concatenate FRF and power files
cat FRF_b1.txt > FRF_concat.txt
for (( i=2; i<=$nCPUs; i++))
do
 myCommand="tail -n+2 FRF_b"$i".txt >> FRF_concat.txt"
 eval $myCommand
done
#tail -n+2 FRF_b2.txt >> FRF_concat.txt
#tail -n+2 FRF_b3.txt >> FRF_concat.txt
#tail -n+2 FRF_b4.txt >> FRF_concat.txt

if [ $computeAcoustic == "True" ]; then
 cat power_b1.txt > power_concat.txt
 for (( i=2; i<=$nCPUs; i++))
 do
  myCommand="tail -n+3 power_b"$i".txt >> power_concat.txt"
  eval $myCommand
 done

# tail -n+3 power_b2.txt >> power_concat.txt
 #tail -n+3 power_b3.txt >> power_concat.txt
 #tail -n+3 power_b4.txt >> power_concat.txt
 
 # Pickle all pressure data into one file, compute Lw, write it on top of power_concat.txt
 $PYTHONPATH ./finalPostPro.py 
fi

#########################################################################################
# SAVE AND REMOVE FILES FROM MAIN DIRECTORY (./)
#########################################################################################
copyFiles=("resuHarm_b1.res.med" "resuHarm_b2.res.med" "resuHarm_b3.res.med" "resuHarm_b4.res.med" "FRF_concat.txt")
if [ $computeAcoustic == "True" ]; then
 copyFiles+=("resuAcc_b1.res.med" "resuAcc_b2.res.med" "resuAcc_b3.res.med" "resuAcc_b4.res.med" "power_concat.txt" "allPressureDataPickled")
fi

if [[ ! -d $saveToDir$simuName/ ]]; then
 mkdir -p $saveToDir$simuName/
fi

cp $parametersFile $saveToDir$simuName/parameters.py
for file in ${copyFiles[*]}; do
 if [[ -f ./$file ]]; then
  cp ./$file $saveToDir$simuName/$file
 fi
done

RemoveFiles

echo End of simulation
