#!/bin/bash

# CONVERT ABAQUS MESH TO ASTER 

## INPUT PARAMETERS
ASRUNPATH=/opt/SalomeMeca/V2019_univ/tools/Code_aster_frontend-20190/bin/as_run
ASRUNJOB="gen3sleeper.export"
### run ASTER to generate mesh to MED format 
$ASRUNPATH $ASRUNJOB
