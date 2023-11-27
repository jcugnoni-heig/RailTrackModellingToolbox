#!/bin/bash

## INPUT PARAMETERS
#ASRUNPATH=__path__asRun
ASRUNPATH=__path__asRunImpulse
ASRUNJOB="generateMesh.export"
#TERMCMD="xterm -hold -e"
TERMCMD="xterm -e"

### run ASTER to generate mesh to MED format 
$TERMCMD $ASRUNPATH $ASRUNJOB