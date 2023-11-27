#!/bin/bash

# Run Phase 1 of Harmonic model: generation of model with ties 

## INPUT PARAMETERS
ASRUNPATH=__path__asRun
ASRUNJOB="padStiffnessPhase2_b"
TERMCMD="xterm -e "
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
