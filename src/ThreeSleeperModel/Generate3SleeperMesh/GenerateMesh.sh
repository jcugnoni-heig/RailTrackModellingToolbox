#!/bin/bash

# CONVERT ABAQUS MESH TO ASTER 

## INPUT PARAMETERS
ASRUNPATH=__path__asRun
ASRUNJOB="gen3sleeper.export"
### run ASTER to generate mesh to MED format 
$ASRUNPATH $ASRUNJOB
