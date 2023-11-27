#!/bin/bash

# Run Phase 1 of Harmonic model: generation of model with ties 

## INPUT PARAMETERS
ASRUNPATH=__path__asRun
ASRUNJOB="padStiffnessPhase1.export"
TERMCMD="xterm -e "
### run ASTER to generate mesh to MED format 
$TERMCMD $ASRUNPATH $ASRUNJOB
