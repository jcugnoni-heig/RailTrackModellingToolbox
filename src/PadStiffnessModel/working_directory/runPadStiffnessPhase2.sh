#!/bin/bash

# Run Phase 1 of Harmonic model: generation of model with ties 

## INPUT PARAMETERS
ASRUNPATH=/opt/SalomeMeca/V2019_univ/tools/Code_aster_frontend-20190/bin/as_run
ASRUNJOB="padStiffnessPhase2_b"
TERMCMD="xterm -hold -e "
### run ASTER to generate mesh to MED format 
#for i in {1..4}
#do
#   $TERMCMD $ASRUNPATH $ASRUNJOB$i.export &
#done

for i in {1..4}
do
 myCommand="$TERMCMD $ASRUNPATH $ASRUNJOB$i.export &"
 eval $myCommand
 myString="pid""$i""=""\$!"
 eval $myString
done

for i in {1..4}
do
 myCommand="wait ""$""pid"$i
 eval $myCommand
done
