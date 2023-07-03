#!/bin/bash

## INPUT PARAMETERS
#ASRUNPATH=/opt/SalomeMeca/V2019_univ/tools/Code_aster_frontend-20190/bin/as_run
ASRUNPATH=/opt/aster/bin/as_run
ASRUNJOB="generateMesh.export"
#TERMCMD="xterm -hold -e"
TERMCMD="xterm -e"

### run ASTER to generate mesh to MED format 
$TERMCMD $ASRUNPATH $ASRUNJOB